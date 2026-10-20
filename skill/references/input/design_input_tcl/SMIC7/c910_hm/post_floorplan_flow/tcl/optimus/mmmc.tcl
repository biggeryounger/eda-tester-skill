
create_lib_set -name libset_cworst_ccworst_T \
    -timing_lib $libset_cworst_ccworst_t_liberty_files

create_lib_set -name libset_cbest_ccbest_T \
    -timing_lib $libset_cbest_ccbest_t_liberty_files

create_rc_corner -name corner_cworst_ccworst_T \
    -rc_tech $cworst_rc_tech_file

create_rc_corner -name corner_cbest_ccbest_T \
    -rc_tech $cbest_rc_tech_file

create_analysis_corner -name analysis_corner_cworst_ccworst_T \
    -rc_corner corner_cworst_ccworst_T \
    -lib_set libset_cworst_ccworst_T

create_analysis_corner -name analysis_corner_cbest_ccbest_T \
    -rc_corner corner_cbest_ccbest_T \
    -lib_set libset_cbest_ccbest_T

create_analysis_mode -name func_mode -constraint_file $sdc_files

create_analysis_view -name func_ssgnp0p765v_m40c -analysis_mode func_mode -analysis_corner analysis_corner_cworst_ccworst_T
create_analysis_view -name func_ffgnp0p935v_125c -analysis_mode func_mode -analysis_corner analysis_corner_cbest_ccbest_T

set_views_status -hold {func_ffgnp0p935v_125c} -setup {func_ssgnp0p765v_m40c}
