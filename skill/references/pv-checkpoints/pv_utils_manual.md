> 资料归档：2026-10-20；来源：`e2_pv_kit/legacy/pv_check_bundle_20261012/reference/pv_utils_manual.md`；原文 SHA-256：`5b4b79507cef1ffd4fc22ef3e09980d2c921082841837b51e9bc521111d4100c`。
> 已将原文部署绝对路径替换为 PV_ROOT 示例，并移除未归档附件的链接。原文中的项目约束与 regolden 示例属于来源背景，生成用例时以 Skill 当前规则为准。版本范围和门禁差异见 [检查点参考入口](index.md)。

# `pv_utils.tcl` / `pv_check_route.tcl` 使用手册

## 1. 文档范围

本文说明基础工具文件 `pv_utils.tcl` 以及独立 Route 扩展文件 `pv_check_route.tcl` 提供的 PV 测试辅助过程，包括检查点输出、日志片段提取、Route 指标解析与容差比对、Golden 文件比对、图片比对、结果汇总和嵌套列表打印。

本地文件信息：

- 远端实际路径：`$env(PV_ROOT)/scripts/pv_utils.tcl`
- `pv_utils.tcl`：24,771 字节，729 行，版本 `pv_utils-1.1.1`
- `pv_utils.tcl` SHA-256：`081692610b0ea2975eb1d7bfc404cfbc1e296380bcfe3489d4da08494cfc0c7d`
- `pv_check_route.tcl`：20,055 字节，523 行
- `pv_check_route.tcl` 版本：`pv_check_route-1.3.3`
- `pv_check_route.tcl` SHA-256：`73526abc1c669797965e23c99daf83611fac26e30e23ed1249a1f18ae3289a16`

`pv_utils.tcl` 最初从 login01 按字节复制；版本 `1.1.0` 在本地加入 marked-log 公共执行与提取层，使普通日志检查和 Route 检查复用同一流程。Route 指标解析和 JSON 比对仍位于独立的 `pv_check_route.tcl`。

> 注意：最初给出的路径为 `.../pv/script/pv_utils.tcl`，其中 `script` 为单数；login01 上该路径不存在。实际文件位于 `.../pv/scripts/pv_utils.tcl`，其中 `scripts` 为复数。

## 2. 加载方式

只使用基础功能时加载：

```tcl
source $env(PV_ROOT)/scripts/pv_utils.tcl
```

如果调用脚本与 `pv_utils.tcl` 在同一目录，也可使用：

```tcl
source [file join [file dirname [info script]] pv_utils.tcl]
```

使用 Route 检查功能时只需加载扩展文件：

```tcl
source /path/to/pv_check_route.tcl
```

`pv_check_route.tcl` 会先用 `info exists` 检查加载标记，仅在尚未加载时按自身所在目录 source 同级的 `pv_utils.tcl`：

```tcl
if {![info exists ::pv_utils_loaded]} {
    source [file join [file dirname [info script]] pv_utils.tcl]
}
```

`pv_utils.tcl` 在全部过程成功定义后设置 `::pv_utils_loaded`。因此先加载基础文件再加载 Route 扩展时，不会重复 source。

因此两个文件必须放在同一目录；调用方不需要再次 source `pv_utils.tcl`。

公共过程及其定义位置：

| 过程 | 定义文件 | 用途 |
| --- | --- | --- |
| `pv_check_point` | `pv_utils.tcl` | 输出 PASS/FAIL 检查点 |
| `pv_mark_begin` / `pv_mark_end` | `pv_utils.tcl` | 输出日志片段的起止标记 |
| `pv_check_golden` | `pv_utils.tcl` | 文本文件与 Golden 比对，或更新 Golden |
| `pv_check_log` | `pv_utils.tcl` | 执行 Tcl 命令、加标记，并检查对应日志片段 |
| `pv_check_mark` | `pv_utils.tcl` | 从日志中提取指定标记范围并与 Golden 比对 |
| `pv_check_route` | `pv_check_route.tcl` | 执行 Route 命令，提取日志、解析 JSON 并按容差比对 |
| `pv_parse_route_mark` | `pv_check_route.tcl` | 独立解析 Route `.mark` 并生成同名 `.json` |
| `pv_compare_route_json` | `pv_check_route.tcl` | 按键比较实际/Golden JSON 中的数值与容差 |
| `pv_diff_str` | `pv_utils.tcl` | 精确比较两个字符串 |
| `pv_find_string` | `pv_utils.tcl` | 在文件中查找固定字符串 |
| `pv_diff_files` | `pv_utils.tcl` | 流式过滤并比较普通文件或 `.gz` 文件 |
| `pv_check_golden_img` | `pv_utils.tcl` | 调用 Python 脚本进行图片或图片目录比对 |
| `pv_rpt_checkpoints` | `pv_utils.tcl` | 汇总日志中的全部检查点 |
| `pv_print_nested_list` | `pv_utils.tcl` | 递归打印嵌套 Tcl 列表的叶子项 |

