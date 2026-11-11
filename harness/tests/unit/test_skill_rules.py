from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]


class SkillRulesTests(unittest.TestCase):
    def test_rules_are_discoverable_and_references_resolve(self):
        import re
        entry = (ROOT / 'skill/SKILL.md').read_text()
        for name in ('input-rules.md', 'output-rules.md'):
            self.assertIn('rules/' + name, entry)
            document = ROOT / 'skill/rules' / name
            self.assertTrue(document.is_file())
            links = re.findall(r'\]\(([^)]+)\)', document.read_text())
            self.assertTrue(links)
            for link in links:
                self.assertTrue((document.parent / link).is_file(), link)
        self.assertFalse(list((ROOT / 'skill/rules').rglob('README.md')))

    def test_rules_survive_link_and_copy_install(self):
        for mode in ('link', 'copy'):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as directory:
                result = subprocess.run(
                    [sys.executable, str(ROOT / 'harness/scripts/install_skill.py'),
                     '--mode', mode, '--skills-dir', directory],
                    capture_output=True, text=True)
                self.assertEqual(0, result.returncode, result.stderr)
                for name in ('input-rules.md', 'output-rules.md'):
                    source = ROOT / 'skill/rules' / name
                    installed = Path(directory) / 'eda-tester-skill/rules' / name
                    self.assertTrue(installed.is_file())
                    self.assertEqual(source.read_bytes(), installed.read_bytes())
