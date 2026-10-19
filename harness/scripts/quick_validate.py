#!/usr/bin/env python3
"""Portable structural validation for the isolated Skill artifact."""

from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    skill = root / "skill"
    required = (
        "SKILL.md",
        "agents/openai.yaml",
        "assets/templates/测试用例设计表.xlsx",
        "references/specs/test-plan-rules.md",
        "references/specs/tcl-script-rules.md",
        "scripts/test_plan_validator.py",
        "scripts/tcl_convention_validator.py",
    )
    missing = [relative for relative in required if not (skill / relative).is_file()]
    text = (skill / "SKILL.md").read_text(encoding="utf-8") if (skill / "SKILL.md").is_file() else ""
    errors = [f"missing runtime file: {relative}" for relative in missing]
    if not text.startswith("---\n") or "\nname: eda-tester-skill\n" not in text:
        errors.append("SKILL.md must declare name: eda-tester-skill")
    forbidden = ("PROCESS.MD", "function.json", "tests", "references/test-plan.md", "references/e2e-test-set.md")
    errors.extend(f"harness entry leaked into skill/: {relative}" for relative in forbidden if (skill / relative).exists())
    readmes = sorted(
        path.relative_to(skill).as_posix()
        for path in skill.rglob("*")
        if path.is_file() and path.name.casefold() == "readme.md"
    )
    errors.extend(f"README.md is not allowed inside skill/: {relative}" for relative in readmes)
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print("PASS: isolated Skill artifact structure is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
