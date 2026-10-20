create_library_set -name slowlib -timing $slowlib_liberty_files
create_library_set -name fastlib -timing $fastlib_liberty_files

create_rc_corner -name corner_rcworst
create_rc_corner -name corner_rcbest

create_delay_corner -name delay_corner_rcworst \
    -rc_corner corner_rcworst \
    -early_library_set fastlib \
    -late_library_set slowlib
create_delay_corner -name delay_corner_rcbest \
    -rc_corner corner_rcbest \
    -early_library_set fastlib \
    -late_library_set slowlib
create_constraint_mode -name func_mode -sdc_files $sdc_files

create_analysis_view -name func_rcworst -constraint_mode func_mode -delay_corner delay_corner_rcworst
create_analysis_view -name func_rcbest  -constraint_mode func_mode -delay_corner delay_corner_rcbest
set_analysis_view -hold {func_rcbest} -setup {func_rcworst}
