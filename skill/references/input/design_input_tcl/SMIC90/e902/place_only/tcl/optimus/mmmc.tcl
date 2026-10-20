create_lib_set -name slowlib -timing_lib $slowlib_liberty_files
create_lib_set -name fastlib -timing_lib $fastlib_liberty_files

create_rc_corner -name corner_rcworst
create_rc_corner -name corner_rcbest

create_analysis_corner -name delay_corner_rcworst \
    -rc_corner corner_rcworst \
    -early_lib_set fastlib \
    -late_lib_set slowlib
create_analysis_corner -name delay_corner_rcbest \
    -rc_corner corner_rcbest \
    -early_lib_set fastlib \
    -late_lib_set slowlib
create_analysis_mode -name func_mode -constraint_file $sdc_files

create_analysis_view -name func_rcworst -analysis_mode func_mode -analysis_corner delay_corner_rcworst
create_analysis_view -name func_rcbest  -analysis_mode func_mode -analysis_corner delay_corner_rcbest
set_views_status -hold {func_rcbest} -setup {func_rcworst}
