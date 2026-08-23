"""Shared app state: settings, progress store, per-language exercise/quiz
engines (built lazily, cached), and the current theme -- built once in
main.py and threaded through every view-builder function as an explicit
parameter (no global state)."""
from __future__ import annotations

from typing import Optional

from app.config.settings import Settings, get_db_path, load_settings, save_settings
from app.engine.lesson_engine import ExerciseEngine
from app.engine.quiz_engine import QuizEngine
from app.progress.store import ProgressStore
from app.ui.theme import ThemePreset, get_preset, resolve_font_scale


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
