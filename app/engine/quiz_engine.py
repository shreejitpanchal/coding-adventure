"""Loads a language track's quiz questions from YAML.

Adding a question means editing content/<language>/quiz/quiz_questions.yaml -- no code changes here.
"""
from __future__ import annotations

import random
from pathlib import Path
from typing import Collection, Optional

from app.config.paths import CONTENT_ROOT
from app.engine.content_loader import ContentError, load_yaml_file
from app.engine.quiz import QuizQuestion


class QuizEngine:
    def __init__(self, language: str, quiz_path: Optional[Path] = None):
        self.language = language
        path = quiz_path or (CONTENT_ROOT / language / "quiz" / "quiz_questions.yaml")
        self._questions: list[QuizQuestion] = []
        if not path.is_file():
            return
        data = load_yaml_file(path) or {}
        if not isinstance(data, dict) or not isinstance(data.get("questions", []), list):
            raise ContentError(path, "expected a top-level mapping with a `questions` list")
        seen: set[str] = set()
        for index, raw in enumerate(data.get("questions", []), start=1):
            try:
                question = QuizQuestion.from_mapping(raw, default_id=f"{language}_q{index}")
            except ValueError as exc:
                raise ContentError(path, str(exc)) from exc
            if question.id in seen:
                raise ContentError(path, f"duplicate quiz question id {question.id!r}")
            seen.add(question.id)
            self._questions.append(question)

    def __len__(self) -> int:
        return len(self._questions)

    def all_questions(self) -> list[QuizQuestion]:
        return list(self._questions)

    def start_session(self, count: Optional[int] = None) -> list[QuizQuestion]:
        """A freshly randomized set of questions for one quiz playthrough --
        which questions are picked and each question's own option order are
        both re-randomized here, so no two playthroughs look the same."""
        return self._build_session(self._questions, count)

    def start_session_for_tags(self, tags: Collection[str], count: Optional[int] = None) -> list[QuizQuestion]:
        tags = set(tags)
        pool = [q for q in self._questions if set(q.concept_tags) & tags] if tags else []
        if not pool:
            pool = self._questions
        return self._build_session(pool, count)

    def _build_session(self, candidates: list[QuizQuestion], count: Optional[int]) -> list[QuizQuestion]:
        if count is not None and 0 < count < len(candidates):
            pool = random.sample(candidates, count)
        else:
            pool = list(candidates)
            random.shuffle(pool)
        return [shuffle_options(q) for q in pool]


def shuffle_options(question: QuizQuestion) -> QuizQuestion:
    """A copy of `question` with its options in random order and `correct`
    re-pointed accordingly. Shared with the lesson screen's comprehension
    check so both multiple-choice surfaces randomize the same way."""
    paired = list(enumerate(question.options))
    random.shuffle(paired)
    new_options = [text for _, text in paired]
    new_correct = next(i for i, (original_index, _) in enumerate(paired) if original_index == question.correct)
    return QuizQuestion(
        id=question.id,
        question=question.question,
        options=new_options,
        correct=new_correct,
        explanation=question.explanation,
        concept_tags=list(question.concept_tags),
    )
