# Print EDA command help from an active Tcl-based tool session.
# Usage:
#   source scripts/dump_tool_help.tcl
#   eda_dump_all_help *
#   eda_dump_all_help report_*
#   eda_dump_command_help {report_qor check_design_data}

set ::eda_help_builtin_commands {
    after append apply array auto_execok auto_import auto_load auto_load_index
    auto_qualify binary break catch cd chan clock close concat continue coroutine
    dict encoding eof error eval exec exit expr fblocked fconfigure fcopy file
    fileevent flush for foreach format gets glob global history if incr info interp
    join lappend lassign lindex linsert list llength lmap load lrange lrepeat lreplace
    lreverse lsearch lset lsort namespace open package pid proc puts pwd read regexp
    regsub rename return scan seek set socket source split string subst switch
    tailcall tell throw time trace try unload unset update uplevel upvar variable
    vwait while yield yieldto zlib
}

proc eda_dump_command_help {commands} {
    set total 0
    set succeeded 0
    set failed 0
    foreach command [lsort -unique $commands] {
        incr total
        puts "===== BEGIN HELP: $command ====="
        if {[llength [info commands $command]] == 0} {
            incr failed
            puts "===== HELP FAILED: $command ====="
            puts "command is not available in the current tool session"
            puts "===== END HELP: $command ====="
            continue
        }
        set code [catch {uplevel #0 [list $command -help]} result]
        if {$code == 0} {
            incr succeeded
            if {$result ne ""} {
                puts $result
            }
        } else {
            incr failed
            puts "===== HELP FAILED: $command ====="
            puts $result
        }
        puts "===== END HELP: $command ====="
    }
    puts "===== SUMMARY total=$total succeeded=$succeeded failed=$failed ====="
    return [list total $total succeeded $succeeded failed $failed]
}

proc eda_dump_all_help {{pattern *}} {
    set commands {}
    foreach command [info commands $pattern] {
        set tail [namespace tail $command]
        if {[lsearch -exact $::eda_help_builtin_commands $tail] >= 0} {
            continue
        }
        if {[string match "eda_dump_*" $tail]} {
            continue
        }
        lappend commands $command
    }
    return [eda_dump_command_help $commands]
}
