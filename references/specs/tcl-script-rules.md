# TCL 用例脚本规范

版本：`1.0-draft`

状态：`CONFIGURED_NOT_IMPLEMENTED`

本文件是 Layer 2B 的唯一业务规则入口。规则已经配置，但确定性检查器和逐条正反测试尚未实现，因此 Layer 2B 不得报告 `PASS`。

## 1. 适用范围和术语

- 适用于生成给 **Optimus**、**iTools / Innovus** 使用的回归用例目录、`nith.run` 和 TCL 文件。
- “用例”指一个包含输入设计、golden、运行入口和 TCL 脚本的完整目录，不仅指单个 `.tcl` 文件。
- “检查点”指通过 `pv_check_log`、`pv_check_golden` 或 `pv_check_qor` 对结果作确定性判断的调用。
- 规则严重级别均为 `error`；任一规则失败时 Layer 2B 为 `FAIL`。
- 本规范不执行 TCL，也不替代 Nagelfar Layer 2A 语法检查。

## 2. 标准目录结构

```text
<case>/
├── design/
│   └── <design inputs>
├── golden/
│   └── <golden files>
├── nith.run
└── tcl/
    ├── case_setup.tcl
    ├── itools/
    │   ├── mmmc.tcl
    │   └── run_<N>.tcl
    └── optimus/
        ├── mmmc.tcl
        └── run_<N>.tcl
```

只生成目标工具所需的工具子目录；例如仅支持 iTools / Innovus 的用例可以不含 `tcl/optimus/`。`run_<N>.tcl` 的编号从 `1` 开始且连续。没有 MMMC 配置需求时可以不生成 `mmmc.tcl`，但不得生成空占位文件。

## 3. 规则清单

### TCL-SUITE-001：禁止符号链接

- 适用对象：整个用例目录树。
- 通过条件：从用例根目录递归检查时，不存在任何符号链接，包括指向用例目录内部的符号链接和失效链接。
- 确定性检查：对每个目录项执行不跟随链接的文件类型检查；发现 `is_symlink = true` 即失败。
- 正例：`design/top.v`、`golden/check_files.log` 均为普通文件。
- 反例：`design/top.v -> /shared/design/top.v` 或 `golden/qor.csv -> ../baseline/qor.csv`。

### TCL-SUITE-002：目录结构符合约定

- 适用对象：整个用例目录树。
- 通过条件：
  - 用例根目录包含普通文件 `nith.run` 以及目录 `design/`、`golden/`、`tcl/`。
  - `tcl/` 包含普通文件 `case_setup.tcl`。
  - 至少存在一个工具目录 `tcl/itools/` 或 `tcl/optimus/`。
  - 每个存在的工具目录至少包含一个 `run_<N>.tcl`，编号从 `run_1.tcl` 开始且连续。
  - `mmmc.tcl` 可选；存在时必须是普通文件。
- 确定性检查：按固定相对路径、文件类型及 `^run_([1-9][0-9]*)\.tcl$` 检查。
- 正例：本节所示目录树。
- 反例：缺少 `golden/`、将脚本直接放在 `tcl/` 下、只有 `run_2.tcl`。

### TCL-RUNNER-001：`nith.run` 初始化段完整

- 适用对象：`nith.run`。
- 通过条件：文件是 Python 入口，初始化段能够导入 NITH，调用 `nith.init()`，并从 `main` 导入运行接口；不得把截图中的机器专属 Python 路径或 NITH 绝对路径原样写入新用例。
- 确定性检查：使用 Python AST 检查所需导入和调用；另以路径规则拒绝用户目录、项目外机器路径及未声明的绝对路径。
- 正例：使用项目批准的可移植启动头，随后调用 `nith.init()` 和 `from main import *`。
- 反例：删除 `nith.init()`，或硬编码某一用户/机器的 NITH 安装路径。

### TCL-RUNNER-002：`nith.run` 按工具顺序调度脚本

