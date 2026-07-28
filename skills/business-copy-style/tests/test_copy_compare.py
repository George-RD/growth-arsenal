import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "copy-compare.py"
spec = importlib.util.spec_from_file_location("copy_compare", SCRIPT)
copy_compare = importlib.util.module_from_spec(spec)
assert spec.loader
sys.modules[spec.name] = copy_compare
spec.loader.exec_module(copy_compare)


class CopyCompareTests(unittest.TestCase):
    def test_result_refuses_to_choose_a_winner(self):
        payload = copy_compare.result("We help owners get more leads.", "Get more leads without another admin job.", baseline_label="A", candidate_label="B", max_grade=6, max_emdash=0, max_sentence=15)
        self.assertIsNone(payload["winner"])
        self.assertIn("qualitative", payload["decision_required"])

    def test_html_extraction_ignores_script_and_style(self):
        text = copy_compare.visible_text("<html><style>bad word</style><body><h1>Clear headline.</h1><script>delve()</script></body></html>", ".html")
        self.assertIn("Clear headline", text)
        self.assertNotIn("delve", text)
        self.assertNotIn("bad word", text)

    def test_metrics_report_gate_failures(self):
        metrics = copy_compare.analyse("We leverage a transformative ecosystem — and navigate the landscape.", max_grade=6, max_emdash=0, max_sentence=15)
        self.assertFalse(metrics.hard_gate_pass)
        self.assertGreater(metrics.tier_1_count, 0)
        self.assertEqual(metrics.em_dashes, 1)

    def test_candidate_delta_is_candidate_minus_baseline(self):
        payload = copy_compare.result("Short copy.", "This candidate has several more words than the baseline copy.", baseline_label="A", candidate_label="B", max_grade=20, max_emdash=0, max_sentence=30)
        self.assertGreater(payload["candidate_minus_baseline"]["words"], 0)

    def test_read_copy_auto_extracts_html(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "copy.html"
            path.write_text("<main><h1>Offer test.</h1><p>Fix it early.</p></main>", encoding="utf-8")
            self.assertEqual(copy_compare.read_copy(path), "Offer test.\nFix it early.")


if __name__ == "__main__":
    unittest.main()
