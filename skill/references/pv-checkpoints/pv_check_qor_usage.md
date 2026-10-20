> 资料归档：2026-10-20；来源：`e2_pv_kit/legacy/pv_check_bundle_20261012/docs/pv_check_qor_usage.md`；原文 SHA-256：`9ceab436d9804092b25abcd6a91dd3716c4167cc3c2f02c307f18752b70a6e06`。
> 已将原文部署绝对路径替换为 PV_ROOT 示例，并移除未归档附件的链接。原文中的项目约束与 regolden 示例属于来源背景，生成用例时以 Skill 当前规则为准。版本范围和门禁差异见 [检查点参考入口](index.md)。

# pv_check_qor 使用与实现手册

更新日期：2026-09-22。以当前仓库中的 `pv_check_qor.tcl` 为准。

Density 以浮点比例小数写入 JSON，例如报告中的 `60.000%` 输出为数值 `0.6`。

`pv_check_qor` 在 Optimus 或 iTools Tcl Shell 中执行受支持的报告命令，提取 QoR/Timing 指标，写出平铺 JSON，并与 JSON Golden 比较。本手册同时说明公开用法和当前实现链路。

## 加载与环境

```tcl
source /absolute/path/to/pv_check_qor.tcl
# 可选：set ::env(PV_TOOL) itools
```

`pv_check_qor.tcl` 会从自身所在目录加载同级 `pv_utils.tcl`。部署时两个文件必须位于同一目录。项目禁止修改 `pv_utils.tcl`；QoR 适配均位于 `pv_check_qor.tcl`。

`PV_TOOL` 是可选的。未设置、空值、`default` 和 `optimus` 都使用默认
Optimus 解析；只有 iTools 需要显式设置 `set ::env(PV_TOOL) itools`。值不区分
大小写，前后空白会被忽略。为了兼容旧调用，环境变量不存在时，
仍会读取 Tcl 全局变量 `::PV_TOOL`；环境变量优先。其他值会返回错误码 `2`。

脚本使用 `::pv_utils_loaded` 作为共享加载标志：未加载时才 `source`
同级 `pv_utils.tcl`，成功后置为 `1`，避免在同一 EDA Tcl Shell 中多次
`source pv_check_qor.tcl` 时重复加载 PVUtils。

## 调用格式

```tcl
pv_check_qor {cmd_block} \
    ?-name <checkpoint>? \
    ?-golden <path.json>? \
    ?-tolerance <toleranceDict>? \
    ?-rel_tolerance <toleranceDict>? \
    ?-ignore_metrics <patterns>? \
    ?-dir <dir>? \
    ?-no_check?
```

| 参数 | 默认值 | 说明 |
|---|---|---|
| `-name` | 首条命令名 | 检查点名称和输出文件前缀 |
| `-golden` | `golden/{name}.json` | 平铺 JSON golden |
| `-tolerance` | 空字典，即所有键为 `0` | Tcl dict：完整 JSON 键与允许的最大绝对差值 |
| `-rel_tolerance` | 未启用 | Tcl dict：完整 JSON 键或 glob 与允许的最大相对差值 |
| `-ignore_metrics` | 空 | 按完整键或 glob 忽略比较；指标仍保留在当前结果中 |
| `-dir` | 当前目录 | 当前结果和 diff 的输出目录 |
| `-no_check` | 未启用 | 只捕获并写当前指标 JSON；不读取或更新 Golden，不执行比较，不生成 diff |

输出格式固定为平铺 JSON，不提供格式选择参数。

## 只输出当前指标

相邻流程步骤需要保留不同检查点名称、暂时不做 Golden 比较时，使用无参数
选项 `-no_check`：

```tcl
pv_check_qor {report_qor -place} \
    -name post_place \
    -dir ./output \
    -no_check
```

该调用写入 `./output/post_place.json`，跳过 Golden 路径检查、Golden 更新和
指标比较，并清除同名的旧 diff。`-no_check` 优先于环境中的 regolden 模式；
命令执行、报告解析、参数或输出文件错误仍返回条件错误码 `2`。公共检查点结果
仍会正常输出，成功时返回 `0`。

## 基本示例

