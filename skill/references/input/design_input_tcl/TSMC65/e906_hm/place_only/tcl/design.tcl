# Design identity and canonical input roots.
set design_name   e906_hm
set tech_name     TSMC65
set design_dir "$env(PV_ROOT)/svn/openedi/design_data/TSMC65/Itools21.1_Ifp_util0.65/$design_name"
set tech_dir   "$env(PV_ROOT)/svn/openedi/design_data/TSMC65/tsmc65_library"

# top design name (itools default var)
set init_top_name openE906
set init_top_cell $init_top_name
# design common setting
set utilization 0.65
set clocks {CPU_CLOCK}
set period {2}
# for fm LEC
set scan_chain_flag 1
set lef_files [list $tech_dir/tcbn65gplus_6lmT1_WITH_NDR.lef $tech_dir/tune_lef/spsram_1024x16_tsmc65.lef  $tech_dir/tune_lef/spsram_128x42_tsmc65.lef   $tech_dir/tune_lef/spsram_256x41_tsmc65.lef   $tech_dir/tune_lef/spsram_512x16_tsmc65.lef  $tech_dir/tune_lef/spsram_64x4_tsmc65.lef $tech_dir/tune_lef/spsram_1024x32_tsmc65.lef  $tech_dir/tune_lef/spsram_128x43_tsmc65.lef   $tech_dir/tune_lef/spsram_256x4_tsmc65.lef    $tech_dir/tune_lef/spsram_512x32_tsmc65.lef  $tech_dir/tune_lef/spsram_64x58_tsmc65.lef $tech_dir/tune_lef/spsram_1024x36_tsmc65.lef  $tech_dir/tune_lef/spsram_128x4_tsmc65.lef    $tech_dir/tune_lef/spsram_256x59_tsmc65.lef   $tech_dir/tune_lef/spsram_512x38_tsmc65.lef  $tech_dir/tune_lef/spsram_64x88_tsmc65.lef $tech_dir/tune_lef/spsram_1024x37_tsmc65.lef  $tech_dir/tune_lef/spsram_128x8_tsmc65.lef    $tech_dir/tune_lef/spsram_32x46_tsmc65.lef    $tech_dir/tune_lef/spsram_512x39_tsmc65.lef  $tech_dir/tune_lef/spsram_64x98_tsmc65.lef $tech_dir/tune_lef/spsram_1024x4_tsmc65.lef   $tech_dir/tune_lef/spsram_2048x32_tsmc65.lef  $tech_dir/tune_lef/spsram_32x47_tsmc65.lef    $tech_dir/tune_lef/spsram_512x4_tsmc65.lef   $tech_dir/tune_lef/spsram_8192x32_tsmc65.lef $tech_dir/tune_lef/spsram_1024x64_tsmc65.lef  $tech_dir/tune_lef/spsram_256x32_tsmc65.lef   $tech_dir/tune_lef/spsram_32x4_tsmc65.lef     $tech_dir/tune_lef/spsram_64x44_tsmc65.lef $tech_dir/tune_lef/spsram_128x32_tsmc65.lef   $tech_dir/tune_lef/spsram_256x40_tsmc65.lef   $tech_dir/tune_lef/spsram_4096x32_tsmc65.lef  $tech_dir/tune_lef/spsram_64x45_tsmc65.lef]
set fast_db [list $tech_dir/tcbn65gplusbc_ccs.db \
    $tech_dir/tune_lib/spsram_1024x32__t65_ccs.db             $tech_dir/tune_lib/spsram_256x41__t65_ccs.db \
    $tech_dir/tune_lib/spsram_256x40__t65_ccs.db              $tech_dir/tune_lib/spsram_512x16__t65_ccs.db \
    $tech_dir/tune_lib/spsram_256x4__t65_ccs.db                $tech_dir/tune_lib/spsram_2048x32__t65_ccs.db]
set slow_db [list $tech_dir/tcbn65gpluswc_ccs.db \
    $tech_dir/tune_lib/spsram_1024x32__t65_ccs.db             $tech_dir/tune_lib/spsram_256x41__t65_ccs.db \
    $tech_dir/tune_lib/spsram_256x40__t65_ccs.db              $tech_dir/tune_lib/spsram_512x16__t65_ccs.db \
    $tech_dir/tune_lib/spsram_256x4__t65_ccs.db                $tech_dir/tune_lib/spsram_2048x32__t65_ccs.db]
set slow_liberty_files [list $tech_dir/tcbn65gpluswc_ccs.lib \
    $tech_dir/tune_lib/spsram_1024x32_tsmc65.lib             $tech_dir/tune_lib/spsram_256x41_tsmc65.lib \
    $tech_dir/tune_lib/spsram_256x40_tsmc65.lib              $tech_dir/tune_lib/spsram_512x16_tsmc65.lib \
    $tech_dir/tune_lib/spsram_256x4_tsmc65.lib                $tech_dir/tune_lib/spsram_2048x32_tsmc65.lib]
set fast_liberty_files [list $tech_dir/tcbn65gplusbc_ccs.lib  \
    $tech_dir/tune_lib/spsram_1024x32_tsmc65.lib             $tech_dir/tune_lib/spsram_256x41_tsmc65.lib \
    $tech_dir/tune_lib/spsram_256x40_tsmc65.lib              $tech_dir/tune_lib/spsram_512x16_tsmc65.lib \
    $tech_dir/tune_lib/spsram_256x4_tsmc65.lib                $tech_dir/tune_lib/spsram_2048x32_tsmc65.lib]

# Stage inputs.
set power_net    VDD
set ground_net   VSS
set verilog_files [list $design_dir/floorplan.v.gz]
set def_file     $design_dir/floorplan.def.gz
set sdc_files    [list $design_dir/floorplan.sdc]
