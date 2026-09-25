"""Exercise search: find any exercise by title, objective, or concept
tag, optionally filtered by difficulty -- a flat lookup across the whole
track's content, useful once a track has hundreds of exercises spread
across many categories."""
from __future__ import annotations

from typing import Optional

import flet as ft

from app.engine.categories import get_category_meta
from app.engine.exercise import DIFFICULTIES
from app.ui.app_state import AppState
from app.ui.components import (
    RADIUS_SM,
    button,
    button_style,
    chip,
    difficulty_color,
    difficulty_label,
    empty_state,
    emoji_circle,
    header_row,
    route_handler,
    spacer,
    tint,
    view_padding,
)
from app.ui.motion import hover_lift
from app.ui.theme import scaled


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
        header = header_row(theme, self._fs, "Search Exercises", route_handler(self.page, "/hub"), back_label="← Hub",
                            icon=ft.Icons.SEARCH_ROUNDED, subtitle=f"{len(self.engine)} exercises in this track")

        self.search_field = ft.TextField(
            hint_text='Search by title, objective, or concept (e.g. "closures")...',
            on_change=self._on_query_change, autofocus=True, prefix_icon=ft.Icons.SEARCH_ROUNDED,
            border_radius=14, bgcolor=theme.card, border_color=tint(theme.text, 0.12),
            focused_border_color=theme.primary, text_size=self._fs(15),
        )

        filter_buttons = [self._make_difficulty_button(None, "All")]
        filter_buttons.extend(self._make_difficulty_button(d, difficulty_label(d)) for d in DIFFICULTIES)

        self.count_text = ft.Text("", size=self._fs(12), color=theme.text_muted)
        self.results_column = ft.Column([], spacing=8)
        self._render_results()

        return ft.View(
            route="/search",
            bgcolor=theme.bg,
            scroll=ft.ScrollMode.AUTO,
            padding=view_padding(self.page),
            controls=[
                header, spacer(8),
                self.search_field,
                ft.Row([*filter_buttons, self.count_text], spacing=8, wrap=True,
                       vertical_alignment=ft.CrossAxisAlignment.CENTER),
                spacer(8),
                self.results_column,
            ],
        )

    def _make_difficulty_button(self, difficulty: Optional[str], label: str) -> ft.Button:
        theme = self.theme

        def on_click(_e: ft.ControlEvent) -> None:
            self.difficulty_filter = difficulty
            for d, b in self.difficulty_buttons.items():
                b.disabled = d == difficulty
                b.style = button_style(theme, "primary" if d == difficulty else "ghost")
            self._render_results()
            self.page.update()

        control = button(
            label, on_click, theme, "primary" if difficulty is None else "ghost",
            height=36, disabled=difficulty is None,
        )
        self.difficulty_buttons[difficulty] = control
        return control

    def _on_query_change(self, e: ft.ControlEvent) -> None:
        self._render_results()
        self.page.update()

    def _render_results(self) -> None:
        theme = self.theme
        query = self.search_field.value or ""
        results = self.engine.search(query, difficulty=self.difficulty_filter)
        self.count_text.value = f"{len(results)} result{'s' if len(results) != 1 else ''}" if (query or self.difficulty_filter) else ""

        if not results:
            self.results_column.controls = [empty_state(
                theme, self._fs, ft.Icons.SEARCH_ROUNDED,
                "No matching exercises" if query or self.difficulty_filter else "Type to search",
                "Try a different word, or pick a difficulty above." if query or self.difficulty_filter
                else "Titles, objectives and concept tags are all searched.",
            )]
            return

        rows: list[ft.Control] = []
        for ex in results:
            meta = get_category_meta(ex.category)
            unlocked = self.engine.is_unlocked(ex, self.completed_ids)
            done = ex.id in self.completed_ids
            if done:
                status: ft.Control = chip("Done", theme.success, self._fs, icon=ft.Icons.CHECK_CIRCLE_ROUNDED)
            elif not unlocked:
                status = chip("Locked", theme.text_muted, self._fs, icon=ft.Icons.LOCK_ROUNDED)
            else:
                status = ft.Icon(ft.Icons.CHEVRON_RIGHT_ROUNDED, color=theme.text_muted, size=self._fs(22))
            row = ft.Container(
                content=ft.Row(
                    [
                        emoji_circle(meta.icon, meta.color, self._fs, size=42, text_size=18),
                        ft.Column(
                            [
                                ft.Text(ex.title, size=self._fs(14), weight=ft.FontWeight.BOLD,
                                        color=theme.text if unlocked else theme.text_muted),
                                ft.Row([
                                    chip(meta.title, meta.color, self._fs),
                                    chip(difficulty_label(ex.difficulty), difficulty_color(theme, ex.difficulty), self._fs),
                                ], spacing=6, wrap=True),
                            ],
                            spacing=4, expand=True,
                        ),
                        status,
                    ],
                    spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor=theme.card, border_radius=RADIUS_SM + 2, padding=ft.Padding.symmetric(horizontal=14, vertical=12),
                border=ft.Border.all(1, tint(meta.color, 0.25)),
                on_click=(lambda _e, eid=ex.id: self.page.go(f"/lesson/{eid}")) if unlocked else None,
                ink=unlocked, opacity=1.0 if unlocked else 0.6,
            )
            rows.append(hover_lift(row, theme, scale=1.01, glow_color=meta.color) if unlocked else row)
        self.results_column.controls = rows
