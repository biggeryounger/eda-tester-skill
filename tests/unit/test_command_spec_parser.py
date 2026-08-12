from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "parse_command_spec.py"
SPEC = importlib.util.spec_from_file_location("command_spec_parser", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load command spec parser")
PARSER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = PARSER
SPEC.loader.exec_module(PARSER)


COMPLETE_SPEC = """\
Tool: Optimus
Version: 21.1
Command: check_design_data
Syntax: check_design_data -file <String> [-netlist] [-mode <full|quick>] [-tag <String>]...
Options:
-file <String> (required) Report output path. Exactly one value.
-netlist (optional) Check netlist-related items. Flag; takes no value.
-mode <Enum> (optional) Values: full, quick. At most once.
-tag <String> (optional, repeatable) Filter tag. One value per occurrence.
Constraints:
- -netlist requires -file
- -mode and -netlist are mutually exclusive
- at least one of -file, -mode
Version Differences:
- 22.1: added -mode; removed -legacy
"""


class CommandSpecParserTests(unittest.TestCase):
    def test_skill_registers_txt_parser_workflow(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        reference = (ROOT / "references" / "command-spec-format.md").read_text(encoding="utf-8")
        self.assertIn("scripts/parse_command_spec.py", skill)
        self.assertIn("SPEC-GAP", skill)
        self.assertIn("schema_version", reference)

    def test_extracts_complete_command_semantics(self) -> None:
        result = PARSER.parse_text(COMPLETE_SPEC, "commands.txt")
        self.assertEqual([], result["diagnostics"])
        command = result["commands"][0]
        self.assertEqual("Optimus", command["tool"])
        self.assertEqual("21.1", command["versions"][0]["version"])
        self.assertEqual("check_design_data", command["name"])
        options = {item["name"]: item for item in command["options"]}
        self.assertTrue(options["-file"]["required"])
        self.assertEqual({"count": {"min": 1, "max": 1}, "type": "string"}, options["-file"]["argument"])
        self.assertEqual({"count": {"min": 0, "max": 0}, "type": "boolean"}, options["-netlist"]["argument"])
        self.assertEqual(["full", "quick"], options["-mode"]["argument"]["enum"])
        self.assertTrue(options["-tag"]["repeatable"])
        relationships = command["relationships"]
        self.assertIn({"kind": "requires", "options": ["-netlist", "-file"], "source_line": 11}, relationships)
        self.assertIn({"kind": "mutually_exclusive", "options": ["-mode", "-netlist"], "source_line": 12}, relationships)
        self.assertIn({"kind": "at_least_one", "options": ["-file", "-mode"], "source_line": 13}, relationships)
        self.assertEqual(
            {"version": "22.1", "added_options": ["-mode"], "removed_options": ["-legacy"], "notes": "added -mode; removed -legacy", "source_line": 15},
            command["version_differences"][0],
        )

    def test_parses_multiple_chinese_command_blocks(self) -> None:
        text = """工具: Optimus\n版本: 21.1\n命令: place\n语法: place [-incremental]\n选项:\n-incremental（可选）布尔开关，不带参数\n\n命令: route\n语法: route [-effort <String>]\n选项:\n-effort <String>（必选）一个字符串参数\n"""
        result = PARSER.parse_text(text, "命令列表.txt")
        self.assertEqual([], result["diagnostics"])
        self.assertEqual(["place", "route"], [item["name"] for item in result["commands"]])
        route = result["commands"][1]
        self.assertEqual("Optimus", route["tool"])
        self.assertEqual("21.1", route["versions"][0]["version"])
        self.assertTrue(route["options"][0]["required"])

    def test_unknown_attributes_are_explicit_gaps(self) -> None:
        result = PARSER.parse_text("Command: place\nOptions:\n-effort Controls effort\n", "partial.txt")
        option = result["commands"][0]["options"][0]
        self.assertIsNone(option["required"])
        self.assertIsNone(option["repeatable"])
        self.assertEqual("unknown", option["argument"]["type"])
        self.assertTrue(any(item["code"] == "SPEC-GAP" for item in result["diagnostics"]))

    def test_square_brackets_are_optional_and_braces_are_required_group(self) -> None:
        text = """Command: report_qor
Syntax: report_qor {-pre_place | -place | -route} [-hold] -prefix <String>
Options:
-pre_place stage flag
-place stage flag
-route stage flag
-hold optional flag
-prefix <String> report prefix
"""
        result = PARSER.parse_text(text, "report_qor.txt")
        options = {item["name"]: item for item in result["commands"][0]["options"]}
        self.assertTrue(options["-pre_place"]["required"])
        self.assertFalse(options["-hold"]["required"])
        self.assertTrue(options["-prefix"]["required"])
        self.assertIn(
            {"kind": "exactly_one", "options": ["-pre_place", "-place", "-route"], "source_line": 2},
            result["commands"][0]["relationships"],
        )

    def test_rejects_relationship_to_undeclared_option(self) -> None:
        result = PARSER.parse_text(
            "Command: place\nOptions:\n-incremental (optional) flag\nConstraints:\n- -missing requires -incremental\n",
            "bad.txt",
        )
        self.assertTrue(any(item["code"] == "SPEC-RELATION-UNKNOWN" and item["severity"] == "error" for item in result["diagnostics"]))

    def test_cli_does_not_write_output_when_errors_exist(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            root = Path(temporary_dir)
            source = root / "bad.txt"
            output = root / "out.json"
            source.write_text("Tool: Optimus\nOptions:\n-file <String> required\n", encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(SCRIPT), str(source), str(output)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(0, completed.returncode)
            self.assertFalse(output.exists())
            report = json.loads(completed.stdout)
            self.assertTrue(any(item["code"] == "SPEC-COMMAND-MISSING" for item in report["diagnostics"]))


if __name__ == "__main__":
    unittest.main()
