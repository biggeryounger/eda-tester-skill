
source ./tcl/design.tcl
source $env(PV_ROOT)/scripts/pv.tcl 
set_options setup.lef_file $lef_files
set_options setup.verilog $netlist
set_options setup.mmmc_file tcl/optimus/mmmc.tcl
set_options setup.ground_net VSS
set_options setup.power_net VDD
set_options setup.top_cell riscv_core
setup_design
add_special_wire -layer M1 -net VDD -rect {10 10 40 50}
add_special_wire -layer M1 -net VDD -rect {30 10 50 50}
write_def test1.def.gz
pv_check_golden test1.def.gz -filter {^#|DESIGN OPMS_CORE_BOX|DESIGN FE_CORE_BOX}
pv_rpt_checkpoints
exit