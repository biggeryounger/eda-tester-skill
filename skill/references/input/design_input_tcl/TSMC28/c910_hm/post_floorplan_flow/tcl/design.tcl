# Design identity and canonical input roots.
set design_name   c910_hm
set tech_name     TSMC28
set init_top_name openC910

#set design_dir "$env(PV_ROOT)/svn/openedi/design_data/TSMC28_C910/$design_name"
set design_dir "$env(PV_ROOT)/svn/openedi/design_data/TSMC28_C910/$init_top_name"
set tech_dir   "$env(PV_ROOT)/svn/openedi/design_data/TSMC28_C910/library"

set power_net  VDD
set ground_net VSS
set lef_files [list $tech_dir/lef/tsmcn28_10lm5X2Y2ZUTRDL.tlef \
    $tech_dir/../NDR_2W2S.lef \
    $tech_dir/lef/tcbn28hpcplusbwp40p140.lef \
    $tech_dir/lef/tcbn28hpcplusbwp35p140.lef \
    $tech_dir/lef/tcbn28hpcplusbwp30p140.lef \
    $tech_dir/lef/tcbn28hpcplusbwp30p140lvt.lef \
    $tech_dir/lef/tcbn28hpcplusbwp35p140lvt.lef \
    $tech_dir/lef/tcbn28hpcplusbwp40p140lvt.lef \
    $tech_dir/lef/tcbn28hpcplusbwp30p140hvt.lef \
    $tech_dir/lef/tcbn28hpcplusbwp35p140hvt.lef \
    $tech_dir/lef/tcbn28hpcplusbwp40p140hvt.lef \
    $tech_dir/lef/ts1n28hpcplvtb1024x128m4sw_180a.lef \
    $tech_dir/lef/ts1n28hpcplvtb1024x144m4sw_180a.lef \
    $tech_dir/lef/ts1n28hpcplvtb1024x32m4sw_180a.lef \
    $tech_dir/lef/ts1n28hpcplvtb1024x59m4sw_180a.lef \
    $tech_dir/lef/ts1n28hpcplvtb1024x64m4sw_180a.lef \
    $tech_dir/lef/ts1n28hpcplvtb1024x92m4sw_180a.lef \
    $tech_dir/lef/ts1n28hpcplvtb128x104m4sw_180a.lef \
    $tech_dir/lef/ts1n28hpcplvtb128x144m4sw_180a.lef \
    $tech_dir/lef/ts1n28hpcplvtb128x16m4sw_180a.lef \
    $tech_dir/lef/ts1n28hpcplvtb2048x128m4sw_180a.lef \
    $tech_dir/lef/ts1n28hpcplvtb2048x144m4sw_180a.lef \
    $tech_dir/lef/ts1n28hpcplvtb2048x32m4sw_180a.lef \
    $tech_dir/lef/ts1n28hpcplvtb2048x59m4sw_180a.lef \
    $tech_dir/lef/ts1n28hpcplvtb2048x88m4sw_180a.lef \
    $tech_dir/lef/ts1n28hpcplvtb256x100m4sw_180a.lef \
    $tech_dir/lef/ts1n28hpcplvtb256x144m4sw_180a.lef \
    $tech_dir/lef/ts1n28hpcplvtb256x23m4sw_180a.lef \
    $tech_dir/lef/ts1n28hpcplvtb256x52m4sw_180a.lef \
    $tech_dir/lef/ts1n28hpcplvtb256x54m4sw_180a.lef \
    $tech_dir/lef/ts1n28hpcplvtb256x59m4sw_180a.lef \
    $tech_dir/lef/ts1n28hpcplvtb256x7m8sw_180a.lef \
    $tech_dir/lef/ts1n28hpcplvtb256x84m4sw_180a.lef \
    $tech_dir/lef/ts1n28hpcplvtb4096x128m4sw_180a.lef \
    $tech_dir/lef/ts1n28hpcplvtb4096x144m4sw_180a.lef \
    $tech_dir/lef/ts1n28hpcplvtb4096x32m4sw_180a.lef \
    $tech_dir/lef/ts1n28hpcplvtb4096x84m4sw_180a.lef \
    $tech_dir/lef/ts1n28hpcplvtb512x144m4sw_180a.lef \
    $tech_dir/lef/ts1n28hpcplvtb512x22m4sw_180a.lef \
    $tech_dir/lef/ts1n28hpcplvtb512x44m4sw_180a.lef \
    $tech_dir/lef/ts1n28hpcplvtb512x52m4sw_180a.lef \
    $tech_dir/lef/ts1n28hpcplvtb512x54m4sw_180a.lef \
    $tech_dir/lef/ts1n28hpcplvtb512x59m4sw_180a.lef \
    $tech_dir/lef/ts1n28hpcplvtb512x7m8sw_180a.lef \
    $tech_dir/lef/ts1n28hpcplvtb512x96m4sw_180a.lef \
    $tech_dir/lef/ts1n28hpcplvtb64x108m4sw_180a.lef \
    $tech_dir/lef/ts1n28hpcplvtb8192x128m4sw_180a.lef \
    $tech_dir/lef/ts1n28hpcplvtb8192x32m4sw_180a.lef]
set verilog_files [list $design_dir/openC910_10m.v]
set def_file      $design_dir/../t28_910_fp_shrink.def.gz
set sdc_files     [list $design_dir/../openC910_10m_tune.sdc]

