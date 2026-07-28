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
        arsenal.command_init(Namespace(workspace=str(self.workspace), project="demo", name="Demo", locale="en-GB", currency="GBP", spelling="british", timezone="Europe/London", force=False))

    def tearDown(self):
        self.temp.cleanup()

    def write_payload(self, name, payload):
        path = self.root / name
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def apply(self, phase, payload, track="offer"):
        path = self.write_payload(f"{track}-{phase}.json", payload)
        return arsenal.command_apply(Namespace(workspace=str(self.workspace), track=track, phase=phase, input=str(path)))

    def add_reviews(self, phase, reviews, track="offer"):
        path = self.write_payload(f"{track}-{phase}-reviews.json", reviews)
        return arsenal.command_add_review(Namespace(workspace=str(self.workspace), track=track, phase=phase, input=str(path)))

    def approve(self, phase, track="offer"):
        return arsenal.command_approve(Namespace(workspace=str(self.workspace), track=track, phase=phase))

    def test_new_workspace_contains_offer_and_leads_tracks(self):
        state = arsenal.load_state(self.workspace)
        self.assertEqual(state["tracks"]["offer"]["current_phase"], "discovery")
        self.assertEqual(state["tracks"]["leads"]["current_phase"], "discovery")
        self.assertIn("rule-of-100", state["tracks"]["leads"]["phases"])

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
        self.add_reviews("discovery", [
            {"reviewer": "marketer", "issues": [{"issue_key": "buyer-too-broad", "finding": "Broad"}]},
            {"reviewer": "strategist", "issues": [{"issue_key": "buyer-too-broad", "finding": "Broad"}]},
        ])
        result = arsenal.command_accept_risk(Namespace(workspace=str(self.workspace), track="offer", phase="discovery", issue_key="buyer-too-broad", reason="Pilot will narrow the market", confirmed_by="user"))
        self.assertTrue(result["gate"]["can_approve"])
        self.assertTrue(result["gate"]["issues"][0]["accepted_risk"])
        self.approve("discovery")

    def test_offer_change_marks_later_offer_phase_stale(self):
        for phase in ("discovery", "market", "pricing"):
            self.apply(phase, {"summary": phase, "data": {"phase": phase}})
            self.approve(phase)
        result = self.apply("market", {"summary": "changed", "data": {"phase": "market", "changed": True}})
        self.assertIn("offer:pricing", result["invalidated"])
        state = arsenal.load_state(self.workspace)
        self.assertEqual(state["tracks"]["offer"]["phases"]["pricing"]["status"], "stale")

    def test_offer_change_invalidates_existing_leads_track(self):
        self.apply("discovery", {"summary": "offer", "data": {}})
        self.approve("discovery")
        self.apply("discovery", {"summary": "lead audit", "data": {"audience": "Garages"}}, track="leads")
        self.approve("discovery", track="leads")
        result = self.apply("discovery", {"summary": "offer changed", "data": {"changed": True}})
        self.assertIn("leads:discovery", result["invalidated"])
        lead_phase = arsenal.load_state(self.workspace)["tracks"]["leads"]["phases"]["discovery"]
        self.assertEqual(lead_phase["status"], "stale")
        self.assertIn("Offer phase discovery changed", lead_phase["stale_reason"])

    def test_leads_change_only_invalidates_later_leads_work(self):
        for phase in ("discovery", "lead-magnet", "channels"):
            self.apply(phase, {"summary": phase, "data": {"phase": phase}}, track="leads")
            self.approve(phase, track="leads")
        result = self.apply("lead-magnet", {"summary": "changed", "data": {"phase": "lead-magnet"}}, track="leads")
        self.assertIn("leads:channels", result["invalidated"])
        self.assertEqual(arsenal.load_state(self.workspace)["tracks"]["offer"]["phases"]["discovery"]["status"], "not_started")

    def test_render_is_self_contained_and_escapes_content(self):
        self.apply("discovery", {"summary": "<script>alert(1)</script>", "data": {}})
        self.approve("discovery")
        result = arsenal.command_render(Namespace(workspace=str(self.workspace), surface="all", output_dir=str(self.root), allow_invalid=False))
        self.assertEqual(len(result["outputs"]), 11)
        progress = (self.root / "demo-workshop-progress.html").read_text(encoding="utf-8")
        leads = (self.root / "demo-leads-blueprint.html").read_text(encoding="utf-8")
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", progress)
        self.assertNotIn("fonts.googleapis.com", progress)
        self.assertIn("growth-arsenal declarative workspace", progress)
        self.assertIn("LEAD SYSTEM", leads)
        for marker in ("{{SCRIPT}}", "{{NAV}}", "{{MAGNET_ROWS}}"):
            self.assertNotIn(marker, leads + progress)

    def test_validate_detects_manual_offer_revision_drift_in_leads(self):
        self.apply("discovery", {"summary": "offer", "data": {}})
        self.approve("discovery")
        self.apply("discovery", {"summary": "leads", "data": {}}, track="leads")
        self.approve("discovery", track="leads")
        state = arsenal.load_state(self.workspace)
        state["tracks"]["offer"]["phases"]["discovery"]["revision"] = 9
        arsenal.atomic_write_text(self.workspace, json.dumps(state))
        findings = arsenal.validate_state(arsenal.load_state(self.workspace))
        self.assertTrue(any(item["code"] == "stale-leads-discovery" for item in findings))


if __name__ == "__main__":
    unittest.main()
