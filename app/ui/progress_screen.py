"""Per-track dashboard: level ring + animated XP bar, weekly stats, mastery
by topic, achievements, a 12-week activity heatmap, weakest quiz
concepts, and the recent activity feed."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import flet as ft

from app.config.clock import today as local_today
from app.engine.categories import get_category_meta
from app.engine.error_insights import summarize_errors
from app.ui.app_state import AppState
from app.ui.components import (
    RADIUS,
    WHITE,
    button,
    card,
    chip,
    header_row,
    icon_circle,
    progress_ring,
    route_handler,
    spacer,
    stat_pill,
    tint,
    view_padding,
    xp_bar,
)
from app.ui.motion import Stagger, fill_later, shadow
from app.ui.theme import scaled

_FAILURE_EVENT_TYPES = {"attempt_error", "attempt_wrong_output", "attempt_timeout", "attempt_blocked"}
_ACTIVITY_LOOKBACK_DAYS = 14
_ACTIVITY_DISPLAY_LIMIT = 15

# A concept needs at least this many recorded quiz answers before its
# accuracy is shown -- a single unlucky miss on a concept only asked once
# would otherwise look identical to a genuinely weak spot.
_MIN_CONCEPT_SAMPLES = 2
_WEAKEST_CONCEPTS_LIMIT = 5

_HEATMAP_WEEKS = 12
_HEATMAP_DAYS = _HEATMAP_WEEKS * 7


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


def _describe_activity(row, engine, theme) -> tuple[ft.IconData, str, str]:
    """(icon, colour, text) for one activity_log row."""
    event_type = row["event_type"]
    lesson_id = row["lesson_id"]
    detail = row["detail"] or ""
    exercise = engine.get(lesson_id) if lesson_id else None
    title = exercise.title if exercise else (lesson_id or "")

    if event_type == "lesson_completed":
        return ft.Icons.CHECK_CIRCLE_ROUNDED, theme.success, f'Completed "{title}"'
    if event_type == "badge_earned":
        return ft.Icons.MILITARY_TECH_ROUNDED, theme.warning, f"Earned achievement: {detail.replace('_', ' ').title()}"
    if event_type == "quiz_completed":
        return ft.Icons.QUIZ_ROUNDED, theme.accent, f"Quiz finished -- {detail}"
    if event_type == "hint_used":
        return ft.Icons.LIGHTBULB_ROUNDED, theme.warning, f'Used a hint on "{title}"'
    if event_type in _FAILURE_EVENT_TYPES:
        return ft.Icons.BUG_REPORT_ROUNDED, theme.danger, f'Attempt didn\'t pass on "{title}"'
    return ft.Icons.HISTORY_ROUNDED, theme.text_muted, f"{event_type}: {detail}" if detail else event_type


def _build_weakest_concepts_card(page: ft.Page, theme, fs, state: AppState) -> ft.Control:
    accuracy = state.progress.get_concept_accuracy(state.language)
    scored = [
        (tag, correct, total, correct / total)
        for tag, (correct, total) in accuracy.items()
        if total >= _MIN_CONCEPT_SAMPLES
    ]
    scored.sort(key=lambda row: row[3])
    weakest = scored[:_WEAKEST_CONCEPTS_LIMIT]

    completed_ids = set(state.progress.get_completed_lesson_ids(state.language))
    engine = state.exercise_engine()

    rows: list[ft.Control] = []
    for tag, correct, total, ratio in weakest:
        pct = round(100 * ratio)
        color = theme.danger if pct < 50 else theme.warning if pct < 80 else theme.success
        row_children: list[ft.Control] = [
            ft.Column(
                [
                    ft.Row([
                        ft.Text(tag.replace("_", " ").title(), size=fs(14), color=theme.text, expand=True),
                        ft.Text(f"{correct}/{total} · {pct}%", size=fs(12), color=theme.text_muted),
                    ]),
                    ft.ProgressBar(value=ratio, color=color, bgcolor=tint(color, 0.15), bar_height=6, border_radius=999),
                ],
                spacing=6, expand=True,
            ),
        ]
        suggestions = engine.recommend_practice_for_tags({tag}, completed_ids, limit=1)
        if suggestions:
            row_children.append(button(
                "Practice", lambda _e, eid=suggestions[0].id: page.go(f"/lesson/{eid}"), theme, "warning", height=34,
                icon=ft.Icons.SCHOOL_ROUNDED,
            ))
        rows.append(ft.Row(row_children, spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER))

    return card(theme, fs, "Weakest concepts", rows or [ft.Text(
        "Not enough quiz data yet -- answer a few more questions per concept to see this.",
        size=fs(13), color=theme.text_muted,
    )], icon=ft.Icons.PSYCHOLOGY, accent=theme.danger, title_size=16, spacing=12)


_ERROR_LOOKBACK_DAYS = 30


def _build_recurring_errors_card(page: ft.Page, theme, fs, state: AppState) -> ft.Control:
    """Which failure explanations keep coming back, with a practice link
    per bucket (by the affected exercises' concept tags, falling back to
    re-opening the most recently affected exercise)."""
    engine = state.exercise_engine()
    rows_in = state.progress.get_recent_errors(state.language, days=_ERROR_LOOKBACK_DAYS)
    insights = summarize_errors(rows_in, engine, state.language)
    completed_ids = set(state.progress.get_completed_lesson_ids(state.language))

    rows: list[ft.Control] = []
    for insight in insights:
        target_id = None
        suggestions = engine.recommend_practice_for_tags(set(insight.concept_tags[:3]), completed_ids, limit=1)
        if suggestions:
            target_id = suggestions[0].id
        elif insight.lesson_ids:
            target_id = insight.lesson_ids[0]
        affected = ", ".join(
            (engine.get(lid).title if engine.get(lid) else lid) for lid in insight.lesson_ids[:2]
        )
        if len(insight.lesson_ids) > 2:
            affected += f" +{len(insight.lesson_ids) - 2} more"
        row_children: list[ft.Control] = [
            ft.Container(
                content=ft.Text(f"×{insight.count}", size=fs(12), weight=ft.FontWeight.BOLD, color=WHITE),
                bgcolor=theme.danger if insight.count >= 5 else theme.warning, border_radius=999,
                padding=ft.Padding.symmetric(horizontal=10, vertical=4),
            ),
            ft.Column(
                [
                    ft.Text(insight.message, size=fs(14), weight=ft.FontWeight.BOLD, color=theme.text),
                    ft.Text(insight.hint, size=fs(12), color=theme.text_muted),
                    ft.Text(f"On: {affected}", size=fs(11), color=theme.text_muted) if affected else ft.Container(),
                ],
                spacing=2, expand=True,
            ),
        ]
        if target_id:
            row_children.append(button("Practice", lambda _e, eid=target_id: page.go(f"/lesson/{eid}"), theme, "warning",
                                       height=34, icon=ft.Icons.SCHOOL_ROUNDED))
        rows.append(ft.Row(row_children, spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER))

    return card(theme, fs, f"Recurring errors, last {_ERROR_LOOKBACK_DAYS} days", rows or [ft.Text(
        "No failed runs recorded yet -- when something keeps tripping you up, it'll show here with a practice link.",
        size=fs(13), color=theme.text_muted,
    )], icon=ft.Icons.BUG_REPORT_ROUNDED, accent=theme.warning, title_size=16, spacing=12)


def _heatmap_color(theme, count: int) -> str:
    if count <= 0:
        return tint(theme.text, 0.08)
    if count == 1:
        return tint(theme.success, 0.35)
    if count <= 3:
        return tint(theme.success, 0.65)
    return theme.success


def _build_activity_heatmap_card(theme, fs, state: AppState) -> ft.Control:
    counts = state.progress.get_daily_activity_counts(state.language, days=_HEATMAP_DAYS)
    today = local_today()
    start = today - timedelta(days=_HEATMAP_DAYS - 1)
    start -= timedelta(days=start.weekday())  # align to the Monday on/before start
    weeks = ((today - start).days // 7) + 1
    active_days = sum(1 for v in counts.values() if v)

    columns: list[ft.Control] = []
    for week in range(weeks):
        cells: list[ft.Control] = []
        for day_offset in range(7):
            day = start + timedelta(days=week * 7 + day_offset)
            if day > today:
                cells.append(ft.Container(width=15, height=15))
                continue
            count = counts.get(day.isoformat(), 0)
            cells.append(ft.Container(
                width=15, height=15, border_radius=4,
                bgcolor=_heatmap_color(theme, count),
                border=ft.Border.all(2, theme.primary) if day == today else None,
                tooltip=f"{day.isoformat()}: {count} event(s)",
            ))
        columns.append(ft.Column(cells, spacing=3))

    legend = ft.Row(
        [
            ft.Text("less", size=fs(10), color=theme.text_muted),
            *[ft.Container(width=12, height=12, border_radius=3, bgcolor=_heatmap_color(theme, n)) for n in (0, 1, 2, 4)],
            ft.Text("more", size=fs(10), color=theme.text_muted),
        ],
        spacing=4, vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return card(theme, fs, f"Activity, last {_HEATMAP_WEEKS} weeks", [
        ft.Text(f"{active_days} active days", size=fs(12), color=theme.text_muted),
        ft.Row(columns, spacing=3, scroll=ft.ScrollMode.AUTO),
        legend,
    ], icon=ft.Icons.CALENDAR_MONTH_ROUNDED, accent=theme.success, title_size=16)


def build_progress_view(page: ft.Page, state: AppState) -> ft.View:
    theme = state.theme
    fs = lambda base: scaled(base, state.font_scale)  # noqa: E731
    engine = state.exercise_engine()
    progress = state.progress
    completed_ids = set(progress.get_completed_lesson_ids(state.language))
    level = progress.get_player_level(state.language)
    streak = progress.get_streak_days(state.language)
    weekly = progress.get_weekly_summary(state.language)
    due_reviews = progress.count_due_reviews(state.language)
    upcoming_reviews = progress.count_upcoming_reviews(state.language, 7)
    freeze_tokens = progress.get_freeze_tokens(state.language)
    week_done = progress.count_completions_this_week(state.language)
    week_goal = max(1, state.settings.weekly_goal)
    stagger = Stagger(page)

    header = header_row(theme, fs, "Progress", route_handler(page, "/hub"), back_label="← Hub",
                        icon=ft.Icons.INSIGHTS, subtitle="Everything you've built up in this track")

    # -- level banner -------------------------------------------------------
    xp_track, xp_fill = xp_bar(theme, level.xp_into_level / max(1, level.xp_needed_for_level), width=360)
    banner = ft.Container(
        content=ft.Row(
            [
                progress_ring(theme, fs, level.xp_into_level / max(1, level.xp_needed_for_level), WHITE, size=96,
                              label=f"L{level.level}", sublabel="level", stroke=9),
                ft.Column(
                    [
                        ft.Text(f"Level {level.level}", size=fs(26), weight=ft.FontWeight.BOLD, color=WHITE),
                        ft.Text(f"{level.xp_into_level} / {level.xp_needed_for_level} XP to the next level · {level.total_xp:,} total",
                                size=fs(13), color=tint(WHITE, 0.88)),
                        xp_track,
                        ft.Row(
                            [
                                stat_pill(theme, fs, ft.Icons.LOCAL_FIRE_DEPARTMENT, f"{streak}",
                                          f"day streak · {freeze_tokens} freeze{'s' if freeze_tokens != 1 else ''}", theme.danger),
                                stat_pill(theme, fs, ft.Icons.TASK_ALT_ROUNDED, f"{weekly.lessons_completed}", "exercises this week", theme.success),
                                stat_pill(theme, fs, ft.Icons.QUIZ_ROUNDED, f"{weekly.quiz_attempts}", "quizzes this week", theme.accent),
                                stat_pill(theme, fs, ft.Icons.CALENDAR_MONTH_ROUNDED, f"{weekly.active_days}", "active days", theme.warning),
                                stat_pill(theme, fs, ft.Icons.REPLAY_ROUNDED, f"{due_reviews}",
                                          f"reviews due · {upcoming_reviews} this week", theme.primary),
                            ],
                            spacing=10, wrap=True,
                        ),
                    ],
                    spacing=10, expand=True,
                ),
            ],
            spacing=22, vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        gradient=ft.LinearGradient(begin=ft.Alignment.TOP_LEFT, end=ft.Alignment.BOTTOM_RIGHT,
                                   colors=[theme.gradient[0], theme.gradient[1]]),
        border_radius=RADIUS + 6, padding=24, shadow=shadow(theme, blur=32, y=12, alpha=0.35, color=theme.gradient[0]),
    )

    # -- mastery ---------------------------------------------------------
    mastery_rows: list[ft.Control] = []
    for category in engine.categories():
        meta = get_category_meta(category)
        items = engine.lessons_in_category(category)
        done = sum(1 for ex in items if ex.id in completed_ids)
        fraction = (done / len(items)) if items else 0
        pct = round(100 * fraction)
        mastery_rows.append(
            ft.Row(
                [
                    ft.Text(meta.icon, size=fs(18)),
                    ft.Column(
                        [
                            ft.Row([
                                ft.Text(meta.title, size=fs(14), color=theme.text, expand=True),
                                ft.Text(f"{done}/{len(items)} · {pct}%", size=fs(12), color=theme.text_muted),
                            ]),
                            ft.ProgressBar(value=fraction, bgcolor=tint(meta.color, 0.15), color=meta.color, bar_height=8,
                                           border_radius=999),
                        ],
                        spacing=5, expand=True,
                    ),
                    chip("Mastered", theme.success, fs, icon=ft.Icons.MILITARY_TECH_ROUNDED, filled=True)
                    if items and done == len(items) else ft.Container(width=0),
                ],
                spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
    mastery_card = card(theme, fs, "Mastery by topic", mastery_rows, icon=ft.Icons.TRENDING_UP_ROUNDED,
                        accent=theme.primary, title_size=16, spacing=12)

    # -- achievements ----------------------------------------------------
    badges = progress.get_badges_with_dates(state.language)
    badge_chips = [
        ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.MILITARY_TECH_ROUNDED, color=theme.warning, size=fs(16)),
                ft.Text(badge_id.replace("_", " ").title(), size=fs(12), weight=ft.FontWeight.BOLD, color=theme.text),
            ], spacing=6, tight=True),
            bgcolor=tint(theme.warning, 0.14), border=ft.Border.all(1, tint(theme.warning, 0.4)),
            border_radius=999, padding=ft.Padding.symmetric(horizontal=12, vertical=7),
            tooltip=f"Earned {_relative_time(earned_at)}",
        )
        for badge_id, earned_at in badges
    ]
    achievements_card = card(theme, fs, f"Achievements · {len(badges)}", [
        ft.Row(badge_chips, wrap=True, spacing=8) if badge_chips
        else ft.Row([
            icon_circle(ft.Icons.EMOJI_EVENTS, theme.text_muted, size=44),
            ft.Text("None yet -- solve a Gotcha Gauntlet puzzle or finish a topic to earn one.", size=fs(13),
                    color=theme.text_muted, expand=True),
        ], spacing=12),
    ], icon=ft.Icons.EMOJI_EVENTS, accent=theme.warning, title_size=16)

    # -- recent activity ---------------------------------------------------
    cutoff = (datetime.now(timezone.utc) - timedelta(days=_ACTIVITY_LOOKBACK_DAYS)).isoformat()
    recent_activity = progress.get_activity_since(state.language, cutoff)[:_ACTIVITY_DISPLAY_LIMIT]
    activity_rows: list[ft.Control] = []
    for row in recent_activity:
        icon, color, text = _describe_activity(row, engine, theme)
        activity_rows.append(ft.Row(
            [
                icon_circle(icon, color, size=32, icon_size=fs(16)),
                ft.Text(text, size=fs(13), color=theme.text, expand=True),
                ft.Text(_relative_time(row["timestamp"]), size=fs(11), color=theme.text_muted),
            ],
            spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ))
    activity_card = card(theme, fs, "Recent activity", activity_rows or [
        ft.Text("Nothing yet -- come back after your first exercise or quiz.", size=fs(13), color=theme.text_muted),
    ], icon=ft.Icons.HISTORY_ROUNDED, accent=theme.text_muted, title_size=16, spacing=10)

    heatmap_card = _build_activity_heatmap_card(theme, fs, state)
    weakest_concepts_card = _build_weakest_concepts_card(page, theme, fs, state)

    goal_fraction = min(1.0, week_done / week_goal)
    if week_done >= week_goal:
        goal_text = "Goal met -- anything more this week is a bonus."
    else:
        goal_text = f"{week_goal - week_done} more exercise{'s' if week_goal - week_done != 1 else ''} to hit this week's goal."
    goal_card = card(theme, fs, "This week", [
        ft.Row(
            [
                progress_ring(theme, fs, goal_fraction, theme.success, size=84, label=f"{week_done}/{week_goal}",
                              sublabel="exercises", stroke=8),
                ft.Column(
                    [
                        ft.Text(goal_text, size=fs(14), color=theme.text),
                        ft.Text(
                            f"Streak freezes: {freeze_tokens} of {3} held. One is earned every 7-day streak and "
                            "spent automatically to cover a single missed day.",
                            size=fs(12), color=theme.text_muted,
                        ),
                        button("Change weekly goal", route_handler(page, "/settings"), theme, "ghost",
                               icon=ft.Icons.SETTINGS_ROUNDED, height=36),
                    ],
                    spacing=8, expand=True,
                ),
            ],
            spacing=20, vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    ], icon=ft.Icons.FLAG_ROUNDED, accent=theme.success, title_size=16)

    review_card = card(theme, fs, "Review schedule", [
        ft.Text(
            "Passed exercises come back on a spaced schedule -- 3 days, then a week, then longer each time you "
            "still get them right. A miss brings one back tomorrow.",
            size=fs(13), color=theme.text_muted,
        ),
        ft.Row(
            [
                stat_pill(theme, fs, ft.Icons.REPLAY_ROUNDED, str(due_reviews), "due now", theme.accent),
                stat_pill(theme, fs, ft.Icons.CALENDAR_MONTH_ROUNDED, str(upcoming_reviews), "in the next 7 days", theme.primary),
                button("Open review queue", route_handler(page, "/review"), theme, "primary" if due_reviews else "ghost",
                       icon=ft.Icons.REPLAY_ROUNDED, height=40),
            ],
            spacing=10, wrap=True, vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    ], icon=ft.Icons.REPLAY_ROUNDED, accent=theme.accent, title_size=16)

    errors_card = _build_recurring_errors_card(page, theme, fs, state)
    two_up = ft.ResponsiveRow(
        [
            stagger.wrap(achievements_card, col={"xs": 12, "lg": 6}),
            stagger.wrap(weakest_concepts_card, col={"xs": 12, "lg": 6}),
        ],
        spacing=16, run_spacing=16,
    )

    controls: list[ft.Control] = [
        header, spacer(8),
        stagger.wrap(banner, distance=0.03), spacer(4),
        ft.ResponsiveRow(
            [stagger.wrap(goal_card, col={"xs": 12, "lg": 6}), stagger.wrap(review_card, col={"xs": 12, "lg": 6})],
            spacing=16, run_spacing=16,
        ), spacer(4),
        stagger.wrap(mastery_card), spacer(4),
        two_up, spacer(4),
        stagger.wrap(errors_card), spacer(4),
        stagger.wrap(heatmap_card), spacer(4),
        stagger.wrap(activity_card),
    ]
    stagger.play()

    fill_later(page, xp_fill, width=xp_fill.data, delay=0.3)

    return ft.View(
        route="/progress",
        bgcolor=theme.bg,
        scroll=ft.ScrollMode.AUTO,
        padding=view_padding(),
        controls=controls,
    )
