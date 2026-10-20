create_rc_corner -name tech_slow
create_rc_corner -name tech_fast
create_constraint_mode -name func -sdc_files $sdc_files
create_library_set -name slowLibSet_40c -timing $slowlibset_40c_liberty_files
create_library_set -name slowLibSet_125c -timing $slowlibset_125c_liberty_files
create_library_set -name fastLibSet_0c -timing $fastlibset_0c_liberty_files

create_delay_corner -name wc_125 -late_library_set slowLibSet_125c -early_library_set fastLibSet_0c -rc_corner tech_slow
create_delay_corner -name wc_-40 -late_library_set slowLibSet_40c -early_library_set fastLibSet_0c -rc_corner tech_slow
create_delay_corner -name bc_125 -late_library_set slowLibSet_125c -early_library_set fastLibSet_0c  -rc_corner tech_fast
create_delay_corner -name bc_-40 -late_library_set slowLibSet_40c -early_library_set fastLibSet_0c -rc_corner tech_fast

create_analysis_view -name func_wc_125 -constraint_mode func -delay_corner wc_125
create_analysis_view -name func_wc_-40 -constraint_mode func -delay_corner wc_-40
create_analysis_view -name func_bc_125 -constraint_mode func -delay_corner bc_125
create_analysis_view -name func_bc_-40 -constraint_mode func -delay_corner bc_-40

set_analysis_view -hold {func_bc_125 func_bc_-40} -setup {func_wc_125 func_wc_-40}
