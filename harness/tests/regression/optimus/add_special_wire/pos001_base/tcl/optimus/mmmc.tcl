global tech_dir design_dir

create_lib_set -name slowLibSet_40c \
    -timing_lib "$tech_dir/scc28nhkcp_hsc30p140_rvt_ss_v0p9_-40c_ccs.lib"
create_lib_set -name fastLibSet_40c \
    -timing_lib "$tech_dir/scc28nhkcp_hsc30p140_rvt_ff_v1p05_-40c_ccs.lib"
create_lib_set -name slowLibSet_125c \
    -timing_lib "$tech_dir/scc28nhkcp_hsc30p140_rvt_ss_v0p9_125c_ccs.lib"
create_lib_set -name fastLibSet_125c \
    -timing_lib "$tech_dir/scc28nhkcp_hsc30p140_rvt_ff_v1p05_125c_ccs.lib"

create_rc_corner -name corner_RCbest
create_rc_corner -name corner_RCworst
create_rc_corner -name corner_Cbest
create_rc_corner -name corner_Cworst

create_analysis_corner -name delay_corner_rcbest \
    -rc_corner corner_RCbest \
    -late_lib_set slowLibSet_40c \
    -early_lib_set fastLibSet_40c
create_analysis_corner -name delay_corner_rcworst \
    -rc_corner corner_RCworst \
    -late_lib_set slowLibSet_40c \
    -early_lib_set fastLibSet_40c
create_analysis_corner -name delay_corner_cbest \
    -rc_corner corner_Cbest \
    -late_lib_set slowLibSet_125c \
    -early_lib_set fastLibSet_125c
create_analysis_corner -name delay_corner_cworst \
    -rc_corner corner_Cworst \
    -late_lib_set slowLibSet_125c \
    -early_lib_set fastLibSet_125c

create_analysis_mode -name func_max_mode -constraint_file "$design_dir/floorplan.sdc"
create_analysis_mode -name func_min_mode -constraint_file "$design_dir/floorplan.sdc"

create_analysis_view -name func_rcbest -analysis_mode func_min_mode -analysis_corner delay_corner_rcbest
create_analysis_view -name func_rcworst -analysis_mode func_max_mode -analysis_corner delay_corner_rcworst
create_analysis_view -name func_cbest -analysis_mode func_min_mode -analysis_corner delay_corner_cbest
create_analysis_view -name func_cworst -analysis_mode func_max_mode -analysis_corner delay_corner_cworst

set_analysis_view_status -view func_rcworst -active true -setup true -hold false
set_analysis_view_status -view func_cworst -active true -setup true -hold false
set_analysis_view_status -view func_rcbest -active true -setup false -hold true
set_analysis_view_status -view func_cbest -active true -setup false -hold true
