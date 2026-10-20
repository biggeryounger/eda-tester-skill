# Jenkins 完整测试与审批合入门禁

## 流程

```text
候选分支/提交
  → 校验包含最新目标分支
  → 运行完整测试集
  → 发布 JUnit、HTML 和完整日志
  → 人工审阅并批准
  → 确认候选提交和远端目标分支均未变化
  → fast-forward 推送到目标分支
```

测试失败时不会出现审批步骤；审批拒绝、超时、候选提交变化或目标分支变化都不会合入。

## 人工结束触发

流水线不会因普通任务完成而自动启动。只有用户明确要求“上传代码”后，才先同步 `skill/SKILL.md` 和相关 README、运行本地完整门禁、推送候选分支，再以该分支触发本流水线。测试通过后仍由用户在 Jenkins 中审批是否合入。

## 启动

1. 复制 `.env.example` 为 `.env`，填写 Jenkins 管理员密码；镜像构建不要求秘密，但启动服务必须提供管理员密码。
2. 填写 GitHub fine-grained token 后才允许审批后合入；未配置 Token 时可以构建和查看 Jenkins，但合入阶段不可用。
3. Token 仅授权 `biggeryounger/eda-tester-skill` 的 Contents 读写，不写入仓库文件或日志。
4. 在本目录执行：

```sh
docker compose up --build -d
```

5. 打开 `http://localhost:8081`，登录后运行 `eda-tester-skill-approved-merge`。如端口仍冲突，可在 `.env` 中修改 `JENKINS_HTTP_PORT` 和 `JENKINS_AGENT_PORT`。
6. `CANDIDATE_REF` 填写远端候选分支，例如 `refs/heads/codex/my-change`；`TARGET_BRANCH` 通常保持 `main`。
7. 测试通过后打开“EDA Tester Skill 完整测试报告”，确认无误再点击“批准合入”。

## GitHub 必需设置

为了保证所有开发代码都经过该门禁，必须为 `main` 配置 branch ruleset：

- 禁止普通开发者直接 push。
- 禁止 force push 和删除分支。
- 仅允许 Jenkins 使用的机器人账号更新 `main`。
- 开发者只能推送候选分支，然后由本流水线测试、审批和合入。

如果仍允许其他账号直接写入 `main`，Jenkinsfile 无法单独保证“每次合入必测”。

## 完整用例集

`harness/scripts/run_jenkins_gate.py` 固定执行：

1. 项目清单、功能登记和 fixture 检查。
2. `harness/tests/unit/` 下全部单元及回归测试。
3. `skill/` 发布产物结构与隔离检查。

完整单元测试包含十项受保护冒烟的契约与执行验证；独立运行入口为 `./init.sh test smoke`。审批时需审阅 `skill/references/input/design_input_tcl/` 输入资源、PV 接口资料和 TCL 检查规则的差异；这些资料的归档不代表真实 EDA 工具验证通过。

报告输出到 `harness/outputs/jenkins/`，Jenkins 会归档：

- `index.html`
- `junit.xml`
- `complete.log`

## 代码来源与信任边界

流水线定义由 Jenkins SCM 从固定 GitHub 仓库的 `main` 加载，不读取本地 Jenkinsfile，也不从 CANDIDATE_REF 加载流水线。启动配置属于管理员控制面；具有修改 Jenkins 配置、启动脚本或容器权限的用户仍能改变门禁。

每次构建先清空 Jenkins 工作区，再从 GitHub 获取候选 ref 并锁定提交 SHA；测试脚本、用例和被测 Skill 均来自该远端提交。本地完整门禁只是上传前检查，不作为 Jenkins 合入依据。

候选提交仍可能修改测试或检查器，因此“来自远端”不能证明测试未被削弱；审批时必须审阅候选提交中 harness、init.sh 和测试依赖的差异。当前机制不提供独立于候选提交的受保护测试基线。

首次迁移需先经现有审批流程使 `main` 包含 `harness/jenkins/Jenkinsfile`，再重建并重启 Jenkins，以应用新的 SCM 任务定义；远端文件缺失或读取失败时构建失败，不回退本地流水线。任务初始化通过重启更新，正在运行的旧构建不因此切换定义。
