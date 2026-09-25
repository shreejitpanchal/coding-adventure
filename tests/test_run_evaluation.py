from app.engine.exercise import Exercise
from app.engine.run_evaluation import Verdict, evaluate_run
from app.execution.base import ExecutionResult


def _exercise(**overrides) -> Exercise:
    base = dict(
        id="ex", title="t", language="python", level=1, objective="o", explanation="e",
        expected_output="hello",
    )
    base.update(overrides)
    return Exercise(**base)


def test_blocked_toolchain():
    outcome = evaluate_run(ExecutionResult(False, blocked=True, blocked_message="no javac"), _exercise(), "", None)
    assert outcome.verdict is Verdict.BLOCKED
    assert outcome.message == "no javac"
    assert outcome.event_type is None  # environment problem, not the user's attempt


def test_timeout():
    outcome = evaluate_run(ExecutionResult(False, timed_out=True), _exercise(), "", None)
    assert outcome.verdict is Verdict.TIMED_OUT
    assert outcome.event_type == "attempt_timeout"


def test_runtime_error_is_translated_with_line_number():
    stderr = 'Traceback:\n  File "<exercise>", line 7, in <module>\nNameError: name x\n'
    outcome = evaluate_run(ExecutionResult(False, stderr=stderr), _exercise(), "", None)
    assert outcome.verdict is Verdict.ERROR
    assert "Undefined name. (line 7)" in outcome.message
    assert outcome.raw == stderr
    assert outcome.event_type == "attempt_error"
    assert outcome.event_detail.endswith("NameError: name x\n")


def test_pass():
    outcome = evaluate_run(ExecutionResult(True, stdout="hello\n"), _exercise(), "print('hello')", None)
    assert outcome.passed
    assert outcome.message == "hello\n"
    assert outcome.event_type is None


def test_pass_with_input_placeholder():
    ex = _exercise(expected_output="Hi, {input}!")
    outcome = evaluate_run(ExecutionResult(True, stdout="Hi, Sam!\n"), ex, "", "Sam")
    assert outcome.passed


def test_right_output_but_missing_required_pattern():
    ex = _exercise(contains_patterns=[r"sorted\("])
    outcome = evaluate_run(ExecutionResult(True, stdout="hello"), ex, "print('hello')", None)
    assert outcome.verdict is Verdict.MISSING_PATTERNS
    assert "actually teaching" in outcome.message
    assert outcome.event_type is None  # not counted as a failed attempt


def test_wrong_output_gets_a_diff_with_input_substituted():
    ex = _exercise(expected_output="Hi, {input}!")
    outcome = evaluate_run(ExecutionResult(True, stdout="Hi Sam!"), ex, "", "Sam")
    assert outcome.verdict is Verdict.WRONG_OUTPUT
    assert outcome.details_label == "Show expected vs. actual"
    assert "Hi,·Sam!" in outcome.raw  # expected line rendered with visible spaces
    assert outcome.event_type == "attempt_wrong_output"


def test_wrong_output_against_pattern_has_no_diff():
    ex = _exercise(expected_output="", expected_output_pattern=r"\d+")
    outcome = evaluate_run(ExecutionResult(True, stdout="abc"), ex, "", None)
    assert outcome.verdict is Verdict.WRONG_OUTPUT
    assert outcome.raw is None


def test_empty_stdout_is_labelled():
    outcome = evaluate_run(ExecutionResult(True, stdout=""), _exercise(), "", None)
    assert outcome.message.startswith("(no output)")
