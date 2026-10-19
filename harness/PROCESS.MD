# EDA Tester Skill 项目进度

最后更新：2026-10-20

项目仓库：<https://github.com/biggeryounger/eda-tester-skill>

仓库状态：2026-08-07 完成首次 GitHub 推送；后续只跟踪该 GitHub 仓库，不再使用或同步 Gitee。

## 当前交接快照

- 当前功能：无；F-036“Agent E2E 用例规范与范式”已完成并标记为 `passing`。
- 工作区状态：当前分支包含既有未提交开发改动；本功能只新增项目侧 Agent E2E 规范、规范契约测试和文档路由，不修改 Skill 运行时产物。
- 最近验证：2026-10-20 删除目标版本可选门禁并补齐兼容覆盖明确文本后，`./init.sh test all` 完整通过：171/171 单元与回归测试 PASS，隔离 Skill 包结构 PASS。
- 阻塞项：真实 Codex 会话验证仍受本机 codex-cli 0.133.0 与当前模型列表协议不兼容影响；不影响协议自动化测试和本次完整门禁。
- 下一条命令：检查上传差异并推送 `codex/` 候选分支
- 涉及文件：`harness/references/agent-e2e-pattern.md`、`harness/references/e2e-test-set.md`、`harness/tests/unit/test_agent_e2e_pattern.py`、`harness/function.json`、`harness/PROCESS.MD`

## 当前目标

完成一个面向 EDA 命令的 Codex Skill：从命令说明或自然语言需求生成测试场景、Excel 测试计划和 TCL 用例，并通过确定性程序完成验证。当前优先支持 Cadence Innovus。

## 当前状态

- 当前活动功能：无。
- 已通过功能：F-002、F-004、F-005、F-006、F-012、F-013、F-015、F-016、F-017、F-018、F-019、F-020、F-021、F-022、F-023、F-024、F-025、F-026、F-027、F-028、F-029、F-030、F-031、F-032、F-033、F-034、F-035、F-036。
- F-015 TCL 脚本规范检查器已升级为目录树模型（`nith.run` + `tcl/design.tcl` + `tcl/<tool>/{run_1.tcl…run_N.tcl, mmmc.tcl}`），状态为 `passing`。
- F-020 TXT 命令说明结构化解析器已实现并通过功能级验证，状态为 `passing`。
- F-021 工具命令 Help 批量采集脚本已实现并通过功能级验证，状态为 `passing`。
- 其余功能保持 `not_started`。

功能状态的唯一正式来源是 `function.json`；本文件只记录会话交接信息，不替代功能清单。

## 历史记录

### 已完成工作

