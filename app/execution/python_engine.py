"""Runs submitted Python code: a fast local syntax pre-check, then an
isolated `python -I` subprocess with a timeout."""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional

from app.execution.base import DEFAULT_TIMEOUT_SECONDS, ExecutionEngine, ExecutionResult, RunHandle


class PythonEngine(ExecutionEngine):
    language = "python"

    def run(
        self,
        code: str,
        timeout: float = DEFAULT_TIMEOUT_SECONDS,
        handle: Optional[RunHandle] = None,
        stdin_text: Optional[str] = None,
    ) -> ExecutionResult:
        try:
            compile(code, "<exercise>", "exec")
        except SyntaxError as exc:
            code_line = (exc.text or "").rstrip("\n")
            stderr = f'  File "<exercise>", line {exc.lineno}\n    {code_line}\nSyntaxError: {exc.msg}\n'
            return ExecutionResult(success=False, stderr=stderr)

        with tempfile.TemporaryDirectory(prefix="codingadventure_") as tmp_dir:
            code_file = Path(tmp_dir) / "exercise.py"
            code_file.write_text(code, encoding="utf-8")

            process = subprocess.Popen(
                [sys.executable, "-I", str(code_file)],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=tmp_dir,
            )
            if handle is not None:
                handle._attach(process)

            try:
                # Always feed (and close) stdin -- even "" -- so an
                # unexpected input() call fails fast with EOFError instead
                # of hanging until the timeout.
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
