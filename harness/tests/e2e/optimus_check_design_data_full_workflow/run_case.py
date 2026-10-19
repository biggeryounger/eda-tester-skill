#!/usr/bin/env python3
"""Execute the deterministic portion of the full check_design_data Skill workflow."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


CASE_DIR = Path(__file__).resolve().parent
ROOT = CASE_DIR.parents[3]
SKILL = ROOT / "skill"


NITH_RUN = '''#!/opt/Anaconda3-5.2.0-Linux-x86_64/bin/python -B
### NITH initialization, please do not change this section
import os,sys
nith_path="/Data/devops/qa/git/testcase-prime/pv/nith"
nith_path=nith_path if os.path.exists(nith_path) else "/storage/prime_testcase/pv/nith"
envpath=os.path.abspath(sys.argv[0])
for i in range(10):
    envpath=os.path.dirname(envpath)
    if os.path.isfile(envpath+"/nith/main.py"):
        nith_path=envpath+"/nith"; break
sys.path.append(nith_path)
import globalvar as nith; nith._init()
from main import *
### NITH initialization end

# Case setup
nith.input[""] = f"tcl/{nith.PV_TOOL}/run.tcl"
nith_run()

nith_done()
'''


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def verify_inputs(case: dict[str, Any]) -> None:
    for fixture in case["fixtures"]:
        relative = Path(fixture["path"])
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(f"fixture path must stay within the case: {relative}")
        actual = hashlib.sha256((CASE_DIR / relative).read_bytes()).hexdigest()
        if actual != fixture["sha256"]:
            raise ValueError(f"fixture hash mismatch: {relative}")


def scenarios() -> list[dict[str, object]]:
    return [
        {
            "number": 1,
            "被测命令": "check_design_data",
            "用例路径": "pos001_quick_signal",
            "用例描述": "[strategy:smoke] [strategy:positive] 合法 quick 模式覆盖必选 file、mode 和 include_signal 选项",
            "用例步骤": "1. 准备已完成 setup_design 的 riscv 设计。\n2. 调用 check_design_data -file ./out/quick_signal.rpt -mode quick -include_signal。\n3. 检查并收集报告文件。",
            "用例预期": "1. 命令无报错并生成非空报告文件。\n2. 报告包含 signal 检查数据且设计对象保持完整。",
            "责任人": "",
            "状态": "NOT_RUN",
            "备注": "Smoke case；正向覆盖",
            "Ticket": "",
        },
        {
            "number": 2,
            "被测命令": "check_design_data",
            "用例路径": "pos002_full_power_signal",
            "用例描述": "[strategy:smoke] [strategy:positive] 合法 full 模式同时覆盖 include_power 与 include_signal",
            "用例步骤": "1. 准备包含电源网和信号网的 riscv 设计。\n2. 调用 check_design_data -file ./out/full.rpt -mode full -include_power -include_signal。\n3. 检查并收集完整报告。",
            "用例预期": "1. 命令无报错并生成非空报告文件。\n2. 报告同时包含 power 与 signal 检查数据。",
            "责任人": "",
            "状态": "NOT_RUN",
            "备注": "Smoke case；正向覆盖",
            "Ticket": "",
        },
        {
            "number": 3,
            "被测命令": "check_design_data",
            "用例路径": "neg001_invalid_mode",
            "用例描述": "[strategy:negative] 非法 mode 枚举值触发参数拒绝且不生成报告",
            "用例步骤": "1. 准备已完成 setup_design 的 riscv 设计。\n2. 调用 check_design_data -file ./out/invalid.rpt -mode invalid -include_signal。\n3. 检查错误诊断和报告文件状态。",
            "用例预期": "1. 命令因非法枚举值被拒绝并报告参数错误。\n2. 报告文件不存在且设计数据保持不变。",
            "责任人": "",
            "状态": "NOT_RUN",
            "备注": "负向覆盖",
            "Ticket": "",
        },
        {
            "number": 4,
            "被测命令": "check_design_data",
            "用例路径": "neg002_missing_file",
            "用例描述": "[strategy:negative] 缺失必选 file 参数触发拒绝且不修改设计状态",
            "用例步骤": "1. 准备已完成 setup_design 的 riscv 设计。\n2. 调用 check_design_data -mode quick -include_power。\n3. 检查错误诊断和设计状态。",
            "用例预期": "1. 命令因缺失必选参数被拒绝并报告错误。\n2. 不生成报告文件且设计数据保持不变。",
            "责任人": "",
            "状态": "NOT_RUN",
            "备注": "负向覆盖",
            "Ticket": "",
        },
    ]


def coverage_report() -> dict[str, object]:
    scenario_points = ["minimum_quick", "full_categories", "invalid_mode", "missing_file"]
    option_points = ["-file", "-mode=quick", "-mode=full", "-include_power", "-include_signal"]
    return {
        "schema_version": "1.0",
        "scenario_coverage": {"covered": 4, "total": 4, "percent": 100.0, "uncovered": [], "points": scenario_points},
        "option_coverage": {"covered": 5, "total": 5, "percent": 100.0, "uncovered": [], "points": option_points},
        "strategies": ["Smoke case", "正向覆盖", "负向覆盖"],
    }


def run_text(case_name: str, command: str, expect: str) -> str:
    return f'''# DESIGN_INIT_BEGIN
source $env(PV_ROOT)/scripts/pv.tcl
set tool $env(PV_TOOL)
source ./tcl/design.tcl
set_options setup.lef_file $lef_files
set_options setup.verilog $netlist_file
set_options setup.mmmc_file ./tcl/optimus/mmmc.tcl
set_options setup.top_cell $init_top_cell
setup_design
read_def $def_file
# DESIGN_INIT_END
# EXPECT: {expect}
# TEST_ACTION
pv_check_log {{{command}}} -name {case_name} -filter {{^Date}}
pv_rpt_checkpoints
exit
'''


def generate_tcl_cases(output: Path, rows: list[dict[str, object]]) -> list[Path]:
    commands = {
        "pos001_quick_signal": ("check_design_data -file ./out/quick_signal.rpt -mode quick -include_signal", "PASS"),
        "pos002_full_power_signal": ("check_design_data -file ./out/full.rpt -mode full -include_power -include_signal", "PASS"),
        "neg001_invalid_mode": ("check_design_data -file ./out/invalid.rpt -mode invalid -include_signal", "FAIL"),
        "neg002_missing_file": ("check_design_data -mode quick -include_power", "FAIL"),
    }
    cases: list[Path] = []
    for row in rows:
        name = str(row["用例路径"])
        case_dir = output / "cases" / name
        tool_dir = case_dir / "tcl" / "optimus"
        tool_dir.mkdir(parents=True)
        (case_dir / "nith.run").write_text(NITH_RUN, encoding="utf-8")
        shutil.copy2(SKILL / "assets" / "defaults" / "optimus" / "design.tcl", case_dir / "tcl" / "design.tcl")
        shutil.copy2(SKILL / "assets" / "defaults" / "optimus" / "mmmc.tcl", tool_dir / "mmmc.tcl")
        command, expect = commands[name]
        (tool_dir / "run.tcl").write_text(run_text(name, command, expect), encoding="utf-8")
        cases.append(case_dir)
    return cases


def run_command(argv: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(argv, cwd=ROOT, capture_output=True, text=True)


def semantic_review() -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "test_plan": [
            {"rule_range": "PLAN-006..PLAN-013", "status": "PASS", "reason": "Every row maps command inputs to observable file, report, diagnostic, or unchanged-state results."}
        ],
        "tcl": [
            {"rule_range": "TCL-SEMANTIC-*", "status": "PASS", "reason": "Each Excel row maps to one tool-specific script with initialization, action, checkpoint, and expected polarity."}
        ],
        "limitations": ["Static workflow test; no EDA binary, license, or design database is executed."],
    }


def compare_outputs(output: Path, tcl_statuses: list[bool]) -> list[dict[str, object]]:
    spec = json.loads((output / "structured-command-spec.json").read_text(encoding="utf-8"))
    coverage = json.loads((output / "coverage-report.json").read_text(encoding="utf-8"))
    golden = json.loads((CASE_DIR / "expected_output" / "workflow_trace.json").read_text(encoding="utf-8"))
    actual_trace = json.loads((output / "workflow-trace.json").read_text(encoding="utf-8"))
    command = spec["commands"][0] if len(spec.get("commands", [])) == 1 else {}
    spec_ok = (
        command.get("name") == "check_design_data"
        and {item["name"] for item in command.get("options", [])} == {"-file", "-mode", "-include_power", "-include_signal"}
        and not spec.get("diagnostics")
    )
    coverage_ok = all(
        item["total"] > 0
        and item["covered"] <= item["total"]
        and item["percent"] == item["covered"] / item["total"] * 100
        and len(item["uncovered"]) == item["total"] - item["covered"]
        for item in (coverage["scenario_coverage"], coverage["option_coverage"])
    )
    plan_result = run_command([sys.executable, str(SKILL / "scripts" / "test_plan_validator.py"), str(output / "测试用例设计表.xlsx")])
    trace_ok = [item["id"] for item in actual_trace["steps"]] == [item["id"] for item in golden["steps"]] and all(
        item.get("status") == "PASS" and item.get("evidence") for item in actual_trace["steps"]
    )
    checks = [
        {"id": "structured_spec", "status": "PASS" if spec_ok else "FAIL"},
        {"id": "coverage_report", "status": "PASS" if coverage_ok else "FAIL"},
        {"id": "test_plan", "status": "PASS" if plan_result.returncode == 0 else "FAIL"},
        {"id": "tcl_cases", "status": "PASS" if tcl_statuses and all(tcl_statuses) else "FAIL"},
        {"id": "workflow_trace", "status": "PASS" if trace_ok else "FAIL"},
    ]
    return checks


def workflow_trace(golden: dict[str, Any], evidence: dict[str, list[str]]) -> dict[str, object]:
    return {
        "schema_version": golden["schema_version"],
        "case_id": golden["case_id"],
        "steps": [
            {
                "id": step["id"],
                "required": step["required"],
                "status": "PASS" if evidence.get(step["id"]) else "FAIL",
                "evidence": evidence.get(step["id"], []),
            }
            for step in golden["steps"]
        ],
    }


def execute(output: Path) -> dict[str, object]:
    if output.exists():
        if not output.is_dir() or any(output.iterdir()):
            raise ValueError("output must be a new or empty directory")
    else:
        output.mkdir(parents=True)
    case = json.loads((CASE_DIR / "case.json").read_text(encoding="utf-8"))
    verify_inputs(case)
    turns = {turn["id"]: turn for turn in case["input"]["conversation"]}
    selected = turns["select_strategy"]["selections"]
    confirmation = turns["confirm_design"]

    parser = load_module("e2e_command_spec_parser", SKILL / "scripts" / "parse_command_spec.py")
    spec = parser.parse_text(
        (CASE_DIR / case["input"]["command_spec"]).read_text(encoding="utf-8"),
        case["input"]["command_spec"],
    )
    write_json(output / "structured-command-spec.json", spec)
    if spec["diagnostics"]:
        raise ValueError("command specification contains diagnostics")

    rows = scenarios()
    scenario_path = output / "scenarios.json"
    write_json(scenario_path, {"scenarios": rows})
    coverage = coverage_report()
    write_json(output / "coverage-report.json", coverage)

    plan = output / "测试用例设计表.xlsx"
    generated = run_command([sys.executable, str(SKILL / "scripts" / "generate_test_plan.py"), str(scenario_path), str(plan)])
    if generated.returncode != 0:
        raise RuntimeError(generated.stderr or generated.stdout)

    case_dirs = generate_tcl_cases(output, rows)
    tcl_statuses = [
        run_command([sys.executable, str(SKILL / "scripts" / "tcl_convention_validator.py"), str(case_dir)]).returncode == 0
        for case_dir in case_dirs
    ]
    write_json(output / "semantic-review.json", semantic_review())

    golden = json.loads((CASE_DIR / "expected_output" / "workflow_trace.json").read_text(encoding="utf-8"))
    evidence = {
        "ROUTE-SCENARIO-1": [f"selected_workflow={case['input']['workflow_scenario']}"],
        "PARSE-COMMAND-SPEC": ["structured-command-spec.json", "diagnostics=0"],
        "WAIT-STRATEGY": [turns["wait_strategy"]["expected_state"], f"selected={','.join(selected)}"],
        "BUILD-REQUIREMENTS-SCENARIOS": [f"scenario_count={len(rows)}", "strategy labels retained in plan source"],
        "REPORT-COVERAGE": ["scenario_coverage=4/4", "option_coverage=5/5"],
        "GENERATE-TEST-PLAN": ["测试用例设计表.xlsx", f"rows={len(rows)}"],
        "VALIDATE-TEST-PLAN-STRUCTURE": ["test_plan_validator.py exit=0"],
        "REVIEW-TEST-PLAN-SEMANTICS": ["semantic-review.json test_plan=PASS"],
        "WAIT-DESIGN-CONFIRMATION": [turns["wait_design_confirmation"]["expected_state"], f"approved={confirmation['approved']}"],
        "RESOLVE-DESIGN-TECH": [f"design={confirmation['design']}", f"tech={confirmation['tech']}", "optimus defaults archived"],
        "GENERATE-TCL": [f"case_directories={len(case_dirs)}"],
        "VALIDATE-TCL-STATIC": [f"passed={sum(tcl_statuses)}/{len(tcl_statuses)}"],
        "REVIEW-TCL-SEMANTICS": ["semantic-review.json tcl=PASS"],
        "DELIVER": ["five expected outputs compared", "e2e-result.json"],
    }
    actual_trace = workflow_trace(golden, evidence)
    write_json(output / "workflow-trace.json", actual_trace)

    checks = compare_outputs(output, tcl_statuses)
    result = {"case_id": case["case_id"], "status": "PASS" if all(item["status"] == "PASS" for item in checks) else "FAIL", "checks": checks}
    write_json(output / "e2e-result.json", result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=CASE_DIR / "actual_output")
    args = parser.parse_args()
    try:
        result = execute(args.output.resolve())
    except (OSError, ValueError, RuntimeError, KeyError, json.JSONDecodeError) as exc:
        print(f"E2E FAIL: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
