#!/usr/bin/env python3
"""Run the complete repository gate and publish HTML, JUnit, and text logs."""

from __future__ import annotations

from dataclasses import dataclass
import datetime as dt
import html
from pathlib import Path
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


CHECKS = (
    Check("Project manifest and fixture validation", ("python3", "skill/scripts/validate.py", "project")),
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
    ET.ElementTree(suite).write(REPORT_DIR / "junit.xml", encoding="utf-8", xml_declaration=True)
    combined = "\n".join(logs)
    (REPORT_DIR / "complete.log").write_text(combined, encoding="utf-8")
    overall = "PASS" if failures == 0 else "FAIL"
    page = f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>EDA Tester Skill 完整测试报告</title>
<style>body{{font-family:system-ui;margin:32px;background:#f5f7fb;color:#172033}}main{{max-width:1100px;margin:auto}}.card{{background:white;border:1px solid #dce3ee;border-radius:12px;padding:22px}}table{{width:100%;border-collapse:collapse}}th,td{{padding:12px;border-bottom:1px solid #e3e8f0;text-align:left}}.pass{{color:#087830;font-weight:700}}.fail{{color:#b42318;font-weight:700}}pre{{white-space:pre-wrap;background:#111827;color:#e5e7eb;padding:16px;border-radius:8px}}</style></head><body><main><div class="card">
<h1>EDA Tester Skill 完整测试报告</h1><p>结果：<strong class="{overall.lower()}">{overall}</strong>　提交：<code>{html.escape(current_commit())}</code>　生成时间：{dt.datetime.now(dt.timezone.utc).isoformat()}</p>
<table><thead><tr><th>检查项</th><th>状态</th><th>耗时</th><th>命令</th></tr></thead><tbody>{''.join(rows)}</tbody></table>
<details><summary>完整日志</summary><pre>{html.escape(combined)}</pre></details></div></main></body></html>"""
    (REPORT_DIR / "index.html").write_text(page, encoding="utf-8")


def main() -> int:
    results = run_checks()
    write_reports(results)
    return 0 if all(result.returncode == 0 for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
