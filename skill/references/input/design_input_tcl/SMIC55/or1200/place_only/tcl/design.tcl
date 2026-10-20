# Design identity and canonical input roots.
set design_name   or1200
set tech_name     SMIC55
set design_dir "$env(PV_ROOT)/svn/openedi/design_data/SMIC55/Itools21.1_Ifp_util0.65/$design_name"
set tech_dir   "$env(PV_ROOT)/svn/openedi/design_data/SMIC55/smic55_library"

# top design name (itools default var)
set init_top_name or1200_top
set init_top_cell $init_top_name
# design common setting
set utilization 0.65
set clocks {core_clk}
set period {7.66}
# for fm LEC
set scan_chain_flag 1
set lef_files [list $tech_dir/scc55nll_9m_8ic_1mttc_alpa1.lef $tech_dir/scc55nll_hd_rvt_ant.lef]

set slowlibset_40c_liberty_files [list $tech_dir/scc55nll_hd_rvt_ss_v1p08_-40c_ccs.lib]

set slowlibset_125c_liberty_files [list $tech_dir/scc55nll_hd_rvt_ss_v1p08_125c_ccs.lib]

set fastlibset_0c_liberty_files [list $tech_dir/scc55nll_hd_rvt_ff_v1p32_0c_ccs.lib]

# Stage inputs.
set power_net    VDD
set ground_net   GND
set verilog_files [list $design_dir/floorplan.v.gz]
set def_file     $design_dir/floorplan.def.gz
set sdc_files    [list $design_dir/floorplan.sdc]
