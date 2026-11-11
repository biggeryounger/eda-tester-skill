
source ./tcl/design.tcl
source $env(PV_ROOT)/scripts/pv.tcl

set init_lef_file $lef_files
set init_verilog $netlist
set init_mmmc_file tcl/itools/mmmc.tcl
set init_gnd_net VSS
set init_pwr_net VDD
set init_top_cell riscv_core
init_design
add_shape -layer M1 -net VDD -rect {10 10 40 50}
add_shape -layer M1 -net VDD -rect {30 10 50 50}
defOut -scanChain -routing -earlyGlobalRoute test1.def.gz
pv_check_golden test1.def.gz -filter {^#|DESIGN OPMS_CORE_BOX|DESIGN FE_CORE_BOX}
pv_rpt_checkpoints
exit
