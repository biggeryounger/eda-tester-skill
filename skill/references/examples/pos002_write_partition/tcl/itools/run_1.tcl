
source ./tcl/design.tcl
source $env(PV_ROOT)/scripts/pv.tcl
setMultiCpuUsage -localCpu 1
set init_lef_file $lef_files
set init_verilog $netlist
set init_mmmc_file tcl/$PV_TOOL/mmmc.tcl
set init_gnd_net VSS
set init_pwr_net VDD
set init_top_cell $top_name
init_design
defIn $def

setObjFPlanBox Module x_cr_tcipif_top/x_cr_clic_top/x_cr_clic_arb/x_cr_clic_arb_kernel 20 20 300 300
pv_check_log {
definePartition -hinst x_cr_tcipif_top/x_cr_clic_top/x_cr_clic_arb/x_cr_clic_arb_kernel -routingHalo 1
} -name $PV_TOOL.partition
assignPtnPin

partition

savePartition cr_clic_arb_kernel_PRIO_WIDTH4_INT_NUM80

exit
