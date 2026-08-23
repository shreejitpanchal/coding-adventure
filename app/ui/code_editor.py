"""A plain monospace multiline code editor -- no live syntax highlighting;
Flet's TextField has no per-token tagging API for that. Good enough for a
"write, run, see the result" refresher loop."""
from __future__ import annotations

import flet as ft

from app.ui.theme import CODE_FONT_FAMILY

EDITOR_BGCOLOR = "#1E1E1E"
EDITOR_TEXT_COLOR = "#D4D4D4"


def make_code_editor(initial_code: str = "", height: int = 260, scale: float = 1.0) -> ft.TextField:
    return ft.TextField(
        value=initial_code,
        multiline=True,
        min_lines=8,
        max_lines=28,
        height=height,
        text_style=ft.TextStyle(
            font_family=CODE_FONT_FAMILY, size=max(1, round(14 * scale)), color=EDITOR_TEXT_COLOR,
        ),
        bgcolor=EDITOR_BGCOLOR,
        border_color="#3C3C3C",
    )


def make_read_only_code_block(code: str, scale: float = 1.0) -> ft.Control:
    return ft.Container(
        content=ft.Text(
            code, font_family=CODE_FONT_FAMILY, size=max(1, round(14 * scale)),
            color=EDITOR_TEXT_COLOR, selectable=True,
        ),
        bgcolor=EDITOR_BGCOLOR, border_radius=8, padding=14,
    )
