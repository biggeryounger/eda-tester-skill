set design_dir "./design"
set lib_dir "$env(PV_ROOT)/data_center/PDK/N7/library/lib"
set tech_dir "$env(PV_ROOT)/svn/openedi/design_data/SMIC7_C910/1p13m_rc_tech"

if {$PV_TOOL == "itools"} {
    set worst_rc_tech "$env(PV_ROOT)/svn/openedi/design_data/SMIC7_C910/library/rc_tech/cworst_ccworst_T/qrcTechFile"
    set best_rc_tech "$env(PV_ROOT)/svn/openedi/design_data/SMIC7_C910/library/rc_tech/cbest_ccbest_T/qrcTechFile"
    set derate_tcl "tcl/$PV_TOOL/set_timing_derate.tcl"
} else {
    set worst_rc_tech "$env(PV_ROOT)/svn/openedi/design_data/SMIC7_C910/1p13m_rc_tech/cworst_ccworst_T/rc_tech"
    set best_rc_tech "$env(PV_ROOT)/svn/openedi/design_data/SMIC7_C910/1p13m_rc_tech/cbest_ccbest_T/rc_tech"
    set derate_tcl "tcl/$PV_TOOL/set_timing_derate.tcl"
}
