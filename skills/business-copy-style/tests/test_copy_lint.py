"""Tests for the POSIX single-copy lint wrapper."""

import subprocess
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


if __name__ == "__main__":
    unittest.main()
