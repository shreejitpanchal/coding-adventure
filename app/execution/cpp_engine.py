"""C++ execution engine -- interface defined, not yet implemented.

Planned shape: write the submitted code to a temp dir as main.cpp, compile
with `g++ -O2 -std=c++17 main.cpp -o main` (compile diagnostics surface the
same way a failed run does today), then run the resulting binary with the
same timeout/RunHandle/stdin contract as
app.execution.python_engine.PythonEngine. Left unimplemented until the C++
content track is built out -- see app.execution.toolchain_check for the
availability gate the UI checks before ever calling into this."""
from __future__ import annotations

from typing import Optional

from app.execution.base import DEFAULT_TIMEOUT_SECONDS, ExecutionEngine, ExecutionResult, RunHandle


class CppEngine(ExecutionEngine):
    language = "cpp"

    def run(
        self,
        code: str,
        timeout: float = DEFAULT_TIMEOUT_SECONDS,
        handle: Optional[RunHandle] = None,
        stdin_text: Optional[str] = None,
    ) -> ExecutionResult:
        raise NotImplementedError("C++ execution is coming soon.")
