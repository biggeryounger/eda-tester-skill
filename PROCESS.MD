# EDA Tester Skill 项目进度

最后更新：2026-08-07

归档仓库：<https://github.com/biggeryounger/eda-tester-skill>

归档状态：2026-08-07 完成首次独立仓库归档；归档范围仅包含 `eda-tester-skill/`。

## 当前目标

完成一个面向 EDA 命令的 Codex Skill：从命令说明或自然语言需求生成测试场景、Excel 测试计划和 TCL 用例，并通过确定性程序完成验证。当前优先支持 Cadence Innovus。

## 当前状态

- 当前活动功能：F-013 测试计划规范验证。
- 已通过功能：F-004 用例命名与组织、F-005 需求可追溯性。
- F-014 Nagelfar 接入代码和测试已完成，但受功能顺序门禁约束，`function.json` 中仍保持 `not_started`。
- F-015 TCL 脚本规范验证为 `blocked`，原因是正式 TCL 规范尚未配置。
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

## 当前验证基线

2026-08-07 最近一次检查结果：

- 项目结构和功能清单验证：PASS。
- Python 单元测试：10/10 PASS。
- Codex Skill 结构检查：PASS。
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
- F-015 的正式 TCL 规范及 Layer 2B 检查器尚未完成。
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
5. 用户要求归档时，只归档当前 `eda-tester-skill/` 子项目，不修改父仓库的 Gitee `origin`。