基础文件另有 `__pv_check_log_common`、`__pv_extract_mark`、`__pv_finish_log_check`、`pv_diff_files_old` 和 `__pv_read_and_filter`；Route 扩展另有 `__pv_finish_route_check`、兼容入口 `__pv_extract_route_mark`、`__pv_normalize_route_number`、`__pv_route_key_component`、`__pv_split_route_pipe_row` 和 `__pv_read_route_numeric_json`。这些属于兼容或内部过程，新代码应优先使用上述公共过程。

## 3. 通用返回码与输出约定

多数检查过程使用以下返回码：

| 返回值 | 含义 |
| ---: | --- |
| `0` | 检查通过，或 regolden 成功 |
| `1` | 内容不一致、未找到目标字符串，或普通检查失败 |
| `2` | 输入文件不存在、参数/环境不完整等执行条件错误 |

检查点输出格式固定为：

```text
Check Point: <name> PASS
Check Point: <name> FAIL
```

`pv_rpt_checkpoints` 依赖这一格式进行汇总。调用方通常应保存返回值并决定是否退出：

```tcl
set rc [pv_check_golden result.txt -golden golden/result.txt]
if {$rc != 0} {
    # 可在此处终止当前测试或累计失败数
}
```

## 4. 环境变量

| 环境变量 | 使用位置 | 作用 |
| --- | --- | --- |
| `PV_CHECK_MODE` | `pv_check_golden`、`pv_check_route`、`pv_compare_route_json`、`pv_check_golden_img`、`pv_rpt_checkpoints` | 值为 `1` 或 `regolden` 时更新 Golden；未设置时执行普通比对 |
| `PV_ROOT` | `pv_check_golden_img` | 定位 `$PV_ROOT/scripts/image_compare.py`，图片比对时必需 |
| `PV_TOOL` | `pv_check_mark`、`pv_parse_route_mark` | Route 解析器选择开关；未设置或为 `default` 时使用当前格式，`optimus` 也映射到当前格式，其他值按命名约定选择工具专用 proc |

建议在启动 EDA/测试工具前设置环境变量，例如：

```sh
export PV_CHECK_MODE=regolden
export PV_ROOT=/path/to/pv
```

## 5. 检查点与日志标记

### 5.1 `pv_check_point`

```tcl
pv_check_point name flag
```

- `name`：检查点名称。
- `flag`：Tcl 布尔值；假值输出 `PASS`，真值输出 `FAIL`。
- 返回：无显式业务返回值。

示例：

```tcl
pv_check_point route_result 0
pv_check_point timing_result 1
```

由于 `1`、`2` 等非零整数都是真值，可直接把本文件其他检查过程的返回码传给 `flag`。

### 5.2 `pv_mark_begin` / `pv_mark_end`

```tcl
pv_mark_begin name
pv_mark_end name
```

输出：

```text
===PV_MARKER begin: <name> ===
===PV_MARKER end: <name> ===
```

标记名应使用不含空白的字符串，因为 `pv_check_mark` 使用 `\S+` 提取名称。

示例：

```tcl
pv_mark_begin report_qor
report_qor
pv_mark_end report_qor
```

### 5.3 `pv_check_log`

```tcl
pv_check_log command ?-name name? ?-filter regexp? ?-match regexp? ?-log_files fileList?
```

该过程是 `__pv_check_log_common` 的轻量入口，完成三件事：

