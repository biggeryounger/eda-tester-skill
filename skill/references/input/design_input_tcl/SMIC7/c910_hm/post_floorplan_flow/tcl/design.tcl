# Design identity and canonical input roots.
set design_name   c910_hm
set tech_name     SMIC7
set init_top_name openC910
set design_dir "$env(PV_ROOT)/svn/openedi/design_data/SMIC7_C910"
set tech_dir   "$env(PV_ROOT)/svn/openedi/design_data/SMIC7_C910/library"

set power_net  VDD
set ground_net VSS
set lef_files [list \
    $tech_dir/tlef/PRTF_Innovus_N7_13M_1X1Xa1Ya5Y2Yy2Z_UTRDL_M1P57_M2P40_M3P44_M4P76_M5P76_M6P76_M7P76_M8P76_M9P76_H240.13_1c.tlef \
    $tech_dir/lef/NDR_2W2S.lef \
    $tech_dir/lef/std/tcbn07_bwph240l8p57pd_base_lvt.lef \
    $tech_dir/lef/std/tcbn07_bwph240l8p57pd_base_ulvt.lef \
    $tech_dir/lef/std/tcbn07_bwph240l8p57pd_base_svt.lef \
    $tech_dir/lef/macro/ct_hsspsram_1024x64m4.lef \
    $tech_dir/lef/macro/ct_hsspsram_512x44m2.lef \
    $tech_dir/lef/macro/ct_spmbsram_2048x32m4Q.lef \
    $tech_dir/lef/macro/ct_hsspsram_128x16m2.lef \
    $tech_dir/lef/macro/ct_hsspsram_512x52m2.lef \
    $tech_dir/lef/macro/ct_spmbsram_4096x128m4Q.lef \
    $tech_dir/lef/macro/ct_hsspsram_256x23m2.lef \
    $tech_dir/lef/macro/ct_hsspsram_512x54m2.lef \
    $tech_dir/lef/macro/ct_spsbsram_1024x128m4.lef \
    $tech_dir/lef/macro/ct_hsspsram_256x84m2.lef \
    $tech_dir/lef/macro/ct_hsspsram_512x59m2.lef \
    $tech_dir/lef/macro/ct_spsbsram_256x196m2.lef \
    $tech_dir/lef/macro/ct_hsspsram_512x144m2.lef \
    $tech_dir/lef/macro/ct_hsspsram_512x8m2.lef \
    $tech_dir/lef/macro/ct_hsspsram_512x22m2.lef \
    $tech_dir/lef/macro/ct_hsspsram_512x96m2.lef]
set verilog_files [list $design_dir/design/netlist/openC910.mapped.v.gz]
set def_file      $design_dir/fp.def.gz
set sdc_files     [list ./openC910.mapped.sdc]

set libset_cworst_ccworst_t_liberty_files [list $tech_dir/lib/std/ssgnp_0p765v_m40c/tcbn07_bwph240l8p57pd_base_lvtssgnp_0p765v_m40c_cworst_CCworst_T_ccs.lib.gz \
    $tech_dir/lib/std/ssgnp_0p765v_m40c/tcbn07_bwph240l8p57pd_base_svtssgnp_0p765v_m40c_cworst_CCworst_T_ccs.lib.gz \
    $tech_dir/lib/std/ssgnp_0p765v_m40c/tcbn07_bwph240l8p57pd_base_ulvtssgnp_0p765v_m40c_cworst_CCworst_T_ccs.lib.gz \
    $tech_dir/lib/macro/ssgnp_0p765v_m40c/ct_hsspsram_1024x64m4_ssgnp_0p765v_m40c_cworst_ccworst_t.lib \
    $tech_dir/lib/macro/ssgnp_0p765v_m40c/ct_hsspsram_128x16m2_ssgnp_0p765v_m40c_cworst_ccworst_t.lib \
    $tech_dir/lib/macro/ssgnp_0p765v_m40c/ct_hsspsram_256x23m2_ssgnp_0p765v_m40c_cworst_ccworst_t.lib \
    $tech_dir/lib/macro/ssgnp_0p765v_m40c/ct_hsspsram_256x84m2_ssgnp_0p765v_m40c_cworst_ccworst_t.lib \
    $tech_dir/lib/macro/ssgnp_0p765v_m40c/ct_hsspsram_512x144m2_ssgnp_0p765v_m40c_cworst_ccworst_t.lib \
    $tech_dir/lib/macro/ssgnp_0p765v_m40c/ct_hsspsram_512x22m2_ssgnp_0p765v_m40c_cworst_ccworst_t.lib \
    $tech_dir/lib/macro/ssgnp_0p765v_m40c/ct_hsspsram_512x44m2_ssgnp_0p765v_m40c_cworst_ccworst_t.lib \
    $tech_dir/lib/macro/ssgnp_0p765v_m40c/ct_hsspsram_512x52m2_ssgnp_0p765v_m40c_cworst_ccworst_t.lib \
    $tech_dir/lib/macro/ssgnp_0p765v_m40c/ct_hsspsram_512x54m2_ssgnp_0p765v_m40c_cworst_ccworst_t.lib \
    $tech_dir/lib/macro/ssgnp_0p765v_m40c/ct_hsspsram_512x59m2_ssgnp_0p765v_m40c_cworst_ccworst_t.lib \
    $tech_dir/lib/macro/ssgnp_0p765v_m40c/ct_hsspsram_512x8m2_ssgnp_0p765v_m40c_cworst_ccworst_t.lib \
    $tech_dir/lib/macro/ssgnp_0p765v_m40c/ct_hsspsram_512x96m2_ssgnp_0p765v_m40c_cworst_ccworst_t.lib \
    $tech_dir/lib/macro/ssgnp_0p765v_m40c/ct_spmbsram_2048x32m4Q_ssgnp_0p765v_m40c_cworst_ccworst_t.lib \
    $tech_dir/lib/macro/ssgnp_0p765v_m40c/ct_spmbsram_4096x128m4Q_ssgnp_0p765v_m40c_cworst_ccworst_t.lib \
    $tech_dir/lib/macro/ssgnp_0p765v_m40c/ct_spsbsram_1024x128m4_ssgnp_0p765v_m40c_cworst_ccworst_t.lib \
    $tech_dir/lib/macro/ssgnp_0p765v_m40c/ct_spsbsram_256x196m2_ssgnp_0p765v_m40c_cworst_ccworst_t.lib]

