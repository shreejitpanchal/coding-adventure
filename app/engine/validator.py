"""Exercise validation: checks behavior/output, not exact code formatting."""
from __future__ import annotations

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
