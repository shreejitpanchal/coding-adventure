"""Turns an ExecutionResult into a user-facing verdict, with no UI in it.

The lesson screen used to hold this decision tree inline in its
run-complete handler, which made the single most important piece of
logic in the app -- "did the user pass?" -- untestable without a Flet
Page. It now lives here as a pure function; lesson_screen.py only
renders the RunOutcome it gets back."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from app.engine.exercise import Exercise
from app.engine.validator import INPUT_PLACEHOLDER, diff_output, validate_contains, validate_output
from app.execution.base import ExecutionResult
from app.execution.errors import extract_error_line_number, translate_error


class Verdict(str, Enum):
    BLOCKED = "blocked"
    TIMED_OUT = "timed_out"
    ERROR = "error"
    WRONG_OUTPUT = "wrong_output"
    MISSING_PATTERNS = "missing_patterns"
    """Output matched but the code doesn't use what the exercise teaches."""
    PASSED = "passed"


# Verdict -> activity_log event_type. PASSED is logged by complete_lesson()
# itself; MISSING_PATTERNS is deliberately not counted as a failure (the
# output was right), and BLOCKED is an environment problem, not the user's.
FAILURE_EVENT_TYPES: dict[Verdict, str] = {
    Verdict.TIMED_OUT: "attempt_timeout",
    Verdict.ERROR: "attempt_error",
    Verdict.WRONG_OUTPUT: "attempt_wrong_output",
}


@dataclass(frozen=True)
class RunOutcome:
    verdict: Verdict
    message: str
    """Primary line shown in the Output card."""
    raw: Optional[str] = None
    """Expandable detail: raw stderr, or an expected-vs-actual diff."""
    details_label: str = "Show raw output"
    event_detail: str = ""
    """Tail of stderr/stdout stored with the activity_log row, if any."""

    @property
    def passed(self) -> bool:
        return self.verdict is Verdict.PASSED

    @property
    def event_type(self) -> Optional[str]:
        return FAILURE_EVENT_TYPES.get(self.verdict)


_EVENT_DETAIL_TAIL = 200


def evaluate_run(result: ExecutionResult, exercise: Exercise, code: str, input_value: Optional[str]) -> RunOutcome:
    if result.blocked:
        return RunOutcome(Verdict.BLOCKED, result.blocked_message or "This toolchain isn't available.")

    if result.timed_out:
        return RunOutcome(Verdict.TIMED_OUT, "Timed out -- check for a loop that never terminates.")

    if not result.success:
        friendly, hint = translate_error(result.stderr, exercise.language)
        line = extract_error_line_number(result.stderr, exercise.language)
        if line:
            friendly = f"{friendly} (line {line})"
        return RunOutcome(
            Verdict.ERROR, f"{friendly}\n{hint}", raw=result.stderr,
            event_detail=result.stderr[-_EVENT_DETAIL_TAIL:],
        )

    output_ok = validate_output(
        result.stdout, exercise.expected_output,
        input_value=input_value, expected_output_pattern=exercise.expected_output_pattern,
    )
    contains_ok = validate_contains(code, exercise.contains_patterns or [])
    shown_stdout = result.stdout or "(no output)"

    if output_ok and contains_ok:
        return RunOutcome(Verdict.PASSED, shown_stdout)

    if output_ok:
        return RunOutcome(
            Verdict.MISSING_PATTERNS,
            f"{shown_stdout}\n\nOutput matches, but try using what this exercise is "
            "actually teaching -- not just a direct answer.",
        )

    diff_text: Optional[str] = None
    if not exercise.expected_output_pattern:
        expected_display = exercise.expected_output
        if input_value is not None and INPUT_PLACEHOLDER in expected_display:
            expected_display = expected_display.replace(INPUT_PLACEHOLDER, input_value)
        diff_text = diff_output(expected_display, result.stdout)
    return RunOutcome(
        Verdict.WRONG_OUTPUT,
        f"{shown_stdout}\n\nNot quite the expected output yet.",
        raw=diff_text,
        details_label="Show expected vs. actual",
        event_detail=result.stdout[-_EVENT_DETAIL_TAIL:],
    )
