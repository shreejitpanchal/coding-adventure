"""Language picker -- the screen shown at the start of every session
(after first-run setup), not just the first time. Deliberately not
auto-skipped by "last selected language" -- that value only pre-highlights
a card here."""
from __future__ import annotations

import flet as ft

from app.engine.languages import LANGUAGE_ORDER, get_language
from app.execution.android_platform import is_android
from app.execution.toolchain_check import check_toolchain, get_install_guide
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

    toolchain = check_toolchain(info.key) if info.available else None
    toolchain_ready = toolchain is None or toolchain.available
    # On Android, a missing Java/C++/Spring toolchain can never be
    # installed through this app (no javac/g++/mvn can exist there at
    # all) -- that's a structurally different situation from "not
    # installed yet on this desktop," so it gets its own messaging rather
    # than showing get_install_guide()'s desktop OS steps (which would be
    # actively wrong on a phone -- e.g. apt/winget commands with nowhere
    # to run them).
    android_unsupported = is_android() and not toolchain_ready and info.key != "python"

    subtitle: str
    if info.available:
        level = state.progress.get_player_level(info.key)
        streak = state.progress.get_streak_days(info.key)
        subtitle = f"Level {level.level} · {level.total_xp} XP · {streak}-day streak"
        if android_unsupported:
            subtitle = "Browse freely -- running code needs a desktop computer."
        elif not toolchain_ready:
            subtitle = f"{toolchain.install_hint}"
    else:
        subtitle = info.tagline

    if not info.available:
        badge_text, badge_bg, badge_color = "Coming soon", theme.card, theme.text_muted
    elif android_unsupported:
        badge_text, badge_bg, badge_color = "Desktop only", theme.text_muted, "#FFFFFF"
    elif not toolchain_ready:
        badge_text, badge_bg, badge_color = "Toolchain needed", theme.warning, "#FFFFFF"
    else:
        badge_text, badge_bg, badge_color = "Available", theme.success, "#FFFFFF"

    def on_click(_e: ft.ControlEvent) -> None:
        if not info.available:
            page.show_dialog(ft.SnackBar(ft.Text(f"{info.title} is coming soon.")))
            return
        # Browsing content (explanations, examples, editing code) never
        # needs a real toolchain -- only actually running code does, and
        # that's disabled directly on the Run button instead
        # (lesson_screen.py checks check_toolchain() itself), not blocked
        # here at the earlier "which language" step. On a desktop machine
        # genuinely missing the toolchain, show the install guide first
        # (it's fixable there); on Android, where it's never fixable, skip
        # straight to the hub instead of a dialog with nothing useful to say.
        if not toolchain_ready and not android_unsupported:
            _show_install_guide_dialog(page, state, info)
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
                    content=ft.Text(badge_text, size=fs(12), weight=ft.FontWeight.BOLD, color=badge_color),
                    bgcolor=badge_bg,
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


def _show_install_guide_dialog(page: ft.Page, state: AppState, info) -> None:
    """Shows a step-by-step, OS-specific install guide for a missing
    toolchain, with a "Continue anyway" escape hatch to the hub (the
    track just stays locked from actually running code until the
    toolchain shows up on PATH)."""
    theme = state.theme
    fs = lambda base: scaled(base, state.font_scale)  # noqa: E731

    guide = get_install_guide(info.key)

    def close(_e: ft.ControlEvent | None = None) -> None:
        page.pop_dialog()

    def continue_anyway(_e: ft.ControlEvent) -> None:
        page.pop_dialog()
        state.select_language(info.key)
        page.go("/hub")

    if guide is None:
        content: ft.Control = ft.Text(
            f"{info.title} needs a local toolchain that wasn't found on this computer.",
            size=fs(14), color=theme.text,
        )
    else:
        steps, verify_command = guide
        step_rows = [
            ft.Row(
                [
                    ft.Text(f"{i}.", size=fs(13), weight=ft.FontWeight.BOLD, color=theme.primary),
                    ft.Text(step, size=fs(13), color=theme.text, expand=True, selectable=True),
                ],
                spacing=8, vertical_alignment=ft.CrossAxisAlignment.START,
            )
            for i, step in enumerate(steps, start=1)
        ]
        content = ft.Column(
            [
                ft.Text(
                    f"{info.title} needs a toolchain that wasn't found on this computer. "
                    "Follow these steps, then relaunch the app:",
                    size=fs(13), color=theme.text_muted,
                ),
                ft.Container(height=4),
                *step_rows,
                ft.Container(height=8),
                ft.Text("Verify it worked by running:", size=fs(12), color=theme.text_muted),
                ft.Container(
                    content=ft.Text(verify_command, size=fs(13), color=theme.text, selectable=True,
                                     font_family="Consolas, 'Courier New', monospace"),
                    bgcolor=theme.bg, border_radius=6, padding=ft.padding.Padding.symmetric(horizontal=10, vertical=6),
                ),
            ],
            spacing=6, tight=True,
        )

    dialog = ft.AlertDialog(
        modal=False,
        bgcolor=theme.card,
        title=ft.Text(f"Install {info.title}'s toolchain", size=fs(18), weight=ft.FontWeight.BOLD, color=theme.text),
        content=ft.Container(content=content, width=440),
        scrollable=True,
        actions=[
            ft.Button("Continue anyway", on_click=continue_anyway,
                      style=ft.ButtonStyle(bgcolor=theme.text_muted, color="#FFFFFF")),
            ft.Button("Got it", on_click=close,
                      style=ft.ButtonStyle(bgcolor=theme.primary, color="#FFFFFF")),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.show_dialog(dialog)
