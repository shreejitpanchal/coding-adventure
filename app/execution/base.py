"""Shared execution contract every per-language engine implements.

Framing is crash-containment, not child safety: exercises run the user's
own code, on their own machine, deliberately -- there's no adversarial
threat model to defend against the way the kids' version of this app had
to. A timeout and subprocess isolation exist so a runaway loop can't hang
the app, not to sandbox against malice.
"""
from __future__ import annotations

import subprocess
import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.engine.exercise import Exercise
    from app.execution.watchdog import Watchdog

DEFAULT_TIMEOUT_SECONDS = 8.0


@dataclass
class ExecutionResult:
    success: bool
    stdout: str = ""
    stderr: str = ""
    timed_out: bool = False
    blocked: bool = False
    blocked_message: str = ""
    """Set when the toolchain itself (compiler/interpreter) isn't available
    on this machine -- see app.execution.toolchain_check. Distinct from a
    compile error, which is a normal, expected failure surfaced via stderr."""


class RunHandle:
    """Lets the UI cancel a run that's in progress (e.g. an infinite loop).

    Every engine but PythonInProcessEngine cancels via subprocess.Popen.kill()
    (attached with `_attach`). PythonInProcessEngine runs in-process instead
    (needed on Android, which won't let a non-rooted app spawn a sibling OS
    process) and has no subprocess to kill, so it attaches a Watchdog
    (`_attach_watchdog`) instead -- cancel() signals whichever one is
    actually in use. A single RunHandle only ever has one or the other
    attached, never both, since a given run only ever goes through one
    engine."""

    def __init__(self) -> None:
        self._process: Optional[subprocess.Popen] = None
        self._watchdog: Optional["Watchdog"] = None
        self._lock = threading.Lock()
        self.cancelled = False

    def _attach(self, process: subprocess.Popen) -> None:
        with self._lock:
            self._process = process
            if self.cancelled:
                process.kill()

    def _attach_watchdog(self, watchdog: "Watchdog") -> None:
        with self._lock:
            self._watchdog = watchdog
            if self.cancelled:
                watchdog.cancel()

    def cancel(self) -> None:
        with self._lock:
            self.cancelled = True
            if self._process is not None:
                self._process.kill()
            if self._watchdog is not None:
                self._watchdog.cancel()


class ExecutionEngine(ABC):
    """One concrete subclass per language track (python_engine.PythonEngine,
    java_engine.JavaEngine, ...)."""

    language: str

    @abstractmethod
    def run(
        self,
        code: str,
        timeout: float = DEFAULT_TIMEOUT_SECONDS,
        handle: Optional[RunHandle] = None,
        stdin_text: Optional[str] = None,
        exercise: Optional["Exercise"] = None,
    ) -> ExecutionResult:
        """exercise is unused by the single-file engines (Python/Java/C++) --
        SpringEngine needs it to look up the exercise's fixed test source
        and scaffold a Maven project, since a Spring exercise isn't a single
        self-contained code string the way the others are."""
        raise NotImplementedError
