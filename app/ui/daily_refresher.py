"""Daily Refresher: a short cross-topic set (app.engine.lesson_engine.
ExerciseEngine.daily_refresher()) rendered with the same list view as a
plain category."""
from __future__ import annotations

import flet as ft

from app.ui.app_state import AppState
from app.ui.category_levels import build_exercise_list_view


def build_daily_refresher_view(page: ft.Page, state: AppState) -> ft.View:
    exercises = state.daily_refresher_exercises()
    return build_exercise_list_view(
        page, state, title="🎯 Daily Refresher", route="/daily", exercises=exercises, back_route="/hub",
    )
