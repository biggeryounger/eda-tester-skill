# Design identity and canonical input roots.
set design_name c906_hm
set tech_name TSMC65
set init_top_name openC906
set init_top_cell $init_top_name
set design_dir "$env(PV_ROOT)/svn/openedi/design_data/TSMC65/Itools21.1_Ifp_util0.65/$design_name"
set tech_dir "$env(PV_ROOT)/svn/openedi/design_data/TSMC65/tsmc65_library"

set power_net VDD
set ground_net VSS

set lef_files [list \
    $tech_dir/tcbn65gplus_6lmT1_WITH_NDR.lef \
    $tech_dir/tune_lef/spsram_1024x16_tsmc65.lef \
    $tech_dir/tune_lef/spsram_128x42_tsmc65.lef \
    $tech_dir/tune_lef/spsram_256x41_tsmc65.lef \
    $tech_dir/tune_lef/spsram_512x16_tsmc65.lef \
    $tech_dir/tune_lef/spsram_64x4_tsmc65.lef \
    $tech_dir/tune_lef/spsram_1024x32_tsmc65.lef \
    $tech_dir/tune_lef/spsram_128x43_tsmc65.lef \
    $tech_dir/tune_lef/spsram_256x4_tsmc65.lef \
    $tech_dir/tune_lef/spsram_512x32_tsmc65.lef \
    $tech_dir/tune_lef/spsram_64x58_tsmc65.lef \
    $tech_dir/tune_lef/spsram_1024x36_tsmc65.lef \
    $tech_dir/tune_lef/spsram_128x4_tsmc65.lef \
    $tech_dir/tune_lef/spsram_256x59_tsmc65.lef \
    $tech_dir/tune_lef/spsram_512x38_tsmc65.lef \
    $tech_dir/tune_lef/spsram_64x88_tsmc65.lef \
    $tech_dir/tune_lef/spsram_1024x37_tsmc65.lef \
    $tech_dir/tune_lef/spsram_128x8_tsmc65.lef \
    $tech_dir/tune_lef/spsram_32x46_tsmc65.lef \
    $tech_dir/tune_lef/spsram_512x39_tsmc65.lef \
    $tech_dir/tune_lef/spsram_64x98_tsmc65.lef \
    $tech_dir/tune_lef/spsram_1024x4_tsmc65.lef \
    $tech_dir/tune_lef/spsram_2048x32_tsmc65.lef \
    $tech_dir/tune_lef/spsram_32x47_tsmc65.lef \
    $tech_dir/tune_lef/spsram_512x4_tsmc65.lef \
    $tech_dir/tune_lef/spsram_8192x32_tsmc65.lef \
    $tech_dir/tune_lef/spsram_1024x64_tsmc65.lef \
    $tech_dir/tune_lef/spsram_256x32_tsmc65.lef \
    $tech_dir/tune_lef/spsram_32x4_tsmc65.lef \
    $tech_dir/tune_lef/spsram_64x44_tsmc65.lef \
    $tech_dir/tune_lef/spsram_128x32_tsmc65.lef \
    $tech_dir/tune_lef/spsram_256x40_tsmc65.lef \
    $tech_dir/tune_lef/spsram_4096x32_tsmc65.lef \
    $tech_dir/tune_lef/spsram_64x45_tsmc65.lef]
set fastlibset_liberty_files [list \
    $tech_dir//tcbn65gplusbc_ccs.lib \
    $tech_dir/tune_lib/spsram_1024x16_tsmc65.lib \
    $tech_dir/tune_lib/spsram_128x8_tsmc65.lib \
    $tech_dir/tune_lib/spsram_256x41_tsmc65.lib \
    $tech_dir/tune_lib/spsram_512x16_tsmc65.lib \
    $tech_dir/tune_lib/spsram_64x98_tsmc65.lib \
    $tech_dir/tune_lib/spsram_1024x32_tsmc65.lib \
    $tech_dir/tune_lib/spsram_2048x32_tsmc65.lib \
    $tech_dir/tune_lib/spsram_256x4_tsmc65.lib \
    $tech_dir/tune_lib/spsram_64x58_tsmc65.lib \
    $tech_dir/tune_lib/spsram_1024x64_tsmc65.lib \
    $tech_dir/tune_lib/spsram_256x40_tsmc65.lib \
    $tech_dir/tune_lib/spsram_256x59_tsmc65.lib \
    $tech_dir/tune_lib/spsram_64x88_tsmc65.lib]
set slowlibset_liberty_files [list \
    $tech_dir//tcbn65gpluswc_ccs.lib \
    $tech_dir/tune_lib/spsram_1024x16_tsmc65.lib \
    $tech_dir/tune_lib/spsram_128x8_tsmc65.lib \
    $tech_dir/tune_lib/spsram_256x41_tsmc65.lib \
    $tech_dir/tune_lib/spsram_512x16_tsmc65.lib \
    $tech_dir/tune_lib/spsram_64x98_tsmc65.lib \
    $tech_dir/tune_lib/spsram_1024x32_tsmc65.lib \
    $tech_dir/tune_lib/spsram_2048x32_tsmc65.lib \
    $tech_dir/tune_lib/spsram_256x4_tsmc65.lib \
    $tech_dir/tune_lib/spsram_64x58_tsmc65.lib \
    $tech_dir/tune_lib/spsram_1024x64_tsmc65.lib \
    $tech_dir/tune_lib/spsram_256x40_tsmc65.lib \
    $tech_dir/tune_lib/spsram_256x59_tsmc65.lib \
    $tech_dir/tune_lib/spsram_64x88_tsmc65.lib]
set liberty_files [concat $fastlibset_liberty_files $slowlibset_liberty_files]

set verilog_files [list $design_dir/route.v.gz]
set def_file $design_dir/route.def.gz
set sdc_files [list $design_dir/route.sdc]
set utilization 0.65
set clocks {CPU_CLK SYS_APB_CLK}
set period {2 4}
set scan_chain_flag 1
