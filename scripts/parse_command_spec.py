#!/usr/bin/env python3
"""Parse EDA command-list text into deterministic, versioned JSON semantics."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "1.0"
FIELD = re.compile(r"^\s*(Tool|工具|Version|版本|Command|命令|Syntax|语法)\s*[:：]\s*(.*?)\s*$", re.I)
SECTION = re.compile(r"^\s*(Options?|Parameters?|选项|参数|Constraints?|Relationships?|约束|关系|Version Differences?|版本差异)\s*[:：]?\s*$", re.I)
OPTION = re.compile(r"^\s*(-[A-Za-z][A-Za-z0-9_.-]*)(?:\s+(<[^>]+>|\{[^}]+\}|\[[^]]+\]))?\s*(.*)$")
VERSION_ITEM = re.compile(r"^\s*[-*]?\s*([0-9]+(?:\.[0-9A-Za-z_-]+)+)\s*[:：]\s*(.*?)\s*$")
OPTION_NAME = re.compile(r"-[A-Za-z][A-Za-z0-9_.-]*")


def _diagnostic(code: str, severity: str, message: str, source: str, line: int | None) -> dict[str, Any]:
    return {"code": code, "severity": severity, "message": message, "source": source, "line": line}


def _type(value: str | None, description: str) -> tuple[str, list[str] | None]:
    token = (value or "").strip("<>{}[] ")
    combined = f"{token} {description}".lower()
    enum: list[str] | None = None
    if "|" in token:
        enum = [item.strip() for item in token.split("|") if item.strip()]
    else:
        match = re.search(r"(?:values?|choices?|枚举(?:值)?|取值)\s*[:：]\s*([^.;。]+)", description, re.I)
        if match:
            enum = [item.strip() for item in re.split(r"[,，|/]", match.group(1)) if item.strip()]
    if enum:
        return "enum", enum
    if re.fullmatch(r"(?i)bool(?:ean)?", token):
        return "boolean", None
    if re.fullmatch(r"(?i)int(?:eger)?", token):
        return "integer", None
    if re.fullmatch(r"(?i)float|double|number|real", token):
        return "number", None
    if re.fullmatch(r"(?i)path|file|directory|dir", token):
        return "path", None
    if re.fullmatch(r"(?i)string|str|name", token):
        return "string", None
    if re.search(r"\b(bool(?:ean)?|flag)\b|布尔|开关", combined):
        return "boolean", None
    if re.search(r"\b(int(?:eger)?)\b|整数", combined):
        return "integer", None
    if re.search(r"\b(float|double|number|real)\b|浮点|数值", combined):
        return "number", None
    if re.search(r"\b(path|file|directory|dir)\b|路径|文件|目录", combined):
        return "path", None
    if re.search(r"\b(string|str|name)\b|字符串|名称", combined):
        return "string", None
    if value:
        return "string", None
    return "unknown", None


def _required(description: str, syntax: str, name: str) -> bool | None:
    if re.search(r"\b(required|mandatory)\b|必选|必须", description, re.I):
        return True
    if re.search(r"\boptional\b|可选", description, re.I):
        return False
    if syntax:
        match = re.search(rf"(?<![A-Za-z0-9_.-]){re.escape(name)}\b", syntax)
        if match:
            prefix = syntax[:match.start()]
            inside_square = prefix.rfind("[") > prefix.rfind("]")
            inside_brace = prefix.rfind("{") > prefix.rfind("}")
            if inside_square:
                return False
            if inside_brace or not inside_square:
                return True
    return None


def _repeatable(description: str, syntax: str, name: str) -> bool | None:
    if re.search(r"\b(repeatable|multiple times|one or more)\b|可重复|多次出现", description, re.I) or re.search(rf"{re.escape(name)}[^\n]*\.\.\.", syntax):
        return True
    if re.search(r"\b(at most once|exactly once|not repeatable)\b|不可重复|最多一次|仅一次", description, re.I):
        return False
    if syntax and len(re.findall(rf"(?<![A-Za-z0-9_.-]){re.escape(name)}\b", syntax)) == 1:
        return False
    return None


def _argument(value: str | None, description: str) -> dict[str, Any]:
    argument_type, enum = _type(value, description)
    no_value = re.search(r"\b(no value|takes no (?:value|argument)|flag)\b|不带参数|无需参数|布尔开关", description, re.I)
    if no_value or (argument_type == "boolean" and value is None):
        count = {"min": 0, "max": 0}
        argument_type = "boolean"
    elif value or re.search(r"\b(one|single|exactly one)\s+(?:value|argument)\b|一个(?:值|参数)|单个参数", description, re.I):
        count = {"min": 1, "max": 1}
    else:
        count = {"min": None, "max": None}
    result: dict[str, Any] = {"count": count, "type": argument_type}
    if enum:
        result["enum"] = enum
    return result


def _parse_relationship(line: str, line_number: int) -> dict[str, Any] | None:
    options = OPTION_NAME.findall(line)
    lowered = line.lower()
    if len(options) >= 2 and ("requires" in lowered or "depends on" in lowered or "依赖" in line or "需要" in line):
        return {"kind": "requires", "options": options[:2], "source_line": line_number}
    if len(options) >= 2 and ("mutually exclusive" in lowered or "conflicts with" in lowered or "互斥" in line or "不能同时" in line):
        return {"kind": "mutually_exclusive", "options": options, "source_line": line_number}
    if len(options) >= 2 and ("at least one" in lowered or "one of" in lowered or "至少一个" in line or "至少选择" in line):
        return {"kind": "at_least_one", "options": options, "source_line": line_number}
    return None


def _version_difference(line: str, line_number: int) -> dict[str, Any] | None:
    match = VERSION_ITEM.match(line)
    if not match:
        return None
    note = match.group(2).strip()
    added_match = re.search(r"(?:added?|新增|增加)\s*([^;；]+)", note, re.I)
    removed_match = re.search(r"(?:removed?|删除|移除)\s*([^;；]+)", note, re.I)
    added = OPTION_NAME.findall(added_match.group(1)) if added_match else []
    removed = OPTION_NAME.findall(removed_match.group(1)) if removed_match else []
    return {"version": match.group(1), "added_options": added, "removed_options": removed, "notes": note, "source_line": line_number}


def parse_text(text: str, source: str = "<memory>") -> dict[str, Any]:
    commands: list[dict[str, Any]] = []
    diagnostics: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    inherited_tool: str | None = None
    inherited_version: str | None = None
    section: str | None = None

    for line_number, raw_line in enumerate(text.splitlines(), 1):
        line = raw_line.strip()
        if not line:
            continue
        field = FIELD.match(line)
        if field:
            key, value = field.group(1).lower(), field.group(2).strip()
            if key in {"tool", "工具"}:
                inherited_tool = value
                if current is not None:
                    current["tool"] = value
            elif key in {"version", "版本"}:
                inherited_version = value
                if current is not None:
                    current["versions"] = [{"version": value, "source_line": line_number}]
            elif key in {"command", "命令"}:
                current = {
                    "name": value,
                    "tool": inherited_tool,
                    "versions": ([{"version": inherited_version, "source_line": line_number}] if inherited_version else []),
                    "syntax": None,
                    "options": [],
                    "relationships": [],
                    "version_differences": [],
                    "source": {"file": source, "line": line_number},
                }
                commands.append(current)
                section = None
            elif key in {"syntax", "语法"}:
                if current is None:
                    diagnostics.append(_diagnostic("SPEC-COMMAND-MISSING", "error", "Syntax appears before a command declaration", source, line_number))
                else:
                    current["syntax"] = value
                    for group in re.findall(r"\{([^{}]+)\}", value):
                        grouped_options = OPTION_NAME.findall(group)
                        if "|" in group and len(grouped_options) >= 2:
                            current["relationships"].append({"kind": "exactly_one", "options": grouped_options, "source_line": line_number})
            continue
        section_match = SECTION.match(line)
        if section_match:
            label = section_match.group(1).lower()
            if label.startswith(("option", "parameter")) or label in {"选项", "参数"}:
                section = "options"
            elif label.startswith(("constraint", "relationship")) or label in {"约束", "关系"}:
                section = "relationships"
            else:
                section = "versions"
            continue
        if current is None:
            continue
        if section == "options":
            option_match = OPTION.match(line)
            if option_match:
                name, value, description = option_match.groups()
                option = {
                    "name": name,
                    "required": _required(description, current["syntax"] or "", name),
                    "argument": _argument(value, description),
                    "repeatable": _repeatable(description, current["syntax"] or "", name),
                    "description": description.strip(" -–—:："),
                    "source_line": line_number,
                }
                current["options"].append(option)
            continue
        if section == "relationships":
            relationship = _parse_relationship(line, line_number)
            if relationship:
                current["relationships"].append(relationship)
            else:
                diagnostics.append(_diagnostic("SPEC-RELATION-UNPARSED", "warning", "Constraint could not be classified", source, line_number))
            continue
        if section == "versions":
            difference = _version_difference(line, line_number)
            if difference:
                current["version_differences"].append(difference)
            else:
                diagnostics.append(_diagnostic("SPEC-VERSION-UNPARSED", "warning", "Version difference could not be classified", source, line_number))

    if not commands:
        diagnostics.append(_diagnostic("SPEC-COMMAND-MISSING", "error", "No Command/命令 declaration was found", source, None))
    for command in commands:
        names = {item["name"] for item in command["options"]}
        for option in command["options"]:
            unknown = []
            if option["required"] is None:
                unknown.append("required")
            if option["repeatable"] is None:
                unknown.append("repeatable")
            if option["argument"]["type"] == "unknown" or option["argument"]["count"]["min"] is None:
                unknown.append("argument")
            if unknown:
                diagnostics.append(_diagnostic("SPEC-GAP", "warning", f"{command['name']} {option['name']} has unknown fields: {', '.join(unknown)}", source, option["source_line"]))
        for relationship in command["relationships"]:
            missing = [name for name in relationship["options"] if name not in names]
            if missing:
                diagnostics.append(_diagnostic("SPEC-RELATION-UNKNOWN", "error", f"{command['name']} relationship references undeclared option(s): {', '.join(missing)}", source, relationship["source_line"]))
    return {"schema_version": SCHEMA_VERSION, "source": source, "commands": commands, "diagnostics": diagnostics}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="UTF-8 TXT command list")
    parser.add_argument("output", type=Path, help="output JSON path")
    args = parser.parse_args(argv)
    try:
        text = args.input.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as exc:
        report = {"schema_version": SCHEMA_VERSION, "source": str(args.input), "commands": [], "diagnostics": [_diagnostic("SPEC-INPUT", "error", str(exc), str(args.input), None)]}
        json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 1
    report = parse_text(text, str(args.input))
    json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    if any(item["severity"] == "error" for item in report["diagnostics"]):
        return 1
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
