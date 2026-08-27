# TCL 用例脚本规范

版本：`2.6`

状态：`CONFIGURED`

本文件是 Layer 2B 的唯一业务规则入口。交付物是**用例名子目录**：每个用例产出一个以用例名命名的目录，目录内包含 `nith.run` 调度器和 `tcl/` 脚本树。不再交付独立单 `.tcl` 文件。

## 交付结构

```text
<posNNN_用例名>/            # 或 negNNN_，目录名即用例名
├── nith.run                # Python 调度器，逐字保留 NITH 固定初始化块
└── tcl/
    ├── design.tcl          # 标准件；声明 run 使用的设计输入变量
    └── <tool>/             # optimus 或 itools，按被测工具生成，只存在一个
        ├── run_1.tcl       # 可多步：run_1.tcl … run_N.tcl，从 1 连续编号
        └── mmmc.tcl        # 该工具方言的 MMMC 定义
```

多步用例：`run_1.tcl` 可输出中间产物（如 db），`run_2.tcl` 读取该产物继续执行；`run_<N>.tcl` 从 1 起连续编号，不得跳号。

## 规则

### TCL-SUITE-001：输入有效

- 校验对象必须是存在的非符号链接目录。
- 反例：指向 `.tcl` 文件、符号链接、不存在的路径。

### TCL-SUITE-002：目录命名

- 目录名匹配 `^(pos|neg)[0-9]{3}_[a-z0-9][a-z0-9_]*$`。
- 正例：`pos001_file`；反例：`case1`。

### TCL-STRUCT-001：目录树契约

- 目录下必须存在：`nith.run`（普通文件）、`tcl/`（目录）、恰好一个 `tcl/<tool>/`（目录）。
- `tcl/<tool>/` 内必须存在：`run_1.tcl`，并可包含 `run_2.tcl … run_N.tcl`（从 1 连续，不跳号），以及 `mmmc.tcl`。
- `tcl/design.tcl` 是每个用例必须包含的标准件；不存在时失败。
- 正例：包含 `design.tcl`、连续 run 和 `mmmc.tcl` 的上述完整树；反例：缺 `design.tcl`、`run_1.tcl` 跳到 `run_2.tcl`、缺 `mmmc.tcl`。

### TCL-STRUCT-002：按被测工具生成

- `<tool>` 只能是 `optimus` 或 `itools` 之一；目录下只允许存在一个工具子目录，不混用方言。
- 反例：同时存在 `tcl/optimus/` 与 `tcl/itools/`；`<tool>` 为 `primetime` 或其他未登记名称。

### TCL-NITH-001：nith.run 契约

- `nith.run` 是 Python 脚本，逐字保留从 `### NITH initialization, please do not change this section` 到 `### NITH initialization end` 的固定块（含 shebang）。
- 固定块之后的 case-setup 段必须按序为每个 `run_<N>.tcl` 写 `nith.input[""] = f"tcl/{nith.PV_TOOL}/run_<N>.tcl"` 并调用 `nith_run()`，最后调用一次 `nith_done()`。
- 引用的 `run_<N>` 必须与 `tcl/<tool>/` 内实际存在且连续编号的文件一一对应。
- 正例：单步 `nith.input[""] = f"tcl/{nith.PV_TOOL}/run_1.tcl"; nith_run(); nith_done()`；多步依次追加 `run_2.tcl` 块。

### TCL-RUNNER-001：路径可移植

- `design.tcl`、`mmmc.tcl`、所有 `run_<N>.tcl` 以及 `nith.run` 的 case-setup 段不得出现用户目录、`/home/`、`/Users/` 或机器专属绝对路径。
- `nith.run` 的固定 NITH 初始化块整体豁免（模板要求逐字保留）。
- 正例：`$env(PV_ROOT)/...` 或相对路径；反例：`source /Users/name/setup.tcl`（位于非豁免段时）。

### TCL-RUNNER-002：树内组织

- NITH 启动 `run_<N>.tcl` 时，工具工作目录是与 `nith.run` 同级的用例统计目录，不是 `run_<N>.tcl` 所在目录。所有相对路径均以该用例目录为基准。
- `run_<N>.tcl` 的 setup 只能来自本树。Optimus 在 `DESIGN_INIT` 段内 source `./tcl/design.tcl`，但不得 source `mmmc.tcl`；MMMC 只能通过 `set_options setup.mmmc_file ./tcl/optimus/mmmc.tcl` 设置。
- 禁止 `source` 树外的 `case_setup.tcl`、绝对路径 setup 或其他外部 setup 脚本。
- 正例：`source ./tcl/design.tcl`、`set_options setup.mmmc_file ./tcl/optimus/mmmc.tcl`；反例：`source ../design.tcl`、`source ./tcl/optimus/mmmc.tcl`、`source ./mmmc.tcl`、`source ./tcl/case_setup.tcl`、`source /abs/setup.tcl`。

