"""Standalone iTools checker integration, without EDA execution."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
CHECK = ROOT / 'skill/scripts/itools_check.py'


class ItoolsManualCheckTests(unittest.TestCase):
    def run_check(self, text, *args):
        with tempfile.TemporaryDirectory() as tmp:
            script = Path(tmp) / 'case.tcl'
            script.write_text(text)
            result = subprocess.run([sys.executable, str(CHECK), str(script), '--format', 'json', *args], cwd=tmp, capture_output=True, text=True)
            self.assertFalse((Path(tmp) / 'SHOULD_NOT_EXIST').exists())
            return result

    def test_valid_and_invalid_commands(self):
        result = self.run_check('ecoDeleteRepeater -inst U1\n')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)[0]['summary']['error'], 0)
        for text, code in [('ecoDeleteRepeater', 'REQUIRED_OPTION'), ('setEcoMode -batchMode maybe', 'INVALID_ENUM'), ('ecoChangeCell -inst U1 -upsize -downsize', 'OPTION_CHOICE'), ('ecoDeleteRepeater -typo', 'UNKNOWN_OPTION')]:
            result = self.run_check(text)
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn(code, {d['code'] for d in json.loads(result.stdout)[0]['diagnostics']})

    def test_gaps_and_no_execution(self):
        result = self.run_check('exec touch SHOULD_NOT_EXIST\necoDeleteRepeater -inst $instance\n')
        report = json.loads(result.stdout)[0]
        self.assertIn('UNRESOLVED', {d['code'] for d in report['diagnostics']})
        self.assertIn('UNLISTED_COMMAND', {d['code'] for d in report['diagnostics']})
        self.assertFalse((ROOT / 'SHOULD_NOT_EXIST').exists())

    def test_missing_rules_and_portable_source(self):
        self.assertEqual(self.run_check('ecoDeleteRepeater', '--rules', '/nonexistent/rules.json').returncode, 2)
        rules = json.loads((ROOT / 'skill/references/itools-syntax/rules.json').read_text())
        self.assertEqual(len(rules['commands']), 1333)
        self.assertFalse(Path(rules['source']['path']).is_absolute())

    def test_workflow_requires_checker_and_gap_review(self):
        doc = (ROOT / 'skill/SKILL.md').read_text()
        self.assertIn('scripts/itools_check.py', doc)
        self.assertIn('rules/output-rules.md', doc)
        doc += (ROOT / 'skill/rules/output-rules.md').read_text()
        self.assertIn('PARTIAL_RULES', doc)
        self.assertIn('references/itools-syntax/index.md', doc)

    def test_multiple_files_and_coverage(self):
        with tempfile.TemporaryDirectory() as tmp:
            a, b = Path(tmp) / 'a.tcl', Path(tmp) / 'b.tcl'
            a.write_text('ecoDeleteRepeater -inst U1')
            b.write_text('ecoDeleteRepeater')
            result = subprocess.run([sys.executable, str(CHECK), str(a), str(b), '--format', 'json'], cwd=tmp, capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            reports = json.loads(result.stdout)
            self.assertEqual(len(reports), 2)
            self.assertEqual(reports[0]['summary']['error'], 0)
            self.assertGreater(reports[1]['summary']['error'], 0)
            coverage = subprocess.run([sys.executable, str(CHECK), '--coverage'], cwd=tmp, capture_output=True, text=True)
            self.assertEqual(coverage.returncode, 0)
            self.assertEqual(json.loads(coverage.stdout)['commands'], 1333)
