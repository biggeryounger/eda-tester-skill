create_lib_set -name slowLib -timing_lib $slowlib_liberty_files
create_lib_set -name fastLib -timing_lib $fastlib_liberty_files

create_rc_corner -name corner_worst_CMAX
create_rc_corner -name corner_fast_CMIN

create_analysis_mode -name func_max_mode -constraint_file $sdc_files
create_analysis_mode -name func_min_mode -constraint_file $sdc_files

create_analysis_corner -name wc -early_lib_set fastLib -late_lib_set slowLib -rc_corner corner_worst_CMAX
create_analysis_corner -name bc -early_lib_set fastLib -late_lib_set slowLib -rc_corner corner_fast_CMIN

create_analysis_view -name func_slow_CMAX -analysis_mode func_max_mode -analysis_corner wc
create_analysis_view -name func_fast_CMIN -analysis_mode func_min_mode -analysis_corner bc

set_views_status -hold {func_fast_CMIN} -setup {func_slow_CMAX}
