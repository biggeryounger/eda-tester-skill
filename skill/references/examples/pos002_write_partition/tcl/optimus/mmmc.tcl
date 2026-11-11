create_lib_set -name libset_fast \
	-timing_lib \
	[list $tech_dir/fast.lib]
create_lib_set -name libset_slow \
	-timing_lib \
	[list $tech_dir/slow.lib]
create_rc_corner -name corner_typical
create_analysis_corner -name delay_corner_slow_CMAX \
	-rc_corner corner_typical \
	-early_lib_set libset_fast \
	-late_lib_set libset_slow
create_analysis_corner -name delay_corner_fast_CMIN \
	-rc_corner corner_typical \
	-early_lib_set libset_fast \
	-late_lib_set libset_slow
create_analysis_mode -name func_mode -constraint_file $design_dir/floorplan.sdc

create_analysis_view -name func_slow_CMAX -analysis_mode func_mode -analysis_corner delay_corner_slow_CMAX
create_analysis_view -name func_fast_CMIN -analysis_mode func_mode -analysis_corner delay_corner_fast_CMIN

set_views_status -hold {func_fast_CMIN} -setup {func_slow_CMAX}
