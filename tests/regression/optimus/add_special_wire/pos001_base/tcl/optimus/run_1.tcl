# DESIGN_INIT_BEGIN
source $env(PV_ROOT)/scripts/pv.tcl
source ./tcl/design.tcl
global max_threads lef_files netlist_file ground_net power_net init_top_cell def_file
set_options global.infra.max_thread_count $max_threads
set_options setup.lef_file $lef_files
set_options setup.verilog $netlist_file
set_options setup.ground_net $ground_net
set_options setup.power_net $power_net
set_options setup.mmmc_file ./tcl/optimus/mmmc.tcl
set_options setup.top_cell $init_top_cell
setup_design
read_def $def_file
# DESIGN_INIT_END

file mkdir ./out

# EXPECT: PASS
# TEST_ACTION
add_special_wire -layer M2 -net test_net -shape NONE -status ROUTED -rect {10.0 10.0 20.0 10.2}
add_special_wire -layer M2 -net test_net -shape RING -status FIXED -rect {10.0 11.0 20.0 11.2}
add_special_wire -layer M2 -net test_net -shape STRIPE -status COVER -rect {10.0 12.0 20.0 12.2}
add_special_wire -layer M2 -net test_net -shape FOLLOWPIN -status NOSHIELD -rect {10.0 13.0 20.0 13.2}
add_special_wire -layer M2 -net test_net -shape IOWIRE -status ROUTED -rect {10.0 14.0 20.0 14.2}
add_special_wire -layer M2 -net test_net -shape COREWIRE -status FIXED -rect {10.0 15.0 20.0 15.2}
add_special_wire -layer M2 -net test_net -shape BLOCKWIRE -status COVER -rect {10.0 16.0 20.0 16.2}
add_special_wire -layer M2 -net test_net -shape FILLWIRE -status NOSHIELD -rect {10.0 17.0 20.0 17.2}
add_special_wire -layer M2 -net test_net -shape BLOCKAGEWIRE -status ROUTED -rect {10.0 18.0 20.0 18.2}
add_special_wire -layer M2 -net test_net -shape PADRING -status FIXED -rect {10.0 19.0 20.0 19.2}
add_special_wire -layer M2 -net test_net -shape BLOCKRING -status COVER -rect {10.0 20.0 20.0 20.2}
add_special_wire -layer M2 -net test_net -shape DRCFILL -status NOSHIELD \
    -polygon {10.0 21.0 20.0 21.0 20.0 21.2 10.0 21.2}
add_special_wire -layer M2 -net test_net -shape FILLWIREOPC -status ROUTED \
    -path_segment {10.0 22.0 20.0 22.0} -width 0.2 \
    -begin_extension 0.1 -end_extension 0.1

set actual_def ./out/add_special_wire.def
file delete -force $actual_def
write_def $actual_def
pv_check_golden $actual_def -golden ./golden/add_special_wire.def
pv_rpt_checkpoints
exit
