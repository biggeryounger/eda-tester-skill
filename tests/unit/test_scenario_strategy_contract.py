from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class ScenarioStrategyContractTests(unittest.TestCase):
    def test_skill_requires_maximum_compatible_coverage_per_case(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Maximize compatible test-point coverage per case", skill)
        self.assertIn("Do not create one case per option", skill)

    def test_strategy_defines_merge_and_split_boundaries(self) -> None:
        strategy = (ROOT / "references" / "test-strategies.md").read_text(encoding="utf-8")
        self.assertIn("单用例多测试点", strategy)
        self.assertIn("前置设计状态一致", strategy)
        self.assertIn("选项互斥或组合非法", strategy)
        self.assertIn("预期结果的性质不同", strategy)
        self.assertIn("故障定位", strategy)

    def test_excel_fields_require_numbered_point_mapping(self) -> None:
        strategy = (ROOT / "references" / "test-strategies.md").read_text(encoding="utf-8")
        self.assertIn("测试点 1", strategy)
        self.assertIn("步骤 1", strategy)
        self.assertIn("预期 1", strategy)

    def test_user_must_confirm_test_design_before_artifact_generation(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        strategy = (ROOT / "references" / "test-strategies.md").read_text(encoding="utf-8")
        self.assertIn("Wait for explicit user confirmation", skill)
        self.assertIn("Do not generate any TCL file before confirmation", skill)
        self.assertLess(skill.index("Serialize the designed rows"), skill.index("Wait for explicit user confirmation"))
        self.assertLess(skill.index("Wait for explicit user confirmation"), skill.index("Generate one case directory per Excel row"))
        self.assertIn("用例设计确认门禁", strategy)
        self.assertIn("确认用例设计可用于生成 TCL", strategy)
        self.assertIn("选择测试策略不等于确认用例设计", strategy)


if __name__ == "__main__":
    unittest.main()
