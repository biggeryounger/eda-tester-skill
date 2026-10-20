# Design identity and canonical input roots.
set design_name   c906_hm
set tech_name     TSMC130
set design_dir "$env(PV_ROOT)/svn/openedi/design_data/TSMC130/Itools21.1_Ifp_util0.65/$design_name"
set tech_dir   "$env(PV_ROOT)/svn/openedi/design_data/TSMC130/tsmc130_library"

# top design name (itools default var)
set init_top_name openC906
set init_top_cell $init_top_name
# design common setting
set utilization 0.65
set clocks {CPU_CLK SYS_APB_CLK}
# for fm LEC
set scan_chain_flag 1
set period {5 8}
set lef_files [list $tech_dir/tcb013bcd_Fsg_6lm_5.7_WITH_NDR.lef  $tech_dir/tune_lef/spsram_1024x16_tsmc130.lef  $tech_dir/tune_lef/spsram_128x42_tsmc130.lef   $tech_dir/tune_lef/spsram_256x41_tsmc130.lef   $tech_dir/tune_lef/spsram_512x16_tsmc130.lef  $tech_dir/tune_lef/spsram_64x4_tsmc130.lef  $tech_dir/tune_lef/spsram_1024x32_tsmc130.lef  $tech_dir/tune_lef/spsram_128x43_tsmc130.lef   $tech_dir/tune_lef/spsram_256x4_tsmc130.lef    $tech_dir/tune_lef/spsram_512x32_tsmc130.lef  $tech_dir/tune_lef/spsram_64x58_tsmc130.lef  $tech_dir/tune_lef/spsram_1024x36_tsmc130.lef  $tech_dir/tune_lef/spsram_128x4_tsmc130.lef    $tech_dir/tune_lef/spsram_256x59_tsmc130.lef   $tech_dir/tune_lef/spsram_512x38_tsmc130.lef  $tech_dir/tune_lef/spsram_64x88_tsmc130.lef  $tech_dir/tune_lef/spsram_1024x37_tsmc130.lef  $tech_dir/tune_lef/spsram_128x8_tsmc130.lef    $tech_dir/tune_lef/spsram_32x46_tsmc130.lef    $tech_dir/tune_lef/spsram_512x39_tsmc130.lef  $tech_dir/tune_lef/spsram_64x98_tsmc130.lef  $tech_dir/tune_lef/spsram_1024x4_tsmc130.lef   $tech_dir/tune_lef/spsram_2048x32_tsmc130.lef  $tech_dir/tune_lef/spsram_32x47_tsmc130.lef    $tech_dir/tune_lef/spsram_512x4_tsmc130.lef   $tech_dir/tune_lef/spsram_8192x32_tsmc130.lef  $tech_dir/tune_lef/spsram_1024x64_tsmc130.lef  $tech_dir/tune_lef/spsram_256x32_tsmc130.lef   $tech_dir/tune_lef/spsram_32x4_tsmc130.lef     $tech_dir/tune_lef/spsram_64x44_tsmc130.lef  $tech_dir/tune_lef/spsram_128x32_tsmc130.lef   $tech_dir/tune_lef/spsram_256x40_tsmc130.lef   $tech_dir/tune_lef/spsram_4096x32_tsmc130.lef  $tech_dir/tune_lef/spsram_64x45_tsmc130.lef]
set fast_liberty_files [list $tech_dir/tcb013bcdbc_ccs.lib \
    $tech_dir/mem_lib_lef/spsram_1024x16_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_1024x64_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_128x8_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_2048x32_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_256x59_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_64x58_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_64x88_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_64x98_ss_1.62_125.lib]
set fast_db [list $tech_dir/tcb013bcdbc_ccs.db \
    $tech_dir/mem_lib_lef/spsram_1024x16_ff_1.98_-40.db \
    $tech_dir/mem_lib_lef/spsram_1024x64_ff_1.98_-40.db \
    $tech_dir/mem_lib_lef/spsram_128x8_ff_1.98_-40.db \
    $tech_dir/mem_lib_lef/spsram_2048x32_ff_1.98_-40.db \
    $tech_dir/mem_lib_lef/spsram_256x59_ff_1.98_-40.db \
    $tech_dir/mem_lib_lef/spsram_64x58_ff_1.98_-40.db \
    $tech_dir/mem_lib_lef/spsram_64x88_ff_1.98_-40.db \
    $tech_dir/mem_lib_lef/spsram_64x98_ff_1.98_-40.db]
set slow_liberty_files [list $tech_dir/tcb013bcdwc_ccs.lib \
    $tech_dir/mem_lib_lef/spsram_1024x16_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_1024x64_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_128x8_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_2048x32_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_256x59_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_64x58_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_64x88_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_64x98_ss_1.62_125.lib]
set slow_db [list $tech_dir/tcb013bcdwc_ccs.db \
    $tech_dir/mem_lib_lef/spsram_1024x16_ss_1.62_125.db \
    $tech_dir/mem_lib_lef/spsram_1024x64_ss_1.62_125.db \
    $tech_dir/mem_lib_lef/spsram_128x8_ss_1.62_125.db \
    $tech_dir/mem_lib_lef/spsram_2048x32_ss_1.62_125.db \
    $tech_dir/mem_lib_lef/spsram_256x59_ss_1.62_125.db \
    $tech_dir/mem_lib_lef/spsram_64x58_ss_1.62_125.db \
    $tech_dir/mem_lib_lef/spsram_64x88_ss_1.62_125.db \
    $tech_dir/mem_lib_lef/spsram_64x98_ss_1.62_125.db]

# Stage inputs.
set power_net    VDD
set ground_net   GND
set verilog_files [list $design_dir/floorplan.v.gz]
set def_file     $design_dir/floorplan.def.gz
set sdc_files    [list $design_dir/floorplan.sdc]
