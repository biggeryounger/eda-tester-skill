create_library_set -name slowLibSet -timing $slowlibset_liberty_files
create_library_set -name fastLibSet -timing $fastlibset_liberty_files

create_constraint_mode -name func_max_mode -sdc_files $sdc_files
create_constraint_mode -name func_min_mode -sdc_files $sdc_files

create_rc_corner -name corner_worst_CMAX
create_rc_corner -name corner_fast_CMIN

create_delay_corner -name wc \
    -early_library_set fastLibSet \
    -late_library_set slowLibSet \
    -rc_corner corner_worst_CMAX
create_delay_corner -name bc \
    -early_library_set fastLibSet \
    -late_library_set slowLibSet \
    -rc_corner corner_fast_CMIN

create_analysis_view -name func_slow_CMAX -constraint_mode func_max_mode -delay_corner wc
create_analysis_view -name func_fast_CMIN -constraint_mode func_min_mode -delay_corner bc

set_analysis_view -hold {func_fast_CMIN} -setup {func_slow_CMAX}
