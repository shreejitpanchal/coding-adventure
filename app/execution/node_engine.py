"""Node.js execution engine: runs submitted JavaScript with `node`, no
separate compile step needed (unlike Java/C++) -- syntax errors just
surface as Node's own stderr output when the file is run, same as
Python's interpreter. Same timeout/RunHandle/stdin contract as the other
single-file engines."""
from __future__ import annotations

import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from app.execution.base import (
    DEFAULT_TIMEOUT_SECONDS,
    ExecutionEngine,
    ExecutionResult,
    RunHandle,
    blocked_result,
    run_subprocess,
)
from app.execution.toolchain_check import check_toolchain

if TYPE_CHECKING:
    from app.engine.exercise import Exercise

CODE_FILENAME = "<exercise>"

# Crash containment for V8: caps the old-space heap so an accidental
# `while (true) arr.push(...)` dies with a heap-limit error instead of
# consuming the machine. Plenty for exercise-sized programs.
NODE_MAX_OLD_SPACE = "--max-old-space-size=256"


class NodeEngine(ExecutionEngine):
    language = "node"

    def run(
        self,
        code: str,
        timeout: float = DEFAULT_TIMEOUT_SECONDS,
        handle: Optional[RunHandle] = None,
        stdin_text: Optional[str] = None,
        exercise: Optional["Exercise"] = None,
    ) -> ExecutionResult:
        status = check_toolchain("node")
        if not status.available:
            return blocked_result("Node.js", status)

        with tempfile.TemporaryDirectory(prefix="codingadventure_node_") as tmp_dir:
            code_file = Path(tmp_dir) / "exercise.js"
            code_file.write_text(code, encoding="utf-8")
            # stdin is fed even though idiomatic Node reads it asynchronously
            # (readline) -- same contract as every other engine.
            outcome = run_subprocess(["node", NODE_MAX_OLD_SPACE, str(code_file)], tmp_dir, stdin_text, timeout, handle)

        if outcome.timed_out:
            return ExecutionResult(success=False, timed_out=True)
        return ExecutionResult(
            success=outcome.returncode == 0,
            stdout=outcome.stdout.replace(str(code_file), CODE_FILENAME),
            stderr=outcome.stderr.replace(str(code_file), CODE_FILENAME),
        )
