# Design identity and canonical input roots.
set design_name   c906_hm
set tech_name     SMIC180
set init_top_name openC906
set design_dir "$env(PV_ROOT)/svn/openedi/design_data/SMIC180/Itools21.1_Ifp_util0.65/$design_name"
set tech_dir   "$env(PV_ROOT)/svn/openedi/large/SMIC180_new/smic180_library"

set power_net  VDD
set ground_net GND

set lef_files [list \
    $tech_dir/smic18_6lm_antRuleWA.lef \
    $tech_dir/mem_lib_lef/spsram_1024x16.lef \
    $tech_dir/mem_lib_lef/spsram_1024x64.lef \
    $tech_dir/mem_lib_lef/spsram_128x8.lef \
    $tech_dir/mem_lib_lef/spsram_2048x32.lef \
    $tech_dir/mem_lib_lef/spsram_256x59.lef \
    $tech_dir/mem_lib_lef/spsram_64x58.lef \
    $tech_dir/mem_lib_lef/spsram_64x88.lef \
    $tech_dir/mem_lib_lef/spsram_64x98.lef]
set slow_liberty_files [list \
    $tech_dir/slow.lib \
    $tech_dir/mem_lib_lef/spsram_1024x16_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_1024x64_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_128x8_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_2048x32_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_256x59_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_64x58_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_64x88_ss_1.62_125.lib \
    $tech_dir/mem_lib_lef/spsram_64x98_ss_1.62_125.lib]
set fast_liberty_files [list \
    $tech_dir/fast.lib \
    $tech_dir/mem_lib_lef/spsram_1024x16_ff_1.98_-40.lib \
    $tech_dir/mem_lib_lef/spsram_1024x64_ff_1.98_-40.lib \
    $tech_dir/mem_lib_lef/spsram_128x8_ff_1.98_-40.lib \
    $tech_dir/mem_lib_lef/spsram_2048x32_ff_1.98_-40.lib \
    $tech_dir/mem_lib_lef/spsram_256x59_ff_1.98_-40.lib \
    $tech_dir/mem_lib_lef/spsram_64x58_ff_1.98_-40.lib \
    $tech_dir/mem_lib_lef/spsram_64x88_ff_1.98_-40.lib \
    $tech_dir/mem_lib_lef/spsram_64x98_ff_1.98_-40.lib]
set liberty_files [concat $slow_liberty_files $fast_liberty_files]

set verilog_files [list $design_dir/place.v.gz]
set def_file      $design_dir/place.def.gz
set sdc_files     [list $design_dir/place.sdc]
