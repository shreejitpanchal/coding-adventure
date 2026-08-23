"""A plain list of exercises -- shared renderer for a single category's
levels and for the Daily Refresher's cross-topic set."""
from __future__ import annotations

from typing import Optional

import flet as ft

from app.engine.categories import get_category_meta
from app.engine.exercise import Exercise
from app.ui.app_state import AppState
from app.ui.theme import scaled


def build_category_levels_view(page: ft.Page, state: AppState, category: str) -> ft.View:
    engine = state.exercise_engine()
    meta = get_category_meta(category)
    items = engine.lessons_in_category(category)
    return build_exercise_list_view(
        page, state, title=f"{meta.icon} {meta.title}", route=f"/categories/{category}", exercises=items,
        back_route="/categories",
    )


def build_exercise_list_view(
    page: ft.Page, state: AppState, title: str, route: str, exercises: list[Exercise],
    back_route: str = "/hub",
) -> ft.View:
    theme = state.theme
    fs = lambda base: scaled(base, state.font_scale)  # noqa: E731
    engine = state.exercise_engine()
    completed_ids = set(state.progress.get_completed_lesson_ids(state.language))

    header = ft.Row(
        [
            ft.Button(
                "← Back", on_click=lambda _e: page.go(back_route), height=44,
                style=ft.ButtonStyle(bgcolor=theme.text_muted, color="#FFFFFF"),
            ),
            ft.Text(title, size=fs(24), weight=ft.FontWeight.BOLD, color=theme.primary, expand=True),
        ],
        spacing=12,
    )

    rows = [
        _build_row(page, theme, fs, engine, exercise, completed_ids)
        for exercise in exercises
    ]
    if not rows:
        rows = [ft.Text("Nothing here yet.", size=fs(14), color=theme.text_muted)]

    return ft.View(
        route=route,
        bgcolor=theme.bg,
        scroll=ft.ScrollMode.AUTO,
        padding=ft.padding.Padding.only(left=24, top=24, right=24, bottom=40),
        controls=[header, ft.Container(height=12), ft.Column(rows, spacing=10)],
    )


def _build_row(page, theme, fs, engine, exercise: Exercise, completed_ids: set[str]) -> ft.Control:
    unlocked = engine.is_unlocked(exercise, completed_ids)
    done = exercise.id in completed_ids

    if done:
        status_icon, status_color = "✓", theme.success
    elif not unlocked:
        status_icon, status_color = "🔒", theme.text_muted
    else:
        status_icon, status_color = "▶", theme.primary

    def on_click(_e: ft.ControlEvent) -> None:
        if unlocked:
            page.go(f"/lesson/{exercise.id}")

    return ft.Container(
        content=ft.Row(
            [
                ft.Text(status_icon, size=fs(18), color=status_color),
                ft.Column(
                    [
                        ft.Text(exercise.title, size=fs(15), weight=ft.FontWeight.BOLD, color=theme.text),
                        ft.Text(
                            f"{exercise.difficulty.replace('_', ' ').title()} · {exercise.xp_reward} XP",
                            size=fs(12), color=theme.text_muted,
                        ),
                    ],
                    spacing=2, expand=True,
                ),
            ],
            spacing=14,
        ),
        bgcolor=theme.card, border_radius=12, padding=16,
        opacity=1.0 if unlocked else 0.5,
        on_click=on_click, ink=unlocked,
    )
