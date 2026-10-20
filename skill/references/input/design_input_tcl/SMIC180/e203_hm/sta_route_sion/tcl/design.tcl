# Design identity and canonical input roots.
set design_name e203_hm
set tech_name SMIC180
set init_top_name e203_soc_top
set init_top_cell $init_top_name
set design_dir "$env(PV_ROOT)/svn/openedi/design_data/SMIC180/Itools21.1_Ifp_util0.65/$design_name"
set tech_dir "$env(PV_ROOT)/svn/openedi/large/SMIC180_new/smic180_library"

set power_net VDD
set ground_net VSS

set lef_files [list \
    $tech_dir/smic18_6lm_antRuleWA.lef \
    $tech_dir/sirv_debug_ram.lef \
    $tech_dir/sirv_gnrl_ram_32.lef \
    $tech_dir/sirv_gnrl_ram.lef \
    $tech_dir/sirv_mrom_2048x32.lef \
    $tech_dir/sirv_sim_ram.lef]
set slowlibset_liberty_files [list \
    $tech_dir/slow.lib \
    $tech_dir/sirv_debug_ram_ss_1.62_125.lib \
    $tech_dir/sirv_gnrl_ram_ss_1.62_125.lib \
    $tech_dir/sirv_mrom_ss_1.62_125.lib \
    $tech_dir/sirv_sim_ram_ss_1.62_125.lib \
    $tech_dir/sirv_mrom_2048x32_ss_1.62_125.lib \
    $tech_dir/sirv_gnrl_ram_32_ss_1.62_125.lib]
set fastlibset_liberty_files [list \
    $tech_dir/fast.lib \
    $tech_dir/sirv_debug_ram_ff_1.98_-40.lib \
    $tech_dir/sirv_gnrl_ram_ff_1.98_-40.lib \
    $tech_dir/sirv_mrom_ff_1.98_-40.lib \
    $tech_dir/sirv_sim_ram_ff_1.98_-40.lib \
    $tech_dir/sirv_mrom_2048x32_ff_1.98_-40.lib \
    $tech_dir/sirv_gnrl_ram_32_ff_1.98_-40.lib]
set liberty_files [concat $slowlibset_liberty_files $fastlibset_liberty_files]

set verilog_files [list $design_dir/route.v.gz]
set def_file $design_dir/route.def.gz
set sdc_files [list $design_dir/route.sdc]
set utilization 0.65
set clocks {hfextclk lfextclk}
set period {11.5 21.5}
set scan_chain_flag 1
