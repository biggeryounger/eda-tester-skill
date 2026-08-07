# EXPECT: PASS
# TEST_ACTION
set result [list sample_command -name {net_1}]
if {[llength $result] == 0} {
    error "sample command was not constructed"
}

