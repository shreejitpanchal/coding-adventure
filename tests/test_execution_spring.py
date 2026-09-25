import shutil

import pytest

from app.engine.exercise import Exercise
from app.execution.spring_engine import SpringEngine

_TOOLCHAIN_PRESENT = shutil.which("mvn") is not None and shutil.which("java") is not None

_PROBE_CODE = "package com.codingadventure.exercise;\npublic class Probe { public int one() { return 1; } }\n"
_PROBE_TEST = (
    "package com.codingadventure.exercise;\n"
    "import org.junit.jupiter.api.Test;\n"
    "public class ProbeTest { @Test void ok() { new Probe().one(); } }\n"
)
_OFFLINE_MARKERS = ("Could not resolve", "No plugin found", "Cannot access central", "offline mode")


def _maven_repo_is_warm() -> bool:
    """SpringEngine runs `mvn -o` (offline); until every scaffold
    dependency and plugin is in the local repository each run fails with a
    resolution error. Probe by running the engine once on a trivial
    exercise: skip only when the failure is a resolution problem, so a
    genuine engine bug still surfaces as a test failure. Warm the
    repository once, with network access, via
    `mvn -f content/spring/scaffold/pom.xml dependency:go-offline`."""
    if not _TOOLCHAIN_PRESENT:
        return False
    from app.engine.exercise import Exercise
    probe_exercise = Exercise(
        id="probe", title="probe", language="spring", level=1, objective="x", explanation="x",
        expected_output_pattern="BUILD SUCCESS", spring_test_code=_PROBE_TEST,
    )
    result = SpringEngine().run(_PROBE_CODE, exercise=probe_exercise)
    if result.success:
        return True
    return not any(marker in result.stderr for marker in _OFFLINE_MARKERS)


pytestmark = pytest.mark.skipif(
    not _maven_repo_is_warm(),
    reason="requires a local Maven + JDK toolchain on PATH and a warmed ~/.m2 "
           "(run: mvn -f content/spring/scaffold/pom.xml dependency:go-offline)",
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
