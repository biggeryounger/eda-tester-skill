# EDA 测试用例生成 Skill 验证计划

## 1. 验证目标

验证 Skill 的两个主要输出：测试计划和 TCL 脚本。验证过程必须由确定性程序执行，不依赖 Agent 对结果进行主观判定。

验证模型固定为两层，其中第二层包含两个独立检查项：

```text
Layer 1：测试计划规范检查
Layer 2：TCL 脚本检查
         ├── 2A：TCL 语法检查
         └── 2B：TCL 脚本规范检查
```

测试计划规范已根据用户提供的模板和 `check_design_data` 手写用例形成规则；TCL 脚本规范适用于用例目录树（`nith.run` + `tcl/design.tcl` + `tcl/<tool>/{run_1.tcl…run_N.tcl, mmmc.tcl}`）和三类 `pv_check_*` 检查点，Layer 1、Layer 2A、Layer 2B 均已有确定性检查器。

## 2. Layer 1：测试计划规范检查

### 输入

- 原始命令说明或需求。
- Skill 输出的测试计划。
- [测试计划规范](specs/test-plan-rules.md)。

### 检查职责

- 检查测试计划的必需章节、字段和格式。
- 检查用例编号、正负属性及命名规则。
- 检查命令参数、约束和测试场景之间的覆盖关系。
- 检查每个测试场景是否包含前置条件、操作、期望结果和来源追溯。
- 检查规范规定的正向、负向、边界和组合场景。

### 明确不检查

- 不检查 TCL 语法。
- 不执行 TCL。
- 不用 Agent 判断测试计划“看起来是否合理”。所有阻断条件必须来自版本化规则。

### 当前状态

规范 draft 已配置，字段结构和命名规则可开始实现自动检查；完整 `.xlsx` 检查器仍待接入。在检查器完成前不得报告 Layer 1 为 `PASS`。

## 3. Layer 2：TCL 脚本检查

Layer 2 仅在 Layer 1 通过后执行，避免为不合格的测试计划验证脚本。其内部 2A 和 2B 分别报告，不能互相替代。

### 2A：TCL 语法检查

#### 输入

- 生成的用例目录及其 `tcl/` 树中的所有 `.tcl` 文件（`design.tcl`、`mmmc.tcl`、`run_1.tcl … run_N.tcl`）。
- Tcl 版本配置。
- EDA 工具专属命令语法数据库。

#### 检查职责

- Tcl 词法和结构完整性。
- 花括号、方括号、双引号和命令边界。
- Tcl 内置命令的参数形式。
- 已登记 EDA 命令的选项、参数数量及可静态确定的参数类型。

#### 实现策略

- 默认接入 Nagelfar 命令行检查器。
- 为 Innovus/iTools 建立独立 syntax database；后续按需增加 Optimus 和 PrimeTime。
- Python 只负责调用工具、设置超时、收集退出码并转换统一诊断，不重新实现完整 Tcl parser。
- 第三方检查器或对应 syntax database 不可用时返回 `TOOL_UNAVAILABLE`，不得降级为完整语法通过。

基础括号平衡检查可作为快速预检，但只能标记为 `PRECHECK_PASS`，不能代替 Nagelfar 的 `PASS`。

### 2B：TCL 脚本规范检查

#### 输入

- 通过 2A 的用例目录。
- [TCL 脚本规范](specs/tcl-script-rules.md)。
- 对应测试计划条目及用例元数据。

#### 检查职责

- 检查文件组织、命名、注释和固定标记。
- 检查 setup、test action、assertion 和 cleanup 的结构。
- 检查正负用例的期望标记是否一致。
- 检查禁止项、危险操作、路径和环境依赖。
- 检查脚本与测试计划条目是否一一对应。

#### 明确不检查

- 不把格式规范检查当作 TCL 语法检查。
- 不判断 Innovus 中的真实设计状态和运行结果。
- 不使用 Agent 自由解释未写入规范的规则。

### 当前状态

版本化规则覆盖目录树结构（`nith.run`、`design.tcl`、`mmmc.tcl`、连续编号 `run_N.tcl`）、可移植路径、PV 入口、检查点存在性及三类 `pv_check_*` 参数约束。确定性检查器和逐条正反样例已经实现。

## 4. 统一结果模型

每项检查返回以下状态之一：

| 状态 | 含义 |
|---|---|
| `PASS` | 所需规则和工具均已配置，全部检查通过 |
| `FAIL` | 至少一个确定性规则失败 |
| `NOT_CONFIGURED` | 对应业务规范尚未配置 |
| `TOOL_UNAVAILABLE` | 所需第三方检查器或语法数据库不可用 |
| `SKIPPED` | 因上游检查未通过而未执行 |

每条诊断至少包含：验证层、规则 ID、严重级别、文件、行号（可确定时）和说明。最终成功只能由 `Layer 1 = PASS`、`Layer 2A = PASS`、`Layer 2B = PASS` 共同构成。

## 5. 执行顺序和门禁

1. 校验 `function.json` 和验证配置本身。
2. 执行 Layer 1。
3. Layer 1 为 `PASS` 时执行 Layer 2A，否则 Layer 2 全部为 `SKIPPED`。
4. Layer 2A 为 `PASS` 时执行 Layer 2B；语法失败时 2B 默认 `SKIPPED`，避免对无效语法产生误导诊断。
5. 汇总结果并返回非零退出码，除非三项均为 `PASS`。

开发阶段允许分别运行某一检查项以调试规则，但发布门禁不得绕过上述顺序。

## 6. 测试策略

### 规则测试

每条规范规则至少包含一个应通过样例和一个应失败样例。规则新增、删除或改变严重级别时必须更新测试。

### 语法检查器测试

- 合法 Tcl 基础语法通过。
- 缺少花括号、方括号或引号失败。
- Tcl 内置命令参数错误失败。
- 已登记 Innovus 命令及选项通过。
- 未知 Innovus 选项或缺少参数失败。
- 动态生成命令无法静态判断时给出明确诊断，而不是误报通过。

### 端到端测试

使用一份固定命令说明，生成测试计划和 TCL 脚本，依次通过 Layer 1、2A、2B。另准备三组故障注入样例，分别确保每个检查项能够独立失败。

## 7. 当前执行入口

现有基础框架：

```sh
python3 scripts/validate.py
python3 scripts/validate.py project --format json
python3 scripts/validate.py tcl path/to/case_dir
python3 scripts/validate.py delivery path/to/test-plan.xlsx path/to/case_dir
python3 -m unittest discover -s tests/unit -v
```

当前验证器已实现 Excel Layer 1、Nagelfar 1.3.5 Layer 2A、目录树 TCL Layer 2B，以及针对同一批 Excel 和一个或多个 TCL 用例目录的 `delivery` 统一门禁。统一结果固定汇总为 L1、L2A、L2B 三项；只有三项全部为 `PASS` 才返回成功。

## 8. 完成标准

- 两份规范均已定稿并具有版本号。
- 每条规则有稳定 ID 和自动化正反测试。
- Nagelfar 版本及 Innovus syntax database 被固定并可复现。
- 三项检查能够分别运行并生成统一格式结果。
- 上游失败正确阻断下游检查。
- 不存在以 Agent 复核代替确定性验证的路径。