- 2026-10-20 新增 F-036“Agent E2E 用例规范与范式”：在 `harness/references/agent-e2e-pattern.md` 固化“确定性控制器 + 真实模型执行 + 确定性最终裁决”的测试模型，明确静态 runner 与 Agent runner 分工、隔离安装、`codex exec --json`/`resume` 多轮协议、WAIT 状态与产物时序、独立验证、断言矩阵、三态结果与退出码、稳定性及证据归档规则，并提供可复制的新增用例清单和当前标准范例。`e2e-test-set.md` 已增加文档路由；规范契约 4/4 PASS、完整 workflow 用例契约 5/5 PASS、项目清单 PASS。
- 2026-10-18 新增 F-035“Codex Skill Agent E2E 执行层”：在隔离工作区安装当前 `skill/` 副本，通过 `codex exec --json` 显式调用 `$eda-tester-skill`，解析 `thread.started` session ID，再以 `codex exec resume` 依次提交三策略选择和 riscv/SMIC28 确认；强制三轮结构化状态为 `WAIT-STRATEGY`、`WAIT-DESIGN-CONFIRMATION`、`DELIVERED`，确认前禁止 TCL，交付后独立执行 Excel/TCL 检查器。新增 `./init.sh test agent-e2e` 统一入口、协议兼容假 Codex 自动化测试及 `TOOL_UNAVAILABLE` 分类。真实冒烟已调用本机 Codex，但 codex-cli 0.133.0 因不能解析模型列表新增的 `max` reasoning 值在首轮前中止；框架正确记录为 `TOOL_UNAVAILABLE`。
- 2026-10-18 新增 F-034“完整 Workflow E2E Runner”：为 `optimus_check_design_data_full_workflow` 增加无需人工输入和 EDA 许可证的自动化 `run_case.py`，实际解析命令说明，生成覆盖率、四条场景的模板化 Excel、自包含 Optimus TCL 用例、语义审查记录和执行 trace；实际调用 Excel/TCL 确定性检查器，并分别比较结构化规格、覆盖率、Excel、TCL 和 workflow trace 五类预期输出。runner 拒绝覆盖非空输出目录；双次运行测试验证 JSON、Excel 规范化行和 TCL 树稳定一致。测试先行基线按预期 FAIL，实现后 runner 2/2 PASS、用例契约 5/5 PASS。
- 2026-10-18 新增 F-033“测试目录收敛”：删除不再需要的 `harness/tests/cases` 和 `harness/tests/fixtures`，清理 F-003/F-004/F-005 的旧路径登记及项目验证器中的 cases 扫描、`--cases` 参数和旧 `case.toml` 校验逻辑；测试目录只保留 `unit`、`regression`、`e2e` 三类有效资产。新增项目硬规则，要求构建 Skill 测试用例必须使用可重复、可稳定运行的自动化脚本，禁止一次性人工操作或不可复现交互结果；契约测试锁定目录和规则。两组测试先行基线均按预期 FAIL，实现后目录结构测试 7/7 PASS、项目验证器测试 5/5 PASS。
- 2026-10-18 新增 F-032“完整 Workflow 端到端用例”：以去敏的 Optimus `check_design_data` 命令说明文本和显式 Skill 用户提示词作为输入，通过多轮对话分别触发 `WAIT-STRATEGY` 与 `WAIT-DESIGN-CONFIRMATION`，并用版本化 golden trace 按顺序登记从场景一路由、命令解析、策略和场景设计、覆盖率、Excel、Design/Tech 资源映射、TCL 生成、双层检查到交付的 14 个必经步骤。fixture 使用 SHA-256 锁定，结构化规格、覆盖率、Excel、TCL 和 trace 均登记确定性比较方法；测试先行基线按预期 FAIL，实现后 5/5 PASS。
- 2026-10-18 新增 F-031“当前交接快照”：在 `PROCESS.MD` 顶部建立固定六字段快照，集中记录当前功能、工作区状态、最近验证、阻塞项、下一条命令和涉及文件；累计完成内容与旧验证结果移入独立历史区。新增契约测试锁定快照位置、字段集合和历史边界，测试先行基线按预期 FAIL，实现后 3/3 PASS。
- 2026-10-15 新增 F-030“用户规则覆盖登记”：在 `harness/references/user-rule-coverage.md` 建立项目侧规则台账，首批登记 17 条既有用户规则；新增自动测试验证稳定编号、规则分类、证据文件和职责层级。静态规则必须同时关联 Skill 检查器与项目单元测试，语义规则必须关联语义规范，workflow 规则必须关联 Skill 入口或注册元数据，项目规则必须关联 `AGENTS.md` 与项目测试。
- 2026-10-15 F-030 测试先行验证：登记文档缺失时专项测试按预期 FAIL；完成台账后 3/3 PASS。测试同时发现覆盖率输出契约在 `SKILL.md` 中表达不足，现已明确场景覆盖率与被测选项覆盖率均报告分子、分母、百分比和未覆盖项，工具不可用时报 `TOOL_UNAVAILABLE` 且不得以人工判断替代。
- 2026-10-15 将 SKILL 通用 TCL 约束纳入 `tcl_convention_validator.py` 静态检查：既有规则继续覆盖唯一工具目录、单步/多步命名、design 输入集中、声明式 MMMC、每 run 初始化与标记/checkpoint/收尾、环境变量和路径限制；新增 TCL-MMMC-002 检查工具方言隔离，新增 TCL-SCRIPT-006 拒绝伪造 PV marker 与强制设置 `PV_CHECK_MODE`。
- 2026-10-15 新增项目硬规则：Skill 产物中的验证脚本、运行资源和文档，与 `harness/` 中的项目开发验证脚本、测试资源和开发文档必须完全物理分离，禁止混合职责和跨目录维护。规则已写入 `AGENTS.md` 并由仓库结构测试自动锁定。
- 2026-10-15 删除 `skill/scripts/validate.py`：项目清单与功能验证迁到 `harness/scripts/project_validator.py`；Skill 运行时直接执行 `test_plan_validator.py` 和 `tcl_convention_validator.py`，两者新增独立 CLI；`init.sh` 仅在项目侧编排这些专项入口。删除旧混合交付门禁测试并将 F-006 改为验证职责分离与顺序编排。
- 2026-10-15 拆分验证结果：完整单元测试 150/150 PASS；F-024、F-006、F-027、F-028 专项验证 PASS；Skill 结构、项目清单和差异格式检查 PASS。
- 2026-10-15 新增 F-029“Design/Tech 资源映射”：用户只确认 design 和 tech，Skill 根据已登记映射自动确定对应的 `design.tcl` 和目标工具方言 `mmmc.tcl`，再自包含归档到每个用例目录；用户无需选择 TCL 文件，也不新增重复等待门禁。
- 2026-10-15 修改脚本生成输入动作：不再由 workflow 自动生成 `design.tcl` 或选择默认 MMMC；用户必须先明确选择 design 与 tech，再将对应的 `design.tcl` 和目标工具方言 `mmmc.tcl` 分别复制归档到每个用例的 `tcl/design.tcl` 与 `tcl/<tool>/mmmc.tcl`。design/tech 确认并入现有 `WAIT-DESIGN-CONFIRMATION`；已有设计表缺少映射时沿用 `WAIT-PLAN-FIX`，不新增重复等待门禁。
- 2026-10-15 删除混合职责的 Skill 统一验证脚本：Skill 直接执行 `test_plan_validator.py` 与 `tcl_convention_validator.py`；项目开发只通过 `harness/scripts/project_validator.py` 验证清单和功能。运行时验证脚本、测试资源、文档与项目开发资产完全分离。
- 2026-10-15 优化“脚本生成与交付门禁”：`SKILL.md` 现在分别执行确定性脚本结构与编程规范检查、EDA 工具脚本静态检查、Agent 语义审查及 Excel → TCL 组合/覆盖率门禁；新增 `WAIT-SCRIPT-DELIVERY-FIX`，明确等待 `FAIL`、`SPEC-GAP` 和 `TOOL_UNAVAILABLE` 的修复条件。
- 2026-10-15 将 `tcl-script-rules.md` 收敛为纯 Agent 语义审查规范，仅保留设计到脚本追溯、工具方言与初始化、检查点充分性、多步数据流与交付完整性四类 `TCL-SEMANTIC-*` 规则；目录、命名、固定标记、白名单、调用形式和顺序等可脚本化职责移至 `tcl_convention_validator.py` 模块注释。
- 2026-10-15 验证结果：F-015 45/45 PASS，F-027 4/4 PASS，F-028 5/5 PASS；Skill 结构、项目清单及 `git diff --check` 均通过。
- 2026-10-14 精确化 `SKILL.md` 的 Excel 门禁：Workflow 明确直接运行 `scripts/test_plan_validator.py` 完成结构检查，再读取 `references/specs/test-plan-rules.md` 完成 Agent 语义审查；两项均通过后才能进入设计确认或 TCL 生成。
- 2026-10-14 将 `test-plan-rules.md` 收敛为纯 Agent 语义审查规范，仅保留 PLAN-006～013 的 EDA 语义、步骤可执行性、预期充分性、正负一致性和追溯判断；全部结构、格式和关键词预筛职责移至 `test_plan_validator.py` 模块注释，不再在 spec 中重复维护。
- 2026-10-14 为 Workflow 增加显式等待门禁：`WAIT-STRATEGY` 等待策略选择，`WAIT-DESIGN-CONFIRMATION` 等待用例设计批准，`WAIT-PLAN-FIX` 等待已有设计表问题修正；每个门禁均明确等待内容、继续条件和不能解除等待的含糊输入。
- 2026-10-14 将两种工作场景正式收敛到 `SKILL.md` 的 `Workflow` 章节：入口先选择且只执行“从命令说明设计新用例”或“从已有用例设计表生成脚本”之一，两条分支最终进入共享的脚本生成与交付门禁。
- 2026-10-14 新增 F-028“双场景 workflow 路由”：场景一接收被测命令说明，完成用例设计、模板化 Excel、覆盖检查和用户确认后才生成 TCL；场景二接收已有测试用例设计表，校验并解析后直接按表生成 TCL，不重复策略选择或擅自改写设计。已有表格存在缺失、歧义或冲突时停止并列出问题。契约测试按测试先行流程由 FAIL 转为 PASS。
- 2026-10-14 新增 F-027“Skill workflow 工具契约”：workflow 明确要求 EDA 工具脚本静态检查分别覆盖 Tcl 基础语法、EDA 工具命令及选项使用、TCL 编程规范；覆盖率检查分别报告场景覆盖率和被测选项覆盖率，并输出分子、分母、百分比和未覆盖项。工具或版本语法库不可用时必须报告 `TOOL_UNAVAILABLE`，不得以人工判断替代。契约测试按测试先行流程由 FAIL 转为 PASS。
- 2026-10-14 优化 Skill 注册元数据：`agents/openai.yaml` 的 `short_description` 按“做什么；何时使用；关键能力”三段组织，明确用户显式调用边界和场景分解、Excel 计划、TCL 生成、静态验证能力；同步精简默认提示词并保留 `allow_implicit_invocation: false`。新增元数据契约测试。
- 2026-10-14 将“Skill 目录内禁止 README.md”固化为产物结构约束：确认当前 `skill/` 中没有 README，仓库级/开发环境 README 不受影响；新增递归单元测试和快速结构检查，文档继续只放在 `SKILL.md` 或 `references/`。
- 2026-10-14 重构前确认 Skill 触发边界：`skill/agents/openai.yaml` 已设置 `policy.allow_implicit_invocation: false`，因此该 Skill 只允许用户显式调用；`SKILL.md` 的 `description` 不承担此强制约束。项目验证与 Skill 结构检查均通过。后续重构应先增加该策略的确定性回归测试，防止配置被误删或改为隐式触发。
- 2026-10-14 将顶层验收改为两层：Layer 1 验证 Skill 环境、工具与启动正常；Layer 2 使用版本化端到端测试集验证真实用户输入及对应输出。
- Excel 和 TCL 规范静态门禁保留为 Layer 2 的内部输出检查，不再作为独立顶层结果宣称端到端通过。
- 新增 `references/e2e-test-set.md`，定义 `case.json` 的输入、fixtures、预期输出、比较规则和实际输出字段，以及确定性比较、版本和脱敏要求。
- 新增 F-023“两层验收标准”和 4 项契约测试；功能级验证通过。F-006 更名为“静态输出检查编排”，准确反映现有 `delivery` 命令职责。
- 2026-10-14 将 Skill 运行产物与项目开环环境隔离：`SKILL.md` 只保留最终用户能力、生成流程和运行时规则，不再引用项目两层验收、端到端测试集或 `function.json`。
- 安装器改为显式运行时白名单并逐文件安装；`references/test-plan.md`、`references/e2e-test-set.md`、知识库/屏幕传输设计稿、`scripts/install_skill.py` 和环境自检脚本不再进入已安装 Skill。链接与复制模式隔离测试均通过，F-016 更新为 15/15 PASS。
- 2026-10-14 完成物理目录隔离：`skill/` 是唯一可安装产物目录，包含 `SKILL.md`、Agent 元数据、运行资产、生成规范和运行脚本；`harness/` 集中存放 `PROCESS.MD`、`function.json`、项目验收文档、安装器、测试、生成结果和运行输出。新增 F-024，目录结构及安装验证 17/17 PASS。
- 2026-10-14 参考 `e2_pv_kit` 建立 Jenkins 人工审批合入门禁：参数化选择候选 ref，锁定候选与远端主分支提交，运行完整用例集，发布 JUnit/HTML/日志，人工批准后再次复核提交与主分支未变化，再 fast-forward 推送。
- Jenkins 环境固定 Python、openpyxl 和 Tcl；初始化脚本自动创建任务与 GitHub 凭据，README 明确要求 GitHub `main` 禁止绕过 Jenkins 直接推送。
- 2026-10-14 按项目实际验证需求移除第三方 TCL 静态语法工具：删除适配器、syntax database、安装选项、集成测试和 Jenkins 镜像依赖；`tcl` 与 `delivery` 仅保留项目 TCL 规范检查，真实语法由目标 EDA 工具端到端测试负责。
- 新增根目录 `init.sh` 统一入口：`dev` 安装隔离开发环境，`deploy` 部署 Skill，`test all/layer1/layer2/unit/project/skill/feature/tcl/plan/delivery` 运行全量、分层或指定场景测试；F-026 专项测试 4/4 PASS。
- `AGENTS.md` 的验证章节已改为只公开 `init.sh` 统一入口、分层语义和返回码约定，不再重复维护底层 Python 命令。
- Skill 安装说明也已收敛到 `init.sh help`：包含支持的 Agent、默认 link/copy 模式、运行时白名单、自定义目录、禁止覆盖、重启扫描、显式启动和未识别排查；`AGENTS.md` 仅保留 `init.sh deploy` 示例。
- 新增用户触发的结束动作契约：仅当用户明确说“上传代码”时，才依次更新 Skill/README 与项目状态、运行全量门禁、推送候选分支、触发 Jenkins，并等待用户审批；普通任务完成不自动上传或触发流水线。
- 首次“上传代码”触发暴露 Jenkins 自举问题：任务原先从尚未包含新 Jenkinsfile 的 `main` 加载流水线而失败。现改为由 Jenkins 镜像/只读挂载提供受控 Jenkinsfile，流水线启动后再检出精确候选提交，不依赖 `main` 预先包含流水线文件。
- 2026-10-14 优化 Jenkins HTML 报告：新增“完整门禁 → 检查组 → 自动化测试用例”的结构摘要，以及检查组、用例总数、通过/失败/跳过和总耗时指标；解析 unittest 明细为按检查组组织的可视化表格，所有用例表格默认折叠，完整日志继续独立折叠展示。F-025 专项验证通过。

