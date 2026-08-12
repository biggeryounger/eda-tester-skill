# EDA Tester Skill 项目进度

最后更新：2026-08-12

项目仓库：<https://github.com/biggeryounger/eda-tester-skill>

仓库状态：2026-08-07 完成首次 GitHub 推送；后续只跟踪该 GitHub 仓库，不再使用或同步 Gitee。

## 当前目标

完成一个面向 EDA 命令的 Codex Skill：从命令说明或自然语言需求生成测试场景、Excel 测试计划和 TCL 用例，并通过确定性程序完成验证。当前优先支持 Cadence Innovus。

## 当前状态

- 当前活动功能：无。
- 已通过功能：F-002、F-004、F-005、F-006、F-012、F-013、F-014、F-015、F-016、F-017、F-018、F-019、F-020、F-021。
- F-014 已使用真实 Nagelfar 1.3.5 完成有效/无效 Innovus TCL 端到端复核，状态为 `passing`。
- F-015 TCL 脚本规范检查器已升级为目录树模型（`nith.run` + `tcl/design.tcl` + `tcl/<tool>/{run_1.tcl…run_N.tcl, mmmc.tcl}`），状态为 `passing`。
- F-020 TXT 命令说明结构化解析器已实现并通过功能级验证，状态为 `passing`。
- F-021 工具命令 Help 批量采集脚本已实现并通过功能级验证，状态为 `passing`。
- 其余功能保持 `not_started`。

功能状态的唯一正式来源是 `function.json`；本文件只记录会话交接信息，不替代功能清单。

## 已完成工作

- 建立 Skill 基础结构、界面元数据、模板、规范和测试目录。
- 建立 `function.json` 功能清单和单一活动功能门禁。
- 建立正负用例目录、`case.toml` 元数据和基础 TCL 契约检查。
- 接入 Nagelfar 1.3.5，并建立 Innovus/iTools syntax database。
- 建立统一验证入口：
  - `python3 scripts/validate.py project`
  - `python3 scripts/validate.py tcl <case_dir>`
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
- `validate.py tcl` 现在按 Layer 2A → Layer 2B 执行；语法失败或工具不可用时 2B 返回 `SKIPPED`。
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
- `scripts/tcl_convention_validator.py` 完全重写为目录树检查器，按角色（suite/nith/struct/design/run/runner/script/checkpoint）分发规则；`scripts/validate.py` 的 `tcl` 子命令接受用例目录，先对树内所有 `.tcl` 文件执行 Layer 2A，全通过后对目录执行 Layer 2B。
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

## 当前验证基线

2026-08-12 本次检查结果：

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
python3 scripts/validate.py project
python3 -m unittest discover -s tests/unit -v
python3 /Users/e2uninova-m4/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
```

## 已知缺口

- `function.json` 登记的两个旧基础用例目录当前不存在，导致项目验证及 3 项项目一致性单元测试失败；不能用不符合旧 `case.toml` 契约的 `pos001_demo_optimus` 直接替代，需决定恢复旧 fixture 还是迁移 F-003/F-004/F-005 的测试契约。
- 用户提供的 Optimus 实机成功语料包含父目录入口 `tests/cases/nith.run`，该入口按序调度 `run_1.tcl`、`run_2.tcl` 并调用 `nith_done()`；案例子目录含两个 run 和 MMMC。当前入口未放在 `pos001_demo_optimus/` 内，且 run 仍依赖目录外 `tcl/case_setup.tcl` 与 golden 文件，因此尚未按当前“每个用例目录自包含 nith.run”契约登记为独立 Layer 2B 通过 fixture。
- 模板自带历史数据不满足新规范；模板作为复制源保留，生成结果必须清除历史业务行后再填充，不能直接把模板本身视为合格测试计划。
- F-001 的 Innovus 语料库查询规则已配置，但尚未实现稳定的程序化查询适配器、响应结构校验和自动化验收样例；站点当前可能返回 `Internal Server Error`。
- F-010 的 Optimus 脱敏语料已配置，但尚未建立流程阶段、MMMC 引用完整性、corner 语义和 PV 入口配置的自动化验收样例。
- Nagelfar 安装在用户级目录，不随仓库分发；其他环境仍需独立安装 1.3.5，或通过 `NAGELFAR` 指向 `nagelfar.tcl`。
- Optimus `check_design_data` Smoke TCL 已按 F-018 默认设计配置重建并通过 Layer 2A + Layer 2B；但实际 EDA 执行（PV_ROOT 提供的 SMIC28 设计数据、报告内容语义与 netlist 范围差异）仍属实机验证范畴，静态检查仅断言报告文件生成与非空。
- 现有 `generated/` 中的 `check_design_data` Smoke 独立 TCL（`pos001_file.tcl`、`pos002_file_netlist.tcl`）仍为旧独立文件模型产物，不满足新的目录树 Layer 2B；需按目录树模型重建为 `nith.run` + `tcl/optimus/{run_1.tcl, mmmc.tcl}` + `tcl/design.tcl`。
- Layer 2A 语法数据库当前仅覆盖 Innovus/iTools；Optimus 顶层命令（`setup_design`、`set_options`）在共享 innovus database 下仅产生 W 而非 E，后续可能需要 Optimus 专用 syntax database。
- `write_def` 截图未给出目标版本、稳定 DEF section/golden 规则，以及 `-help` 是否豁免必选 `<file_name>`；当前按 Optimus 默认 21.1 和常见帮助调用语义记录为待实机确认假设。

## 下一步

1. 恢复旧基础 fixture，或迁移 F-003/F-004/F-005 的测试登记，重新恢复项目级门禁。
2. 等待用户确认 `write_def` Smoke 用例设计；确认后生成 4 个目录树 TCL 用例并运行 F-006 统一交付门禁。
3. 为 F-002 建立策略交互、覆盖矩阵及多策略去重的自动化验收样例。
4. 为 F-001 实现稳定的 Innovus 语料库查询适配器和响应结构校验。
5. 按新目录树模型重建 `generated/` 中的 `check_design_data` Smoke 交付物，并使用 F-006 统一门禁验收。

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
