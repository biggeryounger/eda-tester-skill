# Design identity and canonical input roots.
if ![info exists util] { set util "util0.65" }

set design_name   riscv_core
set tech_name     SMIC28
set init_top_name riscv_core
set design_dir "$env(PV_ROOT)/svn/openedi/design_data/SMIC28/Itools21.1_Ifp_${util}/$design_name"
set tech_dir   "$env(PV_ROOT)/svn/openedi/design_data/SMIC28/smic28_library"

set power_net  VDD
set ground_net VSS

set lef_files [list \
    $tech_dir/scc28n_12t25od33_1p8m_7ic_1tmc_alpa1_WITH_NDR.lef \
    $tech_dir/scc28nhkcp_hsc30p140_rvt_ant.lef]
set cworst_liberty_files [list \
    $tech_dir/scc28nhkcp_hsc30p140_rvt_ss_v0p9_125c_ccs.lib]
set rcworst_liberty_files [list \
    $tech_dir/scc28nhkcp_hsc30p140_rvt_ss_v0p9_-40c_ccs.lib]
set cbest_liberty_files [list \
    $tech_dir/scc28nhkcp_hsc30p140_rvt_ff_v1p05_125c_ccs.lib]
set rcbest_liberty_files [list \
    $tech_dir/scc28nhkcp_hsc30p140_rvt_ff_v1p05_-40c_ccs.lib]
set liberty_files [concat $cworst_liberty_files $rcworst_liberty_files $cbest_liberty_files $rcbest_liberty_files]

switch -- $PV_TOOL {
    optimus {
    set cworst_rc_tech_file  $tech_dir/hsc30p140_rvt_ss_v0p9_125c.enTech
    set rcworst_rc_tech_file $tech_dir/hsc30p140_rvt_ss_v0p9_-40c.enTech
    set cbest_rc_tech_file   $tech_dir/hsc30p140_rvt_ff_v1p05_125c.enTech
    set rcbest_rc_tech_file  $tech_dir/hsc30p140_rvt_ff_v1p05_-40c.enTech
    }
    itools {
    set cworst_rc_tech_file  $tech_dir/hsc30p140_rvt_ss_v0p9_125c.qrcTech
    set rcworst_rc_tech_file $tech_dir/hsc30p140_rvt_ss_v0p9_-40c.qrcTech
    set cbest_rc_tech_file   $tech_dir/hsc30p140_rvt_ff_v1p05_125c.qrcTech
    set rcbest_rc_tech_file  $tech_dir/hsc30p140_rvt_ff_v1p05_-40c.qrcTech
    }
    default { error "Unsupported PV_TOOL: $PV_TOOL" }
}
set rc_tech_file $rcworst_rc_tech_file

# prepared input files in stage of floorplan, place, prects, postcts
if ![info exists stage] { set stage "floorplan" }

set verilog_files [list $design_dir/$stage.v.gz]
#set def_file      $design_dir/$stage.def.gz
set sdc_files     [list $design_dir/$stage.sdc]

if ![info exists mmmc_file] { set mmmc_file "mmmc.tcl" }
if ![info exists def_file] { set def_file "$design_dir/$stage.def.gz" }
set_options setup.power_net $power_net
set_options setup.ground_net $ground_net
set_options setup.lef_file $lef_files
set_options setup.verilog $verilog_files
set_options setup.mmmc_file $mmmc_file
set_options setup.top_cell $init_top_name
setup_design
read_def $def_file

set clk_lib_cells [get_lib_cells *CLK*]
set clk_buffer_cells {CLKBUFV4_140P9T30R CLKBUFV6_140P9T30R CLKBUFV8_140P9T30R CLKBUFV10_140P9T30R CLKBUFV12_140P9T30R}
