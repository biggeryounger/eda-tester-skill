
source ./tcl/design.tcl
source $env(PV_ROOT)/scripts/pv.tcl

set init_lef_file $lef_files
set init_verilog $netlist
set init_mmmc_file tcl/itools/mmmc.tcl
set init_gnd_net VSS
set init_pwr_net VDD
set init_top_cell riscv_core
init_design

defIn  test1.def.gz
defOut -scanChain -routing -earlyGlobalRoute test3.def.gz

pv_check_golden test3.def.gz -filter {^#|DESIGN OPMS_CORE_BOX|DESIGN FE_CORE_BOX}
pv_rpt_checkpoints
exit
