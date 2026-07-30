"""Tests for deterministic paired-copy comparison."""

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "copy-compare.py"
ROOT = Path(__file__).resolve().parents[3]
FIXTURES = ROOT / "evaluations" / "fixtures"
spec = importlib.util.spec_from_file_location("copy_compare", SCRIPT)
copy_compare = importlib.util.module_from_spec(spec)
assert spec.loader
sys.modules[spec.name] = copy_compare
spec.loader.exec_module(copy_compare)


class CopyCompareTests(unittest.TestCase):
    """Cover extraction, gates, structural advisories and winner neutrality."""

    def test_result_refuses_to_choose_a_winner(self):
        payload = copy_compare.result(
            "We help owners get more leads.",
            "Get more leads without another admin job.",
            baseline_label="A",
            candidate_label="B",
            max_grade=6,
            max_emdash=0,
            max_sentence=15,
        )
        self.assertIsNone(payload["winner"])
        self.assertIn("qualitative", payload["decision_required"])

    def test_html_extraction_ignores_script_and_style(self):
        text = copy_compare.visible_text(
            "<html><style>bad word</style><body><h1>Clear headline.</h1>"
            "<script>delve()</script></body></html>",
            ".html",
        )
        self.assertIn("Clear headline", text)
        self.assertNotIn("delve", text)
        self.assertNotIn("bad word", text)

    def test_html_block_elements_preserve_word_boundaries(self):
        text = copy_compare.visible_text(
            "<main><section><div>leverage</div><div>growth.</div></section></main>",
            ".html",
        )
        self.assertEqual(text, "leverage\ngrowth.")
        metrics = copy_compare.analyse(text)
        self.assertEqual(metrics.tier_1_terms, ["leverage"])
        self.assertEqual(metrics.words, 2)

    def test_metrics_report_gate_failures(self):
        metrics = copy_compare.analyse(
            "We leverage a transformative ecosystem — and navigate the landscape.",
            max_grade=6,
            max_emdash=0,
            max_sentence=15,
        )
        self.assertFalse(metrics.hard_gate_pass)
        self.assertGreater(metrics.tier_1_count, 0)
        self.assertEqual(metrics.em_dashes, 1)

    def test_decimal_does_not_create_a_sentence(self):
        metrics = copy_compare.analyse("Buy it for $9.99 today.")
        self.assertEqual(metrics.sentences, 1)

    def test_abbreviation_does_not_create_extra_sentences(self):
        metrics = copy_compare.analyse("Use e.g. this plan. Then test it.")
        self.assertEqual(metrics.sentences, 2)

    def test_url_does_not_create_extra_sentences(self):
        metrics = copy_compare.analyse("Read https://example.com/guide. Then act.")
        self.assertEqual(metrics.sentences, 2)

    def test_candidate_delta_is_candidate_minus_baseline(self):
        payload = copy_compare.result(
            "Short copy.",
            "This candidate has several more words than the baseline copy.",
            baseline_label="A",
            candidate_label="B",
            max_grade=20,
            max_emdash=0,
            max_sentence=30,
        )
        self.assertGreater(payload["candidate_minus_baseline"]["words"], 0)

    def test_read_copy_auto_extracts_html(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "copy.html"
            path.write_text(
                "<main><h1>Offer test.</h1><p>Fix it early.</p></main>",
                encoding="utf-8",
            )
            self.assertEqual(copy_compare.read_copy(path), "Offer test.\nFix it early.")

    def test_positive_fixture_exposes_each_structural_advisory(self):
        metrics = copy_compare.analyse(
            (FIXTURES / "structural-advisory-positive.txt").read_text(encoding="utf-8")
        )
        self.assertGreater(metrics.duplicate_sentence_instances, 0)
        self.assertGreater(metrics.repeated_two_word_starter_instances, 0)
        self.assertGreater(metrics.similar_sentence_length_run_count, 0)
        self.assertGreater(metrics.repeated_four_word_phrase_instances, 0)
        self.assertGreater(metrics.overloaded_paragraph_count, 0)
        self.assertGreater(metrics.first_person_sentence_start_rate, 0)
        self.assertGreater(metrics.contrast_scaffold_count, 0)
        self.assertGreater(metrics.meta_phrase_count, 0)

    def test_negative_fixture_avoids_structural_alerts_and_varies_rhythm(self):
        metrics = copy_compare.analyse(
            (FIXTURES / "structural-advisory-negative.txt").read_text(encoding="utf-8")
        )
        self.assertEqual(metrics.duplicate_sentence_instances, 0)
        self.assertEqual(metrics.repeated_two_word_starter_instances, 0)
        self.assertEqual(metrics.similar_sentence_length_run_count, 0)
        self.assertEqual(metrics.repeated_four_word_phrase_instances, 0)
        self.assertEqual(metrics.overloaded_paragraph_count, 0)
        self.assertEqual(metrics.first_person_sentence_start_rate, 0)
        self.assertEqual(metrics.contrast_scaffold_count, 0)
        self.assertEqual(metrics.meta_phrase_count, 0)
        self.assertGreater(metrics.sentence_length_stdev, 0)

    def test_repeated_phrase_detector_ignores_mostly_stopword_windows(self):
        metrics = copy_compare.analyse(
            "This is in the way. This is in the way.",
            max_grade=20,
            max_sentence=30,
        )
        self.assertEqual(metrics.repeated_four_word_phrase_instances, 0)

    def test_structural_advisories_never_change_hard_gate_or_winner(self):
        repetitive = "We test the offer now. We test the offer now. We test the offer now."
        metrics = copy_compare.analyse(
            repetitive,
            max_grade=20,
            max_sentence=30,
        )
        self.assertTrue(metrics.hard_gate_pass)
        self.assertGreater(metrics.duplicate_sentence_instances, 0)
        payload = copy_compare.result(
            "Clear copy.",
            repetitive,
            baseline_label="A",
            candidate_label="B",
            max_grade=20,
            max_emdash=0,
            max_sentence=30,
        )
        self.assertIsNone(payload["winner"])
        self.assertGreater(
            payload["candidate_minus_baseline"]["duplicate_sentence_instances"],
            0,
        )

    def test_paragraph_thresholds_are_configurable(self):
        text = "One short sentence. A second short sentence."
        default = copy_compare.analyse(text)
        strict = copy_compare.analyse(text, max_paragraph_sentences=1)
        self.assertEqual(default.overloaded_paragraph_count, 0)
        self.assertEqual(strict.overloaded_paragraph_count, 1)

    def test_text_report_labels_structural_signals_as_advisory(self):
        payload = copy_compare.result(
            "Baseline copy.",
            "Candidate copy.",
            baseline_label="A",
            candidate_label="B",
            max_grade=20,
            max_emdash=0,
            max_sentence=30,
        )
        report = copy_compare.text_report(payload)
        self.assertIn("Advisory (structural; never gates)", report)


if __name__ == "__main__":
    unittest.main()