set libset_cbest_ccbest_t_liberty_files [list $tech_dir/lib/std/ffgnp_0p935v_125c/tcbn07_bwph240l8p57pd_base_lvtffgnp_0p935v_125c_cbest_CCbest_T_ccs.lib.gz \
    $tech_dir/lib/std/ffgnp_0p935v_125c/tcbn07_bwph240l8p57pd_base_svtffgnp_0p935v_125c_cbest_CCbest_T_ccs.lib.gz \
    $tech_dir/lib/std/ffgnp_0p935v_125c/tcbn07_bwph240l8p57pd_base_ulvtffgnp_0p935v_125c_cbest_CCbest_T_ccs.lib.gz \
    $tech_dir/lib/macro//ffgnp_0p935v_125c/ct_hsspsram_1024x64m4_ffgnp_0p935v_125c_cbest_ccbest.lib \
    $tech_dir/lib/macro//ffgnp_0p935v_125c/ct_hsspsram_128x16m2_ffgnp_0p935v_125c_cbest_ccbest.lib \
    $tech_dir/lib/macro//ffgnp_0p935v_125c/ct_hsspsram_256x23m2_ffgnp_0p935v_125c_cbest_ccbest.lib \
    $tech_dir/lib/macro//ffgnp_0p935v_125c/ct_hsspsram_256x84m2_ffgnp_0p935v_125c_cbest_ccbest.lib \
    $tech_dir/lib/macro//ffgnp_0p935v_125c/ct_hsspsram_512x144m2_ffgnp_0p935v_125c_cbest_ccbest.lib \
    $tech_dir/lib/macro//ffgnp_0p935v_125c/ct_hsspsram_512x22m2_ffgnp_0p935v_125c_cbest_ccbest.lib \
    $tech_dir/lib/macro//ffgnp_0p935v_125c/ct_hsspsram_512x44m2_ffgnp_0p935v_125c_cbest_ccbest.lib \
    $tech_dir/lib/macro//ffgnp_0p935v_125c/ct_hsspsram_512x52m2_ffgnp_0p935v_125c_cbest_ccbest.lib \
    $tech_dir/lib/macro//ffgnp_0p935v_125c/ct_hsspsram_512x54m2_ffgnp_0p935v_125c_cbest_ccbest.lib \
    $tech_dir/lib/macro//ffgnp_0p935v_125c/ct_hsspsram_512x59m2_ffgnp_0p935v_125c_cbest_ccbest.lib \
    $tech_dir/lib/macro//ffgnp_0p935v_125c/ct_hsspsram_512x8m2_ffgnp_0p935v_125c_cbest_ccbest.lib \
    $tech_dir/lib/macro//ffgnp_0p935v_125c/ct_hsspsram_512x96m2_ffgnp_0p935v_125c_cbest_ccbest.lib \
    $tech_dir/lib/macro//ffgnp_0p935v_125c/ct_spmbsram_2048x32m4Q_ffgnp_0p935v_125c_cbest_ccbest.lib \
    $tech_dir/lib/macro//ffgnp_0p935v_125c/ct_spmbsram_4096x128m4Q_ffgnp_0p935v_125c_cbest_ccbest.lib \
    $tech_dir/lib/macro//ffgnp_0p935v_125c/ct_spsbsram_1024x128m4_ffgnp_0p935v_125c_cbest_ccbest.lib \
    $tech_dir/lib/macro//ffgnp_0p935v_125c/ct_spsbsram_256x196m2_ffgnp_0p935v_125c_cbest_ccbest.lib]

switch -- $PV_TOOL {
    optimus {
    set cworst_rc_tech_file  $env(PV_ROOT)/svn/openedi/design_data/SMIC7_C910/1p13m_rc_tech/cworst_ccworst_T/rc_tech
    set cbest_rc_tech_file  $env(PV_ROOT)/svn/openedi/design_data/SMIC7_C910/1p13m_rc_tech/cbest_ccbest_T/rc_tech
    }
itools {
    set cworst_rc_tech_file  $tech_dir/rc_tech/cworst_ccworst_T/qrcTechFile
    set cbest_rc_tech_file  $tech_dir/rc_tech/cbest_ccbest_T/qrcTechFile
}
default { error "Unsupported PV_TOOL: $PV_TOOL" }
}