- 适用对象：`nith.run` 及 `tcl/<tool>/run_<N>.tcl`。
- 通过条件：
  - 每个 `run_<N>.tcl` 恰好按编号升序登记一次。
  - 登记路径使用 `tcl/{nith.PV_TOOL}/run_<N>.tcl`，不硬编码 `itools` 或 `optimus`。
  - 每次设置 `nith.input[""]` 后紧接一次 `nith_run()`。
  - 所有运行结束后恰好调用一次 `nith_done()`，且没有后续 `nith_run()`。
- 确定性检查：使用 Python AST 检查赋值、调用和顺序，并与目录中脚本集合比对。
- 正例：依次登记并运行 `run_1.tcl`、`run_2.tcl`、`run_3.tcl`，最后 `nith_done()`。
- 反例：漏跑 `run_2.tcl`、重复运行 `run_1.tcl`、硬编码 `tcl/itools/run_1.tcl`。

### TCL-CHECKPOINT-001：每个用例含有效检查点

- 适用对象：`tcl/**/*.tcl` 形成的整个用例脚本集合。
- 通过条件：用例至少包含一次非注释、非字符串文本中的 `pv_check_log`、`pv_check_golden` 或 `pv_check_qor` 命令调用。
- 解释：斜线表示三种允许的检查点类型，不要求每个用例同时调用三种命令；应按被测结果选择合适类型。一个交付的用例集在适用场景存在时应覆盖三种类型。
- 确定性检查：基于 Tcl parser/命令扫描结果识别实际命令调用；不得仅用子串搜索。
- 正例：日志行为用 `pv_check_log`，写出文件用 `pv_check_golden`，QoR/timing 指标用 `pv_check_qor`。
- 反例：只运行被测命令，或仅在注释中写 `pv_check_log`。

### TCL-CHECKPOINT-002：加载已确认的 PV 入口

- 适用对象：包含检查点调用的用例脚本集合。
- 通过条件：首次检查点调用之前已经 source 目标环境确认的 PV 入口；当前资料包含 `$env(PV_ROOT)/pv/scripts/pv.tcl` 和 Optimus 参考流中的 `$env(PV_ROOT)/scripts/pv.tcl` 两种布局。入口可以由 `case_setup.tcl` 统一加载，且各 `run_<N>.tcl` 不得重复加载。
- 确定性检查：从用例配置取得批准的 PV 入口，解析 `source` 命令，并结合 `case_setup.tcl` 与运行脚本的加载顺序判断；没有配置时返回 `NOT_CONFIGURED`，不得任选一个路径。
- 正例：在 `case_setup.tcl` 中加载用例配置明确指定的 PV 入口。
- 反例：直接 source `pv_check_qor.tcl`，或在检查点之后才加载 `pv.tcl`。

### TCL-CHECKPOINT-003：`pv_check_log` 调用有效

- 适用对象：每个 `pv_check_log` 调用。
- 通过条件：
  - 第一个参数是非空 Tcl 命令块。
  - `-name` 若存在则值非空，并在同一用例中唯一。
  - `-filter` 若存在则有一个非空 Tcl 正则值；其语义是排除匹配行。
  - `-log_files` 若存在则为非空 Tcl list。
  - 不手工输出 `===PV_MARKER begin:` 或 `===PV_MARKER end:`；marker 由 `pv_check_log` 生成。
- 确定性检查：由 Tcl parser 提取命令参数，再检查选项参数数量、名称唯一性及手工 marker。
- 正例：`pv_check_log {report_route} -name rpt_route -filter {^#|^$}`。
- 反例：缺少命令块、`-filter` 无值、手工拼接 marker。

### TCL-CHECKPOINT-004：`pv_check_golden` 调用有效

- 适用对象：每个 `pv_check_golden` 调用。
- 通过条件：
  - 只有一个必需位置参数 `out_file`，且非空。
  - 只允许可选参数 `-golden <golden_file>` 和 `-filter <pattern>`，每个选项至多出现一次且必须带值。
  - golden 路径必须位于用例的 `golden/` 下；省略 `-golden` 时由工具使用默认 golden 位置。
  - 用例脚本不得通过设置 `PV_CHECK_MODE=1` 固定进入 regolden；模式由运行环境控制。
