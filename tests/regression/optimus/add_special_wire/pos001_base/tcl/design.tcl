set design_dir "$env(PV_ROOT)/svn/openedi/design_data/SMIC28/Itools21.1_Ifp_util0.65/riscv_core"
set tech_dir "$env(PV_ROOT)/svn/openedi/design_data/SMIC28/smic28_library"

set max_threads 1
set init_top_cell riscv_core
set lef_files [list \
    "$tech_dir/scc28n_12t25od33_1p8m_7ic_1tmc_alpa1_WITH_NDR.lef" \
    "$tech_dir/scc28nhkcp_hsc30p140_rvt_ant.lef"]
set netlist_file "$design_dir/floorplan.v.gz"
set def_file "$design_dir/floorplan.def.gz"
set power_net VDD
set ground_net VSS
