#!/usr/bin/env bash
# Developer task runner (bash). Mirrors scripts/dev.ps1 exactly -- keep both
# in sync when a gate changes, and keep them in step with .github/workflows/ci.yml.
#
# Usage: scripts/dev.sh <task> [<task> ...]
#
# Tasks:
#   lint     ruff check (style/errors only; the rule set lives in pyproject.toml)
#   test     full pytest suite
#   cov      pytest under coverage -> scripts/logs/htmlcov/ + printed total
#   content  content-lint tests only (fast check after editing YAML)
#   all      lint test cov
#   help     this text
#
# Every task truncates scripts/logs/<task>.log, then tees its output there.
# Correctness gates (lint/test/cov) are fatal: the first failure stops the run.
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
LOG_DIR="$SCRIPT_DIR/logs"
mkdir -p "$LOG_DIR"
cd "$REPO_ROOT"

export NO_COLOR=1
export PYTHONUTF8=1

if [ -f ".venv/Scripts/python.exe" ]; then
    PY=".venv/Scripts/python.exe"
elif [ -f ".venv/bin/python" ]; then
    PY=".venv/bin/python"
else
    PY="${PYTHON:-python}"
fi

if [ -t 1 ]; then
    C_STEP=$'\033[36m'; C_OK=$'\033[32m'; C_WARN=$'\033[33m'; C_DIE=$'\033[31m'; C_END=$'\033[0m'
else
    C_STEP=""; C_OK=""; C_WARN=""; C_DIE=""; C_END=""
fi
step() { printf '%s==> %s%s\n' "$C_STEP" "$*" "$C_END"; }
ok()   { printf '%s  ok: %s%s\n' "$C_OK" "$*" "$C_END"; }
warn() { printf '%swarn: %s%s\n' "$C_WARN" "$*" "$C_END" >&2; }
die()  { printf '%sfail: %s%s\n' "$C_DIE" "$*" "$C_END" >&2; exit 1; }

strip_ansi() { sed -r 's/\x1b\[[0-9;]*[mGKHF]//g'; }

# run_logged <task> <cmd...>: fresh log per run, tee everything, keep exit code.
run_logged() {
    local task="$1"; shift
    local log="$LOG_DIR/$task.log"
    {
        echo "== $task  $(date -u +%Y-%m-%dT%H:%M:%SZ)"
        echo "== cwd: $REPO_ROOT"
        echo "== cmd: $*"
    } > "$log"
    "$@" 2>&1 | strip_ansi | tee -a "$log"
    return "${PIPESTATUS[0]}"
}

task_lint() {
    step "lint (ruff)"
    if ! "$PY" -m ruff --version >/dev/null 2>&1; then
        die "ruff is not installed in the venv -- run: $PY -m pip install -r requirements-dev.txt"
    fi
    run_logged lint "$PY" -m ruff check app tests main.py main_web.py || die "lint failed (see $LOG_DIR/lint.log)"
    ok "lint"
}

task_test() {
    step "test (pytest)"
    run_logged test "$PY" -m pytest tests -q -p no:cacheprovider || die "tests failed (see $LOG_DIR/test.log)"
    ok "test"
}

task_content() {
    step "content lint"
    run_logged content "$PY" -m pytest tests/test_content_lint.py -q -p no:cacheprovider || die "content lint failed (see $LOG_DIR/content.log)"
    ok "content"
}

task_cov() {
    step "coverage"
    if ! "$PY" -c "import coverage" >/dev/null 2>&1; then
        die "coverage is not installed in the venv -- run: $PY -m pip install -r requirements-dev.txt"
    fi
    run_logged cov bash -c "
        '$PY' -m coverage run -m pytest tests -q -p no:cacheprovider && \
        '$PY' -m coverage html -d '$LOG_DIR/htmlcov' >/dev/null && \
        '$PY' -m coverage report
    " || die "coverage run failed (see $LOG_DIR/cov.log)"
    ok "coverage report: $LOG_DIR/htmlcov/index.html"
}

usage() {
    sed -n '2,20p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
}

if [ $# -eq 0 ]; then usage; exit 0; fi

for task in "$@"; do
    case "$task" in
        lint) task_lint ;;
        test) task_test ;;
        cov) task_cov ;;
        content) task_content ;;
        all) task_lint; task_test; task_cov ;;
        help|-h|--help) usage ;;
        *) die "unknown task '$task' (try: help)" ;;
    esac
done
