"""The QuizQuestion data model. Quiz content is data, not code -- see content/<language>/quiz/quiz_questions.yaml."""
from __future__ import annotations

from dataclasses import dataclass, field


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
