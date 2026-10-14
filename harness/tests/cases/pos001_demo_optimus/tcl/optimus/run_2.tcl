source ./tcl/case_setup.tcl
source $env(PV_ROOT)/scripts/pv.tcl
if {$PV_TOOL=="itools"} {
    set db_file "./obs.dat"
} else {
    set db_file "./obs"
}
read_db $db_file top
pv_check_golden obs_after_read_db.lef -golden golden/$PV_TOOL.obs.lef -filter {#}
pv_check_log {write_lef obs_after_read_db.lef} -name check_write_lef -filter {"date"|"^#"} -match {ID-0001|ID-0002}
pv_rpt_checkpoints
exit