- 2026-09-08 将 `SKILL.md` 按渐进披露原则压缩为三部分：通用重要规则、工作流程、参考文档索引；总字符数 1,982（含空白），详细规则下沉到 references。相关入口契约测试 26/26 通过，Skill 结构检查通过。
- 2026-09-08 按《EDA用例规则规范去重Checklist》统一规则重构生成门禁：解决单步 `run.tcl` 与旧 `run_1.tcl` 冲突；单步强制无编号，多步才使用连续 `run_1.tcl … run_N.tcl`。
- Layer 2B 新增/收紧：每个 run 独立 checkpoint、MMMC 声明式限制、CMD 禁止 DEF golden、完整占位符集合、`nith_run()` 数量匹配及 `nith_done()` 恰好一次。
- 新增 `references/manual-review-rules.md`，把无法由静态程序证明的覆盖语义、场景合并、版本依据、可观察预期、BUILD 来源、真实结果和归档压缩为 12 项强制人工审查；Skill 要求设计阶段和交付门禁后各执行一次。
- `SKILL.md` 去除重复/冲突的 run 规则，并明确任何后续生成结果都必须通过 Layer 1 → Layer 2A → Layer 2B，静态 PASS 与人工语义/实机结果分开报告。
- 新增规则专项测试通过 44/44；相关策略与规则测试 48/48 通过；Skill 结构检查通过。完整单元测试 127 项中 124 项通过，另 3 项仍是既有缺失 fixture 问题。

