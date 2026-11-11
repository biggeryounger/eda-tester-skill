create_library_set -name fastLibSet -timing $slow_lib
create_library_set -name slowLibSet -timing $fast_lib

create_rc_corner -name corner_worst_CMAX
create_rc_corner -name corner_fast_CMIN

create_constraint_mode -name func_mode -sdc_files $sdc_file

create_delay_corner -name delay_corner_slow_CMAX -early_library_set fastLibSet -late_library_set slowLibSet -rc_corner corner_worst_CMAX
create_delay_corner -name delay_corner_fast_CMIN -early_library_set fastLibSet -late_library_set slowLibSet -rc_corner corner_fast_CMIN

create_analysis_view -name func_slow_CMAX -constraint_mode func_mode -delay_corner delay_corner_slow_CMAX
create_analysis_view -name func_fast_CMIN -constraint_mode func_mode -delay_corner delay_corner_fast_CMIN
set_analysis_view -setup {func_slow_CMAX} -hold {func_fast_CMIN}
