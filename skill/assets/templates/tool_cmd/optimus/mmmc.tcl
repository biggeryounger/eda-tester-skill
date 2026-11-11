create_lib_set -name LS_TYP -timing_lib $liberty_files
create_rc_corner -name RC_FUNCTIONAL
create_analysis_corner -name DC_TYP -lib_set LS_TYP -rc_corner RC_FUNCTIONAL
create_analysis_mode -name CM_FUNC -constraint_file $sdc_files
create_analysis_view -name AV_TYP -analysis_mode CM_FUNC -analysis_corner DC_TYP
set_views_status -setup {AV_TYP} -hold {AV_TYP}