from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "harness" / "scripts" / "run_jenkins_gate.py"
SPEC = importlib.util.spec_from_file_location("eda_jenkins_gate", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load Jenkins gate")
GATE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = GATE
SPEC.loader.exec_module(GATE)


class JenkinsGateTests(unittest.TestCase):
    def test_complete_suite_contains_all_required_project_checks(self) -> None:
        commands = [item.argv for item in GATE.CHECKS]
        self.assertIn(("python3", "skill/scripts/validate.py", "project"), commands)
        self.assertIn(("python3", "-m", "unittest", "discover", "-s", "harness/tests/unit", "-v"), commands)
        self.assertNotIn(("python3", "harness/scripts/verify_nagelfar_install.py"), commands)
        self.assertTrue(any("quick_validate.py" in " ".join(command) for command in commands))

    def test_failure_stops_approval_gate_and_reports_junit(self) -> None:
        results = [
            GATE.CheckResult("Project", ("x",), 0, 0.1, "pass"),
            GATE.CheckResult("Unit", ("y",), 1, 0.2, "failed"),
        ]
        with tempfile.TemporaryDirectory() as directory:
            with mock.patch.object(GATE, "REPORT_DIR", Path(directory)):
                GATE.write_reports(results)
            junit = (Path(directory) / "junit.xml").read_text(encoding="utf-8")
            page = (Path(directory) / "index.html").read_text(encoding="utf-8")
        self.assertIn('failures="1"', junit)
        self.assertIn("Unit", page)
        self.assertIn("FAIL", page)


if __name__ == "__main__":
    unittest.main()