1. 在调用者作用域通过 `uplevel 1` 执行 `command`；
2. 在命令前后输出同名 `PV_MARKER`；
3. 通过 `__pv_finish_log_check` 回调调用 `pv_check_mark`，提取日志并执行 Golden 比对。

参数：

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `command` | 必填 | Tcl 命令列表或脚本；默认检查点名为命令第一个元素 |
| `-name` | 命令第一个元素 | 自定义标记、`.mark` 文件和检查点名称 |
| `-filter` | 空 | 生成 `.mark` 后，比对时忽略匹配该正则的整行 |
| `-match` | 空 | 提取标记范围时只保留匹配该正则的行 |
| `-log_files` | `*.stdout`；若存在则优先 `.pvflow_wrapper.log.tmp` | 要扫描的日志文件或 Tcl 文件列表 |

推荐把命令写成 Tcl 列表，避免参数被错误拆分：

```tcl
set rc [pv_check_log [list report_qor -summary] \
    -name qor_summary \
    -filter {^Generated at:} \
    -log_files {run.stdout}]
```

如果没有发现默认日志，过程会探测当前工具是否支持 `redirect`，并尝试以下两类工具专用接口之一：

```tcl
redirect -file name.pvlog -tee -no_log { ... }
redirect name.pvlog -tee { ... }
```

因此，`pv_check_log` 通常需要在提供 `redirect` 命令的 EDA Tcl 环境中运行；纯 `tclsh` 不一定具备自动重定向能力。

### 5.4 `pv_check_mark`

```tcl
pv_check_mark marker ?-log_files fileList? ?-filter regexp? ?-match regexp?
```

处理流程：

1. 顺序读取每个日志；
2. 捕获匹配 `marker` 的 begin/end 标记之间的内容；
3. 多个捕获片段之间写入 `--- PV_MARKER Separator ---`；
4. 生成 `<marker>.mark`；
5. 调用 `pv_check_golden`，默认与 `golden/<marker>.mark` 比较。

默认行为和参数：

| 项目 | 行为 |
| --- | --- |
| 日志选择 | 当前目录的 `*.stdout`，但 `.pvflow_wrapper.log.tmp` 存在时只使用该文件 |
| `-match regexp` | 非空时，仅写出捕获范围内匹配该正则的行 |
| 无 `-match` | 写出捕获范围内除 `Time: Elapse` 之外的所有行 |
| `-filter regexp` | 不影响提取；在后续 Golden 比对阶段，从实际和 Golden 两边同时过滤匹配行 |
| 输出 | `<marker>.mark` 和一条 PASS/FAIL 检查点 |

示例：

```tcl
set rc [pv_check_mark report_qor \
    -log_files {run_1.stdout run_2.stdout} \
    -match {^(WNS|TNS|Area):} \
    -filter {Elapsed}]
```

异常标记只产生警告：重复 begin、没有 begin 的 end、以及文件结束时仍未闭合的 begin 都不会直接令过程返回 `2`；最终返回值仍由生成的 `.mark` 与 Golden 的比对结果决定。

### 5.5 `pv_check_route`

该过程定义于 `pv_check_route.tcl`。调用前应 source 此扩展文件，而不是只 source `pv_utils.tcl`。

当前文件头版本标记为：

```tcl
# @version pv_check_route-1.3.3
```

```tcl
pv_check_route command \
    ?-name name? \
    ?-filter regexp? \
    ?-match regexp? \
    ?-log_files fileList? \
    ?-golden golden.json? \
    ?-tolerance toleranceDict? \
    ?-tol toleranceDict?
```

`pv_check_route` 与 `pv_check_log` 共同调用 `pv_utils.tcl` 中的 `__pv_check_log_common`，因此参数解析、默认日志选择、`redirect` 探测、marker 包裹和 `.mark` 提取只维护一份。二者仅在公共流程最后选择不同回调：普通日志使用 `__pv_finish_log_check`，Route 使用 `__pv_finish_route_check`。

`pv_check_route` 不会对 `.mark` 文本做普通 `diff`。它会依次：

