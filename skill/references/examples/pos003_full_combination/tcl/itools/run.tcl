source $env(PV_ROOT)/scripts/pv.tcl
#======= init run design ========
source ./tcl/design.tcl
set init_lef_file $lef_files
set init_verilog $netlist
set init_mmmc_file ./tcl/itools/mmmc.tcl
init_design

#======= test_point ========
place_opt_design -place
pv_check_qor {
timeDesign -preCTS -hold -outDir qor_files_01
timeDesign -preCTS -outDir qor_files_02
} -name $PV_TOOL.report_qor
pv_rpt_checkpoints
exit
