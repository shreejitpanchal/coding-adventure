"""First-run setup: just a display name, nothing else."""
from __future__ import annotations

import flet as ft

from app.ui.app_state import AppState
from app.ui.theme import scaled


def build_setup_wizard_view(page: ft.Page, state: AppState) -> ft.View:
    theme = state.theme
    fs = lambda base: scaled(base, state.font_scale)  # noqa: E731

    name_field = ft.TextField(
        hint_text="e.g. Alex", width=340, text_align=ft.TextAlign.CENTER, autofocus=True,
    )
    error_text = ft.Text("", color=theme.danger, size=fs(13))

    def finish(_e=None) -> None:
        handle = (name_field.value or "").strip()
        if not handle:
            error_text.value = "Enter a name to continue."
            page.update()
            return
        state.settings.handle = handle
        state.settings.setup_complete = True
        state.save_settings()
        page.go("/languages")

    name_field.on_submit = finish

    body = ft.Column(
        [
            ft.Text("Coding Adventure", size=fs(34), weight=ft.FontWeight.BOLD, color=theme.primary),
            ft.Text(
                "A focused, offline refresher for Python, Java, C++, and Spring.",
                size=fs(15), color=theme.text_muted,
            ),
            ft.Container(height=20),
            ft.Text("What should we call you?", size=fs(18), weight=ft.FontWeight.BOLD, color=theme.text),
            ft.Container(height=8),
            name_field,
            error_text,
            ft.Container(height=8),
            ft.Button(
                "Continue →", width=200, height=52, on_click=finish,
                style=ft.ButtonStyle(bgcolor=theme.primary, color="#FFFFFF"),
            ),
        ],
        spacing=6, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return ft.View(
        route="/setup",
        bgcolor=theme.bg,
        controls=[
            ft.Container(content=body, alignment=ft.alignment.Alignment.CENTER, expand=True, padding=60),
        ],
    )
