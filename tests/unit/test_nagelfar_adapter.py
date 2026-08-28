from __future__ import annotations

import importlib.util
import stat
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("nagelfar_adapter", ROOT / "scripts" / "nagelfar_adapter.py")
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load Nagelfar adapter")
ADAPTER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = ADAPTER
SPEC.loader.exec_module(ADAPTER)


class NagelfarAdapterTests(unittest.TestCase):
    def make_checker(self, root: Path, version: str = "1.3.5") -> Path:
        checker = root / "nagelfar"
        checker.write_text(
            "#!/bin/sh\n"
            f"if [ \"$1\" = \"-help\" ]; then echo 'Version {version} 2025-02-11'; exit 0; fi\n"
            "case \"$*\" in\n"
            "  *bad.tcl*) echo \"bad.tcl: Line 3: E Unknown option '-bad' to 'add_net'\"; exit 2 ;;\n"
            "  *) exit 0 ;;\n"
            "esac\n",
            encoding="utf-8",
        )
        checker.chmod(checker.stat().st_mode | stat.S_IXUSR)
        return checker

    def test_tool_unavailable_when_checker_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            script = Path(temporary_dir) / "run.tcl"
            script.write_text("set value 1\n", encoding="utf-8")
            result = ADAPTER.run_nagelfar(script, executable=str(Path(temporary_dir) / "missing"))
            self.assertEqual("TOOL_UNAVAILABLE", result.status)
            self.assertEqual("NAGELFAR-NOT-FOUND", result.diagnostics[0].rule_id)

    def test_wrong_version_is_unavailable(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            root = Path(temporary_dir)
            checker = self.make_checker(root, "1.3.4")
            script = root / "run.tcl"
            script.write_text("set value 1\n", encoding="utf-8")
            result = ADAPTER.run_nagelfar(script, executable=str(checker))
            self.assertEqual("TOOL_UNAVAILABLE", result.status)
            self.assertEqual("NAGELFAR-VERSION", result.diagnostics[0].rule_id)

    def test_valid_script_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            root = Path(temporary_dir)
            checker = self.make_checker(root)
            script = root / "good.tcl"
            script.write_text("add_net -name n1\n", encoding="utf-8")
            result = ADAPTER.run_nagelfar(script, executable=str(checker))
            self.assertEqual("PASS", result.status)
            self.assertEqual("1.3.5", result.engine_version)

    def test_nagelfar_error_is_reported_as_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            root = Path(temporary_dir)
            checker = self.make_checker(root)
            script = root / "bad.tcl"
            script.write_text("add_net -bad value\n", encoding="utf-8")
            result = ADAPTER.run_nagelfar(script, executable=str(checker))
            self.assertEqual("FAIL", result.status)
            self.assertEqual("NAGELFAR-SYNTAX", result.diagnostics[0].rule_id)
            self.assertEqual(3, result.diagnostics[0].line)

    def test_resolve_tclsh_rejects_85_and_selects_compatible_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            old = Path(temporary_dir) / "tclsh85"
            old.write_text("#!/bin/sh\necho 8.5.9\n", encoding="utf-8")
            old.chmod(old.stat().st_mode | stat.S_IXUSR)
            with mock.patch.dict("os.environ", {"TCLSH": str(old)}):
                resolved = ADAPTER.resolve_tclsh()
            self.assertIsNotNone(resolved)
            completed = __import__("subprocess").run([resolved], input="puts [info patchlevel]\n", capture_output=True, text=True)
            major_minor = tuple(map(int, completed.stdout.strip().split(".")[:2]))
            self.assertGreaterEqual(major_minor, (8, 6))


if __name__ == "__main__":
    unittest.main()
