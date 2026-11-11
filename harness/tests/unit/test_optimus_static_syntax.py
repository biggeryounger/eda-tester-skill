"""Automated source-snapshot and static checker boundary tests, no EDA license."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / 'skill/scripts'
sys.path.insert(0, str(SCRIPTS))


class OptimusStaticSyntaxTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import optimus_syntax
        cls.checker = optimus_syntax

    def check(self, text, **kwargs):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'run.tcl'
            path.write_text(text)
            return self.checker.check_scripts([path], **kwargs)

    def codes(self, report):
        return {d['rule_id'] for c in report['checks'] for d in c['diagnostics']}

    def test_corpus_has_exact_source_and_all_rows(self):
        db = self.checker.load_database()
        self.assertEqual(len(db['commands']), 464)
        self.assertEqual(db['source_sha256'], '1fa52ed045ae3d37a17fb51752478d7f2a28c0a9bbf3741fd77420e0fa07018b')
        self.assertEqual(sum(len(c['parameters']) for c in db['commands'].values()), 2115)
        self.assertIsNone(db['tool_version'])
        self.assertEqual(db, self.checker.load_database())

    def test_valid_options_and_positionals(self):
        r = self.check('add_instance -cell BUF -name u1 -orientation R0\nread_def floorplan.def\nreport_qor -place\n')
        self.assertEqual(r['status'], 'PASS', r)

    def test_unknown_command_and_option(self):
        self.assertIn('OPT-CMD-001', self.codes(self.check('report_qorr -place')))
        self.assertIn('OPT-OPTION-001', self.codes(self.check('report_qor -typo')))

    def test_missing_required_and_value(self):
        self.assertIn('OPT-REQUIRED-001', self.codes(self.check('check_design_data -netlist')))
        self.assertIn('OPT-ARG-001', self.codes(self.check('check_design_data -file')))
        self.assertIn('OPT-ARG-001', self.codes(self.check('read_def')))

    def test_enum_integer_range_and_double(self):
        for text in ['add_instance -cell X -name u -orientation INVALID',
                     'add_cell_obs -cell X -layer M1 -mask 2147483648',
                     'add_cell_obs -cell X -layer M1 -mask 1.5',
                     'add_cell_obs -cell X -layer M1 -spacing nope']:
            self.assertIn('OPT-TYPE-001', self.codes(self.check(text)), text)
        self.assertEqual(self.check('add_cell_obs -cell X -layer M1 -spacing -0.5')['status'], 'PASS')

    def test_explicit_stage_constraint(self):
        self.assertIn('OPT-RELATION-001', self.codes(self.check('report_qor')))
        self.assertIn('OPT-RELATION-001', self.codes(self.check('report_qor -place -route')))

    def test_duplicate_is_documentation_gap_not_invented_constraint(self):
        r = self.check('report_qor -place -prefix a -prefix b')
        self.assertEqual(r['status'], 'SPEC-GAP')

    def test_static_dispatch_bodies_are_inspected(self):
        for text in ['switch -- $stage {place {report_qor -typo} default {puts ok}}',
                     'try {report_qor -typo} finally {puts done}',
                     'eval {report_qor -typo}',
                     'uplevel #0 {report_qor -typo}',
                     'apply {{} {report_qor -typo}}']:
            self.assertIn('OPT-OPTION-001', self.codes(self.check(text)), text)
        self.assertIn('TCL-SYNTAX-002', self.codes(self.check('if {1} {puts ok} {2} {puts bad}')))
        self.assertIn('TCL-SYNTAX-002', self.codes(self.check('proc f {{a b c}} {puts ok}')))

    def test_real_tcl_grammar_and_no_execution(self):
        for text in ['report_qor {', 'report_qor "abc', 'set x [report_qor -place', 'report_qor {a}b']:
            self.assertIn('TCL-SYNTAX-001', self.codes(self.check(text)), text)
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'must_not_exist'
            r = self.check('exec touch {' + str(target) + '}\nreport_qor -place')
            self.assertFalse(target.exists())
            self.assertEqual(r['status'], 'SPEC-GAP')

    def test_nested_pv_control_and_substitution_are_checked(self):
        for text in ['pv_check_log {report_qor -typo} -name q',
                     'if {1} {report_qor -typo}',
                     'set x [report_qor -typo]',
                     'proc helper {} {report_qor -typo}\nhelper']:
            self.assertIn('OPT-OPTION-001', self.codes(self.check(text)), text)

    def test_nested_syntax_and_expression(self):
        self.assertIn('TCL-SYNTAX-001', self.codes(self.check('if {1} {set x [}')))
        self.assertIn('TCL-SYNTAX-001', self.codes(self.check('if {1 +} {report_qor -place}')))

    def test_comments_quotes_unicode_and_continuations(self):
        r = self.check('# 中文注释\ncheck_design_data \\\n -file {a;b.rpt}; report_qor -place -prefix "a;b"')
        self.assertEqual(r['status'], 'PASS', r)
        r = self.check('# 中文\nreport_qor -wrong')
        self.assertTrue(any(d['line'] == 2 for c in r['checks'] for d in c['diagnostics']))

    def test_dynamic_values_and_script_expansion_are_not_false_pass(self):
        for text in ['add_instance -cell BUF -name u -orientation $orient',
                     '$cmd -place', 'eval $script', 'report_qor {*}$args']:
            self.assertEqual(self.check(text)['status'], 'SPEC-GAP', text)

    def test_local_procedure_and_builtin_are_recognized(self):
        r = self.check('proc query {} {report_qor -place}\nset x {literal}\nquery\nputs $x')
        self.assertEqual(r['status'], 'PASS', r)

    def test_missing_database_and_tool_are_unavailable(self):
        self.assertEqual(self.check('report_qor -place', database=Path('/missing/database.txt'))['status'], 'TOOL_UNAVAILABLE')
        self.assertEqual(self.check('report_qor -place', tool='itools')['status'], 'TOOL_UNAVAILABLE')

    def test_missing_tcl_library_is_unavailable(self):
        with mock.patch.object(self.checker, 'TclParser', side_effect=RuntimeError('no Tcl 8 library')):
            self.assertEqual(self.check('report_qor -place')['status'], 'TOOL_UNAVAILABLE')

    def test_list_and_geometric_types(self):
        self.assertEqual(self.check('add_cell_obs -cell X -layer M1 -rect {0 0 10 10}')['status'], 'PASS')
        self.assertIn('OPT-TYPE-001', self.codes(self.check('add_cell_obs -cell X -layer M1 -rect {0 0 10}')))

    def test_all_464_commands_have_valid_minimum_and_reject_unknown_options(self):
        from tcl_static_parser import TclParser
        parser = TclParser()
        db = self.checker.load_database()
        def sample(parameter):
            kind, legal = parameter['type'], parameter['legal']
            if parameter['name'] == 'body':
                return '{puts sample}'
            if legal.startswith('{'):
                return '{' + parser.split_list(legal[1:-1])[0] + '}'
            if legal.startswith('['):
                return legal[1:].split(',')[0].strip()
            return {'integer': '0', 'double': '0.0', 'point': '{0 0}',
                    'rect': '{0 0 1 1}', 'rect_dbu': '{0 0 1 1}',
                    'int_list': '{0 1}', 'double_list': '{0 1}',
                    'point_list': '{{0 0} {1 1}}', 'double_list_list': '{{0 1}}',
                    'object_list_list': '{{cell_a cell_b}}', 'list_string_list': '{{a b}}'}.get(kind, 'sample')
        for name, spec in db['commands'].items():
            with self.subTest(command=name):
                words = [name]
                for parameter in spec['parameters']:
                    if parameter['optional']:
                        continue
                    if parameter['name'].startswith('-'):
                        words.append(parameter['name'])
                    if parameter['type'] != 'boolean':
                        words.append(sample(parameter))
                for relation in spec['relations']:
                    words.extend([relation['options'][0]])
                    parameter = next(p for p in spec['parameters'] if p['name'] == relation['options'][0])
                    if parameter['type'] != 'boolean':
                        words.append(sample(parameter))
                report = self.check(' '.join(words))
                self.assertNotIn(report['status'], ('FAIL', 'TOOL_UNAVAILABLE'), report)
                self.assertIn('OPT-OPTION-001', self.codes(self.check(' '.join(words) + ' -__not_real_option')))

    def test_every_table_parameter_is_exercised(self):
        from tcl_static_parser import TclParser
        parser = TclParser()
        db = self.checker.load_database()
        exercised = set()
        def sample(p):
            if p['name'] == 'body':
                return '{puts sample}'
            if p['legal'].startswith('{'):
                return '{' + parser.split_list(p['legal'][1:-1])[0] + '}'
            if p['legal'].startswith('['):
                return p['legal'][1:].split(',')[0].strip()
            return {'integer': '0', 'double': '0', 'point': '{0 0}', 'rect': '{0 0 1 1}',
                    'rect_dbu': '{0 0 1 1}', 'int_list': '{0 1}', 'double_list': '{0 1}', 'point_list': '{{0 0} {1 1}}',
                    'double_list_list': '{{0 1}}', 'object_list_list': '{{a b}}',
                    'list_string_list': '{{a b}}'}.get(p['type'], 'sample')
        for name, spec in db['commands'].items():
            groups = [r['options'] for r in spec['relations'] if r['kind'] == 'exactly_one']
            selections = groups[0] if groups else [None]
            for selected in selections:
                words = [name]
                for p in spec['parameters']:
                    if groups and p['name'] in groups[0] and p['name'] != selected:
                        continue
                    exercised.add((name, p['name']))
                    if p['name'].startswith('-'):
                        words.append(p['name'])
                    if p['type'] != 'boolean':
                        words.append(sample(p))
                with self.subTest(command=name, selected=selected):
                    r = self.check(' '.join(words))
                    self.assertNotIn(r['status'], ('FAIL', 'TOOL_UNAVAILABLE'), r)
        self.assertEqual(len(exercised), 2115)

    def test_control_flow_does_not_reuse_stale_literal_assignments(self):
        text = 'set orient R0\nif {$condition} {set orient INVALID}\nadd_instance -cell BUF -name u -orientation $orient'
        self.assertEqual(self.check(text)['status'], 'SPEC-GAP')
        self.assertEqual(self.check('report_qor $args')['status'], 'SPEC-GAP')
        mutation = 'set orient R0\nset ignored [eval {set orient INVALID}]\nadd_instance -cell BUF -name u -orientation $orient'
        self.assertEqual(self.check(mutation)['status'], 'SPEC-GAP')

    def test_expression_substitutions_source_and_empty_inputs(self):
        self.assertIn('OPT-CMD-001', self.codes(self.check('if {[report_qorr]} {puts ok}')))
        self.assertEqual(self.check('source unknown.tcl')['status'], 'SPEC-GAP')
        self.assertEqual(self.checker.check_scripts([])['status'], 'FAIL')
        self.assertIn('TCL-SYNTAX-002', self.codes(self.check('if {1}')))

    def test_end_to_end_complete_positive_case_and_negative_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            case = Path(tmp) / 'pos001_syntax'
            tool = case / 'tcl/optimus'
            tool.mkdir(parents=True)
            (case / 'nith.run').write_text('''### NITH initialization, please do not change this section
### NITH initialization end
nith.input[""] = f"tcl/{nith.PV_TOOL}/run.tcl"
nith_run()
nith_done()
''')
            (case / 'tcl/design.tcl').write_text('''# Generated from central design profile: syntax
set init_top_name syntax
set lef_files chip.lef
set verilog_files chip.v
set lib_files chip.lib
set sdc_files chip.sdc
set def_file chip.def
''')
            (tool / 'mmmc.tcl').write_text('create_lib_set -name slow -timing_lib chip.lib\n')
            run = '''# DESIGN_INIT_BEGIN
source $env(PV_ROOT)/scripts/pv.tcl
source ./tcl/design.tcl
set_options setup.mmmc_file ./tcl/optimus/mmmc.tcl
setup_design
read_def $def_file
# DESIGN_INIT_END
# EXPECT: PASS
# TEST_ACTION
pv_check_log {report_qor -place} -name qor
pv_rpt_checkpoints
exit
'''
            (tool / 'run.tcl').write_text(run)
            command = [sys.executable, str(SCRIPTS / 'tcl_convention_validator.py'), str(case), '--syntax']
            positive = subprocess.run(command, text=True, capture_output=True)
            report = json.loads(positive.stdout)
            self.assertEqual(positive.returncode, 0, report)
            self.assertEqual(report['status'], 'PASS')
            (tool / 'run.tcl').write_text(run.replace('report_qor -place', 'report_qor -typo'))
            negative = subprocess.run(command, text=True, capture_output=True)
            self.assertNotEqual(negative.returncode, 0)
            self.assertIn('OPT-OPTION-001', {d['rule_id'] for d in json.loads(negative.stdout)['diagnostics']})

    def test_unified_cli_reports_three_layers_and_exit_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            case = Path(tmp) / 'pos001_syntax'
            (case / 'tcl/optimus').mkdir(parents=True)
            (case / 'tcl/optimus/run.tcl').write_text('report_qor -typo\n')
            result = subprocess.run([sys.executable, str(SCRIPTS / 'tcl_convention_validator.py'), str(case), '--syntax'], text=True, capture_output=True)
            report = json.loads(result.stdout)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual({x['id'] for x in report['checks'][0]['checks']}, {'TCL-SYNTAX', 'OPTIMUS-COMMANDS', 'TCL-CONVENTIONS'})
            self.assertIn('OPT-OPTION-001', {d['rule_id'] for d in report['diagnostics']})


class NoToolVersionRequirementTests(unittest.TestCase):
    def test_cli_has_no_tool_version_option(self):
        result = subprocess.run([sys.executable, str(SCRIPTS / 'tcl_convention_validator.py'), '--help'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertNotIn('--tool-version', result.stdout)

    def test_workflow_explicitly_does_not_require_version(self):
        text = (ROOT / 'skill/SKILL.md').read_text()
        self.assertIn('rules/input-rules.md', text)
        self.assertIn('不询问或要求工具版本', (ROOT / 'skill/rules/input-rules.md').read_text())
        for relative in ['SKILL.md', 'references/specs/test-plan-rules.md', 'references/specs/tcl-script-rules.md']:
            text = (ROOT / 'skill' / relative).read_text()
            for obsolete in ['版本语法库', '工具版本或命令身份', 'EDA 工具及版本']:
                self.assertNotIn(obsolete, text)