```tcl
pv_check_qor {
    report_timing -view view14
    report_qor -place
} -name post_place \
  -golden ./golden/post_place.json \
  -dir ./output \
  -tolerance [dict create \
      post_place.report_qor.sta.timing.setup.wns.worst.all 0.01]
```

支持的公开 parser 为 `report_timing` 和 `report_qor`；iTools 的 `timeDesign` 会按既有分发规则规范化到 QoR parser。一个命令块内重复命令使用稳定序号，例如 `report_timing_1`、`report_timing_2`。

## 平铺 JSON 协议

当前结果、golden 和 diff 全部使用 JSON object。当前结果的每个键都是完整点分路径：

```json
{
  "post_place.report_qor.sta.timing.setup.wns.worst.all": -0.125,
  "post_place.report_timing.path_1.endpoint": "u_core/state_reg/D",
  "post_place.report_timing.path_1.startpoint": "input_a"
}
```

- 数值保持 JSON number，参与绝对/相对容差比较。
- 起点、终点、`N/A` 等文本保持 JSON string，按字符串精确比较。
- 键按字典序写出，比较按完整键身份进行，不依赖文件中的行序。
- 重复完整键会被拒绝，不会静默覆盖。
- `report_qor` / `timeDesign` 的 DRV 键使用
  `<checkpoint>.sta.drv.<type>.<group>`；timing 键使用
  `<checkpoint>.sta.timing.<mode>.<metric>.<group>`，其中 group 始终是最后一级。
  当整份报告没有 views 表格时，在 group 前加入 `worst`，例如
  `route.sta.timing.setup.wns.worst.reg2reg`。
- 带 analysis view 的 timing 键在 group 前加入 `views.<view>`，例如
  `route.sta.timing.setup.wns.views.slow_view.reg2reg`。
- 显式 `-name` 优先级最高，并完整参与 JSON 键名，不自动删除或改写
  `itools`、`optimus` 等组件。例如 `-name itools.qor` 生成以
  `itools.qor.` 开头的键。需要跨工具共用 Golden 时，应由调用方为两种工具
  传入相同的 `-name`。

| 文件 | 产生条件 |
|---|---|
| `{dir}/{name}.json` | 命令成功解析后总是写出 |
| `{dir}/{name}.diff.json` | check 模式实际完成比较后写出 |
| `{dir}/{name}.result.log` | 每次公开调用写出一次最终检查点结果 |
| `{name}.mark` | PVUtils 从运行日志中提取的命令块，保留在当前工作目录 |
| `golden/{name}.json` | 默认 golden；仅 regolden 模式更新 |

每次调用会先移除同名旧 diff，避免捕获、解析或缺少 golden 时误用历史结果。
实现不创建、读取或比较 CSV；目录中既有的 `.csv` 是旧版本遗留文件，不代表
本次调用的输出。

diff 同样为平铺 JSON，直接以完整指标键作为前缀，例如：

```json
{
  "post_place.report_qor.sta.timing.setup.wns.worst.all.abs_tol": 0.01,
  "post_place.report_qor.sta.timing.setup.wns.worst.all.delta": -0.100,
  "post_place.report_qor.sta.timing.setup.wns.worst.all.rel_delta": 0.800000,
  "post_place.report_qor.sta.timing.setup.wns.worst.all.rel_tol": 0.05
}
```

每个差异直接以当前 JSON 的完整指标键为前缀，固定展开为 `.delta`、
`.rel_delta`、`.abs_tol` 和 `.rel_tol` 四个键，不再使用 `diff_N`，也不单独
保存 `check_point_name` 或 `key`。未启用相对容差，或差异为文本/单边缺失而
无法计算时，对应字段写为空字符串。比较状态、当前值、Golden 值和说明保留在
内部逻辑及 `[DIFF]` 日志中，不写入公开 diff JSON。
除写出 diff JSON 外，每项未忽略差异还会按照 Route 检查器的方式在运行日志中
打印一行 `[DIFF]`，包括完整键、当前值、Golden 值和差异状态；数值不一致时还
包括绝对差值和相对差值。

## Regolden

```tcl
set ::env(PV_CHECK_MODE) 1
pv_check_qor {report_qor -place} -name post_place
unset ::env(PV_CHECK_MODE)
```

`PV_CHECK_MODE=regolden` 与 `1` 等价。regolden 成功时，当前 JSON 仍保留在输出目录，并复制为指定或默认 golden。捕获或解析失败时不会更新 golden。

