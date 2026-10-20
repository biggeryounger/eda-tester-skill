# AGENTS.md — EDA Tester Skill

## 项目描述

本项目用于开发一个 EDA 测试用例生成 Skill。Skill 根据 EDA 命令说明或自然语言需求，完成测试场景分解、测试计划生成和 TCL 测试脚本生成。


## 工作规则

- 每次会话开始时先阅读 `harness/PROCESS.MD` 和 `harness/function.json`，从进度文档的“下一步”继续工作。
- 每次会话结束前更新 `harness/PROCESS.MD`，记录实际完成内容、验证结果、遗留问题和下一步。
- 修改功能前先阅读 `skill/SKILL.md`、`harness/function.json` 及相关规范文档。
- 从 `skill/assets/templates/测试用例设计表.xlsx` 复制并生成测试计划，保留模板结构和格式。
- 不提交 EDA 许可证、PDK、设计数据库、运行日志、Python 缓存或用户本地路径。
- Skill 产物与项目开发资产必须完全分离：`skill/` 只存放运行时验证脚本、运行时资源和 Skill 文档；项目开发验证脚本、测试资源及开发文档只能放在 `harness/`。禁止脚本、测试 fixture、规范或入口同时承担 Skill 运行时与项目开发职责，禁止跨目录混合维护。
- 构建 Skill 测试用例必须使用可重复、可稳定运行的自动化脚本用例；禁止以一次性人工操作或不可复现的交互结果作为测试用例。
- `skill/` 目录内禁止存在任何 `README.md`；Skill 文档只能维护在 `SKILL.md` 或 `references/` 中。
- `harness/function.json` 是项目特性及状态的唯一清单，新增功能时应同步更新。
- `harness/function.json` 中功能点的 `status` 只能是 `not_started`、`active`、`blocked`、`passing`。
- 每次只开发一个功能点，`harness/function.json` 中最多只能有一个功能点处于 `active`。
- 测试先行：功能从 `not_started` 改为 `active` 前，必须先创建对应测试用例，并在该功能的 `test_cases` 和 `validation_commands` 中登记；不得先实现后补测试。
- `active` 功能开发期间运行 `./init.sh test feature <FEATURE_ID>`；只有登记命令全部通过后才能改为 `passing`。
- 当前功能点必须完成端到端验证并将状态更新为 `passing`，才能把下一个功能点改为 `active`。
- 无法继续的功能点标记为 `blocked`；尚未开始的功能点保持 `not_started`。

## 受保护冒烟用例

- 固定保护 `harness/references/protected-smoke.json` 中的 SMOKE-001～SMOKE-010；执行入口为 `./init.sh test smoke`。十项均为可重复自动化测试，不依赖真实模型服务或 EDA 许可证。
- 修改、删除、重命名、替换这些用例，或改动其断言、输入、fixture、预期结果、共享测试辅助代码、runner，必须先获得用户明确允许。即使声称修复、重构或更新 golden，也不得先改后报。
- 不得通过 skip、expectedFailure、减少执行项、移出发现范围、修改执行入口或降低检查强度绕过保护。冒烟清单、本节规则、`harness/scripts/run_smoke.py` 和 `harness/tests/unit/test_protected_smoke.py` 本身也受同样保护。
- 变更前先说明受影响编号、原因、具体差异及对断言强度的影响，获得用户对该范围的明确允许后再实施，并在 `harness/PROCESS.MD` 记录授权原话/来源、允许范围及验证结果。一般开发、修复、上传代码或 Jenkins 合入审批不视为允许修改受保护用例。
- 受保护范围包括所选测试模块的共享 setup/helper，以及 `harness/tests/e2e/optimus_check_design_data_full_workflow/` 中被这些测试使用的输入、预期与执行脚本；其他文件中影响这些测试执行选择或裁决强度的改动同样适用。正常修改被测 Skill 实现无需额外授权，测试失败时优先修复实现。
- 此机制为项目协作规则与自动化执行检查，不是不可篡改的权限隔离；不得宣称其能抵御有权修改仓库或 Jenkins 管理配置的人。首次建立清单由本次用户要求授权，此后的任何保护范围调整均需重新明确允许。

## 开发环境使用

项目主要使用：

- Python 3.9+：验证框架和自动化测试。
- Tcl / Tclsh：TCL 基础环境。
- Microsoft Excel `.xlsx`：测试计划格式。
- Codex Skill：以 `SKILL.md` 作为 Skill 入口。

首次使用优先运行根目录统一入口：

```sh
./init.sh dev
```

该命令创建项目独立的 `.venv`、安装 Python 依赖并检查 Tcl 版本，不安装第三方 TCL 静态语法工具。

## 验证命令

所有入口都从项目根目录通过 `init.sh` 运行；底层命令由脚本统一维护，不在本文重复登记。

```sh
# 查看全部命令
./init.sh help

# 安装开发环境、部署 Skill
./init.sh dev
./init.sh deploy

# 全量和分层验证
./init.sh test all
./init.sh test layer1
./init.sh test layer2 path/to/测试计划.xlsx path/to/pos001_case

# 指定范围验证
./init.sh test project
./init.sh test unit
./init.sh test skill
./init.sh test feature F-026
./init.sh test tcl path/to/pos001_case
./init.sh test plan path/to/测试计划.xlsx
./init.sh test delivery path/to/测试计划.xlsx path/to/pos001_case
```

