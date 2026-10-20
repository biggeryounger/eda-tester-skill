create_rc_corner -name tech_slow
create_rc_corner -name tech_fast
create_analysis_mode -name func -constraint_file $sdc_files
create_lib_set -name slowLibSet_40c -timing_lib $slowlibset_40c_liberty_files
create_lib_set -name slowLibSet_125c -timing_lib $slowlibset_125c_liberty_files
create_lib_set -name fastLibSet_0c -timing_lib $fastlibset_0c_liberty_files

create_analysis_corner -name wc_125 -late_lib_set slowLibSet_125c -early_lib_set fastLibSet_0c -rc_corner tech_slow
create_analysis_corner -name wc_-40 -late_lib_set slowLibSet_40c -early_lib_set fastLibSet_0c -rc_corner tech_slow
create_analysis_corner -name bc_125 -late_lib_set slowLibSet_125c -early_lib_set fastLibSet_0c  -rc_corner tech_fast
create_analysis_corner -name bc_-40 -late_lib_set slowLibSet_40c -early_lib_set fastLibSet_0c -rc_corner tech_fast

create_analysis_view -name func_wc_125 -analysis_mode func -analysis_corner wc_125
create_analysis_view -name func_wc_-40 -analysis_mode func -analysis_corner wc_-40
create_analysis_view -name func_bc_125 -analysis_mode func -analysis_corner bc_125
create_analysis_view -name func_bc_-40 -analysis_mode func -analysis_corner bc_-40

set_views_status -hold {func_bc_125 func_bc_-40} -setup {func_wc_125 func_wc_-40}
