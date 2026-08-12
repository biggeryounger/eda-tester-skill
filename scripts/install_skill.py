#!/usr/bin/env python3
"""Install eda-tester-skill and optionally its pinned Nagelfar dependency."""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
from pathlib import Path
from typing import Mapping


SKILL_NAME = "eda-tester-skill"
SUPPORTED_AGENTS = ("codex", "opencode", "hermes", "workbuddy", "trae")
AGENT_LABELS = {
    "codex": "Codex",
    "opencode": "OpenCode",
    "hermes": "Hermes",
    "workbuddy": "WorkBuddy",
    "trae": "Trae",
}
NAGELFAR_VERSION = "1.3.5"
NAGELFAR_URL = "https://sourceforge.net/projects/nagelfar/files/Rel_135/nagelfar135.tar.gz/download"
NAGELFAR_SHA256 = "3baf920fb34b73e32067118365d074d859298e2bce3748ad9458624bece85b23"

DEV_ONLY_NAMES = frozenset({
    "PROCESS.MD",
    "AGENTS.md",
    "function.json",
    "tests",
    "generated",
    "outputs",
    ".gitignore",
})
JUNK_NAMES = frozenset({".git", ".DS_Store", "__pycache__"})
TOP_LEVEL_EXCLUDED = DEV_ONLY_NAMES | JUNK_NAMES


def fail(message: str) -> int:
    print(f"ERROR: {message}", file=sys.stderr)
    return 1


def validate_source(source: Path) -> list[str]:
    required = ("SKILL.md", "function.json", "agents/openai.yaml")
    missing = [name for name in required if not (source / name).is_file()]
    if missing:
        return [f"missing required file: {name}" for name in missing]
    text = (source / "SKILL.md").read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\nname: eda-tester-skill\n" not in text:
        return ["SKILL.md does not declare name: eda-tester-skill"]
    return []


def ignored(_directory: str, names: list[str]) -> set[str]:
    return {
        name
        for name in names
        if name in JUNK_NAMES or name.endswith((".pyc", ".pyo"))
    }


def runtime_entries(source: Path) -> list[Path]:
    return sorted(
        (entry for entry in source.iterdir() if entry.name not in TOP_LEVEL_EXCLUDED),
        key=lambda path: path.name,
    )


def install_skill(source: Path, target: Path, mode: str, dry_run: bool) -> None:
    if target.exists() or target.is_symlink():
        raise FileExistsError(f"target already exists: {target}")
    entries = runtime_entries(source)
    if dry_run:
        kept = ", ".join(entry.name for entry in entries) or "(none)"
        present_dev = sorted(DEV_ONLY_NAMES & {p.name for p in source.iterdir()})
        print(f"DRY RUN: install {source} -> {target} ({mode})")
        print(f"  keep: {kept}")
        if present_dev:
            print(f"  exclude (dev-only): {', '.join(present_dev)}")
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    target.mkdir(parents=True, exist_ok=True)
    if mode == "link":
        for entry in entries:
            (target / entry.name).symlink_to(entry, target_is_directory=entry.is_dir())
    else:
        for entry in entries:
            destination = target / entry.name
            if entry.is_dir():
                shutil.copytree(entry, destination, ignore=ignored)
            else:
                shutil.copy2(entry, destination)
    print(f"Installed {SKILL_NAME} to {target} ({mode}).")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def safe_extract(archive: Path, destination: Path) -> None:
    destination_resolved = destination.resolve()
    with tarfile.open(archive, "r:gz") as bundle:
        for member in bundle.getmembers():
            member_path = (destination / member.name).resolve()
            if destination_resolved not in member_path.parents and member_path != destination_resolved:
                raise ValueError(f"archive contains unsafe path: {member.name}")
            if member.issym() or member.islnk():
                raise ValueError(f"archive contains unsupported link: {member.name}")
        bundle.extractall(destination)