- 清除测试计划模板中剩余的 7 张工作表图片；`generate_test_plan.py` 在写入用例前也会清除模板携带的全部图片，避免更换模板后再次混入无关图。F-017 回归测试要求模板及生成结果的图片数均为 0。
- 2026-08-29 图片清理验证：`tests.unit.test_test_plan_generator` 4 项全部通过，Skill 结构检查通过；完整单元测试共 122 项，其中 119 项通过，3 项因仓库既有的 `tests/cases/pos001_sample_minimum` 与 `neg001_sample_missing_required` 缺失而失败，项目门禁同因失败，与本次图片改动无关。
- 新增 `references/case-knowledge-base-design.md`，完成独立 EDA 用例生成知识库 `1.0-draft` 架构设计；定义命令语义、测试模式、业务场景、故障模式、环境初始化、检查点和历史案例七类知识，以及统一元数据、来源、版本、可信度、脱敏、检索适配、反馈闭环和确定性验证要求。本次仅完成设计，不新增或启动功能点。
- 建立 Skill 基础结构、界面元数据、模板、规范和测试目录。
- 建立 `function.json` 功能清单和单一活动功能门禁。
- 建立正负用例目录、`case.toml` 元数据和基础 TCL 契约检查。
- 接入 Nagelfar 1.3.5，并建立 Innovus/iTools syntax database。
- 建立项目入口 `./init.sh`，按职责分别调度项目开发验证与 Skill 运行时专项检查。
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
- 为 F-013 实现独立的 Excel Layer 1 确定性检查器 `scripts/test_plan_validator.py`，并在统一入口增加 `plan` 子命令。
- 检查器覆盖 PLAN-001 至 PLAN-014，包括工作簿/工作表、A-J 表头、核心字段、命名与连续编号、描述/步骤/预期、管理字段警告、正负属性及需求清单追溯。
- PLAN-013 支持 `--requirements` JSON 清单，按命令和测试点字符串确定性检查覆盖，不使用 Agent 判断。
- 新增 14 组单元测试，逐条证明 PLAN-001 至 PLAN-014 存在通过样例和失败样例；PLAN-011 仅产生 warning，不导致 Layer 1 失败。
- F-013 功能级验证通过并更新为 `passing`。
- 尝试进入 F-014 真实端到端复核，但当前 `PATH` 和仓库内均无 Nagelfar 1.3.5，按验收门禁将 F-014 标记为 `blocked`。
- 从官方 SourceForge `Rel_135/nagelfar135.tar.gz` 安装 Nagelfar 1.3.5 到用户级目录 `~/.local/share/nagelfar/nagelfar135`；下载包 SHA-256 为 `3baf920fb34b73e32067118365d074d859298e2bce3748ad9458624bece85b23`。
- 在 `~/.local/bin/nagelfar` 建立命令软链接，适配器无需设置用户本地绝对路径即可从 `PATH` 发现检查器。
- 新增 `scripts/verify_nagelfar_install.py` 真实安装验收命令，并登记为 F-014 的 `integration-nagelfar` 验证。
- 真实 Nagelfar 1.3.5 对有效 `add_net` 样例返回 PASS，对包含 `-unknown` 的无效样例返回 FAIL，并准确报告第 3 行错误。
- F-014 功能级验证通过并更新为 `passing`。
- 新增 `scripts/install_skill.py`，默认将当前项目以软链接方式安装到 Codex Skills 目录，并支持 `--mode copy` 独立复制。
- 安装器支持 `--skills-dir`、`--source`、`--dry-run` 和离线 Nagelfar 安装包；安装前检查 Skill 核心结构，拒绝覆盖已有目标。
- `--install-nagelfar` 从官方发布地址安装固定版本 1.3.5，执行固定 SHA-256 校验、安全解包和版本探测，并建立用户级命令链接。
- 新增 7 组安装器测试，覆盖软链接、复制排除仓库状态、已有目标保护、非法源、dry-run、Nagelfar 离线安装及校验和失败。
- F-016 功能级验证通过并更新为 `passing`。
- 依据用户提供的 Optimus `check_design_data -help` 截图生成 Smoke case 交付物：模板化 Excel 测试计划、`pos001_file` / `pos002_netlist` 两个完整用例树、需求清单和命令专用 Nagelfar syntax database；未写入 PDK、设计数据库或本地设计路径。
- `check_design_data` Smoke 测试计划连同 `-file <String>`、`-netlist` 需求清单通过 Layer 1；Layer 2A 因当前 `/usr/bin/tclsh` 为 Tcl 8.5.9、Nagelfar 1.3.5 要求 Tcl 8.6 而返回 `TOOL_UNAVAILABLE`，未误报通过；Layer 2B 检查器仍未实现。
- 根据用户实际交付反馈，将输出契约改为只交付已填充 `.xlsx` 和独立 `.tcl` 文件，不再生成用例目录、`case.toml`、`nith.run`、README 或运行说明。
- 实现 `scripts/generate_test_plan.py`：清除模板历史业务行、写入非空场景、重新打开计数并强制通过 Layer 1；空场景输入不产生文件。
- 将 Layer 2B 规范升级为 `1.0 CONFIGURED`，实现 `scripts/tcl_convention_validator.py` 及 TCL-SUITE/RUNNER/CHECKPOINT/SCRIPT 11 条规则的自动化正反样例。
- TCL 专项检查按 Layer 2A → Layer 2B 执行；语法失败或工具不可用时 2B 返回 `SKIPPED`。
- Nagelfar 适配器主动选择 Tcl 8.6+，本机成功绕过 `/usr/bin/tclsh 8.5.9` 并使用 `/opt/homebrew/bin/tclsh 9.0.3`。
- 独立 `pos001_add_net.tcl` 端到端验证结果：Layer 2A PASS、Layer 2B PASS。
- F-015 和 F-017 功能级验证通过并更新为 `passing`。
- 将测试策略规范升级为 `1.1`：默认采用“单用例多测试点”，优先把同命令、同前置状态、同预期性质的兼容 option、枚举值和检查点合并到一个用例。
- 明确拆分边界：选项互斥、前置状态不同、预期性质不同、合并会破坏故障定位或必须独立观察的枚举/边界值。
- 合并用例在 Excel 的描述、步骤、预期中分别以“测试点 N / 步骤 N / 预期 N”逐项对应，并继续维护 option/枚举/约束到用例的覆盖矩阵。
- 新增 3 项场景策略契约测试，F-002 功能级验证通过并更新为 `passing`。
- 定位 `check_design_data_smoke.xlsx` 看似空表的根因：模板第 2 行为隐藏状态，生成器复制行格式时连同 `hidden=True` 一并继承；自动筛选还残留 `A1:K57`。
- PLAN-014 新增有效用例行必须可见、不可折叠且筛选范围必须匹配实际 A-J 数据范围的确定性检查和失败样例。
- `generate_test_plan.py` 现在强制取消生成行的隐藏、折叠和 outline 状态，并把筛选范围重设为实际 `A1:J<N>`。
- 使用保留的场景 JSON 原子重建 `check_design_data_smoke.xlsx`；行 2、3 可见，筛选范围为 `A1:J3`，Layer 1 PASS。
- 按当前独立文件交付规范重建 Optimus `check_design_data` Smoke 交付物：`pos001_default.tcl` 覆盖无选项默认调用，`pos002_file_netlist.tcl` 合并覆盖 `-file <String>` 与 `-netlist`；后者会删除旧报告并确定性检查指定相对目录生成的报告是非空普通文件。
- 新版 `check_design_data_smoke.xlsx` 由非空 scenarios JSON 从模板生成并重新打开校验；含“默认调用”、“-file <String>”、“-netlist”的需求追溯检查通过。两个独立 TCL 均通过 Nagelfar 1.3.5 Layer 2A 与脚本规范 Layer 2B。
- 将 TCL 脚本规范升级为 `1.1`，新增 `TCL-SCRIPT-003` 系统环境变量白名单：生成脚本只能读取、检查或设置 `PV_ROOT`、`PV_TOOL`，禁止 `PV_ENTRY`、自定义 setup 变量和 `HOME` 等其他变量。
- Layer 2B 检查器已确定性识别 `$env(NAME)`、`$::env(NAME)`、`env(NAME)` 和 `::env(NAME)` 的读取、检查与设置写法；新增白名单通过样例和三类禁止写法失败样例。
- Skill 生成规则不再通过新增环境变量补充设计 setup；setup 必须来自用户提供的 TCL 内容或相对路径，信息不足时记录实机运行缺口。
- 重建 Optimus `check_design_data` Smoke Excel 与两个独立 TCL：步骤和脚本仅使用 `PV_ROOT`，并移除旧用例目录、`case.toml`、`nith.run` 和 README 交付物。
- 将 TCL 脚本规范升级为 `1.2`，新增 `TCL-SCRIPT-004`：每个用例必须在 `# TEST_ACTION` 前包含唯一的 `DESIGN_INIT` 初始化段及真实 EDA 设计激活命令，禁止依赖预加载设计会话。
- Layer 2B 已确定性识别 Optimus `setup_design`、iTools / Innovus `init_design`/`read_db`/`restoreDesign`、PrimeTime `open_block`/`link_design`；缺失标记、空初始化段或动作后初始化均返回失败。
- Skill 现在要求先收集 design input、top、library、LEF、netlist、MMMC/约束等初始化信息；信息不足时停止 TCL 生成并列出缺口，不再交付半成品。
- 同步修正 Optimus TCL 语料：初始化设置必须展开到同一个独立 TCL，并用 `setup_design` 完成设计激活；缺少真实配置时不再使用语义占位符。
- 将测试策略规范升级为 `1.2`，增加用例设计确认门禁：场景分解和覆盖矩阵完成后，先生成并验证 Excel，再展示用例 ID、策略、测试点、初始化前置、步骤、预期、覆盖项、缺口和假设。
- Skill 必须明确询问“确认用例设计可用于生成 TCL 吗？”，只有收到用户明确批准后才能生成 TCL；策略选择或最初的生成请求不视为对尚未展示设计的确认。
- 用户提出修改、回复含糊或只补充资料时继续停留在设计确认阶段，修订并重新生成 Excel 后再次确认；新增契约测试确定性检查确认门禁位于 Excel 生成之后、TCL 生成之前。
- 新增 F-018 Optimus 默认设计初始化：提供 `assets/defaults/optimus/design.tcl` 和 `mmmc.tcl`。根据用户截图将默认版本更新为 `21.1`；默认设计位于 `$env(PV_ROOT)/svn/openedi/design_data/SMIC28/Itools21.1_lfp_util0.65/riscv_core`，top 为 `riscv_core`，包含两份 SMIC28 LEF、`floorplan.v.gz` 和 `floorplan.def.gz`；power/ground net 保持 `VDD`/`VSS`，MMMC 保持 `./mmmc.tcl`。
- 根据用户提供的 Optimus MMMC 截图替换默认 `mmmc.tcl`：使用 `design.tcl` 的 `$tech_dir` 和 `$design_dir`，定义 40c/125c 的四个 slow/fast lib set、四个 RC corner、四个 analysis corner、max/min mode、四个 analysis view 及对应 setup/hold 状态；测试确定性检查各类对象数量和关键映射。
- 新增 `scripts/optimus_defaults.py` 确定性逐字段解析器；未指定、`None` 或空白字段使用默认值，用户提供值逐字段优先。
- 新增 5 项正向/覆盖测试，检查完整回退、部分覆盖、空白回退、默认 TCL 可移植性和 Skill 契约；F-018 功能级验证通过并更新为 `passing`。
- 新增 F-019 iTools 默认 MMMC：根据用户截图创建 `assets/defaults/itools/mmmc.tcl`，保留 iTools / Innovus 的 `create_library_set`、`create_delay_corner`、`create_constraint_mode` 和 `set_analysis_view` 方言，并与 Optimus 默认 MMMC 隔离。
- 新增 4 项确定性测试，检查 4 个 library set、RC corner、delay corner、analysis view，2 个 constraint mode，单一 setup/hold view 选择，以及 iTools/Optimus 方言隔离；F-019 功能级验证通过。
- 清理 Excel 测试计划模板备注区的两张无关图片：仅删除锚定在第 2 行 I 列和第 3 行 K 列的图片，保留其余 7 张原有图片及全部单元格内容、格式和结构；新增 OOXML 回归测试锁定目标锚点。
- 改进 F-017 输出布局：生成器为 A-J 设置有上限的紧凑列宽，所有输出单元格启用换行，数据行按中英文显示宽度和显式换行确定性估算行高，并限制在 30–240 点；使用 `check_design_data` 两行样例完成视觉复核和公式错误扫描。
- F-017 生成器现在删除“用例描述”开头一个或多个大小写不敏感的 `[feature...]` 标签，并保留 `[strategy...]` 等其他方括号内容及描述正文；标签清理后为空时按核心字段缺失拒绝生成。
- 扩展 F-016 Skill 安装器，新增 `--agent`，支持 Codex、OpenCode、Hermes、WorkBuddy 和 Trae；不指定时保持 Codex 兼容行为。
- 为五种 Agent 配置用户级默认 Skills 目录和对应根目录环境变量；Codex 默认软链接，其他 Agent 为规避软链接扫描兼容性问题默认独立复制，`--mode` 和 `--skills-dir` 均可覆盖默认值。
- Skill 安装器测试增至 11 项，新增默认目录、Agent 选择、环境变量覆盖和非法 Agent 拒绝检查；F-016 功能级验证通过并恢复为 `passing`。
- 扩展 F-016 安装排除：软链接与复制安装均不再复制 `PROCESS.MD`、`AGENTS.md`、`function.json`、`tests/`、`generated/`、`outputs/` 和 `.gitignore` 等开发面向文件；保留 `SKILL.md`、`agents/`、`assets/`、`references/` 和 `scripts/` 等运行时文件。
- 软链接模式从“整目录单一软链接”改为“按运行时条目逐项软链接”的精简目录，使开发文件在安装目标中不再可见，同时运行时文件仍随源仓库实时更新；复制模式改为逐条目复制并在子目录内继续过滤 `__pycache__`、`*.pyc` 等。
- 安装器测试增至 14 项，新增复制排除、软链接排除和双模式保留运行时条目检查；F-016 功能级验证再次通过。
- 按用户确认的工具（Optimus）与策略（仅 Smoke case）重建 Optimus `check_design_data` Smoke 交付物。命令语义按用户描述更新：`-file <String>` 为必选（报告输出路径），`-netlist` 为可选布尔开关（仅检查 netlist 相关 items），不再存在无选项默认调用。
- Smoke 覆盖矩阵为两条不合并用例：`pos001_file`（仅含必选 `-file` 的最小合法调用）与 `pos002_file_netlist`（`-file` + `-netlist` 合法组合）。不合并原因：最小合法场景定义要求仅含必选参数，必须排除 `-netlist`，属互斥拆分；`-netlist` 无文档显式关闭值。
- 同步修正 `requirements.json`：旧清单含 `默认调用`，在 `-file` 必选前提下不可覆盖且会导致 PLAN-013 失败，已改为 `["-file","-netlist"]`。
- 新版 `check_design_data_smoke.xlsx` 由非空 scenarios JSON 从模板生成并重新打开校验，Layer 1 PASS，PLAN-013 对 `-file`/`-netlist` 追溯通过。
- 重建两个独立 TCL：`pos001_file.tcl`、`pos002_file_netlist.tcl`。每个脚本包含完整 `# DESIGN_INIT_BEGIN/END` 段（`source $env(PV_ROOT)/scripts/pv.tcl` → 内联写出 F-018 默认 `mmmc.tcl` → `set_options` 配置 LEF/netlist/top/power/ground/MMMC → `setup_design` 激活），`# EXPECT: PASS` + `# TEST_ACTION`，`pv_check_log` 检查点断言指定相对目录生成的报告是非空普通文件。
- 删除已失效的旧 `pos001_default.tcl`（无选项调用，在 `-file` 必选下属负向场景，不属 Smoke 正向用例）。
- 两个新 TCL 均通过 Nagelfar 1.3.5 Layer 2A 与脚本规范 Layer 2B，零诊断；确认顶层未知 Optimus 命令（`setup_design`、`set_options`）在共享 innovus syntax database 下仅产生 W，被 `-severity E` 抑制，Layer 2A 无需将其登记为 E。
- 将 F-015 TCL 交付模型从"独立单文件"完全替换为"用例目录树"：每个用例是一个目录，内含 `nith.run`（Python runner）和 `tcl/` 子树（`design.tcl` + `tcl/<tool>/{run_1.tcl…run_N.tcl, mmmc.tcl}`）。
- `nith.run` 逐字保留固定 NITH 初始化块（`### NITH initialization, please do not change this section` … `### NITH initialization end`），case-setup 段按序引用各 `run_<N>.tcl` 并调用 `nith_run()`/`nith_done()`；固定初始化块豁免可移植性和规范检查。
- 每个 `run_N.tcl` 自带 `# TEST_ACTION`/`# EXPECT` 标记；历史记录中的 `../design.tcl`、`./mmmc.tcl` 路径已由后续 v2.3 规则更正为基于用例统计目录的 `./tcl/design.tcl`、`./tcl/<tool>/mmmc.tcl`。
- `design.tcl` 按类别关键词（top/verilog/netlist/lef/lib/timing/sdc 等）声明设计输入路径，不依赖固定变量名。
- 只为被测工具生成 `tcl/<tool>/`（optimus 或 itools），PrimeTime 规则待定。
- 规范 `references/specs/tcl-script-rules.md` 升级为 v2.0，覆盖目录树结构、角色分发、多步 run、NITH 初始化块、DESIGN_INIT 激活、PV 入口、检查点、环境变量白名单和占位符禁用等约 16 条规则。
- `scripts/tcl_convention_validator.py` 完全重写为目录树检查器，按角色（suite/nith/struct/design/run/runner/script/checkpoint）分发规则并直接接受用例目录。
- `tests/unit/test_tcl_convention_validator.py` 完全重写，含 `build()` 辅助函数和 28 项正反样例；`SKILL.md` 工作流步骤 10–14、TCL 生成规则和交付物已同步目录树模型。
- F-015 目录树模型功能级验证通过并更新为 `passing`（28/28 测试 PASS）。
- 新增 F-020 命令说明结构化解析：`scripts/parse_command_spec.py` 接受 UTF-8 TXT 命令列表，支持一个文件中的多个命令块、中英文常见标题，以及 Tool/Version 上下文继承。
- F-020 输出版本化 JSON，确定性提取命令名、Syntax、option 必选性、参数数量与基本类型、枚举、可重复性、互斥/依赖/至少一个组合关系、版本 option 增删差异和来源行号。
- 无法从原文确定的字段保留为 `null`/`unknown` 并产生 `SPEC-GAP`；缺少命令名或关系引用未声明 option 时返回 error、非零退出且不写交付 JSON。
- 新增 `references/command-spec-format.md` 并将 TXT 解析步骤接入 `SKILL.md`；F-020 功能级验证 6/6 PASS。
- 明确命令 Syntax 括号语义：`[]` 中的 option 为可选，`{}` 中或无括号的 option 为必选；`{ -a | -b }` 结构化为 `exactly_one` 组合关系，F-020 扩展验证 7/7 PASS。
- 新增 `scripts/dump_tool_help.tcl`：在 Optimus 等 Tcl 工具会话中支持按 glob 枚举或显式列表选择命令，逐个执行 `<command> -help`，打印稳定边界标记，并在单命令失败后继续和输出汇总。
- F-021 使用普通 tclsh mock 工具命令完成无许可证确定性验证，3/3 PASS。
- 新增 `references/screen-qr-transfer.md`，记录隔离网络仅可读屏场景下的“压缩 + 分片 + 多帧二维码 + 外网自动采集”单向文本传输方案，包含分片协议、二维码参数、收发流程、完整性校验、恢复策略、安全边界，以及本次 Optimus 命令说明文件的字节数和 MD5 验收值。
- 实现 F-006 `delivery` 统一交付门禁：对同一份 Excel 和一个或多个 TCL 用例目录按 Layer 1 → Layer 2A → Layer 2B 顺序执行，并固定汇总为 L1、L2A、L2B 三项结果。
- Layer 1 未通过时 L2A/L2B 均为 `SKIPPED`；Layer 2A 失败或工具不可用时 L2B 为 `SKIPPED`；只有三层全部 `PASS` 时整体返回成功。
- 新增 6 项确定性门禁测试，覆盖全通过、三层独立失败、Nagelfar 不可用、上游跳过传播及多用例聚合；F-006 功能级验证通过并更新为 `passing`。
- 根据用户提供的 `write_def` 语法与参数截图，按 Optimus、Smoke case 策略完成 4 条用例设计：必选文件名最小调用、`-floorplan`、五个兼容 `-no_*` 开关合并调用及独立 `-help`。使用默认 Optimus 21.1 设计初始化假设生成 `generated/optimus/write_def_smoke/write_def_smoke.xlsx`，Layer 1 及 8 项需求追溯均 PASS；当前停在用例设计确认门禁，尚未生成 TCL。
- 将上述 `Optimus write_def + Smoke case` 输入固化为 `tests/regression/optimus/write_def_smoke/` 回归语料，包含脱敏命令说明、请求上下文、8 项需求契约和 4 条期望场景。新增两项确定性测试，分别锁定输入/覆盖映射，并从固定场景重建 Excel、执行 Layer 1；F-012 功能级验证 2/2 PASS 并更新为 `passing`。`request.json` 明确记录 TCL 尚未获批，回归用例不会绕过设计确认门禁生成脚本。
- 根据用户确认的 Optimus 双 run 成功案例，将检查点语料升级为 `1.2`、TCL 规范升级为 `2.1`：`pv_check_log` 支持 `-filter`/`-match`，`pv_check_golden` 接受 `golden/` 或 `./golden/`，同一 run 生成的实际文件必须按清理→生成→比较顺序执行，每个 `run_N.tcl` 必须以 `pv_rpt_checkpoints`→`exit` 收尾。
- F-015 新增 `TCL-CHECKPOINT-006`、`TCL-SCRIPT-005` 及相应正反样例，功能级验证 32/32 PASS，状态恢复为 `passing`。
- 根据用户确认，`design.tcl` 不是标准件：TCL 规范升级为 `2.2`，目录树不再强制该文件；存在时才验证其输入声明。run 可直接声明设计输入，但仍须在真实设计激活前加载 `mmmc.tcl`。新增无 `design.tcl` 正向样例，F-015 功能级验证更新为 33/33 PASS。
- 进一步确认 `assets/defaults/optimus/design.tcl` 是初始化结构模板，而不是复制件或通用设计缺省值。F-018 更名为“Optimus 设计初始化模板”：用户目标设计的 `.v`/netlist、`.lef` 和 top 缺失时确定性报告缺口；只有用户明确选择仓库示例 profile，才使用 SMIC28/riscv 示例路径。解析器与 6 项测试已同步，F-018 功能级验证 PASS。
- 修复 F-015 的 NITH 工作目录路径契约：`run_N.tcl` 虽位于 `tcl/<tool>/`，实际执行工作目录是与 `nith.run` 同级的用例统计目录，因此可选设计配置必须引用 `./tcl/design.tcl`，MMMC 必须引用 `./tcl/<tool>/mmmc.tcl`；工具选项中的相对文件路径遵循同一基准。
- TCL 规范升级为 `2.3`，Layer 2B 新增旧路径反例：`../design.tcl` 和 `./mmmc.tcl` 均由 `TCL-RUNNER-002` 确定性拒绝；正确用例根路径通过。Optimus 模板默认 `mmmc_path` 同步改为 `./tcl/optimus/mmmc.tcl`。
- 调整 F-018 Optimus 版本契约：目标版本改为可选元数据，不再是测试设计、Excel 或 TCL 生成的必要条件。未提供版本时继续生成版本无关覆盖；仅在具体测试点确实依赖版本且现有命令资料无法确定时记录局部缺口，不阻断其他用例。
- `21.1` 仍可作为 Optimus 初始化模板的元数据默认值，但不得视为用户已确认版本或据此推导版本专属语法；新增缺省版本正向契约测试，F-018 验证为 7/7 PASS。
- 修正 Optimus 示例路径拼写：`Itools21.1_lfp_util0.65` 改为 `Itools21.1_Ifp_util0.65`，解析器示例 profile、`design.tcl` 模板及测试同步更新。
- Optimus 初始化职责收敛到每个 `run_N.tcl` 的 `DESIGN_INIT`：source PV、可选 source `./tcl/design.tcl`、设置 design/tech 相关 setup options、以 `setup.mmmc_file` 指定 MMMC、执行 `setup_design`，再通过 `read_def` 读入 DEF。
- Optimus `mmmc.tcl` 不再被 source；`design.tcl` 与 `mmmc.tcl` 不得重复执行 PV source、`set_options`、`setup_design` 或 `read_def`。TCL 规范升级至 `2.4`，新增缺少 MMMC option、source MMMC、DEF 顺序错误和 helper 重复初始化的确定性失败样例；F-015 验证为 35/35 PASS。
- 将 `tcl/design.tcl` 恢复为每个用例必须包含的标准件，TCL 规范升级至 `2.5`；缺少该文件由 `TCL-STRUCT-001` 确定性拒绝，Optimus 与 iTools / Innovus 的 run 初始化段都必须从用例统计目录 source `./tcl/design.tcl`。
- 新增 `TCL-DESIGN-002`：当 `design.tcl` 已声明 LEF、Verilog/netlist、top、power/ground net 或 DEF 输入变量时，`run_N.tcl` 必须在对应 `set_options`/`read_def` 中直接复用，禁止同名重复 `set` 或改用字面值；新增正反样例后 F-015 验证为 37/37 PASS。
- 新增 F-022 设计路径集中管理：`assets/design-profiles.json` 成为设计目录、技术目录、LEF、netlist、DEF、top、power/ground net 的唯一可编辑配置源，`scripts/design_config.py` 可从指定 profile 一次同步一个或多个用例的 `tcl/design.tcl`。
- 新增 `assets/输入件管理表.xlsx`，由同一 JSON 确定性生成，包含编号、Profile、输入类别、字段、路径/值、必选性、状态、冲突检查、来源和备注；该表是审查视图，不作为第二配置源。
- 配置器拒绝 schema/profile 错误、缺失字段、未知字段、空值、用户目录绝对路径、非 `design.tcl` 输出和重复输出目标；生成文件保留 central profile 来源标记且运行时不依赖仓库配置。
- TCL 规范升级至 `2.6`，新增 `TCL-DESIGN-003`，没有集中 profile 来源标记的 `design.tcl` 由 Layer 2B 确定性拒绝。
- Optimus 示例默认解析器已改为读取集中 profile，消除旧代码与模板间 LEF 文件名 `sec/sc` 和 `scc/scc` 的冲突；DEF 也纳入必选设计输入。
- F-022 功能级验证 6/6 PASS；F-015 38/38 PASS；F-018 7/7 PASS，状态均为 `passing`。

