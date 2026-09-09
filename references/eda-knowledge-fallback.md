# EDA 知识库回退

当用户材料不足以确定命令语法、option、默认值、约束、交互、版本差异、环境前置或预期行为时，禁止凭经验补造，按以下流程查询 `eda-knowledge-base` MCP：

1. 确认 `get_eda_kb_status`、`list_eda_documents`、`ask_eda_question`、`search_eda_knowledge` 可用；不可用时报告知识库未连接，并把缺失事实记为 `SPEC-GAP`。
2. 确定目标工具和版本。未知时先用 `list_eda_documents` 查看可用文档；已知时必须使用精确 `tool`、`version` 过滤，禁止静默混合版本。
3. 一般问题调用 `ask_eda_question`，使用 `scope: "raw"`。命令、option、默认值、互斥/依赖、边界或初次回答较弱时，再用 `search_eda_knowledge` 分项检索。
4. 只采用 `grounded: true` 且有原始证据支持的结论；保留命令、option、变量和 Tcl 的精确拼写，并记录文档、版本、章节及页码或行号。
5. 搜索排名只表示相关度。无证据时记录“当前知识库没有找到足以构造该测试点的证据”；证据冲突时分别记录并优先原始权威材料。不得据此生成未经确认的 TCL。

只有知识库补齐了构造该用例所需的事实，才继续覆盖设计；否则停止受影响用例的 TCL 生成并向用户列出缺口。
