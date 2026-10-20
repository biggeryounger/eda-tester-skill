
create_lib_set -name libset_cworst_ccworst_T \
	-timing_lib \
	[list $lib_dir/tcbn07_bwph300l8p64pd_base_lvtffgnp_0p715v_0c_cbest_CCbest_T_ccs.lib.gz \
			$lib_dir/tcbn07_bwph300l8p64pd_base_svtffgnp_0p715v_0c_cbest_CCbest_T_ccs.lib.gz \
			$lib_dir/tcbn07_bwph300l8p64pd_lvl_lvtffgnp_0p715v_0p715v_0c_cbest_CCbest_T_ccs.lib.gz \
			$lib_dir/tcbn07_bwph300l8p64pd_lvl_svtffgnp_0p715v_0p715v_0c_cbest_CCbest_T_ccs.lib.gz \
			$lib_dir/tcbn07_bwph300l8p64pd_pm_lvtffgnp_0p715v_0c_cbest_CCbest_T_ccs.lib.gz \
			$lib_dir/tcbn07_bwph300l8p64pd_pm_svtffgnp_0p715v_0c_cbest_CCbest_T_ccs.lib.gz]

create_lib_set -name libset_cbest_ccbest_T \
	-timing_lib \
	[list $lib_dir/tcbn07_bwph300l8p64pd_base_lvtssgnp_0p585v_0c_cworst_CCworst_T_ccs.lib.gz \
			$lib_dir/tcbn07_bwph300l8p64pd_base_svtssgnp_0p585v_0c_cworst_CCworst_T_ccs.lib.gz \
			$lib_dir/tcbn07_bwph300l8p64pd_lvl_lvtssgnp_0p585v_0p585v_0c_cworst_CCworst_T_ccs.lib.gz \
			$lib_dir/tcbn07_bwph300l8p64pd_lvl_svtssgnp_0p585v_0p585v_0c_cworst_CCworst_T_ccs.lib.gz \
			$lib_dir/tcbn07_bwph300l8p64pd_pm_lvtssgnp_0p585v_0c_cworst_CCworst_T_ccs.lib.gz \
			$lib_dir/tcbn07_bwph300l8p64pd_pm_svtssgnp_0p585v_0c_cworst_CCworst_T_ccs.lib.gz]

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

create_analysis_mode -name func_mode -constraint_file $design_dir/e902_fp.sdc

create_analysis_view -name func_ssgnp0p765v_m40c -analysis_mode func_mode -analysis_corner analysis_corner_cworst_ccworst_T
create_analysis_view -name func_ffgnp0p935v_125c -analysis_mode func_mode -analysis_corner analysis_corner_cbest_ccbest_T

set_analysis_view_status -view func_ssgnp0p765v_m40c -active true -setup true -hold false
set_analysis_view_status -view func_ffgnp0p935v_125c -active true -setup false -hold true
