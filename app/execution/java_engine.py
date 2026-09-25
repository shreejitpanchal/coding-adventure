"""Java execution engine: detects the submitted code's class name, compiles
it with `javac`, then runs it with `java -cp <dir> <ClassName>` under the
same timeout/RunHandle/stdin contract as python_engine.PythonEngine."""
from __future__ import annotations

import subprocess
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
from app.execution.java_source import detect_class_name
from app.execution.toolchain_check import check_toolchain

if TYPE_CHECKING:
    from app.engine.exercise import Exercise

COMPILE_TIMEOUT_SECONDS = 20.0

# Crash containment for the JVM side: a runaway `new int[1 << 30]` loop
# otherwise grows until the host machine swaps. Generous for any
# exercise here, tight enough that a mistake fails fast with an
# OutOfMemoryError the error translator can name.
JVM_MAX_HEAP = "-Xmx256m"


class JavaEngine(ExecutionEngine):
    language = "java"

    def run(
        self,
        code: str,
        timeout: float = DEFAULT_TIMEOUT_SECONDS,
        handle: Optional[RunHandle] = None,
        stdin_text: Optional[str] = None,
        exercise: Optional["Exercise"] = None,
    ) -> ExecutionResult:
        status = check_toolchain("java")
        if not status.available:
            return blocked_result("Java", status)

        class_name = detect_class_name(code)

        with tempfile.TemporaryDirectory(prefix="codingadventure_java_") as tmp_dir:
            source_file = Path(tmp_dir) / f"{class_name}.java"
            source_file.write_text(code, encoding="utf-8")

            # Both javac and java are given only the bare filename/class name
            # and run with cwd=tmp_dir, so no host path leaks into a compiler
            # error or stack trace.
            try:
                compile_result = subprocess.run(
                    ["javac", source_file.name],
                    cwd=tmp_dir, capture_output=True, text=True, timeout=COMPILE_TIMEOUT_SECONDS,
                )
            except subprocess.TimeoutExpired:
                return ExecutionResult(success=False, timed_out=True)
            if compile_result.returncode != 0:
                return ExecutionResult(success=False, stderr=compile_result.stderr)

            outcome = run_subprocess(
                ["java", JVM_MAX_HEAP, "-cp", ".", class_name], tmp_dir, stdin_text, timeout, handle,
            )

        if outcome.timed_out:
            return ExecutionResult(success=False, timed_out=True)
        return ExecutionResult(success=outcome.returncode == 0, stdout=outcome.stdout, stderr=outcome.stderr)
