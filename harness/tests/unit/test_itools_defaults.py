"""Current single-view MMMC templates preserve tool-specific command dialects."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / 'skill/assets/templates/tool_cmd'


class ItoolsDefaultsTests(unittest.TestCase):
    def test_default_mmmc_matches_single_view_contract(self):
        text = (BASE / 'itools/mmmc.tcl').read_text()
        for name in ('create_library_set', 'create_rc_corner', 'create_delay_corner',
                     'create_constraint_mode', 'create_analysis_view', 'set_analysis_view'):
            self.assertEqual(1, sum(line.startswith(name + ' ') for line in text.splitlines()), name)

    def test_default_mmmc_preserves_library_corner_mode_view_connections(self):
        text = (BASE / 'itools/mmmc.tcl').read_text()
        for line in ('create_library_set -name LS_TYP -timing $liberty_files',
                     'create_rc_corner -name RC_FUNCTIONAL',
                     'create_delay_corner -name DC_TYP -library_set LS_TYP -rc_corner RC_FUNCTIONAL',
                     'create_constraint_mode -name CM_FUNC -sdc_files $sdc_files',
                     'create_analysis_view -name AV_TYP -constraint_mode CM_FUNC -delay_corner DC_TYP',
                     'set_analysis_view -setup {AV_TYP} -hold {AV_TYP}'):
            self.assertIn(line, text.splitlines())

    def test_itools_and_optimus_templates_use_distinct_command_dialects(self):
        itools = (BASE / 'itools/mmmc.tcl').read_text()
        optimus = (BASE / 'optimus/mmmc.tcl').read_text()
        for command in ('create_library_set', 'create_delay_corner', 'create_constraint_mode'):
            self.assertIn(command, itools)
            self.assertNotIn(command, optimus)
        for command in ('create_lib_set', 'create_analysis_corner', 'create_analysis_mode', 'set_views_status'):
            self.assertIn(command, optimus)
            self.assertNotIn(command, itools)
        self.assertIn('set_views_status -setup {AV_TYP} -hold {AV_TYP}', optimus)

    def test_skill_routes_generation_to_corresponding_tool_templates(self):
        text = (ROOT / 'skill/SKILL.md').read_text()
        self.assertIn('assets/templates/tool_cmd/<tool>/', text)
        self.assertIn('对应目标工具', text)
        for tool in ('itools', 'optimus'):
            self.assertIn(f'assets/templates/tool_cmd/{tool}/init.tcl', text)
            self.assertIn(f'assets/templates/tool_cmd/{tool}/mmmc.tcl', text)
