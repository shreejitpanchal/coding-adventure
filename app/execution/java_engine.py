"""Java execution engine -- interface defined, not yet implemented.

Planned shape: write the submitted code to a temp dir as a detected public
class name, `javac` it (compile errors surface the same way a failed run
does today), then `java -cp <dir> <ClassName>` with the same
timeout/RunHandle/stdin contract as app.execution.python_engine.PythonEngine.
Left unimplemented until the Java content track is built out -- see
app.execution.toolchain_check for the availability gate the UI checks
before ever calling into this."""
from __future__ import annotations

from typing import Optional

from app.execution.base import DEFAULT_TIMEOUT_SECONDS, ExecutionEngine, ExecutionResult, RunHandle


class JavaEngine(ExecutionEngine):
    language = "java"

    def run(
        self,
        code: str,
        timeout: float = DEFAULT_TIMEOUT_SECONDS,
        handle: Optional[RunHandle] = None,
        stdin_text: Optional[str] = None,
    ) -> ExecutionResult:
        raise NotImplementedError("Java execution is coming soon.")
