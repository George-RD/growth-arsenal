"""Exercise the installed copy-comparison command from an unrelated directory."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "copy-compare.py"


class CopyCompareCliTests(unittest.TestCase):
    """Keep invalid input distinct from a valid report whose copy fails a gate."""

    def setUp(self):
        """Create independent input files outside the source checkout."""
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.baseline = self.root / "baseline copy.txt"
        self.candidate = self.root / "candidate copy.txt"
        self.baseline.write_text("Clear copy.\n", encoding="utf-8")
        self.candidate.write_text("Clear copy.\n", encoding="utf-8")

    def run_compare(self, *options, baseline=None, candidate=None, output_format="json"):
        """Invoke the real CLI without importing or mocking its implementation."""
        return subprocess.run(
            [
                sys.executable, str(SCRIPT),
                "--baseline", str(baseline or self.baseline),
                "--candidate", str(candidate or self.candidate),
                "--format", output_format, *options,
            ],
            cwd=self.root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=10,
            check=False,
        )

    def assert_input_error(self, process, context):
        """Require a controlled input error with no partial quality report."""
        self.assertEqual(process.returncode, 2, process.stdout + process.stderr)
        self.assertEqual(process.stdout, "")
        self.assertIn(context, process.stderr)
        self.assertNotIn("Traceback", process.stderr)
        self.assertNotIn("hard_gate_pass", process.stderr)

    def test_empty_or_unanalysable_text_is_rejected_in_either_role(self):
        """Neither side of a comparison may turn absent words into a pass."""
        bad = self.root / "unanalysable.txt"
        for text in ("", " \t\r\n", "1234. 56?!", "— … !!!", "你好 世界"):
            bad.write_text(text, encoding="utf-8")
            for role in ("baseline", "candidate"):
                with self.subTest(text=text, role=role):
                    process = self.run_compare(**{role: bad})
                    self.assert_input_error(process, str(bad))
                    self.assertIn("analysable English words", process.stderr)

    def test_nonfinite_float_limits_are_rejected(self):
        """Non-finite limits must not bypass gates or enter a JSON report."""
        for flag in ("--max-grade", "--max-sentence"):
            for value in ("nan", "inf", "-inf", "1e309"):
                with self.subTest(flag=flag, value=value):
                    self.assert_input_error(
                        self.run_compare(f"{flag}={value}"), flag
                    )

    def test_negative_limits_are_rejected(self):
        """Every documented threshold rejects negative values."""
        for flag in (
            "--max-grade", "--max-emdash", "--max-sentence",
            "--similar-length-tolerance", "--similar-run-min",
            "--max-paragraph-words", "--max-paragraph-sentences",
        ):
            with self.subTest(flag=flag):
                self.assert_input_error(self.run_compare(f"{flag}=-1"), flag)

    def test_similar_run_min_cannot_be_silently_clamped(self):
        """The reported minimum must match the minimum actually used."""
        for value in ("0", "1"):
            with self.subTest(value=value):
                self.assert_input_error(
                    self.run_compare(f"--similar-run-min={value}"),
                    "--similar-run-min",
                )

    def test_file_errors_are_controlled_and_identify_the_input(self):
        """Missing, directory and invalid-UTF-8 inputs fail on either side."""
        missing = self.root / "missing.txt"
        invalid = self.root / "invalid.txt"
        invalid.write_bytes(b"\xff\xfe")
        for bad in (missing, self.root, invalid):
            for role in ("baseline", "candidate"):
                with self.subTest(path=bad, role=role):
                    process = self.run_compare(**{role: bad})
                    self.assert_input_error(process, str(bad))
                    error = json.loads(process.stderr)
                    self.assertFalse(error["ok"])
                    self.assertTrue(error["error"])

    def test_unreadable_file_is_a_controlled_input_error(self):
        """Permission failures use the same contract when enforced by the OS."""
        bad = self.root / "unreadable.txt"
        bad.write_text("Clear copy.", encoding="utf-8")
        bad.chmod(0)
        self.addCleanup(bad.chmod, 0o600)
        if os.access(bad, os.R_OK):
            self.skipTest("This user can read files with mode 000")
        for role in ("baseline", "candidate"):
            with self.subTest(role=role):
                self.assert_input_error(self.run_compare(**{role: bad}), str(bad))

    def assert_json_report(self, process):
        """Require a successful, strict-JSON report that remains winner-neutral."""
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(process.stderr, "")
        payload = json.loads(
            process.stdout,
            parse_constant=lambda value: self.fail(f"Non-standard JSON: {value}"),
        )
        self.assertIsNone(payload["winner"])
        return payload

    def test_html_is_checked_after_text_extraction(self):
        """Tags, attributes, comments and ignored elements are not copy."""
        bad = self.root / "empty.html"
        for raw in (
            '<main title="English attribute"><p>&nbsp;</p></main>',
            '<html><!-- English comment --><body></body></html>',
            '<main><script>English script</script><style>English style</style>'
            '<svg><text>English vector</text></svg><noscript>Fallback</noscript></main>',
        ):
            bad.write_text(raw, encoding="utf-8")
            for role in ("baseline", "candidate"):
                with self.subTest(raw=raw, role=role):
                    self.assert_input_error(self.run_compare(**{role: bad}), str(bad))

    def test_malformed_limits_are_rejected(self):
        """Every numeric flag rejects non-numeric text without a traceback."""
        for flag in (
            "--max-grade", "--max-emdash", "--max-sentence",
            "--similar-length-tolerance", "--similar-run-min",
            "--max-paragraph-words", "--max-paragraph-sentences",
        ):
            with self.subTest(flag=flag):
                self.assert_input_error(self.run_compare(f"{flag}=oops"), flag)

    def test_count_limits_reject_fractions(self):
        """Count limits must not truncate fractional input."""
        for flag in (
            "--max-emdash", "--similar-length-tolerance", "--similar-run-min",
            "--max-paragraph-words", "--max-paragraph-sentences",
        ):
            with self.subTest(flag=flag):
                self.assert_input_error(self.run_compare(f"{flag}=2.5"), flag)

    def test_default_report_keeps_known_metrics_and_zero_deltas(self):
        """Input guards do not alter an ordinary two-word comparison."""
        payload = self.assert_json_report(self.run_compare())
        for role in ("baseline", "candidate"):
            self.assertEqual(payload[role]["words"], 2)
            self.assertEqual(payload[role]["sentences"], 1)
            self.assertEqual(payload[role]["average_words_per_sentence"], 2.0)
            self.assertEqual(payload[role]["flesch_kincaid_grade"], 2.9)
            self.assertTrue(payload[role]["hard_gate_pass"])
            self.assertEqual(payload[role]["hard_gate_failures"], [])
        self.assertTrue(all(value == 0 for value in payload["candidate_minus_baseline"].values()))

    def test_fractional_limits_and_zero_count_limits_remain_supported(self):
        """Strict structural limits remain advisory, including zero thresholds."""
        payload = self.assert_json_report(self.run_compare(
            "--max-grade=6.5", "--max-sentence=15.25", "--max-emdash=0",
            "--similar-length-tolerance=0", "--similar-run-min=2",
            "--max-paragraph-words=0", "--max-paragraph-sentences=0",
        ))
        self.assertEqual(payload["thresholds"]["hard_gates"]["max_grade"], 6.5)
        self.assertEqual(payload["thresholds"]["hard_gates"]["max_sentence"], 15.25)
        self.assertEqual(payload["thresholds"]["structural_advisories"]["similar_run_min"], 2)
        self.assertEqual(payload["candidate"]["overloaded_paragraph_count"], 1)
        self.assertTrue(payload["candidate"]["hard_gate_pass"])

    def test_zero_float_limits_produce_a_report_not_a_usage_error(self):
        """Zero is valid even when ordinary copy fails the requested limits."""
        payload = self.assert_json_report(self.run_compare(
            "--max-grade=0", "--max-sentence=0"
        ))
        self.assertFalse(payload["candidate"]["hard_gate_pass"])
        self.assertEqual(len(payload["candidate"]["hard_gate_failures"]), 2)

    def test_large_finite_limits_remain_supported(self):
        """Finite floats and exact Python integer limits need no arbitrary cap."""
        huge_count = "9" * 400
        payload = self.assert_json_report(self.run_compare(
            "--max-grade=1e308", "--max-sentence=1e308",
            f"--max-emdash={huge_count}",
        ))
        self.assertEqual(payload["thresholds"]["hard_gates"]["max_grade"], 1e308)
        self.assertEqual(payload["thresholds"]["hard_gates"]["max_emdash"], int(huge_count))
        self.assertTrue(payload["candidate"]["hard_gate_pass"])

    def test_gate_failures_do_not_turn_a_comparison_into_an_input_error(self):
        """Valid but poor copy still returns a report in both output formats."""
        self.candidate.write_text("We leverage the plan — now.", encoding="utf-8")
        payload = self.assert_json_report(self.run_compare())
        self.assertTrue(payload["baseline"]["hard_gate_pass"])
        self.assertFalse(payload["candidate"]["hard_gate_pass"])
        self.assertIn("em dashes 1 > 0", payload["candidate"]["hard_gate_failures"])
        self.assertIn("Tier-1 vocabulary 1 > 0", payload["candidate"]["hard_gate_failures"])
        process = self.run_compare(output_format="text")
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(process.stderr, "")
        self.assertIn("hard gate PASS", process.stdout)
        self.assertIn("hard gate FAIL", process.stdout)
        self.assertIn("Advisory (structural; never gates)", process.stdout)
        self.assertIn("do not choose the winner", process.stdout)

    def test_html_and_plain_text_remain_comparable(self):
        """Existing suffix-based and automatic HTML extraction stay intact."""
        for suffix in (".html", ".txt"):
            with self.subTest(suffix=suffix):
                candidate = self.root / f"web copy{suffix}"
                candidate.write_text(
                    '<main><p>Clear copy.</p><script>leverage()</script></main>',
                    encoding="utf-8",
                )
                payload = self.assert_json_report(self.run_compare(candidate=candidate))
                self.assertTrue(payload["candidate"]["hard_gate_pass"])
                self.assertTrue(all(
                    value == 0 for value in payload["candidate_minus_baseline"].values()
                ))

    def test_input_errors_never_print_a_text_report(self):
        """The text format has the same no-partial-report error contract."""
        self.candidate.write_text("", encoding="utf-8")
        self.assert_input_error(
            self.run_compare(output_format="text"), str(self.candidate)
        )
        self.assert_input_error(
            self.run_compare("--max-grade=nan", output_format="text"), "--max-grade"
        )

    def test_inputs_remain_unchanged_on_success_and_failure(self):
        """Comparisons are read-only regardless of the exit path."""
        for text, options, expected in (
            ("Clear copy.\n", (), 0),
            ("", (), 2),
            ("Clear copy.\n", ("--max-grade=nan",), 2),
        ):
            self.candidate.write_text(text, encoding="utf-8")
            before = {path: path.read_bytes() for path in (self.baseline, self.candidate)}
            with self.subTest(text=text, options=options):
                self.assertEqual(self.run_compare(*options).returncode, expected)
                self.assertEqual({path: path.read_bytes() for path in before}, before)

    def test_help_explains_inputs_limits_and_report_only_exit_status(self):
        """Help distinguishes input failure from a completed comparison."""
        process = self.run_compare("--help")
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(process.stderr, "")
        help_text = " ".join(process.stdout.split())
        for phrase in (
            "UTF-8", "analysable English words", "finite", "non-negative",
            "--similar-run-min >= 2", "Exit 0", "even when hard gates fail",
            "Invalid input exits 2", "no stdout report",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, help_text)


if __name__ == "__main__":
    unittest.main()
