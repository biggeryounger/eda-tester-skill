# EXPECT: FAIL
# TEST_ACTION
set required_name ""
if {$required_name eq ""} {
    error "missing required option: -name"
}

