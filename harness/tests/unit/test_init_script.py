from __future__ import annotations

import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "init.sh"


class InitScriptTests(unittest.TestCase):
    def run_script(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["sh", str(SCRIPT), *args],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

    def test_help_lists_one_click_workflows(self) -> None:
        result = self.run_script("help")
        self.assertEqual(0, result.returncode, result.stderr)
        for command in ("dev", "deploy", "test all", "test layer1", "test layer2", "test feature"):
            self.assertIn(command, result.stdout)
        for deployment_contract in ("运行时白名单", "不覆盖已有同名 Skill", "重启对应 Agent", "$eda-tester-skill"):
            self.assertIn(deployment_contract, result.stdout)

    def test_dry_run_prints_commands_without_running_them(self) -> None:
        result = self.run_script("--dry-run", "test", "all")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("run_jenkins_gate.py", result.stdout)

    def test_layer_and_scenario_dispatch_are_explicit(self) -> None:
        layer1 = self.run_script("--dry-run", "test", "layer1")
        self.assertIn("validate.py project", layer1.stdout)
        self.assertIn("quick_validate.py", layer1.stdout)

        feature = self.run_script("--dry-run", "test", "feature", "F-026")
        self.assertIn("validate.py feature F-026", feature.stdout)

        tcl = self.run_script("--dry-run", "test", "tcl", "path/to/pos001_case")
        self.assertIn("validate.py tcl path/to/pos001_case", tcl.stdout)

    def test_unknown_workflow_fails(self) -> None:
        result = self.run_script("test", "unknown")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("未知测试场景", result.stderr)


if __name__ == "__main__":
    unittest.main()
