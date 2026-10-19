#!/usr/bin/env python3
"""Run the complete repository gate and publish HTML, JUnit, and text logs."""

from __future__ import annotations

from dataclasses import dataclass
import datetime as dt
import html
from pathlib import Path
import re
import subprocess
import sys
import time
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = ROOT / "harness" / "outputs" / "jenkins"


@dataclass(frozen=True)
class Check:
    name: str
    argv: tuple[str, ...]


@dataclass(frozen=True)
class CheckResult:
    name: str
    argv: tuple[str, ...]
    returncode: int
    duration: float
    output: str

    @property
    def status(self) -> str:
        return "PASS" if self.returncode == 0 else "FAIL"


@dataclass(frozen=True)
class TestCaseResult:
    name: str
    suite: str
    status: str
    detail: str = ""


UNITTEST_CASE_PATTERN = re.compile(
    r"^(?P<name>\S+) \((?P<suite>[^)]+)\) \.\.\. "
    r"(?P<result>ok|FAIL|ERROR|skipped(?: .*)?)$",
    re.MULTILINE,
)


def parse_test_cases(output: str) -> list[TestCaseResult]:
    cases: list[TestCaseResult] = []
    for match in UNITTEST_CASE_PATTERN.finditer(output):
        raw_result = match.group("result")
        if raw_result == "ok":
            status, detail = "PASS", ""
        elif raw_result.startswith("skipped"):
            status, detail = "SKIPPED", raw_result.removeprefix("skipped").strip()
        else:
            status, detail = raw_result, ""
        cases.append(TestCaseResult(match.group("name"), match.group("suite"), status, detail))
    return cases


CHECKS = (
    Check("Project manifest and fixture validation", ("python3", "harness/scripts/project_validator.py", "project")),
    Check("Complete Python unit and regression suite", ("python3", "-m", "unittest", "discover", "-s", "harness/tests/unit", "-v")),
    Check("Isolated Skill package structure", ("python3", "harness/scripts/quick_validate.py")),
)


