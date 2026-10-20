# Design identity and canonical input roots.
set design_name   c910_hm
set tech_name     SMIC28
set init_top_name openC910
set design_dir "$env(PV_ROOT)/svn/openedi/design_data/SMIC28/Itools21.1_Ifp_util0.65/$design_name"
set tech_dir   "$env(PV_ROOT)/svn/openedi/design_data/SMIC28/smic28_library"

set power_net  VDD
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
set cworst_liberty_files [list \
    $tech_dir/scc28nhkcp_hsc30p140_rvt_ss_v0p9_125c_ccs.lib \
    $tech_dir/s28_mem/lib/sp_hde_1024x128_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_1024x144_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_1024x32_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_1024x59_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_1024x64_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_1024x92_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_16384x128_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_2048x128_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_2048x144_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_2048x32_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_2048x59_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_2048x88_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_32768x64_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_4096x128_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_4096x144_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_4096x32_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_4096x84_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x100_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x104_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x108_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x144_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x16_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x22_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x23_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x44_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x52_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x54_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x59_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x7_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x84_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x96_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x98_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_8192x128_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_8192x32_ssg_cworstt_0p90v_0p90v_125c.lib_ccs_tn]
set rcworst_liberty_files [list \
    $tech_dir/scc28nhkcp_hsc30p140_rvt_ss_v0p9_-40c_ccs.lib \
    $tech_dir/s28_mem/lib/sp_hde_1024x128_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_1024x144_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_1024x32_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_1024x59_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_1024x64_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_1024x92_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_16384x128_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_2048x128_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_2048x144_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_2048x32_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_2048x59_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_2048x88_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_32768x64_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_4096x128_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_4096x144_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_4096x32_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_4096x84_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x100_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x104_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x108_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x144_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x16_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x22_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x23_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x44_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x52_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x54_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x59_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x7_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x84_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x96_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x98_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_8192x128_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_8192x32_ssg_cworstt_0p90v_0p90v_m40c.lib_ccs_tn]
set cbest_liberty_files [list \
    $tech_dir/scc28nhkcp_hsc30p140_rvt_ff_v1p05_125c_ccs.lib \
    $tech_dir/s28_mem/lib/sp_hde_1024x128_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_1024x144_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_1024x32_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_1024x59_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_1024x64_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_1024x92_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_16384x128_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_2048x128_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_2048x144_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_2048x32_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_2048x59_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_2048x88_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_32768x64_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_4096x128_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_4096x144_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_4096x32_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_4096x84_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x100_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x104_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x108_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x144_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x16_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x22_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x23_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x44_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x52_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x54_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x59_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x7_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x84_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x96_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x98_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_8192x128_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_8192x32_ff_cbestt_1p05v_1p05v_125c.lib_ccs_tn]
set rcbest_liberty_files [list \
    $tech_dir/scc28nhkcp_hsc30p140_rvt_ff_v1p05_-40c_ccs.lib \
    $tech_dir/s28_mem/lib/sp_hde_1024x128_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_1024x144_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_1024x32_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_1024x59_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_1024x64_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_1024x92_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_16384x128_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_2048x128_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_2048x144_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_2048x32_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_2048x59_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_2048x88_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_32768x64_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_4096x128_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_4096x144_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_4096x32_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_4096x84_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x100_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x104_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x108_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x144_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x16_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x22_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x23_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x44_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x52_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x54_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x59_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x7_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x84_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x96_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_512x98_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_8192x128_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn \
    $tech_dir/s28_mem/lib/sp_hde_8192x32_ff_cbestt_1p05v_1p05v_m40c.lib_ccs_tn]
set liberty_files [concat $cworst_liberty_files $rcworst_liberty_files $cbest_liberty_files $rcbest_liberty_files]

switch -- $PV_TOOL {
    optimus {
    set cworst_rc_tech_file  $tech_dir/hsc30p140_rvt_ss_v0p9_125c.enTech
    set rcworst_rc_tech_file $tech_dir/hsc30p140_rvt_ss_v0p9_-40c.enTech
    set cbest_rc_tech_file   $tech_dir/hsc30p140_rvt_ff_v1p05_125c.enTech
    set rcbest_rc_tech_file  $tech_dir/hsc30p140_rvt_ff_v1p05_-40c.enTech
    }
itools {
    set cworst_rc_tech_file  $tech_dir/hsc30p140_rvt_ss_v0p9_125c.qrcTech
set rcworst_rc_tech_file $tech_dir/hsc30p140_rvt_ss_v0p9_-40c.qrcTech
set cbest_rc_tech_file   $tech_dir/hsc30p140_rvt_ff_v1p05_125c.qrcTech
set rcbest_rc_tech_file  $tech_dir/hsc30p140_rvt_ff_v1p05_-40c.qrcTech
}
default { error "Unsupported PV_TOOL: $PV_TOOL" }
}
set rc_tech_file $rcworst_rc_tech_file

set verilog_files [list $design_dir/prects.v.gz]
set def_file      $design_dir/prects.def.gz
set sdc_files     [list $design_dir/prects.sdc]
