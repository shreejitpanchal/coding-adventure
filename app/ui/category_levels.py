"""A list of exercises -- shared renderer for a single category's levels
and for the Daily Refresher's cross-topic set. Each row: a numbered
level badge in the category colour, title, difficulty + XP chips, and a
status icon (done / next / locked). Rows fade in one after another."""
from __future__ import annotations

from typing import Optional

import flet as ft

from app.engine.categories import get_category_meta
from app.engine.exercise import Exercise
from app.ui.app_state import AppState
from app.ui.components import (
    RADIUS_SM,
    chip,
    difficulty_color,
    difficulty_label,
    empty_state,
    format_duration,
    header_row,
    level_badge,
    route_handler,
    spacer,
    tint,
    view_padding,
)
from app.ui.motion import Stagger, hover_lift
from app.ui.theme import scaled


def build_category_levels_view(page: ft.Page, state: AppState, category: str) -> ft.View:
    engine = state.exercise_engine()
    meta = get_category_meta(category)
    items = engine.lessons_in_category(category)
    completed_ids = set(state.progress.get_completed_lesson_ids(state.language))
    done = sum(1 for ex in items if ex.id in completed_ids)
    return build_exercise_list_view(
        page, state, title=f"{meta.icon} {meta.title}", route=f"/categories/{category}", exercises=items,
        back_route="/categories", subtitle=f"{done}/{len(items)} complete · levels unlock in order",
        accent=meta.color,
    )


def build_exercise_list_view(
    page: ft.Page, state: AppState, title: str, route: str, exercises: list[Exercise],
    back_route: str = "/hub", subtitle: Optional[str] = None, accent: Optional[str] = None,
    summary: Optional[ft.Control] = None,
) -> ft.View:
    theme = state.theme
    fs = lambda base: scaled(base, state.font_scale)  # noqa: E731
    engine = state.exercise_engine()
    completed_ids = set(state.progress.get_completed_lesson_ids(state.language))
    best_times = state.progress.get_best_solve_times(state.language)
    stagger = Stagger(page, step=0.04)

    header = header_row(theme, fs, title, route_handler(page, back_route), subtitle=subtitle)

    rows: list[ft.Control]
    if exercises:
        rows = [
            stagger.wrap(_build_row(page, theme, fs, engine, exercise, completed_ids, index, accent,
                                    best_times.get(exercise.id)))
            for index, exercise in enumerate(exercises, start=1)
        ]
    else:
        rows = [empty_state(theme, fs, ft.Icons.CELEBRATION_ROUNDED, "Nothing here yet",
                            "Every exercise in this list is done, or there's nothing to show right now.")]

    controls: list[ft.Control] = [header, spacer(16)]
    if summary is not None:
        controls.extend([stagger.wrap(summary, distance=0.03), spacer(16)])
    controls.append(ft.Column(rows, spacing=10))
    stagger.play()

    return ft.View(
        route=route,
        bgcolor=theme.bg,
        scroll=ft.ScrollMode.AUTO,
        padding=view_padding(),
        controls=controls,
    )


def _build_row(page, theme, fs, engine, exercise: Exercise, completed_ids: set[str], index: int,
               accent: Optional[str], best_seconds: Optional[int] = None) -> ft.Control:
    unlocked = engine.is_unlocked(exercise, completed_ids)
    done = exercise.id in completed_ids
    meta = get_category_meta(exercise.category)
    color = accent or meta.color

    if done:
        status_icon, status_color, status_text = ft.Icons.CHECK_CIRCLE_ROUNDED, theme.success, "Done"
    elif not unlocked:
        status_icon, status_color, status_text = ft.Icons.LOCK_ROUNDED, theme.text_muted, "Locked"
    else:
        status_icon, status_color, status_text = ft.Icons.PLAY_ARROW_ROUNDED, color, "Start"

    chips: list[ft.Control] = [
        chip(difficulty_label(exercise.difficulty), difficulty_color(theme, exercise.difficulty), fs),
        chip(f"{exercise.xp_reward} XP", theme.warning, fs, icon=ft.Icons.BOLT),
    ]
    if best_seconds is not None:
        chips.append(chip(f"Best {format_duration(best_seconds)}", theme.success, fs, icon=ft.Icons.TIMER_ROUNDED))
    if accent is None:
        # Cross-topic lists (Daily Refresher / Review Queue) show which category each row is from.
        chips.insert(0, chip(meta.title, meta.color, fs))

    row = ft.Container(
        content=ft.Row(
            [
                level_badge(exercise.category_level if accent else index, color, fs, size=38),
                ft.Column(
                    [
                        ft.Text(exercise.title, size=fs(15), weight=ft.FontWeight.BOLD,
                                color=theme.text if unlocked else theme.text_muted),
                        ft.Row(chips, spacing=6, wrap=True),
                    ],
                    spacing=6, expand=True,
                ),
                ft.Column(
                    [ft.Icon(status_icon, color=status_color, size=fs(24)),
                     ft.Text(status_text, size=fs(10), color=status_color)],
                    spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER, tight=True,
                ),
            ],
            spacing=16, vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=tint(theme.success, 0.08) if done else theme.card,
        border=ft.Border.all(1, tint(theme.success, 0.35) if done else tint(color, 0.25)),
        border_radius=RADIUS_SM + 4, padding=ft.Padding.symmetric(horizontal=18, vertical=14),
        opacity=1.0 if unlocked else 0.55,
        on_click=route_handler(page, f"/lesson/{exercise.id}") if unlocked else None, ink=unlocked,
    )
    return hover_lift(row, theme, scale=1.01, glow_color=color) if unlocked else row
