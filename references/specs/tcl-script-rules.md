# TCL 用例脚本规范

版本：`2.3`

状态：`CONFIGURED`

本文件是 Layer 2B 的唯一业务规则入口。交付物是**用例名子目录**：每个用例产出一个以用例名命名的目录，目录内包含 `nith.run` 调度器和 `tcl/` 脚本树。不再交付独立单 `.tcl` 文件。

## 交付结构

```text
<posNNN_用例名>/            # 或 negNNN_，目录名即用例名
├── nith.run                # Python 调度器，逐字保留 NITH 固定初始化块
└── tcl/
    ├── design.tcl          # 可选；不是标准件，存在时声明设计输入
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
- `tcl/design.tcl` 是可选辅助文件，不是标准件；不存在时不构成失败。
- 正例：不含 `design.tcl` 的上述完整树；反例：`run_1.tcl` 跳到 `run_2.tcl`、缺 `mmmc.tcl`。

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
- `run_<N>.tcl` 的 setup 只能来自本树：在 `DESIGN_INIT` 段内使用 `source ./tcl/design.tcl` 与 `source ./tcl/<tool>/mmmc.tcl`；工具选项中的文件引用也遵循同一基准，例如 Optimus `set_options setup.mmmc_file ./tcl/optimus/mmmc.tcl`。
- 禁止 `source` 树外的 `case_setup.tcl`、绝对路径 setup 或其他外部 setup 脚本。
- 正例：`source ./tcl/design.tcl`、`source ./tcl/optimus/mmmc.tcl`；反例：`source ../design.tcl`、`source ./mmmc.tcl`、`source ./tcl/case_setup.tcl`、`source /abs/setup.tcl`。

### TCL-DESIGN-001：可选 design.tcl 声明输入

- `tcl/design.tcl` 不是标准件，可以省略；仅当该文件存在时执行本规则。
- 存在时必须用 `set` 声明至少一种设计输入类别：top（`init_top`/`init_top_name`/`init_top_cell` 等）、网表（`verilog`/`netlist`）、`lef`、库或约束（`lib`/`timing`/`sdc`）。
- 路径用 `$env(PV_ROOT)` 锚定或相对表达；检测按类别关键字，兼容不同变量命名。
- 正例：`set init_top_name riscv_core`、`set lef_files ./design/a.lef`；反例：design.tcl 为空或只含注释。

### TCL-RUN-001：run 脚本加载顺序

- 每个 `run_<N>.tcl` 的 `DESIGN_INIT` 段内必须先 `source ./tcl/<tool>/mmmc.tcl`，随后才调用工具激活命令。
- 如果用例选择使用可选 `./tcl/design.tcl`，必须在 MMMC 之前加载；也可以直接在初始化段声明设计输入，不使用 `design.tcl`。
- 正例：直接设置输入后 source mmmc 再 `setup_design`；反例：未加载 mmmc、或激活之后才 source mmmc。

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
- 初始化段可以直接声明设计输入，也可以选择加载可选的 `./tcl/design.tcl`；必须加载 `source ./tcl/<tool>/mmmc.tcl`，并随后调用目标工具实际的设计激活命令：Optimus `setup_design`，iTools / Innovus `init_design`/`read_db`/`restoreDesign`，PrimeTime `open_block`/`link_design`。仅变量赋值、注释或 PV 加载不算完成初始化。
- 多步用例中后续步读取前一步产物时，`read_db`/`restoreDesign` 即可作为该步激活命令。
- 如果缺少完成初始化所需的信息，停止生成 TCL 并向用户列出缺口；不得交付只能在预加载设计会话中运行的半成品。

### TCL-SCRIPT-005：每个 run 汇总检查点并退出

- 每个 `run_N.tcl` 的最后两个有效命令必须依次为 `pv_rpt_checkpoints` 和 `exit`。
- `pv_rpt_checkpoints` 汇总该 run 内所有 checkpoint 信息；`exit` 明确结束本次工具执行。
- 文件末尾可以有空行或注释，但不得在 `exit` 后继续执行其他命令。

## 执行顺序

Layer 2A（Nagelfar 1.3.5 静态语法）对树内所有 `.tcl` 文件通过后，才执行 Layer 2B 对整棵用例树的规范检查。任一 `.tcl` 的 2A 失败或工具不可用时，2B 返回 `SKIPPED`，不得用规范检查掩盖语法问题。
