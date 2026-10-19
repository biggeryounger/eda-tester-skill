# 用户规则覆盖登记

本文档是项目开发侧的用户规则台账，用于持续登记用户提出的用例设计、工作流和脚本输出风格规范。它不是 Skill 运行时规范，不随 `skill/` 安装。

## 维护约定

- 新规则按 `USR-NNN` 连续编号，只追加或明确修订，不复用旧编号。
- `workflow` 规则必须落实在 `skill/SKILL.md` 或 `skill/agents/openai.yaml`。
- `semantic` 规则必须落实在 `skill/references/specs/` 的 Agent 语义审查文档。
- `static` 规则必须同时具有 `skill/scripts/` 中的确定性检查实现和 `harness/tests/unit/` 中的自动化测试。
- `project` 规则必须同时具有 `AGENTS.md` 项目约束和 `harness/tests/unit/` 中的自动化测试。
- `evidence` 中的 `contains` 是稳定的最小证据；重构实现时必须同步更新本台账。`must_not_exist` 用于锁定禁止出现的文件。

## 当前规则清单

```json
{
  "schema_version": "1.0",
  "rules": [
    {
      "id": "USR-001",
      "summary": "Skill 只能由用户显式触发，禁止自动触发",
      "category": "workflow",
      "evidence": [
        {"path": "skill/agents/openai.yaml", "contains": ["allow_implicit_invocation: false"]},
        {"path": "harness/tests/unit/test_repository_layout.py", "contains": ["allow_implicit_invocation: false"]}
      ]
    },
    {
      "id": "USR-002",
      "summary": "注册描述按做什么、何时使用、关键能力三部分组织",
      "category": "workflow",
      "evidence": [
        {"path": "skill/agents/openai.yaml", "contains": ["short_description:", "用户显式调用", "场景分解", "Excel", "TCL"]},
        {"path": "harness/tests/unit/test_repository_layout.py", "contains": ["description must contain what, when, and capabilities"]}
      ]
    },
    {
      "id": "USR-003",
      "summary": "支持从命令说明先设计再生成脚本，以及从已有设计表直接生成脚本两种场景",
      "category": "workflow",
      "evidence": [
        {"path": "skill/SKILL.md", "contains": ["场景一：从命令说明设计新用例", "场景二：从已有用例设计表生成脚本"]},
        {"path": "harness/tests/unit/test_skill_workflow_modes.py", "contains": ["test_routes_command_spec_to_design_then_script", "test_routes_existing_plan_directly_to_script_generation"]}
      ]
    },
    {
      "id": "USR-004",
      "summary": "所有需要用户确认的暂停点必须用 WAIT 标记并写明等待内容和继续条件",
      "category": "workflow",
      "evidence": [
        {"path": "skill/SKILL.md", "contains": ["WAIT-STRATEGY", "WAIT-DESIGN-CONFIRMATION", "WAIT-PLAN-FIX", "WAIT-SCRIPT-DELIVERY-FIX", "等待内容：", "继续条件："]},
        {"path": "harness/tests/unit/test_skill_workflow_modes.py", "contains": ["test_wait_markers_define_resume_conditions"]}
      ]
    },
    {
      "id": "USR-005",
      "summary": "Excel 确定性规范由测试计划检查脚本执行",
      "category": "static",
      "evidence": [
        {"path": "skill/scripts/test_plan_validator.py", "contains": ["PLAN-001", "PLAN-015"]},
        {"path": "harness/tests/unit/test_test_plan_validator.py", "contains": ["PLAN-001", "PLAN-015"]}
      ]
    },
    {
      "id": "USR-006",
      "summary": "Excel 中需要语义理解的规则只保留在 Agent 语义审查规范",
      "category": "semantic",
      "evidence": [
        {"path": "skill/references/specs/test-plan-rules.md", "contains": ["PLAN-006", "PLAN-013", "Agent"]},
        {"path": "skill/SKILL.md", "contains": ["references/specs/test-plan-rules.md", "执行 Agent 语义审查"]}
      ]
    },
    {
      "id": "USR-007",
      "summary": "TCL 设计追溯、工具语义、检查点充分性和多步数据流由 Agent 语义审查",
      "category": "semantic",
      "evidence": [
        {"path": "skill/references/specs/tcl-script-rules.md", "contains": ["TCL-SEMANTIC-001", "TCL-SEMANTIC-004"]},
        {"path": "skill/SKILL.md", "contains": ["references/specs/tcl-script-rules.md", "检查点充分性"]}
      ]
    },
    {
      "id": "USR-008",
      "summary": "场景覆盖率和被测选项覆盖率必须分别检查并报告未覆盖项",
      "category": "workflow",
      "evidence": [
        {"path": "skill/SKILL.md", "contains": ["场景覆盖率", "被测选项覆盖率", "未覆盖项"]},
        {"path": "harness/tests/unit/test_skill_workflow_tools.py", "contains": ["test_skill_requires_scenario_and_option_coverage"]}
      ]
    },
    {
      "id": "USR-009",
      "summary": "用户确认 design 和 tech 后由映射自动确定 design.tcl 与目标工具方言 mmmc.tcl",
      "category": "workflow",
      "evidence": [
        {"path": "skill/SKILL.md", "contains": ["根据已登记的 design/tech 资源映射自动确定", "用户无需选择文件", "不得跨工具替换 MMMC"]},
        {"path": "harness/tests/unit/test_skill_workflow_modes.py", "contains": ["test_archives_selected_design_and_tech_inputs_into_each_case"]}
      ]
    },
    {
      "id": "USR-010",
      "summary": "每个 case 只有一个工具目录，单步 run.tcl，多步连续 run_1.tcl 到 run_N.tcl",
      "category": "static",
      "evidence": [
        {"path": "skill/scripts/tcl_convention_validator.py", "contains": ["TCL-STRUCT-001", "TCL-STRUCT-002", "单步/多步 run"]},
        {"path": "harness/tests/unit/test_tcl_convention_validator.py", "contains": ["TCL-STRUCT-001", "TCL-STRUCT-002"]}
      ]
    },
    {
      "id": "USR-011",
      "summary": "设计输入集中在 design.tcl，MMMC 保持声明式并隔离工具方言",
      "category": "static",
      "evidence": [
        {"path": "skill/scripts/tcl_convention_validator.py", "contains": ["TCL-DESIGN-001", "TCL-MMMC-001", "TCL-MMMC-002"]},
        {"path": "harness/tests/unit/test_tcl_convention_validator.py", "contains": ["TCL-DESIGN-001", "TCL-MMMC-001", "TCL-MMMC-002"]}
      ]
    },
    {
      "id": "USR-012",
      "summary": "每个 run 必须完成初始化，恰好一个 EXPECT、TEST_ACTION 和 checkpoint，并以 pv_rpt_checkpoints、exit 收尾",
      "category": "static",
      "evidence": [
        {"path": "skill/scripts/tcl_convention_validator.py", "contains": ["TCL-SCRIPT-001", "TCL-SCRIPT-004", "TCL-CHECKPOINT-001", "TCL-SCRIPT-005"]},
        {"path": "harness/tests/unit/test_tcl_convention_validator.py", "contains": ["TCL-SCRIPT-001", "TCL-SCRIPT-004", "TCL-CHECKPOINT-001", "TCL-SCRIPT-005"]}
      ]
    },
    {
      "id": "USR-013",
      "summary": "TCL 仅允许 PV_ROOT 与 PV_TOOL，禁止机器绝对路径和伪造检查结果",
      "category": "static",
      "evidence": [
        {"path": "skill/scripts/tcl_convention_validator.py", "contains": ["TCL-RUNNER-001", "TCL-SCRIPT-003", "TCL-SCRIPT-006"]},
        {"path": "harness/tests/unit/test_tcl_convention_validator.py", "contains": ["TCL-RUNNER-001", "TCL-SCRIPT-003", "TCL-SCRIPT-006"]}
      ]
    },
    {
      "id": "USR-014",
      "summary": "Skill 运行时验证资产与项目开发验证、测试资源和文档完全分离",
      "category": "project",
      "evidence": [
        {"path": "AGENTS.md", "contains": ["Skill 产物与项目开发资产必须完全分离", "禁止跨目录混合维护"]},
        {"path": "harness/tests/unit/test_repository_layout.py", "contains": ["test_runtime_and_development_validation_assets_are_fully_separated"]},
        {"path": "skill/scripts/validate.py", "must_not_exist": true}
      ]
    },
    {
      "id": "USR-015",
      "summary": "Skill 目录内禁止 README.md，文档只进入 SKILL.md 或 references",
      "category": "project",
      "evidence": [
        {"path": "AGENTS.md", "contains": ["目录内禁止存在任何 `README.md`", "`SKILL.md` 或 `references/`"]},
        {"path": "harness/tests/unit/test_repository_layout.py", "contains": ["test_runtime_tree_contains_no_readme_files"]}
      ]
    },
    {
      "id": "USR-016",
      "summary": "每个用例最大化兼容测试点覆盖，仅在冲突、初始化不同或结果无法共同观察时拆分",
      "category": "workflow",
      "evidence": [
        {"path": "skill/SKILL.md", "contains": ["Maximize compatible test-point coverage per case", "测试点冲突", "初始化不同"]},
        {"path": "harness/tests/unit/test_scenario_strategy_contract.py", "contains": ["test_skill_requires_maximum_compatible_coverage_per_case"]}
      ]
    }
  ]
}
```
