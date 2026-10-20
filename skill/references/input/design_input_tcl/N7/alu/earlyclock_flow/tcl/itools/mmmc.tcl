
create_library_set -name libset_cworst_ccworst_T \
	-timing \
	[list $lib_dir/lib/std/ssgnp_0p765v_m40c/tcbn07_bwph240l8p57pd_base_lvtssgnp_0p765v_m40c_cworst_CCworst_T_ccs.lib.gz]

create_library_set -name libset_cbest_ccbest_T \
	-timing \
	[list $lib_dir/lib/std/ffgnp_0p935v_125c/tcbn07_bwph240l8p57pd_base_lvtffgnp_0p935v_125c_cbest_CCbest_T_ccs.lib.gz]

create_rc_corner -name corner_cworst_ccworst_T \
	-qx_tech_file $worst_rc_tech

create_rc_corner -name corner_cbest_ccbest_T \
	-qx_tech_file $best_rc_tech

create_delay_corner -name analysis_corner_cworst_ccworst_T \
	-rc_corner corner_cworst_ccworst_T \
	-library_set libset_cworst_ccworst_T

create_delay_corner -name analysis_corner_cbest_ccbest_T \
	-rc_corner corner_cbest_ccbest_T \
	-library_set libset_cbest_ccbest_T

create_constraint_mode -name func_mode -sdc_files $design_dir/sdc/alu.syn.sdc

create_analysis_view -name func_ssgnp0p765v_m40c -constraint_mode func_mode -delay_corner analysis_corner_cworst_ccworst_T
create_analysis_view -name func_ffgnp0p935v_125c -constraint_mode func_mode -delay_corner analysis_corner_cbest_ccbest_T

set_analysis_view -setup func_ssgnp0p765v_m40c -hold func_ffgnp0p935v_125c
