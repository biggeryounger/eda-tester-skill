from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location("eda_validator_delivery", ROOT / "skill" / "scripts" / "validate.py")
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load unified validator")
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)


def check(check_id: str, status: str) -> dict[str, object]:
    return {"id": check_id, "status": status, "diagnostics": []}


class DeliveryGateTests(unittest.TestCase):
    def run_gate(self, plan_status: str, tcl_checks: list[dict[str, object]]) -> tuple[dict[str, object], mock.Mock]:
        plan_validator = mock.Mock()
        plan_validator.plan_report.return_value = {
            "status": plan_status,
            "checks": [check("L1", plan_status)],
            "diagnostics": [],
        }
        tcl_runner = mock.Mock(return_value={
            "status": "PASS",
            "checks": tcl_checks,
            "diagnostics": [],
        })
        with mock.patch.object(VALIDATOR, "load_test_plan_validator", return_value=plan_validator), mock.patch.object(
            VALIDATOR, "tcl_report", tcl_runner
        ):
            report = VALIDATOR.delivery_report(Path("plan.xlsx"), [Path("pos001_smoke")])
        return report, tcl_runner

    def test_excel_and_tcl_checks_pass(self) -> None:
        report, tcl_runner = self.run_gate("PASS", [check("L2", "PASS")])
        self.assertEqual("PASS", report["status"])
        self.assertEqual(["PASS", "PASS"], [item["status"] for item in report["checks"]])
        tcl_runner.assert_called_once()

    def test_layer_1_failure_skips_tcl_check(self) -> None:
        report, tcl_runner = self.run_gate("FAIL", [])
        self.assertEqual("FAIL", report["status"])
        self.assertEqual(["FAIL", "SKIPPED"], [item["status"] for item in report["checks"]])
        tcl_runner.assert_not_called()

    def test_tcl_failure_fails_delivery(self) -> None:
        report, _ = self.run_gate("PASS", [check("L2", "FAIL")])
        self.assertEqual("FAIL", report["status"])
        self.assertEqual(["PASS", "FAIL"], [item["status"] for item in report["checks"]])

    def test_multiple_cases_are_aggregated(self) -> None:
        report, _ = self.run_gate(
            "PASS",
            [check("L2", "PASS"), check("L2", "FAIL")],
        )
        self.assertEqual(["L1", "L2"], [item["id"] for item in report["checks"]])
        self.assertEqual(["PASS", "FAIL"], [item["status"] for item in report["checks"]])


if __name__ == "__main__":
    unittest.main()
