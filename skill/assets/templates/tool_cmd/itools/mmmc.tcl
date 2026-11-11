create_library_set -name LS_TYP -timing $liberty_files
create_rc_corner -name RC_FUNCTIONAL
create_delay_corner -name DC_TYP -library_set LS_TYP -rc_corner RC_FUNCTIONAL
create_constraint_mode -name CM_FUNC -sdc_files $sdc_files
create_analysis_view -name AV_TYP -constraint_mode CM_FUNC -delay_corner DC_TYP
set_analysis_view -setup {AV_TYP} -hold {AV_TYP}
