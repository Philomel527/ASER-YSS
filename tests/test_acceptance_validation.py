"""用实际验收源文件的故障变体检查静态检查器，不执行 Windows 播放器。"""

from pathlib import Path
import runpy
import unittest


ROOT = Path(__file__).resolve().parents[1]
CHECK = runpy.run_path(str(ROOT / "tools/check_acceptance.py"))
MAIN = "00_all_features.astoryx"


class AcceptanceValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = (ROOT / "story-code" / MAIN).read_text()

    def reject_change(self, before, after, expected):
        self.assertIn(before, self.source)
        changed = self.source.replace(before, after, 1)
        with self.assertRaisesRegex(ValueError, expected):
            CHECK["check_story"](MAIN, changed)

    def test_unknown_named_parameter(self):
        self.reject_change(",@Volume=0.18", ",@Volumee=0.18", "没有参数")

    def test_missing_background(self):
        self.reject_change("背景：bg_amb2026", "背景：不存在的验收背景", "背景不存在")

    def test_missing_branch_target(self):
        self.reject_change("分支：_,@Branches=选择汇合", "分支：_,@Branches=不存在的落点", "分支落点不存在")

    def test_block_argument_count(self):
        self.reject_change("#use 镜头(bg_amb2026,0.3)", "#use 镜头(bg_amb2026)", "参数个数")

    def test_recursive_macro(self):
        self.reject_change(
            "#use 提示([M18] 内层提示块已展开；这不是运行时函数调用。)",
            "#use 嵌套镜头($(bg))", "递归循环",
        )

    def test_misplaced_rule_header(self):
        self.reject_change("#useRule:AdvanceRule", "//#useRule:AdvanceRule", "第二行")

    def test_literal_backslash_t_is_not_a_tab(self):
        self.reject_change("\t[M01]", "\\t[M01]", "真正 Tab")

    def test_non_integer_slot(self):
        self.reject_change(",@SlotIndex=1", ",@SlotIndex=1.5", "不是整数")

    def test_duplicate_parameter(self):
        self.reject_change(",@Volume=0.18", ",@Volume=0.18,@Volume=0.1", "重复")

    def test_unprotected_parameter_like_dialogue(self):
        before = "&{[M03] 原样显示：10/2=5；,@Volume=0.7；这些都属于台词。}"
        self.reject_change(before, before[2:-1], "没有参数")

    def test_metadata_conflict_is_not_accepted_in_main(self):
        with self.assertRaisesRegex(ValueError, "维数不符合"):
            CHECK["check_value"]("Character", "MoveCurve", "Linear,OutQuad", MAIN, [])

    def test_base_rule_single_prefix_branch_is_checked(self):
        source = (ROOT / "story-code/01_base_rule.astoryx").read_text()
        changed = source.replace("分支：choice/基础甲,基础乙", "分支：choice/不存在的甲,基础乙", 1)
        self.assertNotEqual(source, changed)
        with self.assertRaisesRegex(ValueError, "分支落点不存在"):
            CHECK["check_story"]("01_base_rule.astoryx", changed)

    def test_both_core_stories_cover_all_parameters(self):
        for file in [MAIN, "01_base_rule.astoryx"]:
            with self.subTest(file=file):
                result = CHECK["check_story"](file)
                self.assertEqual(21, len(result["expanded_controllers"]))
                self.assertEqual(101, result["explicit_parameter_count"])
                self.assertEqual({}, result["missing_parameters"])


if __name__ == "__main__":
    unittest.main()
