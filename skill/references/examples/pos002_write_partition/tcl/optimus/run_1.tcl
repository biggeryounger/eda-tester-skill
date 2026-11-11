
source ./tcl/design.tcl
source $env(PV_ROOT)/scripts/pv.tcl
set_options global.infra.max_thread_count 1
set_options setup.lef_file $lef_files
set_options setup.verilog $netlist
set_options setup.mmmc_file tcl/$PV_TOOL/mmmc.tcl
set_options setup.ground_net VSS
set_options setup.power_net VDD
set_options setup.top_cell $top_name
setup_design
read_def $def

set_obj_floorplan_box -type Module -name x_cr_tcipif_top/x_cr_clic_top/x_cr_clic_arb/x_cr_clic_arb_kernel -location {20 20 300 300}
pv_check_log {
specify_partition -hinst x_cr_tcipif_top/x_cr_clic_top/x_cr_clic_arb/x_cr_clic_arb_kernel -routing_halo 1
} -name $PV_TOOL.partition
place_partition_pin

commit_partition


write_partition -partition cr_clic_arb_kernel_PRIO_WIDTH4_INT_NUM80 -output_dir output

exit