- `test all` 与 Jenkins 使用相同的完整门禁，并生成 HTML、JUnit 和完整日志。
- `test layer1` 检查项目清单、Skill 结构、Python 依赖和 Tcl 环境。
- `test layer2` 接收一个测试计划及一个或多个 TCL 用例目录，执行 Excel → TCL 规范检查；Excel 未通过时 TCL 检查为 `SKIPPED`。它是端到端 Layer 2 的内部输出门禁，不单独代表用户功能端到端通过。
- `test feature` 运行 `harness/function.json` 中指定功能绑定的全部验证命令。
- `test tcl`、`test plan` 和 `test delivery` 用于调试对应场景。
- `./init.sh --dry-run ...` 只打印命令，不执行。

所有验证仅在全部检查为 `PASS` 时返回退出码 `0`；`FAIL` 或 `TOOL_UNAVAILABLE` 返回非零退出码。顶层验收仍为两层：Layer 1 验证 Skill 环境、工具与启动，Layer 2 使用版本化测试集验证端到端用户功能与输出。

## Skill 安装与启动

安装、预检、Agent 选择、安装模式和目标目录统一通过 `init.sh deploy` 管理：

```sh
./init.sh deploy
./init.sh deploy --agent opencode
./init.sh deploy --mode copy
./init.sh --dry-run deploy --agent trae --skills-dir /path/to/trae/skills
```

具体的运行时白名单、默认模式、支持的 Agent、重装限制、启动示例和故障检查统一查看：

```sh
./init.sh help
```

本项目属于父仓库中的独立子项目，不使用父目录作为统一构建入口。

## 用户触发的结束动作

普通任务完成、测试通过或会话结束时，不自动上传代码，也不自动触发 Jenkins。只有用户明确说“上传代码”时，才按以下顺序执行结束动作：

1. 根据本次实际变更更新 `skill/SKILL.md` 及相关 README 文档；没有相关内容变化时明确记录无需修改，不编造文档变更。
2. 更新 `harness/PROCESS.MD` 和 `harness/function.json`，运行 `./init.sh test all`，确认完整门禁通过。
3. 检查待上传差异及秘密、日志、本地路径和禁止提交文件；只操作当前 `eda-tester-skill/` GitHub 仓库。
4. 创建或使用 `codex/` 候选分支，提交并推送候选分支，不直接推送 `main`。
5. 使用该远端候选分支作为 `CANDIDATE_REF` 触发 Jenkins 的 `eda-tester-skill-approved-merge` 流水线。
6. 发布测试报告并等待用户审批；只有用户在 Jenkins 中批准后，流水线才允许合入目标分支。

“上传代码”只授权上述结束流程，不授权绕过测试、审批、分支保护或操作父目录及其他仓库。若文档、测试、提交、推送或 Jenkins 任一步失败，停止后续步骤并报告失败原因。

## 代码仓库

- 项目唯一跟踪仓库：<https://github.com/biggeryounger/eda-tester-skill>
- 当前项目的 `origin` 必须保持为上述 GitHub 仓库，不再使用或同步 Gitee。
- 仓库范围只包含 `eda-tester-skill/` 项目，不包含父目录中的其他项目。
- 提交或推送前先运行本文件“验证命令”章节中的项目检查、功能检查、单元测试和 Skill 结构检查。
- 只有用户明确要求提交或推送时，才向 GitHub 仓库发布变更。

## 项目文档描述

- `skill/SKILL.md`：最终 Skill 的触发说明、生成流程和输出要求。
- `harness/function.json`：项目功能、优先级、状态和验收标准。
- `harness/PROCESS.MD`：跨会话维护的项目进度、验证基线、遗留问题和下一步。
- `harness/references/test-plan.md`：两层项目验收计划、执行顺序和完成标准。
- `harness/references/e2e-test-set.md`：端到端测试集的输入、预期输出、比较和归档契约。
- `skill/references/specs/test-plan-rules.md`：测试计划 Excel 的运行时详细规则。
- `skill/references/specs/tcl-script-rules.md`：TCL 脚本运行时规范。
- `skill/agents/openai.yaml`：Skill 在 Codex 界面中的名称、简介和默认提示词。

详细业务规则只维护在对应文档中，避免在 `AGENTS.md` 重复定义。

## 项目结构

```text
eda-tester-skill/
├── AGENTS.md                         # 仓库协作入口
├── skill/                            # 唯一可安装代码产物
│   ├── SKILL.md                      # Skill 入口
│   ├── agents/                       # Skill 界面元数据
│   ├── assets/                       # 运行资产与模板
│   ├── references/                   # 生成与输出规范
│   └── scripts/                      # 运行脚本和输出检查器
└── harness/                          # 项目开环开发与验收环境
    ├── PROCESS.MD                    # 项目进度与会话交接
    ├── function.json                 # 功能清单
    ├── references/                   # 项目验收与设计文档
    ├── scripts/                      # 安装器和环境自检工具
    ├── jenkins/                      # 完整测试、人工审批和安全合入流水线
    ├── tests/                        # 单元、回归和端到端测试集
    ├── generated/                    # 开发生成结果
    └── outputs/                      # 开发运行输出
```
