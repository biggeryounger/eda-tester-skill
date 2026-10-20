# Design identity and canonical input roots.
set design_name   e906_hm
set tech_name     SMIC180
set init_top_name openE906
set design_dir "$env(PV_ROOT)/svn/openedi/design_data/SMIC180/Itools21.1_Ifp_util0.65/$design_name"
set tech_dir   "$env(PV_ROOT)/svn/openedi/large/SMIC180_new/smic180_library"

set power_net  VDD
set ground_net GND

set lef_files [list \
    $tech_dir/smic18_6lm_antRuleWA.lef \
    $tech_dir/mem_lib_lef/spsram_1024x32.lef \
    $tech_dir/mem_lib_lef/spsram_1024x36.lef \
    $tech_dir/mem_lib_lef/spsram_1024x37.lef \
    $tech_dir/mem_lib_lef/spsram_1024x4.lef \
    $tech_dir/mem_lib_lef/spsram_128x32.lef \
    $tech_dir/mem_lib_lef/spsram_128x42.lef \
    $tech_dir/mem_lib_lef/spsram_128x43.lef \
    $tech_dir/mem_lib_lef/spsram_128x4.lef \
    $tech_dir/mem_lib_lef/spsram_2048x32.lef \
    $tech_dir/mem_lib_lef/spsram_256x32.lef \
    $tech_dir/mem_lib_lef/spsram_256x40.lef \
    $tech_dir/mem_lib_lef/spsram_256x41.lef \
    $tech_dir/mem_lib_lef/spsram_256x4.lef \
    $tech_dir/mem_lib_lef/spsram_32x46.lef \
    $tech_dir/mem_lib_lef/spsram_32x47.lef \
    $tech_dir/mem_lib_lef/spsram_32x4.lef \
    $tech_dir/mem_lib_lef/spsram_4096x32.lef \
    $tech_dir/mem_lib_lef/spsram_512x16.lef \
    $tech_dir/mem_lib_lef/spsram_512x32.lef \
    $tech_dir/mem_lib_lef/spsram_512x38.lef \
    $tech_dir/mem_lib_lef/spsram_512x39.lef \
    $tech_dir/mem_lib_lef/spsram_512x4.lef \
    $tech_dir/mem_lib_lef/spsram_64x44.lef \
    $tech_dir/mem_lib_lef/spsram_64x45.lef \
    $tech_dir/mem_lib_lef/spsram_64x4.lef \
    $tech_dir/mem_lib_lef/spsram_8192x32.lef]
set slow_liberty_files [list \
    $tech_dir/slow.lib \
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
set fast_liberty_files [list \
    $tech_dir/fast.lib \
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
set liberty_files [concat $slow_liberty_files $fast_liberty_files]

set verilog_files [list $design_dir/place.v.gz]
set def_file      $design_dir/place.def.gz
set sdc_files     [list $design_dir/place.sdc]
