"""Topic browser: a clean grid of category cards (not a winding "adventure
map" -- this app's audience is professionals, not kids)."""
from __future__ import annotations

import flet as ft

from app.engine.categories import get_category_meta
from app.ui.app_state import AppState
from app.ui.theme import scaled


def build_category_map_view(page: ft.Page, state: AppState) -> ft.View:
    theme = state.theme
    fs = lambda base: scaled(base, state.font_scale)  # noqa: E731
    engine = state.exercise_engine()
    completed_ids = set(state.progress.get_completed_lesson_ids(state.language))

    header = ft.Row(
        [
            ft.Button(
                "← Hub", on_click=lambda _e: page.go("/hub"), height=44,
                style=ft.ButtonStyle(bgcolor=theme.text_muted, color="#FFFFFF"),
            ),
            ft.Text("Practice by Topic", size=fs(24), weight=ft.FontWeight.BOLD, color=theme.primary, expand=True),
        ],
        spacing=12,
    )

    cards = [
        _build_category_card(page, theme, fs, engine, category, completed_ids)
        for category in engine.categories()
    ]

    return ft.View(
        route="/categories",
        bgcolor=theme.bg,
        scroll=ft.ScrollMode.AUTO,
        padding=ft.padding.Padding.only(left=24, top=24, right=24, bottom=40),
        controls=[header, ft.Container(height=16), ft.Row(cards, wrap=True, spacing=16, run_spacing=16)],
    )


def _build_category_card(page, theme, fs, engine, category: str, completed_ids: set[str]) -> ft.Control:
    meta = get_category_meta(category)
    items = engine.lessons_in_category(category)
    done = sum(1 for ex in items if ex.id in completed_ids)

    def on_click(_e: ft.ControlEvent) -> None:
        page.go(f"/categories/{category}")

    return ft.Container(
        content=ft.Column(
            [
                ft.Text(meta.icon, size=fs(28)),
                ft.Text(meta.title, size=fs(16), weight=ft.FontWeight.BOLD, color=theme.text),
                ft.Text(f"{done}/{len(items)} complete", size=fs(12), color=theme.text_muted),
            ],
            spacing=6,
        ),
        bgcolor=theme.card, border_radius=16, padding=18, width=220,
        border=ft.border.Border.all(3, meta.color),
        on_click=on_click, ink=True,
    )
