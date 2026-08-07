#!/usr/bin/env python3
"""Unified validation entry point for the EDA tester skill."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


CASE_NAME = re.compile(r"^(pos|neg)([0-9]{3})_([a-z0-9][a-z0-9_]*)$")
FEATURE_ID = re.compile(r"^F-[0-9]{3}$")
VALID_PRIORITIES = {"P0", "P1", "P2", "P3"}
VALID_STATUSES = {"not_started", "active", "blocked", "passing"}
ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class ValidationError:
    path: Path
    message: str

    def __str__(self) -> str:
        return f"{self.path}: {self.message}"


def load_json(path: Path) -> tuple[dict[str, Any] | None, list[ValidationError]]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, [ValidationError(path, f"cannot parse JSON: {exc}")]
    if not isinstance(value, dict):
        return None, [ValidationError(path, "JSON root must be an object")]
    return value, []


def validate_manifest(path: Path) -> tuple[set[str], list[ValidationError]]:
    data, errors = load_json(path)
    if data is None:
        return set(), errors
    if data.get("project") != "eda-tester-skill":
        errors.append(ValidationError(path, "project must be 'eda-tester-skill'"))
    if data.get("status_values") != ["not_started", "active", "blocked", "passing"]:
        errors.append(ValidationError(path, "status_values must be not_started, active, blocked, passing in that order"))
    command_entries = data.get("validation_commands")
    command_ids: set[str] = set()
    if not isinstance(command_entries, list) or not command_entries:
        errors.append(ValidationError(path, "validation_commands must be a non-empty array"))
    else:
        for index, entry in enumerate(command_entries):
            label = f"validation_commands[{index}]"
            if not isinstance(entry, dict):
                errors.append(ValidationError(path, f"{label} must be an object"))
                continue
            command_id = entry.get("id")
            argv = entry.get("argv")
            if not isinstance(command_id, str) or not re.fullmatch(r"[a-z][a-z0-9-]*", command_id):
                errors.append(ValidationError(path, f"{label}.id is invalid"))
            elif command_id in command_ids:
                errors.append(ValidationError(path, f"duplicate validation command id: {command_id}"))
            else:
                command_ids.add(command_id)
            if not isinstance(argv, list) or not argv or not all(isinstance(arg, str) and arg for arg in argv):
                errors.append(ValidationError(path, f"{label}.argv must contain non-empty strings"))
    features = data.get("features")
    if not isinstance(features, list) or not features:
        errors.append(ValidationError(path, "features must be a non-empty array"))
        return set(), errors

    ids: set[str] = set()
    active_ids: list[str] = []
    required = {
        "id",
        "name",
        "priority",
        "status",
        "description",
        "acceptance_criteria",
        "test_cases",
        "validation_commands",
    }
    for index, feature in enumerate(features):
        label = f"features[{index}]"
        if not isinstance(feature, dict):
            errors.append(ValidationError(path, f"{label} must be an object"))
            continue
        missing = required - feature.keys()
        if missing:
            errors.append(ValidationError(path, f"{label} missing: {', '.join(sorted(missing))}"))
        feature_id = feature.get("id")
        if not isinstance(feature_id, str) or not FEATURE_ID.fullmatch(feature_id):
            errors.append(ValidationError(path, f"{label}.id must match F-NNN"))
        elif feature_id in ids:
            errors.append(ValidationError(path, f"duplicate feature id: {feature_id}"))
        else:
            ids.add(feature_id)
        if feature.get("priority") not in VALID_PRIORITIES:
            errors.append(ValidationError(path, f"{label}.priority is invalid"))
        if feature.get("status") not in VALID_STATUSES:
            errors.append(ValidationError(path, f"{label}.status is invalid"))
        elif feature.get("status") == "active" and isinstance(feature_id, str):
            active_ids.append(feature_id)
        criteria = feature.get("acceptance_criteria")
        if not isinstance(criteria, list) or not criteria or not all(isinstance(x, str) and x.strip() for x in criteria):
            errors.append(ValidationError(path, f"{label}.acceptance_criteria must contain non-empty strings"))
        test_cases = feature.get("test_cases")
        if not isinstance(test_cases, list) or not all(isinstance(item, str) and item for item in test_cases):
            errors.append(ValidationError(path, f"{label}.test_cases must be an array of paths"))
        else:
            for test_case in test_cases:
                test_path = path.parent / test_case
                if Path(test_case).is_absolute() or not test_path.exists():
                    errors.append(ValidationError(path, f"{label}.test_cases path does not exist: {test_case}"))
        validation_commands = feature.get("validation_commands")
        if not isinstance(validation_commands, list) or not all(
            isinstance(item, str) and item for item in validation_commands
        ):
            errors.append(ValidationError(path, f"{label}.validation_commands must be an array of command IDs"))
        else:
            unknown_commands = sorted(set(validation_commands) - command_ids)
            if unknown_commands:
                errors.append(
                    ValidationError(path, f"{label} references unknown validation commands: {', '.join(unknown_commands)}")
                )
        if feature.get("status") in {"active", "passing"}:
            if not test_cases:
                errors.append(ValidationError(path, f"{label} must define test_cases before becoming active"))
            if not validation_commands:
                errors.append(ValidationError(path, f"{label} must define validation_commands before becoming active"))
    if len(active_ids) > 1:
        errors.append(ValidationError(path, f"only one feature may be active: {', '.join(active_ids)}"))
    return ids, errors


def delimiters_balanced(text: str) -> bool:
    pairs = {"}": "{", "]": "["}
    stack: list[str] = []
    in_quote = False
    escaped = False
    for char in text:
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char == '"':
            in_quote = not in_quote
        elif not in_quote and char in "{[":
            stack.append(char)
        elif not in_quote and char in "}]":
            if not stack or stack.pop() != pairs[char]:
                return False
    return not in_quote and not stack


def validate_case(case_dir: Path, feature_ids: set[str]) -> list[ValidationError]:
    errors: list[ValidationError] = []
    metadata_path = case_dir / "case.toml"
    try:
        metadata: dict[str, Any] = {}
        for line_number, raw_line in enumerate(metadata_path.read_text(encoding="utf-8").splitlines(), 1):
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                raise ValueError(f"line {line_number} has no '='")
            key, raw_value = (part.strip() for part in line.split("=", 1))
            if not re.fullmatch(r"[a-z_][a-z0-9_]*", key):
                raise ValueError(f"line {line_number} has an invalid key")
            metadata[key] = json.loads(raw_value)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [ValidationError(metadata_path, f"cannot parse TOML: {exc}")]

    match = CASE_NAME.fullmatch(case_dir.name)
    if not match:
        errors.append(ValidationError(case_dir, "directory must match posNNN_<scenario> or negNNN_<scenario>"))
        return errors
    polarity = "positive" if match.group(1) == "pos" else "negative"
    expected = "accept" if polarity == "positive" else "reject"
    required = {"id", "feature_ids", "command", "polarity", "runtime", "script", "expected", "description"}
    missing = required - metadata.keys()
    if missing:
        errors.append(ValidationError(metadata_path, f"missing: {', '.join(sorted(missing))}"))
    if metadata.get("id") != case_dir.name:
        errors.append(ValidationError(metadata_path, "id must equal directory name"))
    if metadata.get("polarity") != polarity:
        errors.append(ValidationError(metadata_path, f"polarity must be '{polarity}'"))
    if metadata.get("expected") != expected:
        errors.append(ValidationError(metadata_path, f"expected must be '{expected}'"))
    if metadata.get("runtime") not in {"static", "eda"}:
        errors.append(ValidationError(metadata_path, "runtime must be 'static' or 'eda'"))
    refs = metadata.get("feature_ids")
    if not isinstance(refs, list) or not refs:
        errors.append(ValidationError(metadata_path, "feature_ids must be a non-empty array"))
    else:
        unknown = sorted(set(refs) - feature_ids)
        if unknown:
            errors.append(ValidationError(metadata_path, f"unknown feature IDs: {', '.join(unknown)}"))

    script_value = metadata.get("script")
    if not isinstance(script_value, str) or Path(script_value).name != script_value or not script_value.endswith(".tcl"):
        errors.append(ValidationError(metadata_path, "script must be a local .tcl filename"))
        return errors
    script_path = case_dir / script_value
    try:
        script = script_path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(ValidationError(script_path, f"cannot read script: {exc}"))
        return errors
    expected_marker = "# EXPECT: PASS" if polarity == "positive" else "# EXPECT: FAIL"
    if script.count("# TEST_ACTION") != 1:
        errors.append(ValidationError(script_path, "must contain exactly one # TEST_ACTION marker"))
    if expected_marker not in script:
        errors.append(ValidationError(script_path, f"missing {expected_marker}"))
    if re.search(r"\b(TODO|TBD)\b", script, re.IGNORECASE):
        errors.append(ValidationError(script_path, "contains an unresolved placeholder"))
    if not delimiters_balanced(script):
        errors.append(ValidationError(script_path, "has unbalanced braces, brackets, or quotes"))
    return errors


def validate_project(root: Path, cases_dir: Path | None = None) -> list[ValidationError]:
    feature_ids, errors = validate_manifest(root / "function.json")
    selected_cases = cases_dir or root / "tests" / "cases"
    if selected_cases.exists():
        for metadata_path in sorted(selected_cases.rglob("case.toml")):
            errors.extend(validate_case(metadata_path.parent, feature_ids))
    return errors


def load_nagelfar_adapter() -> Any:
    module_path = Path(__file__).with_name("nagelfar_adapter.py")
    spec = importlib.util.spec_from_file_location("eda_nagelfar_adapter", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load Nagelfar adapter: {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def project_report(root: Path, cases_dir: Path | None = None) -> dict[str, object]:
    errors = validate_project(root, cases_dir)
    diagnostics = [
        {
            "layer": "PROJECT",
            "rule_id": "PROJECT-VALIDATION",
            "severity": "error",
            "file": str(error.path),
            "line": None,
            "message": error.message,
        }
        for error in errors
    ]
    status = "FAIL" if diagnostics else "PASS"
    return {
        "status": status,
        "checks": [
            {
                "id": "PROJECT",
                "status": status,
                "diagnostics": diagnostics,
            }
        ],
        "diagnostics": diagnostics,
    }


def tcl_report(
    scripts: list[Path],
    syntax_db: Path | None = None,
    executable: str | None = None,
    timeout: float = 30.0,
) -> dict[str, object]:
    adapter = load_nagelfar_adapter()
    checks: list[dict[str, object]] = []
    diagnostics: list[dict[str, object]] = []
    for script in scripts:
        database = syntax_db or adapter.DEFAULT_SYNTAX_DB
        result = adapter.run_nagelfar(script, database, executable, timeout)
        check = result.to_dict()
        check["id"] = "L2A"
        check["input"] = str(script.resolve())
        checks.append(check)
        diagnostics.extend(check["diagnostics"])
    statuses = {str(check["status"]) for check in checks}
    if statuses == {"PASS"}:
        status = "PASS"
    elif "FAIL" in statuses:
        status = "FAIL"
    else:
        status = "TOOL_UNAVAILABLE"
    return {"status": status, "checks": checks, "diagnostics": diagnostics}


def feature_report(root: Path, feature_id: str, timeout: float = 300.0) -> dict[str, object]:
    manifest_path = root / "function.json"
    data, load_errors = load_json(manifest_path)
    if data is None:
        diagnostics = [
            {
                "layer": "FEATURE",
                "rule_id": "FEATURE-MANIFEST",
                "severity": "error",
                "file": str(error.path),
                "line": None,
                "message": error.message,
            }
            for error in load_errors
        ]
        return {"status": "FAIL", "checks": [], "diagnostics": diagnostics}
    commands = {
        entry["id"]: entry["argv"]
        for entry in data.get("validation_commands", [])
        if isinstance(entry, dict) and isinstance(entry.get("id"), str) and isinstance(entry.get("argv"), list)
    }
    feature = next(
        (item for item in data.get("features", []) if isinstance(item, dict) and item.get("id") == feature_id),
        None,
    )
    if feature is None:
        diagnostic = {
            "layer": "FEATURE",
            "rule_id": "FEATURE-NOT-FOUND",
            "severity": "error",
            "file": str(manifest_path),
            "line": None,
            "message": f"unknown feature ID: {feature_id}",
        }
        return {"status": "FAIL", "checks": [], "diagnostics": [diagnostic]}
    command_ids = feature.get("validation_commands", [])
    if not command_ids:
        diagnostic = {
            "layer": "FEATURE",
            "rule_id": "FEATURE-NO-COMMAND",
            "severity": "error",
            "file": str(manifest_path),
            "line": None,
            "message": f"{feature_id} has no validation commands",
        }
        return {"status": "FAIL", "checks": [], "diagnostics": [diagnostic]}
    checks: list[dict[str, object]] = []
    diagnostics: list[dict[str, object]] = []
    for command_id in command_ids:
        argv = commands.get(command_id)
        if argv is None:
            check = {"id": command_id, "status": "FAIL", "returncode": None, "stdout": "", "stderr": "unknown command"}
        else:
            try:
                completed = subprocess.run(
                    argv,
                    cwd=root,
                    check=False,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                )
                check = {
                    "id": command_id,
                    "status": "PASS" if completed.returncode == 0 else "FAIL",
                    "returncode": completed.returncode,
                    "stdout": completed.stdout,
                    "stderr": completed.stderr,
                }
            except (OSError, subprocess.TimeoutExpired) as exc:
                check = {"id": command_id, "status": "FAIL", "returncode": None, "stdout": "", "stderr": str(exc)}
        checks.append(check)
        if check["status"] != "PASS":
            diagnostics.append(
                {
                    "layer": "FEATURE",
                    "rule_id": "FEATURE-COMMAND",
                    "severity": "error",
                    "file": str(manifest_path),
                    "line": None,
                    "message": f"{feature_id} command {command_id} failed: {check['stderr']}",
                }
            )
    return {"status": "FAIL" if diagnostics else "PASS", "checks": checks, "diagnostics": diagnostics}


def print_text(report: dict[str, object]) -> None:
    diagnostics = report["diagnostics"]
    if isinstance(diagnostics, list):
        for item in diagnostics:
            if not isinstance(item, dict):
                continue
            location = str(item.get("file") or "")
            if item.get("line") is not None:
                location = f"{location}:{item['line']}"
            prefix = f"{location}: " if location else ""
            print(
                f"{str(item.get('severity', 'error')).upper()} "
                f"[{item.get('rule_id', 'VALIDATION')}] {prefix}{item.get('message', '')}",
                file=sys.stderr,
            )
    summary = {
        "PASS": "passed",
        "FAIL": "failed",
        "TOOL_UNAVAILABLE": "tool unavailable",
    }.get(str(report["status"]), str(report["status"]).lower())
    print(f"Validation {summary}.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    project_parser = subparsers.add_parser("project", help="validate manifest and case structure")
    project_parser.add_argument("--root", type=Path, default=ROOT)
    project_parser.add_argument("--cases", type=Path, help="override the generated cases directory")
    project_parser.add_argument("--format", choices=("text", "json"), default="text")

    tcl_parser = subparsers.add_parser("tcl", help="run Layer 2A Nagelfar validation")
    tcl_parser.add_argument("scripts", nargs="+", type=Path)
    tcl_parser.add_argument("--syntax-db", type=Path)
    tcl_parser.add_argument("--nagelfar", help="path to Nagelfar executable or nagelfar.tcl")
    tcl_parser.add_argument("--timeout", type=float, default=30.0)
    tcl_parser.add_argument("--format", choices=("text", "json"), default="json")

    feature_parser = subparsers.add_parser("feature", help="run commands assigned to one feature")
    feature_parser.add_argument("feature_id")
    feature_parser.add_argument("--root", type=Path, default=ROOT)
    feature_parser.add_argument("--timeout", type=float, default=300.0)
    feature_parser.add_argument("--format", choices=("text", "json"), default="json")
    return parser


def main(argv: list[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    if not arguments or arguments[0].startswith("-") and arguments[0] not in {"-h", "--help"}:
        arguments.insert(0, "project")
    args = build_parser().parse_args(arguments)
    if args.command == "project":
        cases = args.cases.resolve() if args.cases else None
        report = project_report(args.root.resolve(), cases)
    elif args.command == "tcl":
        report = tcl_report(args.scripts, args.syntax_db, args.nagelfar, args.timeout)
    else:
        report = feature_report(args.root.resolve(), args.feature_id, args.timeout)
    if args.format == "json":
        json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        print_text(report)
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