正常 check 模式缺少 golden 时，命令仍会执行并写出当前 JSON，然后返回 `2`；不会自动建立 golden，也不会生成 diff。

## 返回码与日志

| 返回码 | 含义 |
|---|---|
| `0` | 比较通过，或 regolden 成功 |
| `1` | 指标比较不一致 |
| `2` | 参数、环境、捕获、解析或文件条件错误 |

公开入口会捕获内部 Tcl error，并以返回码表示结果。每次调用只输出一个最终 `Check Point: <name> PASS|FAIL`。

命令捕获直接委托给 PVUtils 1.1 的 `__pv_check_log_common`：一次 `pv_check_qor` 调用只建立一个公共 marked-log 捕获，只打印一组以检查点名称命名的 PV_MARKER，并保留 `<name>.mark`，与 `pv_check_log` 的命名规范一致；例如 `-name itools.report_qor` 生成 `itools.report_qor.mark`。命令块内部仍逐条执行、单独记录执行状态，并在每条命令前打印 `[CMD] <command>`；单条命令失败不会阻止后续命令执行。捕获完成后，QoR 只以这些 `[CMD]` 行为边界，在函数内部拆分各命令输出并分别进行 parser 分发。redirect 形式和默认日志选择由 PVUtils 管理；平铺 JSON、Golden 比较、返回码和一次最终 Check Point 仍由 `pv_check_qor` 管理。生成的 `.mark` 在解析后保留，供问题定位和人工检查。

## 容差配置

绝对容差采用与 `pv_check_route` 相同的字典配置，并扩展支持 glob：

```tcl
set qor_tolerance [dict create \
    post_place.timing.setup.*.* 0.01 \
    post_place.placement.density 0.10]

pv_check_qor {report_qor -place} \
    -name post_place \
    -tolerance $qor_tolerance
```

字典键可以是平铺 JSON 的完整键或 glob。只有匹配配置的键使用自定义绝对
容差，其他键的绝对容差为 `0`。每个 pattern 必须在当前 JSON 和 golden JSON
中都至少匹配一个键，容差必须是非负数，否则返回 `2`。兼容 `pv_check_route` 的历史拼法
`-tolorance`，新调用建议使用 `-tolerance`。

每个配置项采用：

```text
abs(current[key] - golden[key]) <= toleranceDict[key]
```

原有单个数值写法暂时作为兼容模式保留，但新配置应使用按键字典。

相对容差使用完全相同的多指标和通配配置方式：

```tcl
set qor_rel_tolerance [dict create \
    post_place.timing.setup.*.wns 0.02 \
    post_place.timing.setup.*.tns 0.05 \
    post_place.placement.* 0.01]

pv_check_qor {report_qor -place} \
    -name post_place \
    -tolerance $qor_tolerance \
    -rel_tolerance $qor_rel_tolerance
```

精确完整键优先于 glob；没有精确键时，使用字符数最长、最具体的匹配
pattern。同等具体但值不同的重叠 pattern 会作为歧义配置返回 `2`。绝对和
相对容差满足任意一个即可通过。未匹配相对容差配置的指标不启用相对容差。

## 指标忽略

```tcl
pv_check_qor {report_qor -place} \
  -name post_place \
  -ignore_metrics {post_place.report_qor.timing.*.tns *.placement.density}
```

配置值是完整点分 JSON 键或 glob pattern 的 Tcl list。被忽略的指标保留在
当前 JSON，不计入 PASS/FAIL。若其进入 diff 内部记录，公开 diff JSON 仍只写
`.delta`、`.rel_delta`、`.abs_tol` 和 `.rel_tol`，不写 `IGNORED` 状态字段。
每个 pattern 必须至少匹配当前或 Golden 中的一个指标，否则按配置错误返回
`2`，避免键名拼错后静默失效。

## 支持范围

- 公开命令 parser：`report_timing`、`report_qor`；iTools `timeDesign` 规范化为 `report_qor`。
- Optimus `report_timing` 支持 Startpoint/Endpoint 长名称在边沿标注前换行；解析时会去掉报告换行产生的空白并拼回完整名称。无约束输出格式若没有 `data arrival time` 汇总行，会从 `arrival time <value>` 表头提取 `data_arrival_time`。
- 保留时序、QoR、DRV、布局密度、拥塞、线长、via、DRC 等已有非 performance 指标。
- 不提取 runtime、memory、clock 等 performance 指标。
- 不自动识别 stage；内部 parser 显式收到 stage 时才使用它，公开 `pv_check_qor`
  没有 `-stage` 参数。
