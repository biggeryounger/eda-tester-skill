---
name: eda-tester-skill
description: Design EDA test cases from command specifications or generate validated TCL cases from an existing Excel test plan for Optimus or iTools / Innovus.
---

## Workflow

统一 Workflow 按已有输入衔接步骤。开始前读取 [输入规则](rules/input-rules.md)，设计与交付遵守 [输出规则](rules/output-rules.md)。已有测试用例设计表跳过步骤 2，进入步骤 3；新设计依次执行全部步骤。

### 1. 接收输入

读取用户提供的被测命令说明、命令帮助、自然语言测试需求或已有测试用例设计表，确定目标工具。

- 输入为 TXT 命令说明时，运行 `scripts/parse_command_spec.py` 生成结构化命令规格；解析缺口记录为 `SPEC-GAP`。

### 2. 补齐用例设计

**WAIT-STRATEGY**
- 等待内容：用户选择一个或多个测试策略（`Smoke case`、`正向覆盖`、`负向覆盖`）。
- 继续条件：用户明确给出至少一个策略；仅补充命令资料或含糊回复不能解除等待。

将用例设计整理为至少包含一条有效用例的结构化场景数据，运行 `scripts/generate_test_plan.py`，从模板生成测试用例设计表。

### 3. 验证测试计划

对设计表执行检查：

- **执行脚本结构检查**：运行 `python3 scripts/test_plan_validator.py <plan.xlsx> [--requirements <requirements.json>]`，检查工作簿结构、字段格式、编号和其他确定性规则，结果必须为 `PASS`。
- **执行 Agent 语义审查**：读取 `references/specs/test-plan-rules.md`，结合被测命令说明和目标工具逐条审查用例语义，记录每条规则的 `PASS`、`FAIL` 或 `SPEC-GAP` 及理由。
- 两项均通过后才能把表格作为脚本生成输入。新设计检查失败时先修正并重新验证；已有表格的失败项或未处理的 `SPEC-GAP` 进入 `WAIT-PLAN-FIX`。

### 4. 确认设计与运行输入

读取 [输入件管理表](assets/输入件管理表.json) 的 `smic180` 对象，作为本次运行的工艺输入来源；

**WAIT-DESIGN-CONFIRMATION**
- 等待内容：用户明确确认当前用例设计可用于生成 TCL
- 继续条件：用户回复“确认”“可用”“按此生成”或等价的明确批准

**WAIT-PLAN-FIX**
- 等待内容：用户补充或修正列出的问题，或提供修订后的测试用例设计表。
- 继续条件：所有阻塞问题均已获得明确且一致的输入。

### 5. 脚本生成与交付门禁

脚本输出件必须参考 `references/examples/` 中的用例目录结构、运行入口及对应工具的 TCL 脚本组织方式，并结合当前用例设计和以下模板生成。

1. 每条 Excel 用例生成一个用例目录。必须参考 `assets/templates/tool_cmd/common/design.tcl` 和 `assets/templates/tool_cmd/<tool>/` 下的 `init.tcl`、`mmmc.tcl` 模板，生成对应目标工具的 TCL 脚本；工艺目录、LEF 和 LIB 路径使用步骤 4 中输入件管理表的 `smic180` 配置。
2. **执行脚本静态检查**：
   - **强制直接调用门禁**：所有工具均必须先运行 `python3 scripts/tcl_convention_validator.py <case_dir>...` 并取得 `PASS`，不得只运行工具命令检查器或以人工审查替代。

   - Optimus：运行 `python3 scripts/tcl_convention_validator.py <case_dir>... --syntax` 完成脚本检查，并按 `references/specs/tcl-script-rules.md` 完成规则语义检查；两项均通过后方可交付。
   - iTools：运行 `python3 scripts/tcl_convention_validator.py <case_dir>...` 和 `python3 scripts/itools_check.py <case_dir>/tcl/design.tcl <case_dir>/tcl/itools/*.tcl --format json`（包含其他本地 source 文件）完成脚本检查，并按 `references/specs/tcl-script-rules.md` 完成规则语义检查；
3. 只有两个专项静态检查脚本和两份语义规范审查全部通过后才可交付，对每条适用规则记录 `PASS`、`FAIL` 或 `SPEC-GAP`；任何 `FAIL` 或未解决的 `SPEC-GAP` 都必须停止交付。

   **WAIT-SCRIPT-DELIVERY-FIX**
   - 等待内容：用户补充或确认语义缺口、修正失败的设计/脚本，或提供可用的目标工具静态检查环境与命令资料库。
   - 继续条件：全部 `FAIL`、`SPEC-GAP` 和 `TOOL_UNAVAILABLE` 已消除，且上述门禁重新执行后全部通过；等待期间不得交付。

## 参考文档索引
- 脚本输出件示例：`references/examples/`
- 选择策略或确认设计前：`references/test-strategies.md`
- 解析 TXT 命令说明前：[输入格式与命令解析规则](rules/input-rules.md)
- iTools initial design 模板：`assets/templates/tool_cmd/itools/init.tcl`
- Optimus initial design 模板：`assets/templates/tool_cmd/optimus/init.tcl`
- 通用 design.tcl 模板：`assets/templates/tool_cmd/common/design.tcl`
- iTools MMMC 模板：`assets/templates/tool_cmd/itools/mmmc.tcl`
- Optimus MMMC 模板：`assets/templates/tool_cmd/optimus/mmmc.tcl`
- 编写 PV 检查点前：`references/pv-checkpoints/index.md`（PVUtils / QoR 接口手册及门禁差异）
