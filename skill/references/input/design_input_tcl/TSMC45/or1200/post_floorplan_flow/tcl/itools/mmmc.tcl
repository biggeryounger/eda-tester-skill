create_library_set -name slowlib -timing $slowlib_liberty_files
create_library_set -name fastlib -timing $fastlib_liberty_files
#2 view
create_rc_corner -name corner_RCbest
create_rc_corner -name corner_RCworst

create_delay_corner -name delay_corner_rcbest \
    -rc_corner corner_RCbest \
    -early_library_set fastlib \
    -late_library_set slowlib


create_delay_corner -name delay_corner_rcworst \
    -rc_corner corner_RCworst \
    -early_library_set fastlib \
    -late_library_set slowlib



create_constraint_mode -name func_mode -sdc_files $sdc_files
#2view
create_analysis_view -name func_rcbest -constraint_mode func_mode -delay_corner delay_corner_rcbest
create_analysis_view -name func_rcworst -constraint_mode func_mode -delay_corner delay_corner_rcworst


#2 view
set_analysis_view -hold {func_rcbest} -setup {func_rcworst}
