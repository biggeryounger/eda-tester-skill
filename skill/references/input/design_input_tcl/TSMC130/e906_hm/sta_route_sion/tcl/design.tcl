# Design identity and canonical input roots.
set design_name e906_hm
set tech_name TSMC130
set init_top_name openE906
set init_top_cell $init_top_name
set design_dir "$env(PV_ROOT)/svn/openedi/design_data/TSMC130/Itools21.1_Ifp_util0.65/$design_name"
set tech_dir "$env(PV_ROOT)/svn/openedi/design_data/TSMC130/tsmc130_library"

set power_net VDD
set ground_net VSS

set lef_files [list \
    $tech_dir/tcb013bcd_Fsg_6lm_5.7_WITH_NDR.lef \
    $tech_dir/tune_lef/spsram_1024x16_tsmc130.lef \
    $tech_dir/tune_lef/spsram_128x42_tsmc130.lef \
    $tech_dir/tune_lef/spsram_256x41_tsmc130.lef \
    $tech_dir/tune_lef/spsram_512x16_tsmc130.lef \
    $tech_dir/tune_lef/spsram_64x4_tsmc130.lef \
    $tech_dir/tune_lef/spsram_1024x32_tsmc130.lef \
    $tech_dir/tune_lef/spsram_128x43_tsmc130.lef \
    $tech_dir/tune_lef/spsram_256x4_tsmc130.lef \
    $tech_dir/tune_lef/spsram_512x32_tsmc130.lef \
    $tech_dir/tune_lef/spsram_64x58_tsmc130.lef \
    $tech_dir/tune_lef/spsram_1024x36_tsmc130.lef \
    $tech_dir/tune_lef/spsram_128x4_tsmc130.lef \
    $tech_dir/tune_lef/spsram_256x59_tsmc130.lef \
    $tech_dir/tune_lef/spsram_512x38_tsmc130.lef \
    $tech_dir/tune_lef/spsram_64x88_tsmc130.lef \
    $tech_dir/tune_lef/spsram_1024x37_tsmc130.lef \
    $tech_dir/tune_lef/spsram_128x8_tsmc130.lef \
    $tech_dir/tune_lef/spsram_32x46_tsmc130.lef \
    $tech_dir/tune_lef/spsram_512x39_tsmc130.lef \
    $tech_dir/tune_lef/spsram_64x98_tsmc130.lef \
    $tech_dir/tune_lef/spsram_1024x4_tsmc130.lef \
    $tech_dir/tune_lef/spsram_2048x32_tsmc130.lef \
    $tech_dir/tune_lef/spsram_32x47_tsmc130.lef \
    $tech_dir/tune_lef/spsram_512x4_tsmc130.lef \
    $tech_dir/tune_lef/spsram_8192x32_tsmc130.lef \
    $tech_dir/tune_lef/spsram_1024x64_tsmc130.lef \
    $tech_dir/tune_lef/spsram_256x32_tsmc130.lef \
    $tech_dir/tune_lef/spsram_32x4_tsmc130.lef \
    $tech_dir/tune_lef/spsram_64x44_tsmc130.lef \
    $tech_dir/tune_lef/spsram_128x32_tsmc130.lef \
    $tech_dir/tune_lef/spsram_256x40_tsmc130.lef \
    $tech_dir/tune_lef/spsram_4096x32_tsmc130.lef \
    $tech_dir/tune_lef/spsram_64x45_tsmc130.lef]
set fastlibset_liberty_files [list \
    $tech_dir/tcb013bcdbc_ccs.lib \
    $tech_dir/mem_lib_lef/spsram_1024x32_ff_1.98_-40.lib \
    $tech_dir/mem_lib_lef/spsram_1024x36_ff_1.98_-40.lib \
    $tech_dir/mem_lib_lef/spsram_1024x37_ff_1.98_-40.lib \
    $tech_dir/mem_lib_lef/spsram_1024x4_ff_1.98_-40.lib \
    $tech_dir/mem_lib_lef/spsram_128x32_ff_1.98_-40.lib \
    $tech_dir/mem_lib_lef/spsram_128x42_ff_1.98_-40.lib \
    $tech_dir/mem_lib_lef/spsram_128x43_ff_1.98_-40.lib \
    $tech_dir/mem_lib_lef/spsram_128x4_ff_1.98_-40.lib \
    $tech_dir/mem_lib_lef/spsram_2048x32_ff_1.98_-40.lib \
    $tech_dir/mem_lib_lef/spsram_256x32_ff_1.98_-40.lib \
    $tech_dir/mem_lib_lef/spsram_256x40_ff_1.98_-40.lib \
    $tech_dir/mem_lib_lef/spsram_256x41_ff_1.98_-40.lib \
    $tech_dir/mem_lib_lef/spsram_256x4_ff_1.98_-40.lib \
    $tech_dir/mem_lib_lef/spsram_32x46_ff_1.98_-40.lib \
    $tech_dir/mem_lib_lef/spsram_32x47_ff_1.98_-40.lib \
    $tech_dir/mem_lib_lef/spsram_32x4_ff_1.98_-40.lib \
    $tech_dir/mem_lib_lef/spsram_4096x32_ff_1.98_-40.lib \
    $tech_dir/mem_lib_lef/spsram_512x16_ff_1.98_-40.lib \
    $tech_dir/mem_lib_lef/spsram_512x32_ff_1.98_-40.lib \
    $tech_dir/mem_lib_lef/spsram_512x38_ff_1.98_-40.lib \
    $tech_dir/mem_lib_lef/spsram_512x39_ff_1.98_-40.lib \
    $tech_dir/mem_lib_lef/spsram_512x4_ff_1.98_-40.lib \
    $tech_dir/mem_lib_lef/spsram_64x44_ff_1.98_-40.lib \
    $tech_dir/mem_lib_lef/spsram_64x45_ff_1.98_-40.lib \
    $tech_dir/mem_lib_lef/spsram_64x4_ff_1.98_-40.lib \
    $tech_dir/mem_lib_lef/spsram_8192x32_ff_1.98_-40.lib]
set slowlibset_liberty_files [list \
    $tech_dir/tcb013bcdwc_ccs.lib \
    $tech_dir/mem_lib_lef/spsram_1024x32_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_1024x36_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_1024x37_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_1024x4_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_128x32_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_128x42_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_128x43_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_128x4_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_2048x32_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_256x32_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_256x40_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_256x41_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_256x4_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_32x46_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_32x47_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_32x4_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_4096x32_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_512x16_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_512x32_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_512x38_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_512x39_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_512x4_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_64x44_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_64x45_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_64x4_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_8192x32_ss_1.62_125.lib]
set liberty_files [concat $fastlibset_liberty_files $slowlibset_liberty_files]

set verilog_files [list $design_dir/route.v.gz]
set def_file $design_dir/route.def.gz
set sdc_files [list $design_dir/route.sdc]
set utilization 0.65
set clocks {CPU_CLOCK}
set period {5}
set scan_chain_flag 1
