from app.execution.python_engine import PythonEngine

engine = PythonEngine()


def test_successful_run():
    result = engine.run("print('hello')")
    assert result.success
    assert result.stdout.strip() == "hello"


def test_syntax_error_caught_before_subprocess():
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


def test_stdin_is_fed_to_input():
    result = engine.run("name = input()\nprint(f'hi {name}')", stdin_text="Ada\n")
    assert result.success
    assert result.stdout.strip() == "hi Ada"


def test_missing_stdin_fails_fast_with_eof():
    result = engine.run("input()", timeout=3.0)
    assert not result.success
    assert "EOFError" in result.stderr
