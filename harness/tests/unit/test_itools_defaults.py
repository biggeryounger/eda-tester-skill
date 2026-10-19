from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


class ItoolsDefaultsTests(unittest.TestCase):
    def test_default_mmmc_matches_four_view_contract(self) -> None:
        mmmc = (ROOT / "skill" / "assets" / "defaults" / "itools" / "mmmc.tcl").read_text(encoding="utf-8")
        self.assertEqual(4, mmmc.count("create_library_set "))
        self.assertEqual(4, mmmc.count("create_rc_corner "))
        self.assertEqual(4, mmmc.count("create_delay_corner "))
        self.assertEqual(2, mmmc.count("create_constraint_mode "))
        self.assertEqual(4, mmmc.count("create_analysis_view "))
        self.assertEqual(1, mmmc.count("set_analysis_view "))

    def test_default_mmmc_preserves_corner_and_view_mappings(self) -> None:
        mmmc = (ROOT / "skill" / "assets" / "defaults" / "itools" / "mmmc.tcl").read_text(encoding="utf-8")
        for value in (
            "slowLibSet_40c",
            "fastLibSet_40c",
            "slowLibSet_125c",
            "fastLibSet_125c",
            "delay_corner_rcbest",
            "delay_corner_rcworst",
            "delay_corner_cbest",
            "delay_corner_cworst",
            "create_constraint_mode -name func_max_mode -sdc_files $design_dir/floorplan.sdc",
            "create_constraint_mode -name func_min_mode -sdc_files $design_dir/floorplan.sdc",
            "set_analysis_view -setup [list func_rcworst func_cworst] -hold [list func_rcbest func_cbest]",
        ):
            self.assertIn(value, mmmc)

    def test_itools_and_optimus_defaults_use_distinct_command_dialects(self) -> None:
        itools = (ROOT / "skill" / "assets" / "defaults" / "itools" / "mmmc.tcl").read_text(encoding="utf-8")
        optimus = (ROOT / "skill" / "assets" / "defaults" / "optimus" / "mmmc.tcl").read_text(encoding="utf-8")
        self.assertIn("create_library_set", itools)
        self.assertIn("create_delay_corner", itools)
        self.assertNotIn("create_lib_set", itools)
        self.assertIn("create_lib_set", optimus)
        self.assertIn("create_analysis_corner", optimus)

    def test_skill_routes_selected_mmmc_by_target_tool_dialect(self) -> None:
        skill = (ROOT / "skill" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("目标工具方言", skill)
        self.assertIn("不得跨工具替换", skill)


if __name__ == "__main__":
    unittest.main()
