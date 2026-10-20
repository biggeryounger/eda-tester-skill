set lib_dir "$env(PV_ROOT)/svn/openedi/design_data/SMIC28/smic28_library"

set derate_tcl tcl/$PV_TOOL/set_timing_derate.tcl
set netlist "./design/rtl/alu.syn.v"
set lef "$lib_dir/scc28n_12t25od33_1p8m_7ic_1tmc_alpa1_WITH_NDR.lef $lib_dir/scc28nhkcp_hsc30p140_rvt_ant.lef"

set init_top_cell alu

if {$PV_TOOL == "optimus"} {
    set rc_best_tech "$lib_dir/hsc30p140_rvt_ff_v1p05_-40c.enTech"
    set rc_worst_tech "$lib_dir/hsc30p140_rvt_ss_v0p9_-40c.enTech"
    set c_best_tech "$lib_dir/hsc30p140_rvt_ff_v1p05_125c.enTech"
    set c_worst_tech "$lib_dir/hsc30p140_rvt_ss_v0p9_125c.enTech"
} else {
    set rc_best_tech "$lib_dir/hsc30p140_rvt_ff_v1p05_-40c.qrcTech"
    set rc_worst_tech "$lib_dir/hsc30p140_rvt_ss_v0p9_-40c.qrcTech"
    set c_best_tech "$lib_dir/hsc30p140_rvt_ff_v1p05_125c.qrcTech"
    set c_worst_tech "$lib_dir/hsc30p140_rvt_ss_v0p9_125c.qrcTech"
}

set node 28
