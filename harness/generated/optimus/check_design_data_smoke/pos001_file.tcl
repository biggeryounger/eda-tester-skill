# Optimus check_design_data Smoke case: minimal legal call with the required -file only.
if {![info exists env(PV_ROOT)] || $env(PV_ROOT) eq ""} {
    error "PV_ROOT must identify the configured PV installation"
}

source $env(PV_ROOT)/scripts/pv.tcl

# DESIGN_INIT_BEGIN
# Optimus 21.1 default design profile (F-018 registered defaults, anchored on PV_ROOT).
set design_dir "$env(PV_ROOT)/svn/openedi/design_data/SMIC28/Itools21.1_lfp_util0.65/riscv_core"
set tech_dir "$env(PV_ROOT)/svn/openedi/design_data/SMIC28/smic28_library"

# Materialize the registered default MMMC config so setup_design can source it.
# Variable references stay literal inside the braces and resolve when mmmc.tcl runs.
set mmmc_channel [open "./mmmc.tcl" w]
puts $mmmc_channel {create_lib_set -name slowLibSet_40c -timing_lib $tech_dir/scc28nhkcp_hsc30p140_rvt_ss_v0p9_-40c_ccs.lib
create_lib_set -name fastLibSet_40c -timing_lib $tech_dir/scc28nhkcp_hsc30p140_rvt_ff_v1p05_-40c_ccs.lib
create_lib_set -name slowLibSet_125c -timing_lib $tech_dir/scc28nhkcp_hsc30p140_rvt_ss_v0p9_125c_ccs.lib
create_lib_set -name fastLibSet_125c -timing_lib $tech_dir/scc28nhkcp_hsc30p140_rvt_ff_v1p05_125c_ccs.lib
create_rc_corner -name corner_RCbest
create_rc_corner -name corner_RCworst
create_rc_corner -name corner_Cbest
create_rc_corner -name corner_Cworst
create_analysis_corner -name delay_corner_rcbest -rc_corner corner_RCbest -late_lib_set slowLibSet_40c -early_lib_set fastLibSet_40c
create_analysis_corner -name delay_corner_rcworst -rc_corner corner_RCworst -late_lib_set slowLibSet_40c -early_lib_set fastLibSet_40c
create_analysis_corner -name delay_corner_cbest -rc_corner corner_Cbest -late_lib_set slowLibSet_125c -early_lib_set fastLibSet_125c
create_analysis_corner -name delay_corner_cworst -rc_corner corner_Cworst -late_lib_set slowLibSet_125c -early_lib_set fastLibSet_125c
create_analysis_mode -name func_max_mode -constraint_file $design_dir/floorplan.sdc
create_analysis_mode -name func_min_mode -constraint_file $design_dir/floorplan.sdc
create_analysis_view -name func_rcbest -analysis_mode func_min_mode -analysis_corner delay_corner_rcbest
create_analysis_view -name func_rcworst -analysis_mode func_max_mode -analysis_corner delay_corner_rcworst
create_analysis_view -name func_cbest -analysis_mode func_min_mode -analysis_corner delay_corner_cbest
create_analysis_view -name func_cworst -analysis_mode func_max_mode -analysis_corner delay_corner_cworst
set_analysis_view_status -view func_rcworst -active true -setup true -hold false
set_analysis_view_status -view func_cworst -active true -setup true -hold false
set_analysis_view_status -view func_rcbest -active true -setup false -hold true
set_analysis_view_status -view func_cbest -active true -setup false -hold true}
close $mmmc_channel

set_options global.infra.max_thread_count 4
set_options setup.lef_file [list "$tech_dir/sec28n_12t25od33_1p8m_7ic_1tmc_alpa1_WITH_NDR.lef" "$tech_dir/sc28nhkcp_hsc30p140_rvt_ant.lef"]
set_options setup.verilog "$design_dir/floorplan.v.gz"
set_options setup.ground_net VSS
set_options setup.power_net VDD
set_options setup.mmmc_file ./mmmc.tcl
set_options setup.top_cell riscv_core
setup_design
# DESIGN_INIT_END

set report_dir ./out/check_design_data
set report_file [file join $report_dir check_design_data.rpt]
file mkdir $report_dir
file delete -force $report_file

# EXPECT: PASS
# TEST_ACTION
pv_check_log {
    check_design_data -file $report_file
    if {![file isfile $report_file]} {
        error "check_design_data did not generate the report file: $report_file"
    }
    if {[file size $report_file] <= 0} {
        error "check_design_data generated an empty report file: $report_file"
    }
} -name check_design_data_file
