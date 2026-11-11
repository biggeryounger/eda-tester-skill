
source ./tcl/design.tcl
source $env(PV_ROOT)/scripts/pv.tcl

if {$PV_TOOL == "itools"} {
    set db "./cr_clic_arb_kernel_PRIO_WIDTH4_INT_NUM80.enc.dat"
}
if {$PV_TOOL == "optimus"} {
    set db "./output/cr_clic_arb_kernel_PRIO_WIDTH4_INT_NUM80"
}

read_db $db cr_clic_arb_kernel_PRIO_WIDTH4_INT_NUM80

exit
