#case initial
source ./tcl/case_setup.tcl
source $env(PV_ROOT)/scripts/pv.tcl
set_options global.infra.max_thread_count 1
set_options setup.lef_file $lef_files
set_options setup.verilog $netlist
set_options setup.mmmc_file tcl/$PV_TOOL/mmmc.tcl
set_options setup.ground_net VSS
set_options setup.power_net VDD
set_options setup.top_cell $init_top_cell
setup_design

#test step
add_cell_obs -cell BUFV10_140P9T30R -layer M1 -rect {0 0 1 1} -mask 0
add_cell_obs -cell BUFV10_140P9T30R -layer M2 -rect {0 0 1 1} -design_rule_width 2
add_cell_obs -cell BUFV10_140P9T30R -layer M3 -polygon {0 0 0 2 2 2 2 1 1 1 1 0} -mask 0
add_cell_obs -cell BUFV10_140P9T30R -layer M5 -rect {-1 -1 1 1} -spacing 1.5
#add_cell_obs -cell [get_obj [get_lib_cell BUFV10_140P9T30R] .base_name] -layer 4 -rect {0.5 0.5 1 1}

write_lef obs.lef
write_db obs

#check point
pv_check_golden obs.lef -golden golden/$PV_TOOL.obs_after_read_db.lef -filter {“#”}
pv_check_log {write_lef obs_after_read_db.lef} -name check_write_lef -filter {"date"|"^#"} -match {ID-0001|ID-0002}
pv_rpt_checkpoints
exit