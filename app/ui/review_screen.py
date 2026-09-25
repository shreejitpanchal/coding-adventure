"""Review queue: every exercise whose spaced-repetition review is due
(see ProgressStore.schedule_review), most overdue first, rendered with
the shared exercise list under a summary card. Passing one pushes its
next review further out; failing one brings it back tomorrow."""
from __future__ import annotations

import flet as ft

from app.ui.app_state import AppState
from app.ui.category_levels import build_exercise_list_view
from app.ui.components import card, icon_circle, progress_ring, stat_pill
from app.ui.theme import scaled

_UPCOMING_DAYS = 7


def build_review_view(page: ft.Page, state: AppState) -> ft.View:
    theme = state.theme
    fs = lambda base: scaled(base, state.font_scale)  # noqa: E731
    exercises = state.due_review_exercises()
    due = len(exercises)
    upcoming = state.progress.count_upcoming_reviews(state.language, _UPCOMING_DAYS)
    completed_total = len(state.progress.get_completed_lesson_ids(state.language))

    if due == 0:
        headline = "Nothing due -- memory's holding."
        detail = (f"{upcoming} review{'s' if upcoming != 1 else ''} coming up in the next {_UPCOMING_DAYS} days."
                  if upcoming else "Complete a few exercises and they'll start showing up here on a spaced schedule.")
    else:
        headline = f"{due} to review"
        detail = ("Each pass pushes the next review further out (3 days, then a week, then longer). "
                  "Miss one and it comes back tomorrow.")

    summary = card(theme, fs, None, [
        ft.Row(
            [
                progress_ring(theme, fs, 1.0 if completed_total == 0 else 1 - due / max(1, completed_total), theme.accent,
                              size=84, label=str(due), sublabel="due", stroke=8)
                if due else icon_circle(ft.Icons.CHECK_CIRCLE_ROUNDED, theme.success, size=84, icon_size=fs(40)),
                ft.Column(
                    [
                        ft.Text(headline, size=fs(20), weight=ft.FontWeight.BOLD, color=theme.text),
                        ft.Text(detail, size=fs(13), color=theme.text_muted),
                        ft.Row(
                            [
                                stat_pill(theme, fs, ft.Icons.CALENDAR_MONTH_ROUNDED, str(upcoming),
                                          f"due in next {_UPCOMING_DAYS} days", theme.primary),
                                stat_pill(theme, fs, ft.Icons.TASK_ALT_ROUNDED, str(completed_total), "in rotation", theme.success),
                            ],
                            spacing=10, wrap=True,
                        ),
                    ],
                    spacing=8, expand=True,
                ),
            ],
            spacing=20, vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    ], accent=theme.accent)

    return build_exercise_list_view(
        page, state, title="Review Queue", route="/review", exercises=exercises, back_route="/hub",
        subtitle="Spaced repetition -- most overdue first", summary=summary,
    )
