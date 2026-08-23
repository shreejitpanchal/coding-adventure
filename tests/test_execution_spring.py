import shutil

import pytest

from app.engine.exercise import Exercise
from app.execution.spring_engine import SpringEngine

pytestmark = pytest.mark.skipif(
    shutil.which("mvn") is None or shutil.which("java") is None,
    reason="requires a local Maven + JDK toolchain on PATH",
)

engine = SpringEngine()


def _exercise(starter_code: str, spring_test_code: str) -> Exercise:
    return Exercise(
        id="test", title="test", language="spring", level=1, objective="x", explanation="x",
        example_code="x", starter_code=starter_code, challenge="x",
        spring_test_code=spring_test_code,
    )


def test_successful_run():
    code = (
        "package com.codingadventure.exercise;\n"
        "import org.springframework.stereotype.Component;\n"
        "@Component\n"
        "public class Greeter {\n"
        "    public String greet(String name) { return \"hi \" + name; }\n"
        "}\n"
    )
    test_code = (
        "package com.codingadventure.exercise;\n"
        "import org.junit.jupiter.api.Test;\n"
        "import static org.assertj.core.api.Assertions.assertThat;\n"
        "public class GreeterTest {\n"
        "    @Test void greets() { assertThat(new Greeter().greet(\"Ada\")).isEqualTo(\"hi Ada\"); }\n"
        "}\n"
    )
    result = engine.run(code, exercise=_exercise(code, test_code))
    assert result.success
    assert result.stdout.strip() == "BUILD SUCCESS"


def test_compile_error_surfaces_in_stderr():
    code = (
        "package com.codingadventure.exercise;\n"
        "public class Greeter {\n"
        "    public String greet(String name) { return \"hi \" + name\n"
        "}\n"
    )
    test_code = (
        "package com.codingadventure.exercise;\n"
        "import org.junit.jupiter.api.Test;\n"
        "public class GreeterTest { @Test void x() {} }\n"
    )
    result = engine.run(code, exercise=_exercise(code, test_code))
    assert not result.success
    assert not result.blocked
    assert "COMPILATION ERROR" in result.stderr
    assert "AppData" not in result.stderr and "Users" not in result.stderr


def test_failing_assertion_surfaces_in_stderr():
    code = (
        "package com.codingadventure.exercise;\n"
        "import org.springframework.stereotype.Component;\n"
        "@Component\n"
        "public class Greeter {\n"
        "    public String greet(String name) { return \"hey \" + name; }\n"
        "}\n"
    )
    test_code = (
        "package com.codingadventure.exercise;\n"
        "import org.junit.jupiter.api.Test;\n"
        "import static org.assertj.core.api.Assertions.assertThat;\n"
        "public class GreeterTest {\n"
        "    @Test void greets() { assertThat(new Greeter().greet(\"Ada\")).isEqualTo(\"hi Ada\"); }\n"
        "}\n"
    )
    result = engine.run(code, exercise=_exercise(code, test_code))
    assert not result.success
    assert "AssertionFailedError" in result.stderr


def test_missing_test_definition_fails_cleanly():
    code = "package com.codingadventure.exercise;\npublic class Solution {}\n"
    result = engine.run(code, exercise=_exercise(code, ""))
    assert not result.success
    assert not result.blocked
