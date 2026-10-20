#4 view
create_library_set -name slowLibSet_40c -timing $rcworst_liberty_files
create_library_set -name fastLibSet_40c -timing $rcbest_liberty_files
create_library_set -name slowLibSet_125c -timing $cworst_liberty_files
create_library_set -name fastLibSet_125c -timing $cbest_liberty_files

create_rc_corner -name corner_RCbest -qx_tech_file $rcbest_rc_tech_file
create_rc_corner -name corner_RCworst -qx_tech_file $rcworst_rc_tech_file
create_rc_corner -name corner_Cbest -qx_tech_file $cbest_rc_tech_file
create_rc_corner -name corner_Cworst -qx_tech_file $cworst_rc_tech_file

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

create_constraint_mode -name func_max_mode -sdc_files $sdc_files
create_constraint_mode -name func_min_mode -sdc_files $sdc_files
#4 view
create_analysis_view -name func_rcbest -constraint_mode func_min_mode -delay_corner delay_corner_rcbest
create_analysis_view -name func_rcworst -constraint_mode func_max_mode -delay_corner delay_corner_rcworst
create_analysis_view -name func_cbest -constraint_mode func_min_mode -delay_corner delay_corner_cbest
create_analysis_view -name func_cworst -constraint_mode func_max_mode -delay_corner delay_corner_cworst

#4 view
set_analysis_view -hold {func_rcbest func_cbest} -setup {func_rcworst func_cworst}
#set_analysis_view_status -view func_rcbest -active true -setup false -hold true
#set_analysis_view_status -view func_rcworst -active true -setup true -hold false
# set_analysis_view_status -view func_cbest -active true -setup false -hold true
 #set_analysis_view_status -view func_cworst -active true -setup true -hold false
