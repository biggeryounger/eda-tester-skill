create_lib_set -name slowLibSet_40c -timing_lib $slowlibset_40c_liberty_files

create_lib_set -name fastLibSet_40c -timing_lib $fastlibset_40c_liberty_files

create_lib_set -name slowLibSet_125c -timing_lib $slowlibset_125c_liberty_files

create_lib_set -name fastLibSet_125c -timing_lib $fastlibset_125c_liberty_files

#4 view
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

create_analysis_mode -name func_max_mode -constraint_file $sdc_files
create_analysis_mode -name func_min_mode -constraint_file $sdc_files
#4 view
create_analysis_view -name func_rcbest -analysis_mode func_min_mode -analysis_corner delay_corner_rcbest
create_analysis_view -name func_rcworst -analysis_mode func_max_mode -analysis_corner delay_corner_rcworst
#create_analysis_view -name func_cbest -analysis_mode func_min_mode -analysis_corner delay_corner_cbest
#create_analysis_view -name func_cworst -analysis_mode func_max_mode -analysis_corner delay_corner_cworst

#4 view
set_views_status -hold {func_rcbest} -setup {func_rcworst}
#set_analysis_view_status -view func_cbest -active true -setup false -hold true
#set_analysis_view_status -view func_cworst -active true -setup true -hold false
