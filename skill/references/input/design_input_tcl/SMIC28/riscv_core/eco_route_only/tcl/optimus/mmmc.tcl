#4 view
create_lib_set -name slowLibSet_40c -timing_lib $rcworst_liberty_files
create_lib_set -name fastLibSet_40c -timing_lib $rcbest_liberty_files
create_lib_set -name slowLibSet_125c -timing_lib $cworst_liberty_files
create_lib_set -name fastLibSet_125c -timing_lib $cbest_liberty_files

create_rc_corner -name corner_RCbest -rc_tech $rcbest_rc_tech_file
create_rc_corner -name corner_RCworst -rc_tech $rcworst_rc_tech_file
create_rc_corner -name corner_Cbest -rc_tech $cbest_rc_tech_file
create_rc_corner -name corner_Cworst -rc_tech $cworst_rc_tech_file

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
create_analysis_view -name func_cbest -analysis_mode func_min_mode -analysis_corner delay_corner_cbest
create_analysis_view -name func_cworst -analysis_mode func_max_mode -analysis_corner delay_corner_cworst

#4 view
set_views_status -hold {func_rcbest func_cbest} -setup {func_rcworst func_cworst}
#set_analysis_view_status -view func_rcbest -active true -setup false -hold true
#set_analysis_view_status -view func_rcworst -active true -setup true -hold false
# set_analysis_view_status -view func_cbest -active true -setup false -hold true
 #set_analysis_view_status -view func_cworst -active true -setup true -hold false
