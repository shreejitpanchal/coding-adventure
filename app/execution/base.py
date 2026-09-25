"""Shared execution contract every per-language engine implements.

Framing is crash-containment, not child safety: exercises run the user's
own code, on their own machine, deliberately -- there's no adversarial
threat model to defend against the way the kids' version of this app had
to. A timeout and subprocess isolation exist so a runaway loop can't hang
the app, not to sandbox against malice.

Besides the ABC, this module holds the two helpers every subprocess-based
engine shares so they aren't copy-pasted per language: `run_subprocess()`
(Popen + stdin feed + timeout + RunHandle cancellation, one implementation)
and `blocked_result()` (the "toolchain missing" ExecutionResult).
"""
from __future__ import annotations

import logging
import os
import signal
import subprocess
import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, Sequence

if TYPE_CHECKING:
    from app.engine.exercise import Exercise
    from app.execution.toolchain_check import ToolchainStatus
    from app.execution.watchdog import Watchdog

logger = logging.getLogger(__name__)

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
    (attached with `attach`). PythonInProcessEngine runs in-process instead
    (needed on Android, which won't let a non-rooted app spawn a sibling OS
    process) and has no subprocess to kill, so it attaches a Watchdog
    (`attach_watchdog`) instead -- cancel() signals whichever one is
    actually in use. A single RunHandle only ever has one or the other
    attached, never both, since a given run only ever goes through one
    engine."""

    def __init__(self) -> None:
        self._process: Optional[subprocess.Popen] = None
        self._watchdog: Optional["Watchdog"] = None
        self._lock = threading.Lock()
        self.cancelled = False

    def attach(self, process: subprocess.Popen) -> None:
        with self._lock:
            self._process = process
            if self.cancelled:
                process.kill()

    def attach_watchdog(self, watchdog: "Watchdog") -> None:
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


@dataclass
class SubprocessOutcome:
    """What run_subprocess() hands back: either the process finished
    (returncode/stdout/stderr populated) or it was stopped early
    (timed_out -- which also covers a RunHandle cancellation, since the
    UI treats both the same way)."""
    returncode: int = 0
    stdout: str = ""
    stderr: str = ""
    timed_out: bool = False


def run_subprocess(
    args: Sequence[str],
    cwd: str,
    stdin_text: Optional[str],
    timeout: float,
    handle: Optional[RunHandle] = None,
    feed_stdin: bool = True,
) -> SubprocessOutcome:
    """Run `args` to completion under the shared contract:

    - stdin is always fed and closed (even as "") when `feed_stdin` is
      True, so a stray input()/Scanner/readline fails fast with EOF
      instead of hanging until the timeout;
    - the process is killed and reported as timed_out when `timeout`
      elapses, or when `handle.cancel()` is called mid-run;
    - text mode, stdout/stderr captured separately.
    """
    process = subprocess.Popen(
        list(args),
        stdin=subprocess.PIPE if feed_stdin else None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=cwd,
        # Own process group on POSIX so a timeout can kill the whole tree.
        start_new_session=(os.name != "nt"),
    )
    if handle is not None:
        handle.attach(process)
    try:
        stdout, stderr = process.communicate(
            input=(stdin_text or "") if feed_stdin else None, timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        _kill_and_release(process)
        logger.info("Subprocess %s timed out after %.1fs", args[0], timeout)
        return SubprocessOutcome(timed_out=True)

    if handle is not None and handle.cancelled:
        return SubprocessOutcome(timed_out=True)

    return SubprocessOutcome(returncode=process.returncode, stdout=stdout or "", stderr=stderr or "")


def _kill_and_release(process: subprocess.Popen) -> None:
    """Stop a timed-out child -- and its whole process tree -- then drain.

    `Popen.kill()` only terminates the direct child. The Windows `java.exe`
    launcher re-executes itself as a grandchild that inherits our pipe
    handles, so after a plain kill() the pipes never reach EOF and the
    documented "kill(); communicate()" pattern blocks forever. Killing the
    tree (taskkill /T on Windows, the process group elsewhere) closes every
    handle, after which communicate() completes immediately."""
    if os.name == "nt":
        subprocess.run(
            ["taskkill", "/T", "/F", "/PID", str(process.pid)],
            capture_output=True, timeout=10,
        )
    else:
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGKILL)
        except Exception:
            process.kill()
    try:
        process.communicate(timeout=5)
    except subprocess.TimeoutExpired:
        logger.warning("Subprocess %s still holding pipes 5s after kill; abandoning it", process.args)
        for stream in (process.stdout, process.stderr):
            if stream is not None:
                try:
                    stream.close()
                except Exception:
                    pass


def blocked_result(label: str, status: "ToolchainStatus") -> ExecutionResult:
    """The ExecutionResult every engine returns when its toolchain is
    missing -- one wording, one place."""
    return ExecutionResult(
        success=False, blocked=True,
        blocked_message=f"{label} toolchain not found (missing: {', '.join(status.missing)}). {status.install_hint}",
    )


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
