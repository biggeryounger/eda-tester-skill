source $env(PV_ROOT)/scripts/pv.tcl
source ./tcl/design.tcl

set_options global.infra.max_thread_count 8

set_options setup.lef_file $lef_files
set_options setup.verilog $verilog_files
set_options setup.ground_net $ground_net
set_options setup.power_net $power_net
set_options setup.mmmc_file ./tcl/optimus/mmmc.tcl
set_options setup.top_cell $init_top_name
setup_design

#return
read_def $def_file