1. 由公共流程在 `command` 前后输出 `PV_MARKER`，并在调用者作用域执行命令；
2. 由公共 `__pv_extract_mark` 从日志中提取 `<name>.mark`；
3. 调用 `pv_parse_route_mark` 生成 `<name>.json`；
4. 调用 `pv_compare_route_json`，将实际 JSON 与 Golden JSON 按键做数值差比较；
5. 输出 `Check Point: <name> PASS|FAIL` 并返回状态码。

参数：

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `command` | 必填 | Tcl 命令列表或脚本；默认检查点名为命令第一个元素 |
| `-name` | 命令第一个元素 | 标记名，以及生成的 `.mark`/`.json` 基本名称 |
| `-filter` | 空 | 解析 `.mark` 时跳过匹配该 Tcl 正则的整行 |
| `-match` | 空 | 提取标记范围时仅保留匹配该正则的行 |
| `-log_files` | 与 `pv_check_log` 相同 | 要扫描的日志文件或 Tcl 文件列表 |
| `-golden` | `golden/<name>.json` | Golden JSON 的路径 |
| `-tolerance`、`-tol` | 空字典，即所有键为 `0` | Tcl 字典：JSON 键名与允许的最大绝对差值 |

只接受 `-tolerance` 和它的简写 `-tol`；新代码建议优先使用完整拼法 `-tolerance`。若同时提供这两个参数，后出现的值覆盖前面的值。

典型用法：

```tcl
set route_tolerance [dict create \
    "total_wire_length" 10 \
    "total_number_of_vias" 5 \
    "global_routing.horizontal_overflow" 0.05 \
    "vertical_overflow" 0.10]

set rc [pv_check_route [list route_design] \
    -name route \
    -log_files {run.stdout} \
    -golden golden/route.json \
    -tolerance $route_tolerance]
```

容差采用绝对差：

```text
abs(actual_value - golden_value) <= tolerance
```

只有字典中显式列出的键使用自定义容差；其他键的容差均为 `0`。容差必须是非负数，容差键必须同时存在于实际 JSON 和 Golden JSON 中，否则返回 `2`，可避免键名拼错后静默失效。

当 `PV_CHECK_MODE` 为 `1` 或 `regolden` 时，实际 JSON 会覆盖 `-golden`，父目录不存在时自动创建。此模式仍会先确认实际 JSON 可解析，并检查容差键存在于实际 JSON 中。

> 若使用 `-match`，必须同时保留阶段名、子表名、表头和数据行。仅匹配数值行会丢失表格上下文，导致 DR、congestion 或 hotspot 表格无法解析。

### 5.6 `pv_parse_route_mark`

```tcl
pv_parse_route_mark mark_file ?filter_pattern?
```

`pv_parse_route_mark` 是由 `PV_TOOL` 控制的调度入口。它选择工具专用解析过程，再由该过程读取 Route `.mark` 并在同一目录生成同基本名称的 JSON。例如 `result/route.mark` 会生成 `result/route.json`。

调度规则：

| `PV_TOOL` | 调用的 proc |
| --- | --- |
| 未设置、空值或 `default` | `pv_parse_route_mark_default` |
| `optimus` | `pv_parse_route_mark_optimus`，当前转调默认解析器 |
| 其他值 | `pv_parse_route_mark_<规范化工具名>` |

工具名会转成小写，并把非字母、数字、下划线的字符替换为下划线。例如：

```text
PV_TOOL=mock-tool -> pv_parse_route_mark_mock_tool
```

新增工具解析器应使用相同参数和返回约定：

```tcl
proc pv_parse_route_mark_mytool {mark_file {filter_pattern ""}} {
    # 解析 mytool 格式，生成 [file rootname $mark_file].json
    return [file rootname $mark_file].json
}

set ::env(PV_TOOL) mytool
set json_file [pv_parse_route_mark route.mark]
```

若对应 proc 不存在，调度入口会抛出 Tcl error 并指出预期的 proc 名称；`pv_check_route` 会将其转换为返回码 `2`。当前默认解析器的规则如下。

当前识别的区段：

- `Global routing`
- `Track routing`
- `Detail routing`
- `Wire spreading`

当前识别的指标：

