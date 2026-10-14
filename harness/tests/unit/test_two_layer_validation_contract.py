from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


class TwoLayerValidationContractTests(unittest.TestCase):
    def test_validation_plan_defines_environment_and_e2e_layers(self) -> None:
        text = (ROOT / "harness" / "references" / "test-plan.md").read_text(encoding="utf-8")
        self.assertIn("Layer 1：Skill 环境、工具与启动验证", text)
        self.assertIn("Layer 2：端到端用户功能与输出验证", text)
        self.assertIn("输入", text)
        self.assertIn("预期输出", text)

    def test_project_gate_is_not_embedded_in_runtime_skill(self) -> None:
        text = (ROOT / "skill" / "SKILL.md").read_text(encoding="utf-8")
        self.assertNotIn("环境、工具与启动", text)
        self.assertNotIn("端到端测试集", text)
        self.assertNotIn("function.json", text)

    def test_e2e_dataset_contract_is_versioned_and_deterministic(self) -> None:
        text = (ROOT / "harness" / "references" / "e2e-test-set.md").read_text(encoding="utf-8")
        for required in (
            "case_id",
            "input",
            "expected_output",
            "comparison",
            "fixtures",
            "actual_output",
        ):
            self.assertIn(f"`{required}`", text)
        self.assertIn("版本", text)
        self.assertIn("不得由 Agent 自由判断", text)

    def test_static_output_checks_are_nested_under_layer_2(self) -> None:
        text = (ROOT / "harness" / "references" / "test-plan.md").read_text(encoding="utf-8")
        self.assertIn("Excel 规范检查和 TCL 规范检查", text)
        self.assertIn("第二层的内部检查", text)


if __name__ == "__main__":
    unittest.main()