### 验证记录

2026-10-20 上传前完整门禁结果：

- `./init.sh test all`：FAIL（169/172 PASS）。
- 失败项：`test_skill_requires_user_selected_design_and_tech_inputs`、`test_skill_requires_maximum_compatible_coverage_per_case`、`test_every_rule_has_live_evidence`（USR-017）。
- 失败原因均为 `skill/SKILL.md` 缺少已登记的显式契约文本；按上传流程立即停止，未创建提交、未推送候选分支、未触发 Jenkins。
- 按用户要求，随后删除“Optimus 目标版本为可选信息”契约及其 F-018 验收项、USR-017 规则登记和自动化门禁；不再要求 `SKILL.md` 声明该规则。
- 删除该门禁后完整测试为 170/171 PASS；剩余失败是既有“最大化兼容覆盖”规则缺少反向明确文本，已在 `skill/SKILL.md` 补充“Do not create one case per option”，等待完整门禁复验。
- 补齐文本后重新执行 `./init.sh test all`：171/171 PASS，隔离 Skill 包结构 PASS，允许继续候选分支上传流程。

2026-10-14 本次 Excel 双检查门禁描述验证：

- F-028 workflow 路由：PASS（5/5）。
- F-013 测试计划检查：PASS（16/16）。
- F-002 设计确认门禁：PASS（4/4）。
- 项目验证和 Codex Skill 结构检查：PASS；`git diff --check`：PASS。