def version_of(command: Path) -> str | None:
    try:
        completed = subprocess.run(
            [str(command), "-help"],
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    output = completed.stdout + completed.stderr
    return NAGELFAR_VERSION if f"Version {NAGELFAR_VERSION}" in output else None


def install_nagelfar(
    prefix: Path,
    bin_dir: Path,
    archive: Path | None,
    expected_sha256: str,
    dry_run: bool,
) -> None:
    install_dir = prefix / "nagelfar135"
    executable = install_dir / "nagelfar.tcl"
    command = bin_dir / "nagelfar"
    if version_of(executable) == NAGELFAR_VERSION:
        print(f"Nagelfar {NAGELFAR_VERSION} already installed at {install_dir}.")
    elif dry_run:
        print(f"DRY RUN: install Nagelfar {NAGELFAR_VERSION} to {install_dir}")
        return
    else:
        if install_dir.exists() or install_dir.is_symlink():
            raise FileExistsError(f"Nagelfar target already exists but is not version {NAGELFAR_VERSION}: {install_dir}")
        with tempfile.TemporaryDirectory(prefix="eda-nagelfar-") as temporary_dir:
            temporary = Path(temporary_dir)
            package = archive.resolve() if archive else temporary / "nagelfar135.tar.gz"
            if archive is None:
                print(f"Downloading Nagelfar {NAGELFAR_VERSION} from the official SourceForge release.")
                urllib.request.urlretrieve(NAGELFAR_URL, package)
            actual = sha256(package)
            if actual != expected_sha256:
                raise ValueError(f"Nagelfar archive SHA-256 mismatch: expected {expected_sha256}, got {actual}")
            extracted = temporary / "extract"
            extracted.mkdir()
            safe_extract(package, extracted)
            source = extracted / "nagelfar135"
            if not (source / "nagelfar.tcl").is_file():
                raise ValueError("Nagelfar archive is missing nagelfar135/nagelfar.tcl")
            prefix.mkdir(parents=True, exist_ok=True)
            shutil.copytree(source, install_dir)
        if version_of(executable) != NAGELFAR_VERSION:
            raise RuntimeError(f"installed Nagelfar did not report Version {NAGELFAR_VERSION}")
        print(f"Installed Nagelfar {NAGELFAR_VERSION} to {install_dir}.")
    if not dry_run:
        bin_dir.mkdir(parents=True, exist_ok=True)
        if command.exists() or command.is_symlink():
            if command.resolve() != executable.resolve():
                raise FileExistsError(f"Nagelfar command already exists: {command}")
        else:
            command.symlink_to(executable)
        if version_of(command) != NAGELFAR_VERSION:
            raise RuntimeError(f"Nagelfar command did not report Version {NAGELFAR_VERSION}: {command}")
        print(f"Nagelfar command available at {command}.")


def default_skills_dir(
    agent: str,
    *,
    home: Path | None = None,
    environ: Mapping[str, str] | None = None,
) -> Path:
    """Return the user-level Skills directory for a supported agent."""
    user_home = home or Path.home()
    environment = os.environ if environ is None else environ
    configured_homes = {
        "codex": ("CODEX_HOME", user_home / ".codex"),
        "opencode": ("OPENCODE_CONFIG_DIR", user_home / ".config" / "opencode"),
        "hermes": ("HERMES_HOME", user_home / ".hermes"),
        "workbuddy": ("WORKBUDDY_HOME", user_home / ".workbuddy"),
        "trae": ("TRAE_HOME", user_home / ".trae"),
    }
    if agent not in configured_homes:
        raise ValueError(f"unsupported agent: {agent}")
    variable, fallback = configured_homes[agent]
    configured = environment.get(variable)
    root = Path(configured).expanduser() if configured else fallback
    return root / "skills"


def rescan_message(agent: str) -> str:
    if agent == "codex":
        return "Restart Codex or create a new task so the Skill is rescanned."
    return f"Restart {AGENT_LABELS[agent]} so the Skill is rescanned."


def build_parser() -> argparse.ArgumentParser:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=root, help="Skill source directory")
    parser.add_argument("--agent", choices=SUPPORTED_AGENTS, default="codex", help="target agent (default: codex)")
    parser.add_argument("--skills-dir", type=Path, help="override the target agent's Skills directory")
    parser.add_argument(
        "--mode",
        choices=("link", "copy"),
        help="installation mode (default: link for Codex, copy for other agents)",
    )
    parser.add_argument("--install-nagelfar", action="store_true", help="install pinned Nagelfar 1.3.5")
    parser.add_argument("--skip-nagelfar", action="store_true", help="explicitly skip Nagelfar installation")
    parser.add_argument("--nagelfar-prefix", type=Path, default=Path.home() / ".local" / "share" / "nagelfar")
    parser.add_argument("--bin-dir", type=Path, default=Path.home() / ".local" / "bin")
    parser.add_argument("--nagelfar-archive", type=Path, help="use an offline nagelfar135.tar.gz")
    parser.add_argument("--nagelfar-sha256", default=NAGELFAR_SHA256, help=argparse.SUPPRESS)
    parser.add_argument("--dry-run", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.install_nagelfar and args.skip_nagelfar:
        return fail("--install-nagelfar and --skip-nagelfar are mutually exclusive")
    source = args.source.expanduser().resolve()
    errors = validate_source(source)
    if errors:
        return fail("; ".join(errors))
    skills_dir = args.skills_dir or default_skills_dir(args.agent)
    target = skills_dir.expanduser().resolve() / SKILL_NAME
    mode = args.mode or ("link" if args.agent == "codex" else "copy")
    try:
        if target.exists() or target.is_symlink():
            raise FileExistsError(f"target already exists: {target}")
        if args.install_nagelfar:
            install_nagelfar(
                args.nagelfar_prefix.expanduser().resolve(),
                args.bin_dir.expanduser().resolve(),
                args.nagelfar_archive,
                args.nagelfar_sha256,
                args.dry_run,
            )
        install_skill(source, target, mode, args.dry_run)
    except (OSError, ValueError, RuntimeError) as exc:
        return fail(str(exc))
    if not args.install_nagelfar:
        print("Nagelfar installation skipped; use --install-nagelfar to install pinned version 1.3.5.")
    print(f"Target agent: {AGENT_LABELS[args.agent]}.")
    print(rescan_message(args.agent))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
