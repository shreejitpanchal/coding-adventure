"""Per-track dashboard: streak, XP, mastery by topic, achievements."""
from __future__ import annotations

import flet as ft

from app.engine.categories import get_category_meta
from app.ui.app_state import AppState
from app.ui.theme import scaled


def build_progress_view(page: ft.Page, state: AppState) -> ft.View:
    theme = state.theme
    fs = lambda base: scaled(base, state.font_scale)  # noqa: E731
    engine = state.exercise_engine()
    progress = state.progress
    completed_ids = set(progress.get_completed_lesson_ids(state.language))
    level = progress.get_player_level(state.language)
    streak = progress.get_streak_days(state.language)
    weekly = progress.get_weekly_summary(state.language)

    header = ft.Row(
        [
            ft.Button(
                "← Hub", on_click=lambda _e: page.go("/hub"), height=44,
                style=ft.ButtonStyle(bgcolor=theme.text_muted, color="#FFFFFF"),
            ),
            ft.Text("Progress", size=fs(24), weight=ft.FontWeight.BOLD, color=theme.primary, expand=True),
        ],
        spacing=12,
    )

    xp_card = ft.Container(
        content=ft.Column(
            [
                ft.Text(f"Level {level.level}", size=fs(22), weight=ft.FontWeight.BOLD, color=theme.text),
                ft.Text(
                    f"{level.xp_into_level} / {level.xp_needed_for_level} XP to next level "
                    f"({level.total_xp} total)",
                    size=fs(13), color=theme.text_muted,
                ),
                ft.Text(f"{streak}-day streak", size=fs(13), color=theme.text_muted),
                ft.Text(
                    f"This week: {weekly.lessons_completed} exercises, "
                    f"{weekly.quiz_attempts} quizzes, {weekly.badges_earned} achievements, "
                    f"{weekly.active_days} active days",
                    size=fs(13), color=theme.text_muted,
                ),
            ],
            spacing=6,
        ),
        bgcolor=theme.card, border_radius=16, padding=20,
    )

    mastery_rows = []
    for category in engine.categories():
        meta = get_category_meta(category)
        items = engine.lessons_in_category(category)
        done = sum(1 for ex in items if ex.id in completed_ids)
        pct = round(100 * done / len(items)) if items else 0
        mastery_rows.append(
            ft.Row(
                [
                    ft.Text(f"{meta.icon} {meta.title}", size=fs(14), color=theme.text, expand=True),
                    ft.Text(f"{done}/{len(items)} ({pct}%)", size=fs(13), color=theme.text_muted),
                ],
            )
        )
    mastery_card = ft.Container(
        content=ft.Column(
            [ft.Text("Mastery by topic", size=fs(16), weight=ft.FontWeight.BOLD, color=theme.text), *mastery_rows],
            spacing=8,
        ),
        bgcolor=theme.card, border_radius=16, padding=20,
    )

    badges = progress.get_badges_with_dates(state.language)
    badge_chips = [
        ft.Container(
            content=ft.Text(badge_id.replace("_", " ").title(), size=fs(12), color="#FFFFFF"),
            bgcolor=theme.success, border_radius=8, padding=ft.padding.Padding.symmetric(horizontal=10, vertical=6),
        )
        for badge_id, _ in badges
    ]
    achievements_card = ft.Container(
        content=ft.Column(
            [
                ft.Text("Achievements", size=fs(16), weight=ft.FontWeight.BOLD, color=theme.text),
                ft.Row(badge_chips, wrap=True, spacing=8) if badge_chips
                else ft.Text("None yet -- solve a Gotcha Gauntlet puzzle or finish a topic to earn one.", size=fs(13), color=theme.text_muted),
            ],
            spacing=10,
        ),
        bgcolor=theme.card, border_radius=16, padding=20,
    )

    return ft.View(
        route="/progress",
        bgcolor=theme.bg,
        scroll=ft.ScrollMode.AUTO,
        padding=ft.padding.Padding.only(left=24, top=24, right=24, bottom=40),
        controls=[header, ft.Container(height=12), xp_card, ft.Container(height=12), mastery_card, ft.Container(height=12), achievements_card],
    )
