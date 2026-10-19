# Codex Skill Agent E2E 用例规范与范式

版本：`1.0`

状态：`ACTIVE`

## 1. 目的和适用范围

本规范定义如何用自动化脚本驱动真实 Codex 会话，显式调用 EDA Tester Skill，跨多个用户回合触发完整 workflow，并用独立、确定性的检查器给出最终测试结论。

适用于以下目标：

- 验证 `$eda-tester-skill` 是否被真实 Agent 加载和执行；
- 验证输入路由、等待门禁、会话恢复、产物生成顺序和最终交付；
- 验证模型生成的 Excel、TCL 和结构化结果是否满足项目规则；
- 把模型、认证或 Codex CLI 不可用与 Skill 功能失败明确区分。

本规范不把一次人工对话、聊天截图或人工主观判断视为测试用例。每个用例都必须能由脚本重复启动、采集证据并返回机器可读结果。

## 2. 核心范式

Agent E2E 是“确定性测试控制器 + 真实模型执行 + 确定性最终裁决”：

```text
版本化输入
   │
   ▼
Agent runner ── codex exec --json ──► 模型显式执行 Skill
   │                                      │
   │◄──── JSONL 事件、结构化状态、产物 ────┘
   │
   ├── 在 WAIT 门禁检查产物时序
   ├── codex exec resume + 固定用户响应
   ├── 独立运行 Excel/TCL 检查器
   └── 汇总 PASS / FAIL / TOOL_UNAVAILABLE
```

职责必须分离：

- 模型负责理解输入、遵循 `SKILL.md`、完成语义设计与审查、生成业务产物，并报告当前 workflow 状态。
- 脚本负责安装被测 Skill、组织固定输入、驱动回合、保存原始事件、检查门禁、检查文件时序、调用独立验证器并计算最终状态。
- 不得让模型自行裁决整个 E2E 是否通过。模型输出的 `state`、摘要和语义审查记录都是被测结果，不是可信的最终判定器。

`run_case.py` 与 `run_agent_case.py` 是互补的两层执行器：

| 执行器 | 是否调用模型 | 用途 | 是否能证明 Skill 被调用 |
|---|---:|---|---:|
| `run_case.py` | 否 | 快速、稳定地验证解析器、生成器、检查器及 golden 比较 | 否 |
| `run_agent_case.py` | 是 | 通过真实 Codex 多轮会话验证 Skill workflow | 是 |

普通单元测试可以用协议兼容的假 Codex 验证 runner 自身，但不能把假 Codex 的通过宣称为真实 Agent E2E 通过。

## 3. 标准目录

```text
harness/tests/e2e/<case_id>/
├── case.json
├── input/
│   ├── command-spec.txt
│   └── user-prompt.txt
├── expected_output/
│   └── workflow_trace.json
├── run_case.py
└── run_agent_case.py
```

规则如下：

- `case.json` 是用例清单和比较契约的唯一入口。
- `input/` 仅存放该用例的版本化输入；项目不建立公共 `fixtures/`。
- `expected_output/` 只保存稳定、去敏、可审阅的预期契约。
- 实际输出写入调用者指定的新建或空目录，不默认提交仓库。
- 用例不得依赖用户本地绝对路径、人工点击、历史聊天状态或未登记的共享文件。
- 输入文件以 SHA-256 锁定；动态输出通过明确的规范化规则比较，禁止宽泛忽略整个文件。

## 4. `case.json` 契约

每个 Agent E2E 用例至少登记：

- `schema_version`、`case_id`、`feature_ids`；
- `automation.agent_runner`、`automation.agent_command` 和 `requires_human_input: false`；
- `input`：初始用户提示、附件和完整多轮 conversation；
- `fixtures`：本用例输入文件的相对路径、用途和 SHA-256；此字段是清单名称，不代表建立公共 `fixtures/` 目录；
- `preconditions`：Agent、CLI、运行依赖、许可证和 EDA 环境要求；
- `expected_output`：最终状态、每个必需产物、等待状态和禁止项；
- `comparison`：每个预期输出对应的确定性比较方法；
- `actual_output`：采集范围和保留策略。

