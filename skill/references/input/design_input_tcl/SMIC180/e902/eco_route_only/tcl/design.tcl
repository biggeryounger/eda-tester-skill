# Design identity and canonical input roots.
set design_name   e902
set tech_name     SMIC180
set init_top_name openE902
set design_dir "$env(PV_ROOT)/svn/openedi/design_data/SMIC180/Itools21.1_Ifp_util0.65/$design_name"
set tech_dir   "$env(PV_ROOT)/svn/openedi/large/SMIC180_new/smic180_library"

set power_net  VDD
set ground_net GND

set lef_files [list \
    $tech_dir/smic18_6lm_0202_ndr.lef]
set slow_liberty_files [list \
    $tech_dir/slow.lib]
set fast_liberty_files [list \
    $tech_dir/fast.lib]
set liberty_files [concat $slow_liberty_files $fast_liberty_files]


set verilog_files [list $design_dir/for_ecoroute.v.gz]
set def_file      $design_dir/for_ecoroute.def.gz
set sdc_files     [list $design_dir/for_ecoroute.sdc]
