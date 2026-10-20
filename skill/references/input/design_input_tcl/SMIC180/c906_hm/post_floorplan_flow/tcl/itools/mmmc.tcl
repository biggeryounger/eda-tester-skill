# Two-library, one-RC-corner model preserved from the source SMIC180 cases.
create_library_set -name libset_slow -timing $slow_liberty_files
create_library_set -name libset_fast -timing $fast_liberty_files

create_rc_corner -name rc_corner_typical

create_delay_corner -name analysis_corner_setup -rc_corner rc_corner_typical -late_library_set libset_slow -early_library_set libset_fast
create_delay_corner -name analysis_corner_hold -rc_corner rc_corner_typical -late_library_set libset_slow -early_library_set libset_fast

create_constraint_mode -name mode_setup -sdc_files $sdc_files
create_constraint_mode -name mode_hold -sdc_files $sdc_files
create_analysis_view -name view_setup -constraint_mode mode_setup -delay_corner analysis_corner_setup
create_analysis_view -name view_hold -constraint_mode mode_hold -delay_corner analysis_corner_hold
set_analysis_view -hold {view_hold} -setup {view_setup}
