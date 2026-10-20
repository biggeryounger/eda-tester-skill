# Initial design 参考模板

来源：用户于 2026-10-20 提供的两张截图，按可见内容转录。图 1 为 Optimus，图 2 为 iTools。截图为参考资料，脚本未经真实 EDA 工具执行验证。

| 工具 | TCL 模板 | 原始截图 |
| --- | --- | --- |
| iTools | [itools.tcl](itools.tcl) | [itools-source.png](itools-source.png) |
| Optimus | [optimus.tcl](optimus.tcl) | [optimus-source.png](optimus-source.png) |

## 使用上下文

- 从用例根目录执行，依赖 `$env(PV_ROOT)/scripts/pv.tcl` 和 `./tcl/design.tcl`。
- `design.tcl` 提供 `lef_files`、`verilog_files`、`ground_net`、`power_net`、`init_top_name`、`def_file`；MMMC 分别来自 `./tcl/itools/mmmc.tcl` 或 `./tcl/optimus/mmmc.tcl`。
- 保留原图线程数 8、初始化顺序、初始化后的 DEF 读取及 `#return` 注释；`#return` 不会中断执行。
- 这些文件只记录初始化片段；生成完整测试用例时仍遵循 Skill workflow 和 TCL 规范，按目标工具使用对应方言，并从已确认的 design/tech 映射归档输入文件。