conversation 中每一个用户响应必须固定并版本化。若 workflow 有多个合法分支，应拆成独立用例，不允许测试运行时临时询问人类选择。

## 5. Agent runner 标准流程

### 5.1 隔离和安装

1. 拒绝非空输出目录，避免旧产物造成假通过。
2. 创建隔离 workspace。
3. 将当前仓库的 `skill/` 副本安装到 workspace 的 `.codex/skills/eda-tester-skill/`。
4. 将该用例的 `input/` 复制到 workspace。
5. 仅允许 Agent 向 workspace 内约定的 `delivery/` 写入交付物。

### 5.2 首轮启动

首轮必须使用 `codex exec --json`，并在 prompt 中显式写出 `$eda-tester-skill`。同时应：

- 指定隔离工作目录和可写沙箱；
- 要求读取版本化输入文件；
- 限制真实 EDA、许可证和外部设计数据库访问；
- 用 JSON Schema 约束最终响应，至少含 `state`、`summary`、`artifacts`；
- 保存完整 JSONL，不只保存最终自然语言消息。

runner 从 `thread.started` 事件取得 session ID。缺少 session ID、JSONL 非法、回合未以完成/失败事件结束或结构化最终响应缺失，均为执行失败。

### 5.3 多轮恢复和等待门禁

后续固定用户响应通过 `codex exec resume` 和同一 session ID 发送。不得为每个回合新建无上下文会话。

每个 WAIT 门禁必须同时验证“状态”和“副作用边界”。以当前范例为例：

| 回合 | 固定用户输入 | 期望状态 | 必须存在 | 禁止项 |
|---|---|---|---|---|
| 1 | 初始需求与命令说明 | `WAIT-STRATEGY` | session ID | Excel、TCL |
| 2 | 选择三种策略 | `WAIT-DESIGN-CONFIRMATION` | 非空 Excel 测试计划 | 任何 TCL |
| 3 | 确认设计及 design/tech | `DELIVERED` | Excel、每行对应的 TCL 用例 | 未解决的失败或缺口 |

只检查最终 `DELIVERED` 不足以覆盖 workflow；如果确认前已经生成 TCL，即使最终产物正确也必须失败。

### 5.4 独立验证

模型交付后，runner 必须从文件系统重新发现产物，并使用仓库中的确定性工具独立验证：

- Excel：模板/工作簿结构、字段、编号以及可脚本化规则；
- TCL：目录树、文件命名、固定标记、调用形式、顺序和其他静态规范；
- workflow：实际状态序列和证据对照版本化预期 trace；
- 禁止项：提前生成、空产物、本地绝对路径、许可证、PDK、客户数据或敏感日志。

模型声称“检查通过”不能替代这些检查器。语义规则确实需要模型参与时，也必须输出逐规则的结构化证据，runner 再检查规则集合、状态取值、缺失项和阻塞项。

## 6. 断言矩阵

一个完整用例至少覆盖下列断言层：

| 层 | 断言对象 | 典型证据 | 裁决者 |
|---|---|---|---|
| 调用 | Skill 是否显式触发 | 首轮 prompt、JSONL | 脚本 |
| 会话 | 是否在同一线程继续 | `thread.started`、session ID、resume 调用 | 脚本 |
| 控制流 | WAIT/DELIVERED 顺序 | 每轮结构化 `state` | 脚本 |
| 副作用 | 文件生成时机 | 每轮结束后的目录快照 | 脚本 |
| 业务产物 | Excel/TCL 内容与结构 | 独立检查器输出 | 脚本 |
| 语义 | 场景合理性和规则审查 | 逐规则结构化记录 | 模型生成、脚本校验完整性 |
| 安全 | 敏感信息与越界访问 | 产物扫描、执行限制 | 脚本 |

