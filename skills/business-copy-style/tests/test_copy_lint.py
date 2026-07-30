"""Tests for the POSIX single-copy lint wrapper."""

import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "copy-lint.sh"
FIXTURES = ROOT / "evaluations" / "fixtures"


class CopyLintTests(unittest.TestCase):
    """Cover optional structural output and unchanged hard-gate behaviour."""

    def run_lint(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["sh", str(SCRIPT), *arguments],
            check=False,
            text=True,
            capture_output=True,
        )

    def test_structure_summary_is_opt_in(self):
        fixture = str(FIXTURES / "structural-advisory-negative.txt")
        ordinary = self.run_lint("--max-grade", "20", fixture)
        structured = self.run_lint("--structure", "--max-grade", "20", fixture)
        self.assertNotIn("structural advisory", ordinary.stdout)
        self.assertIn("structural advisory (never gates)", structured.stdout)

    def test_structure_summary_reports_positive_fixture(self):
        result = self.run_lint(
            "--structure",
            "--max-grade",
            "20",
            str(FIXTURES / "structural-advisory-positive.txt"),
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("duplicate sentences 2", result.stdout)
        self.assertIn("similar-length runs 1", result.stdout)
        self.assertIn("overloaded paragraphs 1", result.stdout)
        self.assertIn("contrast 1", result.stdout)
        self.assertIn("meta phrases 1", result.stdout)

    def test_structural_signals_do_not_change_exit_code(self):
        fixture = str(FIXTURES / "structural-advisory-positive.txt")
        ordinary = self.run_lint("--max-grade", "20", fixture)
        structured = self.run_lint("--structure", "--max-grade", "20", fixture)
        self.assertEqual(ordinary.returncode, structured.returncode)

    def test_missing_threshold_value_returns_usage_error(self):
        result = self.run_lint("--max-paragraph-words")
        self.assertEqual(result.returncode, 2)
        self.assertIn("requires a value", result.stderr)


if __name__ == "__main__":
    unittest.main()
