import shutil

import pytest

from app.execution.cpp_engine import CppEngine

pytestmark = pytest.mark.skipif(
    shutil.which("g++") is None,
    reason="requires a local g++ toolchain on PATH",
)

engine = CppEngine()


def test_successful_run():
    code = '#include <iostream>\nint main() { std::cout << "hello" << std::endl; return 0; }'
    result = engine.run(code)
    assert result.success
    assert result.stdout.strip() == "hello"


def test_compile_error_surfaces_in_stderr():
    code = '#include <iostream>\nint main() { std::cout << "hi" << std::endl return 0; }'
    result = engine.run(code)
    assert not result.success
    assert not result.blocked
    assert "error" in result.stderr


def test_runtime_exception_surfaces_in_stderr():
    code = (
        "#include <vector>\n"
        "int main() { std::vector<int> v(1); return v.at(5); }"
    )
    result = engine.run(code)
    assert not result.success
    assert "out_of_range" in result.stderr


def test_timeout_on_infinite_loop():
    code = "int main() { while (true) {} return 0; }"
    result = engine.run(code, timeout=2.0)
    assert result.timed_out


def test_stdin_is_fed_to_cin():
    code = (
        "#include <iostream>\n#include <string>\n"
        "int main() { std::string name; std::getline(std::cin, name); "
        'std::cout << "hi " << name << std::endl; return 0; }'
    )
    result = engine.run(code, stdin_text="Ada\n")
    assert result.success
    assert result.stdout.strip() == "hi Ada"


def test_crash_gets_translated_note_when_stderr_empty():
    code = "int main() { int a = 5, b = 0; return a / b; }"
    result = engine.run(code)
    assert not result.success
    assert result.stderr.strip() != ""
