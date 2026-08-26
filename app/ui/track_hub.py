"""Per-language hub: the top of one track's navigation -- Daily Refresher,
Practice by Topic, the flagship Gotcha Gauntlet debug-puzzle track, Quiz
Bank, and the track's own progress dashboard."""
from __future__ import annotations

import flet as ft

from app.engine.categories import GOTCHA_CATEGORY, get_category_meta
from app.engine.languages import get_language
from app.ui.app_state import AppState
from app.ui.theme import scaled


def build_track_hub_view(page: ft.Page, state: AppState) -> ft.View:
    theme = state.theme
    fs = lambda base: scaled(base, state.font_scale)  # noqa: E731
    language = get_language(state.language)
    engine = state.exercise_engine()
    completed_ids = set(state.progress.get_completed_lesson_ids(state.language))
    level = state.progress.get_player_level(state.language)
    streak = state.progress.get_streak_days(state.language)

    header = ft.Column(
        [
            ft.Row(
                [
                    ft.Button(
                        "← Tracks", on_click=lambda _e: page.go("/languages"), height=44,
                        style=ft.ButtonStyle(bgcolor=theme.text_muted, color="#FFFFFF"),
                    ),
                    ft.Text(
                        f"{language.icon} {language.title}", size=fs(26), weight=ft.FontWeight.BOLD,
                        color=theme.primary, expand=True,
                    ),
                    ft.Button(
                        "⚙ Settings", on_click=lambda _e: page.go("/settings"), height=44,
                        style=ft.ButtonStyle(bgcolor=theme.text_muted, color="#FFFFFF"),
                    ),
                ],
                spacing=12,
            ),
            ft.Text(
                f"Level {level.level} · {level.total_xp} XP · {streak}-day streak",
                size=fs(14), color=theme.text_muted,
            ),
        ],
        spacing=8,
    )

    daily = state.daily_refresher_exercises()
    daily_done = sum(1 for ex in daily if ex.id in completed_ids)
    if not daily:
        daily_status = "All caught up"
    elif daily_done == len(daily):
        daily_status = "All done today!"
    else:
        daily_status = f"{daily_done}/{len(daily)} done today"
    gotcha_items = engine.lessons_in_category(GOTCHA_CATEGORY)
    gotcha_done = sum(1 for ex in gotcha_items if ex.id in completed_ids)
    quiz_engine = state.quiz_engine()
    best = state.progress.get_best_quiz_score(state.language)
    quiz_status = f"Best: {best[0]}/{best[1]}" if best else f"{len(quiz_engine)} questions available"

    cards = [
        _card(
            page, theme, fs, "🎯 Daily Refresher",
            "A short round-robin across every topic -- five exercises to keep everything warm.",
            daily_status,
            "/daily",
        ),
        _card(
            page, theme, fs, "🗂 Practice by Topic",
            "Browse every category and work through it at your own pace.",
            f"{len(engine.categories())} topics", "/categories",
        ),
        _card(
            page, theme, fs, f"{get_category_meta(GOTCHA_CATEGORY).icon} Gotcha Gauntlet",
            "Find-the-bug puzzles covering the mistakes that trip up even senior engineers.",
            f"{gotcha_done}/{len(gotcha_items)} solved" if gotcha_items else "Coming soon",
            f"/categories/{GOTCHA_CATEGORY}",
        ),
        _card(
            page, theme, fs, "❓ Quiz Bank",
            "Randomized multiple-choice questions across the whole track.",
            quiz_status, "/quiz",
        ),
        _card(
            page, theme, fs, "📈 Progress",
            "Streak, XP, mastery by topic, and achievements.",
            f"{len(completed_ids)}/{len(engine)} exercises completed", "/progress",
        ),
    ]

    return ft.View(
        route="/hub",
        bgcolor=theme.bg,
        scroll=ft.ScrollMode.AUTO,
        padding=ft.padding.Padding.only(left=24, top=24, right=24, bottom=40),
        controls=[header, ft.Container(height=16), *_stack(cards)],
    )


def _stack(cards: list[ft.Control]) -> list[ft.Control]:
    out: list[ft.Control] = []
    for card in cards:
        out.append(card)
        out.append(ft.Container(height=12))
    if out:
        out.pop()
    return out


def _card(page: ft.Page, theme, fs, title: str, subtitle: str, status: str, route: str) -> ft.Control:
    def on_click(_e: ft.ControlEvent) -> None:
        page.go(route)

    return ft.Container(
        content=ft.Column(
            [
                ft.Text(title, size=fs(20), weight=ft.FontWeight.BOLD, color=theme.text),
                ft.Text(subtitle, size=fs(13), color=theme.text_muted),
                ft.Text(status, size=fs(12), color=theme.primary, weight=ft.FontWeight.BOLD),
            ],
            spacing=6,
        ),
        bgcolor=theme.card, border_radius=16, padding=20,
        on_click=on_click, ink=True,
    )
