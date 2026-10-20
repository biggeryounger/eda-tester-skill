source $env(PV_ROOT)/scripts/pv.tcl
source ./tcl/design.tcl

setMultiCpuUsage -localCpu 8

set init_lef_file $lef_files
set init_verilog $verilog_files
set init_gnd_net $ground_net
set init_pwr_net $power_net
set init_mmmc_file ./tcl/itools/mmmc.tcl
set init_top_cell $init_top_name
init_design

#return
defIn $def_file
