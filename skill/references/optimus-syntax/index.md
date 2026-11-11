# Optimus 静态语法检查

## 来源与覆盖范围

语法资料为用户指定的 `eda-coverage_20261015_125944/reference/all_cmd_1008.txt`，已按原字节归档为 [all_cmd_1008.txt](all_cmd_1008.txt)。

- 实际包含 **464 个命令、2,115 个参数条目**，编号 1～464；文件名中的 1008 不代表实际命令数。
- 文档快照 ID：`optimus-doc-20261015-1fa52ed045ae`。
- SHA-256：`1fa52ed045ae3d37a17fb51752478d7f2a28c0a9bbf3741fd77420e0fa07018b`。
- 来源未标注 Optimus 软件版本；快照 ID 不等于软件版本。更换资料需登记新快照并验证，不能改文件后继续使用原身份。

解析器逐行读取所有命令及表格，保留来源行号、参数类型、`[]` 可选性、枚举及数值范围；不根据文件名补造缺失命令。boolean 命名选项按表中的开关形式处理，不额外消费值；其余参数按一个 Tcl 单词消费，列表应写成一个 Tcl list 单词。表中没有说明重复性、列表多单词消费或 operation 语义时，遇到相关调用报告 `SPEC-GAP`。

## 使用

统一入口：

```sh
python3 scripts/tcl_convention_validator.py <case_dir>... --syntax
```

在项目中通过 `./init.sh test tcl <case_dir>... --syntax` 调用。同一次检查分别输出：

| 检查组 | 检查内容 |
| --- | --- |
| `TCL-SYNTAX` | Tcl 原生语法解析、已识别控制体/表达式与嵌套脚本语法 |
| `OPTIMUS-COMMANDS` | 快照内命令、选项、必选参数、参数数量、静态类型/枚举/范围与明确约束 |
| `TCL-CONVENTIONS` | 既有用例结构、初始化、PV 检查点、命名、归档和编程规范 |

`--syntax-db <all_cmd_1008.txt>` 可显式指定同一 SHA-256 快照；文件缺失或身份不匹配时不可用。工具版本不作为输入或匹配门禁；使用命令资料快照进行检查，无需询问版本。当前仅支持 Optimus 命令库，iTools 会明确报告 `TOOL_UNAVAILABLE`。

不加 `--syntax` 保留历史的规范检查模式，不能据其 PASS 宣称已完成语法校验。Skill 交付流程必须使用 `--syntax`；历史开发回归和规范 API 保持兼容，不能把历史回归通过当作完整语法检查通过。

## 解析与裁决

依赖可加载的 Tcl **8.5 或 8.6 共享库**，调用 `Tcl_ParseCommand`、`Tcl_ParseExpr`、`Tcl_SplitList` 等解析 API；不创建解释器，不执行输入命令，不 source 用户脚本，不需要 EDA 许可证。Tcl 9 ABI 不兼容时不尝试强行解析；只有 tclsh 可执行文件、却没有兼容共享库时同样报告工具不可用。

- 解析换行、分号、注释、引号、花括号、转义、续行、变量与命令替换，不用正则代替 Tcl 语法解析。
- 检查命令替换、PV log/qor/route 的命令块、proc、if、while、for、foreach/lmap/foreach_in_collection、catch/time、静态 eval/uplevel、try/switch、apply 及 namespace eval 中的脚本。表达式中的命令替换也会检查。
- 对检查集合中的静态 source 文件，在不执行文件的情况下顺序分析其 AST；仅传播可证明的简单 `set` 字面值。控制流、helper 和其他可能修改变量的调用后不沿用过期常量。外部 PV 入口是明确的运行时依赖，PV API 的参数仍由既有规范检查和语义审查负责。
- 动态命令名、无法解析的参数展开、需要静态类型/枚举证明的动态值、动态脚本/外部 source、subst/interp/外部进程或其他未覆盖分发形式报告 `SPEC-GAP`；不执行这些内容以探测结果。
- 明确约束包括 report_qor 阶段必须恰好选择一个，以及 delete_tie_high_low 至少选择 cell/prefix 之一。其他未声明的互斥、依赖或重复性不作猜测。
- 未知命令按快照与本地 proc 集合拒绝；可能是拼写错误，也可能超出资料范围，不能据此声称目标软件不存在该命令。
- 检查不证明设计数据库对象存在、PDK 合法性、set_options 属性键的有效性、运行阶段正确性或 EDA 结果符合预期；这些仍需语义审查与目标工具验证。

结果为 `PASS`、`FAIL`、`SPEC-GAP` 或 `TOOL_UNAVAILABLE`，仅全部 PASS 返回退出码 0。报告包含源行号、快照 ID、实际检查次数和未解决项；源文档的软件版本仍为 null。故意调用非法选项的负向用例也会被静态检查报告，不能仅凭 `EXPECT: FAIL` 跳过或豁免；需要先明确可验证的负向测试验收契约。

本资料定义的是 **464 命令文档快照范围内的静态校验**，不是完整 Optimus 软件语言或所有动态 Tcl 程序的可执行性证明。
