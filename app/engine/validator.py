"""Exercise validation: checks behavior/output, not exact code formatting."""
from __future__ import annotations

import difflib
import re
from typing import Optional

INPUT_PLACEHOLDER = "{input}"


def validate_contains(code: str, patterns: list[str]) -> bool:
    """True if `code` contains every required pattern.

    Each pattern is matched as a case-sensitive regular expression against
    the raw source text -- a language-agnostic replacement for AST-based
    checks, so the same Exercise.contains_patterns field works whether the
    exercise is Python, Java, or C++. Intentionally lenient (substring/regex,
    not a parser) -- a structural/pedagogical nudge, not a precise linter.
    """
    if not patterns:
        return True
    return all(re.search(pattern, code) is not None for pattern in patterns)


def validate_output(
    actual_stdout: str,
    expected_output: str = "",
    input_value: Optional[str] = None,
    expected_output_pattern: Optional[str] = None,
) -> bool:
    """Compares output, optionally substituting what the user typed into a template.

    - expected_output_pattern (a regex) takes priority when set -- for
      exercises with non-deterministic output.
    - Otherwise expected_output can contain "{input}" as a placeholder for
      whatever was entered via the stdin box.
    """
    actual = actual_stdout.strip()

    if expected_output_pattern:
        return re.fullmatch(expected_output_pattern, actual) is not None

    expected = expected_output
    if input_value is not None and INPUT_PLACEHOLDER in expected:
        expected = expected.replace(INPUT_PLACEHOLDER, input_value)
    return actual == expected.strip()


def diff_output(expected: str, actual: str) -> str:
    """A readable expected-vs-actual comparison for output that failed
    validate_output(), for display in the lesson screen's details panel.

    Trailing-newline and stray-whitespace mismatches are the most common
    "wrong output" near-miss for a professional user who otherwise has the
    logic right -- both make every space/tab visible (so an invisible
    difference stops being invisible) and call out the first line that
    actually differs, rather than leaving "wrong output" as a bare
    pass/fail with nothing to act on.
    """
    def visible(line: str) -> str:
        return line.replace("\t", "→").replace(" ", "·")

    expected_lines = expected.rstrip("\n").split("\n")
    actual_lines = actual.rstrip("\n").split("\n")

    first_diff_line = None
    for i in range(max(len(expected_lines), len(actual_lines))):
        exp = expected_lines[i] if i < len(expected_lines) else None
        act = actual_lines[i] if i < len(actual_lines) else None
        if exp != act:
            first_diff_line = i + 1
            break

    diff_lines = list(difflib.unified_diff(
        [visible(line) for line in expected_lines],
        [visible(line) for line in actual_lines],
        fromfile="expected", tofile="actual", lineterm="",
    ))

    header = f"First difference at line {first_diff_line}.\n\n" if first_diff_line else ""
    return header + "\n".join(diff_lines)
