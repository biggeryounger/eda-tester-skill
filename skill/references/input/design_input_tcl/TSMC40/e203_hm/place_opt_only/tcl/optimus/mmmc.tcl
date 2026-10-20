create_lib_set -name slowlib -timing_lib $slow_liberty_files
create_lib_set -name fastlib -timing_lib $fast_liberty_files
create_rc_corner -name tech_slow
create_rc_corner -name tech_fast
create_analysis_mode -name func -constraint_file $sdc_files

create_analysis_corner -name wc -late_lib_set slowlib -early_lib_set fastlib  -rc_corner tech_slow
create_analysis_corner -name bc -late_lib_set slowlib -early_lib_set fastlib  -rc_corner tech_fast

create_analysis_view -name func_wc -analysis_mode func -analysis_corner wc
create_analysis_view -name func_bc -analysis_mode func -analysis_corner bc

set_views_status -hold {func_bc} -setup {func_wc}
