# Design identity and canonical input roots.
set design_name c906_hm
set tech_name TSMC40
set init_top_name openC906
set init_top_cell $init_top_name
set design_dir "$env(PV_ROOT)/svn/openedi/design_data/TSMC40/Itools21.1_Ifp_util0.65/$design_name"
set tech_dir "$env(PV_ROOT)/svn/openedi/design_data/TSMC40/tsmc40_library"

set power_net VDD
set ground_net VSS

set lef_files [list \
    $tech_dir/tcbn40lpbwp_8lm5X2ZRDL_WITH_NDR.lef \
    $tech_dir/tune_lef/spsram_1024x16_tsmc40.lef \
    $tech_dir/tune_lef/spsram_128x42_tsmc40.lef \
    $tech_dir/tune_lef/spsram_256x41_tsmc40.lef \
    $tech_dir/tune_lef/spsram_512x16_tsmc40.lef \
    $tech_dir/tune_lef/spsram_64x4_tsmc40.lef \
    $tech_dir/tune_lef/spsram_1024x32_tsmc40.lef \
    $tech_dir/tune_lef/spsram_128x43_tsmc40.lef \
    $tech_dir/tune_lef/spsram_256x4_tsmc40.lef \
    $tech_dir/tune_lef/spsram_512x32_tsmc40.lef \
    $tech_dir/tune_lef/spsram_64x58_tsmc40.lef \
    $tech_dir/tune_lef/spsram_1024x36_tsmc40.lef \
    $tech_dir/tune_lef/spsram_128x4_tsmc40.lef \
    $tech_dir/tune_lef/spsram_256x59_tsmc40.lef \
    $tech_dir/tune_lef/spsram_512x38_tsmc40.lef \
    $tech_dir/tune_lef/spsram_64x88_tsmc40.lef \
    $tech_dir/tune_lef/spsram_1024x37_tsmc40.lef \
    $tech_dir/tune_lef/spsram_128x8_tsmc40.lef \
    $tech_dir/tune_lef/spsram_32x46_tsmc40.lef \
    $tech_dir/tune_lef/spsram_512x39_tsmc40.lef \
    $tech_dir/tune_lef/spsram_64x98_tsmc40.lef \
    $tech_dir/tune_lef/spsram_1024x4_tsmc40.lef \
    $tech_dir/tune_lef/spsram_2048x32_tsmc40.lef \
    $tech_dir/tune_lef/spsram_32x47_tsmc40.lef \
    $tech_dir/tune_lef/spsram_512x4_tsmc40.lef \
    $tech_dir/tune_lef/spsram_8192x32_tsmc40.lef \
    $tech_dir/tune_lef/spsram_1024x64_tsmc40.lef \
    $tech_dir/tune_lef/spsram_256x32_tsmc40.lef \
    $tech_dir/tune_lef/spsram_32x4_tsmc40.lef \
    $tech_dir/tune_lef/spsram_64x44_tsmc40.lef \
    $tech_dir/tune_lef/spsram_128x32_tsmc40.lef \
    $tech_dir/tune_lef/spsram_256x40_tsmc40.lef \
    $tech_dir/tune_lef/spsram_4096x32_tsmc40.lef \
    $tech_dir/tune_lef/spsram_64x45_tsmc40.lef]
set slowlib_liberty_files [list \
    $tech_dir/tcbn40lpbwpwc_ccs.lib \
    $tech_dir/tune_lib/spsram_1024x16_tsmc40.lib \
    $tech_dir/tune_lib/spsram_128x8_tsmc40.lib \
    $tech_dir/tune_lib/spsram_256x41_tsmc40.lib \
    $tech_dir/tune_lib/spsram_512x16_tsmc40.lib \
    $tech_dir/tune_lib/spsram_64x98_tsmc40.lib \
    $tech_dir/tune_lib/spsram_1024x32_tsmc40.lib \
    $tech_dir/tune_lib/spsram_2048x32_tsmc40.lib \
    $tech_dir/tune_lib/spsram_256x4_tsmc40.lib \
    $tech_dir/tune_lib/spsram_64x58_tsmc40.lib \
    $tech_dir/tune_lib/spsram_1024x64_tsmc40.lib \
    $tech_dir/tune_lib/spsram_256x40_tsmc40.lib \
    $tech_dir/tune_lib/spsram_256x59_tsmc40.lib \
    $tech_dir/tune_lib/spsram_64x88_tsmc40.lib]
set fastlib_liberty_files [list \
    $tech_dir/tcbn40lpbwpbc_ccs.lib \
    $tech_dir/tune_lib/spsram_1024x16_tsmc40.lib \
    $tech_dir/tune_lib/spsram_128x8_tsmc40.lib \
    $tech_dir/tune_lib/spsram_256x41_tsmc40.lib \
    $tech_dir/tune_lib/spsram_512x16_tsmc40.lib \
    $tech_dir/tune_lib/spsram_64x98_tsmc40.lib \
    $tech_dir/tune_lib/spsram_1024x32_tsmc40.lib \
    $tech_dir/tune_lib/spsram_2048x32_tsmc40.lib \
    $tech_dir/tune_lib/spsram_256x4_tsmc40.lib \
    $tech_dir/tune_lib/spsram_64x58_tsmc40.lib \
    $tech_dir/tune_lib/spsram_1024x64_tsmc40.lib \
    $tech_dir/tune_lib/spsram_256x40_tsmc40.lib \
    $tech_dir/tune_lib/spsram_256x59_tsmc40.lib \
    $tech_dir/tune_lib/spsram_64x88_tsmc40.lib]
set liberty_files [concat $slowlib_liberty_files $fastlib_liberty_files]

set verilog_files [list $design_dir/route.v.gz]
set def_file $design_dir/route.def.gz
set sdc_files [list $design_dir/route.sdc]
set utilization 0.65
set clocks {CPU_CLK SYS_APB_CLK}
set period {3.5 7}
set scan_chain_flag 1
