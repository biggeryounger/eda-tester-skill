from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[3]


class ProtectedSmokeTests(unittest.TestCase):
    def test_registry_has_ten_unique_loadable_cases(self):
        data = json.loads((ROOT / 'harness/references/protected-smoke.json').read_text())
        cases = data['cases']
        self.assertEqual([f'SMOKE-{n:03d}' for n in range(1, 11)], [c['id'] for c in cases])
        self.assertEqual(10, len({c['test'] for c in cases}))
        for case in cases:
            suite = unittest.defaultTestLoader.loadTestsFromName(case['test'])
            self.assertEqual(1, suite.countTestCases(), case['id'])
            self.assertFalse(unittest.defaultTestLoader.errors)
            self.assertTrue(case['purpose'])
        rules = (ROOT / 'AGENTS.md').read_text()
        self.assertIn('## 受保护冒烟用例', rules)
        self.assertIn('必须先获得用户明确允许', rules)

    def test_smoke_entry_executes_ten_cases_without_skips(self):
        result = subprocess.run([str(ROOT / 'init.sh'), 'test', 'smoke'], cwd=ROOT,
                                capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn('Ran 10 tests', result.stderr)
        self.assertNotIn('skipped=', result.stderr)
