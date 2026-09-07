"""Approval readiness through the public workspace CLI, not internal mocks."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "arsenal.py"


class GateCliTests(unittest.TestCase):
    """Gate results must agree with approval for the same workspace revision."""

    def setUp(self):
        """Run commands from an unrelated directory with an isolated workspace."""

        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.workspace = self.root / "demo.arsenal.json"
        self.run_command("init", "--project", "demo")

    def run_command(self, command, *options, exit_code=0):
        """Invoke the real CLI and check its JSON and process contract."""

        result = subprocess.run(
            [
                sys.executable, str(SCRIPT), command,
                "--workspace", str(self.workspace), *options,
            ],
            cwd=self.root,
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
        self.assertEqual(result.returncode, exit_code, result.stdout + result.stderr)
        self.assertEqual(result.stderr, "")
        return json.loads(result.stdout)

    def apply(self, phase):
        """Apply a real phase payload through the CLI."""

        payload = self.root / "phase.json"
        payload.write_text(
            json.dumps({"summary": phase, "data": {"phase": phase}}),
            encoding="utf-8",
        )
        return self.run_command("apply", "--phase", phase, "--input", str(payload))

    def review(self, phase, reviews=None):
        """Submit real reviews, defaulting to two independent clean reviews."""

        if reviews is None:
            reviews = [
                {"reviewer": "marketer", "issues": []},
                {"reviewer": "strategist", "issues": []},
            ]
        payload = self.root / "reviews.json"
        payload.write_text(json.dumps(reviews), encoding="utf-8")
        return self.run_command("add-review", "--phase", phase, "--input", str(payload))

    def prepare(self, *phases):
        """Build approved predecessors using only supported transitions."""

        for phase in phases:
            self.apply(phase)
            self.review(phase)
            self.assert_ready_and_approve(phase)

    def edit_phase(self, phase, changes):
        """Deliberately change the on-disk contract to exercise drift guards."""

        state = json.loads(self.workspace.read_text(encoding="utf-8"))
        state["tracks"]["offer"]["phases"][phase].update(changes)
        self.workspace.write_text(json.dumps(state), encoding="utf-8")

    def assert_blocked(self, phase, *codes):
        """Blocked commands agree, remain deterministic and never write state."""

        before = self.workspace.read_bytes()
        gate = self.run_command("gate", "--phase", phase, exit_code=1)
        self.assertFalse(gate["can_approve"])
        self.assertTrue(set(codes) <= {item["code"] for item in gate["blockers"]})
        self.assertEqual(self.workspace.read_bytes(), before)
        self.assertEqual(
            self.run_command("gate", "--phase", phase, exit_code=1), gate
        )
        rejected = self.run_command("approve", "--phase", phase, exit_code=2)
        self.assertEqual(rejected["error"], gate["blockers"][0]["message"])
        self.assertEqual(self.workspace.read_bytes(), before)
        return gate

    def assert_ready_and_approve(self, phase):
        """A read-only passing gate predicts the actual approval transition."""

        before = self.workspace.read_bytes()
        gate = self.run_command("gate", "--phase", phase)
        self.assertTrue(gate["can_approve"])
        self.assertTrue(gate["review_gate_passed"])
        self.assertEqual(gate["blockers"], [])
        self.assertEqual(self.workspace.read_bytes(), before)
        self.assertTrue(self.run_command("approve", "--phase", phase)["ok"])

    def test_upstream_change_blocks_gate_without_erasing_review_history(self):
        """Clean historical reviews cannot make a stale phase approval-ready."""

        self.prepare("discovery", "market", "pricing")
        self.apply("market")
        gate = self.assert_blocked(
            "pricing", "predecessors-unapproved", "stale-phase", "upstream-revision-drift"
        )
        self.assertTrue(gate["review_requirement_met"])
        self.assertTrue(gate["review_gate_passed"])
        self.assertEqual(gate["review_count"], 2)

    def test_only_reviewed_current_work_is_ready_for_approval(self):
        """Untouched, draft and already-approved phases are not pending approval."""

        self.assert_blocked("discovery", "untouched-phase", "reviewers-required")
        self.apply("discovery")
        self.assert_blocked("discovery", "phase-not-in-review", "reviewers-required")
        self.review("discovery")
        self.edit_phase("discovery", {"status": "draft"})
        gate = self.assert_blocked("discovery", "phase-not-in-review")
        self.assertTrue(gate["review_gate_passed"])
        self.apply("discovery")
        self.review("discovery")
        self.assert_ready_and_approve("discovery")
        gate = self.assert_blocked("discovery", "already-approved")
        self.assertTrue(gate["review_gate_passed"])
        self.assertTrue(self.run_command("validate")["ok"])

    def test_unapproved_predecessor_blocks_otherwise_clean_reviews(self):
        """Predecessor approval matters even when recorded revisions still match."""

        self.prepare("discovery")
        self.apply("market")
        self.review("market")
        self.edit_phase("discovery", {"status": "in_review", "approved_at": None})
        gate = self.assert_blocked("market", "predecessors-unapproved")
        self.assertEqual(len(gate["blockers"]), 1)
        self.assertTrue(gate["review_gate_passed"])

    def test_manual_drift_blocks_reviewed_work(self):
        """Revision drift, data edits and a retained stale reason each block approval."""

        self.prepare("discovery")
        self.apply("market")
        self.review("market")
        original = self.workspace.read_bytes()
        cases = [
            ("discovery", {"revision": 9}, "upstream-revision-drift"),
            ("market", {"data": {"changed": True}}, "phase-data-drift"),
            ("market", {"stale_reason": "Upstream decision changed"}, "stale-phase"),
        ]
        for phase, changes, code in cases:
            with self.subTest(code=code):
                self.workspace.write_bytes(original)
                self.edit_phase(phase, changes)
                gate = self.assert_blocked("market", code)
                self.assertEqual(len(gate["blockers"]), 1)
                self.assertTrue(gate["review_gate_passed"])

    def test_recovery_requires_fresh_downstream_content_and_reviews(self):
        """Re-approving the source alone cannot revive stale downstream reviews."""

        self.prepare("discovery", "market", "pricing")
        self.apply("market")
        self.review("market")
        self.assert_ready_and_approve("market")
        self.assert_blocked("pricing", "stale-phase", "upstream-revision-drift")
        self.apply("pricing")
        gate = self.assert_blocked("pricing", "reviewers-required")
        self.assertEqual(gate["review_count"], 0)
        self.assertFalse(gate["review_gate_passed"])
        self.review("pricing")
        self.assert_ready_and_approve("pricing")
        self.prepare("value", "stack", "enhancement")
        self.assert_blocked("enhancement", "already-approved")
        self.assertTrue(self.run_command("validate")["ok"])

    def test_duplicate_reviewer_cannot_satisfy_quorum(self):
        """Multiple submissions from one identity still need an independent reviewer."""

        self.apply("discovery")
        self.review("discovery", [{"reviewer": "marketer", "issues": []}])
        self.assert_blocked("discovery", "reviewers-required")
        self.review("discovery", [{"reviewer": "marketer", "issues": []}])
        gate = self.assert_blocked("discovery", "reviewers-required")
        self.assertFalse(gate["review_gate_passed"])
        self.review("discovery", [{"reviewer": "strategist", "issues": []}])
        self.assert_ready_and_approve("discovery")

    def test_explicit_risk_acceptance_unblocks_only_current_revision(self):
        """A critical finding requires an explicit acceptance again after re-apply."""

        reviews = [
            {"reviewer": "marketer", "issues": [{"issue_key": "buyer-too-broad", "blocking": True}]},
            {"reviewer": "strategist", "issues": []},
        ]
        self.apply("discovery")
        self.review("discovery", reviews)
        gate = self.assert_blocked("discovery", "critical-issues")
        self.assertTrue(gate["review_requirement_met"])
        self.assertFalse(gate["review_gate_passed"])
        result = self.run_command(
            "accept-risk", "--phase", "discovery", "--issue-key", "buyer-too-broad",
            "--reason", "Pilot will test a narrower segment", "--confirmed-by", "user",
        )
        self.assertTrue(result["gate"]["can_approve"])
        self.assert_ready_and_approve("discovery")
        self.apply("discovery")
        self.review("discovery", reviews)
        gate = self.assert_blocked("discovery", "critical-issues")
        self.assertFalse(gate["issues"][0]["accepted_risk"])

    def test_unknown_phase_is_an_error_not_a_readiness_result(self):
        """An invalid phase remains a domain error with no state changes."""

        before = self.workspace.read_bytes()
        gate = self.run_command("gate", "--phase", "unknown", exit_code=2)
        approved = self.run_command("approve", "--phase", "unknown", exit_code=2)
        self.assertEqual(gate, approved)
        self.assertEqual(gate, {"ok": False, "error": "Unknown phase offer:unknown"})
        self.assertEqual(self.workspace.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
