# Design identity and canonical input roots.
set design_name   or1200
set tech_name     TSMC180
set design_dir "$env(PV_ROOT)/svn/openedi/design_data/TSMC180/Itools21.1_Ifp_util0.65/$design_name"
set tech_dir   "$env(PV_ROOT)/svn/openedi/design_data/TSMC180/tsmc180_library"

# top design name (itools default var)
set init_top_name or1200_top
set init_top_cell $init_top_name
# design common setting
set utilization 0.65
set clocks {core_clk}
set period {7.66}
# for fm LEC
set scan_chain_flag 1
if {[string match "*/default/*" [pwd]]} {
    set period {6.66}
    set scan_chain_flag 0
}
set lef_files [list $tech_dir/tcb018gbwp7t_6lm.lef]

set slowlib_liberty_files [list $tech_dir/tcb018gbwp7twc_ccs.lib]

set fastlib_liberty_files [list $tech_dir/tcb018gbwp7tbc_ccs.lib]

# Stage inputs.
set power_net    VDD
set ground_net   GND
set verilog_files [list $design_dir/place.v.gz]
set def_file     $design_dir/place.def.gz
set sdc_files    [list $design_dir/place.sdc]
