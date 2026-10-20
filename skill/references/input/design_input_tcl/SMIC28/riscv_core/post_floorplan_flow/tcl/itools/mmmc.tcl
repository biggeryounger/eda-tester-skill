# Four-corner MMMC model; setup/hold roles are preserved from the source cases.
create_library_set -name libset_cworst -timing $cworst_liberty_files
create_library_set -name libset_rcworst -timing $rcworst_liberty_files
create_library_set -name libset_cbest -timing $cbest_liberty_files
create_library_set -name libset_rcbest -timing $rcbest_liberty_files

create_rc_corner -name rc_corner_cworst -qx_tech_file $cworst_rc_tech_file
create_rc_corner -name rc_corner_rcworst -qx_tech_file $rcworst_rc_tech_file
create_rc_corner -name rc_corner_cbest -qx_tech_file $cbest_rc_tech_file
create_rc_corner -name rc_corner_rcbest -qx_tech_file $rcbest_rc_tech_file

create_delay_corner -name analysis_corner_cworst -rc_corner rc_corner_cworst -late_library_set libset_cworst -early_library_set libset_cbest
create_delay_corner -name analysis_corner_rcworst -rc_corner rc_corner_rcworst -late_library_set libset_rcworst -early_library_set libset_rcbest
create_delay_corner -name analysis_corner_cbest -rc_corner rc_corner_cbest -late_library_set libset_cworst -early_library_set libset_cbest
create_delay_corner -name analysis_corner_rcbest -rc_corner rc_corner_rcbest -late_library_set libset_rcworst -early_library_set libset_rcbest

create_constraint_mode -name mode_setup -sdc_files $sdc_files
create_constraint_mode -name mode_hold -sdc_files $sdc_files
create_analysis_view -name view_setup_cworst -constraint_mode mode_setup -delay_corner analysis_corner_cworst
create_analysis_view -name view_setup_rcworst -constraint_mode mode_setup -delay_corner analysis_corner_rcworst
create_analysis_view -name view_hold_cbest -constraint_mode mode_hold -delay_corner analysis_corner_cbest
create_analysis_view -name view_hold_rcbest -constraint_mode mode_hold -delay_corner analysis_corner_rcbest
set_analysis_view -hold {view_hold_cbest view_hold_rcbest} -setup {view_setup_cworst view_setup_rcworst}
