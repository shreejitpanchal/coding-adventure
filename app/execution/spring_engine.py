"""Spring execution engine -- interface defined, not yet implemented.

Spring exercises don't fit the single-file run-and-check-stdout shape the
other engines use -- a Spring Boot exercise needs a pre-scaffolded Maven
project per exercise, run via `mvn test` (parsing Surefire results) or by
starting the app and hitting an endpoint. That's a separate design pass,
not a variant of this engine's run() contract -- left unimplemented until
that pass happens. See app.execution.toolchain_check for the availability
gate the UI checks before ever calling into this."""
from __future__ import annotations

from typing import Optional

from app.execution.base import DEFAULT_TIMEOUT_SECONDS, ExecutionEngine, ExecutionResult, RunHandle


class SpringEngine(ExecutionEngine):
    language = "spring"

    def run(
        self,
        code: str,
        timeout: float = DEFAULT_TIMEOUT_SECONDS,
        handle: Optional[RunHandle] = None,
        stdin_text: Optional[str] = None,
    ) -> ExecutionResult:
        raise NotImplementedError("Spring execution is coming soon.")
