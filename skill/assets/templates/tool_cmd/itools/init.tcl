source $env(PV_ROOT)/scripts/pv.tcl
source ./tcl/design.tcl
set init_lef_file $lef_files
set init_verilog $netlist_file
set init_pwr_net $power_net
set init_gnd_net $ground_net
set init_mmmc_file ./tcl/itools/mmmc.tcl
set init_top_cell $init_top_name
init_design
defIn $def_file