### TCL-DESIGN-001：标准 design.tcl 声明输入

- `tcl/design.tcl` 是标准件，必须声明有意义的设计输入变量。
- 存在时必须用 `set` 声明至少一种设计输入类别：top（`init_top`/`init_top_name`/`init_top_cell` 等）、网表（`verilog`/`netlist`）、`lef`、库或约束（`lib`/`timing`/`sdc`）。
- 路径用 `$env(PV_ROOT)` 锚定或相对表达；检测按类别关键字，兼容不同变量命名。
- 正例：`set init_top_name riscv_core`、`set lef_files ./design/a.lef`；反例：design.tcl 为空或只含注释。

### TCL-DESIGN-002：run 复用 design.tcl 输入变量

- `run_<N>.tcl` 必须 source `./tcl/design.tcl`。
- 当 `design.tcl` 已声明 LEF、Verilog/netlist、top、power net、ground net 或 DEF 输入变量时，run 中对应的 `set_options` 或 `read_def` 必须直接引用该变量。
- run 不得再次 `set` 同名变量，也不得以字面路径或字面名称绕过已存在的变量。
- 正例：`set_options setup.lef_file $lef_files`、`read_def $def`；反例：run 中再次 `set lef_files ...`、`set_options setup.lef_file ./design/a.lef`、`read_def ./design/a.def`。

### TCL-DESIGN-003：设计路径集中管理

- `assets/design-profiles.json` 是设计路径和值的唯一配置源；`assets/输入件管理表.xlsx` 是由它生成的审查视图，不作为第二配置源。
- 每个 `design.tcl` 必须由 `scripts/design_config.py` 同步生成，并包含 `# Generated from central design profile: <profile>` 来源标记。
- 修改路径时只修改 JSON profile，再批量同步目标用例；禁止直接手改各用例中的路径。
- 配置器拒绝缺失字段、未知字段、机器专属绝对路径和同一批次重复输出目标。

### TCL-RUN-001：run 脚本加载顺序

- Optimus `run_<N>.tcl` 的 `DESIGN_INIT` 段依次完成：source PV、source `./tcl/design.tcl`、以其中变量设置 design/tech 相关 `setup.*` option、设置 `setup.mmmc_file`、执行 `setup_design`、最后以 `read_def` 读入 DEF。
- Optimus 禁止 source `mmmc.tcl`，禁止用 `set_options` 设置 DEF，禁止在 `setup_design` 之前执行 `read_def`。
- `design.tcl` 和 `mmmc.tcl` 不得重复 source PV、执行 `set_options`、`setup_design` 或 `read_def`；这些初始化动作只属于 run init 块。

### TCL-CHECKPOINT-001：包含检查点

- 整个用例树内至少实际调用一次 `pv_check_log`、`pv_check_golden` 或 `pv_check_qor`；注释和字符串中的文字不计。
- 正例：某 `run_<N>.tcl` 内 `pv_check_log {report_qor}`；反例：全树只有被测命令或仅在注释中提到检查点。

### TCL-CHECKPOINT-002：先加载 PV 入口

- 每个 `run_<N>.tcl` 内，首次 `pv_check_*` 调用之前必须 `source $env(PV_ROOT)/scripts/pv.tcl` 或 `$env(PV_ROOT)/pv/scripts/pv.tcl`。
- 不得引入 `PV_ENTRY` 等别名；按目标工具或参考资料选择已知布局。

### TCL-CHECKPOINT-003：`pv_check_log` 调用有效

- 第一个参数必须是非空命令块；禁止手工输出 `===PV_MARKER`。
- 允许 `-name`、`-filter`、`-match`、`-log_files`；出现时必须带非空值，且同名 option 不得重复。
- `-filter` 排除匹配的屏幕输出行；`-match` 存在时，只比较匹配该表达式的行。两者可以同时使用。

### TCL-CHECKPOINT-004：`pv_check_golden` 调用有效

