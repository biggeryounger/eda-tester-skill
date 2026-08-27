from __future__ import annotations

import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("tcl_conventions", ROOT / "scripts" / "tcl_convention_validator.py")
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load convention validator")
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)


NITH_RUN = '''#!/opt/Anaconda3-5.2.0-Linux-x86_64/bin/python -B
### NITH initialization, please do not change this section
import os,sys
nith_path="/Data/devops/qa/git/testcase-prime/pv/nith"
nith_path=nith_path if os.path.exists(nith_path) else "/storage/prime_testcase/pv/nith"
envpath=os.path.abspath(sys.argv[0])
for i in range(10):
    envpath=os.path.dirname(envpath)
    if os.path.isfile(envpath+"/nith/main.py"):
        nith_path=envpath+"/nith"; break
sys.path.append(nith_path)
import globalvar as nith; nith._init()
from main import *
### NITH initialization end

# Case setup
nith.input[""] = f"tcl/{nith.PV_TOOL}/run_1.tcl"
nith_run()

nith_done()
'''

NITH_RUN_TWO_STEP = NITH_RUN.replace(
    'nith.input[""] = f"tcl/{nith.PV_TOOL}/run_1.tcl"\nnith_run()\n',
    'nith.input[""] = f"tcl/{nith.PV_TOOL}/run_1.tcl"\nnith_run()\n'
    'nith.input[""] = f"tcl/{nith.PV_TOOL}/run_2.tcl"\nnith_run()\n',
)

DESIGN_TCL = '''# Generated from central design profile: smoke
set init_top_name smoke_top
set verilog_files ./design/smoke.v
set lef_files ./design/smoke.lef
set lib_files ./design/smoke.lib
set sdc_files ./design/smoke.sdc
'''

MMMC_TCL = '''create_lib_set -name slowLibSet -timing_lib ./design/smoke.lib
'''

RUN_TCL = '''# DESIGN_INIT_BEGIN
source $env(PV_ROOT)/scripts/pv.tcl
set tool $env(PV_TOOL)
source ./tcl/design.tcl
set_options setup.lef_file $lef_files
set_options setup.verilog $verilog_files
set_options setup.mmmc_file ./tcl/optimus/mmmc.tcl
set_options setup.top_cell $init_top_name
setup_design
read_def $def
# DESIGN_INIT_END
# EXPECT: PASS
# TEST_ACTION
report_qor
pv_check_log {report_qor} -name smoke -filter {^Date} -match {WNS|TNS}
pv_rpt_checkpoints
exit
'''

RUN_TCL_STEP2 = RUN_TCL.replace("setup_design\nread_def $def\n", "read_db ./work/smoke.db\n")

ITOOLS_RUN_TCL = '''# DESIGN_INIT_BEGIN
source $env(PV_ROOT)/scripts/pv.tcl
source ./tcl/design.tcl
set init_lef_file $lef_files
set init_verilog $verilog_files
set init_top_cell $init_top_name
set init_mmmc_file ./tcl/itools/mmmc.tcl
init_design
read_def $def
# DESIGN_INIT_END
# EXPECT: PASS
# TEST_ACTION
report_qor
pv_check_log {report_qor} -name smoke -filter {^Date}
pv_rpt_checkpoints
exit
'''


class TclConventionValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self._counter = 0

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def build(
        self,
        *,
        name: str = "pos001_smoke",
        tool: str = "optimus",
        nith_run: str = NITH_RUN,
        design: str | None = None,
        mmmc: str = MMMC_TCL,
        runs: dict[str, str] | None = None,
    ) -> Path:
        if runs is None:
            runs = {"run_1.tcl": RUN_TCL}
        if design is None:
            design = DESIGN_TCL + "set def ./design/smoke.def\n"
        self._counter += 1
        case = self.root / f"case_{self._counter}" / name
        case.mkdir(parents=True)
        (case / "nith.run").write_text(nith_run, encoding="utf-8")
        tcl = case / "tcl"
        tcl.mkdir()
        if design:
            (tcl / "design.tcl").write_text(design, encoding="utf-8")
        tool_dir = tcl / tool
        tool_dir.mkdir()
        (tool_dir / "mmmc.tcl").write_text(mmmc, encoding="utf-8")
        for run_name, run_text in runs.items():
            (tool_dir / run_name).write_text(run_text, encoding="utf-8")
        return case

    def rules(self, case_dir: Path) -> list[str]:
        return [item.rule_id for item in VALIDATOR.validate_tcl_conventions(case_dir)]

    def test_valid_single_step_case_passes_all_rules(self) -> None:
        self.assertEqual([], self.rules(self.build()))

    def test_valid_two_step_case_passes_all_rules(self) -> None:
        case = self.build(
            nith_run=NITH_RUN_TWO_STEP,
            runs={"run_1.tcl": RUN_TCL, "run_2.tcl": RUN_TCL_STEP2},
        )
        self.assertEqual([], self.rules(case))

    def test_design_without_central_profile_marker_fails(self) -> None:
        case = self.build(design=DESIGN_TCL.replace("# Generated from central design profile: smoke\n", "") + "set def ./design/smoke.def\n")
        self.assertIn("TCL-DESIGN-003", self.rules(case))

    def test_suite_001_rejects_non_directory_input(self) -> None:
        file_path = self.root / "pos002_file.tcl"
        file_path.write_text(RUN_TCL, encoding="utf-8")
        self.assertIn("TCL-SUITE-001", self.rules(file_path))

    def test_suite_002_rejects_bad_directory_name(self) -> None:
        self.assertIn("TCL-SUITE-002", self.rules(self.build(name="case1_smoke")))

    def test_struct_001_requires_tree_files(self) -> None:
        case = self.build()
        (case / "nith.run").unlink()
        self.assertIn("TCL-STRUCT-001", self.rules(case))

    def test_struct_001_requires_design_tcl_as_standard_file(self) -> None:
        case = self.build(design="")
        self.assertFalse((case / "tcl" / "design.tcl").exists())
        self.assertIn("TCL-STRUCT-001", self.rules(case))

    def test_struct_001_rejects_run_number_gap(self) -> None:
        case = self.build(runs={"run_2.tcl": RUN_TCL})
        self.assertIn("TCL-STRUCT-001", self.rules(case))

    def test_struct_001_requires_mmmc(self) -> None:
        case = self.build()
        (case / "tcl" / "optimus" / "mmmc.tcl").unlink()
        self.assertIn("TCL-STRUCT-001", self.rules(case))

    def test_struct_002_rejects_multiple_tool_dirs(self) -> None:
        case = self.build()
        (case / "tcl" / "itools").mkdir()
        (case / "tcl" / "itools" / "mmmc.tcl").write_text(MMMC_TCL, encoding="utf-8")
        self.assertIn("TCL-STRUCT-002", self.rules(case))

    def test_struct_002_rejects_unknown_tool(self) -> None:
        self.assertIn("TCL-STRUCT-002", self.rules(self.build(tool="primetime")))

    def test_nith_001_requires_verbatim_init_block(self) -> None:
        case = self.build(nith_run=NITH_RUN.replace("### NITH initialization end", "### changed"))
        self.assertIn("TCL-NITH-001", self.rules(case))

    def test_nith_001_setup_must_match_run_files(self) -> None:
        case = self.build(nith_run=NITH_RUN.replace("run_1.tcl", "run_2.tcl"))
        self.assertIn("TCL-NITH-001", self.rules(case))

    def test_nith_001_requires_nith_done(self) -> None:
        case = self.build(nith_run=NITH_RUN.replace("nith_done()", ""))
        self.assertIn("TCL-NITH-001", self.rules(case))

    def test_runner_001_rejects_machine_path_in_run_tcl(self) -> None:
        case = self.build(runs={"run_1.tcl": RUN_TCL + "source /Users/name/setup.tcl\n"})
        self.assertIn("TCL-RUNNER-001", self.rules(case))

    def test_runner_001_exempts_nith_fixed_block(self) -> None:
        self.assertEqual([], self.rules(self.build()))

    def test_runner_001_rejects_machine_path_in_nith_case_setup(self) -> None:
        case = self.build(nith_run=NITH_RUN.replace("# Case setup", "# Case setup\nsome_path = '/Users/name/leak'\n"))
        self.assertIn("TCL-RUNNER-001", self.rules(case))

    def test_runner_002_forbids_external_setup(self) -> None:
        case = self.build(runs={"run_1.tcl": RUN_TCL.replace("# DESIGN_INIT_BEGIN\n", "# DESIGN_INIT_BEGIN\nsource ./tcl/case_setup.tcl\n")})
        self.assertIn("TCL-RUNNER-002", self.rules(case))

    def test_runner_002_resolves_sources_from_case_working_directory(self) -> None:
        with_design = RUN_TCL
        self.assertNotIn(
            "TCL-RUNNER-002",
            self.rules(self.build(design=DESIGN_TCL, runs={"run_1.tcl": with_design})),
        )
        replacements = (("source ./tcl/design.tcl", "source ../design.tcl"),)
        for current, old_path in replacements:
            with self.subTest(old_path=old_path):
                invalid = with_design.replace(current, old_path)
                self.assertIn(
                    "TCL-RUNNER-002",
                    self.rules(self.build(design=DESIGN_TCL, runs={"run_1.tcl": invalid})),
                )

    def test_design_001_validates_declarations_only_when_file_exists(self) -> None:
        self.assertNotIn("TCL-DESIGN-001", self.rules(self.build()))
        self.assertIn("TCL-DESIGN-001", self.rules(self.build(design="# only a comment\n")))

    def test_design_002_rejects_redefinition_of_design_variable_in_run(self) -> None:
        invalid = RUN_TCL.replace(
            "set_options setup.lef_file $lef_files\n",
            "set lef_files ./design/other.lef\nset_options setup.lef_file $lef_files\n",
        )
        self.assertIn("TCL-DESIGN-002", self.rules(self.build(runs={"run_1.tcl": invalid})))

    def test_design_002_requires_run_inputs_to_reuse_design_variables(self) -> None:
        replacements = (
            ("set_options setup.lef_file $lef_files", "set_options setup.lef_file ./design/other.lef"),
            ("set_options setup.verilog $verilog_files", "set_options setup.verilog ./design/other.v"),
            ("set_options setup.top_cell $init_top_name", "set_options setup.top_cell other_top"),
            ("read_def $def", "read_def ./design/other.def"),
        )
        for current, replacement in replacements:
            with self.subTest(replacement=replacement):
                invalid = RUN_TCL.replace(current, replacement)
                self.assertIn("TCL-DESIGN-002", self.rules(self.build(runs={"run_1.tcl": invalid})))

    def test_run_001_requires_mmmc_option_then_setup_then_read_def(self) -> None:
        self.assertNotIn("TCL-RUN-001", self.rules(self.build()))
        no_mmmc = RUN_TCL.replace("set_options setup.mmmc_file ./tcl/optimus/mmmc.tcl\n", "")
        self.assertIn("TCL-RUN-001", self.rules(self.build(runs={"run_1.tcl": no_mmmc})))
        sourced_mmmc = RUN_TCL.replace(
            "set_options setup.mmmc_file ./tcl/optimus/mmmc.tcl\n",
            "source ./tcl/optimus/mmmc.tcl\n",
        )
        self.assertIn("TCL-RUN-001", self.rules(self.build(runs={"run_1.tcl": sourced_mmmc})))
        reordered = RUN_TCL.replace("setup_design\nread_def $def\n", "read_def $def\nsetup_design\n")
        self.assertIn("TCL-RUN-001", self.rules(self.build(runs={"run_1.tcl": reordered})))

    def test_run_001_itools_uses_init_mmmc_file_without_source(self) -> None:
        valid = self.build(tool="itools", runs={"run_1.tcl": ITOOLS_RUN_TCL})
        self.assertNotIn("TCL-RUN-001", self.rules(valid))

        sourced = ITOOLS_RUN_TCL.replace(
            "set init_mmmc_file ./tcl/itools/mmmc.tcl\n",
            "source ./tcl/itools/mmmc.tcl\n",
        )
        invalid = self.build(tool="itools", runs={"run_1.tcl": sourced})
        self.assertIn("TCL-RUN-001", self.rules(invalid))

        wrong_path = ITOOLS_RUN_TCL.replace(
            "set init_mmmc_file ./tcl/itools/mmmc.tcl",
            "set init_mmmc_file ./other/mmmc.tcl",
        )
        invalid_path = self.build(tool="itools", runs={"run_1.tcl": wrong_path})
        self.assertIn("TCL-RUN-001", self.rules(invalid_path))

    def test_run_001_rejects_repeated_init_commands_in_helper_tcl(self) -> None:
        for helper, content in (
            ("design", DESIGN_TCL + "set_options setup.top_cell smoke_top\n"),
            ("mmmc", MMMC_TCL + "source $env(PV_ROOT)/scripts/pv.tcl\n"),
        ):
            with self.subTest(helper=helper):
                kwargs = {helper: content}
                self.assertIn("TCL-RUN-001", self.rules(self.build(**kwargs)))

    def test_checkpoint_001_requires_real_call_in_tree(self) -> None:
        no_check = RUN_TCL.replace(
            "pv_check_log {report_qor} -name smoke -filter {^Date} -match {WNS|TNS}\n",
            "puts done\n",
        )
        self.assertIn("TCL-CHECKPOINT-001", self.rules(self.build(runs={"run_1.tcl": no_check})))

    def test_checkpoint_002_requires_source_before_checkpoint(self) -> None:
        text = (
            "# DESIGN_INIT_BEGIN\nsource ./tcl/design.tcl\n"
            "set_options setup.mmmc_file ./tcl/optimus/mmmc.tcl\nsetup_design\nread_def $def\n# DESIGN_INIT_END\n"
            "# EXPECT: PASS\n# TEST_ACTION\npv_check_log {report_qor}\nsource $env(PV_ROOT)/scripts/pv.tcl\n"
        )
        self.assertIn("TCL-CHECKPOINT-002", self.rules(self.build(runs={"run_1.tcl": text})))

    def test_checkpoint_003_validates_log_call(self) -> None:
        text = RUN_TCL.replace(
            "pv_check_log {report_qor} -name smoke -filter {^Date} -match {WNS|TNS}",
            "pv_check_log {} -name",
        )
        self.assertIn("TCL-CHECKPOINT-003", self.rules(self.build(runs={"run_1.tcl": text})))

    def test_checkpoint_003_accepts_filter_and_match(self) -> None:
        self.assertNotIn("TCL-CHECKPOINT-003", self.rules(self.build()))
        empty_match = RUN_TCL.replace("-match {WNS|TNS}", "-match {}")
        self.assertIn("TCL-CHECKPOINT-003", self.rules(self.build(runs={"run_1.tcl": empty_match})))

    def test_checkpoint_004_validates_golden_call(self) -> None:
        text = RUN_TCL.replace(
            "pv_check_log {report_qor} -name smoke -filter {^Date} -match {WNS|TNS}",
            "pv_check_golden ./out/design.def -golden ../shared/design.def",
        )
        self.assertIn("TCL-CHECKPOINT-004", self.rules(self.build(runs={"run_1.tcl": text})))

    def test_checkpoint_004_accepts_golden_directory_with_optional_dot_prefix(self) -> None:
        for golden in ("golden/optimus.obs.lef", "./golden/optimus.obs.lef"):
            with self.subTest(golden=golden):
                text = RUN_TCL.replace(
                    "pv_check_log {report_qor} -name smoke -filter {^Date} -match {WNS|TNS}",
                    f"pv_check_golden ./out/obs.lef -golden {golden} -filter {{^#}}",
                )
                self.assertNotIn("TCL-CHECKPOINT-004", self.rules(self.build(runs={"run_1.tcl": text})))

    def test_checkpoint_006_requires_clean_generate_compare_order(self) -> None:
        valid = RUN_TCL.replace(
            "pv_check_log {report_qor} -name smoke -filter {^Date} -match {WNS|TNS}",
            "file delete -force ./out/obs.lef\n"
            "write_lef ./out/obs.lef\n"
            "pv_check_golden ./out/obs.lef -golden golden/optimus.obs.lef",
        )
        self.assertNotIn("TCL-CHECKPOINT-006", self.rules(self.build(runs={"run_1.tcl": valid})))

        stale = valid.replace("file delete -force ./out/obs.lef\n", "")
        self.assertIn("TCL-CHECKPOINT-006", self.rules(self.build(runs={"run_1.tcl": stale})))

        wrong_order = valid.replace(
            "write_lef ./out/obs.lef\npv_check_golden ./out/obs.lef -golden golden/optimus.obs.lef",
            "pv_check_golden ./out/obs.lef -golden golden/optimus.obs.lef\nwrite_lef ./out/obs.lef",
        )
        self.assertIn("TCL-CHECKPOINT-006", self.rules(self.build(runs={"run_1.tcl": wrong_order})))

    def test_checkpoint_005_validates_qor_call(self) -> None:
        text = RUN_TCL.replace(
            "pv_check_log {report_qor} -name smoke -filter {^Date} -match {WNS|TNS}",
            "pv_check_qor {report_power} -tolerance -1",
        )
        self.assertIn("TCL-CHECKPOINT-005", self.rules(self.build(runs={"run_1.tcl": text})))

    def test_script_005_requires_checkpoint_summary_then_exit(self) -> None:
        self.assertNotIn("TCL-SCRIPT-005", self.rules(self.build()))
        no_summary = RUN_TCL.replace("pv_rpt_checkpoints\n", "")
        self.assertIn("TCL-SCRIPT-005", self.rules(self.build(runs={"run_1.tcl": no_summary})))
        no_exit = RUN_TCL.replace("exit\n", "")
        self.assertIn("TCL-SCRIPT-005", self.rules(self.build(runs={"run_1.tcl": no_exit})))
        reversed_tail = RUN_TCL.replace("pv_rpt_checkpoints\nexit\n", "exit\npv_rpt_checkpoints\n")
        self.assertIn("TCL-SCRIPT-005", self.rules(self.build(runs={"run_1.tcl": reversed_tail})))

    def test_script_001_requires_per_run_markers_and_polarity(self) -> None:
        no_action = RUN_TCL.replace("# TEST_ACTION\n", "")
        self.assertIn("TCL-SCRIPT-001", self.rules(self.build(name="pos001_bad", runs={"run_1.tcl": no_action})))
        self.assertIn("TCL-SCRIPT-001", self.rules(self.build(name="neg001_bad")))

    def test_script_002_rejects_placeholders_anywhere(self) -> None:
        self.assertIn("TCL-SCRIPT-002", self.rules(self.build(design=DESIGN_TCL + "# TODO later\n")))
        self.assertIn("TCL-SCRIPT-002", self.rules(self.build(nith_run=NITH_RUN.replace("# Case setup", "# Case setup\n# TBD\n"))))

    def test_script_003_allows_only_pv_root_and_pv_tool(self) -> None:
        for index, statement in enumerate(
            ("set entry $env(PV_ENTRY)", "set env(HOME) /x", "puts $::env(OPTIMUS_SETUP)"),
            start=2,
        ):
            with self.subTest(statement=statement):
                text = RUN_TCL.replace("set tool $env(PV_TOOL)\n", f"set tool $env(PV_TOOL)\n{statement}\n")
                self.assertIn("TCL-SCRIPT-003", self.rules(self.build(name=f"pos{index:03d}_env", runs={"run_1.tcl": text})))

    def test_script_004_requires_complete_init_per_run(self) -> None:
        no_activation = RUN_TCL.replace("setup_design\n", "")
        self.assertIn("TCL-SCRIPT-004", self.rules(self.build(runs={"run_1.tcl": no_activation})))
        no_block = RUN_TCL.replace("# DESIGN_INIT_BEGIN\n", "").replace("# DESIGN_INIT_END\n", "")
        self.assertIn("TCL-SCRIPT-004", self.rules(self.build(runs={"run_1.tcl": no_block})))

    def test_script_004_accepts_tool_activation_commands(self) -> None:
        for index, command in enumerate(("setup_design", "init_design", "read_db ./base.db", "restoreDesign ./base.enc", "open_block top", "link_design top"), start=1):
            with self.subTest(command=command):
                text = RUN_TCL.replace("setup_design\n", f"{command}\n")
                self.assertNotIn("TCL-SCRIPT-004", self.rules(self.build(name=f"pos{index:03d}_act", runs={"run_1.tcl": text})))


if __name__ == "__main__":
    unittest.main()
