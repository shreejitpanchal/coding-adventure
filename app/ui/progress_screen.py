"""Per-track dashboard: streak, XP, mastery by topic, achievements."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import flet as ft

from app.engine.categories import get_category_meta
from app.ui.app_state import AppState
from app.ui.theme import scaled

_FAILURE_EVENT_TYPES = {"attempt_error", "attempt_wrong_output", "attempt_timeout", "attempt_blocked"}
_ACTIVITY_LOOKBACK_DAYS = 14
_ACTIVITY_DISPLAY_LIMIT = 15


def _relative_time(iso_timestamp: str) -> str:
    dt = datetime.fromisoformat(iso_timestamp)
    seconds = (datetime.now(timezone.utc) - dt).total_seconds()
    if seconds < 60:
        return "just now"
    if seconds < 3600:
        return f"{int(seconds // 60)}m ago"
    if seconds < 86400:
        return f"{int(seconds // 3600)}h ago"
    return f"{int(seconds // 86400)}d ago"


def _describe_activity(row, engine) -> str:
    event_type = row["event_type"]
    lesson_id = row["lesson_id"]
    detail = row["detail"] or ""
    exercise = engine.get(lesson_id) if lesson_id else None
    title = exercise.title if exercise else (lesson_id or "")

    if event_type == "lesson_completed":
        return f'✓ Completed "{title}"'
    if event_type == "badge_earned":
        return f"🏆 Earned achievement: {detail.replace('_', ' ').title()}"
    if event_type == "quiz_completed":
        return f"❓ Quiz finished -- {detail}"
    if event_type == "hint_used":
        return f'💡 Used a hint on "{title}"'
    if event_type in _FAILURE_EVENT_TYPES:
        return f'✗ Attempt didn\'t pass on "{title}"'
    return f"{event_type}: {detail}" if detail else event_type


def build_progress_view(page: ft.Page, state: AppState) -> ft.View:
    theme = state.theme
    fs = lambda base: scaled(base, state.font_scale)  # noqa: E731
    engine = state.exercise_engine()
    progress = state.progress
    completed_ids = set(progress.get_completed_lesson_ids(state.language))
    level = progress.get_player_level(state.language)
    streak = progress.get_streak_days(state.language)
    weekly = progress.get_weekly_summary(state.language)

    header = ft.Row(
        [
            ft.Button(
                "← Hub", on_click=lambda _e: page.go("/hub"), height=44,
                style=ft.ButtonStyle(bgcolor=theme.text_muted, color="#FFFFFF"),
            ),
            ft.Text("Progress", size=fs(24), weight=ft.FontWeight.BOLD, color=theme.primary, expand=True),
        ],
        spacing=12,
    )

    xp_card = ft.Container(
        content=ft.Column(
            [
                ft.Text(f"Level {level.level}", size=fs(22), weight=ft.FontWeight.BOLD, color=theme.text),
                ft.Text(
                    f"{level.xp_into_level} / {level.xp_needed_for_level} XP to next level "
                    f"({level.total_xp} total)",
                    size=fs(13), color=theme.text_muted,
                ),
                ft.Text(f"{streak}-day streak", size=fs(13), color=theme.text_muted),
                ft.Text(
                    f"This week: {weekly.lessons_completed} exercises, "
                    f"{weekly.quiz_attempts} quizzes, {weekly.badges_earned} achievements, "
                    f"{weekly.active_days} active days",
                    size=fs(13), color=theme.text_muted,
                ),
            ],
            spacing=6,
        ),
        bgcolor=theme.card, border_radius=16, padding=20,
    )

    mastery_rows = []
    for category in engine.categories():
        meta = get_category_meta(category)
        items = engine.lessons_in_category(category)
        done = sum(1 for ex in items if ex.id in completed_ids)
        fraction = (done / len(items)) if items else 0
        pct = round(100 * fraction)
        mastery_rows.append(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(f"{meta.icon} {meta.title}", size=fs(14), color=theme.text, expand=True),
                            ft.Text(f"{done}/{len(items)} ({pct}%)", size=fs(13), color=theme.text_muted),
                        ],
                    ),
                    ft.ProgressBar(value=fraction, bgcolor=theme.bg, color=meta.color, height=8, border_radius=4),
                ],
                spacing=4,
            )
        )
    mastery_card = ft.Container(
        content=ft.Column(
            [ft.Text("Mastery by topic", size=fs(16), weight=ft.FontWeight.BOLD, color=theme.text), *mastery_rows],
            spacing=8,
        ),
        bgcolor=theme.card, border_radius=16, padding=20,
    )

    badges = progress.get_badges_with_dates(state.language)
    badge_chips = [
        ft.Container(
            content=ft.Text(badge_id.replace("_", " ").title(), size=fs(12), color="#FFFFFF"),
            bgcolor=theme.success, border_radius=8, padding=ft.padding.Padding.symmetric(horizontal=10, vertical=6),
        )
        for badge_id, _ in badges
    ]
    achievements_card = ft.Container(
        content=ft.Column(
            [
                ft.Text("Achievements", size=fs(16), weight=ft.FontWeight.BOLD, color=theme.text),
                ft.Row(badge_chips, wrap=True, spacing=8) if badge_chips
                else ft.Text("None yet -- solve a Gotcha Gauntlet puzzle or finish a topic to earn one.", size=fs(13), color=theme.text_muted),
            ],
            spacing=10,
        ),
        bgcolor=theme.card, border_radius=16, padding=20,
    )

    cutoff = (datetime.now(timezone.utc) - timedelta(days=_ACTIVITY_LOOKBACK_DAYS)).isoformat()
    recent_activity = progress.get_activity_since(state.language, cutoff)[:_ACTIVITY_DISPLAY_LIMIT]
    activity_rows = [
        ft.Row(
            [
                ft.Text(_describe_activity(row, engine), size=fs(13), color=theme.text, expand=True),
                ft.Text(_relative_time(row["timestamp"]), size=fs(11), color=theme.text_muted),
            ],
            spacing=8,
        )
        for row in recent_activity
    ]
    activity_card = ft.Container(
        content=ft.Column(
            [
                ft.Text("Recent activity", size=fs(16), weight=ft.FontWeight.BOLD, color=theme.text),
                *(activity_rows if activity_rows
                  else [ft.Text("Nothing yet -- come back after your first exercise or quiz.", size=fs(13), color=theme.text_muted)]),
            ],
            spacing=8,
        ),
        bgcolor=theme.card, border_radius=16, padding=20,
    )

    return ft.View(
        route="/progress",
        bgcolor=theme.bg,
        scroll=ft.ScrollMode.AUTO,
        padding=ft.padding.Padding.only(left=24, top=24, right=24, bottom=40),
        controls=[
            header, ft.Container(height=12), xp_card, ft.Container(height=12), mastery_card,
            ft.Container(height=12), achievements_card, ft.Container(height=12), activity_card,
        ],
    )
