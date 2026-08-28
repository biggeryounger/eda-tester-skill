create_lib_set -name libset_fast \
  -timing_lib \
  [list $tech_dir/scc28nhkcp_hsc30p140_rvt_ff_v1p05_-40c_ccs.lib]

create_lib_set -name libset_slow \
  -timing_lib \
  [list $tech_dir/scc28nhkcp_hsc30p140_rvt_ff_v1p05_-40c_ccs.lib]

create_rc_corner -name corner_typical

create_analysis_corner -name delay_corner_slow_CMAX \
  -rc_corner corner_typical \
  -early_lib_set libset_fast \
  -late_lib_set libset_slow

create_analysis_corner -name delay_corner_fast_CMIN \
  -rc_corner corner_typical \
  -early_lib_set libset_fast \
  -late_lib_set libset_slow

create_analysis_mode -name func_mode2 -constraint_file $design_dir/chip_late.sdc

create_analysis_view -name func_slow_CMAX -analysis_mode func_mode2 -analysis_corner delay_corner_slow_CMAX
create_analysis_view -name func_fast_CMIN -analysis_mode func_mode2 -analysis_corner delay_corner_fast_CMIN

set_analysis_view_status -view func_fast_CMIN -setup false -hold true -active true
set_analysis_view_status -view func_slow_CMAX -setup true -hold false -active true