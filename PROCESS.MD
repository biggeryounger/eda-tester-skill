# EDA Tester Skill 项目进度

最后更新：2026-08-07

项目仓库：<https://github.com/biggeryounger/eda-tester-skill>

仓库状态：2026-08-07 完成首次 GitHub 推送；后续只跟踪该 GitHub 仓库，不再使用或同步 Gitee。

## 当前目标

完成一个面向 EDA 命令的 Codex Skill：从命令说明或自然语言需求生成测试场景、Excel 测试计划和 TCL 用例，并通过确定性程序完成验证。当前优先支持 Cadence Innovus。

## 当前状态

- 当前活动功能：F-013 测试计划规范验证。
- 已通过功能：F-004 用例命名与组织、F-005 需求可追溯性。
- F-014 Nagelfar 接入代码和测试已完成，但受功能顺序门禁约束，`function.json` 中仍保持 `not_started`。
- F-015 TCL 脚本规范 `1.0-draft` 已配置，功能状态回到 `not_started`；确定性检查器及逐条正反样例尚未实现。
- 其余功能保持 `not_started`。

功能状态的唯一正式来源是 `function.json`；本文件只记录会话交接信息，不替代功能清单。

## 已完成工作

- 建立 Skill 基础结构、界面元数据、模板、规范和测试目录。
- 建立 `function.json` 功能清单和单一活动功能门禁。
- 建立正负用例目录、`case.toml` 元数据和基础 TCL 契约检查。
- 接入 Nagelfar 1.3.5，并建立 Innovus/iTools syntax database。
- 建立统一验证入口：
  - `python3 scripts/validate.py project`
  - `python3 scripts/validate.py tcl <script.tcl>`
  - `python3 scripts/validate.py feature <FEATURE_ID>`
- 将顶层验证配置改为 `validation_commands` 命令注册表。
- 为功能增加 `test_cases` 和 `validation_commands`，建立测试先行门禁。
- `active` 或 `passing` 功能如果没有登记测试和命令，项目验证会失败。
- 根据用户提供的目录与 `nith.run` 截图、`pv_check tcl 命令用户指南.pdf` 和 `pv_check_qor_usage.md`，建立 TCL 用例脚本规范 `1.0-draft`。
- 新规范包含 11 条稳定规则：禁止符号链接、目录结构、NITH 初始化与调度、检查点存在性、PV 入口加载、三类 `pv_check_*` 调用约束、动作/期望标记和占位符禁用。
- 将 F-015 从 `blocked` 调整为 `not_started`；F-013 仍是唯一 `active` 功能，未越过功能顺序门禁实现 F-015。
- 建立测试场景生成策略 `1.0`：Smoke case、正向覆盖、负向覆盖。Skill 在输出测试设计前必须让用户选择，支持多选且不擅自使用默认策略。
- Smoke case 覆盖全部选项与枚举值；正向覆盖按业务场景设计；负向覆盖边界值、异常值和选项冲突。多策略结果取并集、去重并保留策略标签。
- 同步更新 F-002 的描述和验收标准，但保持 `not_started`；F-013 仍为唯一 `active` 功能。
- 接入 Innovus 命令背景知识查询规则：iTools / Innovus 命令使用 `http://49.1.1.123:5175/` 的 `INNOVUS191` NotebookLM Bridge 查询语法、选项、约束、示例和来源引用。
- 规定语料库只发送命令名和通用文档问题，不发送设计数据、日志、内部路径等敏感内容；目标版本非 19.1、来源冲突或站点失败时必须记录缺口并降级到用户手册。
- 实际验证页面可访问并能进入 `INNOVUS191` 问答界面；本次 `add_net` 试查遇到站点侧 `Internal Server Error`，已验证失败分支确有必要。
- 同步更新 F-001 的描述和验收标准，但保持 `not_started`；F-013 仍为唯一 `active` 功能。
- 根据用户提供的 Optimus 全流程 TCL 和 MMMC TCL 建立脱敏语料：保留 setup、floorplan、place、CTS、route、post-route 的阶段顺序、输出节点和检查点，以及 lib set、RC corner、analysis corner、mode、view 的对象依赖。
- 未将来源中的 N7 PDK/library/cell、设计名、时钟名、内部路径和具体调优数值写入仓库；生成时必须从目标用例配置取得这些数据。
- 记录来源中的两个待确认问题：MMMC 的 `cbest/cworst` 命名与 library 文件属性看起来交叉，以及 PV 入口存在 `$env(PV_ROOT)/scripts/pv.tcl` 与 `$env(PV_ROOT)/pv/scripts/pv.tcl` 两种布局。
- 同步更新 F-010 的描述和验收标准，但保持 `not_started`；F-013 仍为唯一 `active` 功能。

