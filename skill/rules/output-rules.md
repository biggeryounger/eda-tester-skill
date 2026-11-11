# 输出规则

## 设计与 Excel

依据 [测试策略](../references/test-strategies.md) 最大化单用例的兼容测试点覆盖；不得一项 option 一个用例。仅在测试点冲突、初始化不同或预期无法共同观察时拆分。由命令规格清单建立覆盖矩阵，分别报告场景覆盖率、被测选项覆盖率的分子、分母、百分比和未覆盖项。

必须通过 [生成器](../scripts/generate_test_plan.py) 从测试计划模板生成至少一条有效用例；禁止空表交付。Excel 必须同时通过 [结构检查](../scripts/test_plan_validator.py) 和 [语义审查](../references/specs/test-plan-rules.md)。

新设计必须先展示设计及覆盖结果，等待明确批准；确认前不得生成 TCL。策略选择不等于用例设计确认。

## TCL 与交付

每条 Excel 用例生成一个独立目录，参考 [脚本示例](../references/examples/pos001_keep_shape/nith.run)。通用设计配置归档到 `<case_dir>/tcl/design.tcl`，目标工具 MMMC 归档到 `<case_dir>/tcl/<tool>/mmmc.tcl`；归档后不得依赖模板原目录，不得跨工具替换 MMMC。

所有工具均需通过 [编程规范检查](../scripts/tcl_convention_validator.py)。Optimus 使用 `--syntax` 分别报告 Tcl 基础语法、EDA 工具命令及选项使用、TCL 编程规范，详见 [检查边界](../references/optimus-syntax/index.md)。iTools 使用 [命令检查器](../scripts/itools_check.py)，详见 [规则覆盖与缺口](../references/itools-syntax/index.md)：PARTIAL_RULES 等未解决覆盖缺口不得视为完整通过。

按 [TCL 语义规范](../references/specs/tcl-script-rules.md) 审查设计追溯、工具语义、检查点充分性及多步数据流。检查环境或资料缺失报告 `TOOL_UNAVAILABLE`，不得以人工判断替代；任何 `FAIL`、未解决 `SPEC-GAP` 或 `TOOL_UNAVAILABLE` 都必须停止交付，进入 `WAIT-SCRIPT-DELIVERY-FIX`，全部问题解决并重新验证通过后恢复。
