from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


class ScenarioStrategyContractTests(unittest.TestCase):
    def test_skill_requires_maximum_compatible_coverage_per_case(self) -> None:
        skill = (ROOT / "skill" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("rules/output-rules.md", skill)
        rules = (ROOT / "skill/rules/output-rules.md").read_text()
        self.assertIn("最大化单用例的兼容测试点覆盖", rules)
        self.assertIn("不得一项 option 一个用例", rules)

    def test_strategy_defines_merge_and_split_boundaries(self) -> None:
        strategy = (ROOT / "skill" / "references" / "test-strategies.md").read_text(encoding="utf-8")
        self.assertIn("单用例多测试点", strategy)
        self.assertIn("前置设计状态一致", strategy)
        self.assertIn("选项互斥或组合非法", strategy)
        self.assertIn("预期结果的性质不同", strategy)
        self.assertIn("故障定位", strategy)

    def test_excel_fields_require_numbered_point_mapping(self) -> None:
        strategy = (ROOT / "skill" / "references" / "test-strategies.md").read_text(encoding="utf-8")
        self.assertIn("测试点 1", strategy)
        self.assertIn("步骤 1", strategy)
        self.assertIn("预期 1", strategy)

    def test_user_must_confirm_test_design_before_artifact_generation(self) -> None:
        skill = (ROOT / "skill" / "SKILL.md").read_text(encoding="utf-8")
        strategy = (ROOT / "skill" / "references" / "test-strategies.md").read_text(encoding="utf-8")
        self.assertIn("rules/output-rules.md", skill)
        rules = (ROOT / "skill/rules/output-rules.md").read_text()
        self.assertIn("确认前不得生成 TCL", rules)
        self.assertIn("等待明确批准", rules)
        self.assertLess(skill.index("### 2."), skill.index("**WAIT-DESIGN-CONFIRMATION**"))
        self.assertLess(skill.index("**WAIT-DESIGN-CONFIRMATION**"), skill.index("### 5."))
        self.assertIn("用例设计确认门禁", strategy)
        self.assertIn("确认用例设计可用于生成 TCL", strategy)
        self.assertIn("选择测试策略不等于确认用例设计", strategy)


if __name__ == "__main__":
    unittest.main()
