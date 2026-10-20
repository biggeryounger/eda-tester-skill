
create_lib_set -name libset_rcworst \
    -timing_lib $libset_rcworst_liberty_files

create_rc_corner -name corner_rcworst \
    -rc_tech $design_dir/../rc_tech/rcworst/optimus_rc.enTech

create_analysis_corner -name delay_corner_rcworst \
    -rc_corner corner_rcworst \
    -early_lib_set libset_rcworst \
    -late_lib_set libset_rcworst

create_analysis_mode -name func_mode -constraint_file $sdc_files

create_analysis_view -name func_ssg0p81v_-40c -analysis_mode func_mode -analysis_corner delay_corner_rcworst

set_views_status -hold {func_ssg0p81v_-40c} -setup {func_ssg0p81v_-40c}
