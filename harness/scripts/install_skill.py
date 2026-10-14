#!/usr/bin/env python3
"""Install eda-tester-skill into a supported Agent Skills directory."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
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
RUNTIME_TOP_LEVEL = frozenset({"SKILL.md", "agents", "assets", "references", "scripts"})
PROJECT_ONLY_RELATIVE = frozenset({
    "references/test-plan.md",
    "references/e2e-test-set.md",
    "references/case-knowledge-base-design.md",
    "references/screen-qr-transfer.md",
    "scripts/install_skill.py",
})


def fail(message: str) -> int:
    print(f"ERROR: {message}", file=sys.stderr)
    return 1


def validate_source(source: Path) -> list[str]:
    required = ("SKILL.md", "agents/openai.yaml")
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


def runtime_entries(source: Path) -> list[tuple[Path, Path]]:
    entries: list[tuple[Path, Path]] = []
    for top_name in sorted(RUNTIME_TOP_LEVEL):
        top = source / top_name
        if not top.exists():
            continue
        if top.is_file():
            entries.append((top, Path(top_name)))
            continue
        entries.append((top, Path(top_name)))
        for item in sorted(top.rglob("*")):
            relative = item.relative_to(source)
            if any(part in JUNK_NAMES for part in relative.parts):
                continue
            if item.name.endswith((".pyc", ".pyo")):
                continue
            if relative.as_posix() in PROJECT_ONLY_RELATIVE:
                continue
            entries.append((item, relative))
    return entries


def install_skill(source: Path, target: Path, mode: str, dry_run: bool) -> None:
    if target.exists() or target.is_symlink():
        raise FileExistsError(f"target already exists: {target}")
    entries = runtime_entries(source)
    if dry_run:
        kept = ", ".join(sorted(RUNTIME_TOP_LEVEL)) or "(none)"
        present_dev = sorted(DEV_ONLY_NAMES & {p.name for p in source.iterdir()})
        print(f"DRY RUN: install {source} -> {target} ({mode})")
        print(f"  keep: {kept}")
        if present_dev:
            print(f"  exclude (dev-only): {', '.join(present_dev)}")
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    target.mkdir(parents=True, exist_ok=True)
    for entry, relative in entries:
        destination = target / relative
        if entry.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
        elif mode == "link":
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.symlink_to(entry)
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(entry, destination)
    print(f"Installed {SKILL_NAME} to {target} ({mode}).")


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
    root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=root / "skill", help="Skill runtime source directory")
    parser.add_argument("--agent", choices=SUPPORTED_AGENTS, default="codex", help="target agent (default: codex)")
    parser.add_argument("--skills-dir", type=Path, help="override the target agent's Skills directory")
    parser.add_argument(
        "--mode",
        choices=("link", "copy"),
        help="installation mode (default: link for Codex, copy for other agents)",
    )
    parser.add_argument("--dry-run", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
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
        install_skill(source, target, mode, args.dry_run)
    except (OSError, ValueError, RuntimeError) as exc:
        return fail(str(exc))
    print(f"Target agent: {AGENT_LABELS[args.agent]}.")
    print(rescan_message(args.agent))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
