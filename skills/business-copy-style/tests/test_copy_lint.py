"""Tests for the POSIX single-copy lint wrapper."""

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "copy-lint.sh"
POSITIVE_COPY = (
    "I help owners fix late books. I help owners fix late books. "
    "I help owners fix late books. Here is what this means. "
    "It is not just cleanup, it is control. Owners see the cash. Cash stops hiding."
)
NEGATIVE_COPY = (
    "Late books hide cash. Owners waste hours chasing receipts every Friday. "
    "The service fixes the backlog, then gives the team a simple weekly routine."
)


class CopyLintTests(unittest.TestCase):
    """Cover optional structural output and unchanged hard-gate behaviour."""

    def run_lint(
        self,
        *arguments: str,
        input_text: str | None = None,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["sh", str(SCRIPT), *arguments],
            input=input_text,
            check=False,
            text=True,
            capture_output=True,
            timeout=5,
        )

    def test_structure_summary_is_opt_in(self):
        ordinary = self.run_lint("--max-grade", "20", "-", input_text=NEGATIVE_COPY)
        structured = self.run_lint(
            "--structure", "--max-grade", "20", "-", input_text=NEGATIVE_COPY
        )
        self.assertNotIn("structural advisory", ordinary.stdout)
        self.assertIn("structural advisory (never gates)", structured.stdout)

    def test_structure_summary_reports_positive_fixture(self):
        result = self.run_lint(
            "--structure",
            "--max-grade",
            "20",
            "-",
            input_text=POSITIVE_COPY,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("duplicate sentences 2", result.stdout)
        self.assertIn("similar-length runs 1", result.stdout)
        self.assertIn("overloaded paragraphs 1", result.stdout)
        self.assertIn("contrast 1", result.stdout)
        self.assertIn("meta phrases 2", result.stdout)

    def test_structure_summary_reports_comma_not_contrast(self):
        result = subprocess.run(
            ["sh", str(SCRIPT), "--structure", "--max-grade", "20", "-"],
            input="The case supports a pilot charter, not an ROI claim.",
            check=False,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("contrast 1", result.stdout)
    def test_structure_summary_ignores_comma_not_gerund(self):
        result = subprocess.run(
            ["sh", str(SCRIPT), "--structure", "--max-grade", "20", "-"],
            input="We asked, not knowing the answer.",
            check=False,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("contrast 0", result.stdout)


    def test_structural_signals_do_not_change_exit_code(self):
        ordinary = self.run_lint("--max-grade", "20", "-", input_text=POSITIVE_COPY)
        structured = self.run_lint(
            "--structure", "--max-grade", "20", "-", input_text=POSITIVE_COPY
        )
        self.assertEqual(ordinary.returncode, structured.returncode)

    def test_missing_threshold_value_returns_usage_error(self):
        result = self.run_lint("--max-paragraph-words")
        self.assertEqual(result.returncode, 2)
        self.assertIn("requires a value", result.stderr)

    def test_input_without_english_words_is_an_input_error(self):
        for text in ("", " \t\n\r\n", "... !!! ???", "123 456", "— –"):
            with self.subTest(text=text):
                result = self.run_lint("-", input_text=text)
                self.assertEqual(result.returncode, 2)
                self.assertIn("no analysable English words", result.stderr)
                self.assertEqual(result.stdout, "")

    def test_empty_file_is_an_input_error(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / "empty.md"
            path.write_text("", encoding="utf-8")
            result = self.run_lint(str(path))
        self.assertEqual(result.returncode, 2)
        self.assertIn("no analysable English words", result.stderr)
        self.assertEqual(result.stdout, "")

    def test_malformed_thresholds_are_rejected_before_reading_input(self):
        options = (
            "--max-grade", "--max-emdash", "--max-sentence",
            "--similar-length-tolerance", "--similar-run-min",
            "--max-paragraph-words", "--max-paragraph-sentences",
        )
        invalid = ("nonsense", "NaN", "inf", "1e309", "-1", "1.2.3", " 2", "2 ", "9" * 400)
        with tempfile.TemporaryDirectory() as root:
            missing = str(Path(root) / "missing.md")
            for option in options:
                for value in invalid:
                    with self.subTest(option=option, value=value):
                        result = self.run_lint(option, value, missing)
                        self.assertEqual(result.returncode, 2)
                        self.assertIn(option, result.stderr)
                        self.assertNotIn("no such file", result.stderr)
                        self.assertEqual(result.stdout, "")

    def test_count_thresholds_reject_fractions(self):
        for option in (
            "--max-emdash", "--similar-length-tolerance", "--similar-run-min",
            "--max-paragraph-words", "--max-paragraph-sentences",
        ):
            with self.subTest(option=option):
                result = self.run_lint(option, "2.5", "-", input_text="We fix books.")
                self.assertEqual(result.returncode, 2)
                self.assertIn(option, result.stderr)
                self.assertEqual(result.stdout, "")

    def test_similar_run_minimum_requires_at_least_two_sentences(self):
        for minimum in ("0", "1"):
            with self.subTest(minimum=minimum):
                result = self.run_lint(
                    "--similar-run-min", minimum, "-", input_text="We fix books."
                )
                self.assertEqual(result.returncode, 2)
                self.assertIn("--similar-run-min", result.stderr)

    def test_decimal_limits_and_zero_count_limits_remain_valid(self):
        result = self.run_lint(
            "--max-grade", "6.5", "--max-sentence", "15.5", "--max-emdash", "0",
            "--similar-length-tolerance", "0", "--similar-run-min", "2",
            "--max-paragraph-words", "0", "--max-paragraph-sentences", "0",
            "--structure", "-", input_text="We fix books."
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("overloaded paragraphs 1", result.stdout)

    def test_multiple_inputs_never_silently_select_the_last_file(self):
        with tempfile.TemporaryDirectory() as root:
            first = Path(root) / "first.md"
            second = Path(root) / "second.md"
            first.write_text("We leverage tools.", encoding="utf-8")
            second.write_text("We fix books.", encoding="utf-8")
            for arguments in (
                (str(first), str(second)),
                ("-", str(second)),
                (str(first), "-"),
                ("-", "-"),
                (str(first), "--", str(second)),
            ):
                with self.subTest(arguments=arguments):
                    result = self.run_lint(*arguments, input_text="We fix books.")
                    self.assertEqual(result.returncode, 2)
                    self.assertIn("exactly one input", result.stderr)
                    self.assertEqual(result.stdout, "")

    def test_end_of_options_accepts_a_dash_prefixed_filename(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / "-draft.md"
            path.write_text("We fix books.", encoding="utf-8")
            result = subprocess.run(
                ["sh", str(SCRIPT), "--", path.name], cwd=root,
                capture_output=True, text=True, check=False, timeout=5,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("words / sentences        : 3 / 1", result.stdout)

    def test_file_and_stdin_reports_match(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / "draft with spaces.md"
            path.write_text(NEGATIVE_COPY, encoding="utf-8")
            from_file = self.run_lint("--max-grade", "20", str(path))
            from_stdin = self.run_lint("--max-grade", "20", "-", input_text=NEGATIVE_COPY)
        self.assertEqual(from_file.returncode, 0, from_file.stderr)
        self.assertEqual(from_file.stdout, from_stdin.stdout)
        self.assertEqual(from_file.returncode, from_stdin.returncode)

    def test_missing_input_and_unknown_options_are_usage_errors(self):
        for arguments in ((), ("--",), ("--unknown",)):
            with self.subTest(arguments=arguments):
                result = self.run_lint(*arguments)
                self.assertEqual(result.returncode, 2)
                self.assertIn("copy-lint:", result.stderr)
                self.assertEqual(result.stdout, "")

    def test_hard_gate_failures_still_return_one(self):
        cases = (
            ((), "We fix books—fast.", "FAIL em dashes"),
            ((), "We leverage tools.", "FAIL Tier-1 vocab"),
            (("--max-grade", "0"), "The recommendation requires executive approval.", "FAIL grade"),
            (("--max-sentence", "2"), "We fix books each week.", "FAIL avg sentence"),
        )
        for arguments, text, diagnostic in cases:
            with self.subTest(arguments=arguments, text=text):
                result = self.run_lint(*arguments, "-", input_text=text)
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertIn(diagnostic, result.stdout)
                self.assertEqual(result.stderr, "")

    def test_an_explicit_valid_dash_limit_still_applies(self):
        result = self.run_lint("--max-emdash", "1", "-", input_text="We fix books—fast.")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("em dashes (U+2014)       : 1", result.stdout)

    def test_decimal_notation_and_leading_zeroes_remain_valid(self):
        for value in ("0", "0.0", ".5", "6.", "06.5"):
            with self.subTest(value=value):
                result = self.run_lint("--max-grade", value, "-", input_text="We fix books.")
                self.assertEqual(result.returncode, 0, result.stderr)
        result = self.run_lint("--max-emdash", "00", "-", input_text="We fix books.")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_awk_escapes_cannot_disguise_invalid_thresholds(self):
        for value in (r"\061", r"6\n", r"6\x00", ".", "+2"):
            with self.subTest(value=value):
                result = self.run_lint("--max-grade", value, "-", input_text="We fix books.")
                self.assertEqual(result.returncode, 2)
                self.assertIn("--max-grade", result.stderr)
                self.assertEqual(result.stdout, "")

    def test_overriding_an_invalid_limit_does_not_hide_the_error(self):
        result = self.run_lint(
            "--max-emdash", "nonsense", "--max-emdash", "1", "-",
            input_text="We fix books—fast.",
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("--max-emdash", result.stderr)
        self.assertEqual(result.stdout, "")

    def test_end_of_options_also_accepts_stdin(self):
        result = self.run_lint("--", "-", input_text="We fix books.")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_stdin_read_failure_is_an_input_error(self):
        with tempfile.TemporaryDirectory() as root:
            descriptor = os.open(root, os.O_RDONLY)
            try:
                result = subprocess.run(
                    ["sh", str(SCRIPT), "-"], stdin=descriptor,
                    capture_output=True, text=True, check=False, timeout=5,
                )
            finally:
                os.close(descriptor)
        self.assertEqual(result.returncode, 2)
        self.assertIn("could not read stdin", result.stderr)
        self.assertEqual(result.stdout, "")

    def test_help_describes_validation_without_reading_input(self):
        result = self.run_lint("--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        for phrase in ("exactly one", "non-negative", "at least 2", "Exit codes:"):
            self.assertIn(phrase, result.stdout)
        self.assertNotIn("set -eu", result.stdout)
        self.assertEqual(result.stderr, "")

    def test_large_finite_limits_are_not_rejected_as_overflow(self):
        result = self.run_lint(
            "--max-grade", "1" + "0" * 308, "-", input_text="We fix books."
        )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
