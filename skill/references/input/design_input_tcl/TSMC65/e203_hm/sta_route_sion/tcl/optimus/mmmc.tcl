create_lib_set -name fastLibSet -timing_lib $fastlibset_liberty_files
create_lib_set -name slowLibSet -timing_lib $slowlibset_liberty_files

create_rc_corner -name corner_fast_CMIN
create_rc_corner -name corner_worst_CMAX

create_analysis_corner  -name delay_corner_rcbest \
                        -late_lib_set slowLibSet \
                        -early_lib_set fastLibSet \
                        -rc_corner corner_fast_CMIN

create_analysis_corner -name delay_corner_rcworst \
                        -late_lib_set slowLibSet \
                        -early_lib_set fastLibSet \
                        -rc_corner corner_worst_CMAX

create_analysis_mode -name func_max_mode -constraint_file $sdc_files
create_analysis_mode -name func_min_mode -constraint_file $sdc_files

create_analysis_view -name func_cbest -analysis_mode func_min_mode -analysis_corner delay_corner_rcbest
create_analysis_view -name func_cworst -analysis_mode func_max_mode -analysis_corner delay_corner_rcworst

set_views_status -hold {func_cbest} -setup {func_cworst}
