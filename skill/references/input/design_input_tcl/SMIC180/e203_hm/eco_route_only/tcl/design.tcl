# Design identity and canonical input roots.
set design_name   e203_hm
set tech_name     SMIC180
set init_top_name e203_soc_top
set design_dir "$env(PV_ROOT)/svn/openedi/design_data/SMIC180/Itools21.1_Ifp_util0.65/$design_name"
set tech_dir   "$env(PV_ROOT)/svn/openedi/large/SMIC180_new/smic180_library"

set power_net  VDD
set ground_net GND

set lef_files [list \
    $tech_dir/smic18_6lm_antRuleWA.lef \
    $tech_dir/sirv_debug_ram.lef \
    $tech_dir/sirv_gnrl_ram_32.lef \
    $tech_dir/sirv_gnrl_ram.lef \
    $tech_dir/sirv_mrom_2048x32.lef \
    $tech_dir/sirv_sim_ram.lef]
set slow_liberty_files [list \
    $tech_dir/slow.lib \
    $tech_dir/sirv_debug_ram_ss_1.62_125.lib \
    $tech_dir/sirv_gnrl_ram_ss_1.62_125.lib \
    $tech_dir/sirv_mrom_ss_1.62_125.lib \
    $tech_dir/sirv_sim_ram_ss_1.62_125.lib \
    $tech_dir/sirv_mrom_2048x32_ss_1.62_125.lib \
    $tech_dir/sirv_gnrl_ram_32_ss_1.62_125.lib]
set fast_liberty_files [list \
    $tech_dir/fast.lib \
    $tech_dir/sirv_debug_ram_ff_1.98_-40.lib \
    $tech_dir/sirv_gnrl_ram_ff_1.98_-40.lib \
    $tech_dir/sirv_mrom_ff_1.98_-40.lib \
    $tech_dir/sirv_sim_ram_ff_1.98_-40.lib \
    $tech_dir/sirv_mrom_2048x32_ff_1.98_-40.lib \
    $tech_dir/sirv_gnrl_ram_32_ff_1.98_-40.lib]
set liberty_files [concat $slow_liberty_files $fast_liberty_files]


set verilog_files [list $design_dir/for_ecoroute.v.gz]
set def_file      $design_dir/for_ecoroute.def.gz
set sdc_files     [list $design_dir/for_ecoroute.sdc]
