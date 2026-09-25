"""Language picker -- the screen shown at the start of every session
(after first-run setup), not just the first time. Deliberately not
auto-skipped by "last selected language" -- that value only pre-highlights
a card here.

Layout: a gradient hero greeting with cross-track stats, then a
responsive grid of track cards (signature colour, level ring, streak)
that lift on hover and fade in one after another."""
from __future__ import annotations

from typing import Optional

import flet as ft

from app.engine.languages import LANGUAGE_ORDER, LanguageInfo, get_language
from app.execution.android_platform import is_android
from app.execution.toolchain_check import check_toolchain, get_install_guide
from app.ui.app_state import AppState
from app.ui.components import (
    RADIUS,
    WHITE,
    button,
    chip,
    emoji_circle,
    icon_button,
    is_compact,
    progress_ring,
    route_handler,
    spacer,
    stat_pill,
    tint,
    view_padding,
)
from app.ui.motion import Stagger, hover_lift, shadow
from app.ui.theme import CODE_FONT_FAMILY, scaled

_TRACK_COL = {"xs": 12, "sm": 6, "md": 4, "lg": 3}


def build_language_select_view(page: ft.Page, state: AppState) -> ft.View:
    theme = state.theme
    fs = lambda base: scaled(base, state.font_scale)  # noqa: E731
    handle = state.settings.handle or "there"
    stagger = Stagger(page)

    hero = _build_hero(page, state, fs, handle)

    cards = [
        stagger.wrap(_build_language_card(page, state, get_language(key), fs), col=_TRACK_COL)
        for key in LANGUAGE_ORDER
    ]
    grid = ft.ResponsiveRow(cards, spacing=16, run_spacing=16)

    controls: list[ft.Control] = [
        stagger.wrap(hero, distance=0.03),
        spacer(20),
        stagger.wrap(ft.Row(
            [
                ft.Icon(ft.Icons.CATEGORY_ROUNDED, color=theme.primary, size=fs(20)),
                ft.Text("Pick a track", size=fs(20), weight=ft.FontWeight.BOLD, color=theme.text),
                ft.Text(f"{len(LANGUAGE_ORDER)} tracks · progress is kept separately for each",
                        size=fs(12), color=theme.text_muted),
            ],
            spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )),
        spacer(8),
        grid,
    ]
    stagger.play()

    return ft.View(
        route="/languages",
        bgcolor=theme.bg,
        scroll=ft.ScrollMode.AUTO,
        padding=view_padding(page),
        controls=controls,
    )


def _build_hero(page: ft.Page, state: AppState, fs, handle: str) -> ft.Control:
    """Gradient greeting with total XP, best streak, and a Continue link
    for the last-used track (only when there's something to continue)."""
    theme = state.theme
    available_keys = [key for key in LANGUAGE_ORDER if get_language(key).available]
    total_xp = sum(state.progress.get_player_level(key).total_xp for key in available_keys)
    best_streak = max((state.progress.get_streak_days(key) for key in available_keys), default=0)
    completed = sum(len(state.progress.get_completed_lesson_ids(key)) for key in available_keys)

    pills: list[ft.Control] = [
        stat_pill(theme, fs, ft.Icons.BOLT, f"{total_xp:,}", "total XP", theme.warning),
        stat_pill(theme, fs, ft.Icons.LOCAL_FIRE_DEPARTMENT, f"{best_streak}", "best streak", theme.danger),
        stat_pill(theme, fs, ft.Icons.TASK_ALT_ROUNDED, f"{completed}", "exercises done", theme.success),
    ]

    continue_link: Optional[ft.Control] = None
    last_language = state.language
    if last_language in available_keys:
        current_id = state.progress.get_current_exercise(last_language)
        if current_id:
            exercise = state.exercise_engine(last_language).get(current_id)
            if exercise is not None:
                info = get_language(last_language)

                def on_continue(_e: ft.ControlEvent, language=last_language, exercise_id=current_id) -> None:
                    state.select_language(language)
                    page.go(f"/lesson/{exercise_id}")

                continue_link = button(
                    f"Continue · {exercise.title}  ({info.title})", on_continue, theme, "ghost",
                    icon=ft.Icons.PLAY_ARROW_ROUNDED, height=46,
                )
    if continue_link is not None:
        pills.append(continue_link)

    greeting = "Welcome back" if total_xp or completed else "Welcome"
    compact = is_compact(page)
    return ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        *([] if compact else [ft.Container(
                            content=ft.Icon(ft.Icons.WAVING_HAND_ROUNDED, color=WHITE, size=fs(30)),
                            width=60, height=60, shape=ft.BoxShape.CIRCLE, bgcolor=tint(WHITE, 0.18),
                            alignment=ft.Alignment.CENTER,
                        )]),
                        ft.Column(
                            [
                                ft.Text(f"{greeting}, {handle}.", size=fs(30 if not compact else 24),
                                        weight=ft.FontWeight.BOLD, color=WHITE),
                                ft.Text("Ten focused minutes a day keeps every language sharp. What are we refreshing today?",
                                        size=fs(14), color=tint(WHITE, 0.88)),
                            ],
                            spacing=4, expand=True,
                        ),
                        icon_button(ft.Icons.SETTINGS_ROUNDED, route_handler(page, "/settings"), theme,
                                    color=WHITE, bgcolor=tint(WHITE, 0.18), tooltip="Settings"),
                    ],
                    spacing=18, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Row(pills, spacing=12, wrap=True, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ],
            spacing=18,
        ),
        gradient=ft.LinearGradient(begin=ft.Alignment.TOP_LEFT, end=ft.Alignment.BOTTOM_RIGHT,
                                   colors=[theme.gradient[0], theme.gradient[1]]),
        border_radius=RADIUS + 6, padding=ft.Padding.symmetric(horizontal=28, vertical=26),
        shadow=shadow(theme, blur=32, y=12, alpha=0.35, color=theme.gradient[0]),
    )


