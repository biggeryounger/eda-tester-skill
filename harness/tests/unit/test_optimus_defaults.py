from __future__ import annotations

import unittest
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "skill"))

from scripts.optimus_defaults import EXAMPLE_PROFILE, resolve_template


class OptimusDefaultsTests(unittest.TestCase):
    def test_missing_design_inputs_are_reported_not_filled_from_example(self) -> None:
        resolved = resolve_template({})
        self.assertEqual("21.1", resolved["values"]["optimus_version"])
        self.assertIsNone(resolved["values"]["lef_path"])
        self.assertIsNone(resolved["values"]["netlist_path"])
        self.assertIsNone(resolved["values"]["top_cell"])
        self.assertEqual(["lef_path", "netlist_path", "def_path", "top_cell"], resolved["missing_required"])

    def test_example_profile_requires_explicit_selection(self) -> None:
        import json
        resolved = resolve_template({}, use_example_profile=True)
        self.assertEqual(["def_path"], resolved["missing_required"])
        self.assertEqual(EXAMPLE_PROFILE, resolved["values"])
        process = json.loads((ROOT / "skill/assets/输入件管理表.json").read_text())["smic180"]
        self.assertEqual(" ".join(process["lef_files"]), EXAMPLE_PROFILE["lef_path"])
        self.assertEqual("./design/input.v", EXAMPLE_PROFILE["netlist_path"])
        self.assertEqual("ddp_partition_top", EXAMPLE_PROFILE["top_cell"])
        self.assertEqual("./tcl/optimus/mmmc.tcl", EXAMPLE_PROFILE["mmmc_path"])
        self.assertTrue(resolved["example_profile_selected"])

    def test_user_values_override_individually(self) -> None:
        resolved = resolve_template(
            {
                "optimus_version": "24.1",
                "top_cell": "chip_top",
                "power_net": "VDD_MAIN",
            }
        )
        self.assertEqual("24.1", resolved["values"]["optimus_version"])
        self.assertEqual("chip_top", resolved["values"]["top_cell"])
        self.assertEqual("VDD_MAIN", resolved["values"]["power_net"])
        self.assertIsNone(resolved["values"]["lef_path"])
        self.assertIn("lef_path", resolved["missing_required"])

    def test_blank_values_are_treated_as_missing(self) -> None:
        resolved = resolve_template({"lef_path": " ", "ground_net": None})
        self.assertIsNone(resolved["values"]["lef_path"])
        self.assertEqual("VSS", resolved["values"]["ground_net"])
        self.assertIn("lef_path", resolved["missing_required"])

    def test_default_tcl_files_are_portable_and_connected(self) -> None:
        base = ROOT / "skill/assets/templates/tool_cmd"
        design = (base / "common/design.tcl").read_text()
        mmmc = (base / "optimus/mmmc.tcl").read_text()
        for value in ('set init_top_name "ddp_partition_top"',
                      'set netlist_file "./design/input.v"', 'set def_file {}',
                      'set liberty_files [list "$tech_dir/synopsys/typical.lib"]'):
            self.assertIn(value, design)
        for command in ("create_lib_set", "create_rc_corner", "create_analysis_corner",
                        "create_analysis_mode", "create_analysis_view", "set_views_status"):
            self.assertEqual(1, sum(line.startswith(command + " ") for line in mmmc.splitlines()))
        self.assertIn("set_views_status -setup {AV_TYP} -hold {AV_TYP}", mmmc)
        for forbidden in ("/Users/", "/home/", "smic28"):
            self.assertNotIn(forbidden, design + mmmc)

    def test_skill_uses_management_table_and_target_tool_templates(self) -> None:
        skill = (ROOT / "skill/SKILL.md").read_text()
        self.assertIn("assets/输入件管理表.json", skill)
        self.assertIn("assets/templates/tool_cmd/<tool>/", skill)
        self.assertIn("对应目标工具", skill)


if __name__ == "__main__":
    unittest.main()
