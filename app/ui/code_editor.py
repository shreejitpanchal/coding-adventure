"""A plain monospace multiline code editor -- no live syntax highlighting;
Flet's TextField has no per-token tagging API for that. Good enough for a
"write, run, see the result" refresher loop."""
from __future__ import annotations

import flet as ft

from app.ui.theme import CODE_FONT_FAMILY, ThemePreset

# Fallback colors for call sites that don't have a ThemePreset handy --
# every real call site should pass one so code areas match the active
# theme (a fixed dark editor looked like a dark island on GitHub Light).
_FALLBACK_BGCOLOR = "#1E1E1E"
_FALLBACK_TEXT_COLOR = "#D4D4D4"


def make_code_editor(
    initial_code: str = "", height: int = 260, scale: float = 1.0, theme: ThemePreset | None = None,
) -> ft.TextField:
    bgcolor = theme.card if theme else _FALLBACK_BGCOLOR
    text_color = theme.text if theme else _FALLBACK_TEXT_COLOR
    border_color = theme.text_muted if theme else "#3C3C3C"
    return ft.TextField(
        value=initial_code,
        multiline=True,
        min_lines=8,
        max_lines=28,
        height=height,
        text_style=ft.TextStyle(
            font_family=CODE_FONT_FAMILY, size=max(1, round(14 * scale)), color=text_color,
        ),
        bgcolor=bgcolor,
        border_color=border_color,
    )


def make_read_only_code_block(code: str, scale: float = 1.0, theme: ThemePreset | None = None) -> ft.Control:
    bgcolor = theme.card if theme else _FALLBACK_BGCOLOR
    text_color = theme.text if theme else _FALLBACK_TEXT_COLOR
    return ft.Container(
        content=ft.Text(
            code, font_family=CODE_FONT_FAMILY, size=max(1, round(14 * scale)),
            color=text_color, selectable=True,
        ),
        bgcolor=bgcolor, border_radius=8, padding=14,
    )
