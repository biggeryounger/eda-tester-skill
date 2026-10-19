#!/usr/bin/env python3
"""Drive the EDA tester Skill through a real Codex JSONL session."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


CASE_DIR = Path(__file__).resolve().parent
ROOT = CASE_DIR.parents[3]
SKILL = ROOT / "skill"


FINAL_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "additionalProperties": False,
    "required": ["state", "summary", "artifacts"],
    "properties": {
        "state": {"enum": ["WAIT-STRATEGY", "WAIT-DESIGN-CONFIRMATION", "DELIVERED", "FAILED"]},
        "summary": {"type": "string"},
        "artifacts": {"type": "array", "items": {"type": "string"}},
    },
}


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def prepare_output(output: Path) -> Path:
    if output.exists():
        if not output.is_dir() or any(output.iterdir()):
            raise ValueError("output must be a new or empty directory")
    else:
        output.mkdir(parents=True)
    workspace = output / "workspace"
    installed_skill = workspace / ".codex" / "skills" / "eda-tester-skill"
    installed_skill.parent.mkdir(parents=True)
    shutil.copytree(SKILL, installed_skill)
    shutil.copytree(CASE_DIR / "input", workspace / "input")
    (workspace / "delivery").mkdir()
    return workspace


def parse_events(text: str) -> tuple[list[dict[str, Any]], str | None]:
    events: list[dict[str, Any]] = []
    session_id: str | None = None
    for number, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Codex emitted invalid JSONL at line {number}: {exc}") from exc
        if not isinstance(event, dict) or not isinstance(event.get("type"), str):
            raise ValueError(f"Codex event {number} has no type")
        events.append(event)
        if event["type"] == "thread.started":
            value = event.get("thread_id", event.get("threadId"))
            if isinstance(value, str) and value:
                session_id = value
    if not events or events[-1].get("type") not in {"turn.completed", "turn.failed"}:
        raise ValueError("Codex JSONL did not end with a turn completion event")
    return events, session_id


def run_codex(
    codex_bin: str,
    workspace: Path,
    output: Path,
    schema: Path,
    turn: int,
    prompt: str,
    timeout: float,
    session_id: str | None = None,
    model: str | None = None,
) -> tuple[dict[str, Any], str | None]:
    final_path = output / f"turn-{turn}-final.json"
    if session_id is None:
        argv = [
            codex_bin,
            "exec",
            "--json",
            "--sandbox",
            "workspace-write",
            "--cd",
            str(workspace),
            "--skip-git-repo-check",
            "--output-schema",
            str(schema),
            "-o",
            str(final_path),
        ]
        if model:
            argv.extend(["--model", model])
        argv.append(prompt)
    else:
        argv = [
            codex_bin,
            "exec",
            "resume",
            "--json",
            "--skip-git-repo-check",
            "--output-schema",
            str(schema),
            "-o",
            str(final_path),
        ]
        if model:
            argv.extend(["--model", model])
        argv.extend([session_id, prompt])
    environment = os.environ.copy()
    environment["EDA_E2E_WORKSPACE"] = str(workspace)
    completed = subprocess.run(argv, cwd=workspace, env=environment, capture_output=True, text=True, timeout=timeout)
    (output / f"turn-{turn}.events.jsonl").write_text(completed.stdout, encoding="utf-8")
    if completed.returncode != 0:
        message = completed.stderr.strip() or f"codex exited with {completed.returncode}"
        raise RuntimeError(f"Codex turn {turn} failed: {message}")
    _, discovered_session = parse_events(completed.stdout)
    if not final_path.is_file():
        raise ValueError(f"Codex turn {turn} did not write its final structured response")
    try:
        final = json.loads(final_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Codex turn {turn} final response is not JSON: {exc}") from exc
    return final, discovered_session


def delivery_tcl_files(workspace: Path) -> list[Path]:
    return sorted((workspace / "delivery").rglob("*.tcl"))


def validate_delivery(workspace: Path) -> tuple[bool, bool, list[str]]:
    delivery = workspace / "delivery"
    plan = delivery / "测试用例设计表.xlsx"
    diagnostics: list[str] = []
    plan_completed = subprocess.run(
        [sys.executable, str(SKILL / "scripts" / "test_plan_validator.py"), str(plan)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    plan_ok = plan_completed.returncode == 0
    if not plan_ok:
        diagnostics.append("test plan validation failed")
    case_root = delivery / "cases"
    case_dirs = sorted(path for path in case_root.iterdir() if path.is_dir()) if case_root.is_dir() else []
    tcl_ok = bool(case_dirs)
    for case_dir in case_dirs:
        completed = subprocess.run(
            [sys.executable, str(SKILL / "scripts" / "tcl_convention_validator.py"), str(case_dir)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            tcl_ok = False
            diagnostics.append(f"TCL validation failed: {case_dir.name}")
    return plan_ok, tcl_ok, diagnostics


def execute(codex_bin: str, output: Path, timeout: float, model: str | None) -> dict[str, object]:
    resolved = shutil.which(codex_bin) if Path(codex_bin).name == codex_bin else codex_bin
    if not resolved or not Path(resolved).is_file():
        raise ValueError(f"Codex executable not found: {codex_bin}")
    workspace = prepare_output(output)
    schema = output / "turn-schema.json"
    write_json(schema, FINAL_SCHEMA)
    initial_text = (workspace / "input" / "user-prompt.txt").read_text(encoding="utf-8").strip()
    common = (
        "这是自动化 Skill E2E。必须显式使用 $eda-tester-skill，并读取 input/command-spec.txt。"
        "所有生成物只能写入 delivery/。不得调用真实 EDA 工具，不得访问许可证或外部设计数据库。"
        "每轮结束时严格按输出 schema 返回当前 state、摘要和相对 artifact 路径。"
    )
    first_prompt = f"{common}\n\n{initial_text}\n当前只执行到策略等待门禁；不得生成 Excel 或 TCL。"
    first, session_id = run_codex(resolved, workspace, output, schema, 1, first_prompt, timeout, model=model)
    if not session_id:
        raise ValueError("Codex did not emit a thread.started session ID")
    first_boundary = first.get("state") == "WAIT-STRATEGY" and not list((workspace / "delivery").rglob("*.xlsx")) and not delivery_tcl_files(workspace)

    second_prompt = (
        f"{common}\n三种策略都选择：Smoke case、正向覆盖、负向覆盖。继续生成并验证测试计划，"
        "展示完整用例设计和两类覆盖率，然后停在 WAIT-DESIGN-CONFIRMATION；确认前不得生成任何 TCL。"
    )
    second, _ = run_codex(resolved, workspace, output, schema, 2, second_prompt, timeout, session_id, model)
    second_boundary = (
        second.get("state") == "WAIT-DESIGN-CONFIRMATION"
        and (workspace / "delivery" / "测试用例设计表.xlsx").is_file()
        and not delivery_tcl_files(workspace)
    )

    third_prompt = (
        f"{common}\n确认当前用例设计可用于生成 TCL。design 选择 riscv，tech 选择 SMIC28。"
        "继续完成资源映射、TCL 生成、静态检查和交付，最终 state 必须是 DELIVERED。"
    )
    third, _ = run_codex(resolved, workspace, output, schema, 3, third_prompt, timeout, session_id, model)
    plan_ok, tcl_ok, diagnostics = validate_delivery(workspace)
    checks = [
        {"id": "codex_session", "status": "PASS" if session_id else "FAIL"},
        {"id": "wait_strategy", "status": "PASS" if first_boundary else "FAIL"},
        {"id": "wait_design_confirmation", "status": "PASS" if second_boundary else "FAIL"},
        {"id": "delivered_state", "status": "PASS" if third.get("state") == "DELIVERED" else "FAIL"},
        {"id": "test_plan", "status": "PASS" if plan_ok else "FAIL"},
        {"id": "tcl_cases", "status": "PASS" if tcl_ok else "FAIL"},
    ]
    result = {
        "case_id": "optimus_check_design_data_full_workflow",
        "status": "PASS" if all(item["status"] == "PASS" for item in checks) else "FAIL",
        "turns": [
            {"number": 1, "state": first.get("state")},
            {"number": 2, "state": second.get("state")},
            {"number": 3, "state": third.get("state")},
        ],
        "checks": checks,
        "diagnostics": diagnostics,
    }
    write_json(output / "agent-e2e-result.json", result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex-bin", default="codex")
    parser.add_argument("--output", type=Path, default=CASE_DIR / "agent_actual_output")
    parser.add_argument("--timeout", type=float, default=900.0)
    parser.add_argument("--model")
    args = parser.parse_args()
    try:
        result = execute(args.codex_bin, args.output.resolve(), args.timeout, args.model)
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired, json.JSONDecodeError) as exc:
        message = str(exc)
        unavailable_markers = (
            "Codex executable not found",
            "failed to load models cache",
            "failed to refresh available models",
            "unknown variant",
            "not logged in",
            "authentication",
        )
        status = "TOOL_UNAVAILABLE" if any(marker.lower() in message.lower() for marker in unavailable_markers) else "FAIL"
        failure = {
            "case_id": "optimus_check_design_data_full_workflow",
            "status": status,
            "turns": [],
            "checks": [{"id": "codex_session", "status": status}],
            "diagnostics": [message[:1000]],
        }
        output = args.output.resolve()
        if output.is_dir():
            write_json(output / "agent-e2e-result.json", failure)
        print(f"AGENT E2E {status}: {message[:1000]}", file=sys.stderr)
        return 2 if status == "TOOL_UNAVAILABLE" else 1
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
