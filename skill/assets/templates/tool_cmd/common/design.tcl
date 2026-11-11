set design_dir "./design"
set tech_dir "$env(PV_ROOT)/data_center/tmp_share/tech/smic180/digital/sc"

set init_top_name "ddp_partition_top"
set lef_files [list \
    "$env(PV_ROOT)/data_center/tmp_share/tech/smic180/digital/sc/lef/smic18_5lm_grid.lef"]
set netlist_file "./design/input.v"
set def_file {}
set power_net "VDD"
set ground_net "VSS"
# No DEF is consumed: these tests examine logical hierarchy and connectivity.
set liberty_files [list "$tech_dir/synopsys/typical.lib"]
set sdc_files [list ./design/input.sdc]
set reference_netlist ./design/input.v