- 确定性检查：解析参数表、规范化相对路径，并扫描对 `env(PV_CHECK_MODE)` 的写操作。
- 正例：`pv_check_golden ./out/design.def -golden ./golden/design.def`。
- 反例：golden 指向用例目录外、未知选项、在用例内设置 `set env(PV_CHECK_MODE) 1`。

### TCL-CHECKPOINT-005：`pv_check_qor` 调用有效

- 适用对象：每个 `pv_check_qor` 调用。
- 通过条件：
  - 第一个参数是非空命令块。
  - 只允许 `-name`、`-golden`、`-tolerance`、`-rel_tolerance`、`-dir`，每个选项至多出现一次且必须带值。
  - `-name` 若存在则非空，并在同一用例中唯一。
  - `-golden` 若存在则位于用例的 `golden/` 下。
  - `-tolerance` 和 `-rel_tolerance` 若存在，必须是大于或等于 `0` 的有限数值。
  - `-dir` 若存在，必须位于用例运行输出目录内，不得使用用例外绝对路径或 `..` 逃逸。
  - 命令块只使用当前已支持的解析命令：Optimus 的 `report_timing`、`report_qor`，或 iTools / Innovus 的 `report_timing`、`timeDesign`。
- 确定性检查：解析调用参数、数值和规范化路径；根据用例工具上下文核对命令白名单。
- 正例：`pv_check_qor {timeDesign -postRoute} -name post_route -golden ./golden/post_route.csv -dir ./out -tolerance 0.01`。
- 反例：负容差、`-golden ../shared/qor.csv`、对未注册的 `report_power` 使用 QoR 检查点。

### TCL-SCRIPT-001：测试动作与期望标记

- 适用对象：每个 `run_<N>.tcl`。
- 通过条件：恰好一个 `# TEST_ACTION`，且在其前面存在与用例极性一致的 `# EXPECT: PASS` 或 `# EXPECT: FAIL`。
- 确定性检查：按行解析注释标记，并与测试计划/用例元数据比对。
- 正例：正例脚本在动作前标记 `# EXPECT: PASS`。
- 反例：两个 `# TEST_ACTION`，或负例使用 `# EXPECT: PASS`。

### TCL-SCRIPT-002：禁止未完成占位符

- 适用对象：`nith.run` 和全部 `.tcl` 文件。
- 通过条件：代码及注释中不含独立词 `TODO` 或 `TBD`。
- 确定性检查：大小写不敏感的词边界扫描。
- 正例：所有配置和断言均已填写。
- 反例：`# TODO: add checkpoint`。

## 4. 检查点选型

| 被检查结果 | 使用命令 | 典型用途 |
|---|---|---|
| EDA 命令的日志片段 | `pv_check_log` | 自动执行命令、生成 marker、过滤并对比日志 |
| 已写出的 DEF/SPEF/report 等文件 | `pv_check_golden` | 当前输出文件与 golden 文件直接比较 |
| timing/QoR 数值指标 | `pv_check_qor` | 解析指标 CSV，按绝对或相对容差比较 |

不得只凭进程退出码判定用例通过，也不得用手工 `puts "PASS"` 代替检查点。

## 5. 来源与实现边界

- 目录结构与 `nith.run`：用户提供的参考截图。
- `pv_check_log`、`pv_check_golden`：`pv_check tcl 命令用户指南.pdf`。
- `pv_check_qor`：`pv_check_qor_usage.md`。
- 截图中的 Python shebang 和 NITH 搜索绝对路径只作为旧入口行为参考，不作为可复制的跨机器路径规范。
- 后续实现 F-015 时，每条规则必须增加至少一个自动化正例和一个自动化反例；在此之前保持 `CONFIGURED_NOT_IMPLEMENTED`。
