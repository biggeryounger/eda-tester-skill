create_lib_set -name fastLibSet -timing_lib $slow_lib
create_lib_set -name slowLibSet -timing_lib $fast_lib

create_rc_corner -name corner_worst_CMAX
create_rc_corner -name corner_fast_CMIN

create_analysis_mode -name func_mode -constraint_file $sdc_file

create_analysis_corner -name delay_corner_slow_CMAX -early_lib_set fastLibSet -late_lib_set slowLibSet -rc_corner corner_worst_CMAX
create_analysis_corner -name delay_corner_fast_CMIN -early_lib_set fastLibSet -late_lib_set slowLibSet -rc_corner corner_fast_CMIN

create_analysis_view -name func_slow_CMAX -analysis_mode func_mode -analysis_corner delay_corner_slow_CMAX
create_analysis_view -name func_fast_CMIN -analysis_mode func_mode -analysis_corner delay_corner_fast_CMIN
set_views_status -setup {func_slow_CMAX} -hold {func_fast_CMIN}
