from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CASE = ROOT / "tests" / "regression" / "optimus" / "write_def_smoke"


class RegressionCorpusTests(unittest.TestCase):
    def test_write_def_smoke_input_and_coverage_contract(self) -> None:
        request = json.loads((CASE / "request.json").read_text(encoding="utf-8"))
        requirements = json.loads((CASE / "requirements.json").read_text(encoding="utf-8"))
        scenarios = json.loads((CASE / "expected_scenarios.json").read_text(encoding="utf-8"))["scenarios"]
        command_spec = (CASE / "command-spec.txt").read_text(encoding="utf-8")

        self.assertEqual(request["tool"], "Optimus")
        self.assertEqual(request["tool_version"], "21.1")
        self.assertEqual(request["strategies"], ["Smoke case"])
        self.assertEqual(
            requirements["write_def"],
            [
                "<file_name>",
                "-help",
                "-floorplan",
                "-no_early_route_wire",
                "-no_logical_stdcell",
                "-no_routing",
                "-no_scanchain",
                "-no_special_net",
            ],
        )
        for requirement in requirements["write_def"]:
            self.assertIn(requirement, command_spec)
        self.assertEqual(
            [scenario["用例路径"] for scenario in scenarios],
            [
                "pos001_required_file",
                "pos002_floorplan",
                "pos003_exclude_optional_content",
                "pos004_help",
            ],
        )
        searchable = "\n".join(
            f'{scenario["用例描述"]}\n{scenario["用例步骤"]}\n{scenario["备注"]}' for scenario in scenarios
        )
        for requirement in requirements["write_def"]:
            self.assertIn(requirement, searchable)

    def test_write_def_smoke_expected_plan_passes_layer_1(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workbook = Path(temporary) / "write_def_smoke.xlsx"
            generated = subprocess.run(
                [
                    "python3",
                    "scripts/generate_test_plan.py",
                    str(CASE / "expected_scenarios.json"),
                    str(workbook),
                    "--requirements",
                    str(CASE / "requirements.json"),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(generated.returncode, 0, generated.stderr)
            validated = subprocess.run(
                [
                    "python3",
                    "scripts/validate.py",
                    "plan",
                    str(workbook),
                    "--requirements",
                    str(CASE / "requirements.json"),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(validated.returncode, 0, validated.stdout + validated.stderr)


if __name__ == "__main__":
    unittest.main()
