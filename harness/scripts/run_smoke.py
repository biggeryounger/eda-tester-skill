#!/usr/bin/env python3
"""Run the protected, versioned ten-case smoke selection; skips never pass."""
from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'harness'))


def main() -> int:
    data = json.loads((ROOT / 'harness/references/protected-smoke.json').read_text(encoding='utf-8'))
    cases = data['cases']
    if ([c['id'] for c in cases] != [f'SMOKE-{n:03d}' for n in range(1, 11)]
            or len({c['test'] for c in cases}) != 10):
        raise ValueError('Expected exactly ten unique protected smoke cases')
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for case in cases:
        selected = loader.loadTestsFromName(case['test'])
        if loader.errors or selected.countTestCases() != 1:
            raise ValueError(f"Cannot load protected case: {case['id']}")
        suite.addTests(selected)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if (result.wasSuccessful() and result.testsRun == 10
                 and not result.skipped and not result.expectedFailures) else 1


if __name__ == '__main__':
    raise SystemExit(main())
