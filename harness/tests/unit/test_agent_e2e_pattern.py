from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
REFERENCE = ROOT / "harness" / "references" / "agent-e2e-pattern.md"
DATASET_REFERENCE = ROOT / "harness" / "references" / "e2e-test-set.md"


class AgentE2EPatternTests(unittest.TestCase):
    def test_reference_defines_the_agent_execution_boundary(self) -> None:
        text = REFERENCE.read_text(encoding="utf-8")
        for required in (
            "codex exec --json",
            "codex exec resume",
            "$eda-tester-skill",
            "模型负责",
            "脚本负责",
            "不得让模型自行裁决",
        ):
            self.assertIn(required, text)

    def test_reference_defines_repeatable_structure_and_protocol(self) -> None:
        text = REFERENCE.read_text(encoding="utf-8")
        for required in (
            "case.json",
            "run_case.py",
            "run_agent_case.py",
            "input/",
            "expected_output/",
            "WAIT-STRATEGY",
            "WAIT-DESIGN-CONFIRMATION",
            "DELIVERED",
            "thread.started",
            "session ID",
        ):
            self.assertIn(required, text)

    def test_reference_defines_deterministic_verdicts_and_failure_classes(self) -> None:
        text = REFERENCE.read_text(encoding="utf-8")
        for required in (
            "PASS",
            "FAIL",
            "TOOL_UNAVAILABLE",
            "退出码 `0`",
            "退出码 `1`",
            "退出码 `2`",
            "独立验证",
            "禁止项",
        ):
            self.assertIn(required, text)

    def test_reference_contains_a_copyable_case_checklist_and_current_example(self) -> None:
        text = REFERENCE.read_text(encoding="utf-8")
        self.assertIn("新增用例清单", text)
        self.assertIn("optimus_check_design_data_full_workflow", text)
        self.assertIn("./init.sh test agent-e2e", text)
        self.assertIn("agent-e2e-pattern.md", DATASET_REFERENCE.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
