# EDA 命令说明 TXT 解析格式

## 1. 用途

使用 `scripts/parse_command_spec.py` 将包含一个或多个 EDA 命令说明的 UTF-8 TXT 转换成版本化 JSON。该 JSON 是后续生成 Nagelfar syntax database 和确定性 option 关系检查规则的输入，不直接等同于 Nagelfar 数据库。

如果尚未取得 TXT，可在已经启动的 Optimus 等 Tcl 工具会话中批量打印命令帮助：

```tcl
source scripts/dump_tool_help.tcl
eda_dump_all_help *
```

`eda_dump_all_help report_*` 只采集匹配名称的命令；`eda_dump_command_help {report_qor check_design_data}` 只采集显式列表。脚本跳过标准 Tcl 内建命令，为每个工具命令执行 `<command> -help`，一个命令失败时继续处理其余命令，并最终打印成功/失败汇总。通过工具自身的日志功能或终端重定向将完整输出保存为 TXT，再交给解析器。

```sh
python3 scripts/parse_command_spec.py commands.txt commands.json
```

解析报告同时写到标准输出。存在 `error` 诊断时返回非零退出码，且不生成或覆盖输出 JSON；只有 warning 时可以生成 JSON。

## 2. 推荐输入结构

支持英文或中文字段名。`Tool/工具` 和 `Version/版本` 会被后续命令块继承，直到出现新值。

```text
Tool: Optimus
Version: 21.1
Command: check_design_data
Syntax: check_design_data -file <String> [-netlist]
Options:
-file <String> (required) Report output path. Exactly one value.
-netlist (optional) Flag; takes no value.
Constraints:
- -netlist requires -file
Version Differences:
- 22.1: added -mode; removed -legacy
```

每个新命令必须以 `Command:` 或 `命令:` 开始。支持以下段落标题：

- `Options`、`Option`、`Parameters`、`选项`、`参数`
- `Constraints`、`Relationships`、`约束`、`关系`
- `Version Differences`、`版本差异`

## 3. 可确定提取的语义

- option 必选性：`[]` 内为可选，`{}` 内或无括号为必选；显式的 `required`、`mandatory`、`必选`、`必须`与该规则一致。
- 参数数量：显式 `<Type>`、`一个参数`、`takes no value`、`不带参数`等。
- 基本类型：boolean、integer、number、string、path、enum、unknown。
- 枚举：`<full|quick>` 或 `Values: full, quick`。
- 可重复性：`repeatable`、`可重复`、Syntax 后缀 `...`；Syntax 中单次出现且无 `...` 时为 false。
- 关系：requires/依赖、mutually exclusive/互斥、at least one/至少一个。Syntax 中 `{ -a | -b }` 解析为 `exactly_one` 必选组合。
- 版本差异：按版本记录 added/新增和 removed/移除的 option。

## 4. JSON约束

根对象包含：

- `schema_version`：当前为 `1.0`。
- `source`：输入文件来源。
- `commands`：命令结构数组。
- `diagnostics`：结构化错误、警告和信息缺口。

每个 option 包含 `required`、`argument.count`、`argument.type` 和 `repeatable`。原文不能确定的布尔字段使用 `null`，不能确定的参数类型使用 `unknown`，同时产生 `SPEC-GAP` warning。不得由 Agent 补猜缺失事实。

关系引用未声明 option、缺少命令声明或输入不可读属于 error。此类结果不得用于生成语法检查规则。
