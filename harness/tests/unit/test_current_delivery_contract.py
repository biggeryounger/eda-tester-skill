"""Current installed Skill must contain its referenced gates and runtime data."""
import importlib.util
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[3]


class CurrentDeliveryContractTests(unittest.TestCase):
    def test_entry_rule_links_resolve_and_keep_generation_gates(self):
        entry = (ROOT / 'skill/SKILL.md').read_text()
        for name in ('input-rules', 'output-rules'):
            relative = f'rules/{name}.md'
            self.assertIn(relative, entry)
            text = (ROOT / 'skill' / relative).read_text()
            for target in re.findall(r'\]\(([^)]+)\)', text):
                self.assertTrue((ROOT / 'skill/rules' / target).is_file(), target)
        output = (ROOT / 'skill/rules/output-rules.md').read_text()
        for token in ('场景覆盖率', '被测选项覆盖率', '未覆盖项', '确认前不得生成 TCL', 'TOOL_UNAVAILABLE'):
            self.assertIn(token, output)

    def test_current_defaults_import_without_deleted_design_profiles(self):
        spec = importlib.util.spec_from_file_location('current_optimus_defaults', ROOT / 'skill/scripts/optimus_defaults.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        resolved = module.resolve_template({})
        self.assertTrue(resolved['missing_required'])
        self.assertIsNone(resolved['values']['netlist_path'])
        self.assertNotIn('smic28', str(module.EXAMPLE_PROFILE).lower())

    def test_required_command_databases_are_packaged(self):
        sys.path.insert(0, str(ROOT / 'skill/scripts'))
        import optimus_syntax
        import json
        db = optimus_syntax.load_database()
        self.assertEqual(464, len(db['commands']))
        data = json.loads((ROOT / 'skill/references/itools-syntax/rules.json').read_text())
        self.assertEqual(1333, len(data['commands']))
