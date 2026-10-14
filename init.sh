#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
DRY_RUN=0

if [ "${1:-}" = "--dry-run" ]; then
    DRY_RUN=1
    shift
fi

PYTHON=python3
if [ -x "$ROOT/.venv/bin/python" ]; then
    PYTHON="$ROOT/.venv/bin/python"
fi

print_command() {
    printf '+'
    for argument in "$@"; do
        printf ' %s' "$argument"
    done
    printf '\n'
}

run() {
    print_command "$@"
    if [ "$DRY_RUN" -eq 0 ]; then
        "$@"
    fi
}

usage() {
    cat <<'EOF'
用法：./init.sh [--dry-run] <命令> [参数]

一键工作流：
  dev                         创建 .venv，安装 Python 依赖并检查 Tcl
  deploy [安装器参数...]       结构预检并部署 Skill；参数透传给安装器
  test all                    运行 Jenkins 同款完整测试门禁
  test layer1                 检查项目、Skill 结构、Python 依赖和 Tcl 环境
  test layer2 PLAN CASE...    检查测试计划和对应 TCL 用例目录
  test unit                   运行全部 Python 单元测试
  test project                检查项目清单、用例元数据和基础契约
  test skill                  检查可安装 Skill 的结构
  test feature FEATURE_ID     运行指定功能点登记的测试
  test tcl CASE_DIR...        运行指定 TCL 用例目录的规范检查
  test plan PLAN [参数...]    运行 Excel 测试计划检查
  test delivery PLAN CASE...  运行 Excel → TCL 交付门禁
  help                        显示本帮助

示例：
  ./init.sh dev
  ./init.sh deploy
  ./init.sh deploy --agent opencode
  ./init.sh deploy --mode copy
  ./init.sh --dry-run deploy --agent trae --skills-dir /path/to/trae/skills
  ./init.sh test all
  ./init.sh test feature F-026
  ./init.sh test layer2 plan.xlsx path/to/pos001_case

部署约定：
  - 默认目标是 Codex，使用逐项软链接；其他 Agent 默认复制独立副本。
  - 支持 codex、opencode、hermes、workbuddy、trae。
  - 默认目录由对应 Agent 根目录决定，可用 --skills-dir 覆盖。
  - 仅部署 skill/ 运行时白名单内容，不包含 harness/ 开发与测试环境。
  - 不覆盖已有同名 Skill；需要重装时先人工确认并移走原目标。
  - 部署后重启对应 Agent；Codex 也可以新建任务触发重新扫描。

启动示例：
  $eda-tester-skill 根据这份 Innovus 命令说明生成测试计划和 TCL 用例。

未识别 Skill 时检查：
  1. 安装目录下是否直接存在 eda-tester-skill/SKILL.md。
  2. SKILL.md 是否声明 name: eda-tester-skill。
  3. 是否已重启 Agent 或新建 Codex 任务。
EOF
}

need_args() {
    minimum=$1
    actual=$2
    message=$3
    if [ "$actual" -lt "$minimum" ]; then
        printf 'ERROR: %s\n' "$message" >&2
        exit 2
    fi
}

command=${1:-help}
if [ "$#" -gt 0 ]; then
    shift
fi

cd "$ROOT"

case "$command" in
    help|-h|--help)
        usage
        ;;
    dev)
        run python3 -m venv "$ROOT/.venv"
        if [ "$DRY_RUN" -eq 0 ]; then
            PYTHON="$ROOT/.venv/bin/python"
        else
            PYTHON="$ROOT/.venv/bin/python"
        fi
        run "$PYTHON" -m pip install --upgrade pip openpyxl
        run "$PYTHON" -c 'import openpyxl; print("openpyxl", openpyxl.__version__)'
        run tclsh "$ROOT/harness/scripts/check_tcl_environment.tcl"
        ;;
    deploy)
        run "$PYTHON" "$ROOT/harness/scripts/quick_validate.py"
        run "$PYTHON" "$ROOT/harness/scripts/install_skill.py" "$@"
        ;;
    test)
        scenario=${1:-}
        need_args 1 "$#" "test 后必须指定场景"
        shift
        case "$scenario" in
            all)
                run "$PYTHON" "$ROOT/harness/scripts/run_jenkins_gate.py"
                ;;
            layer1)
                run "$PYTHON" "$ROOT/skill/scripts/validate.py" project
                run "$PYTHON" "$ROOT/harness/scripts/quick_validate.py"
                run "$PYTHON" -c 'import openpyxl; print("openpyxl", openpyxl.__version__)'
                run tclsh "$ROOT/harness/scripts/check_tcl_environment.tcl"
                ;;
            layer2)
                need_args 2 "$#" "test layer2 需要 PLAN 和至少一个 CASE_DIR"
                run "$PYTHON" "$ROOT/skill/scripts/validate.py" delivery "$@"
                ;;
            unit)
                run "$PYTHON" -m unittest discover -s "$ROOT/harness/tests/unit" -v
                ;;
            project)
                run "$PYTHON" "$ROOT/skill/scripts/validate.py" project "$@"
                ;;
            skill)
                run "$PYTHON" "$ROOT/harness/scripts/quick_validate.py"
                ;;
            feature)
                need_args 1 "$#" "test feature 需要 FEATURE_ID"
                run "$PYTHON" "$ROOT/skill/scripts/validate.py" feature "$@"
                ;;
            tcl|plan|delivery)
                need_args 1 "$#" "test $scenario 缺少输入参数"
                run "$PYTHON" "$ROOT/skill/scripts/validate.py" "$scenario" "$@"
                ;;
            *)
                printf 'ERROR: 未知测试场景：%s\n' "$scenario" >&2
                usage >&2
                exit 2
                ;;
        esac
        ;;
    *)
        printf 'ERROR: 未知命令：%s\n' "$command" >&2
        usage >&2
        exit 2
        ;;
esac
