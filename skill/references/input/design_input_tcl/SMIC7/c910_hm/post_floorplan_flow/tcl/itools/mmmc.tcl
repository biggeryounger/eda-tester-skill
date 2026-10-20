
create_library_set -name libset_cworst_ccworst_T \
    -timing $libset_cworst_ccworst_t_liberty_files

create_library_set -name libset_cbest_ccbest_T \
    -timing $libset_cbest_ccbest_t_liberty_files

create_rc_corner -name corner_cworst_ccworst_T \
    -qx_tech_file $cworst_rc_tech_file

create_rc_corner -name corner_cbest_ccbest_T \
    -qx_tech_file $cbest_rc_tech_file

create_delay_corner -name analysis_corner_cworst_ccworst_T \
    -rc_corner corner_cworst_ccworst_T \
    -library_set libset_cworst_ccworst_T

create_delay_corner -name analysis_corner_cbest_ccbest_T \
    -rc_corner corner_cbest_ccbest_T \
    -library_set libset_cbest_ccbest_T

create_constraint_mode -name func_mode -sdc_files $sdc_files

create_analysis_view -name func_ssgnp0p765v_m40c -constraint_mode func_mode -delay_corner analysis_corner_cworst_ccworst_T
create_analysis_view -name func_ffgnp0p935v_125c -constraint_mode func_mode -delay_corner analysis_corner_cbest_ccbest_T

set_analysis_view -hold {func_ffgnp0p935v_125c} -setup {func_ssgnp0p765v_m40c}