| 日志字段 | 汇总 JSON 键 | 数值单位 |
| --- | --- | --- |
| `horizontal overflow` | `horizontal_overflow` | `%` |
| `vertical overflow` | `vertical_overflow` | `%` |
| `total length` 或 `total wire length` | `total_wire_length` | 日志所示的 `um` |
| `number of vias` 或 `total number of vias` | `total_number_of_vias` | 个数 |
| `total number of violations` | `total_number_of_violations` | 个数 |
| `total number of antenna violations` | `total_number_of_antenna_violations` | 个数 |

所有日志字段中的空格在 JSON 键里都会替换成下划线。例如 `total number of violations` 对应 `total_number_of_violations`。

此外，版本 `1.2.0` 支持以下二维表格：

| 日志表格 | JSON 键格式 | 说明 |
| --- | --- | --- |
| `[initial routing]` | `detail_routing.initial_routing.<drc行>.<列>` | 保存全部 DRC 行列 |
| `[DR iteration N]` | `detail_routing.dr_iteration_N.<drc行>.<列>` | 每次 iteration 独立保存，表头允许动态增减 |
| `congestion analysis by layer` | `global_routing.congestion_analysis_by_layer.<Layer>.<列>.count` / `.percent` | 将 `81(0.69%)` 拆成 count 与 percent |
| `Hotspot score` | `global_routing.hotspot_score.<Layer>.<列>` | 保存 Max Hotspot、Total Hotspot 等数值 |

DR 表格首列表头 `drc` 是行维度，下面对应 `M1`、`V1`、`total` 等行名；其余表头才是数值列。例如：

```text
drc     prl  eol  shrt  cutsp  minarea  volsp  total
M2        2    1     5      0        4      0     12
```

生成的键包括：

```json
{
  "detail_routing.dr_iteration_1.M2.cutsp": 0,
  "detail_routing.dr_iteration_1.M2.minarea": 4,
  "detail_routing.dr_iteration_1.M2.shrt": 5,
  "detail_routing.dr_iteration_1.M2.total": 12
}
```

不同 iteration 的列集合可以不同。例如 iteration 1 含 `eol`、`cutsp`、`volsp`，iteration 2 只含 `prl`、`shrt`、`minarea`、`total`，解析器会按各自表头生成键，不会补零或虚构缺失列。`total` 行也会完整保存。

Global routing 表格示例键：

```json
{
  "global_routing.congestion_analysis_by_layer.M2(H).con(1-2).count": 81,
  "global_routing.congestion_analysis_by_layer.M2(H).con(1-2).percent": 0.69,
  "global_routing.congestion_analysis_by_layer.Total.total_con.count": 268,
  "global_routing.hotspot_score.M1(V).max_hotspot": 2005.11,
  "global_routing.hotspot_score.M1(V).total_hotspot": 2213.22
}
```

除汇总键外，同一指标还会生成 `<区段名>.<指标名>` 形式的阶段键。例如：

```json
{
  "detail_routing.total_number_of_violations": 0,
  "global_routing.horizontal_overflow": 0.3,
  "total_number_of_antenna_violations": 0,
  "total_number_of_vias": 6736,
  "total_wire_length": 5573,
  "wire_spreading.total_wire_length": 5573
}
```

一个指标在日志中出现多次时，同一区段键和汇总键均采用最后一次出现的值。因此示例日志中最终的 `total wire length` 来自 `Wire spreading`，同一区段内重复出现的 `total number of violations` 也取最后一条。所有 JSON 值均为数字，而不是字符串；键按字典序输出，便于审阅和版本管理。

独立调用示例：

```tcl
set json_file [pv_parse_route_mark route.mark {^\s*#}]
puts "generated $json_file"
```

### 5.7 `pv_compare_route_json`

```tcl
pv_compare_route_json actual.json golden.json ?toleranceDict?
```

该过程可脱离命令执行和日志提取单独使用：

```tcl
set tolerance [dict create \
    "total_wire_length" 10 \
    "total_number_of_vias" 5 \
    "detail_routing.dr_iteration_1.M2.shrt" 2 \
    "global_routing.congestion_analysis_by_layer.M2(H).con(1-2).percent" 0.05 \
    "global_routing.hotspot_score.M1(V).max_hotspot" 10]

set rc [pv_compare_route_json route.json golden/route.json $tolerance]
```

比较规则：

