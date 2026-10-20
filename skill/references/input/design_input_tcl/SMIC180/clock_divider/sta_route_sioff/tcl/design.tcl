# Design identity and canonical input roots.
set design_name clock_divider
set tech_name SMIC180
set init_top_name clkdivider
set init_top_cell $init_top_name
set design_dir "$env(PV_ROOT)/svn/openedi/design_data/SMIC180/Itools21.1_Ifp_util0.65/$design_name"
set tech_dir "$env(PV_ROOT)/svn/openedi/large/SMIC180_new/smic180_library"

set power_net VDD
set ground_net VSS

set lef_files [list $tech_dir]
set slowlib_liberty_files [list $tech_dir/slow.lib]
set fastlib_liberty_files [list $tech_dir/fast.lib]
set liberty_files [concat $slowlib_liberty_files $fastlib_liberty_files]

set verilog_files [list $design_dir/route.v.gz]
set def_file $design_dir/route.def.gz
set sdc_files [list $design_dir/route.sdc]
set clocks {clk}
set period {0.55}
