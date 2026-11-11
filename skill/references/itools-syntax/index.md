# iTools 命令静态检查

用户提供的 Innovus 手册检查器归档为 `scripts/itools_check.py`，配套规则为本目录 `rules.json`。仅调整默认规则路径和规则内来源路径（去除用户本地绝对路径）；不复制构建脚本、缓存、原 PDF 或开发测试。原始 check.py SHA-256：`4e93c7b4c432f83fd28330c562289a07990fdeef90c76c4db3adfb9f5e85fcb2`。

## 运行

在 Skill 根目录运行：

```sh
python3 scripts/itools_check.py <case_dir>/tcl/design.tcl <case_dir>/tcl/itools/*.tcl --format json
python3 scripts/itools_check.py --coverage
```

对每个生成用例执行，显式包含 design、MMMC 和全部 run 脚本；若还有被 source 的本地 Tcl 文件，亦需显式传入。支持 `--rules <rules.json>`。仅依赖 Python 标准库，不执行输入脚本、不自动 source、不需要 EDA 许可证。规则按脚本位置定位，不依赖当前目录或原始工具目录。

## 规则与裁决

资料为 Innovus Text Command Reference 18.13（January 2019），PDF SHA-256 保留在规则 source 元数据中；这是来源信息，不要求用户提供或匹配工具版本。

收录 1,333 个命令，6 个命令人工核对了选项全集及关键约束：ecoAddRepeater、ecoChangeCell、ecoDeleteRepeater、ecoPlace、setEcoMode、addHierInst。支持已提取的选项、缺值、必填、互斥、依赖和枚举；诊断包含文件、行列、手册页码。

- 退出码 1：有确定命令规则错误，必须修复。
- 退出码 2：检查无法完成，作为 TOOL_UNAVAILABLE 阻止交付。
- 退出码 0：仅表示已实现规则未发现确定错误。必须同时查看 summary 和 diagnostics。
- PARTIAL_RULES、UNVERIFIED_OPTION、UNRESOLVED、UNLISTED_COMMAND 等 info/warning 表示覆盖缺口，记录 SPEC-GAP，结合命令说明核实并记录依据；未解决时进入 WAIT-SCRIPT-DELIVERY-FIX，不得直接宣称 PASS。

检查器只做最小词法拆分，不提供 Tcl 基础语法诊断。部分控制体和命令替换会递归检查，但不展开 PV 命令块、source、eval/uplevel/switch/try/apply，不做变量传播。未收录命令可能是 PV、自定义过程或其他工具命令，不能据此判定不存在。检查不证明对象存在、设计状态正确或脚本可在真实 EDA 中运行。Tcl 基础语法未验证或其他资料不足亦须明确记录，不能以本工具替代完整语法验证。
