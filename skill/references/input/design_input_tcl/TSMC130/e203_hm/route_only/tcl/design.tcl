# Design identity and canonical input roots.
set design_name   e203_hm
set tech_name     TSMC130
set design_dir "$env(PV_ROOT)/svn/openedi/design_data/TSMC130/Itools21.1_Ifp_util0.65/$design_name"
set tech_dir   "$env(PV_ROOT)/svn/openedi/design_data/TSMC130/tsmc130_library"

# top design name (itools default var)
set init_top_name e203_soc_top
set init_top_cell $init_top_name
# design common setting
set utilization 0.65
set clocks {hfextclk lfextclk}
set period {8 10}
# for fm LEC
set scan_chain_flag 1
set lef_files [list \
    $tech_dir/tcb013bcd_Fsg_6lm_5.7_WITH_NDR.lef \
    $tech_dir/tune_lef/sirv_gnrl_ram_32_tsmc130.lef \
    $tech_dir/tune_lef/sirv_gnrl_ram_tsmc130.lef \
    $tech_dir/tune_lef/sirv_mrom_2048x32_tsmc130.lef]
set fast_liberty_files [list \
    $tech_dir/tcb013bcdbc_ccs.lib \
    $tech_dir/sirv_gnrl_ram_32_ss_1.62_125.lib \
    $tech_dir/sirv_gnrl_ram_ss_1.62_125.lib \
    $tech_dir/sirv_mrom_2048x32_ss_1.62_125.lib]
set fast_db [list \
    $tech_dir/tcb013bcdbc_ccs.db \
    $tech_dir/sirv_gnrl_ram_32_ss_1.62_125.db \
    $tech_dir/sirv_gnrl_ram_ss_1.62_125.db \
    $tech_dir/sirv_mrom_2048x32_ss_1.62_125.db]
set slow_liberty_files [list \
    $tech_dir/tcb013bcdwc_ccs.lib \
    $tech_dir/sirv_gnrl_ram_32_ss_1.62_125.lib \
    $tech_dir/sirv_gnrl_ram_ss_1.62_125.lib \
    $tech_dir/sirv_mrom_2048x32_ss_1.62_125.lib]
set slow_db [list \
    $tech_dir/tcb013bcdwc_ccs.db \
    $tech_dir/sirv_gnrl_ram_32_ss_1.62_125.db \
    $tech_dir/sirv_gnrl_ram_ss_1.62_125.db \
    $tech_dir/sirv_mrom_2048x32_ss_1.62_125.db]

# Stage inputs.
set power_net    VDD
set ground_net   GND
set verilog_files [list $design_dir/postcts.v.gz]
set def_file     $design_dir/postcts.def.gz
set sdc_files    [list $design_dir/postcts.sdc]
