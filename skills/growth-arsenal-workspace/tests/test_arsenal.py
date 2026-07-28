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


class WorkspaceTests(unittest.TestCase):
    def setUp(self):
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
        self.temp.cleanup()

    def write_payload(self, name, payload):
        path = self.root / name
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def apply(self, phase, payload):
        path = self.write_payload(f"{phase}.json", payload)
        return arsenal.command_apply(Namespace(workspace=str(self.workspace), track="offer", phase=phase, input=str(path)))

    def add_reviews(self, phase, reviews):
        path = self.write_payload(f"{phase}-reviews.json", reviews)
        return arsenal.command_add_review(Namespace(workspace=str(self.workspace), track="offer", phase=phase, input=str(path)))

    def approve(self, phase):
        return arsenal.command_approve(Namespace(workspace=str(self.workspace), track="offer", phase=phase))

    def test_consensus_gate_requires_two_distinct_reviewers(self):
        self.apply("discovery", {"summary": "A business", "data": {}})
        reviews = [
            {"reviewer": "marketer", "score": 6, "issues": [{"issue_key": "buyer-too-broad", "finding": "Buyer is broad"}]},
            {"reviewer": "strategist", "score": 5, "issues": [{"issue_key": "buyer-too-broad", "finding": "Acquisition cannot be targeted"}]},
        ]
        result = self.add_reviews("discovery", reviews)
        self.assertFalse(result["gate"]["can_approve"])
        self.assertEqual(result["gate"]["critical_open"][0]["consensus_count"], 2)

    def test_explicit_risk_acceptance_unblocks_without_erasing_issue(self):
        self.apply("discovery", {"summary": "A business", "data": {}})
        self.add_reviews(
            "discovery",
            [
                {"reviewer": "marketer", "issues": [{"issue_key": "buyer-too-broad", "finding": "Broad"}]},
                {"reviewer": "strategist", "issues": [{"issue_key": "buyer-too-broad", "finding": "Broad"}]},
            ],
        )
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
        self.assertTrue(result["gate"]["issues"][0]["accepted_risk"])
        self.approve("discovery")

    def test_upstream_change_marks_downstream_stale(self):
        for phase in ("discovery", "market", "pricing"):
            self.apply(phase, {"summary": phase, "data": {"phase": phase}})
            self.approve(phase)
        result = self.apply("market", {"summary": "changed", "data": {"phase": "market", "changed": True}})
        self.assertIn("pricing", result["invalidated"])
        state = arsenal.load_state(self.workspace)
        self.assertEqual(state["tracks"]["offer"]["phases"]["pricing"]["status"], "stale")

    def test_render_is_self_contained_and_escapes_content(self):
        self.apply("discovery", {"summary": "<script>alert(1)</script>", "data": {}})
        self.approve("discovery")
        result = arsenal.command_render(
            Namespace(workspace=str(self.workspace), surface="all", output_dir=str(self.root), allow_invalid=False)
        )
        self.assertEqual(len(result["outputs"]), 6)
        progress = (self.root / "demo-workshop-progress.html").read_text(encoding="utf-8")
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", progress)
        self.assertNotIn("fonts.googleapis.com", progress)
        self.assertIn("growth-arsenal declarative workspace", progress)
        self.assertNotIn("{{SCRIPT}}", progress)
        self.assertNotIn("{{NAV}}", progress)

    def test_validate_detects_manual_revision_drift(self):
        self.apply("discovery", {"summary": "one", "data": {}})
        self.approve("discovery")
        self.apply("market", {"summary": "two", "data": {}})
        self.approve("market")
        state = arsenal.load_state(self.workspace)
        state["tracks"]["offer"]["phases"]["discovery"]["revision"] = 9
        arsenal.atomic_write_text(self.workspace, json.dumps(state))
        findings = arsenal.validate_state(arsenal.load_state(self.workspace))
        self.assertTrue(any(item["code"] == "stale-offer-market" for item in findings))


if __name__ == "__main__":
    unittest.main()
