"""A plain monospace multiline code editor -- no live syntax highlighting;
Flet's TextField has no per-token tagging API for that. Good enough for a
"write, run, see the result" refresher loop. Both the editor and the
read-only block are dressed as a small "window": a title bar with the
three coloured dots and an optional filename label."""
from __future__ import annotations

from typing import Optional

import flet as ft

from app.ui.theme import CODE_FONT_FAMILY, ThemePreset

# Fallback colors for call sites that don't have a ThemePreset handy --
# every real call site should pass one so code areas match the active
# theme (a fixed dark editor looked like a dark island on GitHub Light).
_FALLBACK_BGCOLOR = "#1E1E1E"
_FALLBACK_TEXT_COLOR = "#D4D4D4"
_FALLBACK_MUTED = "#6B7280"

_DOTS = ("#FF5F57", "#FEBC2E", "#28C840")


def _window_bar(label: str, muted: str, scale: float = 1.0) -> ft.Container:
    return ft.Container(
        content=ft.Row(
            [
                *[ft.Container(width=11, height=11, shape=ft.BoxShape.CIRCLE, bgcolor=c) for c in _DOTS],
                ft.Container(width=6),
                ft.Text(label, size=max(1, round(11 * scale)), color=muted, font_family=CODE_FONT_FAMILY),
            ],
            spacing=6, vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.Padding.only(left=12, right=12, top=8, bottom=6),
    )


def _frame(theme: Optional[ThemePreset], bar_label: str, body: ft.Control, scale: float = 1.0) -> ft.Container:
    bgcolor = theme.surface if theme else _FALLBACK_BGCOLOR
    muted = theme.text_muted if theme else _FALLBACK_MUTED
    return ft.Container(
        content=ft.Column([_window_bar(bar_label, muted, scale), body], spacing=0),
        bgcolor=bgcolor, border_radius=14,
        border=ft.Border.all(1, ft.Colors.with_opacity(0.10, theme.text if theme else "white")),
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
    )


def make_code_editor(
    initial_code: str = "", height: int = 260, scale: float = 1.0, theme: ThemePreset | None = None,
    filename: str = "your_solution",
) -> ft.TextField:
    """The editable TextField itself (callers read/write `.value`). Wrap it
    with `frame_editor()` for the window look."""
    bgcolor = theme.surface if theme else _FALLBACK_BGCOLOR
    text_color = theme.text if theme else _FALLBACK_TEXT_COLOR
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
        border=ft.InputBorder.NONE,
        content_padding=ft.Padding.symmetric(horizontal=14, vertical=10),
        cursor_color=theme.primary if theme else "#61AFEF",
    )


def frame_editor(editor: ft.TextField, theme: ThemePreset | None = None, filename: str = "your_solution",
                 scale: float = 1.0) -> ft.Container:
    return _frame(theme, filename, editor, scale)


def make_read_only_code_block(code: str, scale: float = 1.0, theme: ThemePreset | None = None,
                              filename: str = "example") -> ft.Control:
    text_color = theme.text if theme else _FALLBACK_TEXT_COLOR
    body = ft.Container(
        content=ft.Text(
            code, font_family=CODE_FONT_FAMILY, size=max(1, round(14 * scale)),
            color=text_color, selectable=True,
        ),
        padding=ft.Padding.only(left=16, right=16, top=6, bottom=14),
    )
    return _frame(theme, filename, body, scale)
