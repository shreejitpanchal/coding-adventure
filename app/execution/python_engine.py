"""Runs submitted Python code: a fast local syntax pre-check, then an
isolated `python -I` subprocess with a timeout."""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from app.execution.base import (
    DEFAULT_TIMEOUT_SECONDS,
    ExecutionEngine,
    ExecutionResult,
    RunHandle,
    run_subprocess,
)

if TYPE_CHECKING:
    from app.engine.exercise import Exercise

CODE_FILENAME = "<exercise>"


class PythonEngine(ExecutionEngine):
    language = "python"

    def run(
        self,
        code: str,
        timeout: float = DEFAULT_TIMEOUT_SECONDS,
        handle: Optional[RunHandle] = None,
        stdin_text: Optional[str] = None,
        exercise: Optional["Exercise"] = None,
    ) -> ExecutionResult:
        try:
            compile(code, CODE_FILENAME, "exec")
        except SyntaxError as exc:
            code_line = (exc.text or "").rstrip("\n")
            stderr = f'  File "{CODE_FILENAME}", line {exc.lineno}\n    {code_line}\nSyntaxError: {exc.msg}\n'
            return ExecutionResult(success=False, stderr=stderr)

        with tempfile.TemporaryDirectory(prefix="codingadventure_") as tmp_dir:
            code_file = Path(tmp_dir) / "exercise.py"
            code_file.write_text(code, encoding="utf-8")
            outcome = run_subprocess([sys.executable, "-I", str(code_file)], tmp_dir, stdin_text, timeout, handle)

        if outcome.timed_out:
            return ExecutionResult(success=False, timed_out=True)
        return ExecutionResult(
            success=outcome.returncode == 0,
            stdout=outcome.stdout.replace(str(code_file), CODE_FILENAME),
            stderr=outcome.stderr.replace(str(code_file), CODE_FILENAME),
        )
