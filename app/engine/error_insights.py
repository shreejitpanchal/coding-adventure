"""Recurring-error insight: which kinds of failures keep coming back.

Every failed run already logs an `attempt_error` row with the tail of
stderr. This groups those rows by the same friendly explanation
`translate_error()` shows in the lesson (so "Null reference." and
"Index out of range." are separate buckets even when the raw text
differs), counts them, and gathers the concept tags of the exercises
they happened on so the Progress screen can offer targeted practice.
Pure function over rows -- no UI, no store access."""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Iterable, Optional

from app.engine.lesson_engine import ExerciseEngine
from app.execution.errors import translate_error


@dataclass
class ErrorInsight:
    message: str
    """The friendly one-liner from translate_error(), e.g. "Null reference."."""
    hint: str
    count: int
    concept_tags: list[str] = field(default_factory=list)
    """Most-common-first tags of the exercises this error occurred on."""
    lesson_ids: list[str] = field(default_factory=list)
    """Distinct exercises affected, most recent first."""


def summarize_errors(
    rows: Iterable[tuple[Optional[str], str]], engine: ExerciseEngine, language: str, *, limit: int = 5,
) -> list[ErrorInsight]:
    """`rows` are (lesson_id, stderr_tail) pairs, most recent first."""
    counts: Counter[str] = Counter()
    hints: dict[str, str] = {}
    tags: dict[str, Counter[str]] = defaultdict(Counter)
    lessons: dict[str, list[str]] = defaultdict(list)

    for lesson_id, detail in rows:
        message, hint = translate_error(detail or "", language)
        counts[message] += 1
        hints.setdefault(message, hint)
        if lesson_id:
            if lesson_id not in lessons[message]:
                lessons[message].append(lesson_id)
            exercise = engine.get(lesson_id)
            if exercise is not None:
                tags[message].update(exercise.concept_tags)

    insights = [
        ErrorInsight(
            message=message, hint=hints[message], count=count,
            concept_tags=[tag for tag, _ in tags[message].most_common()],
            lesson_ids=lessons[message],
        )
        for message, count in counts.most_common(limit)
    ]
    return insights
