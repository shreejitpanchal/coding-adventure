"""Meta-achievements: badges earned from cross-cutting milestones (a
streak reaching a milestone, a whole category completed, a perfect quiz,
a track's very first completion) rather than a single exercise's own
YAML-declared `achievement` field.

Reuses ProgressStore.award_badge()'s existing idempotent insert -- the
Progress screen's badge list and export/import don't need to know
whether a badge came from an exercise or from here; they're all just
rows in the same `badges` table.
"""
from __future__ import annotations

from app.engine.lesson_engine import ExerciseEngine
from app.progress.store import ProgressStore

STREAK_MILESTONES = [3, 7, 14, 30, 100]


def evaluate_lesson_completion_achievements(
    progress: ProgressStore, engine: ExerciseEngine, language: str, category: str,
) -> list[str]:
    """Call after ProgressStore.complete_lesson() and record_play_today()
    (streak_days needs to already reflect today). Returns the ids of any
    meta-achievement badges newly awarded by this call."""
    newly_awarded: list[str] = []
    completed_ids = set(progress.get_completed_lesson_ids(language))

    if len(completed_ids) == 1 and progress.award_badge(language, "first_completion"):
        newly_awarded.append("first_completion")

    category_items = engine.lessons_in_category(category)
    if category_items and all(ex.id in completed_ids for ex in category_items):
        badge_id = f"category_complete_{category}"
        if progress.award_badge(language, badge_id):
            newly_awarded.append(badge_id)

    streak = progress.get_streak_days(language)
    if streak in STREAK_MILESTONES:
        badge_id = f"streak_{streak}"
        if progress.award_badge(language, badge_id):
            newly_awarded.append(badge_id)

    return newly_awarded


def evaluate_quiz_achievements(progress: ProgressStore, language: str, score: int, total: int) -> list[str]:
    """Call after ProgressStore.record_quiz_attempt(). Returns the ids of
    any meta-achievement badges newly awarded by this call."""
    newly_awarded: list[str] = []
    if total > 0 and score == total and progress.award_badge(language, "perfect_quiz"):
        newly_awarded.append("perfect_quiz")
    return newly_awarded
