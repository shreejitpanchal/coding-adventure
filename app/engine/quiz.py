"""The QuizQuestion data model. Quiz content is data, not code -- see
content/<language>/quiz/quiz_questions.yaml. The same dataclass is used
for an exercise's inline comprehension check (Exercise.comprehension_check),
so one validation rule set covers both places multiple-choice content
comes from."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

MIN_OPTIONS = 2


@dataclass
class QuizQuestion:
    id: str
    question: str
    options: list[str]
    correct: int
    explanation: str = ""
    concept_tags: list[str] = field(default_factory=list)
    """Which concepts this question tests, from the same fixed vocabulary
    as Exercise.concept_tags -- used to recommend relevant practice
    exercises after a quiz. Empty is valid."""

    def __post_init__(self) -> None:
        # Fail at load time with the question id in the message, not at
        # render time with a bare IndexError on some button.
        if not isinstance(self.options, list) or len(self.options) < MIN_OPTIONS:
            raise ValueError(
                f"Question {self.id!r}: needs at least {MIN_OPTIONS} options, got "
                f"{self.options!r}. Fix the YAML's `options` list."
            )
        if not isinstance(self.correct, int) or not 0 <= self.correct < len(self.options):
            raise ValueError(
                f"Question {self.id!r}: `correct` must be an index into options "
                f"(0..{len(self.options) - 1}), got {self.correct!r}."
            )
        if not str(self.question).strip():
            raise ValueError(f"Question {self.id!r}: `question` text is empty.")

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any], default_id: str) -> "QuizQuestion":
        """Build from a YAML mapping. `default_id` is used when the mapping
        has no `id` of its own -- comprehension-check questions inside an
        exercise file don't carry one, so the caller derives it from the
        exercise id and position."""
        if not isinstance(data, Mapping):
            raise ValueError(f"Question {default_id!r}: expected a mapping, got {type(data).__name__}")
        payload = dict(data)
        payload.setdefault("id", default_id)
        try:
            return cls(**payload)
        except TypeError as exc:
            # Unknown key -- say which one, not just "unexpected keyword".
            raise ValueError(f"Question {payload['id']!r}: {exc}") from exc
