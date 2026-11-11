
source ./tcl/design.tcl
source $env(PV_ROOT)/scripts/pv.tcl

set_options setup.lef_file $lef_files
set_options setup.verilog $netlist
set_options setup.mmmc_file tcl/optimus/mmmc.tcl
set_options setup.ground_net VSS
set_options setup.power_net VDD
set_options setup.top_cell riscv_core
setup_design

read_def -keep_shape test1.def.gz
write_def test2.def.gz

pv_check_golden test2.def.gz -filter {^#|DESIGN OPMS_CORE_BOX|DESIGN FE_CORE_BOX}
pv_rpt_checkpoints
exit
