# PV 检查点参考

资料来源：用户指定的 `e2_pv_kit/legacy/pv_check_bundle_20261012` 两份手册，归档日期 2026-10-20。用于接口查询，不表示已验证当前部署的 PV 版本；实际接口冲突时需核对目标环境，不推测兼容。

- [PVUtils 使用手册](pv_utils_manual.md)：基础检查点、日志、文件/图片 Golden、Route 扩展及汇总；文档标注 PVUtils 1.1.1、Route 1.3.3。
- [QoR 使用与实现手册](pv_check_qor_usage.md)：更新日期 2026-09-22，涵盖 QoR 参数、平铺 JSON、容差、返回码及支持范围。

## 生成检查点时的接口选择

每个 `pv_check_log` 命令块最多包含 4 条顶层 Tcl 命令；超过时拆分为多个独立命名的检查点。按换行或分号计数，注释、空语句和续行不计，参数内的分隔符不拆分命令；该静态计数不展开 proc、循环或动态脚本。

按用例预期选择下列场景；命令、指标键、Golden 和容差须来自已确认的设计与目标工具版本。以下覆盖主检查点的公开选项，完整签名和默认值见两份手册。标有“门禁缺口”的能力目前仅作接口参考，不能直接作为可交付脚本。

| 检查方式 | 使用场景 | 选项组合与判定 |
| --- | --- | --- |
| `pv_check_log` | 检查查询、报告命令的稳定输出 | `{command} -name query_state`；捕获为 `query_state.mark`，默认与 `golden/query_state.mark` 比较；`-name` 应唯一且不含空白，省略时使用命令首元素。 |
| `pv_check_log` | 同一命令验证不同选项组合 | 每个组合使用不同 `-name`，分别维护对应 `.mark` Golden，避免覆盖输出或混用基线。 |
| `pv_check_log` | 检查指定诊断消息或负向用例提示 | `-match {<预期诊断正则>}` 提取目标行并做 Golden 比较；不是“匹配到就通过”。Golden 应含预期诊断，且不能遗漏需要检测的其他错误。 |
| `pv_check_log` | 排除日期、主机等不稳定行 | `-filter {^(Date|Host|Elapsed):}`；比对时从实际和 Golden 两边排除整行。多个条件合为单个 Tcl 正则。 |
| `pv_check_log` | 多日志、包装器日志或明确的运行日志来源 | `-log_files {run_1.stdout run_2.stdout}`；可与 `-name/-match/-filter` 组合。默认优先 `.pvflow_wrapper.log.tmp`，否则扫描 `*.stdout`；无默认日志时依赖 EDA `redirect` 捕获。 |
| `pv_check_golden` | 比较生成的稳定文本报告、LEF 或结构化查询结果 | `out_file -golden golden/result.rpt`；逐行精确比较；省略 `-golden` 时使用 `golden/<实际文件名>`。同一 run 内先清理旧文件、生成新文件，再比较；CMD 用例不得以 DEF 作 Golden。 |
| `pv_check_golden` | 比较带时间戳的报告或压缩输出 | `out_file -filter {^(Date|Host):}`；过滤两边整行。实际文件不存在但同名 `.gz` 存在时自动读取压缩文件，依赖 `diff/gunzip`。 |
| `pv_check_golden` | 将业务检查点名称与报告路径分开 | `out_file -name report_state -golden golden/result.rpt`；默认名为原始 `out_file` 字符串。**门禁缺口：`-name`**。 |
| `pv_check_qor` | 对单条 timing/QoR 报告做严格指标回归 | `{report_qor <目标版本选项>} -name post_place -golden ./golden/post_place.json -dir ./out`；省略 `-name` 使用首条命令名，默认 Golden 为 `golden/<name>.json`，默认输出目录为当前目录。不配容差时数值零容差、文本精确比较。 |
| `pv_check_qor` | 一个阶段同时检查 timing 与 QoR，或多次 timing 查询 | `cmd_block` 放入多条受支持命令；JSON 键按命令区分，重复命令用稳定 `_1/_2` 序号。支持 report_timing/report_qor，iTools timeDesign 归一到 QoR parser。跨工具共用 Golden 时显式使用相同 `-name`，并先确认键与指标语义一致。 |
| `pv_check_qor` | 不同指标使用不同绝对容差 | `-tolerance [dict create <完整指标键或glob> <非负容差>]`；未匹配指标的容差为 0，每个 pattern 必须在当前与 Golden 两边均命中。历史拼法 `-tolorance` 和单个数值仍兼容，新调用优先使用标准拼法与字典。**门禁缺口：字典及历史拼法**。 |
| `pv_check_qor` | 对不同量级指标设相对容差，或结合绝对容差 | `-rel_tolerance [dict create <完整指标键或glob> 0.02]` 表示允许 2% 相对差；可与 `-tolerance` 组合，满足任一个即通过。精确键优先于 glob；glob 选最具体者，同等具体但值不同则报配置错误。**门禁缺口：字典**。 |
| `pv_check_qor` | 忽略已说明原因且不属于被测预期的指标 | `-ignore_metrics {<完整指标键或glob> ...}`；指标仍输出但不参与判定，每个 pattern 至少命中当前或 Golden 的一个指标；不能靠忽略被测指标获得 PASS。**门禁缺口：该选项**。 |
| `pv_check_qor` | 分阶段留存当前指标，暂不比较基线 | `-name post_place -dir ./out -no_check`；只捕获并写 JSON，不读取或更新 Golden，不生成 diff，清除同名旧 diff；捕获成功返回 0，不能据此声称指标回归通过。**门禁缺口：`-no_check`**。 |
| `pv_rpt_checkpoints` | 每个 run 末尾汇总所有检查点 | 无参数；从日志提取 `Check Point:` 行写入 `checkpoints.log` 并统计 PASS/FAIL，随后按用例约定退出。重复名称会警告但仍计数。发现 FAIL 不自动返回非零值，无日志也可能返回 0，必须检查真实检查点结果，不能仅看退出码。 |

