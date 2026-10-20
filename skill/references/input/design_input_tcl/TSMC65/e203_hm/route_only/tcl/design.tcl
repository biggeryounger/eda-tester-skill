# Design identity and canonical input roots.
set design_name   e203_hm
set tech_name     TSMC65
set design_dir "$env(PV_ROOT)/svn/openedi/design_data/TSMC65/Itools21.1_Ifp_util0.65/$design_name"
set tech_dir   "$env(PV_ROOT)/svn/openedi/design_data/TSMC65/tsmc65_library"

# top design name (itools default var)
set init_top_name e203_soc_top
set init_top_cell $init_top_name
# design common setting
set utilization 0.65
set clocks {hfextclk lfextclk}
# for fm LEC
set scan_chain_flag 1
set period {2.5 5}
set lef_files [list $tech_dir/tcbn65gplus_6lmT1_WITH_NDR.lef $tech_dir/tune_lef/sirv_gnrl_ram_32_tsmc65.lef  $tech_dir/tune_lef/sirv_gnrl_ram_tsmc65.lef  $tech_dir/tune_lef/sirv_mrom_2048x32_tsmc65.lef]
set fast_db [list $tech_dir/tcbn65gplusbc_ccs.db \
    $tech_dir/tune_lib/sirv_gnrl_ram_32_t65_ccs.db  $tech_dir/tune_lib/sirv_gnrl_ram_t65_ccs.db  \
    $tech_dir/tune_lib/sirv_mrom_2048x32_t65_ccs.db]
set slow_db [list $tech_dir/tcbn65gpluswc_ccs.db \
    $tech_dir/tune_lib/sirv_gnrl_ram_32_t65_ccs.db  $tech_dir/tune_lib/sirv_gnrl_ram_t65_ccs.db  \
    $tech_dir/tune_lib/sirv_mrom_2048x32_t65_ccs.db]
set slow_liberty_files [list $tech_dir/tcbn65gpluswc_ccs.lib \
    $tech_dir/tune_lib/sirv_gnrl_ram_32_tsmc65.lib  $tech_dir/tune_lib/sirv_gnrl_ram_tsmc65.lib  \
    $tech_dir/tune_lib/sirv_mrom_2048x32_tsmc65.lib]
set fast_liberty_files [list $tech_dir/tcbn65gplusbc_ccs.lib \
    $tech_dir/tune_lib/sirv_gnrl_ram_32_tsmc65.lib  $tech_dir/tune_lib/sirv_gnrl_ram_tsmc65.lib  \
    $tech_dir/tune_lib/sirv_mrom_2048x32_tsmc65.lib]

# Stage inputs.
set power_net    VDD
set ground_net   VSS
set verilog_files [list $design_dir/postcts.v.gz]
set def_file     $design_dir/postcts.def.gz
set sdc_files    [list $design_dir/postcts.sdc]
