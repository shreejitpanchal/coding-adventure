"""Daily Refresher: a short cross-topic set (app.engine.lesson_engine.
ExerciseEngine.daily_refresher()) rendered with the same list view as a
plain category."""
from __future__ import annotations

import flet as ft

from app.ui.app_state import AppState
from app.ui.category_levels import build_exercise_list_view


def build_daily_refresher_view(page: ft.Page, state: AppState) -> ft.View:
    engine = state.exercise_engine()
    completed_ids = set(state.progress.get_completed_lesson_ids(state.language))
    exercises = engine.daily_refresher(completed_ids, count=5)
    return build_exercise_list_view(
        page, state, title="🎯 Daily Refresher", route="/daily", exercises=exercises, back_route="/hub",
    )
