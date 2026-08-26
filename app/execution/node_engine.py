"""Node.js execution engine: runs submitted JavaScript with `node`, no
separate compile step needed (unlike Java/C++) -- syntax errors just
surface as Node's own stderr output when the file is run, same as
Python's interpreter. Same timeout/RunHandle/stdin contract as the other
single-file engines."""
from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from app.execution.base import DEFAULT_TIMEOUT_SECONDS, ExecutionEngine, ExecutionResult, RunHandle
from app.execution.toolchain_check import check_toolchain

if TYPE_CHECKING:
    from app.engine.exercise import Exercise


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
            return ExecutionResult(
                success=False, blocked=True,
                blocked_message=f"Node.js toolchain not found (missing: {', '.join(status.missing)}). {status.install_hint}",
            )

        with tempfile.TemporaryDirectory(prefix="codingadventure_node_") as tmp_dir:
            code_file = Path(tmp_dir) / "exercise.js"
            code_file.write_text(code, encoding="utf-8")

            process = subprocess.Popen(
                ["node", str(code_file)],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=tmp_dir,
            )
            if handle is not None:
                handle._attach(process)

            try:
                # Always feed (and close) stdin -- even "" -- matching every
                # other engine's contract, even though idiomatic Node code
                # reads stdin asynchronously (readline) rather than via a
                # blocking call the way Python's input()/Java's Scanner do.
                stdout, stderr = process.communicate(input=stdin_text or "", timeout=timeout)
            except subprocess.TimeoutExpired:
                process.kill()
                process.communicate()
                return ExecutionResult(success=False, timed_out=True)

        if handle is not None and handle.cancelled:
            return ExecutionResult(success=False, timed_out=True)

        stdout = (stdout or "").replace(str(code_file), "<exercise>")
        stderr = (stderr or "").replace(str(code_file), "<exercise>")
        return ExecutionResult(success=process.returncode == 0, stdout=stdout, stderr=stderr)
