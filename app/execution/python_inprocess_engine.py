"""In-process Python execution engine, used specifically on Android in
place of PythonEngine (app/execution/python_engine.py) -- a non-rooted
Android app can't spawn a sibling OS process the way subprocess.Popen
does on desktop/web, so submitted code is exec()'d in this same process
instead, with an AST-injected cooperative watchdog
(app/execution/watchdog.py) standing in for the OS-level
`process.kill()` that handles a runaway loop everywhere else.

Deliberately does NOT restrict builtins or imports the way
python-adventure-kids' equivalent (app/sandbox/inprocess_runner.py in
that sibling repo) does -- this app's whole execution model is "run the
user's own code on their own device, on purpose" (see base.py's
docstring), the same trust model PythonEngine already uses; only the
*mechanism* needed porting for Android, not a kid-safety sandbox this
app never had in the first place. Any exception type (including
BaseException subclasses like SystemExit) is still caught and reported
as a normal execution result rather than allowed to propagate into the
host app, though -- unlike a subprocess, there's no OS-level isolation
backstopping an uncaught exception here.
"""
from __future__ import annotations

import contextlib
import io
import threading
import traceback
from typing import TYPE_CHECKING, Optional

from app.execution.base import DEFAULT_TIMEOUT_SECONDS, ExecutionEngine, ExecutionResult, RunHandle
from app.execution.watchdog import TICK_FUNC_NAME, Watchdog, WatchdogTimeout, compile_with_watchdog

if TYPE_CHECKING:
    from app.engine.exercise import Exercise

CODE_FILENAME = "<exercise>"

# contextlib.redirect_stdout mutates process-global state (sys.stdout), so
# only one in-process run can be in flight at a time -- enforced here as a
# defensive invariant. In practice this is never contended: the lesson
# screen already disables the Run button while a run is in progress, so
# there's only ever one caller at a time regardless.
_run_lock = threading.Lock()


def _split_stdin(stdin_text: Optional[str]) -> list[str]:
    """Mirrors how a real stdin pipe behaves: a trailing newline marks the
    end of the last line, it doesn't introduce a phantom empty one after
    it. "Ada\\n" -> one answer ("Ada"), not two."""
    answers = (stdin_text or "").split("\n")
    if answers and answers[-1] == "":
        answers.pop()
    return answers


def _make_input(answers: list[str], out: io.StringIO):
    def _input(prompt: str = "") -> str:
        if prompt:
            out.write(str(prompt))
        if not answers:
            raise EOFError()
        return answers.pop(0)

    return _input


class PythonInProcessEngine(ExecutionEngine):
    """Same ExecutionResult/RunHandle contract as PythonEngine, but runs
    code in-process via exec() instead of spawning `python -I` as a
    subprocess -- see this module's docstring for why."""

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
            compiled = compile_with_watchdog(code, filename=CODE_FILENAME)
        except SyntaxError as exc:
            code_line = (exc.text or "").rstrip("\n")
            stderr = f'  File "{CODE_FILENAME}", line {exc.lineno}\n    {code_line}\nSyntaxError: {exc.msg}\n'
            return ExecutionResult(success=False, stderr=stderr)

        with _run_lock:
            watchdog = Watchdog(timeout)
            if handle is not None:
                handle._attach_watchdog(watchdog)

            out = io.StringIO()
            exec_globals: dict = {
                "__name__": "__main__",
                TICK_FUNC_NAME: watchdog.tick,
                "input": _make_input(_split_stdin(stdin_text), out),
            }

            try:
                with contextlib.redirect_stdout(out):
                    exec(compiled, exec_globals)
            except WatchdogTimeout:
                return ExecutionResult(success=False, timed_out=True, stdout=out.getvalue())
            except SystemExit as exc:
                code_arg = exc.code
                exit_code = 0 if code_arg is None else (code_arg if isinstance(code_arg, int) else 1)
                if exit_code == 0:
                    return ExecutionResult(success=True, stdout=out.getvalue())
                return ExecutionResult(success=False, stdout=out.getvalue(), stderr=f"SystemExit: {code_arg}\n")
            except BaseException as exc:
                # exc.__traceback__'s first frame is this method's own
                # `exec(compiled, exec_globals)` call site, not anything
                # from the submitted code -- a real subprocess never shows
                # that (the child process boundary hides it entirely), so
                # skip it here too rather than leaking this engine's own
                # internals into a user-facing traceback.
                tb = exc.__traceback__
                if tb is not None:
                    tb = tb.tb_next
                formatted = "".join(traceback.format_exception(type(exc), exc, tb))
                return ExecutionResult(success=False, stdout=out.getvalue(), stderr=formatted)

        if handle is not None and handle.cancelled:
            return ExecutionResult(success=False, timed_out=True, stdout=out.getvalue())

        return ExecutionResult(success=True, stdout=out.getvalue())
