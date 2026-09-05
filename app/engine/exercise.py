"""The Exercise data model. Content is data, not code -- see content/<language>/lessons/*.yaml."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Exercise:
    id: str
    title: str
    language: str
    level: int
    objective: str
    explanation: str
    example_code: str = ""
    starter_code: str = ""
    challenge: str = ""
    expected_output: str = ""
    expected_output_pattern: Optional[str] = None
    """Regex alternative to expected_output, for exercises with
    non-deterministic output (e.g. involving randomness or timing)."""
    hints: list[str] = field(default_factory=list)
    xp_reward: int = 10
    achievement: Optional[str] = None
    input_prompt: Optional[str] = None
    """Drives a labeled stdin input box, templated into expected_output via {input}."""
    category: str = "general"
    category_level: int = 1
    """1-based position within category -- drives the topic-browser unlock order."""
    difficulty: str = "core"
    """One of warmup/core/gotcha/deep_dive -- purely descriptive, shown as a badge."""
    contains_patterns: Optional[list[str]] = None
    """Structural check: substrings/regex the submitted code must contain
    (e.g. a specific stdlib call the exercise is teaching) -- language-
    agnostic replacement for the old app's Python-AST-only ast_contains,
    see app.engine.validator.validate_contains()."""
    concept_tags: list[str] = field(default_factory=list)
    """Fixed vocabulary shared with quiz questions, feeds adaptive practice
    recommendations."""
    spring_test_code: str = ""
    """Spring-only: the fixed JUnit test class source that gates completion
    via `mvn test`, since a Spring exercise isn't a single self-contained
    code string like the other languages -- see app.execution.spring_engine."""
    requires_code: bool = True
    """False for purely conceptual exercises with no code to write or run
    (e.g. the `architecture` track) -- lesson_screen.py skips the code
    editor/Run button entirely and gates completion on comprehension_check
    instead. Never calls get_engine()/check_toolchain() for these, so a
    track using this doesn't need an execution engine registered at all."""
    comprehension_check: list = field(default_factory=list)
    """Only used when requires_code is False: a short list of inline
    multiple-choice questions (each a dict with question/options/correct/
    explanation, same shape as a QuizQuestion) that gate completion instead
    of running code -- answering every one correctly marks the exercise
    complete."""
