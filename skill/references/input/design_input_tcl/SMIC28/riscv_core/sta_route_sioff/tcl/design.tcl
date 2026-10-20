# Design identity and canonical input roots.
set design_name riscv_core
set tech_name SMIC28
set init_top_name riscv_core
set init_top_cell $init_top_name
set design_dir "$env(PV_ROOT)/svn/openedi/design_data/SMIC28/Itools21.1_Ifp_util0.65/$design_name"
set tech_dir "$env(PV_ROOT)/svn/openedi/design_data/SMIC28/smic28_library"

set power_net VDD
set ground_net VSS

set lef_files [list \
    $tech_dir/scc28n_12t25od33_1p8m_7ic_1tmc_alpa1_WITH_NDR.lef \
    $tech_dir/scc28nhkcp_hsc30p140_rvt_ant.lef]
set slowlibset_40c_liberty_files [list $tech_dir/scc28nhkcp_hsc30p140_rvt_ss_v0p9_-40c_ccs.lib]
set fastlibset_40c_liberty_files [list $tech_dir/scc28nhkcp_hsc30p140_rvt_ff_v1p05_-40c_ccs.lib]
set slowlibset_125c_liberty_files [list $tech_dir/scc28nhkcp_hsc30p140_rvt_ss_v0p9_125c_ccs.lib]
set fastlibset_125c_liberty_files [list $tech_dir/scc28nhkcp_hsc30p140_rvt_ff_v1p05_125c_ccs.lib]
set liberty_files [concat $slowlibset_40c_liberty_files $fastlibset_40c_liberty_files $slowlibset_125c_liberty_files $fastlibset_125c_liberty_files]

set verilog_files [list $design_dir/route.v.gz]
set def_file $design_dir/route.def.gz
set sdc_files [list $design_dir/route.sdc]
set utilization 0.65
set clocks {core_clk}
set period {1}
set scan_chain_flag 1
