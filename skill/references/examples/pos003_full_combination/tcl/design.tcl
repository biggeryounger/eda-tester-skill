set tech_dir "$env(PV_ROOT)/svn/openedi/large/SMIC180/smic180_library"
set idb_achive "$env(PV_ROOT)/svn/openedi/small/RV32Core_180"
set lef_files $tech_dir/smic18_6lm_0202_ndr.lef
set slow_lib [list $tech_dir/slow.lib]
set fast_lib [list $tech_dir/fast.lib]
set netlist ./design/demo/s180_max_time_borrow.v

set sdc_file {design/hier_example/sdc/sta.sdc}

set itools_mmmc_file {./tcl/itools/mmmc.tcl}

set optimus_mmmc_file {./tcl/optimus/mmmc.tcl}
set top_name top