def run_checks() -> list[CheckResult]:
    results: list[CheckResult] = []
    for check in CHECKS:
        print(f"== {check.name} ==", flush=True)
        started = time.monotonic()
        completed = subprocess.run(check.argv, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
        duration = time.monotonic() - started
        sys.stdout.write(completed.stdout)
        results.append(CheckResult(check.name, check.argv, completed.returncode, duration, completed.stdout))
    return results


def current_commit() -> str:
    completed = subprocess.run(("git", "rev-parse", "HEAD"), cwd=ROOT, text=True, capture_output=True, check=False)
    return completed.stdout.strip() if completed.returncode == 0 else "unknown"


def write_reports(results: list[CheckResult]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    failures = sum(result.returncode != 0 for result in results)
    duration = sum(result.duration for result in results)
    suite = ET.Element("testsuite", name="eda_tester_skill_complete_gate", tests=str(len(results)), failures=str(failures), time=f"{duration:.3f}")
    rows: list[str] = []
    logs: list[str] = []
    case_groups: list[str] = []
    all_cases: list[TestCaseResult] = []
    for result in results:
        case = ET.SubElement(suite, "testcase", classname="jenkins.full_gate", name=result.name, time=f"{result.duration:.3f}")
        if result.returncode:
            failure = ET.SubElement(case, "failure", message=f"exit code {result.returncode}")
            failure.text = result.output
        rows.append(
            "<tr>"
            f"<td>{html.escape(result.name)}</td>"
            f'<td class="{result.status.lower()}">{result.status}</td>'
            f"<td>{result.duration:.3f}s</td>"
            f"<td><code>{html.escape(' '.join(result.argv))}</code></td>"
            "</tr>"
        )
        logs.append(f"== {result.name} ==\n$ {' '.join(result.argv)}\n{result.output}")
        cases = parse_test_cases(result.output)
        all_cases.extend(cases)
        if cases:
            case_rows = []
            for test_case in cases:
                detail = f"<br><small>{html.escape(test_case.detail)}</small>" if test_case.detail else ""
                case_rows.append(
                    "<tr>"
                    f"<td><code>{html.escape(test_case.name)}</code></td>"
                    f"<td>{html.escape(test_case.suite)}</td>"
                    f'<td><span class="badge {test_case.status.lower()}">{test_case.status}</span>{detail}</td>'
                    "</tr>"
                )
            passed = sum(case.status == "PASS" for case in cases)
            case_groups.append(
                '<details class="case-group">'
                f"<summary>{html.escape(result.name)} — {len(cases)} 个用例，{passed} 个通过</summary>"
                '<div class="table-wrap"><table><thead><tr><th>用例</th><th>测试套件</th><th>状态</th></tr></thead>'
                f"<tbody>{''.join(case_rows)}</tbody></table></div></details>"
            )
    ET.ElementTree(suite).write(REPORT_DIR / "junit.xml", encoding="utf-8", xml_declaration=True)
    combined = "\n".join(logs)
    (REPORT_DIR / "complete.log").write_text(combined, encoding="utf-8")
    overall = "PASS" if failures == 0 else "FAIL"
    passed_cases = sum(case.status == "PASS" for case in all_cases)
    failed_cases = sum(case.status in {"FAIL", "ERROR"} for case in all_cases)
    skipped_cases = sum(case.status == "SKIPPED" for case in all_cases)
    page = f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>EDA Tester Skill 完整测试报告</title>
<style>body{{font-family:system-ui;margin:32px;background:#f5f7fb;color:#172033}}main{{max-width:1200px;margin:auto}}.card{{background:white;border:1px solid #dce3ee;border-radius:12px;padding:22px}}.summary-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:18px 0 24px}}.metric{{background:#f8fafc;border:1px solid #e3e8f0;border-radius:10px;padding:14px}}.metric span{{display:block;color:#64748b;font-size:13px}}.metric strong{{display:block;font-size:24px;margin-top:4px}}.structure{{color:#475569}}table{{width:100%;border-collapse:collapse}}th,td{{padding:12px;border-bottom:1px solid #e3e8f0;text-align:left;vertical-align:top}}th{{background:#f8fafc}}.table-wrap{{overflow-x:auto}}.pass{{color:#087830;font-weight:700}}.fail,.error{{color:#b42318;font-weight:700}}.skipped{{color:#8a5b00;font-weight:700}}.badge{{display:inline-block;padding:3px 9px;border-radius:999px;background:#eef2f7;font-size:12px}}details{{margin-top:14px;border:1px solid #dce3ee;border-radius:10px;background:#fff}}summary{{cursor:pointer;padding:14px 16px;font-weight:650}}details table{{border-top:1px solid #e3e8f0}}small{{color:#64748b}}pre{{white-space:pre-wrap;background:#111827;color:#e5e7eb;padding:16px;border-radius:0 0 8px 8px;margin:0}}</style></head><body><main><div class="card">
<h1>EDA Tester Skill 完整测试报告</h1><p>结果：<strong class="{overall.lower()}">{overall}</strong>　提交：<code>{html.escape(current_commit())}</code>　生成时间：{dt.datetime.now(dt.timezone.utc).isoformat()}</p>
<h2>测试结构摘要</h2><p class="structure">完整门禁 → {len(results)} 个检查组 → {len(all_cases)} 个自动化测试用例</p>
<div class="summary-grid"><div class="metric"><span>检查组</span><strong>{len(results)}</strong></div><div class="metric"><span>用例总数</span><strong>{len(all_cases)}</strong></div><div class="metric"><span>通过用例</span><strong>{passed_cases}</strong></div><div class="metric"><span>失败用例</span><strong>{failed_cases}</strong></div><div class="metric"><span>跳过用例</span><strong>{skipped_cases}</strong></div><div class="metric"><span>总耗时</span><strong>{duration:.2f}s</strong></div></div>
<h2>门禁检查</h2>
<table><thead><tr><th>检查项</th><th>状态</th><th>耗时</th><th>命令</th></tr></thead><tbody>{''.join(rows)}</tbody></table>
<h2>测试用例明细</h2><p class="structure">用例表格默认折叠，点击分组标题展开。</p>{''.join(case_groups) or '<p>未从命令输出中识别到测试用例。</p>'}
<details><summary>完整日志</summary><pre>{html.escape(combined)}</pre></details></div></main></body></html>"""
    (REPORT_DIR / "index.html").write_text(page, encoding="utf-8")


def main() -> int:
    results = run_checks()
    write_reports(results)
    return 0 if all(result.returncode == 0 for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
