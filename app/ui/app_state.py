"""Shared app state: settings, progress store, per-language exercise/quiz
engines (built lazily, cached), and the current theme -- built once in
main.py and threaded through every view-builder function as an explicit
parameter (no global state)."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from app.config.settings import Settings, get_db_path, load_settings, save_settings
from app.engine.exercise import Exercise
from app.engine.lesson_engine import ExerciseEngine
from app.engine.quiz_engine import QuizEngine
from app.progress.store import ProgressStore
from app.ui.theme import ThemePreset, get_preset, resolve_font_scale


def resolve_daily_refresher(
    engine: ExerciseEngine, progress: ProgressStore, language: str, today: str,
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
    exercises = engine.daily_refresher(completed_ids, count=5)
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

    def daily_refresher_exercises(self, language: Optional[str] = None) -> list[Exercise]:
        """Today's fixed Daily Refresher set -- generated once per calendar
        day and persisted, so it stays a stable, finishable checklist
        instead of silently reshuffling in the incomplete exercises as
        items get completed during the day."""
        lang = language or self.language
        today = datetime.now(timezone.utc).date().isoformat()
        return resolve_daily_refresher(self.exercise_engine(lang), self.progress, lang, today)

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

    def save_settings(self) -> None:
        save_settings(self.settings)

    def close(self) -> None:
        self.progress.close()
