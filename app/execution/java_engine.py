"""Java execution engine: detects the submitted code's class name, compiles
it with `javac`, then runs it with `java -cp <dir> <ClassName>` under the
same timeout/RunHandle/stdin contract as python_engine.PythonEngine."""
from __future__ import annotations

import re
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

from app.execution.base import DEFAULT_TIMEOUT_SECONDS, ExecutionEngine, ExecutionResult, RunHandle
from app.execution.toolchain_check import check_toolchain

COMPILE_TIMEOUT_SECONDS = 20.0

_PUBLIC_CLASS_RE = re.compile(r"\bpublic\s+(?:final\s+|abstract\s+)?class\s+(\w+)")
_ANY_CLASS_RE = re.compile(r"\bclass\s+(\w+)")


def _detect_class_name(code: str) -> str:
    match = _PUBLIC_CLASS_RE.search(code)
    if match:
        return match.group(1)
    match = _ANY_CLASS_RE.search(code)
    if match:
        return match.group(1)
    return "Solution"


class JavaEngine(ExecutionEngine):
    language = "java"

    def run(
        self,
        code: str,
        timeout: float = DEFAULT_TIMEOUT_SECONDS,
        handle: Optional[RunHandle] = None,
        stdin_text: Optional[str] = None,
    ) -> ExecutionResult:
        status = check_toolchain("java")
        if not status.available:
            return ExecutionResult(
                success=False, blocked=True,
                blocked_message=f"Java toolchain not found (missing: {', '.join(status.missing)}). {status.install_hint}",
            )

        class_name = _detect_class_name(code)

        with tempfile.TemporaryDirectory(prefix="codingadventure_java_") as tmp_dir:
            source_file = Path(tmp_dir) / f"{class_name}.java"
            source_file.write_text(code, encoding="utf-8")

            try:
                compile_result = subprocess.run(
                    ["javac", source_file.name],
                    cwd=tmp_dir, capture_output=True, text=True, timeout=COMPILE_TIMEOUT_SECONDS,
                )
            except subprocess.TimeoutExpired:
                return ExecutionResult(success=False, timed_out=True)

            if compile_result.returncode != 0:
                return ExecutionResult(success=False, stderr=compile_result.stderr)

            process = subprocess.Popen(
                ["java", "-cp", tmp_dir, class_name],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=tmp_dir,
            )
            if handle is not None:
                handle._attach(process)

            try:
                stdout, stderr = process.communicate(input=stdin_text or "", timeout=timeout)
            except subprocess.TimeoutExpired:
                process.kill()
                process.communicate()
                return ExecutionResult(success=False, timed_out=True)

        if handle is not None and handle.cancelled:
            return ExecutionResult(success=False, timed_out=True)

        return ExecutionResult(success=process.returncode == 0, stdout=stdout, stderr=stderr)
