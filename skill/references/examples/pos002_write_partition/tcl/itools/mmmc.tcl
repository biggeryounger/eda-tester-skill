create_library_set -name libset_fast \
	-timing \
	[list $tech_dir/fast.lib]
create_library_set -name libset_slow \
	-timing \
	[list $tech_dir/slow.lib]
create_rc_corner -name corner_typical
create_delay_corner -name delay_corner_slow_CMAX \
	-rc_corner corner_typical \
	-early_library_set libset_fast \
	-late_library_set libset_slow
create_delay_corner -name delay_corner_fast_CMIN \
	-rc_corner corner_typical \
	-early_library_set libset_fast \
	-late_library_set libset_slow
create_constraint_mode -name func_mode -sdc_files $design_dir/floorplan.sdc

create_analysis_view -name func_slow_CMAX -constraint_mode func_mode -delay_corner delay_corner_slow_CMAX
create_analysis_view -name func_fast_CMIN -constraint_mode func_mode -delay_corner delay_corner_fast_CMIN

set_analysis_view -setup [list func_slow_CMAX] -hold [list func_fast_CMIN]
