#!/usr/bin/env python3
"""Run pinned Nagelfar validation and emit a stable Layer 2A result."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence


NAGELFAR_VERSION = "1.3.5"
VERSION_PATTERN = re.compile(r"Version\s+([0-9]+(?:\.[0-9]+)+)")
DIAGNOSTIC_PATTERN = re.compile(
    r"^(?:(?P<file>.*?):\s*)?(?:Line\s+)?(?P<line>[0-9]+):\s+"
    r"(?P<severity>[NWE])\s+(?P<message>.*)$"
)
DEFAULT_SYNTAX_DB = (
    Path(__file__).resolve().parents[1]
    / "references"
    / "nagelfar"
    / "syntaxdb-innovus.tcl"
)


@dataclass(frozen=True)
class Diagnostic:
    layer: str
    rule_id: str
    severity: str
    file: str
    line: int | None
    message: str


@dataclass(frozen=True)
class NagelfarResult:
    layer: str
    status: str
    engine: str
    engine_version: str | None
    syntax_database: str
    diagnostics: list[Diagnostic]

    def to_dict(self) -> dict[str, object]:
        value = asdict(self)
        return value


def unavailable(rule_id: str, message: str, syntax_db: Path) -> NagelfarResult:
    return NagelfarResult(
        layer="L2A",
        status="TOOL_UNAVAILABLE",
        engine="Nagelfar",
        engine_version=None,
        syntax_database=str(syntax_db),
        diagnostics=[
            Diagnostic("L2A", rule_id, "error", "", None, message)
        ],
    )


def resolve_command(explicit: str | None) -> list[str] | None:
    configured = explicit or os.environ.get("NAGELFAR")
    candidate = configured or shutil.which("nagelfar") or shutil.which("nagelfar.tcl")
    if not candidate:
        return None
    path = Path(candidate).expanduser()
    if configured and not path.is_file() and not shutil.which(candidate):
        return None
    resolved = str(path.resolve()) if path.is_file() else candidate
    if resolved.endswith(".tcl"):
        tclsh = shutil.which("tclsh")
        return [tclsh, resolved] if tclsh else None
    return [resolved]


def detect_version(command: Sequence[str], timeout: float) -> tuple[str | None, str]:
    try:
        completed = subprocess.run(
            [*command, "-help"],
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return None, str(exc)
    output = "\n".join(part for part in (completed.stdout, completed.stderr) if part)
    match = VERSION_PATTERN.search(output)
    return (match.group(1), output) if match else (None, output)


def parse_diagnostics(output: str, fallback_file: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for raw_line in output.splitlines():
        match = DIAGNOSTIC_PATTERN.match(raw_line.strip())
        if not match:
            continue
        severity_code = match.group("severity")
        severity = {"E": "error", "W": "warning", "N": "note"}[severity_code]
        diagnostics.append(
            Diagnostic(
                layer="L2A",
                rule_id="NAGELFAR-SYNTAX",
                severity=severity,
                file=match.group("file") or str(fallback_file),
                line=int(match.group("line")),
                message=match.group("message").strip(),
            )
        )
    return diagnostics


def run_nagelfar(
    script: Path,
    syntax_db: Path = DEFAULT_SYNTAX_DB,
    executable: str | None = None,
    timeout: float = 30.0,
) -> NagelfarResult:
    script = script.resolve()
    syntax_db = syntax_db.resolve()
    if not script.is_file():
        return NagelfarResult(
            "L2A",
            "FAIL",
            "Nagelfar",
            None,
            str(syntax_db),
            [Diagnostic("L2A", "L2A-INPUT", "error", str(script), None, "TCL file does not exist")],
        )
    if not syntax_db.is_file():
        return unavailable("NAGELFAR-DB-MISSING", f"syntax database not found: {syntax_db}", syntax_db)

    command = resolve_command(executable)
    if command is None:
        return unavailable(
            "NAGELFAR-NOT-FOUND",
            "Nagelfar is not installed; set NAGELFAR to nagelfar.tcl or its executable",
            syntax_db,
        )
    version, version_output = detect_version(command, timeout)
    if version != NAGELFAR_VERSION:
        actual = version or "unknown"
        return unavailable(
            "NAGELFAR-VERSION",
            f"Nagelfar {NAGELFAR_VERSION} is required; found {actual}: {version_output.strip()}",
            syntax_db,
        )

    invocation = [
        *command,
        "-s",
        "_",
        "-s",
        str(syntax_db),
        "-severity",
        "E",
        "-quiet",
        "-H",
        "-exitcode",
        str(script),
    ]
    try:
        completed = subprocess.run(
            invocation,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return unavailable("NAGELFAR-TIMEOUT", f"Nagelfar timed out after {timeout:g}s", syntax_db)
    except OSError as exc:
        return unavailable("NAGELFAR-EXEC", f"cannot execute Nagelfar: {exc}", syntax_db)

    output = "\n".join(part for part in (completed.stdout, completed.stderr) if part)
    diagnostics = parse_diagnostics(output, script)
    has_error = any(item.severity == "error" for item in diagnostics)
    if completed.returncode == 0 and not has_error:
        status = "PASS"
    elif completed.returncode in {1, 2} or has_error:
        status = "FAIL"
    else:
        return unavailable(
            "NAGELFAR-EXEC",
            f"Nagelfar exited with unexpected code {completed.returncode}: {output.strip()}",
            syntax_db,
        )
    if status == "FAIL" and not diagnostics:
        diagnostics.append(
            Diagnostic("L2A", "NAGELFAR-OUTPUT", "error", str(script), None, output.strip() or "Nagelfar failed")
        )
    return NagelfarResult(
        "L2A",
        status,
        "Nagelfar",
        version,
        str(syntax_db),
        diagnostics,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("script", type=Path)
    parser.add_argument("--syntax-db", type=Path, default=DEFAULT_SYNTAX_DB)
    parser.add_argument("--nagelfar", help="path to Nagelfar executable or nagelfar.tcl")
    parser.add_argument("--timeout", type=float, default=30.0)
    args = parser.parse_args()
    result = run_nagelfar(args.script, args.syntax_db, args.nagelfar, args.timeout)
    json.dump(result.to_dict(), sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0 if result.status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
