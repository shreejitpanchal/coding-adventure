"""Same behavioral contract as test_execution_python.py (PythonEngine),
run against PythonInProcessEngine instead -- this is the engine actually
used on Android (see registry.py), but it runs identically on desktop
too, which is how it's verified here: there's no Android device in CI,
so exercising the exact same in-process code path on desktop is the only
way to confirm it behaves the same as the subprocess-based engine before
it ever reaches a real device."""
from app.execution.base import RunHandle
from app.execution.python_inprocess_engine import PythonInProcessEngine

engine = PythonInProcessEngine()


def test_successful_run():
    result = engine.run("print('hello')")
    assert result.success
    assert result.stdout.strip() == "hello"


def test_syntax_error_caught_before_exec():
    result = engine.run("def f(:\n    pass")
    assert not result.success
    assert not result.blocked
    assert "SyntaxError" in result.stderr


def test_runtime_error_surfaces_in_stderr():
    result = engine.run("1 / 0")
    assert not result.success
    assert "ZeroDivisionError" in result.stderr


def test_timeout_on_infinite_loop():
    result = engine.run("while True:\n    pass", timeout=1.0)
    assert result.timed_out


def test_cancel_stops_an_in_progress_loop():
    handle = RunHandle()
    handle.cancel()  # cancelled before the watchdog is even attached
    result = engine.run("while True:\n    pass", timeout=10.0, handle=handle)
    assert result.timed_out


def test_stdin_is_fed_to_input():
    result = engine.run("name = input()\nprint(f'hi {name}')", stdin_text="Ada\n")
    assert result.success
    assert result.stdout.strip() == "hi Ada"


def test_missing_stdin_fails_fast_with_eof():
    result = engine.run("input()", timeout=3.0)
    assert not result.success
    assert "EOFError" in result.stderr


def test_output_partially_captured_before_timeout():
    result = engine.run("print('before')\nwhile True:\n    pass", timeout=1.0)
    assert result.timed_out
    assert "before" in result.stdout


def test_sys_exit_zero_is_success():
    result = engine.run("import sys\nprint('done')\nsys.exit(0)")
    assert result.success
    assert result.stdout.strip() == "done"


def test_sys_exit_nonzero_is_failure():
    result = engine.run("import sys\nsys.exit(1)")
    assert not result.success


def test_full_stdlib_access_not_restricted():
    # Unlike the kids app's inprocess sandbox, this one has no import
    # allowlist -- arbitrary stdlib modules must work, same as PythonEngine.
    result = engine.run("import json\nprint(json.dumps({'a': 1}))")
    assert result.success
    assert result.stdout.strip() == '{"a": 1}'


def test_line_numbers_survive_loop_injection():
    code = "x = 1\nfor i in range(3):\n    pass\nraise ValueError('boom')"
    result = engine.run(code)
    assert not result.success
    assert 'File "<exercise>", line 4' in result.stderr