## 当前验证基线

2026-08-07 最近一次检查结果：

- 项目结构和功能清单验证：PASS。
- Python 单元测试：10/10 PASS。
- Codex Skill 结构检查：PASS。
- F-013 功能级验证：PASS。
- F-004 功能级验证：PASS。
- F-014 功能级验证：PASS。

复现命令：

```sh
python3 scripts/validate.py project
python3 -m unittest discover -s tests/unit -v
python3 /Users/e2uninova-m4/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
```

## 已知缺口

- F-013 尚未实现完整的 `.xlsx` Layer 1 检查器。
- PLAN-001 至 PLAN-014 尚未全部具备自动化正反样例。
- 完整 Layer 1 尚不能报告 `PASS`。
- F-015 的规范已配置，但 Layer 2B 确定性检查器和逐条自动化正反样例仍未完成。
- F-002 的策略规则已配置，但尚未建立策略交互、覆盖矩阵及多策略去重的自动化验收样例。
- F-001 的 Innovus 语料库查询规则已配置，但尚未实现稳定的程序化查询适配器、响应结构校验和自动化验收样例；站点当前可能返回 `Internal Server Error`。
- F-010 的 Optimus 脱敏语料已配置，但尚未建立流程阶段、MMMC 引用完整性、corner 语义和 PV 入口配置的自动化验收样例。
- 尚未实现 Layer 1 → Layer 2A → Layer 2B 的完整门禁编排。
- Nagelfar 未作为项目依赖安装；运行真实 L2A 检查时需要在 `PATH` 中提供 Nagelfar 1.3.5，或设置 `NAGELFAR`。

## 下一步

1. 为 F-013 先补齐 PLAN-001 至 PLAN-014 的测试输入和预期结果。
2. 实现 `.xlsx` 测试计划检查器，保持模板 A-J 列结构和格式。
3. 运行 `python3 scripts/validate.py feature F-013` 和完整单元测试。
4. 仅在 F-013 验收标准全部满足后，将其状态改为 `passing`。
5. 再将 F-014 改为 `active`，复核真实 Nagelfar 1.3.5 端到端结果后更新状态。

## 每次会话开始时

1. 阅读 `PROCESS.MD` 和 `function.json`，确认当前活动功能与下一步。
2. 阅读 `SKILL.md`、`AGENTS.md` 及当前功能涉及的规范文件。
3. 运行 `python3 scripts/validate.py project`，确认仓库处于一致状态。
4. 从本文件“下一步”的第一项未完成工作继续。

## 每次会话结束前

1. 更新本文件的当前状态、已完成工作、验证基线、已知缺口和下一步。
2. 运行项目验证、相关功能验证和单元测试。
3. 确认 `function.json` 的状态、测试路径和验证命令与实际实现一致。
4. 汇报已完成内容和未解决问题；只有用户明确要求时才提交版本控制变更。
5. 用户要求提交或推送时，只操作当前 `eda-tester-skill/` 的 GitHub 仓库，不操作父目录中的其他仓库。
