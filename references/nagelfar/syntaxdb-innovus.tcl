# Nagelfar 1.3.5 syntax database additions for Innovus/iTools commands.
# Keep command names and options aligned with the checked-in command corpus.
lappend ::dbInfo {EDA Tester Skill Innovus/iTools command additions 1.0}

set ::syntax(add_net) {o*}
set ::option(add_net) {-help -bus -ground -power -module -name}
set {::option(add_net -bus)} x
set {::option(add_net -module)} x
set {::option(add_net -name)} x

set ::syntax(report_qor) {o*}
set ::option(report_qor) {
    -help -prefix -pre_place -place -place_opt -cts -cts_opt -route -route_opt
    -view -type
}
set {::option(report_qor -view)} x
set {::option(report_qor -type)} x

# Frequently used setup helpers are intentionally permissive. They are registered
# so generated standalone cases can be checked without hiding option errors on the
# commands under test above.
set ::syntax(read_db) {x+}
set ::syntax(read_mmmc) {x+}
set ::syntax(read_physical) {x+}
set ::syntax(read_netlist) {x+}
set ::syntax(init_design) {x*}
set ::syntax(exit) {x?}

# Project checkpoint commands used by standalone generated tests.
set ::syntax(pv_check_log) {x p*}
set ::option(pv_check_log) {-name -filter -log_files}
set ::syntax(pv_check_golden) {x p*}
set ::option(pv_check_golden) {-golden -filter}
set ::syntax(pv_check_qor) {x p*}
set ::option(pv_check_qor) {-name -golden -tolerance -rel_tolerance -dir}
