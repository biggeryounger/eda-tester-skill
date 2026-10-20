# Design identity and canonical input roots.
set design_name c906_hm
set tech_name SMIC28
set init_top_name openC906
set init_top_cell $init_top_name
set design_dir "$env(PV_ROOT)/svn/openedi/design_data/SMIC28/Itools21.1_Ifp_util0.65/$design_name"
set tech_dir "$env(PV_ROOT)/svn/openedi/design_data/SMIC28/smic28_library"

set power_net VDD
set ground_net VSS

set lef_files [list \
    $tech_dir/scc28n_12t25od33_1p8m_7ic_1tmc_alpa1_WITH_NDR.lef \
    $tech_dir/scc28nhkcp_hsc30p140_rvt_ant.lef \
    $tech_dir/tune_lef/spsram_1024x16_small.lef \
    $tech_dir/tune_lef/spsram_1024x64_small.lef \
    $tech_dir/tune_lef/spsram_128x8_small.lef \
    $tech_dir/tune_lef/spsram_2048x32_small.lef \
    $tech_dir/tune_lef/spsram_256x59_small.lef \
    $tech_dir/tune_lef/spsram_64x58_small.lef \
    $tech_dir/tune_lef/spsram_64x88_small.lef \
    $tech_dir/tune_lef/spsram_64x98_small.lef]
set slowlibset_40c_liberty_files [list \
    $tech_dir/scc28nhkcp_hsc30p140_rvt_ss_v0p9_-40c_ccs.lib \
    $tech_dir/tune_lib/spsram_1024x16.lib \
    $tech_dir/tune_lib/spsram_1024x64.lib \
    $tech_dir/tune_lib/spsram_128x8.lib \
    $tech_dir/tune_lib/spsram_2048x32.lib \
    $tech_dir/tune_lib/spsram_256x59.lib \
    $tech_dir/tune_lib/spsram_64x58.lib \
    $tech_dir/tune_lib/spsram_64x88.lib \
    $tech_dir/tune_lib/spsram_64x98.lib]
set fastlibset_40c_liberty_files [list \
    $tech_dir/scc28nhkcp_hsc30p140_rvt_ff_v1p05_-40c_ccs.lib \
    $tech_dir/tune_lib/spsram_1024x16.lib \
    $tech_dir/tune_lib/spsram_1024x64.lib \
    $tech_dir/tune_lib/spsram_128x8.lib \
    $tech_dir/tune_lib/spsram_2048x32.lib \
    $tech_dir/tune_lib/spsram_256x59.lib \
    $tech_dir/tune_lib/spsram_64x58.lib \
    $tech_dir/tune_lib/spsram_64x88.lib \
    $tech_dir/tune_lib/spsram_64x98.lib]
set slowlibset_125c_liberty_files [list \
    $tech_dir/scc28nhkcp_hsc30p140_rvt_ss_v0p9_125c_ccs.lib \
    $tech_dir/tune_lib/spsram_1024x16.lib \
    $tech_dir/tune_lib/spsram_1024x64.lib \
    $tech_dir/tune_lib/spsram_128x8.lib \
    $tech_dir/tune_lib/spsram_2048x32.lib \
    $tech_dir/tune_lib/spsram_256x59.lib \
    $tech_dir/tune_lib/spsram_64x58.lib \
    $tech_dir/tune_lib/spsram_64x88.lib \
    $tech_dir/tune_lib/spsram_64x98.lib]
set fastlibset_125c_liberty_files [list \
    $tech_dir/scc28nhkcp_hsc30p140_rvt_ff_v1p05_125c_ccs.lib \
    $tech_dir/tune_lib/spsram_1024x16.lib \
    $tech_dir/tune_lib/spsram_1024x64.lib \
    $tech_dir/tune_lib/spsram_128x8.lib \
    $tech_dir/tune_lib/spsram_2048x32.lib \
    $tech_dir/tune_lib/spsram_256x59.lib \
    $tech_dir/tune_lib/spsram_64x58.lib \
    $tech_dir/tune_lib/spsram_64x88.lib \
    $tech_dir/tune_lib/spsram_64x98.lib]
set liberty_files [concat $slowlibset_40c_liberty_files $fastlibset_40c_liberty_files $slowlibset_125c_liberty_files $fastlibset_125c_liberty_files]

set verilog_files [list $design_dir/route.v.gz]
set def_file $design_dir/route.def.gz
set sdc_files [list $design_dir/route.sdc]
set utilization 0.65
set clocks {CPU_CLK SYS_APB_CLK}
set period {6 13}
set scan_chain_flag 1