1. 两边必须是非空、扁平的 JSON object，且所有 value 必须为数字；
2. 两边键集合必须完全相同，缺键或多键按比较失败返回 `1`；
3. 逐键计算绝对差，自定义容差之外的键使用零容差；
4. 超差时打印键名、实际值、Golden 值、差值和容差；
5. JSON/容差格式错误、文件缺失或无效容差键返回 `2`。

该功能使用 Tcl 内置能力实现，不依赖 `jq` 或 Tcllib JSON 包。

## 6. 文本与文件检查

### 6.1 `pv_check_golden`

```tcl
pv_check_golden out_file ?-name name? ?-golden golden_file? ?-filter regexp?
```

参数：

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `out_file` | 必填 | 实际输出文件；若不存在但 `out_file.gz` 存在，会自动改用 `.gz` 文件 |
| `-name` | 原始 `out_file` 字符串 | 检查点名称 |
| `-golden` | `golden/<实际文件名>` | Golden 路径 |
| `-filter` | 空 | 比对前过滤掉匹配该 Tcl 正则的整行 |

普通模式：调用 `pv_diff_files` 比较文件并输出检查点。

```tcl
set rc [pv_check_golden reports/qor.rpt \
    -golden golden/qor.rpt \
    -name qor \
    -filter {^(Date|Host):}]
```

Regolden 模式：当 `PV_CHECK_MODE` 为 `1` 或 `regolden` 时，自动创建 Golden 的父目录并强制复制实际文件，然后输出 PASS。

```tcl
set ::env(PV_CHECK_MODE) regolden
pv_check_golden reports/qor.rpt -golden golden/qor.rpt
```

未知选项只打印错误提示，过程仍会继续。调用方应保证可选参数严格成对出现。

### 6.2 `pv_diff_files`

```tcl
pv_diff_files file1 file2 ?filter_pattern?
```

- 精确逐行比较两个文件。
- `filter_pattern` 是一个 Tcl 正则；任一文件中匹配该正则的整行都会在比较前删除。
- 根据扩展名自动用 `gunzip -c` 读取 `.gz` 文件，扩展名判断不区分大小写。
- 无过滤且文件不是 `.gz` 时，直接比较原文件；否则先生成进程级临时文件 `.pv_check_file_1_<pid>.tmp` 和 `.pv_check_file_2_<pid>.tmp`。
- 使用外部 `diff -- file1 file2` 执行比较。
- 不同内容时打印最多 1,000 个字符的 diff 输出，并保留临时文件以便排查；相同时清理临时文件。

示例：

```tcl
set rc [pv_diff_files result.log golden/result.log {^(Timestamp|Elapsed):}]
set rc [pv_diff_files result.log.gz golden/result.log.gz]
```

当前实现的 `filter_pattern` 是单个正则，不是正则列表。若需忽略多类行，请使用正则分支：

```tcl
set ignore {^(Timestamp:|Host:|Elapsed:)}
pv_diff_files actual.rpt golden.rpt $ignore
```

运行依赖：系统命令 `diff`；处理 `.gz` 时还需要 `gunzip`。

### 6.3 `pv_diff_files_old`（兼容接口）

```tcl
pv_diff_files_old file1 file2 ?ignorePatterns?
```

旧实现接受“正则列表”，逐行过滤后一次性把内容读入内存。它不支持 `.gz`，并会在当前目录留下 `.pv_check_file_*_<pid>.tmp` 文件。仅为兼容旧测试保留，新代码建议使用 `pv_diff_files`。

### 6.4 `pv_diff_str`

```tcl
pv_diff_str str1 str2
```

使用 Tcl `eq` 做精确字符串比较。相同返回 `0`；不同返回 `1`，并打印两个字符串各自的前 100 个字符。

```tcl
if {[pv_diff_str $actual $expected]} {
    error "string check failed"
}
```

### 6.5 `pv_find_string`

```tcl
pv_find_string check_string file_path
```

把整个文件读入内存，并使用 `string first` 查找固定字符串，不把 `check_string` 当作正则。

- 找到返回 `0`；
- 未找到返回 `1`；
- 文件不存在返回 `2`。

```tcl
set rc [pv_find_string "Route completed" run.log]
pv_check_point route_message $rc
```

大文件或需要正则匹配时，建议改用流式扫描逻辑。

## 7. 图片 Golden 检查

