create_rc_corner -name corner_Cworst
create_rc_corner -name corner_RCworst
create_rc_corner -name corner_Cbest
create_rc_corner -name corner_RCbest

create_lib_set -name lib_ss0p9_125c -timing_lib $lib_ss0p9_125c_liberty_files
create_lib_set -name lib_ss0p9_-40c -timing_lib $lib_ss0p9_40c_liberty_files
create_lib_set -name lib_ff1p05_125c -timing_lib $lib_ff1p05_125c_liberty_files
create_lib_set -name lib_ff1p05_-40c -timing_lib $lib_ff1p05_40c_liberty_files
create_analysis_corner -name delay_corner_cworst \
    -late_lib_set lib_ss0p9_125c \
    -early_lib_set lib_ff1p05_125c \
    -rc_corner corner_Cworst
create_analysis_corner -name delay_corner_rcworst \
    -late_lib_set lib_ss0p9_-40c \
    -early_lib_set lib_ff1p05_-40c \
    -rc_corner corner_RCworst
create_analysis_corner -name delay_corner_cbest \
    -late_lib_set lib_ss0p9_125c \
    -early_lib_set lib_ff1p05_125c \
    -rc_corner corner_Cbest
create_analysis_corner -name delay_corner_rcbest \
    -late_lib_set lib_ss0p9_-40c \
    -early_lib_set lib_ff1p05_-40c \
    -rc_corner corner_RCbest

create_analysis_mode -name func_max_mode -constraint_file $sdc_files
create_analysis_mode -name func_min_mode -constraint_file $sdc_files

#create_analysis_view -name func_cworst -analysis_mode func_max_mode \
#    -analysis_corner delay_corner_cworst
create_analysis_view -name func_rcworst -analysis_mode func_max_mode \
    -analysis_corner delay_corner_rcworst
#create_analysis_view -name func_cbest -analysis_mode func_min_mode \
#    -analysis_corner delay_corner_cbest
create_analysis_view -name func_rcbest -analysis_mode func_min_mode \
    -analysis_corner delay_corner_rcbest

set_views_status -hold {func_rcbest} -setup {func_rcworst}
#set_analysis_view_status -view func_cbest -active true -setup false -hold true
#set_analysis_view_status -view func_cworst -active true -setup true -hold false
