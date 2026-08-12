from __future__ import annotations

import subprocess
import sys
import hashlib
import io
import tarfile
import tempfile
import unittest
from pathlib import Path

from scripts.install_skill import default_skills_dir


ROOT = Path(__file__).resolve().parents[2]
INSTALLER = ROOT / "scripts" / "install_skill.py"


class SkillInstallerTests(unittest.TestCase):
    def run_installer(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(INSTALLER), *args],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

    def test_link_install_creates_discoverable_skill(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            skills_dir = Path(temporary_dir) / "skills"
            result = self.run_installer("--skills-dir", str(skills_dir), "--skip-nagelfar")
            target = skills_dir / "eda-tester-skill"
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertTrue(target.is_dir())
            self.assertFalse(target.is_symlink())
            self.assertTrue((target / "SKILL.md").is_symlink())
            self.assertEqual((ROOT / "SKILL.md").resolve(), (target / "SKILL.md").resolve())

    def test_supported_agents_use_expected_default_directories(self) -> None:
        home = Path("/users/tester")
        expected = {
            "codex": home / ".codex" / "skills",
            "opencode": home / ".config" / "opencode" / "skills",
            "hermes": home / ".hermes" / "skills",
            "workbuddy": home / ".workbuddy" / "skills",
            "trae": home / ".trae" / "skills",
        }
        for agent, skills_dir in expected.items():
            with self.subTest(agent=agent):
                self.assertEqual(skills_dir, default_skills_dir(agent, home=home, environ={}))

    def test_each_supported_agent_can_be_selected(self) -> None:
        for agent in ("opencode", "hermes", "workbuddy", "trae"):
            with self.subTest(agent=agent), tempfile.TemporaryDirectory() as temporary_dir:
                skills_dir = Path(temporary_dir) / "skills"
                result = self.run_installer(
                    "--agent", agent,
                    "--skills-dir", str(skills_dir),
                    "--skip-nagelfar",
                )
                target = skills_dir / "eda-tester-skill"
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertTrue(target.is_dir())
                self.assertFalse(target.is_symlink())
                self.assertIn(agent, result.stdout.lower())

    def test_agent_home_environment_variable_overrides_default(self) -> None:
        configured = Path("/opt/agent-config")
        cases = {
            "codex": "CODEX_HOME",
            "opencode": "OPENCODE_CONFIG_DIR",
            "hermes": "HERMES_HOME",
            "workbuddy": "WORKBUDDY_HOME",
            "trae": "TRAE_HOME",
        }
        for agent, variable in cases.items():
            with self.subTest(agent=agent):
                actual = default_skills_dir(agent, environ={variable: str(configured)})
                self.assertEqual(configured / "skills", actual)

    def test_unknown_agent_is_rejected(self) -> None:
        result = self.run_installer("--agent", "unknown", "--dry-run", "--skip-nagelfar")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("invalid choice", result.stderr)

    def test_copy_install_excludes_repository_state(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            skills_dir = Path(temporary_dir) / "skills"
            result = self.run_installer("--mode", "copy", "--skills-dir", str(skills_dir), "--skip-nagelfar")
            target = skills_dir / "eda-tester-skill"
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertTrue(target.is_dir())
            self.assertFalse(target.is_symlink())
            self.assertFalse((target / ".git").exists())
            self.assertFalse(any(target.rglob("__pycache__")))

    def test_copy_install_excludes_dev_only_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            skills_dir = Path(temporary_dir) / "skills"
            result = self.run_installer("--mode", "copy", "--skills-dir", str(skills_dir), "--skip-nagelfar")
            target = skills_dir / "eda-tester-skill"
            self.assertEqual(0, result.returncode, result.stderr)
            for name in ("PROCESS.MD", "AGENTS.md", "function.json", ".gitignore"):
                self.assertFalse((target / name).exists(), f"{name} must be excluded")
            for name in ("tests", "generated", "outputs"):
                self.assertFalse((target / name).exists(), f"{name}/ must be excluded")

    def test_link_install_excludes_dev_only_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            skills_dir = Path(temporary_dir) / "skills"
            result = self.run_installer("--mode", "link", "--skills-dir", str(skills_dir), "--skip-nagelfar")
            target = skills_dir / "eda-tester-skill"
            self.assertEqual(0, result.returncode, result.stderr)
            for name in ("PROCESS.MD", "AGENTS.md", "function.json", ".gitignore"):
                self.assertFalse((target / name).exists(), f"{name} must be excluded")
            self.assertFalse((target / "tests").exists(), "tests/ must be excluded")

    def test_install_keeps_runtime_entries_in_both_modes(self) -> None:
        for mode in ("link", "copy"):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as temporary_dir:
                skills_dir = Path(temporary_dir) / "skills"
                result = self.run_installer("--mode", mode, "--skills-dir", str(skills_dir), "--skip-nagelfar")
                target = skills_dir / "eda-tester-skill"
                self.assertEqual(0, result.returncode, result.stderr)
                for name in ("SKILL.md", "agents", "assets", "references", "scripts"):
                    self.assertTrue((target / name).exists(), f"{name} must be kept ({mode})")

    def test_existing_target_is_not_overwritten(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            skills_dir = Path(temporary_dir) / "skills"
            target = skills_dir / "eda-tester-skill"
            target.mkdir(parents=True)
            marker = target / "keep.txt"
            marker.write_text("keep", encoding="utf-8")
            result = self.run_installer("--skills-dir", str(skills_dir), "--skip-nagelfar")
            self.assertNotEqual(0, result.returncode)
            self.assertEqual("keep", marker.read_text(encoding="utf-8"))
            self.assertIn("already exists", result.stderr)

    def test_invalid_source_is_rejected_before_install(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            root = Path(temporary_dir)
            invalid_source = root / "invalid"
            invalid_source.mkdir()
            result = self.run_installer(
                "--source",
                str(invalid_source),
                "--skills-dir",
                str(root / "skills"),
                "--skip-nagelfar",
            )
            self.assertNotEqual(0, result.returncode)
            self.assertIn("SKILL.md", result.stderr)

    def test_dry_run_does_not_write(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            skills_dir = Path(temporary_dir) / "skills"
            result = self.run_installer("--skills-dir", str(skills_dir), "--skip-nagelfar", "--dry-run")
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertFalse(skills_dir.exists())
            self.assertIn("DRY RUN", result.stdout)

    def make_nagelfar_archive(self, root: Path) -> tuple[Path, str]:
        archive = root / "nagelfar135.tar.gz"
        content = b'#!/bin/sh\necho "Version 1.3.5 2025-02-11"\n'
        info = tarfile.TarInfo("nagelfar135/nagelfar.tcl")
        info.mode = 0o755
        info.size = len(content)
        with tarfile.open(archive, "w:gz") as bundle:
            bundle.addfile(info, io.BytesIO(content))
        digest = hashlib.sha256(archive.read_bytes()).hexdigest()
        return archive, digest

    def test_offline_nagelfar_install_is_version_checked(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            root = Path(temporary_dir)
            archive, digest = self.make_nagelfar_archive(root)
            prefix = root / "share" / "nagelfar"
            bin_dir = root / "bin"
            result = self.run_installer(
                "--skills-dir", str(root / "skills"),
                "--install-nagelfar",
                "--nagelfar-archive", str(archive),
                "--nagelfar-sha256", digest,
                "--nagelfar-prefix", str(prefix),
                "--bin-dir", str(bin_dir),
            )
            self.assertEqual(0, result.returncode, result.stderr)
            command = bin_dir / "nagelfar"
            self.assertTrue(command.is_symlink())
            version = subprocess.run([str(command), "-help"], check=False, capture_output=True, text=True)
            self.assertIn("Version 1.3.5", version.stdout)

    def test_nagelfar_checksum_mismatch_stops_install(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            root = Path(temporary_dir)
            archive, _digest = self.make_nagelfar_archive(root)
            skills_dir = root / "skills"
            result = self.run_installer(
                "--skills-dir", str(skills_dir),
                "--install-nagelfar",
                "--nagelfar-archive", str(archive),
                "--nagelfar-sha256", "0" * 64,
                "--nagelfar-prefix", str(root / "share"),
                "--bin-dir", str(root / "bin"),
            )
            self.assertNotEqual(0, result.returncode)
            self.assertIn("SHA-256 mismatch", result.stderr)
            self.assertFalse((skills_dir / "eda-tester-skill").exists())


if __name__ == "__main__":
    unittest.main()
