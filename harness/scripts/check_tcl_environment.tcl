if {[package vcompare [info patchlevel] 8.6] < 0} {
    puts stderr "Tcl 8.6+ is required; found [info patchlevel]"
    exit 1
}
puts "Tcl [info patchlevel]"