- 不支持 CSV、格式选择或 debug 开关；公开数据文件统一为平铺 JSON。

## 实现方式

### 1. 加载与公开边界

`pv_check_qor.tcl` 用 `[info script]` 定位自身，加载同级 `pv_utils.tcl`。公开入口
`pv_check_qor` 调用内部 `pv_check_qor_impl`，把 Tcl 异常统一转换为 `0/1/2`，并且
无论成功还是失败都只输出一个最终 Check Point。

### 2. 命令块执行与 marked-log

1. 展开命令块中的 Tcl 变量，拆分为多条逻辑命令。
2. 将整个命令块只交给一次 PVUtils `__pv_check_log_common`，因此一次调用只有
   一组 `PV_MARKER begin/end` 和一个 `<name>.mark`。
3. `pv_qor_execute_command_block` 仍逐条执行命令；每条命令前通过 `pv_stdout_line`
   打印 `[CMD] <command>`，这行既是命令提示，也是后续拆分的唯一边界。
4. 每条命令单独 `catch`并保存执行状态；某条命令失败不阻止后续命令执行，
   但整个检查点最终按错误处理。
5. PVUtils 负责 redirect 和日志选择：优先 `.pvflow_wrapper.log.tmp`，其次已有
   `*.stdout`；需要自行 redirect 时生成 `<name>.pvlog`。PVUtils 再按 Marker 提取
   `<name>.mark`，QoR 保留该文件。

`[CMD]` 行由 `pv_check_qor` 的命令块执行层打印，不是 EDA 命令自身输出。

### 3. 分块、分发与指标命名

`pv_qor_split_command_capture` 读取整个 Mark 内容，严格核对 `[CMD]` 数量、顺序和
命令文本，然后把每段日志与对应的执行状态合并。`pv_parse_dispatch` 根据
`::pv_parser_registry` 调用 `report_timing` 或 `report_qor` parser；`timeDesign` 先转换为
`report_qor` 的规范命令名。

解析后的指标先规范化为内部 metric row，再生成公开平铺键：

- 单命令：`<name>.<metric_path>`。
- 多命令：`<name>.<canonical_command>.<metric_path>`。
- 同名命令重复：按出现顺序增加 `_1`、`_2` 等后缀。
- 多条 timing path：使用 `path_1`、`path_2` 等稳定序号。

### 4. JSON、Golden 与比较

1. 先写 `{dir}/{name}.json`；命令或解析失败时保留当前结果，跳过比较。
2. regolden 模式仅在所有命令执行和解析成功后更新 Golden。
3. check 模式按完整键名对齐 current 与 Golden，处理单边缺失、文本差异和数值差异。
4. `-ignore_metrics`、`-tolerance` 和 `-rel_tolerance` 都支持完整键和 glob；容差
   精确键优先，glob 按最具体匹配选择。
5. 未忽略差异打印 Route 风格 `[DIFF]` 日志，同时写成以完整指标键为前缀的
   `{dir}/{name}.diff.json`。
6. 每次开始执行前删除同名旧 diff，防止失败时误读历史结果。

### 5. 结果收口

内部结果 `PASS`、`FAIL`、`REGOLDEN` 在公开入口统一映射为 `0/1/0`；参数、
环境、命令捕获、解析和文件错误映射为 `2`。最后只由公开入口写一次
`Check Point: <name> PASS|FAIL`及 `{dir}/{name}.result.log`，避免 PVUtils 内层检查点与
QoR 公开检查点重复。


## 离线日志解析器

`tools/parse_metrics_log.tcl` 是独立工具，不是 `pv_check_qor` 的公开输出路径。它固定输出与主流程一致的平铺 JSON。原资料另附 offline_log_parser.md（不在本次归档范围）。

## 验证边界

本仓库回归使用脱敏 mock fixture。mock 通过不代表真实 Optimus/iTools Shell 集成通过；真实工具验证需单独记录版本、命令和脱敏结果。
