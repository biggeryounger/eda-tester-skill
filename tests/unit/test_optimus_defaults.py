from __future__ import annotations

import unittest
from pathlib import Path

from scripts.optimus_defaults import EXAMPLE_PROFILE, resolve_template


ROOT = Path(__file__).resolve().parents[2]


class OptimusDefaultsTests(unittest.TestCase):
    def test_missing_design_inputs_are_reported_not_filled_from_example(self) -> None:
        resolved = resolve_template({})
        self.assertEqual("21.1", resolved["values"]["optimus_version"])
        self.assertIsNone(resolved["values"]["lef_path"])
        self.assertIsNone(resolved["values"]["netlist_path"])
        self.assertIsNone(resolved["values"]["top_cell"])
        self.assertEqual(["lef_path", "netlist_path", "top_cell"], resolved["missing_required"])

    def test_example_profile_requires_explicit_selection(self) -> None:
        resolved = resolve_template({}, use_example_profile=True)
        self.assertEqual([], resolved["missing_required"])
        self.assertEqual(EXAMPLE_PROFILE, resolved["values"])
        self.assertEqual("21.1", EXAMPLE_PROFILE["optimus_version"])
        self.assertEqual(
            "$env(PV_ROOT)/svn/openedi/design_data/SMIC28/smic28_library/sec28n_12t25od33_1p8m_7ic_1tmc_alpa1_WITH_NDR.lef "
            "$env(PV_ROOT)/svn/openedi/design_data/SMIC28/smic28_library/sc28nhkcp_hsc30p140_rvt_ant.lef",
            EXAMPLE_PROFILE["lef_path"],
        )
        self.assertEqual(
            "$env(PV_ROOT)/svn/openedi/design_data/SMIC28/Itools21.1_lfp_util0.65/riscv_core/floorplan.v.gz",
            EXAMPLE_PROFILE["netlist_path"],
        )
        self.assertEqual("riscv_core", EXAMPLE_PROFILE["top_cell"])
        self.assertEqual("./tcl/optimus/mmmc.tcl", EXAMPLE_PROFILE["mmmc_path"])

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
        defaults_dir = ROOT / "assets" / "defaults" / "optimus"
        design = (defaults_dir / "design.tcl").read_text(encoding="utf-8")
        mmmc = (defaults_dir / "mmmc.tcl").read_text(encoding="utf-8")
        for value in (
            "Itools21.1_lfp_util0.65/riscv_core",
            "smic28_library",
            "set init_top_cell riscv_core",
            "sec28n_12t25od33_1p8m_7ic_1tmc_alpa1_WITH_NDR.lef",
            "sc28nhkcp_hsc30p140_rvt_ant.lef",
            "set netlist $design_dir/floorplan.v.gz",
            "set def $design_dir/floorplan.def.gz",
        ):
            self.assertIn(value, design)
        self.assertIn("create_analysis_view", mmmc)
        self.assertEqual(4, mmmc.count("create_lib_set "))
        self.assertEqual(4, mmmc.count("create_rc_corner "))
        self.assertEqual(4, mmmc.count("create_analysis_corner "))
        self.assertEqual(2, mmmc.count("create_analysis_mode "))
        self.assertEqual(4, mmmc.count("create_analysis_view "))
        self.assertEqual(4, mmmc.count("set_analysis_view_status "))
        for value in (
            "slowLibSet_40c",
            "fastLibSet_40c",
            "slowLibSet_125c",
            "fastLibSet_125c",
            "delay_corner_rcbest",
            "delay_corner_rcworst",
            "delay_corner_cbest",
            "delay_corner_cworst",
            "$design_dir/floorplan.sdc",
            "func_rcworst -active true -setup true -hold false",
            "func_rcbest -active true -setup false -hold true",
        ):
            self.assertIn(value, mmmc)
        self.assertNotIn("/Users/", design + mmmc)
        self.assertNotIn("/home/", design + mmmc)
        self.assertNotIn("set_options", design)

    def test_skill_declares_template_and_explicit_example_semantics(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("assets/defaults/optimus/design.tcl", skill)
        self.assertIn("template", skill.lower())
        self.assertIn("explicitly selects the repository example profile", skill)


if __name__ == "__main__":
    unittest.main()
