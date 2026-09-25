"""Daily Refresher: today's fixed cross-topic set (see
app.ui.app_state.resolve_daily_refresher) rendered with the same list
view as a plain category, under a summary card with a progress ring."""
from __future__ import annotations

import flet as ft

from app.ui.app_state import AppState
from app.ui.category_levels import build_exercise_list_view
from app.ui.components import card, progress_ring
from app.ui.theme import scaled


def build_daily_refresher_view(page: ft.Page, state: AppState) -> ft.View:
    theme = state.theme
    fs = lambda base: scaled(base, state.font_scale)  # noqa: E731
    exercises = state.daily_refresher_exercises()
    completed_ids = set(state.progress.get_completed_lesson_ids(state.language))
    done = sum(1 for ex in exercises if ex.id in completed_ids)
    total = len(exercises)

    if total and done == total:
        headline, detail = "All done for today!", "Come back tomorrow for a fresh set -- or keep going in Practice by Topic."
    elif total:
        headline, detail = f"{total - done} to go", "A short round-robin across your topics. Finish the set to keep your streak alive."
    else:
        headline, detail = "You're all caught up", "Every unlocked exercise is complete. Nice."

    summary = card(theme, fs, None, [
        ft.Row(
            [
                progress_ring(theme, fs, (done / total) if total else 1.0, theme.warning, size=84,
                              label=f"{done}/{total}", sublabel="today"),
                ft.Column(
                    [
                        ft.Text(headline, size=fs(20), weight=ft.FontWeight.BOLD, color=theme.text),
                        ft.Text(detail, size=fs(13), color=theme.text_muted),
                    ],
                    spacing=6, expand=True,
                ),
            ],
            spacing=20, vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    ], accent=theme.warning)

    return build_exercise_list_view(
        page, state, title="Daily Refresher", route="/daily", exercises=exercises, back_route="/hub",
        subtitle="Today's set stays fixed until midnight", summary=summary,
    )
