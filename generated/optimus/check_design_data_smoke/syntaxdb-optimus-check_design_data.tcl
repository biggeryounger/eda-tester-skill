# Nagelfar 1.3.5 additions derived only from the supplied Optimus help screenshot.
lappend ::dbInfo {Optimus check_design_data smoke syntax 1.0}

set ::syntax(check_design_data) {o*}
set ::option(check_design_data) {-file -netlist}
set {::option(check_design_data -file)} x

# The checkpoint implementation belongs to the configured regression environment.
set ::syntax(pv_check_log) {x x*}
