set design_dir "$env(PV_ROOT)/svn/openedi/design_data/SMIC180/Itools21.1_Ifp_util0.65/e902"
set tech_dir "$env(PV_ROOT)/svn/openedi/large/SMIC180_new/smic180_library"

# top design name (itools default var)
set top_name openE902

#lef_file
set lef_files "$tech_dir/smic18_6lm_0202_ndr.lef"

#netlist
set netlist $design_dir/place.v.gz
set def $design_dir/place.def.gz

