source $env(PV_ROOT)/scripts/pv.tcl
#======= init run design ========
source ./tcl/design.tcl
set_options setup.lef_file $lef_files
set_options setup.verilog $netlist
set_options setup.mmmc_file ./tcl/optimus/mmmc.tcl
setup_design

#======= test_point ========
place
pv_check_qor {
report_qor -place -view func_fast_CMIN -hold -output_dir qor_files_01
report_qor -place -view func_slow_CMAX -output_dir qor_files_02
} -name $PV_TOOL.report_qor
pv_rpt_checkpoints
exit
