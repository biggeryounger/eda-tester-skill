from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


class SkillWorkflowToolsTests(unittest.TestCase):
    def test_skill_requires_three_independent_tcl_static_checks(self) -> None:
        skill = (ROOT / "skill" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Tcl 基础语法", skill)
        self.assertIn("EDA 工具命令及选项使用", skill)
        self.assertIn("TCL 编程规范", skill)
        self.assertIn("分别报告", skill)

    def test_skill_requires_scenario_and_option_coverage(self) -> None:
        skill = (ROOT / "skill" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("场景覆盖率", skill)
        self.assertIn("被测选项覆盖率", skill)
        self.assertIn("未覆盖项", skill)
        self.assertIn("命令规格清单", skill)

    def test_missing_tool_cannot_be_reported_as_pass(self) -> None:
        skill = (ROOT / "skill" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("TOOL_UNAVAILABLE", skill)
        self.assertIn("不得以人工判断替代", skill)

    def test_delivery_gate_separates_script_and_semantic_checks(self) -> None:
        skill = (ROOT / "skill" / "SKILL.md").read_text(encoding="utf-8")
        validator = (ROOT / "skill" / "scripts" / "tcl_convention_validator.py").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("scripts/validate.py", skill)
        self.assertIn("python3 scripts/test_plan_validator.py <plan.xlsx>", skill)
        self.assertIn("python3 scripts/tcl_convention_validator.py <case_dir>...", skill)
        self.assertIn("scripts/test_plan_validator.py", skill)
        self.assertIn("scripts/tcl_convention_validator.py", skill)
        self.assertIn("references/specs/test-plan-rules.md", skill)
        self.assertIn("references/specs/tcl-script-rules.md", skill)
        self.assertEqual(1, skill.count("**执行脚本静态检查**"))
        self.assertNotIn("**执行自动检查脚本**", skill)
        self.assertNotIn("**执行 EDA 工具脚本静态检查**", skill)
        self.assertIn("统一的 TCL 脚本静态检查器", validator)
        self.assertIn("Tcl 基础语法、EDA 工具命令及选项使用、TCL 编程规范", validator)


if __name__ == "__main__":
    unittest.main()