def _build_language_card(page: ft.Page, state: AppState, info: LanguageInfo, fs) -> ft.Control:
    theme = state.theme

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
    is_last = info.key == state.settings.last_selected_language

    level = state.progress.get_player_level(info.key) if info.available else None
    streak = state.progress.get_streak_days(info.key) if info.available else 0
    completed = len(state.progress.get_completed_lesson_ids(info.key)) if info.available else 0

    if not info.available:
        badge = chip("Coming soon", theme.text_muted, fs, icon=ft.Icons.HOURGLASS_TOP_ROUNDED)
    elif android_unsupported:
        badge = chip("Browse only", theme.warning, fs, icon=ft.Icons.MENU_BOOK_ROUNDED)
    elif not toolchain_ready:
        badge = chip("Toolchain needed", theme.warning, fs, icon=ft.Icons.ERROR_OUTLINE_ROUNDED)
    elif is_last:
        badge = chip("Last used", info.color, fs, icon=ft.Icons.HISTORY_ROUNDED, filled=True)
    else:
        badge = chip("Ready", theme.success, fs, icon=ft.Icons.CHECK_CIRCLE_ROUNDED)

    if level is not None:
        ring = progress_ring(
            theme, fs, level.xp_into_level / max(1, level.xp_needed_for_level), info.color,
            size=64, label=f"L{level.level}", sublabel="level", stroke=6,
        )
        stats = ft.Row(
            [
                ft.Icon(ft.Icons.LOCAL_FIRE_DEPARTMENT, color=theme.danger if streak else theme.text_muted, size=fs(16)),
                ft.Text(f"{streak}-day", size=fs(12), color=theme.text_muted),
                ft.Container(width=8),
                ft.Icon(ft.Icons.TASK_ALT_ROUNDED, color=theme.success if completed else theme.text_muted, size=fs(16)),
                ft.Text(f"{completed} done", size=fs(12), color=theme.text_muted),
            ],
            spacing=4, vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
    else:
        ring = ft.Container(width=64, height=64)
        stats = ft.Text(info.tagline, size=fs(12), color=theme.text_muted)

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

    card_body = ft.Column(
        [
            ft.Row(
                [emoji_circle(info.icon, info.color, fs, size=56, text_size=26), ft.Container(expand=True), ring],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Text(info.title, size=fs(20), weight=ft.FontWeight.BOLD, color=theme.text),
            ft.Text(info.tagline, size=fs(12), color=theme.text_muted, max_lines=3, overflow=ft.TextOverflow.ELLIPSIS),
            stats,
            badge,
        ],
        spacing=10,
    )

    container = ft.Container(
        content=card_body,
        bgcolor=theme.card, border_radius=RADIUS + 2, padding=20,
        border=ft.Border.all(2 if is_last else 1, info.color if is_last else tint(info.color, 0.35)),
        opacity=1.0 if info.available else 0.7,
        on_click=on_click, ink=info.available,
    )
    return hover_lift(container, theme, glow_color=info.color) if info.available else container


def _show_install_guide_dialog(page: ft.Page, state: AppState, info: LanguageInfo) -> None:
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
                    ft.Container(
                        content=ft.Text(str(i), size=fs(12), weight=ft.FontWeight.BOLD, color=WHITE),
                        width=24, height=24, shape=ft.BoxShape.CIRCLE, bgcolor=info.color, alignment=ft.Alignment.CENTER,
                    ),
                    ft.Text(step, size=fs(13), color=theme.text, expand=True, selectable=True),
                ],
                spacing=10, vertical_alignment=ft.CrossAxisAlignment.START,
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
                spacer(4),
                *step_rows,
                spacer(8),
                ft.Text("Verify it worked by running:", size=fs(12), color=theme.text_muted),
                ft.Container(
                    content=ft.Text(verify_command, size=fs(13), color=theme.text, selectable=True,
                                     font_family=CODE_FONT_FAMILY),
                    bgcolor=theme.surface, border_radius=8, padding=ft.Padding.symmetric(horizontal=10, vertical=6),
                ),
            ],
            spacing=8, tight=True,
        )

    dialog = ft.AlertDialog(
        modal=False,
        bgcolor=theme.card,
        title=ft.Row(
            [ft.Icon(ft.Icons.BUG_REPORT_ROUNDED, color=theme.warning),
             ft.Text(f"Install {info.title}'s toolchain", size=fs(18), weight=ft.FontWeight.BOLD, color=theme.text)],
            spacing=10,
        ),
        content=ft.Container(content=content, width=460),
        scrollable=True,
        actions=[
            button("Continue anyway", continue_anyway, theme, "ghost"),
            button("Got it", close, theme, "primary", icon=ft.Icons.CHECK_CIRCLE_ROUNDED),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.show_dialog(dialog)
