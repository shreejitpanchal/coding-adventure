"""Exercise search: find any exercise by title, objective, or concept
tag, optionally filtered by difficulty -- a flat lookup across the whole
track's content, useful once a track has hundreds of exercises spread
across many categories."""
from __future__ import annotations

from typing import Optional

import flet as ft

from app.engine.categories import get_category_meta
from app.ui.app_state import AppState
from app.ui.theme import scaled

_DIFFICULTIES = ["warmup", "core", "gotcha", "deep_dive"]


def build_search_view(page: ft.Page, state: AppState) -> ft.View:
    return _SearchController(page, state).build_view()


class _SearchController:
    def __init__(self, page: ft.Page, state: AppState) -> None:
        self.page = page
        self.state = state
        self.theme = state.theme
        self.scale = state.font_scale
        self.engine = state.exercise_engine()
        self.completed_ids = set(state.progress.get_completed_lesson_ids(state.language))
        self.difficulty_filter: Optional[str] = None
        self.difficulty_buttons: dict[Optional[str], ft.Button] = {}

    def _fs(self, base: int) -> int:
        return scaled(base, self.scale)

    def build_view(self) -> ft.View:
        theme = self.theme
        header = ft.Row(
            [
                ft.Button(
                    "← Hub", on_click=lambda _e: self.page.go("/hub"), height=44,
                    style=ft.ButtonStyle(bgcolor=theme.text_muted, color="#FFFFFF"),
                ),
                ft.Text(
                    "Search Exercises", size=self._fs(24), weight=ft.FontWeight.BOLD,
                    color=theme.primary, expand=True,
                ),
            ],
            spacing=12,
        )

        self.search_field = ft.TextField(
            hint_text='Search by title, objective, or concept (e.g. "closures")...',
            on_change=self._on_query_change, autofocus=True,
        )

        filter_buttons = [self._make_difficulty_button(None, "All")]
        filter_buttons.extend(self._make_difficulty_button(d, d.replace("_", " ").title()) for d in _DIFFICULTIES)

        self.results_column = ft.Column([], spacing=8)
        self._render_results()

        return ft.View(
            route="/search",
            bgcolor=theme.bg,
            scroll=ft.ScrollMode.AUTO,
            padding=ft.padding.Padding.only(left=24, top=24, right=24, bottom=40),
            controls=[
                header,
                self.search_field,
                ft.Row(filter_buttons, spacing=8, wrap=True),
                ft.Container(height=8),
                self.results_column,
            ],
        )

    def _make_difficulty_button(self, difficulty: Optional[str], label: str) -> ft.Button:
        theme = self.theme

        def on_click(_e: ft.ControlEvent) -> None:
            self.difficulty_filter = difficulty
            for d, b in self.difficulty_buttons.items():
                b.disabled = d == difficulty
                b.style = ft.ButtonStyle(
                    bgcolor=theme.primary if d == difficulty else theme.text_muted, color="#FFFFFF",
                )
            self._render_results()
            self.page.update()

        button = ft.Button(
            label, on_click=on_click, height=36, disabled=difficulty is None,
            style=ft.ButtonStyle(bgcolor=theme.primary if difficulty is None else theme.text_muted, color="#FFFFFF"),
        )
        self.difficulty_buttons[difficulty] = button
        return button

    def _on_query_change(self, e: ft.ControlEvent) -> None:
        self._render_results()
        self.page.update()

    def _render_results(self) -> None:
        theme = self.theme
        query = self.search_field.value or ""
        results = self.engine.search(query, difficulty=self.difficulty_filter)

        if not results:
            self.results_column.controls = [ft.Text(
                "No matching exercises." if query or self.difficulty_filter
                else "Type to search, or pick a difficulty above.",
                size=self._fs(13), color=theme.text_muted,
            )]
            return

        rows: list[ft.Control] = []
        for ex in results:
            meta = get_category_meta(ex.category)
            unlocked = self.engine.is_unlocked(ex, self.completed_ids)
            done = ex.id in self.completed_ids
            status = "✓ Done" if done else ("🔒 Locked" if not unlocked else "")
            rows.append(ft.Container(
                content=ft.Row(
                    [
                        ft.Text(meta.icon, size=self._fs(18)),
                        ft.Column(
                            [
                                ft.Text(ex.title, size=self._fs(14), weight=ft.FontWeight.BOLD, color=theme.text),
                                ft.Text(
                                    f"{meta.title} · {ex.difficulty.replace('_', ' ').title()}",
                                    size=self._fs(11), color=theme.text_muted,
                                ),
                            ],
                            spacing=2, expand=True,
                        ),
                        ft.Text(status, size=self._fs(12), color=theme.success if done else theme.warning),
                    ],
                    spacing=10,
                ),
                bgcolor=theme.card, border_radius=10, padding=14,
                on_click=(lambda _e, eid=ex.id: self.page.go(f"/lesson/{eid}")) if unlocked else None,
                ink=unlocked, opacity=1.0 if unlocked else 0.6,
            ))
        self.results_column.controls = rows
