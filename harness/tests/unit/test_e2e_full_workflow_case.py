from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CASE_DIR = ROOT / "harness" / "tests" / "e2e" / "optimus_check_design_data_full_workflow"


class FullWorkflowE2ECaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.case = json.loads((CASE_DIR / "case.json").read_text(encoding="utf-8"))
        self.trace = json.loads(
            (CASE_DIR / "expected_output" / "workflow_trace.json").read_text(encoding="utf-8")
        )

    def test_declares_text_spec_and_user_prompt_as_inputs(self) -> None:
        self.assertEqual("1.0", self.case["schema_version"])
        self.assertEqual("optimus_check_design_data_full_workflow", self.case["case_id"])
        self.assertEqual("run_case.py", self.case["automation"]["runner"])
        self.assertEqual("run_agent_case.py", self.case["automation"]["agent_runner"])
        self.assertFalse(self.case["automation"]["requires_human_input"])
        self.assertTrue((CASE_DIR / self.case["automation"]["runner"]).is_file())
        self.assertTrue((CASE_DIR / self.case["automation"]["agent_runner"]).is_file())
        self.assertEqual("scenario_1_command_spec", self.case["input"]["workflow_scenario"])
        self.assertEqual("input/command-spec.txt", self.case["input"]["command_spec"])
        self.assertEqual("input/user-prompt.txt", self.case["input"]["user_prompt"])
        self.assertTrue((CASE_DIR / self.case["input"]["command_spec"]).read_text(encoding="utf-8").strip())
        self.assertTrue((CASE_DIR / self.case["input"]["user_prompt"]).read_text(encoding="utf-8").strip())

    def test_fixture_hashes_are_exact_and_portable(self) -> None:
        for fixture in self.case["fixtures"]:
            relative = Path(fixture["path"])
            self.assertFalse(relative.is_absolute())
            digest = hashlib.sha256((CASE_DIR / relative).read_bytes()).hexdigest()
            self.assertEqual(fixture["sha256"], digest)

    def test_expects_every_scenario_one_workflow_step_in_order(self) -> None:
        expected_steps = [
            "ROUTE-SCENARIO-1",
            "PARSE-COMMAND-SPEC",
            "WAIT-STRATEGY",
            "BUILD-REQUIREMENTS-SCENARIOS",
            "REPORT-COVERAGE",
            "GENERATE-TEST-PLAN",
            "VALIDATE-TEST-PLAN-STRUCTURE",
            "REVIEW-TEST-PLAN-SEMANTICS",
            "WAIT-DESIGN-CONFIRMATION",
            "RESOLVE-DESIGN-TECH",
            "GENERATE-TCL",
            "VALIDATE-TCL-STATIC",
            "REVIEW-TCL-SEMANTICS",
            "DELIVER",
        ]
        self.assertEqual(expected_steps, [step["id"] for step in self.trace["steps"]])
        self.assertTrue(all(step["required"] for step in self.trace["steps"]))
        self.assertTrue(all(step["evidence"] for step in self.trace["steps"]))

    def test_wait_gates_have_explicit_user_responses(self) -> None:
        turns = {turn["id"]: turn for turn in self.case["input"]["conversation"]}
        self.assertEqual("assistant", turns["wait_strategy"]["role"])
        self.assertEqual("user", turns["select_strategy"]["role"])
        self.assertEqual(["Smoke case", "正向覆盖", "负向覆盖"], turns["select_strategy"]["selections"])
        self.assertEqual("assistant", turns["wait_design_confirmation"]["role"])
        self.assertEqual("user", turns["confirm_design"]["role"])
        self.assertTrue(turns["confirm_design"]["approved"])
        self.assertEqual("riscv", turns["confirm_design"]["design"])
        self.assertEqual("SMIC28", turns["confirm_design"]["tech"])

    def test_expected_outputs_and_comparisons_cover_plan_tcl_and_trace(self) -> None:
        expected_ids = {item["id"] for item in self.case["expected_output"]["items"]}
        comparison_targets = {item["target"] for item in self.case["comparison"]}
        self.assertEqual(
            {"structured_spec", "coverage_report", "test_plan", "tcl_cases", "workflow_trace"},
            expected_ids,
        )
        self.assertEqual(expected_ids, comparison_targets)
        self.assertEqual("temporary", self.case["actual_output"]["retention"])


if __name__ == "__main__":
    unittest.main()
