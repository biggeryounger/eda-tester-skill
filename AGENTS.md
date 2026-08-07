# AGENTS.md — EDA Tester Skill

## 项目描述

本项目用于开发一个 EDA 测试用例生成 Skill。Skill 根据 EDA 命令说明或自然语言需求，完成测试场景分解、测试计划生成和 TCL 测试脚本生成。

当前优先支持 Cadence Innovus。项目中涉及工具名称时，保持以下名称不变：**Optimus**、**iTools / Innovus**、**PrimeTime**。

项目验证分为两层：

1. 检查生成的测试计划是否符合项目规范。
2. 检查 TCL 脚本，包括语法检查和脚本规范检查。

验证必须由确定性程序完成，不使用 Agent 判断代替自动检查。

## 工作规则

- 每次会话开始时先阅读 `PROCESS.MD` 和 `function.json`，从 `PROCESS.MD` 的“下一步”继续工作。
- 每次会话结束前更新 `PROCESS.MD`，记录实际完成内容、验证结果、遗留问题和下一步。
- 修改功能前先阅读 `SKILL.md`、`function.json` 及相关规范文档。
- 从 `assets/templates/测试用例设计表.xlsx` 复制并生成测试计划，保留模板结构和格式。
- TCL 语法检查优先使用 Nagelfar 等确定性第三方工具；不得通过直接执行脚本来代替静态语法检查。
- 新增或修改验证规则时，同时增加通过和失败测试样例。
- 不提交 EDA 许可证、PDK、设计数据库、运行日志、Python 缓存或用户本地路径。
- `function.json` 是项目特性及状态的唯一清单，新增功能时应同步更新。
- `function.json` 中功能点的 `status` 只能是 `not_started`、`active`、`blocked`、`passing`。
- 每次只开发一个功能点，`function.json` 中最多只能有一个功能点处于 `active`。
- 测试先行：功能从 `not_started` 改为 `active` 前，必须先创建对应测试用例，并在该功能的 `test_cases` 和 `validation_commands` 中登记；不得先实现后补测试。
- `active` 功能开发期间运行 `python3 scripts/validate.py feature <FEATURE_ID>`；只有登记命令全部通过后才能改为 `passing`。
- 当前功能点必须完成端到端验证并将状态更新为 `passing`，才能把下一个功能点改为 `active`。
- 无法继续的功能点标记为 `blocked`；尚未开始的功能点保持 `not_started`。

## 开发环境使用

项目主要使用：

- Python 3.9+：验证框架和自动化测试。
- Tcl / Tclsh：TCL 基础环境。
- Nagelfar 1.3.5：TCL 静态语法检查器。
- Microsoft Excel `.xlsx`：测试计划格式。
- Codex Skill：以 `SKILL.md` 作为 Skill 入口。

## 验证命令

所有验证命令都从本项目根目录运行。

运行项目清单、用例元数据和基础 TCL 契约检查：

```sh
python3 scripts/validate.py
python3 scripts/validate.py project
python3 scripts/validate.py project --format json
```

运行 Nagelfar Layer 2A 静态语法检查；可一次传入一个或多个 TCL 文件：

```sh
python3 scripts/validate.py tcl path/to/run.tcl
python3 scripts/validate.py tcl path/to/case_1.tcl path/to/case_2.tcl
```

Nagelfar 不在 `PATH` 中时，通过环境变量或命令参数指定 `nagelfar.tcl`：

```sh
NAGELFAR=/path/to/nagelfar135/nagelfar.tcl python3 scripts/validate.py tcl path/to/run.tcl
python3 scripts/validate.py tcl --nagelfar /path/to/nagelfar135/nagelfar.tcl path/to/run.tcl
```

运行全部 Python 单元测试：

```sh
python3 -m unittest discover -s tests/unit -v
```

运行 `function.json` 中某个功能绑定的全部验证命令：

```sh
python3 scripts/validate.py feature F-014
```

修改 Skill 后运行 Codex Skill 结构检查：

