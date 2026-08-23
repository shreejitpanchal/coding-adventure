"""C++ execution engine: compiles the submitted code with `g++`, then runs
the resulting binary under the same timeout/RunHandle/stdin contract as
python_engine.PythonEngine."""
from __future__ import annotations

import platform
import subprocess
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from app.execution.base import DEFAULT_TIMEOUT_SECONDS, ExecutionEngine, ExecutionResult, RunHandle
from app.execution.toolchain_check import check_toolchain

if TYPE_CHECKING:
    from app.engine.exercise import Exercise

COMPILE_TIMEOUT_SECONDS = 20.0
_EXE_NAME = "main.exe" if platform.system() == "Windows" else "main"

# A crashed C++ program (segfault, div-by-zero, stack overflow, ...) usually
# prints nothing useful to stderr on its own -- the OS just reports an exit
# code. These are the common Windows NTSTATUS crash codes and POSIX signal
# numbers (negative returncode = killed by signal N), translated into a
# synthetic stderr line so app.execution.errors.translate_error has
# something to work with either way.
_WINDOWS_CRASH_CODES: dict[int, str] = {
    0xC0000005: "STATUS_ACCESS_VIOLATION -- invalid memory access (null or dangling pointer, out-of-bounds access)",
    0xC000001D: "STATUS_ILLEGAL_INSTRUCTION -- often an integer division by zero",
    0xC0000094: "STATUS_INTEGER_DIVIDE_BY_ZERO",
    0xC00000FD: "STATUS_STACK_OVERFLOW -- likely infinite or too-deep recursion",
    0xC0000409: "STATUS_STACK_BUFFER_OVERRUN / abort() -- often an uncaught C++ exception",
}
_POSIX_SIGNALS: dict[int, str] = {
    11: "SIGSEGV -- invalid memory access (null or dangling pointer, out-of-bounds access)",
    8: "SIGFPE -- often an integer division by zero",
    6: "SIGABRT -- often an uncaught C++ exception or a failed assertion",
    4: "SIGILL -- illegal instruction",
}


def _describe_crash(returncode: int) -> str:
    if returncode < 0:
        desc = _POSIX_SIGNALS.get(-returncode)
        return f"[process terminated by signal {-returncode}{f': {desc}' if desc else ''}]"
    unsigned = returncode & 0xFFFFFFFF
    desc = _WINDOWS_CRASH_CODES.get(unsigned)
    if desc:
        return f"[process exited with code {hex(unsigned)}: {desc}]"
    return ""


class CppEngine(ExecutionEngine):
    language = "cpp"

    def run(
        self,
        code: str,
        timeout: float = DEFAULT_TIMEOUT_SECONDS,
        handle: Optional[RunHandle] = None,
        stdin_text: Optional[str] = None,
        exercise: Optional["Exercise"] = None,
    ) -> ExecutionResult:
        status = check_toolchain("cpp")
        if not status.available:
            return ExecutionResult(
                success=False, blocked=True,
                blocked_message=f"C++ toolchain not found (missing: {', '.join(status.missing)}). {status.install_hint}",
            )

        with tempfile.TemporaryDirectory(prefix="codingadventure_cpp_") as tmp_dir:
            source_file = Path(tmp_dir) / "main.cpp"
            source_file.write_text(code, encoding="utf-8")

            try:
                compile_result = subprocess.run(
                    ["g++", "-O2", "-std=c++17", source_file.name, "-o", _EXE_NAME],
                    cwd=tmp_dir, capture_output=True, text=True, timeout=COMPILE_TIMEOUT_SECONDS,
                )
            except subprocess.TimeoutExpired:
                return ExecutionResult(success=False, timed_out=True)

            if compile_result.returncode != 0:
                return ExecutionResult(success=False, stderr=compile_result.stderr)

            process = subprocess.Popen(
                [str(Path(tmp_dir) / _EXE_NAME)],
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

        success = process.returncode == 0
        if not success and not stderr.strip():
            crash_note = _describe_crash(process.returncode)
            if crash_note:
                stderr = crash_note

        return ExecutionResult(success=success, stdout=stdout, stderr=stderr)
