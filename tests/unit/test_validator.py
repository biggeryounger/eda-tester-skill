from __future__ import annotations

import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("eda_validator", ROOT / "scripts" / "validate.py")
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load validator")
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)


class ValidatorTests(unittest.TestCase):
    def test_repository_fixtures_pass(self) -> None:
        self.assertEqual([], VALIDATOR.validate_project(ROOT))

    def test_unbalanced_tcl_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            case_dir = Path(temporary_dir) / "neg001_bad_syntax"
            case_dir.mkdir()
            (case_dir / "case.toml").write_text(
                '\n'.join([
                    'id = "neg001_bad_syntax"',
                    'feature_ids = ["F-006"]',
                    'command = "bad"',
                    'polarity = "negative"',
                    'runtime = "static"',
                    'script = "run.tcl"',
                    'expected = "reject"',
                    'description = "fixture"',
                ]),
                encoding="utf-8",
            )
            (case_dir / "run.tcl").write_text(
                "# EXPECT: FAIL\n# TEST_ACTION\nset value {broken\n",
                encoding="utf-8",
            )
            errors = VALIDATOR.validate_case(case_dir, {"F-006"})
            self.assertTrue(any("unbalanced" in error.message for error in errors))

    def test_multiple_active_features_are_rejected(self) -> None:
        feature = {
            "name": "fixture",
            "priority": "P0",
            "status": "active",
            "description": "fixture",
            "acceptance_criteria": ["verified"],
        }
        manifest = {
            "project": "eda-tester-skill",
            "status_values": ["not_started", "active", "blocked", "passing"],
            "features": [
                {"id": "F-001", **feature},
                {"id": "F-002", **feature},
            ],
        }
        with tempfile.TemporaryDirectory() as temporary_dir:
            path = Path(temporary_dir) / "function.json"
            path.write_text(json.dumps(manifest), encoding="utf-8")
            _, errors = VALIDATOR.validate_manifest(path)
            self.assertTrue(any("only one feature may be active" in error.message for error in errors))

    def test_project_report_uses_unified_shape(self) -> None:
        report = VALIDATOR.project_report(ROOT)
        self.assertEqual("PASS", report["status"])
        self.assertEqual("PROJECT", report["checks"][0]["id"])
        self.assertEqual([], report["diagnostics"])

    def test_active_feature_requires_tests_and_commands(self) -> None:
        manifest = {
            "project": "eda-tester-skill",
            "status_values": ["not_started", "active", "blocked", "passing"],
            "validation_commands": [
                {"id": "unit", "argv": ["python3", "-m", "unittest"]},
            ],
            "features": [
                {
                    "id": "F-001",
                    "name": "fixture",
                    "priority": "P0",
                    "status": "active",
                    "description": "fixture",
                    "acceptance_criteria": ["verified"],
                    "test_cases": [],
                    "validation_commands": [],
                }
            ],
        }
        with tempfile.TemporaryDirectory() as temporary_dir:
            path = Path(temporary_dir) / "function.json"
            path.write_text(json.dumps(manifest), encoding="utf-8")
            _, errors = VALIDATOR.validate_manifest(path)
            messages = [error.message for error in errors]
            self.assertTrue(any("test_cases before becoming active" in message for message in messages))
            self.assertTrue(any("validation_commands before becoming active" in message for message in messages))

    def test_legacy_no_argument_entry_point_still_passes(self) -> None:
        stdout = io.StringIO()
        original = sys.stdout
        try:
            sys.stdout = stdout
            exit_code = VALIDATOR.main([])
        finally:
            sys.stdout = original
        self.assertEqual(0, exit_code)
        self.assertIn("Validation pass", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
