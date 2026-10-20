# Two-library, one-RC-corner model preserved from the source SMIC180 cases.
create_lib_set -name libset_slow -timing_lib $slow_liberty_files
create_lib_set -name libset_fast -timing_lib $fast_liberty_files

create_rc_corner -name rc_corner_typical

create_analysis_corner -name analysis_corner_setup -rc_corner rc_corner_typical -late_lib_set libset_slow -early_lib_set libset_fast
create_analysis_corner -name analysis_corner_hold -rc_corner rc_corner_typical -late_lib_set libset_slow -early_lib_set libset_fast

create_analysis_mode -name mode_setup -constraint_file $sdc_files
create_analysis_mode -name mode_hold -constraint_file $sdc_files
create_analysis_view -name view_setup -analysis_mode mode_setup -analysis_corner analysis_corner_setup
create_analysis_view -name view_hold -analysis_mode mode_hold -analysis_corner analysis_corner_hold
set_views_status -hold {view_hold} -setup {view_setup}
