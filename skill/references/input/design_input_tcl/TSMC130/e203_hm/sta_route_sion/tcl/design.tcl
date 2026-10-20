# Design identity and canonical input roots.
set design_name e203_hm
set tech_name TSMC130
set init_top_name e203_soc_top
set init_top_cell $init_top_name
set design_dir "$env(PV_ROOT)/svn/openedi/design_data/TSMC130/Itools21.1_Ifp_util0.65/$design_name"
set tech_dir "$env(PV_ROOT)/svn/openedi/design_data/TSMC130/tsmc130_library"

set power_net VDD
set ground_net VSS

set lef_files [list \
    $tech_dir/tcb013bcd_Fsg_6lm_5.7_WITH_NDR.lef \
    $tech_dir/tune_lef/sirv_gnrl_ram_32_tsmc130.lef \
    $tech_dir/tune_lef/sirv_gnrl_ram_tsmc130.lef \
    $tech_dir/tune_lef/sirv_mrom_2048x32_tsmc130.lef]
set fastlibset_liberty_files [list \
    $tech_dir/tcb013bcdbc_ccs.lib \
    $tech_dir/sirv_gnrl_ram_32_ss_1.62_125.lib \
    $tech_dir/sirv_gnrl_ram_ss_1.62_125.lib \
    $tech_dir/sirv_mrom_2048x32_ss_1.62_125.lib]
set slowlibset_liberty_files [list \
    $tech_dir/tcb013bcdwc_ccs.lib \
    $tech_dir/sirv_gnrl_ram_32_ss_1.62_125.lib \
    $tech_dir/sirv_gnrl_ram_ss_1.62_125.lib \
    $tech_dir/sirv_mrom_2048x32_ss_1.62_125.lib]
set liberty_files [concat $fastlibset_liberty_files $slowlibset_liberty_files]

set verilog_files [list $design_dir/route.v.gz]
set def_file $design_dir/route.def.gz
set sdc_files [list $design_dir/route.sdc]
set utilization 0.65
set clocks {hfextclk lfextclk}
set period {8 10}
set scan_chain_flag 1