- 必须提供一个非空输出文件；只允许 `-golden`、`-filter`。
- `-golden` 必须使用 `golden/` 或 `./golden/` 下的相对路径；禁止在脚本中设置 `env(PV_CHECK_MODE)`。

### TCL-CHECKPOINT-005：`pv_check_qor` 调用有效

- 第一个参数必须是 `report_timing`、`report_qor` 或 `timeDesign` 的非空命令块。
- 只允许 `-name`、`-golden`、`-tolerance`、`-rel_tolerance`、`-dir`；容差必须是有限非负数。
- `-golden` 使用 `./golden/`，`-dir` 使用相对输出路径且不得包含 `..`。

### TCL-CHECKPOINT-006：golden 产物顺序与旧文件隔离

- 当某个 `pv_check_golden` 的实际文件由同一个 `run_N.tcl` 中的 `write_*` 命令生成时，必须按“`file delete -force <actual>` → `write_* <actual>` → `pv_check_golden <actual>`”顺序执行。
- 禁止先比较后生成，也禁止在未清理同名旧文件的情况下生成并比较；这样可以避免工作目录残留导致误通过。
- 如果实际文件由明确的前序 run 生成，当前 run 没有同名 `write_*`，本规则不推断跨 run 数据流，由用例设计和实机运行验证负责。

### TCL-SCRIPT-001：测试动作与期望标记

- 每个 `run_<N>.tcl` 恰好包含一个 `# TEST_ACTION`，其前恰好包含一个 `# EXPECT: PASS` 或 `# EXPECT: FAIL`。
- `pos` 用例使用 PASS，`neg` 用例使用 FAIL。

### TCL-SCRIPT-002：禁止未完成占位符

- 用例树内所有文件（含 `nith.run`、`design.tcl`、`mmmc.tcl`、`run_<N>.tcl`）的代码及注释不得包含独立词 `TODO` 或 `TBD`。

### TCL-SCRIPT-003：系统环境变量白名单

- 树内所有 `.tcl` 只能读取、检查或设置 `env(PV_ROOT)` 和 `env(PV_TOOL)`；`$::env(...)`、`::env(...)` 等价写法同样受此限制，动态 `env($name)` 也禁止。
- 禁止 `PV_ENTRY`、`HOME` 及任何其他系统环境变量；设计 setup 缺失时记录缺口，不得用新环境变量代替。

### TCL-SCRIPT-004：完整 EDA 设计初始化

- 每个 `run_<N>.tcl` 必须可直接读入目标 EDA 工具，不假定调用者已预先读入设计。
- 恰好使用一组 `# DESIGN_INIT_BEGIN`、`# DESIGN_INIT_END` 标记初始化段，初始化段必须在 `# TEST_ACTION` 之前完成。
- 初始化段必须加载标准件 `./tcl/design.tcl` 并复用其中的输入变量，不得在 run 中重复声明对应输入。Optimus 必须通过 `setup.mmmc_file` 指定 MMMC，执行 `setup_design` 后再 `read_def`；iTools / Innovus 必须在 `init_design` 前设置 `init_mmmc_file ./tcl/itools/mmmc.tcl`，由 `init_design` 加载 MMMC，禁止直接 `source` iTools MMMC 文件。iTools / Innovus 仍使用其工具适配的 `init_design`/`read_db`/`restoreDesign` 流程。仅变量赋值、注释或 PV 加载不算完成初始化。
- 多步用例中后续步读取前一步产物时，`read_db`/`restoreDesign` 即可作为该步激活命令。
- 如果缺少完成初始化所需的信息，停止生成 TCL 并向用户列出缺口；不得交付只能在预加载设计会话中运行的半成品。

### TCL-SCRIPT-005：每个 run 汇总检查点并退出

- 每个 `run_N.tcl` 的最后两个有效命令必须依次为 `pv_rpt_checkpoints` 和 `exit`。
- `pv_rpt_checkpoints` 汇总该 run 内所有 checkpoint 信息；`exit` 明确结束本次工具执行。
- 文件末尾可以有空行或注释，但不得在 `exit` 后继续执行其他命令。

## 执行顺序

Layer 2A（Nagelfar 1.3.5 静态语法）对树内所有 `.tcl` 文件通过后，才执行 Layer 2B 对整棵用例树的规范检查。任一 `.tcl` 的 2A 失败或工具不可用时，2B 返回 `SKIPPED`，不得用规范检查掩盖语法问题。