### 7.1 `pv_check_golden_img`

```tcl
pv_check_golden_img \
    -mode img|dir \
    ?-tol tolerance? \
    ?-out-dir directory? \
    ?-test-pattern globPattern? \
    ?-test-dir directory? \
    -golden path \
    ?-name checkpointName?
```

公共参数：

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `-mode` | 空 | 必填：`img` 或 `dir` |
| `-tol` | `0.002` | 传给图片比较脚本的容差 |
| `-out-dir` | `.` | 比较结果输出目录 |
| `-golden` | 空 | 必填：Golden 图片、目录或归档路径 |
| `-name` | `pv_check_golden_img` | 检查点名称 |

模式专用参数：

- `img`：必须给出 `-test-pattern` 和 `-golden`。
- `dir`：必须给出存在的 `-test-dir` 和 `-golden`。

普通模式执行：

```text
python3 $PV_ROOT/scripts/image_compare.py \
  --mode <img|dir> --tol <tol> --out-dir <dir> --golden <path> \
  [--test-pattern <glob> | --test-dir <dir>]
```

`img` 示例：

```tcl
set ::env(PV_ROOT) /path/to/pv
set rc [pv_check_golden_img \
    -mode img \
    -test-pattern {snapshots/top.png} \
    -golden golden/top.png \
    -tol 0.002 \
    -out-dir image_diff \
    -name top_snapshot]
```

`dir` 示例：

```tcl
set rc [pv_check_golden_img \
    -mode dir \
    -test-dir snapshots \
    -golden golden/snapshots \
    -out-dir image_diff \
    -name snapshot_set]
```

Regolden 行为：

- `img` 模式：展开 `-test-pattern`，把匹配图片复制到 `-golden` 指定位置；若匹配多个文件，它们会依次覆盖同一目标，因此该模式宜保证只匹配一张图。
- `dir` 模式：只复制 `-test-dir` 顶层的 `*.png`，不递归且不会删除 Golden 中的旧文件。
- 当 `-golden` 以 `.tar.gz` 结尾时，`dir` 模式只警告需要手工打包，但仍输出 PASS 并返回 `0`。

运行依赖：`python3`、环境变量 `PV_ROOT`，以及 `$PV_ROOT/scripts/image_compare.py`。

## 8. 检查点汇总

### 8.1 `pv_rpt_checkpoints`

```tcl
pv_rpt_checkpoints
```

过程会：

1. 创建或覆盖 `checkpoints.log`，首行写入系统日期；
2. 从 `*.stdout` 中提取以 `Check Point:` 开头的行；若 `.pvflow_wrapper.log.tmp` 存在则只处理该文件；
3. 对重复检查点名称打印警告；
4. 统计 PASS 和 FAIL，并在终端打印最终摘要。

典型调用位置是测试脚本末尾：

```tcl
pv_rpt_checkpoints
```

运行依赖：系统命令 `date`、`echo` 和支持 `-E` 的 `grep`。

行为提示：

- 重复检查点虽然会报警，但仍计入 PASS/FAIL 总数。
- 没有日志时打印警告并返回 `0`。
- 汇总发现 FAIL 时只打印“The test case failed.”，不会自动返回非零值。
- 汇总过程内部发生 Tcl 错误时会直接 `exit 1`，而不是把错误码返回给调用者。

## 9. 嵌套列表打印

### 9.1 `pv_print_nested_list`

```tcl
pv_print_nested_list lst
```

递归遍历 Tcl 列表：元素的 `llength` 大于 1 时继续展开，否则用 `puts` 打印。

```tcl
pv_print_nested_list {{a b} {c {d e}} f}
```

输出：

```text
a
b
c
d
e
f
```

该过程按 Tcl 列表语义判断是否需要递归，因此一个包含空格、但本意是原子文本的合法列表字符串也可能被继续拆分。需要保留整段文本时，不要使用此过程。

## 10. 推荐工作流

### 10.1 文本报告

```tcl
source /path/to/pv_utils.tcl

# 产生报告
report_qor > reports/qor.rpt

# 比对；开发 Golden 时设置 PV_CHECK_MODE=regolden
set rc [pv_check_golden reports/qor.rpt \
    -golden golden/qor.rpt \
    -filter {^(Date|Host|Elapsed):} \
    -name qor_report]
```

