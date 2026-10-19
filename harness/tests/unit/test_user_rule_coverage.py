from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
REGISTRY = ROOT / "harness" / "references" / "user-rule-coverage.md"
ALLOWED_CATEGORIES = {"workflow", "semantic", "static", "project"}


def load_registry() -> dict:
    text = REGISTRY.read_text(encoding="utf-8")
    blocks = re.findall(r"```json\s*\n(.*?)\n```", text, flags=re.DOTALL)
    if len(blocks) != 1:
        raise AssertionError("registry must contain exactly one fenced JSON manifest")
    return json.loads(blocks[0])


class UserRuleCoverageTests(unittest.TestCase):
    def test_registry_is_project_only_and_well_formed(self) -> None:
        self.assertTrue(REGISTRY.is_file())
        self.assertFalse((ROOT / "skill" / "references" / REGISTRY.name).exists())
        manifest = load_registry()
        self.assertEqual("1.0", manifest.get("schema_version"))
        rules = manifest.get("rules")
        self.assertIsInstance(rules, list)
        self.assertGreater(len(rules), 0)
        ids = [rule.get("id") for rule in rules]
        self.assertEqual(len(ids), len(set(ids)), "rule ids must be unique")
        self.assertEqual([f"USR-{i:03d}" for i in range(1, len(ids) + 1)], ids)
        for rule in rules:
            with self.subTest(rule=rule.get("id")):
                self.assertTrue(rule.get("summary"))
                self.assertIn(rule.get("category"), ALLOWED_CATEGORIES)
                self.assertIsInstance(rule.get("evidence"), list)
                self.assertGreater(len(rule["evidence"]), 0)

    def test_every_rule_has_live_evidence(self) -> None:
        for rule in load_registry()["rules"]:
            with self.subTest(rule=rule["id"]):
                for evidence in rule["evidence"]:
                    path = ROOT / evidence["path"]
                    if evidence.get("must_not_exist"):
                        self.assertFalse(path.exists(), f"forbidden path exists: {path}")
                        continue
                    self.assertTrue(path.is_file(), f"missing evidence file: {path}")
                    content = path.read_text(encoding="utf-8")
                    for token in evidence.get("contains", []):
                        self.assertIn(token, content, f"{rule['id']} missing token in {path}")
                    for token in evidence.get("absent", []):
                        self.assertNotIn(token, content, f"{rule['id']} forbidden token in {path}")

    def test_rule_category_requires_correct_implementation_layer(self) -> None:
        for rule in load_registry()["rules"]:
            paths = [evidence["path"] for evidence in rule["evidence"]]
            with self.subTest(rule=rule["id"], category=rule["category"]):
                if rule["category"] == "workflow":
                    self.assertTrue(any(path in {"skill/SKILL.md", "skill/agents/openai.yaml"} for path in paths))
                elif rule["category"] == "semantic":
                    self.assertTrue(any(path.startswith("skill/references/specs/") for path in paths))
                elif rule["category"] == "static":
                    self.assertTrue(any(path.startswith("skill/scripts/") for path in paths))
                    self.assertTrue(any(path.startswith("harness/tests/unit/") for path in paths))
                elif rule["category"] == "project":
                    self.assertTrue(any(path == "AGENTS.md" for path in paths))
                    self.assertTrue(any(path.startswith("harness/tests/unit/") for path in paths))


if __name__ == "__main__":
    unittest.main()
