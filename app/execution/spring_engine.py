"""Spring execution engine: unlike the single-file engines, a Spring
exercise isn't one self-contained code string -- it's a class the user
edits plus a fixed JUnit test class that gates completion. Each run
scaffolds a temp Maven project (shared `content/spring/scaffold/pom.xml`
copied in, submitted code + the exercise's fixed test written under
`src/main`/`src/test`) and runs `mvn -o test` against it.

Uses plain Spring Framework (spring-context/spring-test), not Spring Boot
-- no embedded server, no autoconfiguration -- so `mvn test` stays fast
(a few seconds) and fully offline after the scaffold's dependencies are
warmed into the local `~/.m2` repository once. Maven's own logger writes
everything (including [ERROR] diagnostics) to stdout, never stderr, so
that's routed into ExecutionResult.stderr on failure to match the other
engines' contract (stdout is reserved for the synthetic "BUILD SUCCESS"
summary validate_output()/expected_output_pattern checks against)."""
from __future__ import annotations

import platform
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from app.config.paths import SPRING_SCAFFOLD_DIR
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

# mvn+Spring context startup needs more headroom than the other engines'
# 8s default -- ignores the `timeout` argument passed in and uses this
# instead, the same way cpp_engine's COMPILE_TIMEOUT_SECONDS is separate
# from the passed run timeout.
MVN_TIMEOUT_SECONDS = 45.0

_PACKAGE_PATH = Path("com") / "codingadventure" / "exercise"
# Windows needs the .cmd extension explicitly -- Popen can't launch a bare
# batch file the way a shell can.
_MVN_CMD = "mvn.cmd" if platform.system() == "Windows" else "mvn"


class SpringEngine(ExecutionEngine):
    language = "spring"

    def run(
        self,
        code: str,
        timeout: float = DEFAULT_TIMEOUT_SECONDS,
        handle: Optional[RunHandle] = None,
        stdin_text: Optional[str] = None,
        exercise: Optional["Exercise"] = None,
    ) -> ExecutionResult:
        status = check_toolchain("spring")
        if not status.available:
            return blocked_result("Spring", status)

        if exercise is None or not exercise.spring_test_code.strip():
            return ExecutionResult(success=False, stderr="This exercise is missing its Spring test definition.")

        with tempfile.TemporaryDirectory(prefix="codingadventure_spring_") as tmp_dir:
            tmp_path = Path(tmp_dir)
            (tmp_path / "pom.xml").write_text(
                (SPRING_SCAFFOLD_DIR / "pom.xml").read_text(encoding="utf-8"), encoding="utf-8",
            )

            main_dir = tmp_path / "src" / "main" / "java" / _PACKAGE_PATH
            test_dir = tmp_path / "src" / "test" / "java" / _PACKAGE_PATH
            main_dir.mkdir(parents=True)
            test_dir.mkdir(parents=True)

            main_class = detect_class_name(code, "Solution")
            test_class = detect_class_name(exercise.spring_test_code, "SolutionTest")
            (main_dir / f"{main_class}.java").write_text(code, encoding="utf-8")
            (test_dir / f"{test_class}.java").write_text(exercise.spring_test_code, encoding="utf-8")

            outcome = run_subprocess(
                [_MVN_CMD, "-q", "-o", "-Dstyle.color=never", "test"],
                tmp_dir, stdin_text=None, timeout=MVN_TIMEOUT_SECONDS, handle=handle, feed_stdin=False,
            )

            if outcome.timed_out:
                return ExecutionResult(success=False, timed_out=True)
            if outcome.returncode == 0:
                # Every Spring exercise's expected_output_pattern is just
                # "BUILD SUCCESS" -- a single deterministic value keeps
                # validate_output()'s re.fullmatch() simple, since the real
                # surefire summary (elapsed time, per-exercise class name)
                # varies run to run and exercise to exercise.
                return ExecutionResult(success=True, stdout="BUILD SUCCESS")
            output = _sanitize_path(outcome.stdout, tmp_dir)
            return ExecutionResult(success=False, stderr=output or "BUILD FAILURE")


def _sanitize_path(text: str, tmp_dir: str) -> str:
    """Maven reports absolute paths (both backslash and the forward-slash
    form it uses internally, e.g. /C:/Users/...) -- strip the temp dir
    prefix so no host path leaks into the UI, matching the other engines."""
    if not text:
        return text
    forward = tmp_dir.replace("\\", "/")
    text = text.replace(f"/{forward}/", "").replace(f"/{forward}", "")
    text = text.replace(f"{tmp_dir}\\", "").replace(tmp_dir, "")
    return text
