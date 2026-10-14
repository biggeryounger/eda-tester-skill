# 4 view
create_library_set -name slowLibSet_40c -timing $tech_dir/scc28nhkcp_hsc30p140_rvt_ss_v0p9_-40c_ccs.lib
create_library_set -name fastLibSet_40c -timing $tech_dir/scc28nhkcp_hsc30p140_rvt_ff_v1p05_-40c_ccs.lib
create_library_set -name slowLibSet_125c -timing $tech_dir/scc28nhkcp_hsc30p140_rvt_ss_v0p9_125c_ccs.lib
create_library_set -name fastLibSet_125c -timing $tech_dir/scc28nhkcp_hsc30p140_rvt_ff_v1p05_125c_ccs.lib

create_rc_corner -name corner_RCbest
create_rc_corner -name corner_RCworst
create_rc_corner -name corner_Cbest
create_rc_corner -name corner_Cworst

create_delay_corner -name delay_corner_rcbest \
    -rc_corner corner_RCbest \
    -late_library_set slowLibSet_40c \
    -early_library_set fastLibSet_40c

create_delay_corner -name delay_corner_rcworst \
    -rc_corner corner_RCworst \
    -late_library_set slowLibSet_40c \
    -early_library_set fastLibSet_40c

create_delay_corner -name delay_corner_cbest \
    -rc_corner corner_Cbest \
    -late_library_set slowLibSet_125c \
    -early_library_set fastLibSet_125c

create_delay_corner -name delay_corner_cworst \
    -rc_corner corner_Cworst \
    -late_library_set slowLibSet_125c \
    -early_library_set fastLibSet_125c

create_constraint_mode -name func_max_mode -sdc_files $design_dir/floorplan.sdc
create_constraint_mode -name func_min_mode -sdc_files $design_dir/floorplan.sdc

# 4 view
create_analysis_view -name func_rcbest -constraint_mode func_min_mode -delay_corner delay_corner_rcbest
create_analysis_view -name func_rcworst -constraint_mode func_max_mode -delay_corner delay_corner_rcworst
create_analysis_view -name func_cbest -constraint_mode func_min_mode -delay_corner delay_corner_cbest
create_analysis_view -name func_cworst -constraint_mode func_max_mode -delay_corner delay_corner_cworst

# 4 view
set_analysis_view -setup [list func_rcworst func_cworst] -hold [list func_rcbest func_cbest]
