# Optimus TCL 生成语料

版本：`1.0`

本语料来自用户提供的 Optimus 全流程 TCL 和 MMMC TCL。它用于生成 Optimus 测试脚本的流程背景知识，不是命令语法手册，也不能替代目标项目的 PDK、library、设计约束和工具版本配置。

## 使用原则

- 只在目标工具为 **Optimus** 时加载本语料。
- 复用流程阶段、命令顺序、对象依赖、输出节点和检查点位置。
- 不复制来源中的 PDK 路径、library 文件名、cell 名、设计名、时钟名、金属层、process node、绝对数值或内部目录。
- 所有设计相关值从用户提供的 `design.tcl`、测试需求或脱敏配置中取得；缺失时使用语义占位符并记录缺口，不生成看似可执行的虚构值。
- 单个命令的选项、枚举、默认值和约束必须来自对应 Optimus 命令说明；本流程中出现某个写法，只能证明该组合是一个参考用法，不能证明它覆盖全部语法。
- 生成的用例仍需遵守测试策略、目录结构、`nith.run` 和 `pv_check_*` 规范。

## 1. 全流程阶段模型

参考流程按以下顺序组织：

```text
环境与设计配置
  -> setup_design
  -> initialize_floorplan
  -> 电源连接与基础选项
  -> place
  -> optimize -post_place
  -> synthesize_clock_tree
  -> optimize -post_cts
  -> route
  -> optimize -post_route
  -> optimize_via
  -> pv_rpt_checkpoints
  -> exit
```

### 1.1 环境与设计配置

```tcl
source $env(PV_ROOT)/scripts/pv.tcl
source ./tcl/design.tcl

set_options global.infra.max_thread_count $max_threads
set_options setup.lef_file $lef_files
set_options setup.verilog $netlist_file
set_options setup.ground_net $ground_net
set_options setup.power_net $power_net
set_options setup.mmmc_file ./tcl/optimus/mmmc.tcl
set_options setup.top_cell $top_cell
setup_design
```

生成约束：

- `$max_threads`、`$lef_files`、`$netlist_file`、`$ground_net`、`$power_net`、`$top_cell` 必须来自用例配置。
- `setup.mmmc_file` 指向用例内普通文件，不得使用软连接。
- 来源流程使用 `$env(PV_ROOT)/scripts/pv.tcl`；若实际环境配置了其他 PV 入口，必须以用户确认的路径为准并记录差异。

### 1.2 Floorplan 与 PG 准备

```tcl
initialize_floorplan \
    -site $core_site \
    -utilization $target_utilization \
    -core_to_die_offset $core_to_die_offset \
    -aspect_ratio $aspect_ratio

connect_pg_net -pg_net $power_net -pins $power_pins -type pg_pin
connect_pg_net -pg_net $ground_net -pins $ground_pins -type pg_pin
allocate_pg_mask
```

`core_site`、利用率、die offset、aspect ratio、PG pin 映射均为项目数据，不从语料中的示例值推导。

### 1.3 Placement 配置与执行

来源流程在 placement 前配置以下类别：

- timing analysis：OCV、clock path pessimism removal。
- detailed placement：legalization gap、filler、EEQ cell、DRC。
- global placement：power/timing/congestion driven、density、scan chain、IO pin、channel blockage。
- `set_dont_use` cell 约束。

参考骨架：

```tcl
set_options timing_analysis.analysis_type $analysis_type
set_options timing_analysis.clock_path_pessimism_removal $enable_cppr
set_options place.global.congestion_effort $congestion_effort
set_options place.global.max_density $max_density
set_options place.global.timing_driven_effort $timing_effort

place
write_def odb/place.def.gz
write_verilog odb/place.v.gz
write_sdc odb/place.sdc
```

仅生成被测场景所需选项；不要把全流程中的所有调优选项无差别复制到每个测试用例。

### 1.4 Post-place 优化与检查点

```tcl
source $derate_tcl
set_interactive_analysis_modes $analysis_mode
set_clock_uncertainty $post_place_uncertainty -setup [get_clocks $clock_name]
set_options optimize.target_setup_slack $post_place_target_slack

optimize -post_place
pv_check_qor {report_qor -place_opt} -name place_opt.$PV_TOOL

write_def odb/prects.def.gz
write_verilog odb/prects.v.gz
write_sdc odb/prects.sdc
```

如果测试对象不是 QoR/timing 行为，应根据输出类型改用 `pv_check_log` 或 `pv_check_golden`，不得为了贴合参考流强制使用 `pv_check_qor`。

### 1.5 CTS 与 post-CTS

来源流程包含：

- early clock flow。
- CTS inverter/buffer cell 约束。
- top/trunk/leaf routing layer range。
- NDR 创建、CTS routing rule 和 shield net。
- `synthesize_clock_tree`、clock summary、post-CTS 优化。

参考骨架：