set libset_rcworst_liberty_files [list $tech_dir/lib/tcbn28hpcplusbwp40p140ssg0p81vm40c.lib \
    $tech_dir/lib/tcbn28hpcplusbwp30p140ssg0p81vm40c.lib \
    $tech_dir/lib/tcbn28hpcplusbwp35p140ssg0p81vm40c.lib \
    $tech_dir/lib/tcbn28hpcplusbwp40p140lvtssg0p81vm40c.lib \
    $tech_dir/lib/tcbn28hpcplusbwp30p140lvtssg0p81vm40c.lib \
    $tech_dir/lib/tcbn28hpcplusbwp35p140lvtssg0p81vm40c.lib \
    $tech_dir/lib/tcbn28hpcplusbwp40p140hvtssg0p81vm40c.lib \
    $tech_dir/lib/tcbn28hpcplusbwp30p140hvtssg0p81vm40c.lib \
    $tech_dir/lib/tcbn28hpcplusbwp35p140hvtssg0p81vm40c.lib \
    $tech_dir/lib/ts1n28hpcplvtb1024x128m4sw_180a_ssg0p81vm40c.lib \
    $tech_dir/lib/ts1n28hpcplvtb1024x144m4sw_180a_ssg0p81vm40c.lib \
    $tech_dir/lib/ts1n28hpcplvtb1024x32m4sw_180a_ssg0p81vm40c.lib \
    $tech_dir/lib/ts1n28hpcplvtb1024x59m4sw_180a_ssg0p81vm40c.lib \
    $tech_dir/lib/ts1n28hpcplvtb1024x64m4sw_180a_ssg0p81vm40c.lib \
    $tech_dir/lib/ts1n28hpcplvtb1024x92m4sw_180a_ssg0p81vm40c.lib \
    $tech_dir/lib/ts1n28hpcplvtb128x104m4sw_180a_ssg0p81vm40c.lib \
    $tech_dir/lib/ts1n28hpcplvtb128x144m4sw_180a_ssg0p81vm40c.lib \
    $tech_dir/lib/ts1n28hpcplvtb128x16m4sw_180a_ssg0p81vm40c.lib \
    $tech_dir/lib/ts1n28hpcplvtb2048x128m4sw_180a_ssg0p81vm40c.lib \
    $tech_dir/lib/ts1n28hpcplvtb2048x144m4sw_180a_ssg0p81vm40c.lib \
    $tech_dir/lib/ts1n28hpcplvtb2048x32m4sw_180a_ssg0p81vm40c.lib \
    $tech_dir/lib/ts1n28hpcplvtb2048x59m4sw_180a_ssg0p81vm40c.lib \
    $tech_dir/lib/ts1n28hpcplvtb2048x88m4sw_180a_ssg0p81vm40c.lib \
    $tech_dir/lib/ts1n28hpcplvtb256x100m4sw_180a_ssg0p81vm40c.lib \
    $tech_dir/lib/ts1n28hpcplvtb256x144m4sw_180a_ssg0p81vm40c.lib \
    $tech_dir/lib/ts1n28hpcplvtb256x23m4sw_180a_ssg0p81vm40c.lib \
    $tech_dir/lib/ts1n28hpcplvtb256x52m4sw_180a_ssg0p81vm40c.lib \
    $tech_dir/lib/ts1n28hpcplvtb256x54m4sw_180a_ssg0p81vm40c.lib \
    $tech_dir/lib/ts1n28hpcplvtb256x59m4sw_180a_ssg0p81vm40c.lib \
    $tech_dir/lib/ts1n28hpcplvtb256x7m8sw_180a_ssg0p81vm40c.lib \
    $tech_dir/lib/ts1n28hpcplvtb256x84m4sw_180a_ssg0p81vm40c.lib \
    $tech_dir/lib/ts1n28hpcplvtb4096x128m4sw_180a_ssg0p81vm40c.lib \
    $tech_dir/lib/ts1n28hpcplvtb4096x144m4sw_180a_ssg0p81vm40c.lib \
    $tech_dir/lib/ts1n28hpcplvtb4096x32m4sw_180a_ssg0p81vm40c.lib \
    $tech_dir/lib/ts1n28hpcplvtb4096x84m4sw_180a_ssg0p81vm40c.lib \
    $tech_dir/lib/ts1n28hpcplvtb512x144m4sw_180a_ssg0p81vm40c.lib \
    $tech_dir/lib/ts1n28hpcplvtb512x22m4sw_180a_ssg0p81vm40c.lib \
    $tech_dir/lib/ts1n28hpcplvtb512x44m4sw_180a_ssg0p81vm40c.lib \
    $tech_dir/lib/ts1n28hpcplvtb512x52m4sw_180a_ssg0p81vm40c.lib \
    $tech_dir/lib/ts1n28hpcplvtb512x54m4sw_180a_ssg0p81vm40c.lib \
    $tech_dir/lib/ts1n28hpcplvtb512x59m4sw_180a_ssg0p81vm40c.lib \
    $tech_dir/lib/ts1n28hpcplvtb512x7m8sw_180a_ssg0p81vm40c.lib \
    $tech_dir/lib/ts1n28hpcplvtb512x96m4sw_180a_ssg0p81vm40c.lib \
    $tech_dir/lib/ts1n28hpcplvtb64x108m4sw_180a_ssg0p81vm40c.lib \
    $tech_dir/lib/ts1n28hpcplvtb8192x128m4sw_180a_ssg0p81vm40c.lib \
    $tech_dir/lib/ts1n28hpcplvtb8192x32m4sw_180a_ssg0p81vm40c.lib]


switch -- $PV_TOOL {
    optimus {
    set rcworst_rc_tech_file  $env(PV_ROOT)/svn/openedi/design_data/TSMC28_C910/rc_tech/rcworst/optimus_rc.enTech
    }
itools {
    set rcworst_rc_tech_file  $env(PV_ROOT)/svn/openedi/design_data/TSMC28_C910/rc_tech/rcworst/qrcTechFile
}
default { error "Unsupported PV_TOOL: $PV_TOOL" }
}
set rc_tech_file $rcworst_rc_tech_file
