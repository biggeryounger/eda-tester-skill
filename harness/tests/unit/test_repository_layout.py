from __future__ import annotations

import unittest
from pathlib import Path
import re


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

    def test_runtime_and_development_validation_assets_are_fully_separated(self) -> None:
        runtime = ROOT / "skill"
        harness = ROOT / "harness"
        self.assertFalse((runtime / "scripts" / "validate.py").exists())
        self.assertTrue((harness / "scripts" / "project_validator.py").is_file())
        self.assertTrue((runtime / "scripts" / "test_plan_validator.py").is_file())
        self.assertTrue((runtime / "scripts" / "tcl_convention_validator.py").is_file())
        self.assertFalse((runtime / "tests").exists())
        self.assertTrue((harness / "tests").is_dir())
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("Skill 产物与项目开发资产必须完全分离", agents)
        self.assertIn("禁止跨目录混合维护", agents)

    def test_skill_test_cases_must_be_repeatable_automated_scripts(self) -> None:
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("构建 Skill 测试用例必须使用可重复、可稳定运行的自动化脚本用例", agents)
        self.assertIn("禁止以一次性人工操作或不可复现的交互结果作为测试用例", agents)

    def test_runtime_tree_contains_no_readme_files(self) -> None:
        runtime = ROOT / "skill"
        readmes = sorted(
            path.relative_to(runtime).as_posix()
            for path in runtime.rglob("*")
            if path.is_file() and path.name.casefold() == "readme.md"
        )
        self.assertEqual([], readmes, f"README.md is not allowed inside skill/: {readmes}")

    def test_tests_tree_uses_no_legacy_cases_or_shared_fixtures_directories(self) -> None:
        tests = ROOT / "harness" / "tests"
        project_validator = (ROOT / "harness" / "scripts" / "project_validator.py").read_text(encoding="utf-8")
        self.assertFalse((tests / "cases").exists(), "harness/tests/cases is no longer part of the test layout")
        self.assertFalse((tests / "fixtures").exists(), "harness/tests/fixtures is no longer part of the test layout")
        self.assertTrue((tests / "unit").is_dir())
        self.assertTrue((tests / "regression").is_dir())
        self.assertTrue((tests / "e2e").is_dir())
        self.assertNotIn('"tests" / "cases"', project_validator)
        self.assertNotIn('add_argument("--cases"', project_validator)

    def test_openai_registration_metadata_has_three_part_description(self) -> None:
        metadata = (ROOT / "skill" / "agents" / "openai.yaml").read_text(encoding="utf-8")
        match = re.search(r'^  short_description: "([^"]+)"$', metadata, re.MULTILINE)
        self.assertIsNotNone(match, "openai.yaml must define a quoted short_description")
        description = match.group(1)
        self.assertGreaterEqual(len(description), 25)
        self.assertLessEqual(len(description), 64)
        self.assertEqual(3, len(description.split("；")), "description must contain what, when, and capabilities")
        self.assertIn("显式调用", description)
        self.assertIn("场景分解", description)
        self.assertIn("Excel", description)
        self.assertIn("TCL", description)
        self.assertIn('$eda-tester-skill', metadata)
        self.assertIn("allow_implicit_invocation: false", metadata)


if __name__ == "__main__":
    unittest.main()
