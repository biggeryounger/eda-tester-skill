---
name: eda-tester-skill
description: Design EDA test cases from command specifications or generate validated TCL cases from an existing Excel test plan for Optimus or iTools / Innovus.
---

## Workflow

先根据用户输入选择且只执行以下一个场景；两个场景最终进入同一套“脚本生成与交付门禁”。

### 场景一：从命令说明设计新用例

当用户输入被测命令说明、命令帮助或自然语言测试需求，且尚无测试用例设计表时：

1. 输入为 TXT 命令说明时，先运行 `scripts/parse_command_spec.py` 生成结构化命令规格；解析缺口记录为 `SPEC-GAP`。
2. 若用户尚未明确选择测试策略，立即进入等待门禁：

   **WAIT-STRATEGY**
   - 等待内容：用户选择一个或多个测试策略（`Smoke case`、`正向覆盖`、`负向覆盖`）。
   - 继续条件：用户明确给出至少一个策略；仅补充命令资料或含糊回复不能解除等待。

   策略明确后，根据命令规格清单建立需求—场景矩阵。Maximize compatible test-point coverage per case；Do not create one case per option。只有测试点冲突、初始化不同或预期无法共同观察时才拆分用例。分别检查场景覆盖率和被测选项覆盖率；两项均报告分子、分母、百分比和未覆盖项。执行所需工具或版本语法库不可用时报告 `TOOL_UNAVAILABLE`，不得以人工判断替代。
3. 将用例设计整理为至少包含一条有效用例的结构化场景数据，运行 `scripts/generate_test_plan.py`，从模板生成测试用例设计表。Do not hand off an empty workbook。生成后依次完成：
   - **执行脚本结构检查**：运行 `python3 scripts/test_plan_validator.py <plan.xlsx> [--requirements <requirements.json>]`，检查工作簿结构、字段格式、编号和其他确定性规则，结果必须为 `PASS`。
   - **执行 Agent 语义审查**：读取 `references/specs/test-plan-rules.md`，结合被测命令说明和目标工具逐条审查用例语义，记录每条规则的 `PASS`、`FAIL` 或 `SPEC-GAP` 及理由。
   - 两项均通过后才能展示设计并进入确认等待；任一项失败或存在未处理的 `SPEC-GAP` 时，先修正测试计划，不得继续生成 TCL。
4. 展示 Excel、完整用例设计和两类覆盖率结果，然后进入等待门禁：

   **WAIT-DESIGN-CONFIRMATION**
   - 等待内容：用户明确确认当前用例设计可用于生成 TCL，并确认所选 design 和 tech。
   - 继续条件：用户回复“确认”“可用”“按此生成”或等价的明确批准，且已明确 design 和 tech；修改意见、补充资料或含糊回复不能解除等待。用户无需选择或确认 `design.tcl`、`mmmc.tcl` 文件。

   Wait for explicit user confirmation；确认前不得生成 TCL。Do not generate any TCL file before confirmation.
5. 确认后，Generate one case directory per Excel row，并执行下方“脚本生成与交付门禁”。

### 场景二：从已有用例设计表生成脚本

当用户提供已有测试用例设计表并要求生成脚本时：

1. 读取表格，逐行提取用例 ID、工具、前置条件、测试步骤、预期结果和覆盖项，然后依次完成：
   - **执行脚本结构检查**：运行 `python3 scripts/test_plan_validator.py <plan.xlsx> [--requirements <requirements.json>]`，结果必须为 `PASS`。
   - **执行 Agent 语义审查**：读取 `references/specs/test-plan-rules.md`，结合被测命令说明和目标工具逐条审查用例语义。
   - 两项均通过后才能把表格作为脚本生成输入；失败项和未处理的 `SPEC-GAP` 必须进入 `WAIT-PLAN-FIX`。
2. 以表格为已批准的设计输入，不重新执行场景设计或策略选择，不得擅自改写已给出的用例设计。
3. 若必需字段、初始化输入或可执行预期存在缺失、歧义或冲突，停止脚本生成并逐项列出问题，然后进入等待门禁：

   **WAIT-PLAN-FIX**
   - 等待内容：用户补充或修正列出的问题，或提供修订后的测试用例设计表；若 design 或 tech 未明确，也在此等待补充。
   - 继续条件：所有阻塞问题均已获得明确且一致的输入，且 design 和 tech 已确定；不得猜测补全，未解决时保持等待。

4. 检查通过后，按每条有效用例直接生成 TCL，并执行下方“脚本生成与交付门禁”。

### 共享：脚本生成与交付门禁

1. Generate one case directory per Excel row。取得用户选择的 design 和 tech 后，Skill 根据已登记的 design/tech 资源映射自动确定对应的 `design.tcl`，并结合目标工具自动确定目标工具方言的 `mmmc.tcl`；用户无需选择文件。不得跨工具替换 MMMC。将确定的文件复制并归档到每个用例目录：`design.tcl` 放入 `<case_dir>/tcl/design.tcl`，`mmmc.tcl` 放入 `<case_dir>/tcl/<tool>/mmmc.tcl`。归档后的用例不得依赖原始文件所在目录；映射缺失或不唯一时记录 `SPEC-GAP` 并停止生成。
2. **执行脚本静态检查**：
   - 运行 `python3 scripts/tcl_convention_validator.py <case_dir>...`，在同一次 TCL 检查中分别报告 Tcl 基础语法、EDA 工具命令及选项使用、TCL 编程规范；编程规范包含用例目录、文件结构、命名、固定标记、白名单、调用形式及顺序等确定性规则。
3. **执行 Agent 语义审查**：必须分别读取以下文档，不得用自动检查 PASS 替代：
   - `references/specs/tcl-script-rules.md`：审查设计到脚本的可追溯性、工具方言与初始化语义、检查点充分性、多步数据流及交付完整性。
   对每条适用规则记录 `PASS`、`FAIL` 或 `SPEC-GAP`；任何 `FAIL` 或未解决的 `SPEC-GAP` 都必须停止交付。
4. 只有两个专项静态检查脚本和两份语义规范审查全部通过后才可交付。

   **WAIT-SCRIPT-DELIVERY-FIX**
   - 等待内容：用户补充或确认语义缺口、修正失败的设计/脚本，或提供可用的目标工具静态检查环境与版本语法库。
   - 继续条件：全部 `FAIL`、`SPEC-GAP` 和 `TOOL_UNAVAILABLE` 已消除，且上述门禁重新执行后全部通过；等待期间不得交付。

## 参考文档索引
- 选择策略或确认设计前：`references/test-strategies.md`
- 解析 TXT 命令说明前：`references/command-spec-format.md`
- 生成 Optimus full-flow 或 MMMC 时：`references/optimus-tcl-corpus.md`