QoR 的当前结果和 diff 均为平铺 JSON；没有公开 `-stage`、CSV 格式选择或 debug 开关。`-dir` 控制 `<name>.json`、`<name>.diff.json` 和 `<name>.result.log` 的目录，`<name>.mark` 保留在当前工作目录。Density 使用比例小数，如 60% 写为 0.6，容差必须使用相应指标单位。

正式验证使用已有且来源明确的 Golden。两份手册的 regolden 模式说明仅用于基线维护：`PV_CHECK_MODE=1/regolden` 会更新基线，QoR 的 `-no_check` 优先于该模式。Skill 生成的正式用例不得自行开启 regolden，缺失基线不能靠当次输出自动补成 PASS。

QoR 返回码：0 为比较通过或 regolden 成功（`-no_check` 捕获成功也为 0），1 为比较不一致，2 为参数、环境、捕获、解析或文件条件错误。基础过程存在历史差异，不能将此严格约定套用于所有 proc。

## 与当前 Skill 门禁的边界

- 来源中的 regolden 示例用于说明接口。生成的正式用例不得自行设置 `PV_CHECK_MODE` 或覆盖 Golden；沿用当前 Skill 的基线和结果真实性约束。
- 当前 TCL 静态检查器仅接受 QoR 数值容差，尚不支持手册中的字典容差、`-ignore_metrics`、`-no_check`，且 `pv_check_golden` 尚不接受 `-name`。这些是已知接口覆盖缺口；需要使用时记录 `SPEC-GAP` 并停止交付，不得绕过检查或把字典容差擅自改写为单个数值。本次仅更新资料，不修改检查器。
- Route、图片及基础辅助 proc 作为查询资料保留，不因此扩展 Skill 当前认可的检查点集合（log/golden/qor）。
- 每个 run 仍需独立检查点，最后汇总并退出；PASS/FAIL 应结合真实返回码与检查点日志裁决，不能只看脚本退出码或文件存在。mock 和文档核对不代表 EDA 实机通过。
