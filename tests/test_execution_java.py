import shutil

import pytest

from app.execution.java_engine import JavaEngine

pytestmark = pytest.mark.skipif(
    shutil.which("javac") is None or shutil.which("java") is None,
    reason="requires a local JDK (javac/java) on PATH",
)

engine = JavaEngine()


def test_successful_run():
    code = 'public class Solution { public static void main(String[] args) { System.out.println("hello"); } }'
    result = engine.run(code)
    assert result.success
    assert result.stdout.strip() == "hello"


def test_compile_error_surfaces_in_stderr():
    code = 'public class Solution { public static void main(String[] args) { System.out.println("hi") } }'
    result = engine.run(code)
    assert not result.success
    assert not result.blocked
    assert "error" in result.stderr


def test_runtime_exception_surfaces_in_stderr():
    code = (
        "public class Solution { public static void main(String[] args) { "
        "int[] a = new int[1]; System.out.println(a[5]); } }"
    )
    result = engine.run(code)
    assert not result.success
    assert "ArrayIndexOutOfBoundsException" in result.stderr


def test_timeout_on_infinite_loop():
    code = "public class Solution { public static void main(String[] args) { while (true) {} } }"
    result = engine.run(code, timeout=2.0)
    assert result.timed_out


def test_stdin_is_fed_to_scanner():
    code = (
        "import java.util.Scanner;"
        "public class Solution { public static void main(String[] args) { "
        "Scanner sc = new Scanner(System.in); String name = sc.nextLine(); "
        'System.out.println("hi " + name); } }'
    )
    result = engine.run(code, stdin_text="Ada\n")
    assert result.success
    assert result.stdout.strip() == "hi Ada"


def test_class_name_detected_from_source():
    code = 'public class Greeter { public static void main(String[] args) { System.out.println("ok"); } }'
    result = engine.run(code)
    assert result.success
    assert result.stdout.strip() == "ok"
