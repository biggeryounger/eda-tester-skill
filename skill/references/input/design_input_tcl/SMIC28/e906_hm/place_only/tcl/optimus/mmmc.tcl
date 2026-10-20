# Four-corner MMMC model; setup/hold roles are preserved from the source cases.
create_lib_set -name libset_cworst -timing_lib $cworst_liberty_files
create_lib_set -name libset_rcworst -timing_lib $rcworst_liberty_files
create_lib_set -name libset_cbest -timing_lib $cbest_liberty_files
create_lib_set -name libset_rcbest -timing_lib $rcbest_liberty_files

create_rc_corner -name rc_corner_cworst -rc_tech $cworst_rc_tech_file
create_rc_corner -name rc_corner_rcworst -rc_tech $rcworst_rc_tech_file
create_rc_corner -name rc_corner_cbest -rc_tech $cbest_rc_tech_file
create_rc_corner -name rc_corner_rcbest -rc_tech $rcbest_rc_tech_file

create_analysis_corner -name analysis_corner_cworst -rc_corner rc_corner_cworst -late_lib_set libset_cworst -early_lib_set libset_cbest
create_analysis_corner -name analysis_corner_rcworst -rc_corner rc_corner_rcworst -late_lib_set libset_rcworst -early_lib_set libset_rcbest
create_analysis_corner -name analysis_corner_cbest -rc_corner rc_corner_cbest -late_lib_set libset_cworst -early_lib_set libset_cbest
create_analysis_corner -name analysis_corner_rcbest -rc_corner rc_corner_rcbest -late_lib_set libset_rcworst -early_lib_set libset_rcbest

create_analysis_mode -name mode_setup -constraint_file $sdc_files
create_analysis_mode -name mode_hold -constraint_file $sdc_files
create_analysis_view -name view_setup_cworst -analysis_mode mode_setup -analysis_corner analysis_corner_cworst
create_analysis_view -name view_setup_rcworst -analysis_mode mode_setup -analysis_corner analysis_corner_rcworst
create_analysis_view -name view_hold_cbest -analysis_mode mode_hold -analysis_corner analysis_corner_cbest
create_analysis_view -name view_hold_rcbest -analysis_mode mode_hold -analysis_corner analysis_corner_rcbest
set_views_status -hold {view_hold_cbest view_hold_rcbest} -setup {view_setup_cworst view_setup_rcworst}
