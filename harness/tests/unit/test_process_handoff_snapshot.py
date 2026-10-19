import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PROCESS = ROOT / "harness" / "PROCESS.MD"


class ProcessHandoffSnapshotTests(unittest.TestCase):
    def setUp(self):
        self.text = PROCESS.read_text(encoding="utf-8")

    def test_snapshot_is_the_first_project_section(self):
        headings = re.findall(r"^## .+$", self.text, flags=re.MULTILINE)
        self.assertTrue(headings)
        self.assertEqual(headings[0], "## 当前交接快照")

    def test_snapshot_has_exactly_the_fixed_fields(self):
        snapshot = self.text.split("## 当前交接快照", 1)[1].split("\n## ", 1)[0]
        fields = re.findall(r"^- ([^：\n]+)：", snapshot, flags=re.MULTILINE)
        self.assertEqual(
            fields,
            ["当前功能", "工作区状态", "最近验证", "阻塞项", "下一条命令", "涉及文件"],
        )

    def test_history_is_separate_from_current_snapshot(self):
        snapshot_pos = self.text.index("## 当前交接快照")
        history_pos = self.text.index("## 历史记录")
        self.assertLess(snapshot_pos, history_pos)
        snapshot = self.text[snapshot_pos:history_pos]
        history = self.text[history_pos:]
        self.assertNotRegex(snapshot, r"^## 已完成工作$", msg="历史完成记录不得留在当前快照")
        self.assertIn("### 已完成工作", history)
        self.assertRegex(history, r"2026-\d{2}-\d{2}")


if __name__ == "__main__":
    unittest.main()