```sh
python3 /Users/e2uninova-m4/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
```

统一验证接口只在全部检查为 `PASS` 时返回退出码 `0`；`FAIL` 或 `TOOL_UNAVAILABLE` 返回非零退出码。当前不得使用单一命令宣称完整两层门禁通过，因为 Excel Layer 1 检查器和正式 Layer 2B 规范仍未完成。

## Skill 安装与启动

安装前先确保 Skill 结构检查通过，并确认目标目录中不存在同名 Skill。

本地开发时推荐使用软链接安装，使项目修改可以立即反映到已安装 Skill：

```sh
mkdir -p ~/.codex/skills
ln -s /Users/e2uninova-m4/Desktop/test_project/eda-tester-skill ~/.codex/skills/eda-tester-skill
```

需要安装独立副本时使用复制方式：

```sh
mkdir -p ~/.codex/skills
cp -R /Users/e2uninova-m4/Desktop/test_project/eda-tester-skill ~/.codex/skills/eda-tester-skill
```

安装完成后重启 Codex，或重新创建一个任务，使 Codex 重新扫描 Skills。使用以下方式显式启动：

```text
$eda-tester-skill 根据这份 Innovus 命令说明生成测试计划和 TCL 用例。
```

也可以提出与 `SKILL.md` 描述匹配的自然语言请求，让 Codex 自动选择该 Skill。开发和验收时优先显式写出 `$eda-tester-skill`，避免无法判断是否成功加载。

若 Skill 没有被识别，依次检查：

1. 安装路径是否为 `~/.codex/skills/eda-tester-skill/`。
2. 该目录下是否直接存在 `SKILL.md`，而不是多嵌套了一层目录。
3. `SKILL.md` 的名称是否为 `eda-tester-skill`，结构检查是否通过。
4. 安装后是否已经重启 Codex或创建新任务。

本项目属于父仓库中的独立子项目，不使用父目录作为统一构建入口。

## 代码仓库

- 项目唯一跟踪仓库：<https://github.com/biggeryounger/eda-tester-skill>
- 当前项目的 `origin` 必须保持为上述 GitHub 仓库，不再使用或同步 Gitee。
- 仓库范围只包含 `eda-tester-skill/` 项目，不包含父目录中的其他项目。
- 提交或推送前先运行本文件“验证命令”章节中的项目检查、功能检查、单元测试和 Skill 结构检查。
- 只有用户明确要求提交或推送时，才向 GitHub 仓库发布变更。

## 项目文档描述

- `SKILL.md`：Skill 的触发说明、生成流程和输出要求。
- `function.json`：项目计划实现的功能、优先级、状态和验收标准。
- `PROCESS.MD`：跨会话维护的项目进度、验证基线、遗留问题和下一步。
- `references/test-plan.md`：两层验证计划、执行顺序和完成标准。
- `references/specs/test-plan-rules.md`：测试计划 Excel 的详细检查规则。
- `references/specs/tcl-script-rules.md`：TCL 脚本规范；规则仍待继续补充。
- `agents/openai.yaml`：Skill 在 Codex 界面中的名称、简介和默认提示词。

详细业务规则只维护在对应文档中，避免在 `AGENTS.md` 重复定义。

## 项目结构

```text
eda-tester-skill/
├── AGENTS.md                         # 项目协作说明
├── SKILL.md                          # Skill 入口
├── function.json                     # 功能清单
├── PROCESS.MD                        # 项目进度与会话交接
├── agents/
│   └── openai.yaml                   # Skill 界面元数据
├── assets/
│   └── templates/
│       └── 测试用例设计表.xlsx        # 测试计划模板
├── references/
│   ├── test-plan.md                  # 验证计划
│   └── specs/
│       ├── test-plan-rules.md        # 测试计划规范
│       └── tcl-script-rules.md       # TCL 脚本规范
├── scripts/
│   └── validate.py                   # 基础验证器
└── tests/
    ├── cases/                        # 正向和负向验证样例
    └── unit/                         # Python 单元测试
```