2026-10-14 本次测试计划语义规范收敛结果：

- F-013 功能级验证：PASS（16/16）。
- `test-plan-rules.md` 仅包含 Agent 语义规则；脚本职责已迁移至 `test_plan_validator.py` 模块注释。
- 项目验证：PASS。
- Codex Skill 结构检查：PASS；`git diff --check`：PASS。

2026-10-14 本次测试计划检查职责分类结果：

- F-013 功能级验证：PASS（16/16）。
- 项目验证：PASS。
- Codex Skill 结构检查：PASS；`git diff --check`：PASS。
- 分类仅定义脚本与 Agent 的目标职责；此前识别的 PLAN-007、PLAN-015 及语义预筛实现缺口仍需后续按测试先行规则补齐。

2026-10-14 本次双场景 workflow 路由检查结果：

- F-028 功能级验证：PASS（3/3）。
- F-002 确认门禁回归：PASS（4/4）；F-027 工具契约回归：PASS（3/3）。
- 项目验证：PASS。
- Codex Skill 结构检查：PASS；`git diff --check`：PASS。

2026-10-14 本次 Skill workflow 工具契约检查结果：

- F-027 功能级验证：PASS（3/3）。
- 项目验证：PASS。
- Codex Skill 结构检查：PASS；`git diff --check`：PASS。
- 本次只完成工具调用与结果契约；EDA 命令静态语法引擎和独立覆盖率计算器仍需后续按测试先行规则分别实现。

