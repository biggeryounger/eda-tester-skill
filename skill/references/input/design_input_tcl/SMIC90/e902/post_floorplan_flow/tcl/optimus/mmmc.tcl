create_lib_set -name slowlib -timing_lib $lib_dir/scc90nbcd_hd_rvt_ss_v1p08_125c_ccs.lib
create_lib_set -name fastlib -timing_lib $lib_dir/scc90nbcd_hd_rvt_ff_v1p32_125c_ccs.lib

create_rc_corner -name corner_rcworst
create_rc_corner -name corner_rcbest

create_analysis_corner -name delay_corner_rcworst \
	-rc_corner corner_rcworst \
	-early_lib_set fastlib \
        -late_lib_set slowlib
create_analysis_corner -name delay_corner_rcbest \
	-rc_corner corner_rcbest \
	-early_lib_set fastlib \
        -late_lib_set slowlib
create_analysis_mode -name func_mode -constraint_file $design_dir/floorplan.sdc

create_analysis_view -name func_rcworst -analysis_mode func_mode -analysis_corner delay_corner_rcworst
create_analysis_view -name func_rcbest  -analysis_mode func_mode -analysis_corner delay_corner_rcbest
set_analysis_view_status -view func_rcbest -active true -setup false -hold true
set_analysis_view_status -view func_rcworst -active true -setup true -hold false