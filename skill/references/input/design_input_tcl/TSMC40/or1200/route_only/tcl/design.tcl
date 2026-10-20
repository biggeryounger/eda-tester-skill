# Design identity and canonical input roots.
set design_name   or1200
set tech_name     TSMC40
set design_dir "$env(PV_ROOT)/svn/openedi/design_data/TSMC40/Itools21.1_Ifp_util0.65/$design_name"
set tech_dir   "$env(PV_ROOT)/svn/openedi/design_data/TSMC40/tsmc40_library"

# top design name (itools default var)
set init_top_name or1200_top
set init_top_cell $init_top_name
# design common setting
set utilization 0.65
set clocks {core_clk}
set period {3.2}
# for fm LEC
set scan_chain_flag 1
set lef_files [list $tech_dir/tcbn40lpbwp_8lm5X2ZRDL_WITH_NDR.lef]

set slowlib_liberty_files [list $tech_dir/tcbn40lpbwpwc_ccs.lib]

set fastlib_liberty_files [list $tech_dir/tcbn40lpbwpbc_ccs.lib]

# Stage inputs.
set power_net    VDD
set ground_net   GND
set verilog_files [list $design_dir/postcts.v.gz]
set def_file     $design_dir/postcts.def.gz
set sdc_files    [list $design_dir/postcts.sdc]
