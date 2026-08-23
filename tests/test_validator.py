from app.engine.validator import validate_contains, validate_output


def test_validate_output_exact_match():
    assert validate_output("hello\n", "hello")
    assert not validate_output("goodbye\n", "hello")


def test_validate_output_input_placeholder():
    assert validate_output("Hi, Sam!\n", "Hi, {input}!", input_value="Sam")


def test_validate_output_pattern():
    assert validate_output("42\n", expected_output_pattern=r"\d+")
    assert not validate_output("abc\n", expected_output_pattern=r"\d+")


def test_validate_contains_empty_patterns_always_true():
    assert validate_contains("print(1)", [])


def test_validate_contains_requires_all_patterns():
    code = "def f():\n    return sorted(x)\n"
    assert validate_contains(code, ["sorted\\("])
    assert not validate_contains(code, ["reversed\\("])
