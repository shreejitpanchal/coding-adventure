"""Settings: theme presets and code font size."""
from __future__ import annotations

import flet as ft

from app.ui.app_state import AppState
from app.ui.theme import FONT_SIZE_SCALES, THEME_PRESETS, ThemePreset, scaled


def build_settings_view(page: ft.Page, state: AppState) -> ft.View:
    theme = state.theme
    fs = lambda base: scaled(base, state.font_scale)  # noqa: E731

    back_route = "/hub" if state.language else "/languages"

    header = ft.Row(
        [
            ft.Button(
                "← Back", on_click=lambda _e: page.go(back_route), height=44,
                style=ft.ButtonStyle(bgcolor=theme.text_muted, color="#FFFFFF"),
            ),
            ft.Text("Settings", size=fs(24), weight=ft.FontWeight.BOLD, color=theme.primary, expand=True),
        ],
        spacing=12,
    )

    return ft.View(
        route="/settings",
        bgcolor=theme.bg,
        scroll=ft.ScrollMode.AUTO,
        padding=ft.padding.Padding.only(left=24, top=24, right=24, bottom=40),
        controls=[header, _build_font_card(page, state), _build_theme_card(page, state)],
    )


_FONT_SIZE_LABELS = {"small": "Small", "medium": "Medium", "large": "Large"}


def _build_font_card(page: ft.Page, state: AppState) -> ft.Control:
    theme = state.theme
    fs = lambda base: scaled(base, state.font_scale)  # noqa: E731

    def select(size_key: str):
        def handler(_e=None) -> None:
            state.apply_font_size(size_key)
            page.views.clear()
            page.views.append(build_settings_view(page, state))
            page.update()
        return handler

    current = state.settings.code_font_size
    buttons = [
        ft.Button(
            label, on_click=select(key), height=40, disabled=current == key,
            style=ft.ButtonStyle(bgcolor=theme.primary if current == key else theme.text_muted, color="#FFFFFF"),
        )
        for key in FONT_SIZE_SCALES for label in [_FONT_SIZE_LABELS.get(key, key)]
    ]

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Code font size", size=fs(18), weight=ft.FontWeight.BOLD, color=theme.text),
                ft.Row(buttons, wrap=True, spacing=8),
            ],
            spacing=10,
        ),
        bgcolor=theme.card, border_radius=16, padding=20, margin=ft.margin.Margin.only(top=16),
    )


def _build_theme_card(page: ft.Page, state: AppState) -> ft.Control:
    theme = state.theme
    fs = lambda base: scaled(base, state.font_scale)  # noqa: E731
    current_key = state.settings.theme

    options = [_build_theme_option(page, state, preset, current_key == preset.key) for preset in THEME_PRESETS.values()]

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Theme", size=fs(18), weight=ft.FontWeight.BOLD, color=theme.text),
                ft.Row(options, wrap=True, spacing=16, run_spacing=16),
            ],
            spacing=10,
        ),
        bgcolor=theme.card, border_radius=16, padding=20, margin=ft.margin.Margin.only(top=16),
    )


def _build_theme_option(page: ft.Page, state: AppState, preset: ThemePreset, is_selected: bool) -> ft.Control:
    def select(_e=None) -> None:
        state.apply_theme(preset.key)
        page.views.clear()
        page.views.append(build_settings_view(page, state))
        page.bgcolor = state.theme.bg
        page.theme_mode = ft.ThemeMode.DARK if state.theme.is_dark else ft.ThemeMode.LIGHT
        page.update()

    swatches = ft.Row(
        [ft.Container(bgcolor=color, width=24, height=24, border_radius=6) for color in (preset.primary, preset.success, preset.warning, preset.danger)],
        spacing=6,
    )

    return ft.Container(
        content=ft.Column(
            [
                ft.Text(f"{preset.icon} {preset.title}", size=scaled(15, state.font_scale), weight=ft.FontWeight.BOLD, color=preset.text),
                swatches,
                ft.Button(
                    "Selected" if is_selected else "Select", disabled=is_selected, on_click=select, height=40,
                    style=ft.ButtonStyle(bgcolor=preset.primary, color="#FFFFFF"),
                ),
            ],
            spacing=8,
        ),
        bgcolor=preset.bg, border_radius=14, padding=16, width=220,
        border=ft.border.Border.all(3, state.theme.primary if is_selected else preset.card),
    )
