"""The single registered process supplies both tool templates without selection."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[3]


class FixedSmic180Tests(unittest.TestCase):
    def test_workflow_fixes_process_without_a_technology_selection_gate(self):
        text = (ROOT / 'skill/SKILL.md').read_text()
        section = text.split('### 4.', 1)[1].split('### 5.', 1)[0]
        self.assertIn('assets/输入件管理表.json', section)
        self.assertIn('`smic180` 对象', section)
        self.assertNotIn('确认所选 design 和 tech', section)
        self.assertNotIn('WAIT-DESIGN-TECH-SELECTION', text)
        data = json.loads((ROOT / 'skill/assets/输入件管理表.json').read_text())
        self.assertEqual(['smic180'], list(data))

    def test_process_paths_are_complete_and_have_no_alternate_process(self):
        process = json.loads((ROOT / 'skill/assets/输入件管理表.json').read_text())['smic180']
        for field in ('tech_dir', 'lef_files', 'lib_files'):
            self.assertTrue(process[field])
        self.assertIn('/smic180/', process['tech_dir'])
        for path in process['lef_files'] + process['lib_files']:
            self.assertTrue(path.startswith(process['tech_dir'] + '/'))
            self.assertTrue(path.startswith('$env(PV_ROOT)/'))

    def test_process_paths_match_common_design_and_both_tools(self):
        data = json.loads((ROOT / 'skill/assets/输入件管理表.json').read_text())['smic180']
        base = ROOT / 'skill/assets/templates/tool_cmd'
        design = (base / 'common/design.tcl').read_text()
        self.assertIn(data['tech_dir'], design)
        for lef in data['lef_files']:
            self.assertIn(lef, design)
        for lib in data['lib_files']:
            self.assertIn(lib.replace(data['tech_dir'], '$tech_dir'), design)
        for tool in ('optimus', 'itools'):
            text = (base / tool / 'mmmc.tcl').read_text()
            self.assertIn('$liberty_files', text)
            self.assertIn('$sdc_files', text)
