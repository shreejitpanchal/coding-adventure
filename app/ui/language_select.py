"""Language picker -- the screen shown at the start of every session
(after first-run setup), not just the first time. Deliberately not
auto-skipped by "last selected language" -- that value only pre-highlights
a card here."""
from __future__ import annotations

import flet as ft

from app.engine.languages import LANGUAGE_ORDER, get_language
from app.ui.app_state import AppState
from app.ui.theme import scaled


def build_language_select_view(page: ft.Page, state: AppState) -> ft.View:
    theme = state.theme
    fs = lambda base: scaled(base, state.font_scale)  # noqa: E731
    handle = state.settings.handle or "there"

    header = ft.Column(
        [
            ft.Row(
                [
                    ft.Text("Coding Adventure", size=fs(28), weight=ft.FontWeight.BOLD, color=theme.primary, expand=True),
                    ft.Button(
                        "⚙ Settings", on_click=lambda _e: page.go("/settings"), height=44,
                        style=ft.ButtonStyle(bgcolor=theme.text_muted, color="#FFFFFF"),
                    ),
                ],
            ),
            ft.Text(f"Welcome back, {handle}. Pick a track to sharpen.", size=fs(15), color=theme.text_muted),
        ],
        spacing=6,
    )

    cards = [
        _build_language_card(page, state, get_language(key))
        for key in LANGUAGE_ORDER
    ]

    return ft.View(
        route="/languages",
        bgcolor=theme.bg,
        scroll=ft.ScrollMode.AUTO,
        padding=ft.padding.Padding.only(left=24, top=24, right=24, bottom=40),
        controls=[
            header,
            ft.Container(height=16),
            ft.Row(cards, wrap=True, spacing=16, run_spacing=16),
        ],
    )


def _build_language_card(page: ft.Page, state: AppState, info) -> ft.Control:
    theme = state.theme
    fs = lambda base: scaled(base, state.font_scale)  # noqa: E731

    subtitle: str
    if info.available:
        level = state.progress.get_player_level(info.key)
        streak = state.progress.get_streak_days(info.key)
        subtitle = f"Level {level.level} · {level.total_xp} XP · {streak}-day streak"
    else:
        subtitle = info.tagline

    def on_click(_e: ft.ControlEvent) -> None:
        if not info.available:
            page.show_dialog(ft.SnackBar(ft.Text(f"{info.title} is coming soon.")))
            return
        state.select_language(info.key)
        page.go("/hub")

    return ft.Container(
        content=ft.Column(
            [
                ft.Text(info.icon, size=fs(36)),
                ft.Text(info.title, size=fs(20), weight=ft.FontWeight.BOLD, color=theme.text),
                ft.Text(subtitle, size=fs(13), color=theme.text_muted),
                ft.Container(
                    content=ft.Text(
                        "Available" if info.available else "Coming soon",
                        size=fs(12), weight=ft.FontWeight.BOLD,
                        color="#FFFFFF" if info.available else theme.text_muted,
                    ),
                    bgcolor=theme.success if info.available else theme.card,
                    border_radius=8, padding=ft.padding.Padding.symmetric(horizontal=10, vertical=4),
                ),
            ],
            spacing=8,
        ),
        bgcolor=theme.card, border_radius=20, padding=24, width=240,
        border=ft.border.Border.all(2, theme.primary if info.available else theme.text_muted),
        opacity=1.0 if info.available else 0.7,
        on_click=on_click, ink=info.available,
    )
