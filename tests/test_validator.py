from app.engine.validator import diff_output, validate_contains, validate_output


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


def test_diff_output_calls_out_first_differing_line():
    result = diff_output("one\ntwo\nthree", "one\nTWO\nthree")
    assert "First difference at line 2." in result


def test_diff_output_makes_whitespace_visible():
    # A trailing space is otherwise invisible in a plain string comparison.
    result = diff_output("hello", "hello ")
    assert "·" in result  # the trailing space rendered as a visible dot
    assert "First difference at line 1." in result


def test_diff_output_reports_no_difference_line_when_lengths_only_differ_by_suffix():
    # Identical up through every existing line, but actual has an extra one.
    result = diff_output("one\ntwo", "one\ntwo\nthree")
    assert "First difference at line 3." in result
