---
name: eda-tester-skill
description: Generate traceable EDA Excel plans and validated TCL cases for Optimus or iTools / Innovus.
---

# EDA Test

## 通用重要规则

- 不猜测语法、MMMC、日志或结果，未知项记为 `SPEC-GAP`。Optimus target version is optional and must not block。
- 用户选择 `Smoke case`、`正向覆盖`、`负向覆盖`，多选取并集。Maximize compatible test-point coverage per case. Do not create one case per option；仅因互斥、前置或预期不同而拆分。
- 计划可追溯且预期可观察；负例写明非法构造、拒绝和不变状态。
- 每个 case 只有一个工具目录。单步用 `run.tcl`；多步才用连续 `run_1.tcl … run_N.tcl`。输入集中在 `design.tcl`，MMMC 声明式且方言隔离。
- 每个 run 完成初始化，恰好一个 `# EXPECT`、`# TEST_ACTION` 和 checkpoint，以 `pv_rpt_checkpoints`、`exit` 收尾。仅允许 `PV_ROOT`、`PV_TOOL`；禁止绝对路径和伪造结果。
- 交付前执行 Excel、TCL 语法与脚本规范检查；静态、人工和实机结果分别报告。

## 工作流程

1. 读取输入；不足时按知识库回退规则查询 EDA MCP，仍无证据则记录缺口。TXT 用 `scripts/parse_command_spec.py`。
2. 确认策略，建立需求—场景矩阵，执行人工审查。
3. Serialize the designed rows 为非空 scenarios，运行 `scripts/generate_test_plan.py`。Do not hand off an empty workbook；生成后执行 Excel 规范检查。
4. 展示 Excel 和设计。Wait for explicit user confirmation. Do not generate any TCL file before confirmation.
5. Generate one case directory per Excel row。用 `scripts/design_config.py` 生成 `design.tcl`。iTools 可用 `assets/defaults/itools/mmmc.tcl`；Do not substitute the Optimus MMMC dialect。`assets/defaults/optimus/design.tcl` 仅为 template；只有用户 explicitly selects the repository example profile 才用示例值。
6. 运行 `python3 scripts/validate.py delivery <plan.xlsx> <case_dir>... [--requirements <requirements.json>]`；Excel 与 TCL 规范检查必须全部 PASS。
7. 完成人工审查；有缺口或失败则停止。

## 参考文档索引

- 选择策略或确认设计前：`references/test-strategies.md`
- 检查 Excel 时：`references/specs/test-plan-rules.md`
- 生成或检查 case/TCL 时：`references/specs/tcl-script-rules.md`
- 设计场景及静态门禁完成后：`references/manual-review-rules.md`
- 解析 TXT 命令说明前：`references/command-spec-format.md`
- 材料不足时：`references/eda-knowledge-fallback.md`
- 查询或生成 iTools / Innovus 用例时：`references/innovus-command-corpus.md`
- 生成 Optimus full-flow 或 MMMC 时：`references/optimus-tcl-corpus.md`
