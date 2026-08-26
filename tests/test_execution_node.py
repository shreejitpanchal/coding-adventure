import shutil

import pytest

from app.execution.node_engine import NodeEngine

pytestmark = pytest.mark.skipif(
    shutil.which("node") is None,
    reason="requires a local Node.js toolchain on PATH",
)

engine = NodeEngine()


def test_successful_run():
    code = 'console.log("hello");'
    result = engine.run(code)
    assert result.success
    assert result.stdout.strip() == "hello"


def test_syntax_error_surfaces_in_stderr():
    code = "function bad() {\n  let x = ;\n}"
    result = engine.run(code)
    assert not result.success
    assert not result.blocked
    assert "SyntaxError" in result.stderr


def test_runtime_exception_surfaces_in_stderr():
    code = "null.foo();"
    result = engine.run(code)
    assert not result.success
    assert "TypeError" in result.stderr


def test_timeout_on_infinite_loop():
    code = "while (true) {}"
    result = engine.run(code, timeout=2.0)
    assert result.timed_out


def test_stdin_is_fed_via_readline():
    code = (
        "const readline = require('readline');\n"
        "const rl = readline.createInterface({ input: process.stdin });\n"
        "rl.on('line', (line) => { console.log(`hi ${line}`); rl.close(); });\n"
    )
    result = engine.run(code, stdin_text="Ada\n")
    assert result.success
    assert result.stdout.strip() == "hi Ada"
