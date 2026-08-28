from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "dump_tool_help.tcl"


class ToolHelpDumperTests(unittest.TestCase):
    @unittest.skipUnless(shutil.which("tclsh"), "tclsh is required")
    def test_prints_matching_command_help_and_continues_after_failure(self) -> None:
        harness = f"""
proc eda_test_alpha {{arg}} {{puts "alpha usage $arg"}}
proc eda_test_broken {{arg}} {{error "help unavailable"}}
source {{{SCRIPT}}}
eda_dump_all_help eda_test_*
"""
        completed = subprocess.run(
            [shutil.which("tclsh") or "tclsh"],
            input=harness,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, completed.returncode)
        self.assertIn("===== BEGIN HELP: eda_test_alpha =====", completed.stdout)
        self.assertIn("alpha usage -help", completed.stdout)
        self.assertIn("===== HELP FAILED: eda_test_broken =====", completed.stdout)
        self.assertIn("SUMMARY total=2 succeeded=1 failed=1", completed.stdout)

    @unittest.skipUnless(shutil.which("tclsh"), "tclsh is required")
    def test_explicit_command_list_avoids_unrelated_commands(self) -> None:
        harness = f"""
proc eda_test_one {{arg}} {{return "one $arg"}}
proc eda_test_two {{arg}} {{return "two $arg"}}
source {{{SCRIPT}}}
eda_dump_command_help {{eda_test_two}}
"""
        completed = subprocess.run(
            [shutil.which("tclsh") or "tclsh"], input=harness, check=False, capture_output=True, text=True
        )
        self.assertEqual(0, completed.returncode)
        self.assertNotIn("eda_test_one", completed.stdout)
        self.assertIn("two -help", completed.stdout)

    def test_parser_contract_documents_help_capture_input(self) -> None:
        reference = (ROOT / "references" / "command-spec-format.md").read_text(encoding="utf-8")
        self.assertIn("dump_tool_help.tcl", reference)
        self.assertIn("eda_dump_all_help", reference)


if __name__ == "__main__":
    unittest.main()
