from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PATH = ROOT / 'skill/scripts/tcl_convention_validator.py'
SPEC = importlib.util.spec_from_file_location('pv_direct_validator', PATH)
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)
RULE = 'TCL-CHECKPOINT-008'


class PvDirectCallTests(unittest.TestCase):
    def diagnostics(self, text):
        items = []
        VALIDATOR._validate_pv_direct_calls(text, Path('run.tcl'), items)
        return [item for item in items if item.rule_id == RULE]

    def test_direct_calls_and_literal_mentions_pass(self):
        for text in (
            'pv_check_log {report_qor} -name state\n',
            'pv_check_golden ./out/state.txt -golden golden/state.txt\n',
            '::pv_check_log {puts hi} -name state\n',
            '# set rc [pv_check_log {report_qor}]\nputs {pv_check_log is documentation}\n',
            'set example {set rc [pv_check_log {report_qor}]}\n',
            'pv_check_log {puts {[not_a_command]}} -name literal\n',
        ):
            with self.subTest(text=text):
                self.assertEqual([], self.diagnostics(text))

    def test_return_capture_and_condition_wrappers_fail(self):
        for function, args in (('pv_check_log', '{report_qor} -name state'),
                               ('pv_check_golden', './out/state.txt')):
            call = f'{function} {args}'
            for text in (
                f'set check_rc [{call}]\n',
                f'set arbitrary_name [\n{call}\n]\n',
                f'if {{[{call}] != 0}} {{error failed}}\n',
                f'if {{0}} {{puts unused}} elseif {{[{call}]}} {{error failed}}\n',
                f'puts "result=[{call}]"\n',
                f'catch {{{call}}} rc\n',
                f'proc wrapper {{}} {{{call}}}\n',
                f'eval {{{call}}}\n',
                f'expr {{[{call}] == 0}}\n',
                f'if {{1}} {{set rc [{call}]}}\n',
                f'switch $mode {{x {{set rc [{call}]}}}}\n',
                f'apply {{{{}} {{{call}}}}}\n',
                f'namespace eval checks {{set rc [{call}]}}\n',
            ):
                with self.subTest(text=text):
                    self.assertTrue(self.diagnostics(text), text)

    def test_multiline_location(self):
        items = self.diagnostics('# intro\nset rc [\n  pv_check_log {puts hi} -name stage\n]\n')
        self.assertEqual(3, items[0].line)

    def test_valid_case_passes_default_cli_and_wrapped_variant_fails(self):
        from tests.unit.test_tcl_convention_validator import TclConventionValidatorTests
        fixture = TclConventionValidatorTests()
        fixture.setUp()
        try:
            case = fixture.build()
            command = [sys.executable, str(PATH), str(case)]
            cp = subprocess.run(command, text=True, capture_output=True)
            self.assertEqual(0, cp.returncode, cp.stdout + cp.stderr)
            run = case / 'tcl/optimus/run.tcl'
            text = run.read_text()
            text = text.replace('pv_check_log {report_qor} -name smoke -filter {^Date} -match {WNS|TNS}',
                                'set check_rc [pv_check_log {report_qor} -name smoke -filter {^Date} -match {WNS|TNS}]')
            run.write_text(text)
            cp = subprocess.run(command, text=True, capture_output=True)
            self.assertNotEqual(0, cp.returncode)
            self.assertIn(RULE, cp.stdout)
        finally:
            fixture.tearDown()

    def test_default_cli_blocks_helper_wrapper(self):
        with tempfile.TemporaryDirectory() as directory:
            case = Path(directory) / 'pos001_direct_call'
            tool = case / 'tcl/itools'
            tool.mkdir(parents=True)
            (case / 'tcl/design.tcl').write_text('set init_top_name top\n')
            (tool / 'mmmc.tcl').write_text('')
            (tool / 'run.tcl').write_text('pv_check_log {puts hi} -name state\n')
            (tool / 'check.tcl').write_text('set result [pv_check_golden ./out/result]\n')
            cp = subprocess.run([sys.executable, str(PATH), str(case)], text=True, capture_output=True)
            self.assertNotEqual(0, cp.returncode)
            report = json.loads(cp.stdout)
            hits = [d for d in report['diagnostics'] if d['rule_id'] == RULE]
            self.assertTrue(hits, report)
            self.assertTrue(hits[0]['file'].endswith('check.tcl'))


if __name__ == '__main__':
    unittest.main()