最终结果只能由 runner 汇总，不采用自然语言相似度或“看起来合理”作为通过标准。

## 7. 结果状态和退出码

- `PASS`，退出码 `0`：所有回合、门禁、产物、独立检查和禁止项检查均通过。
- `FAIL`，退出码 `1`：Skill 行为、状态、产物、格式、语义证据或 runner 协议不符合用例契约。
- `TOOL_UNAVAILABLE`，退出码 `2`：Codex 可执行文件缺失、认证不可用、CLI/服务端协议不兼容、模型目录不可用等导致测试没有真正开始或无法继续。

`TOOL_UNAVAILABLE` 不是 PASS，也不得降级为静态 runner 的结果。报告必须保留原因，但要截断和去敏，禁止归档 token、许可证或完整私有日志。

## 8. 稳定性策略

模型输出可能存在措辞和排列差异，因此稳定性来自“约束和裁决”，不是假设模型逐字重复：

- 固定输入、回合顺序、Skill 版本、输出 schema 和允许写入范围；
- 优先比较状态、结构、集合、规则结果和经过规范化的业务字段；
- 不断言自由文本逐字相等，除非它本身就是业务契约；
- 模型、CLI 或推理配置需要固定时，在用例元数据和执行报告中记录；
- 对非确定性风险较高的用例可登记有限重跑策略，但不得用“多跑几次取一次成功”掩盖真实失败；
- 单元层通过假 Codex 稳定覆盖 runner 协议，真实 Agent E2E 由显式命令启动并单独报告。

## 9. 证据与归档

每次执行至少保存：

- 每轮 JSONL 事件；
- 每轮结构化最终响应；
- session ID、CLI/模型版本和环境摘要；
- 每个门禁的断言结果；
- 生成文件清单及独立检查器结果；
- 汇总文件 `agent-e2e-result.json`。

默认实际输出为临时保留。只有去敏且确有回归价值的 golden/trace 才进入 `expected_output/`；原始运行日志、用户路径和外部设计数据不得提交。

## 10. 新增用例清单

新增或评审 Agent E2E 用例时逐项确认：

- [ ] 用例覆盖一个清晰的用户 workflow 分支，并绑定功能 ID。
- [ ] 输入和每轮用户回复均已版本化，不需要人工交互。
- [ ] `case.json` 为所有输入登记相对路径和 SHA-256。
- [ ] `run_case.py` 仅承担确定性集成验证，未冒充真实 Skill E2E。
- [ ] `run_agent_case.py` 在隔离 workspace 安装当前 Skill。
- [ ] 首轮显式调用 `$eda-tester-skill` 并使用 `codex exec --json`。
- [ ] 后续回合通过 `codex exec resume` 和同一 session ID 驱动。
- [ ] 每个 WAIT 状态都同时断言允许产物和禁止项。
- [ ] 最终产物由独立检查器重新验证。
- [ ] runner 输出 `PASS`、`FAIL` 或 `TOOL_UNAVAILABLE` 以及约定退出码。
- [ ] runner 有不调用真实模型的协议单元测试。
- [ ] 用例可重复执行，不依赖人工操作、历史会话或未登记环境。
- [ ] 输入、预期和归档证据已去敏。

## 11. 当前标准范例

标准范例为 `harness/tests/e2e/optimus_check_design_data_full_workflow`。它以命令说明和用户提示词启动场景一，依次触发 `WAIT-STRATEGY`、`WAIT-DESIGN-CONFIRMATION` 和 `DELIVERED`，并在确认后独立验证 Excel 与 TCL。

真实 Agent E2E 的统一执行方式：

```sh
./init.sh test agent-e2e harness/tests/e2e/optimus_check_design_data_full_workflow \
  --output /tmp/eda-agent-e2e
```

runner 协议自身的稳定回归通过对应功能验证命令执行；真实命令只有在 Codex CLI、认证和模型服务可用时才能产生 PASS。
