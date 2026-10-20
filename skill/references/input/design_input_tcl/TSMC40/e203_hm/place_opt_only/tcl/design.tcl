# Design identity and canonical input roots.
set design_name   e203_hm
set tech_name     TSMC40
set design_dir "$env(PV_ROOT)/svn/openedi/design_data/TSMC40/Itools21.1_Ifp_util0.65/$design_name"
set tech_dir   "$env(PV_ROOT)/svn/openedi/design_data/TSMC40/tsmc40_library"

# top design name (itools default var)
set init_top_name e203_soc_top
set init_top_cell $init_top_name
# design common setting
set utilization 0.65
set clocks {hfextclk lfextclk}
set period  {6.6 13.2}
# for fm LEC
set scan_chain_flag 1
set lef_files [list $tech_dir/tcbn40lpbwp_8lm5X2ZRDL_WITH_NDR.lef $tech_dir/tune_lef/sirv_gnrl_ram_32_tsmc40.lef  $tech_dir/tune_lef/sirv_gnrl_ram_tsmc40.lef  $tech_dir/tune_lef/sirv_mrom_2048x32_tsmc40.lef]
set fast_db [list $tech_dir/tcbn40lpbwpbc_ccs.db $tech_dir/tune_lib/sirv_gnrl_ram_32_wc_ccs.db  $tech_dir/tune_lib/sirv_gnrl_ram_wc_ccs.db  $tech_dir/tune_lib/sirv_mrom_2048x32_wc_ccs.db]
set slow_db [list $tech_dir/tcbn40lpbwpwc_ccs.db $tech_dir/tune_lib/sirv_gnrl_ram_32_wc_ccs.db  $tech_dir/tune_lib/sirv_gnrl_ram_wc_ccs.db  $tech_dir/tune_lib/sirv_mrom_2048x32_wc_ccs.db]
set slow_liberty_files [list $tech_dir/tcbn40lpbwpwc_ccs.lib \
    $tech_dir/tune_lib/sirv_gnrl_ram_32_tsmc40.lib  $tech_dir/tune_lib/sirv_gnrl_ram_tsmc40.lib  $tech_dir/tune_lib/sirv_mrom_2048x32_tsmc40.lib]
set fast_liberty_files [list $tech_dir/tcbn40lpbwpbc_ccs.lib \
    $tech_dir/tune_lib/sirv_gnrl_ram_32_tsmc40.lib  $tech_dir/tune_lib/sirv_gnrl_ram_tsmc40.lib  $tech_dir/tune_lib/sirv_mrom_2048x32_tsmc40.lib]

# Stage inputs.
set power_net    VDD
set ground_net   GND
set verilog_files [list $design_dir/place.v.gz]
set def_file     $design_dir/place.def.gz
set sdc_files    [list $design_dir/place.sdc]
