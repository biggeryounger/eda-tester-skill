create_library_set -name slowlib -timing $slowlib_liberty_files
create_library_set -name fastlib -timing $fastlib_liberty_files
create_rc_corner -name tech_slow
create_rc_corner -name tech_fast
create_constraint_mode -name func -sdc_files $sdc_files

create_delay_corner -name wc -late_library_set slowlib -early_library_set fastlib  -rc_corner tech_slow
create_delay_corner -name bc -late_library_set slowlib -early_library_set fastlib  -rc_corner tech_fast

create_analysis_view -name func_wc -constraint_mode func -delay_corner wc
create_analysis_view -name func_bc -constraint_mode func -delay_corner bc

set_analysis_view -hold {func_bc} -setup {func_wc}
