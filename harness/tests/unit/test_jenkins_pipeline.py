from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


class JenkinsPipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.pipeline = (ROOT / "harness" / "jenkins" / "Jenkinsfile").read_text(encoding="utf-8")
        cls.job = (ROOT / "harness" / "jenkins" / "init.groovy.d" / "create-job.groovy").read_text(encoding="utf-8")
        cls.dockerfile = (ROOT / "harness" / "jenkins" / "Dockerfile").read_text(encoding="utf-8")
        cls.compose = (ROOT / "harness" / "jenkins" / "compose.yaml").read_text(encoding="utf-8")
        cls.instructions = (ROOT / "AGENTS.md").read_text(encoding="utf-8")

    def test_full_suite_precedes_report_review_and_merge(self) -> None:
        full_suite = self.pipeline.index("stage('Run complete test suite')")
        report = self.pipeline.index("stage('Publish test report')")
        review = self.pipeline.index("stage('Review and approve')")
        merge = self.pipeline.index("stage('Merge approved commit')")
        self.assertLess(full_suite, report)
        self.assertLess(report, review)
        self.assertLess(review, merge)
        self.assertIn("harness/scripts/run_jenkins_gate.py", self.pipeline)

    def test_approval_is_bound_to_exact_candidate_and_fresh_main(self) -> None:
        self.assertIn('test "$(git rev-parse HEAD)" = "${CANDIDATE_COMMIT}"', self.pipeline)
        self.assertIn('test "${CURRENT_REMOTE_COMMIT}" = "${REMOTE_BASE_COMMIT}"', self.pipeline)
        self.assertIn('"${CANDIDATE_COMMIT}:refs/heads/${TARGET_BRANCH}"', self.pipeline)
        self.assertIn("disableConcurrentBuilds(abortPrevious: false)", self.pipeline)

    def test_job_accepts_candidate_ref_and_loads_pipeline_from_harness(self) -> None:
        self.assertIn("CANDIDATE_REF", self.job)
        self.assertIn("CpsFlowDefinition", self.job)
        self.assertIn("/usr/share/jenkins/ref/Jenkinsfile", self.job)
        self.assertIn("github-eda-tester-skill-push", self.job)

    def test_pipeline_bootstraps_without_requiring_main_to_contain_jenkinsfile(self) -> None:
        self.assertNotIn("checkout scm", self.pipeline)
        self.assertIn("git init", self.pipeline)
        self.assertIn("Jenkinsfile:/usr/share/jenkins/ref/Jenkinsfile:ro", self.compose)

    def test_controller_image_has_test_and_report_dependencies(self) -> None:
        for dependency in ("git", "python3", "python3-openpyxl", "tcl", "junit", "htmlpublisher"):
            self.assertIn(dependency, self.dockerfile)
        self.assertNotIn("nagelfar", self.dockerfile.lower())

    def test_local_startup_is_repeatable_and_avoids_default_jenkins_ports(self) -> None:
        self.assertIn("JENKINS_HTTP_PORT:-8081", self.compose)
        self.assertIn("JENKINS_AGENT_PORT:-50001", self.compose)
        self.assertIn("jenkins.install.runSetupWizard=false", self.compose)
        self.assertIn("create-job.groovy:ro", self.compose)
        self.assertIn("Details.fromPlainPassword(password)", self.job)

    def test_upload_code_is_the_explicit_end_action_trigger(self) -> None:
        section = self.instructions.split("## 用户触发的结束动作", 1)[1]
        self.assertIn("用户明确说“上传代码”", section)
        documentation = section.index("1. 根据本次实际变更更新 `skill/SKILL.md`")
        push = section.index("4. 创建或使用 `codex/` 候选分支")
        jenkins = section.index("5. 使用该远端候选分支")
        approval = section.index("6. 发布测试报告并等待用户审批")
        self.assertLess(documentation, push)
        self.assertLess(push, jenkins)
        self.assertLess(jenkins, approval)


if __name__ == "__main__":
    unittest.main()