2026-10-14 本次两层标准调整检查结果：

- F-023 功能级验证：PASS（4/4）。
- Python 单元测试：140/140 PASS。
- 项目验证：PASS；两个旧基础 fixture 已按既有 `case.toml` 契约恢复。
- Codex Skill 结构检查：PASS；`git diff --check`：PASS。
- Skill 产物隔离：F-016 15/15 PASS；F-023 4/4 PASS。
- 目录物理隔离：F-024 17/17 PASS；Skill 结构检查直接对 `skill/` 执行并通过。
- Jenkins 完整门禁：F-025 6/6 PASS；本机完整门禁四项全部 PASS，Python 140/140 PASS。
- Jenkins 容器端到端启动验证：镜像构建 PASS，登录页 HTTP 200，管理员认证 PASS，`eda-tester-skill-approved-merge` 任务已创建且 `buildable=true`。
- 移除第三方 TCL 静态语法工具后的完整回归：项目验证 PASS，Python 136/136 PASS，Skill 结构 PASS，`git diff --check` PASS。
- 本项目 Jenkins 使用宿主机 `8081`/`50001`，避免与已有 Jenkins 的 `8080`/`50000` 冲突；端口可通过本地 `.env` 覆盖。管理员密码和 GitHub token 均已从 Git 跟踪文件隔离，本次未触发构建、审批或代码合入。

2026-09-09 GitHub 推送前复核：

- 当前分支与上游基线无领先/落后；待提交内容为规则去重、确定性验证器、对应正反测试、Skill 渐进披露文档和无图片 Excel 模板。
- Python 单元测试 124/127 PASS；3 项失败仍仅由已记录的两个旧基础 fixture 缺失引起。
- 项目验证仅报告同一组 6 条缺失 fixture 路径；Codex Skill 结构检查 PASS，`git diff --check` PASS。
- 两处 `.DS_Store` 本地元数据变化不纳入提交。

2026-08-23 本次文档设计检查结果：

