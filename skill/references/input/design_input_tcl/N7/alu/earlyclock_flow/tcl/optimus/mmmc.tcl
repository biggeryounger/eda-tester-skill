
create_lib_set -name libset_cworst_ccworst_T \
	-timing_lib \
	[list $lib_dir/lib/std/ssgnp_0p765v_m40c/tcbn07_bwph240l8p57pd_base_lvtssgnp_0p765v_m40c_cworst_CCworst_T_ccs.lib.gz]

create_lib_set -name libset_cbest_ccbest_T \
	-timing_lib \
	[list $lib_dir/lib/std/ffgnp_0p935v_125c/tcbn07_bwph240l8p57pd_base_lvtffgnp_0p935v_125c_cbest_CCbest_T_ccs.lib.gz]

create_rc_corner -name corner_cworst_ccworst_T \
	-rc_tech $worst_rc_tech

create_rc_corner -name corner_cbest_ccbest_T \
	-rc_tech $best_rc_tech

create_analysis_corner -name analysis_corner_cworst_ccworst_T \
	-rc_corner corner_cworst_ccworst_T \
	-lib_set libset_cworst_ccworst_T

create_analysis_corner -name analysis_corner_cbest_ccbest_T \
	-rc_corner corner_cbest_ccbest_T \
	-lib_set libset_cbest_ccbest_T

create_analysis_mode -name func_mode -constraint_file $design_dir/sdc/alu.syn.sdc

create_analysis_view -name func_ssgnp0p765v_m40c -analysis_mode func_mode -analysis_corner analysis_corner_cworst_ccworst_T
create_analysis_view -name func_ffgnp0p935v_125c -analysis_mode func_mode -analysis_corner analysis_corner_cbest_ccbest_T

set_analysis_view_status -view func_ssgnp0p765v_m40c -active true -setup true -hold false
set_analysis_view_status -view func_ffgnp0p935v_125c -active true -setup false -hold true
