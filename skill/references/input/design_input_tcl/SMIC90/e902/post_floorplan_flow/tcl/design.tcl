set design_dir "$env(PV_ROOT)/svn/openedi/design_data/SMIC90/Itools21.1_Ifp_util0.65/e902"
set lib_dir "$env(PV_ROOT)/svn/openedi/design_data/SMIC90/smic90_library"

set derate_tcl "$env(PV_ROOT)/svn/openedi/design_data/SMIC7_C910/set_timing_derate.tcl"
set netlist "$design_dir/floorplan.v.gz"
set def "$design_dir/floorplan.def.gz"
set lef "$lib_dir/scc90nbcd_1p6m_5ic_1mttc_alpa1.lef $lib_dir/scc90nbcd_hd_rvt_ant.lef"
set init_top_cell openE902

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
