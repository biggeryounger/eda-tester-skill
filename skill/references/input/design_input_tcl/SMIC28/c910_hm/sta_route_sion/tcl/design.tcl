# Design identity and canonical input roots.
set design_name c910_hm
set tech_name SMIC28
set init_top_name openC910
set init_top_cell $init_top_name
set design_dir "$env(PV_ROOT)/svn/openedi/design_data/SMIC28/Itools21.1_Ifp_util0.65/$design_name"
set tech_dir "$env(PV_ROOT)/svn/openedi/design_data/SMIC28/smic28_library"

set power_net VDD
set ground_net VSS

set lef_files [list \
    $tech_dir/scc28n_12t25od33_1p8m_7ic_1tmc_alpa1_WITH_NDR.lef \
    $tech_dir/scc28nhkcp_hsc30p140_rvt_ant.lef \
    $tech_dir/S28_memory/sp_hde_1024x128.lef \
    $tech_dir/S28_memory/sp_hde_1024x144.lef \
    $tech_dir/S28_memory/sp_hde_1024x32.lef \
    $tech_dir/S28_memory/sp_hde_1024x59.lef \
    $tech_dir/S28_memory/sp_hde_1024x64.lef \
    $tech_dir/S28_memory/sp_hde_1024x92.lef \
    $tech_dir/S28_memory/sp_hde_16384x128.lef \
    $tech_dir/S28_memory/sp_hde_2048x128.lef \
    $tech_dir/S28_memory/sp_hde_2048x144.lef \
    $tech_dir/S28_memory/sp_hde_2048x32.lef \
    $tech_dir/S28_memory/sp_hde_2048x59.lef \
    $tech_dir/S28_memory/sp_hde_2048x88.lef \
    $tech_dir/S28_memory/sp_hde_32768x64.lef \
    $tech_dir/S28_memory/sp_hde_4096x128.lef \
    $tech_dir/S28_memory/sp_hde_4096x144.lef \
    $tech_dir/S28_memory/sp_hde_4096x32.lef \
    $tech_dir/S28_memory/sp_hde_4096x84.lef \
    $tech_dir/S28_memory/sp_hde_512x100.lef \
    $tech_dir/S28_memory/sp_hde_512x104.lef \
    $tech_dir/S28_memory/sp_hde_512x108.lef \
    $tech_dir/S28_memory/sp_hde_512x144.lef \
    $tech_dir/S28_memory/sp_hde_512x16.lef \
    $tech_dir/S28_memory/sp_hde_512x22.lef \
    $tech_dir/S28_memory/sp_hde_512x23.lef \
    $tech_dir/S28_memory/sp_hde_512x44.lef \
    $tech_dir/S28_memory/sp_hde_512x52.lef \
    $tech_dir/S28_memory/sp_hde_512x54.lef \
    $tech_dir/S28_memory/sp_hde_512x59.lef \
    $tech_dir/S28_memory/sp_hde_512x7.lef \
    $tech_dir/S28_memory/sp_hde_512x84.lef \
    $tech_dir/S28_memory/sp_hde_512x96.lef \
    $tech_dir/S28_memory/sp_hde_512x98.lef \
    $tech_dir/S28_memory/sp_hde_8192x128.lef \
    $tech_dir/S28_memory/sp_hde_8192x32.lef]
set lib_ss0p9_125c_liberty_files [list \
    $tech_dir/scc28nhkcp_hsc30p140_rvt_ss_v0p9_125c_ccs.lib \
    $tech_dir/S28_memory/sp_hde_1024x128_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_1024x144_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_1024x32_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_1024x59_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_1024x64_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_1024x92_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_16384x128_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_2048x128_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_2048x144_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_2048x32_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_2048x59_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_2048x88_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_32768x64_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_4096x128_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_4096x144_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_4096x32_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_4096x84_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x100_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x104_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x108_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x144_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x16_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x22_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x23_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x44_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x52_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x54_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x59_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x7_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x84_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x96_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x98_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_8192x128_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_8192x32_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn]
set lib_ss0p9_40c_liberty_files [list \
    $tech_dir/scc28nhkcp_hsc30p140_rvt_ss_v0p9_-40c_ccs.lib \
    $tech_dir/S28_memory/sp_hde_1024x128_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_1024x144_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_1024x32_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_1024x59_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_1024x64_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_1024x92_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_16384x128_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_2048x128_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_2048x144_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_2048x32_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_2048x59_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_2048x88_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_32768x64_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_4096x128_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_4096x144_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_4096x32_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_4096x84_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x100_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x104_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x108_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x144_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x16_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x22_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x23_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x44_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x52_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x54_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x59_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x7_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x84_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x96_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x98_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_8192x128_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_8192x32_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn]
set lib_ff1p05_125c_liberty_files [list \
    $tech_dir/scc28nhkcp_hsc30p140_rvt_ff_v1p05_125c_ccs.lib \
    $tech_dir/S28_memory/sp_hde_1024x128_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_1024x144_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_1024x32_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_1024x59_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_1024x64_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_1024x92_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_16384x128_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_2048x128_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_2048x144_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_2048x32_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_2048x59_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_2048x88_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_32768x64_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_4096x128_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_4096x144_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_4096x32_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_4096x84_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x100_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x104_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x108_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x144_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x16_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x22_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x23_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x44_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x52_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x54_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x59_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x7_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x84_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x96_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x98_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_8192x128_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_8192x32_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn]
set lib_ff1p05_40c_liberty_files [list \
    $tech_dir/scc28nhkcp_hsc30p140_rvt_ff_v1p05_-40c_ccs.lib \
    $tech_dir/S28_memory/sp_hde_1024x128_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_1024x144_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_1024x32_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_1024x59_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_1024x64_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_1024x92_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_16384x128_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_2048x128_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_2048x144_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_2048x32_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_2048x59_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_2048x88_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_32768x64_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_4096x128_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_4096x144_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_4096x32_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_4096x84_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x100_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x104_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x108_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x144_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x16_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x22_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x23_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x44_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x52_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x54_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x59_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x7_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x84_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x96_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_512x98_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_8192x128_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/S28_memory/sp_hde_8192x32_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn]
set liberty_files [concat $lib_ss0p9_125c_liberty_files $lib_ss0p9_40c_liberty_files $lib_ff1p05_125c_liberty_files $lib_ff1p05_40c_liberty_files]

set verilog_files [list $design_dir/route.v.gz]
set def_file $design_dir/route.def.gz
set sdc_files [list $design_dir/route.sdc]
set utilization 0.65
set clocks {CPU_CLK JTG_CLK}
set period {1 20}
set scan_chain_flag 1
