create_lib_set -name slow -timing_lib $slow_liberty_files
create_lib_set -name fast -timing_lib $fast_liberty_files

create_rc_corner -name corner_typical
create_analysis_mode -name func_max_mode -constraint_file $sdc_files
create_analysis_mode -name func_min_mode -constraint_file $sdc_files
create_analysis_corner -name wc -late_lib_set slow -early_lib_set fast -rc_corner corner_typical
create_analysis_corner -name bc -late_lib_set slow -early_lib_set fast -rc_corner corner_typical
create_analysis_view -name func_wc -analysis_mode func_max_mode -analysis_corner wc
create_analysis_view -name func_bc -analysis_mode func_min_mode -analysis_corner bc
#set_analysis_view_status -view func_wc -active true -setup true -hold false
#set_analysis_view_status -view func_bc -active true -setup false -hold true
set_views_status -hold {func_bc} -setup {func_wc}