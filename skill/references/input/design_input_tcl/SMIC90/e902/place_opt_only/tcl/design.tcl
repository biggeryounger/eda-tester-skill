# Design identity and canonical input roots.
set design_name   e902
set tech_name     SMIC90
set design_dir "$env(PV_ROOT)/svn/openedi/design_data/SMIC90/Itools21.1_Ifp_util0.65/$design_name"
set tech_dir   "$env(PV_ROOT)/svn/openedi/design_data/SMIC90/smic90_library"

# top design name (itools default var)
set init_top_name openE902
set init_top_cell $init_top_name
# design common setting
set utilization 0.65
set clocks {CPU_CLK JTG_CLK}
set period {13.6 21}
# for fm LEC
set scan_chain_flag 1
if {[string match "*/default/*" [pwd]]} {
    set period {12.6 20}
    set scan_chain_flag 0
}
set lef_files [list $tech_dir/scc90nbcd_1p6m_5ic_1mttc_alpa1.lef $tech_dir/scc90nbcd_hd_rvt_ant.lef]

set slowlib_liberty_files [list $tech_dir/scc90nbcd_hd_rvt_ss_v1p08_125c_ccs.lib]

set fastlib_liberty_files [list $tech_dir/scc90nbcd_hd_rvt_ff_v1p32_125c_ccs.lib]

# Stage inputs.
set power_net    VDD
set ground_net   VSS
set verilog_files [list $design_dir/place.v.gz]
set def_file     $design_dir/place.def.gz
set sdc_files    [list $design_dir/place.sdc]
