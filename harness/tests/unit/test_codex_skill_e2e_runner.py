from __future__ import annotations

import json
import os
import stat
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CASE_DIR = ROOT / "harness" / "tests" / "e2e" / "optimus_check_design_data_full_workflow"
RUNNER = CASE_DIR / "run_agent_case.py"


class CodexSkillE2ERunnerTests(unittest.TestCase):
    def make_fake_codex(self, root: Path) -> Path:
        script = root / "fake-codex"
        script.write_text(
            textwrap.dedent(
                f'''\
                #!{sys.executable}
                import json, os, shutil, subprocess, sys
                from pathlib import Path

                args = sys.argv[1:]
                workspace = Path(os.environ["EDA_E2E_WORKSPACE"])
                calls = Path(os.environ["EDA_E2E_CALLS"])
                with calls.open("a", encoding="utf-8") as stream:
                    stream.write(json.dumps(args, ensure_ascii=False) + "\\n")
                output_file = Path(args[args.index("-o") + 1])
                is_resume = len(args) > 1 and args[0] == "exec" and args[1] == "resume"
                prompt = args[-1]
                if not is_resume:
                    state = "WAIT-STRATEGY"
                    event = {{"type": "thread.started", "thread_id": "11111111-1111-4111-8111-111111111111"}}
                elif "三种策略" in prompt:
                    state = "WAIT-DESIGN-CONFIRMATION"
                    temp = workspace / "prepared"
                    subprocess.run([{json.dumps(sys.executable)}, {json.dumps(str(CASE_DIR / 'run_case.py'))}, "--output", str(temp)], check=True, capture_output=True)
                    (workspace / "delivery").mkdir(exist_ok=True)
                    shutil.copy2(temp / "测试用例设计表.xlsx", workspace / "delivery" / "测试用例设计表.xlsx")
                    event = {{"type": "turn.started"}}
                else:
                    state = "DELIVERED"
                    temp = workspace / "prepared"
                    delivery = workspace / "delivery"
                    for item in temp.iterdir():
                        target = delivery / item.name
                        if target.exists():
                            continue
                        shutil.copytree(item, target) if item.is_dir() else shutil.copy2(item, target)
                    event = {{"type": "turn.started"}}
                output_file.write_text(json.dumps({{"state": state, "summary": state, "artifacts": []}}, ensure_ascii=False), encoding="utf-8")
                print(json.dumps(event))
                print(json.dumps({{"type": "item.completed", "item": {{"type": "agent_message", "text": state}}}}))
                print(json.dumps({{"type": "turn.completed"}}))
                '''
            ),
            encoding="utf-8",
        )
        script.chmod(script.stat().st_mode | stat.S_IXUSR)
        return script

    def test_drives_three_codex_turns_and_validates_agent_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            root = Path(temporary_dir)
            output = root / "actual"
            calls = root / "calls.jsonl"
            fake = self.make_fake_codex(root)
            environment = os.environ.copy()
            environment["EDA_E2E_CALLS"] = str(calls)
            completed = subprocess.run(
                [sys.executable, str(RUNNER), "--codex-bin", str(fake), "--output", str(output)],
                cwd=ROOT,
                env=environment,
                capture_output=True,
                text=True,
            )
            self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
            result = json.loads((output / "agent-e2e-result.json").read_text(encoding="utf-8"))
            self.assertEqual("PASS", result["status"])
            self.assertEqual(
                ["WAIT-STRATEGY", "WAIT-DESIGN-CONFIRMATION", "DELIVERED"],
                [turn["state"] for turn in result["turns"]],
            )
            invocations = [json.loads(line) for line in calls.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(3, len(invocations))
            self.assertEqual("exec", invocations[0][0])
            self.assertIn("--json", invocations[0])
            self.assertIn("$eda-tester-skill", invocations[0][-1])
            self.assertEqual(["exec", "resume"], invocations[1][:2])
            self.assertEqual(["exec", "resume"], invocations[2][:2])
            self.assertTrue((output / "workspace" / "delivery" / "测试用例设计表.xlsx").is_file())
            self.assertTrue((output / "workspace" / "delivery" / "cases").is_dir())

    def test_reports_incompatible_codex_as_tool_unavailable(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            root = Path(temporary_dir)
            fake = root / "incompatible-codex"
            fake.write_text(
                f'#!{sys.executable}\nimport sys\nsys.stderr.write("failed to load models cache: unknown variant max\\n")\nraise SystemExit(1)\n',
                encoding="utf-8",
            )
            fake.chmod(fake.stat().st_mode | stat.S_IXUSR)
            output = root / "actual"
            completed = subprocess.run(
                [sys.executable, str(RUNNER), "--codex-bin", str(fake), "--output", str(output)],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(2, completed.returncode)
            result = json.loads((output / "agent-e2e-result.json").read_text(encoding="utf-8"))
            self.assertEqual("TOOL_UNAVAILABLE", result["status"])


if __name__ == "__main__":
    unittest.main()
