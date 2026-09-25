"""First-run setup: just a display name, nothing else -- on a full-bleed
gradient with a spring-in welcome card."""
from __future__ import annotations

import flet as ft

from app.engine.languages import LANGUAGE_ORDER, get_language
from app.ui.app_state import AppState
from app.ui.components import RADIUS, WHITE, button, is_compact, spacer, tint
from app.ui.motion import glow, pop_in, prepare_pop
from app.ui.theme import scaled


def build_setup_wizard_view(page: ft.Page, state: AppState) -> ft.View:
    theme = state.theme
    fs = lambda base: scaled(base, state.font_scale)  # noqa: E731

    name_field = ft.TextField(
        hint_text="e.g. Alex", width=340, text_align=ft.TextAlign.CENTER, autofocus=True, border_radius=14,
        bgcolor=theme.surface, border_color=tint(theme.text, 0.15), focused_border_color=theme.primary,
        text_size=fs(16),
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

    track_row = ft.Row(
        [
            ft.Container(
                content=ft.Text(get_language(key).icon, size=fs(20)),
                width=40, height=40, shape=ft.BoxShape.CIRCLE, bgcolor=tint(get_language(key).color, 0.22),
                alignment=ft.Alignment.CENTER, tooltip=get_language(key).title,
            )
            for key in LANGUAGE_ORDER
        ],
        spacing=8, alignment=ft.MainAxisAlignment.CENTER,
    )

    card_body = ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Icon(ft.Icons.ROCKET_LAUNCH, color=WHITE, size=fs(40)),
                    width=84, height=84, shape=ft.BoxShape.CIRCLE,
                    gradient=ft.LinearGradient(begin=ft.Alignment.TOP_LEFT, end=ft.Alignment.BOTTOM_RIGHT,
                                               colors=[theme.gradient[0], theme.gradient[1]]),
                    alignment=ft.Alignment.CENTER, shadow=glow(theme.gradient[0], alpha=0.5),
                ),
                ft.Text("Coding Adventure", size=fs(34), weight=ft.FontWeight.BOLD, color=theme.text),
                ft.Text(
                    "A focused, offline refresher for professionals -- seven tracks, real toolchains, "
                    "and a little XP to keep it fun.",
                    size=fs(14), color=theme.text_muted, text_align=ft.TextAlign.CENTER,
                ),
                track_row,
                spacer(12),
                ft.Text("What should we call you?", size=fs(18), weight=ft.FontWeight.BOLD, color=theme.text),
                name_field,
                error_text,
                button("Let's go", finish, theme, "primary", icon=ft.Icons.ARROW_FORWARD_ROUNDED, width=220, height=52),
            ],
            spacing=12, horizontal_alignment=ft.CrossAxisAlignment.CENTER, tight=True,
        ),
        bgcolor=theme.card, border_radius=RADIUS + 8,
        padding=ft.Padding.symmetric(horizontal=48 if not is_compact(page) else 20, vertical=40),
        width=min(560, int(page.width) - 32) if page.width else 560,
        shadow=glow(theme.gradient[1], alpha=0.25, blur=48),
    )
    prepare_pop(card_body)
    pop_in(page, card_body)

    return ft.View(
        route="/setup",
        bgcolor=theme.bg,
        padding=0,
        controls=[
            ft.Container(
                content=card_body, alignment=ft.Alignment.CENTER, expand=True, padding=40 if not is_compact(page) else 12,
                gradient=ft.LinearGradient(
                    begin=ft.Alignment.TOP_LEFT, end=ft.Alignment.BOTTOM_RIGHT,
                    colors=[tint(theme.gradient[0], 0.35), theme.bg, tint(theme.gradient[1], 0.35)],
                ),
            ),
        ],
    )