### 10.2 命令日志片段

```tcl
source /path/to/pv_utils.tcl

set rc [pv_check_log [list report_timing] \
    -name timing \
    -log_files run.stdout \
    -match {^(WNS|TNS|Violations):}]
```

### 10.3 Route 指标

```tcl
source /path/to/pv_check_route.tcl
```

第一次生成 Golden：

```tcl
set ::env(PV_CHECK_MODE) regolden
set rc [pv_check_route [list route_design] \
    -name route \
    -log_files run.stdout]
unset ::env(PV_CHECK_MODE)
```

正常检查：

```tcl
set route_tolerance [dict create \
    "total_wire_length" 10 \
    "total_number_of_vias" 5 \
    "global_routing.horizontal_overflow" 0.05 \
    "global_routing.vertical_overflow" 0.05]

set rc [pv_check_route [list route_design] \
    -name route \
    -log_files run.stdout \
    -tolerance $route_tolerance]
```

默认生成 `route.mark`、`route.json`，并与 `golden/route.json` 比较。

### 10.4 测试结尾汇总

```tcl
pv_rpt_checkpoints
```

## 11. 已知限制与排障

1. **工作目录很重要。** 默认 Golden、`.mark`、`*.stdout`、临时文件和 `checkpoints.log` 都相对于当前工作目录，而不是相对于 Tcl 文件所在目录；只有 `pv_check_route.tcl` 对 `pv_utils.tcl` 的依赖路径按扩展文件自身目录解析。
2. **选项行为存在历史差异。** 原有多数过程遇到未知选项只打印提示；新增的 `pv_check_route` 会输出 FAIL 并返回 `2`。所有调用仍应保证选项和值成对。
3. **当前文件比对只接受单个正则。** 多个过滤条件请合并成 `(...|...)`。
4. **日志标记名不要含空白。** 否则提取时只能识别第一个非空白片段。
5. **外部命令必须可用。** 文本/汇总功能依赖 `diff`、`gunzip`、`grep`、`date`、`echo`；图片功能还依赖 `python3` 和 `image_compare.py`。
6. **`pv_diff_files` 对 `exec diff` 错误的区分有限。** 当前代码使用 Tcl `catch` 的完成码，因此外部 `diff` 不存在等系统错误也可能按“发现差异”返回 `1`，而不是文档注释期望的 `2`。
7. **差异时临时文件会保留。** 可检查 `.pv_check_file_1_<pid>.tmp` 和 `.pv_check_file_2_<pid>.tmp`；确认不再需要后再清理。
8. **Regolden 会覆盖基线。** 在 CI 或正式验证环境中应确保 `PV_CHECK_MODE` 未被误设为 `1`/`regolden`。
9. **Route JSON 是扁平数值对象。** `pv_compare_route_json` 不接受嵌套 object、array、字符串、布尔值或 `null`；这是为了保持 Tcl 8.5 环境下无需额外 JSON 依赖。生成键的各组成部分均会将空白替换为下划线。
10. **Route 汇总值采用最后一次出现。** 若日志阶段顺序变化或同一阶段重复打印指标，最终汇总键会随最后一条匹配记录变化；阶段键可用于定位来源。
11. **二维表依赖表头。** DR 表需位于 `[initial routing]` 或 `[DR iteration N]` 内并以 `drc` 开头；congestion/hotspot 表需位于 `[Global routing]` 内并使用截图所示的 `|` 分隔格式。未知表格格式会被跳过，不会猜测列含义。

## 12. 完整性校验

在 Linux 上：

```sh
sha256sum pv_utils.tcl pv_check_route.tcl
```

在 macOS 上：

```sh
shasum -a 256 pv_utils.tcl pv_check_route.tcl
```

预期结果：

```text
081692610b0ea2975eb1d7bfc404cfbc1e296380bcfe3489d4da08494cfc0c7d  pv_utils.tcl
73526abc1c669797965e23c99daf83611fac26e30e23ed1249a1f18ae3289a16  pv_check_route.tcl
```

以上是本地重构后版本的校验值；同步到 login01 时应同时更新两个 Tcl 文件并再次核对这两个值。
