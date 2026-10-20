
create_library_set -name libset_rcworst \
    -timing $libset_rcworst_liberty_files

create_rc_corner -name corner_rcworst \
    -qx_tech_file $rc_tech_file

create_delay_corner -name delay_corner_rcworst \
    -rc_corner corner_rcworst \
    -early_library_set libset_rcworst \
    -late_library_set libset_rcworst

create_constraint_mode -name func_mode -sdc_files $sdc_files

create_analysis_view -name func_ssg0p81v_-40c -constraint_mode func_mode -delay_corner delay_corner_rcworst

set_analysis_view -hold {func_ssg0p81v_-40c} -setup {func_ssg0p81v_-40c}
