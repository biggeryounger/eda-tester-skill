from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


class SkillWorkflowModesTests(unittest.TestCase):
    def setUp(self) -> None:
        self.skill = (ROOT / "skill" / "SKILL.md").read_text(encoding="utf-8")

    def test_routes_command_spec_to_design_then_script(self) -> None:
        self.assertIn("## Workflow", self.skill)
        self.assertIn("选择且只执行以下一个场景", self.skill)
        self.assertIn("场景一：从命令说明设计新用例", self.skill)
        self.assertIn("被测命令说明", self.skill)
        self.assertIn("生成测试用例设计表", self.skill)
        self.assertIn("用户明确确认", self.skill)
        self.assertIn("确认前不得生成 TCL", self.skill)
        self.assertIn("WAIT-STRATEGY", self.skill)
        self.assertIn("等待内容：用户选择一个或多个测试策略", self.skill)
        self.assertIn("WAIT-DESIGN-CONFIRMATION", self.skill)
        self.assertIn("等待内容：用户明确确认当前用例设计可用于生成 TCL", self.skill)

    def test_routes_existing_plan_directly_to_script_generation(self) -> None:
        self.assertIn("场景二：从已有用例设计表生成脚本", self.skill)
        self.assertIn("已有测试用例设计表", self.skill)
        self.assertIn("不重新执行场景设计或策略选择", self.skill)
        self.assertIn("不得擅自改写已给出的用例设计", self.skill)
        self.assertIn("直接生成 TCL", self.skill)
        self.assertIn("共享：脚本生成与交付门禁", self.skill)

    def test_existing_plan_stops_on_invalid_or_ambiguous_rows(self) -> None:
        self.assertIn("缺失、歧义或冲突", self.skill)
        self.assertIn("停止脚本生成", self.skill)
        self.assertIn("WAIT-PLAN-FIX", self.skill)
        self.assertIn("等待内容：用户补充或修正列出的问题", self.skill)

    def test_wait_markers_define_resume_conditions(self) -> None:
        self.assertEqual(4, self.skill.count("**WAIT-"))
        self.assertNotIn("WAIT-DESIGN-TECH-SELECTION", self.skill)
        self.assertIn("WAIT-DESIGN-CONFIRMATION", self.skill)
        self.assertIn("并确认所选 design 和 tech", self.skill)
        self.assertNotIn("确认相应的 `design.tcl` 与 `mmmc.tcl`", self.skill)
        self.assertIn("WAIT-SCRIPT-DELIVERY-FIX", self.skill)
        self.assertIn("等待内容：用户补充或确认语义缺口", self.skill)
        self.assertGreaterEqual(self.skill.count("继续条件："), 4)

    def test_archives_selected_design_and_tech_inputs_into_each_case(self) -> None:
        self.assertIn("用户选择的 design 和 tech", self.skill)
        self.assertIn("根据已登记的 design/tech 资源映射自动确定", self.skill)
        self.assertIn("<case_dir>/tcl/design.tcl", self.skill)
        self.assertIn("<case_dir>/tcl/<tool>/mmmc.tcl", self.skill)
        self.assertIn("复制并归档", self.skill)

    def test_excel_gate_names_script_and_semantic_review_source(self) -> None:
        self.assertIn("scripts/test_plan_validator.py", self.skill)
        self.assertIn("references/specs/test-plan-rules.md", self.skill)
        self.assertIn("执行脚本结构检查", self.skill)
        self.assertIn("执行 Agent 语义审查", self.skill)
        self.assertIn("两项均通过后", self.skill)


if __name__ == "__main__":
    unittest.main()