- EDA 用例生成知识库设计文档已生成，章节和内容非空检查通过，`git diff --check` 通过。
- Codex Skill 结构检查：PASS。
- 项目验证仍因 2 个已知旧基础 fixture 缺失而失败，共影响 F-003/F-004/F-005 的 6 条路径登记；与本次文档设计无关，未修改或伪造这些 fixture。

2026-08-14 本次检查结果：

- F-022 设计路径集中管理：PASS（6/6）。
- F-015 TCL Layer 2B：PASS（38/38，含 `TCL-DESIGN-003` 正反检查）。
- F-018 Optimus 默认解析：PASS（7/7）。
- Python 单元测试：118/121 PASS；仅 3 项已知旧 fixture 缺失失败，与会话开始基线一致。
- `assets/输入件管理表.xlsx` 可重新打开，包含 2 个工作表和 8 条 repository_example 输入记录，无公式及 Excel 错误字符串。

2026-08-12 本次检查结果：

- F-015 标准 design.tcl 与输入变量复用规则：PASS（37/37）。
- Codex Skill 结构检查：PASS；完整 Python 单元测试除 3 项已知旧 fixture 缺失失败外，其余 111/114 PASS。
- F-015 功能级验证：PASS（34/34，含用例统计目录路径正反检查）。
- Codex Skill 结构检查：PASS。
- Git 待发布快照 Python 单元测试：110/110 PASS。
- Git 待发布快照项目结构和功能清单验证：PASS；基础 fixture 的本地删除未纳入发布范围。

2026-08-11 最近一次检查结果：

- 项目结构和功能清单验证：PASS。
- Python 单元测试：103/103 PASS。
- Codex Skill 结构检查：PASS。
- F-013 功能级验证：PASS。
- F-004 功能级验证：PASS。
- F-014 功能级验证：PASS。
- Nagelfar 真实安装端到端验证：PASS（版本 1.3.5）。
- F-016 多 Agent Skill 安装器功能级验证：PASS（14/14，含开发文件排除）。
- F-015 目录树 TCL Layer 2B 功能级验证：PASS（28/28，目录树模型）。
- F-017 非空测试计划生成功能级验证：PASS。
- F-002 测试场景分解功能级验证：PASS。
- TCL-SCRIPT-003 环境变量白名单正反用例：PASS。
- TCL-SCRIPT-004 多工具初始化正反用例：PASS。
- F-002 用例设计确认门禁契约测试：PASS。
- F-018 Optimus 设计初始化模板功能级验证：PASS（6/6）。
- F-019 iTools 默认 MMMC 功能级验证：PASS。
- F-020 命令说明结构化解析功能级验证：PASS（6/6）。
- F-020 括号语义扩展验证：PASS（7/7）。
- F-021 工具命令 Help 批量采集功能级验证：PASS（3/3）。
- F-006 统一交付门禁功能级验证：PASS（6/6）。
- `write_def` Smoke Excel 测试计划：Layer 1 PASS（4 条非空用例，8 项命令需求全部可追溯）。
- F-012 回归语料库功能级验证：PASS（2/2，固定 `write_def` 输入、覆盖契约及 Excel Layer 1 重建）。

复现命令：

```sh
./init.sh test project
python3 -m unittest discover -s harness/tests/unit -v
python3 "$CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py" skill
```

## 已知缺口

- 两层顶层标准和测试集契约已经定稿，但 Layer 2 测试集结构校验器及端到端运行器尚未实现；现有 `delivery` 命令只负责 Layer 2 内部的 Excel 和 TCL 静态输出门禁。
- 尚未建立首批 `tests/e2e/<case_id>/` 输入与预期输出测试集；需要由用户提供或确认代表性输入和预期交付。

- 用户提供的 Optimus 实机成功语料包含父目录入口 `tests/cases/nith.run`，该入口按序调度 `run_1.tcl`、`run_2.tcl` 并调用 `nith_done()`；案例子目录含两个 run 和 MMMC。当前入口未放在 `pos001_demo_optimus/` 内，且 run 仍依赖目录外 `tcl/case_setup.tcl` 与 golden 文件，因此尚未按当前“每个用例目录自包含 nith.run”契约登记为独立 Layer 2B 通过 fixture。
- 模板自带历史数据不满足新规范；模板作为复制源保留，生成结果必须清除历史业务行后再填充，不能直接把模板本身视为合格测试计划。
- F-001 的 Innovus 语料库查询规则已配置，但尚未实现稳定的程序化查询适配器、响应结构校验和自动化验收样例；站点当前可能返回 `Internal Server Error`。
- F-010 的 Optimus 脱敏语料已配置，但尚未建立流程阶段、MMMC 引用完整性、corner 语义和 PV 入口配置的自动化验收样例。
- Optimus `check_design_data` Smoke TCL 已按 F-018 默认设计配置重建并通过 Layer 2A + Layer 2B；但实际 EDA 执行（PV_ROOT 提供的 SMIC28 设计数据、报告内容语义与 netlist 范围差异）仍属实机验证范畴，静态检查仅断言报告文件生成与非空。
- 现有 `generated/` 中的 `check_design_data` Smoke 独立 TCL（`pos001_file.tcl`、`pos002_file_netlist.tcl`）仍为旧独立文件模型产物，不满足新的目录树 Layer 2B；需按目录树模型重建为 `nith.run` + `tcl/optimus/{run_1.tcl, mmmc.tcl}` + `tcl/design.tcl`。
- Layer 2A 语法数据库当前仅覆盖 Innovus/iTools；Optimus 顶层命令（`setup_design`、`set_options`）在共享 innovus database 下仅产生 W 而非 E，后续可能需要 Optimus 专用 syntax database。
- `write_def` 截图未给出目标版本、稳定 DEF section/golden 规则，以及 `-help` 是否豁免必选 `<file_name>`；当前按 Optimus 默认 21.1 和常见帮助调用语义记录为待实机确认假设。

## 下一步

1. 按测试先行规则实现 EDA 工具脚本静态检查器，依次覆盖 Tcl 基础语法、EDA 工具命令及选项使用和 TCL 编程规范；先确认各目标工具的版本化语法来源。
2. 静态检查器通过后，再单独实现覆盖率检查器，输出场景覆盖率、被测选项覆盖率和未覆盖项。
3. 按测试先行规则登记并新增“仅显式用户调用”契约测试，锁定 `policy.allow_implicit_invocation: false`。
4. 按测试先行规则新增 Layer 1 自动环境/工具/启动检查功能点。
5. 建立 Layer 2 测试集 schema 校验器与端到端运行器；先由用户确认首批输入及预期输出测试集。

## 每次会话开始时

1. 阅读 `harness/PROCESS.MD` 和 `harness/function.json`，确认当前活动功能与下一步。
2. 阅读 `skill/SKILL.md`、`AGENTS.md` 及当前功能涉及的规范文件。
3. 运行 `./init.sh test project`，确认仓库处于一致状态。
4. 从本文件“下一步”的第一项未完成工作继续。

## 每次会话结束前

1. 更新本文件的当前状态、已完成工作、验证基线、已知缺口和下一步。
2. 运行项目验证、相关功能验证和单元测试。
3. 确认 `function.json` 的状态、测试路径和验证命令与实际实现一致。
4. 汇报已完成内容和未解决问题；只有用户明确要求时才提交版本控制变更。
5. 用户要求提交或推送时，只操作当前 `eda-tester-skill/` 的 GitHub 仓库，不操作父目录中的其他仓库。
