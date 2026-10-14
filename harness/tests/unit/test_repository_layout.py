from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


class RepositoryLayoutTests(unittest.TestCase):
    def test_runtime_product_and_project_harness_are_physically_separated(self) -> None:
        runtime = ROOT / "skill"
        harness = ROOT / "harness"
        for relative in ("SKILL.md", "agents", "assets", "references", "scripts"):
            self.assertTrue((runtime / relative).exists(), f"missing runtime entry: skill/{relative}")
        for relative in ("PROCESS.MD", "function.json", "tests", "references", "scripts"):
            self.assertTrue((harness / relative).exists(), f"missing harness entry: harness/{relative}")

    def test_project_harness_files_are_absent_from_runtime_tree(self) -> None:
        runtime = ROOT / "skill"
        for relative in (
            "PROCESS.MD",
            "function.json",
            "tests",
            "references/test-plan.md",
            "references/e2e-test-set.md",
            "scripts/install_skill.py",
        ):
            self.assertFalse((runtime / relative).exists(), f"harness file leaked into skill/: {relative}")


if __name__ == "__main__":
    unittest.main()
