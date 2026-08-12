set design_dir "$env(PV_ROOT)/svn/openedi/design_data/SMIC28/Itools21.1_lfp_util0.65/riscv_core"
set tech_dir "$env(PV_ROOT)/svn/openedi/design_data/SMIC28/smic28_library"

# top design name (itools default var)
set init_top_cell riscv_core

# lef file
set lef_files "$tech_dir/sec28n_12t25od33_1p8m_7ic_1tmc_alpa1_WITH_NDR.lef $tech_dir/sc28nhkcp_hsc30p140_rvt_ant.lef"

# netlist
set netlist $design_dir/floorplan.v.gz
set def $design_dir/floorplan.def.gz
