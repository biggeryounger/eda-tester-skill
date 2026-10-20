"""Contract for the runtime design/tech/stage selection instructions."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


class DesignInputSelectionTests(unittest.TestCase):
    def test_both_routes_offer_available_combinations(self):
        text = (ROOT / 'skill/SKILL.md').read_text()
        first, rest = text.split('### 场景二：', 1)
        second, shared = rest.split('### 共享：', 1)
        for route in (first, second):
            self.assertIn('design/tech/stage', route)
            self.assertIn('可选输入列表', route)
        self.assertIn('references/input/design_input_tcl/<tech>/<design>/<stage>/tcl', shared)
        self.assertIn('编号、design、tech、stage、可用工具', shared)
        self.assertIn('实际存在', shared)
        self.assertIn('不得跨 stage', shared)
        self.assertIn('stage 未明确', second)

    def test_selection_requires_matching_files_and_confirmation(self):
        text = (ROOT / 'skill/SKILL.md').read_text()
        self.assertIn('同时存在 `design.tcl` 和 `<tool>/mmmc.tcl`', text)
        self.assertIn('用户选择编号或明确的 design/tech/stage 组合', text)
        self.assertIn('缺失或不唯一', text)
        self.assertIn('SPEC-GAP', text)
