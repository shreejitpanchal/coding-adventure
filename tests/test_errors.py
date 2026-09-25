"""app/execution/errors.py -- the regexes that turn raw toolchain output
into a one-line explanation and a line number. Each language gets one
representative sample per branch."""
from app.execution.errors import (
    DEFAULT_MESSAGE,
    extract_error_line_number,
    translate_error,
)

PY_TRACEBACK = (
    'Traceback (most recent call last):\n'
    '  File "<exercise>", line 3, in <module>\n'
    '    print(1 / 0)\n'
    'ZeroDivisionError: division by zero\n'
)

JAVA_COMPILE = "Solution.java:4: error: ';' expected\n        System.out.println(\"hi\")\n"
JAVA_RUNTIME = (
    'Exception in thread "main" java.lang.ArrayIndexOutOfBoundsException: Index 5 out of bounds for length 1\n'
    "\tat Solution.main(Solution.java:2)\n"
)

CPP_COMPILE = "main.cpp:3:5: error: expected ';' before 'return'\n"
CPP_THROW = "terminate called after throwing an instance of 'std::out_of_range'\n  what():  vector::_M_range_check\n"
CPP_JOINABLE = "terminate called without an active exception\n"
CPP_CRASH = "[process exited with code 0xc0000005: STATUS_ACCESS_VIOLATION -- invalid memory access (null or dangling pointer, out-of-bounds access)]"

SPRING_COMPILE = "[ERROR] COMPILATION ERROR :\n[ERROR] Greeter.java:[3,45] ';' expected\n"
SPRING_ASSERT = (
    "org.opentest4j.AssertionFailedError: \nexpected: \"hi Ada\"\n but was: \"hey Ada\"\n"
    "\tat GreeterTest.greets(GreeterTest.java:7)\n"
    "\tat java.base/java.util.ArrayList.forEach(ArrayList.java:1596)\n"
)
SPRING_DI = "Caused by: org.springframework.beans.factory.NoSuchBeanDefinitionException: No qualifying bean\n"

NODE_ERROR = (
    "<exercise>:2\n"
    "console.log(undefinedThing);\n"
    "            ^\n\n"
    "ReferenceError: undefinedThing is not defined\n"
    "    at Object.<anonymous> (<exercise>:2:13)\n"
)
NODE_ASSERT = (
    "node:assert:124\n  throw new AssertionError(obj);\n"
    "AssertionError [ERR_ASSERTION]: Expected values to be strictly equal\n"
    "    at Object.<anonymous> (<exercise>:5:8)\n"
)


def test_python_and_ai_share_translation():
    assert translate_error(PY_TRACEBACK, "python")[0] == "Division by zero."
    assert translate_error(PY_TRACEBACK, "ai") == translate_error(PY_TRACEBACK, "python")
    assert extract_error_line_number(PY_TRACEBACK, "python") == 3


def test_python_unknown_exception_falls_back():
    message, _ = translate_error("SomethingWeird: boom", "python")
    assert message == DEFAULT_MESSAGE


def test_java_compile_vs_runtime():
    assert translate_error(JAVA_COMPILE, "java")[0] == "Compile error."
    assert extract_error_line_number(JAVA_COMPILE, "java") == 4
    assert translate_error(JAVA_RUNTIME, "java")[0] == "Array index out of range."
    assert extract_error_line_number(JAVA_RUNTIME, "java") == 2


def test_cpp_branches_in_priority_order():
    assert translate_error(CPP_COMPILE, "cpp")[0] == "Compile error."
    assert extract_error_line_number(CPP_COMPILE, "cpp") == 3
    message, _ = translate_error(CPP_THROW, "cpp")
    assert message.startswith("Out-of-range access.")
    assert "vector::_M_range_check" in message
    assert "std::terminate()" in translate_error(CPP_JOINABLE, "cpp")[0]
    message, hint = translate_error(CPP_CRASH, "cpp")
    assert message == "STATUS_ACCESS_VIOLATION."
    assert hint.startswith("Invalid memory access")


def test_spring_branches_and_first_frame_line_number():
    assert translate_error(SPRING_COMPILE, "spring")[0] == "Compile error."
    message, _ = translate_error(SPRING_ASSERT, "spring")
    assert message == 'Test assertion failed -- expected "hi Ada", but was "hey Ada".'
    # First .java:N match is the test file, not the JDK-internal ArrayList frame.
    assert extract_error_line_number(SPRING_ASSERT, "spring") == 7
    assert translate_error(SPRING_DI, "spring")[0] == "No matching bean found."
    assert translate_error("BUILD FAILURE", "spring") == ("Test failed.", "Check the raw output below for details.")


def test_node_header_line_and_bracketed_error_code():
    assert translate_error(NODE_ERROR, "node")[0] == "Undefined reference."
    assert extract_error_line_number(NODE_ERROR, "node") == 2
    assert translate_error(NODE_ASSERT, "node")[0] == "Assertion failed."
    # No "<exercise>:N" header (throw originates in node:assert) -> first stack frame.
    assert extract_error_line_number(NODE_ASSERT, "node") == 5


def test_unknown_language_falls_back_cleanly():
    assert translate_error("anything", "cobol")[0] == DEFAULT_MESSAGE
    assert extract_error_line_number("no frames here", "cobol") is None
