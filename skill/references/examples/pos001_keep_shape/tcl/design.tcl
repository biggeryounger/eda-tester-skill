set design_dir "$env(PV_ROOT)/svn/openedi/design_data/SMIC28/Itools21.1_Ifp_util0.65/riscv_core"
set tech_dir "$env(PV_ROOT)/svn/openedi/design_data/SMIC28/smic28_library"

# top design name (itools default var)
set top_name riscv_core

#lef_file
set lef_files "$tech_dir/scc28n_12t25od33_1p8m_7ic_1tmc_alpa1_WITH_NDR.lef $tech_dir/scc28nhkcp_hsc30p140_rvt_ant.lef"

#netlist
set netlist $design_dir/floorplan.v.gz

#def
set def $design_dir/floorplan.def.gz
set scan_def $design_dir/scan.def.gz

