"""Current resource migration contract; no dependency on retired design trees."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[3]


class CurrentResourceContractTests(unittest.TestCase):
    def test_management_source_has_portable_complete_process_inputs(self):
        data = json.loads((ROOT / 'skill/assets/输入件管理表.json').read_text())
        self.assertEqual({'smic180'}, set(data))
        process = data['smic180']
        self.assertEqual({'tech_dir', 'lef_files', 'lib_files'}, set(process))
        self.assertTrue(process['tech_dir'].startswith('$env(PV_ROOT)/'))
        for field in ('lef_files', 'lib_files'):
            self.assertIsInstance(process[field], list)
            self.assertTrue(process[field])
            for value in process[field]:
                self.assertTrue(value.startswith(process['tech_dir'] + '/'))
                self.assertNotIn('..', value.split('/'))

    def test_both_tools_have_connected_templates(self):
        base = ROOT / 'skill/assets/templates/tool_cmd'
        self.assertTrue((base / 'common/design.tcl').is_file())
        for tool in ('optimus', 'itools'):
            for name in ('init.tcl', 'mmmc.tcl'):
                text = (base / tool / name).read_text()
                self.assertTrue(text.strip())
                self.assertNotIn('/Users/', text)
                self.assertNotIn('/home/', text)
            self.assertIn('$liberty_files', (base / tool / 'mmmc.tcl').read_text())
            self.assertIn('$sdc_files', (base / tool / 'mmmc.tcl').read_text())

    def test_input_gate_uses_management_table_and_current_templates(self):
        text = (ROOT / 'skill/SKILL.md').read_text()
        for token in ('assets/输入件管理表.json', '`smic180`',
                      'assets/templates/tool_cmd/common/design.tcl',
                      'assets/templates/tool_cmd/<tool>/'):
            self.assertIn(token, text)
        self.assertNotIn('references/input/design_input_tcl/', text)

    def test_migrated_gate_tests_do_not_read_retired_resources(self):
        for name in ('test_design_input_selection.py', 'test_fixed_smic180.py',
                     'test_itools_defaults.py'):
            text = (ROOT / 'harness/tests/unit' / name).read_text()
            for obsolete in ('assets/defaults', '"defaults"', 'references/input/design_input_tcl'):
                self.assertNotIn(obsolete, text, name)


class CentralInputGateTests(unittest.TestCase):
    def test_current_template_is_accepted_but_wrong_process_or_libraries_fail(self):
        import importlib.util
        import sys
        spec = importlib.util.spec_from_file_location('current_gate_validator', ROOT / 'skill/scripts/tcl_convention_validator.py')
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        template = (ROOT / 'skill/assets/templates/tool_cmd/common/design.tcl').read_text()
        self.assertTrue(module.matches_central_design_source(template))
        for original, replacement in (('/smic180/', '/smic28/'),
                                      ('smic18_5lm_grid.lef', 'wrong.lef'),
                                      ('typical.lib', 'wrong.lib')):
            with self.subTest(original=original):
                self.assertFalse(module.matches_central_design_source(template.replace(original, replacement)))
        self.assertFalse(module.matches_central_design_source('# ' + template.replace('\n', '\n# ')))
