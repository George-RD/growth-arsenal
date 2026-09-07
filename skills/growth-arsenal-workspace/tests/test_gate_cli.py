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
            [sys.executable, str(SCRIPT), command,
             "--workspace", str(self.workspace), *options],
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

    def review(self, phase):
        """Submit two independent clean reviews through the CLI."""

        payload = self.root / "reviews.json"
        payload.write_text(
            json.dumps([
                {"reviewer": "marketer", "issues": []},
                {"reviewer": "strategist", "issues": []},
            ]),
            encoding="utf-8",
        )
        return self.run_command("add-review", "--phase", phase, "--input", str(payload))

    def prepare(self, *phases):
        """Build approved predecessors using only supported transitions."""

        for phase in phases:
            self.apply(phase)
            self.review(phase)
            self.run_command("approve", "--phase", phase)

    def test_upstream_change_blocks_gate_without_erasing_review_history(self):
        """Clean historical reviews cannot make a stale phase approval-ready."""

        self.prepare("discovery", "market", "pricing")
        self.apply("market")
        before = self.workspace.read_bytes()

        gate = self.run_command("gate", "--phase", "pricing", exit_code=1)

        self.assertFalse(gate["can_approve"])
        self.assertTrue(gate["review_requirement_met"])
        self.assertTrue(gate["review_gate_passed"])
        self.assertEqual(gate["review_count"], 2)
        self.assertIn("stale-phase", {item["code"] for item in gate["blockers"]})
        self.assertEqual(self.workspace.read_bytes(), before)
        rejected = self.run_command("approve", "--phase", "pricing", exit_code=2)
        self.assertEqual(rejected["error"], gate["blockers"][0]["message"])
        self.assertEqual(self.workspace.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
