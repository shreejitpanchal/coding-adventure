"""Shared app state: settings, progress store, per-language exercise/quiz/
execution engines (built lazily, cached), and the current theme -- built
once in main.py and threaded through every view-builder function as an
explicit parameter (no global state)."""
from __future__ import annotations

from typing import Optional

from app.config.clock import today_iso
from app.config.settings import Settings, get_db_path, load_settings, save_settings
from app.engine.exercise import Exercise
from app.engine.lesson_engine import ExerciseEngine
from app.engine.quiz_engine import QuizEngine
from app.execution.base import ExecutionEngine
from app.execution.registry import create_engine
from app.progress.store import ProgressStore
from app.ui.theme import ThemePreset, get_preset, resolve_font_scale


# How many of the Daily Refresher's slots (at most) go to a spaced-review
# item -- an exercise whose scheduled review (ProgressStore.review_schedule)
# is due -- instead of a fresh, never-completed one. Only actually used
# when something is due; a freshly-started track fills every slot with
# fresh picks, unaffected by this. The full due list lives on /review.
_REVIEW_SLOT_COUNT = 1


def resolve_daily_refresher(
    engine: ExerciseEngine, progress: ProgressStore, language: str, today: str, count: int = 5,
) -> list[Exercise]:
    """Pure lookup/generate step behind AppState.daily_refresher_exercises(),
    split out so it's testable without a full AppState (which reads real
    on-disk settings/progress)."""
    saved_ids = progress.get_daily_refresher_picks(language, today)
    if saved_ids:
        exercises = [ex for eid in saved_ids if (ex := engine.get(eid)) is not None]
        if exercises:
            return exercises

    completed_ids = set(progress.get_completed_lesson_ids(language))

    review_exercises: list[Exercise] = []
    review_slots = min(_REVIEW_SLOT_COUNT, count)
    for lesson_id in progress.get_due_reviews(language, today):
        if len(review_exercises) >= review_slots:
            break
        exercise = engine.get(lesson_id)
        if exercise is not None:
            review_exercises.append(exercise)

    fresh_count = max(count - len(review_exercises), 0)
    fresh_exercises = engine.daily_refresher(completed_ids, count=fresh_count)

    exercises = fresh_exercises + review_exercises
    if exercises:
        progress.save_daily_refresher_picks(language, today, [ex.id for ex in exercises])
    return exercises


class AppState:
    def __init__(self) -> None:
        self.settings: Settings = load_settings()
        self.progress = ProgressStore(get_db_path())
        self.language: str = self.settings.last_selected_language or "python"
        self._exercise_engines: dict[str, ExerciseEngine] = {}
        self._quiz_engines: dict[str, QuizEngine] = {}
        self._execution_engines: dict[str, ExecutionEngine] = {}
        # Where the lesson screen's Back button (and a completed exercise's
        # "Next exercise" logic) should return to -- set by app_window.py's
        # route_change() to whatever route was active just before entering
        # a /lesson/* route, so leaving a lesson lands back on the Daily
        # Refresher / category list / hub the user actually came from,
        # instead of always jumping to the hub.
        self.lesson_return_route: str = "/hub"

    @property
    def theme(self) -> ThemePreset:
        return get_preset(self.settings.theme)

    @property
    def font_scale(self) -> float:
        return resolve_font_scale(self.settings.code_font_size)

    def exercise_engine(self, language: Optional[str] = None) -> ExerciseEngine:
        lang = language or self.language
        if lang not in self._exercise_engines:
            self._exercise_engines[lang] = ExerciseEngine(lang)
        return self._exercise_engines[lang]

    def quiz_engine(self, language: Optional[str] = None) -> QuizEngine:
        lang = language or self.language
        if lang not in self._quiz_engines:
            self._quiz_engines[lang] = QuizEngine(lang)
        return self._quiz_engines[lang]

    def execution_engine(self, language: Optional[str] = None) -> ExecutionEngine:
        """The ExecutionEngine for a track, built on first use and cached
        here -- the registry itself holds no instances."""
        lang = language or self.language
        if lang not in self._execution_engines:
            self._execution_engines[lang] = create_engine(lang)
        return self._execution_engines[lang]

    def daily_refresher_exercises(self, language: Optional[str] = None) -> list[Exercise]:
        """Today's fixed Daily Refresher set -- generated once per (local)
        calendar day and persisted, so it stays a stable, finishable
        checklist instead of silently reshuffling in the incomplete
        exercises as items get completed during the day."""
        lang = language or self.language
        return resolve_daily_refresher(
            self.exercise_engine(lang), self.progress, lang, today_iso(), count=self.settings.daily_refresher_size,
        )

    def due_review_exercises(self, language: Optional[str] = None) -> list[Exercise]:
        """Exercises whose spaced review is due today (most overdue
        first), skipping any whose content no longer exists."""
        lang = language or self.language
        engine = self.exercise_engine(lang)
        return [ex for eid in self.progress.get_due_reviews(lang, today_iso()) if (ex := engine.get(eid)) is not None]

    def select_language(self, language: str) -> None:
        self.language = language
        self.settings.last_selected_language = language
        self.save_settings()

    def apply_theme(self, theme_key: str) -> None:
        self.settings.theme = theme_key
        self.save_settings()

    def apply_font_size(self, size_key: str) -> None:
        self.settings.code_font_size = size_key
        self.save_settings()

    def apply_daily_refresher_size(self, size: int) -> None:
        self.settings.daily_refresher_size = size
        self.save_settings()

    def apply_weekly_goal(self, goal: int) -> None:
        self.settings.weekly_goal = goal
        self.save_settings()

    def save_settings(self) -> None:
        save_settings(self.settings)

    def close(self) -> None:
        self.progress.close()
