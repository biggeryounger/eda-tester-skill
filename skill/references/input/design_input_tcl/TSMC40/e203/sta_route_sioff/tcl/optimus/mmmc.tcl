create_lib_set -name slowLib -timing_lib $slowlib_liberty_files
create_lib_set -name fastLib -timing_lib $fastlib_liberty_files

create_rc_corner -name corner_worst_CMAX
create_rc_corner -name corner_fast_CMIN

create_analysis_mode -name func_max_mode -constraint_file $sdc_files
create_analysis_mode -name func_min_mode -constraint_file $sdc_files

create_analysis_corner -name delay_corner_slow_CMAX -late_lib_set slowLib -early_lib_set fastLib -rc_corner corner_worst_CMAX
create_analysis_corner -name delay_corner_fast_CMIN -late_lib_set slowLib -early_lib_set fastLib -rc_corner corner_fast_CMIN

create_analysis_view -name func_worst -analysis_mode func_max_mode -analysis_corner delay_corner_slow_CMAX
create_analysis_view -name func_best -analysis_mode func_min_mode -analysis_corner delay_corner_fast_CMIN

set_views_status -hold {func_best} -setup {func_worst}
