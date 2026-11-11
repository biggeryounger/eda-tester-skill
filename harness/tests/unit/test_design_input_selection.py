"""Input contracts for the current management table and tool templates."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


class DesignInputSelectionTests(unittest.TestCase):
    def test_workflow_resolves_process_from_management_table(self):
        text = (ROOT / 'skill/SKILL.md').read_text()
        self.assertEqual(1, text.count('## Workflow'))
        self.assertNotIn('### 场景一', text)
        self.assertNotIn('### 场景二', text)
        section = text.split('### 4.', 1)[1].split('### 5.', 1)[0]
        self.assertIn('assets/输入件管理表.json', section)
        self.assertIn('`smic180`', section)
        self.assertIn('WAIT-DESIGN-CONFIRMATION', section)
        self.assertIn('明确批准', section)
        self.assertIn('WAIT-PLAN-FIX', section)
        self.assertIn('所有阻塞问题均已获得明确且一致的输入', section)

    def test_generation_connects_selected_tool_and_process_inputs(self):
        text = (ROOT / 'skill/SKILL.md').read_text().split('### 5.', 1)[1]
        for token in ('每条 Excel 用例生成一个用例目录',
                      'assets/templates/tool_cmd/common/design.tcl',
                      'assets/templates/tool_cmd/<tool>/', '`init.tcl`、`mmmc.tcl`',
                      'LEF 和 LIB 路径', '`smic180` 配置', 'SPEC-GAP', '停止交付'):
            self.assertIn(token, text)
