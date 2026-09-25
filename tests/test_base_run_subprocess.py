"""The shared subprocess helper every engine is built on."""
import sys
import threading
import time

from app.execution.base import RunHandle, run_subprocess


def _py(code: str) -> list[str]:
    return [sys.executable, "-c", code]


def test_captures_stdout_stderr_and_returncode(tmp_path):
    outcome = run_subprocess(
        _py("import sys; print('out'); print('err', file=sys.stderr); sys.exit(3)"),
        str(tmp_path), stdin_text=None, timeout=10,
    )
    assert not outcome.timed_out
    assert outcome.returncode == 3
    assert outcome.stdout.strip() == "out"
    assert outcome.stderr.strip() == "err"


def test_stdin_is_fed_and_closed(tmp_path):
    outcome = run_subprocess(_py("print(input().upper())"), str(tmp_path), "ada\n", timeout=10)
    assert outcome.stdout.strip() == "ADA"
    # No stdin text still closes the pipe, so input() fails fast with EOF.
    outcome = run_subprocess(_py("input()"), str(tmp_path), None, timeout=10)
    assert outcome.returncode != 0
    assert "EOFError" in outcome.stderr


def test_timeout_kills_the_process(tmp_path):
    start = time.monotonic()
    outcome = run_subprocess(_py("while True: pass"), str(tmp_path), None, timeout=1.0)
    assert outcome.timed_out
    assert time.monotonic() - start < 8


def test_cancel_via_handle_reports_timed_out(tmp_path):
    handle = RunHandle()
    threading.Timer(0.5, handle.cancel).start()
    outcome = run_subprocess(_py("while True: pass"), str(tmp_path), None, timeout=30, handle=handle)
    assert outcome.timed_out
    assert handle.cancelled


def test_cancel_before_attach_kills_immediately(tmp_path):
    handle = RunHandle()
    handle.cancel()
    outcome = run_subprocess(_py("while True: pass"), str(tmp_path), None, timeout=30, handle=handle)
    assert outcome.timed_out
