"""Independent boundary tests; no protected fixtures or helpers."""
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location('pv_log_limit_validator', ROOT / 'skill/scripts/tcl_convention_validator.py')
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)


class PvLogCommandLimitTests(unittest.TestCase):
    def diagnostics(self, block):
        result = []
        text = 'pv_check_log {' + block + '} -name limit\n'
        VALIDATOR._validate_run_script(text, Path('run.tcl'), 'pos', [], result)
        return [d for d in result if d.rule_id == 'TCL-CHECKPOINT-007']

    def test_four_commands_pass(self):
        self.assertEqual(self.diagnostics('report_a\nreport_b; report_c\nreport_d'), [])

    def test_five_commands_fail_with_location(self):
        result = self.diagnostics('report_a; report_b; report_c; report_d; report_e')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].line, 1)
        self.assertIn('5', result[0].message)

    def test_comments_empty_statements_and_continuations_do_not_count(self):
        self.assertEqual(self.diagnostics('# ignored; ignored\nreport_a \\\n -x 1\n;\nreport_b\nreport_c\nreport_d\n'), [])

    def test_quoted_braced_and_bracket_separators_do_not_split_outer_commands(self):
        block = 'report_a "x;y"\nreport_b {x;y}\nreport_c [list x; list y]\nreport_d'
        self.assertEqual(self.diagnostics(block), [])
        self.assertEqual(len(self.diagnostics(block + '\nreport_e')), 1)

    def test_escaped_separators_do_not_split(self):
        self.assertEqual(self.diagnostics('report_a x\\;y\nreport_b\nreport_c\nreport_d'), [])
