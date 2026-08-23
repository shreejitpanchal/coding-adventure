"""Loads a language track's quiz questions from YAML.

Adding a question means editing content/<language>/quiz/quiz_questions.yaml -- no code changes here.
"""
from __future__ import annotations

import random
from pathlib import Path
from typing import Collection, Optional

import yaml

from app.engine.quiz import QuizQuestion

CONTENT_ROOT = Path(__file__).resolve().parent.parent.parent / "content"


class QuizEngine:
    def __init__(self, language: str, quiz_path: Optional[Path] = None):
        self.language = language
        path = quiz_path or (CONTENT_ROOT / language / "quiz" / "quiz_questions.yaml")
        if path.is_file():
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            self._questions = [QuizQuestion(**q) for q in data.get("questions", [])]
        else:
            self._questions = []

    def __len__(self) -> int:
        return len(self._questions)

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

        session: list[QuizQuestion] = []
        for question in pool:
            paired = list(enumerate(question.options))
            random.shuffle(paired)
            new_options = [text for _, text in paired]
            new_correct = next(i for i, (original_index, _) in enumerate(paired) if original_index == question.correct)
            session.append(QuizQuestion(
                id=question.id,
                question=question.question,
                options=new_options,
                correct=new_correct,
                explanation=question.explanation,
                concept_tags=question.concept_tags,
            ))
        return session
