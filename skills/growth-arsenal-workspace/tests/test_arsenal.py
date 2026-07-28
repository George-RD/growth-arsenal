"""Unit tests for the Growth Arsenal workspace lifecycle."""

import importlib.util
import json
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "arsenal.py"
spec = importlib.util.spec_from_file_location("arsenal", SCRIPT)
arsenal = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(arsenal)

import render as renderer


class WorkspaceTests(unittest.TestCase):
    """Exercise state transitions, gates, invalidation and deterministic output."""

    def setUp(self):
        """Create an isolated workspace for each test."""

        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.workspace = self.root / "demo.arsenal.json"
        args = Namespace(
            workspace=str(self.workspace),
            project="demo",
            name="Demo",
            locale="en-GB",
            currency="GBP",
            spelling="british",
            timezone="Europe/London",
            force=False,
        )
        arsenal.command_init(args)

    def tearDown(self):
        """Remove the isolated workspace."""

        self.temp.cleanup()

    def write_payload(self, name, payload):
        """Write a JSON input file for a command."""

        path = self.root / name
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def apply(self, phase, payload):
        """Apply an offer-track phase payload."""

        path = self.write_payload(f"{phase}.json", payload)
        return arsenal.command_apply(
            Namespace(
                workspace=str(self.workspace),
                track="offer",
                phase=phase,
                input=str(path),
            )
        )

    def add_reviews(self, phase, reviews):
        """Attach review payloads to an offer-track phase."""

        path = self.write_payload(f"{phase}-reviews.json", reviews)
        return arsenal.command_add_review(
            Namespace(
                workspace=str(self.workspace),
                track="offer",
                phase=phase,
                input=str(path),
            )
        )

    def approve(self, phase):
        """Approve an offer-track phase."""

        return arsenal.command_approve(
            Namespace(workspace=str(self.workspace), track="offer", phase=phase)
        )

    def clean_reviews(self):
        """Return two independent no-issue reviews."""

        return [
            {"reviewer": "marketer", "score": 8, "issues": []},
            {"reviewer": "strategist", "score": 8, "issues": []},
        ]

    def review_and_approve(self, phase):
        """Attach clean reviews and approve the phase."""

        self.add_reviews(phase, self.clean_reviews())
        return self.approve(phase)

    def apply_approve_sequence(self, phases):
        """Apply and approve phases in dependency order."""

        for phase in phases:
            self.apply(phase, {"summary": phase, "data": {"phase": phase}})
            self.review_and_approve(phase)

    def test_approval_requires_two_independent_reviews(self):
        """An applied phase cannot pass with zero or one distinct reviewer."""

        self.apply("discovery", {"summary": "A business", "data": {}})
        with self.assertRaises(arsenal.ArsenalError):
            self.approve("discovery")
        gate = self.add_reviews(
            "discovery",
            [{"reviewer": "marketer", "score": 8, "issues": []}],
        )["gate"]
        self.assertFalse(gate["can_approve"])
        self.assertFalse(gate["review_requirement_met"])

    def test_consensus_gate_requires_two_distinct_reviewers(self):
        """The same issue from two reviewers becomes critical."""

        self.apply("discovery", {"summary": "A business", "data": {}})
        reviews = [
            {
                "reviewer": "marketer",
                "score": 6,
                "issues": [
                    {"issue_key": "buyer-too-broad", "finding": "Buyer is broad"}
                ],
            },
            {
                "reviewer": "strategist",
                "score": 5,
                "issues": [
                    {
                        "issue_key": "buyer-too-broad",
                        "finding": "Acquisition cannot be targeted",
                    }
                ],
            },
        ]
        result = self.add_reviews("discovery", reviews)
        self.assertFalse(result["gate"]["can_approve"])
        self.assertEqual(result["gate"]["critical_open"][0]["consensus_count"], 2)

    def test_explicit_risk_acceptance_is_revision_scoped(self):
        """An old acceptance cannot unblock the same issue in a new revision."""

        self.apply("discovery", {"summary": "A business", "data": {}})
        reviews = [
            {
                "reviewer": "marketer",
                "issues": [{"issue_key": "buyer-too-broad", "finding": "Broad"}],
            },
            {
                "reviewer": "strategist",
                "issues": [{"issue_key": "buyer-too-broad", "finding": "Broad"}],
            },
        ]
        self.add_reviews("discovery", reviews)
        result = arsenal.command_accept_risk(
            Namespace(
                workspace=str(self.workspace),
                track="offer",
                phase="discovery",
                issue_key="buyer-too-broad",
                reason="Pilot will narrow the market",
                confirmed_by="user",
            )
        )
        self.assertTrue(result["gate"]["can_approve"])
        self.approve("discovery")

        self.apply(
            "discovery",
            {"summary": "A revised business", "data": {"revision": 2}},
        )
        result = self.add_reviews("discovery", reviews)
        self.assertFalse(result["gate"]["can_approve"])
        self.assertFalse(result["gate"]["issues"][0]["accepted_risk"])

    def test_apply_requires_approved_predecessors(self):
        """Later phases cannot be applied before the declared workflow order."""

        with self.assertRaises(arsenal.ArsenalError):
            self.apply("pricing", {"summary": "Skipped ahead", "data": {}})

    def test_upstream_change_marks_downstream_stale(self):
        """Changing an approved upstream phase invalidates populated dependants."""

        self.apply_approve_sequence(("discovery", "market", "pricing"))
        result = self.apply(
            "market",
            {"summary": "changed", "data": {"phase": "market", "changed": True}},
        )
        self.assertIn("pricing", result["invalidated"])
        state = arsenal.load_state(self.workspace)
        self.assertEqual(
            state["tracks"]["offer"]["phases"]["pricing"]["status"],
            "stale",
        )

    def test_stale_phase_cannot_be_reapproved_unchanged(self):
        """Approval cannot clear stale state without a fresh apply and reviews."""

        self.apply_approve_sequence(("discovery", "market", "pricing"))
        self.apply(
            "market",
            {"summary": "changed", "data": {"phase": "market", "changed": True}},
        )
        with self.assertRaises(arsenal.ArsenalError):
            self.approve("pricing")

    def test_whitespace_only_reviewer_is_rejected(self):
        """Reviewer identities must survive trimming."""

        self.apply("discovery", {"summary": "A business", "data": {}})
        with self.assertRaises(arsenal.ArsenalError):
            self.add_reviews("discovery", [{"reviewer": "   ", "issues": []}])

    def test_template_substitution_does_not_rescan_inserted_values(self):
        """User text resembling another placeholder remains literal."""

        template_path = (
            Path(renderer.__file__).resolve().parents[1]
            / "assets"
            / "templates"
            / "collision-test.html"
        )
        template_path.write_text("{{A}}|{{B}}", encoding="utf-8")
        try:
            self.assertEqual(
                renderer.template(
                    "collision-test.html",
                    {"A": "{{B}}", "B": "replacement"},
                ),
                "{{B}}|replacement",
            )
        finally:
            template_path.unlink(missing_ok=True)

    def test_markdown_json_uses_a_safe_fence(self):
        """Triple backticks inside JSON cannot terminate the generated fence."""

        rendered = renderer.fenced_json({"copy": "before ``` after"})
        self.assertTrue(rendered.startswith("````json\n"))
        self.assertTrue(rendered.endswith("\n````"))

    def test_render_is_self_contained_and_escapes_content(self):
        """Reports escape user HTML and contain no remote font dependency."""

        self.apply(
            "discovery",
            {"summary": "<script>alert(1)</script>", "data": {}},
        )
        self.review_and_approve("discovery")
        result = arsenal.command_render(
            Namespace(
                workspace=str(self.workspace),
                surface="all",
                output_dir=str(self.root),
                allow_invalid=False,
            )
        )
        self.assertEqual(len(result["outputs"]), 6)
        progress = (self.root / "demo-workshop-progress.html").read_text(
            encoding="utf-8"
        )
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", progress)
        self.assertNotIn("fonts.googleapis.com", progress)
        self.assertIn("growth-arsenal declarative workspace", progress)
        self.assertNotIn("{{SCRIPT}}", progress)
        self.assertNotIn("{{NAV}}", progress)

    def test_validate_detects_manual_revision_drift(self):
        """Manual upstream revision edits invalidate approved dependants."""

        self.apply_approve_sequence(("discovery", "market"))
        state = arsenal.load_state(self.workspace)
        state["tracks"]["offer"]["phases"]["discovery"]["revision"] = 9
        arsenal.atomic_write_text(self.workspace, json.dumps(state))
        findings = arsenal.validate_state(arsenal.load_state(self.workspace))
        self.assertTrue(
            any(item["code"] == "stale-offer-market" for item in findings)
        )


if __name__ == "__main__":
    unittest.main()