```tcl
set_options design.enable_early_clock_flow $enable_early_clock_flow
set_options cts.use_inverters $use_inverters
set_cts_attribute inverter_cells $cts_inverter_cells

create_ndr -name $ndr_name \
    -non_default_spacing_multiplier $ndr_spacing \
    -non_default_width_multiplier $ndr_width

synthesize_clock_tree
report_clock_timing -type summary
pv_check_qor {report_qor -cts} -name cts.$PV_TOOL

optimize -post_cts
pv_check_qor {report_qor -cts_opt} -name cts_opt.$PV_TOOL
```

cell、layer、NDR 和 shield 配置全部由目标 PDK/设计决定。

### 1.6 Route 与 post-route

来源流程在 route 前配置 antenna、trim metal、via 和 detail route 选项，然后执行 route 和 post-route 优化：

```tcl
set_options route.fix_antenna_insert_antenna_diode $enable_antenna_fix
set_options route.antenna_cells $antenna_cells
set_options route.via_swap $via_swap_mode
set_options route.detail.end_iteration $route_iterations

route
pv_check_qor {report_qor -route} -name route.$PV_TOOL

set_options optimize.target_setup_slack $post_route_target_slack
optimize -post_route
optimize_via -cut_spacing
pv_check_qor {report_qor -route_opt} -name route_opt.$PV_TOOL

write_def odb/postroute.def.gz
write_verilog odb/postroute.v.gz
write_sdc odb/postroute.sdc
pv_rpt_checkpoints
exit
```

trim-metal mask、pitch、offset、width 和 antenna cell 属于 PDK 数据，禁止从来源样例复制。

## 2. MMMC 对象模型

MMMC 文件按以下依赖图生成：

```text
timing libraries -> create_lib_set ─────────────┐
                                                ├-> create_analysis_corner
RC technology  -> create_rc_corner ─────────────┘
constraint file -> create_analysis_mode
analysis_corner + analysis_mode -> create_analysis_view
analysis_view -> set_analysis_view_status
```

### 2.1 可移植 MMMC 骨架

```tcl
create_lib_set -name $setup_lib_set \
    -timing_lib $setup_timing_libraries

create_lib_set -name $hold_lib_set \
    -timing_lib $hold_timing_libraries

create_rc_corner -name $setup_rc_corner \
    -rc_tech $setup_rc_tech

create_rc_corner -name $hold_rc_corner \
    -rc_tech $hold_rc_tech

create_analysis_corner -name $setup_analysis_corner \
    -rc_corner $setup_rc_corner \
    -lib_set $setup_lib_set

create_analysis_corner -name $hold_analysis_corner \
    -rc_corner $hold_rc_corner \
    -lib_set $hold_lib_set

create_analysis_mode -name $functional_mode \
    -constraint_file $functional_sdc

create_analysis_view -name $setup_view \
    -analysis_mode $functional_mode \
    -analysis_corner $setup_analysis_corner

create_analysis_view -name $hold_view \
    -analysis_mode $functional_mode \
    -analysis_corner $hold_analysis_corner

set_analysis_view_status -view $setup_view \
    -active true -setup true -hold false

set_analysis_view_status -view $hold_view \
    -active true -setup false -hold true
```

### 2.2 MMMC 生成约束

- timing library 使用 Tcl list；不得把某个工艺库文件名写死在 Skill 中。
- lib set、RC corner、analysis corner、analysis mode 和 view 名称在文件内必须唯一。
- `create_analysis_corner` 引用的 lib set 和 RC corner 必须先创建。
- `create_analysis_view` 引用的 mode 和 corner 必须先创建。
- setup view 必须引用用户指定的 setup library/RC corner；hold view 同理，不能只根据变量名猜测 corner 语义。
- `set_analysis_view_status` 的 setup/hold 标志必须与 view 的设计目的一致。
- constraint file 必须位于用例 `design/` 或其他已批准的用例内目录，不得引用用户机器绝对路径。

## 3. 来源中需要人工确认的事项

- 用户提供的 MMMC 示例中，`libset_cworst...` 使用文件名含 `cbest...` 的 library，而 `libset_cbest...` 使用文件名含 `cworst...` 的 library；名称与文件属性看起来交叉。
- analysis view 名称中的 PVT 字符串与 analysis corner 名称也不能仅凭文本证明一致。
- 生成实际 MMMC 前，必须根据目标 library metadata 或用户确认建立 setup/hold 对应关系；不得照抄来源命名。
- 来源全流程的 PV 入口是 `$env(PV_ROOT)/scripts/pv.tcl`，此前 pv_check 使用资料给出的入口是 `$env(PV_ROOT)/pv/scripts/pv.tcl`。生成时使用目标环境确认的入口，并在测试设计中记录来源差异。

## 4. 语料边界

本语料可以回答“Optimus 全流程通常如何组织”和“MMMC 对象如何连接”，但不能单独回答：

- 某个命令的完整选项集合。
- 选项默认值、枚举值或版本差异。
- 某 PDK 的合法 layer、cell、library 和 RC tech。
- 某设计的时钟、不确定度、目标 slack、密度或约束。

这些信息必须来自目标版本命令说明和用户提供的脱敏设计配置。
