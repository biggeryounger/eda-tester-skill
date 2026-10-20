create_library_set -name slow -timing $slow_liberty_files
create_library_set -name fast -timing $fast_liberty_files

create_rc_corner -name corner_typical
create_constraint_mode -name func_max_mode -sdc_files $sdc_files
create_constraint_mode -name func_min_mode -sdc_files $sdc_files
create_delay_corner -name wc -late_library_set slow -early_library_set fast -rc_corner corner_typical
create_delay_corner -name bc -late_library_set slow -early_library_set fast -rc_corner corner_typical
create_analysis_view -name func_wc -constraint_mode func_max_mode -delay_corner wc
create_analysis_view -name func_bc -constraint_mode func_min_mode -delay_corner bc
#set_analysis_view_status -view func_wc -active true -setup true -hold false
#set_analysis_view_status -view func_bc -active true -setup false -hold true
set_analysis_view -hold {func_bc} -setup {func_wc}