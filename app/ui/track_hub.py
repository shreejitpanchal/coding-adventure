"""Per-language hub: the top of one track's navigation -- Daily Refresher,
Practice by Topic, the flagship Gotcha Gauntlet debug-puzzle track, Quiz
Bank, Progress and Search, under a gradient banner showing level, XP and
streak for this track."""
from __future__ import annotations

import flet as ft

from app.engine.categories import GOTCHA_CATEGORY
from app.engine.languages import get_language
from app.ui.app_state import AppState
from app.ui.components import (
    RADIUS,
    WHITE,
    button,
    card,
    emoji_circle,
    icon_button,
    is_compact,
    nav_tile,
    progress_ring,
    route_handler,
    spacer,
    stat_pill,
    tint,
    view_padding,
    xp_bar,
)
from app.ui.motion import Stagger, fill_later, shadow
from app.ui.shortcuts import Shortcuts
from app.ui.theme import scaled

_TILE_COL = {"xs": 12, "md": 6, "xl": 4}


def build_track_hub_view(page: ft.Page, state: AppState) -> ft.View:
    theme = state.theme
    fs = lambda base: scaled(base, state.font_scale)  # noqa: E731
    language = get_language(state.language)
    engine = state.exercise_engine()
    completed_ids = set(state.progress.get_completed_lesson_ids(state.language))
    level = state.progress.get_player_level(state.language)
    streak = state.progress.get_streak_days(state.language)
    freeze_tokens = state.progress.get_freeze_tokens(state.language)
    week_done = state.progress.count_completions_this_week(state.language)
    week_goal = max(1, state.settings.weekly_goal)
    stagger = Stagger(page)

    # -- banner -----------------------------------------------------------
    compact = is_compact(page)
    bar_width = 340 if not compact else max(160, int((page.width or 360) - 120))
    xp_track, xp_fill = xp_bar(theme, level.xp_into_level / max(1, level.xp_needed_for_level), width=bar_width,
                               color=language.color)
    back_btn = icon_button(ft.Icons.ARROW_BACK_ROUNDED, route_handler(page, "/languages"), theme,
                           color=WHITE, bgcolor=tint(WHITE, 0.18), tooltip="All tracks")
    settings_btn = icon_button(ft.Icons.SETTINGS_ROUNDED, route_handler(page, "/settings"), theme,
                               color=WHITE, bgcolor=tint(WHITE, 0.18), tooltip="Settings")
    emoji = emoji_circle(language.icon, WHITE, fs, size=60, text_size=30)
    title_col = ft.Column(
        [
            ft.Text(f"{language.title} track", size=fs(30 if not compact else 24), weight=ft.FontWeight.BOLD, color=WHITE),
            ft.Text(language.tagline, size=fs(13), color=tint(WHITE, 0.88), max_lines=3, overflow=ft.TextOverflow.ELLIPSIS),
        ],
        spacing=4, expand=True,
    )
    ring = progress_ring(theme, fs, len(completed_ids) / max(1, len(engine)), WHITE, size=78,
                         label=f"{round(100 * len(completed_ids) / max(1, len(engine)))}%", sublabel="complete")
    pills = [
        stat_pill(theme, fs, ft.Icons.WORKSPACE_PREMIUM, f"Level {level.level}",
                  f"{level.xp_into_level}/{level.xp_needed_for_level} XP to next", theme.warning),
        stat_pill(theme, fs, ft.Icons.LOCAL_FIRE_DEPARTMENT, f"{streak}",
                  f"day streak · {freeze_tokens} freeze{'s' if freeze_tokens != 1 else ''}", theme.danger),
        stat_pill(theme, fs, ft.Icons.FLAG_ROUNDED, f"{week_done}/{week_goal}",
                  "weekly goal" if week_done < week_goal else "weekly goal · done!", theme.success),
        stat_pill(theme, fs, ft.Icons.BOLT, f"{level.total_xp:,}", "total XP", theme.warning),
        ft.Column([ft.Text("Progress to next level", size=fs(11), color=tint(WHITE, 0.85)), xp_track], spacing=6),
    ]
    if compact:
        # Phone: the title keeps the full width; emoji + ring share a row below it.
        banner_rows: list[ft.Control] = [
            ft.Row([back_btn, title_col, settings_btn], spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Row([emoji, ring], spacing=20, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Row(pills, spacing=10, wrap=True, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        ]
    else:
        banner_rows = [
            ft.Row([back_btn, emoji, title_col, ring, settings_btn], spacing=16,
                   vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Row(pills, spacing=12, wrap=True, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        ]
    banner = ft.Container(
        content=ft.Column(banner_rows, spacing=18),
        gradient=ft.LinearGradient(begin=ft.Alignment.TOP_LEFT, end=ft.Alignment.BOTTOM_RIGHT,
                                   colors=[language.color, theme.gradient[1]]),
        border_radius=RADIUS + 6, padding=ft.Padding.symmetric(horizontal=26 if not compact else 18, vertical=24),
        shadow=shadow(theme, blur=32, y=12, alpha=0.35, color=language.color),
    )

    # -- tiles ------------------------------------------------------------
    daily = state.daily_refresher_exercises()
    daily_done = sum(1 for ex in daily if ex.id in completed_ids)
    if not daily:
        daily_status = "All caught up"
    elif daily_done == len(daily):
        daily_status = "All done today!"
    else:
        daily_status = f"{daily_done}/{len(daily)} done today"
    daily_bar = ft.ProgressBar(value=(daily_done / len(daily)) if daily else 1.0, color=theme.warning,
                               bgcolor=tint(theme.warning, 0.15), bar_height=6, border_radius=999, width=200)

    gotcha_items = engine.lessons_in_category(GOTCHA_CATEGORY)
    gotcha_done = sum(1 for ex in gotcha_items if ex.id in completed_ids)
    quiz_engine = state.quiz_engine()
    best = state.progress.get_best_quiz_score(state.language)
    quiz_status = f"Best score {best[0]}/{best[1]}" if best else f"{len(quiz_engine)} questions ready"

    due_reviews = state.progress.count_due_reviews(state.language)
    upcoming_reviews = state.progress.count_upcoming_reviews(state.language, 7)
    if due_reviews:
        review_status = f"{due_reviews} due now"
    elif upcoming_reviews:
        review_status = f"Nothing due · {upcoming_reviews} this week"
    else:
        review_status = "Complete exercises to start the schedule"

    tiles = [
        nav_tile(page, theme, fs, icon=ft.Icons.TODAY_ROUNDED, title="Daily Refresher",
                 subtitle=f"{state.settings.daily_refresher_size} exercises across every topic to keep everything warm.",
                 status=daily_status, route="/daily", color=theme.warning, extra=daily_bar),
        nav_tile(page, theme, fs, icon=ft.Icons.REPLAY_ROUNDED, title="Review Queue",
                 subtitle="Spaced repetition: exercises you've passed come back just before you'd forget them.",
                 status=review_status, route="/review", color=theme.accent),
        nav_tile(page, theme, fs, icon=ft.Icons.CATEGORY_ROUNDED, title="Practice by Topic",
                 subtitle="Browse every category and work through it at your own pace.",
                 status=f"{len(engine.categories())} topics", route="/categories", color=theme.primary),
        nav_tile(page, theme, fs, icon=ft.Icons.BUG_REPORT_ROUNDED, title="Gotcha Gauntlet",
                 subtitle="Find-the-bug puzzles covering the mistakes that trip up even senior engineers.",
                 status=f"{gotcha_done}/{len(gotcha_items)} solved" if gotcha_items else "Coming soon",
                 route=f"/categories/{GOTCHA_CATEGORY}", color=theme.danger),
        nav_tile(page, theme, fs, icon=ft.Icons.QUIZ_ROUNDED, title="Quiz Bank",
                 subtitle="Randomized multiple-choice questions across the whole track.",
                 status=quiz_status, route="/quiz", color=language.color),
        nav_tile(page, theme, fs, icon=ft.Icons.INSIGHTS, title="Progress",
                 subtitle="Streak, XP, mastery by topic, weakest concepts, and achievements.",
                 status=f"{len(completed_ids)}/{len(engine)} exercises completed", route="/progress", color=theme.success),
        nav_tile(page, theme, fs, icon=ft.Icons.SEARCH_ROUNDED, title="Search",
                 subtitle="Find any exercise by title, objective, or concept tag.",
                 status=f"{len(engine)} exercises", route="/search", color=theme.text_muted),
    ]
    grid = ft.ResponsiveRow([stagger.wrap(t, col=_TILE_COL) for t in tiles], spacing=16, run_spacing=16)

    # Digits jump straight to a tile, in the order shown; Escape returns to the picker.
    tile_routes = ["/daily", "/review", "/categories", f"/categories/{GOTCHA_CATEGORY}", "/quiz", "/progress", "/search"]
    shortcuts = Shortcuts().bind("escape", lambda: page.go("/languages"))
    for i, route in enumerate(tile_routes, start=1):
        shortcuts.bind(str(i), lambda r=route: page.go(r))
    shortcuts.install(page)
    keys_help = ft.Text(
        Shortcuts().describe((f"1-{len(tile_routes)}", "open a tile"), ("escape", "all tracks")),
        size=fs(11), color=theme.text_muted,
    )

    controls: list[ft.Control] = [stagger.wrap(banner, distance=0.03), spacer(20), grid, spacer(8), keys_help]
    revisit_section = _build_revisit_later_section(page, theme, fs, state, engine)
    if revisit_section is not None:
        controls.append(spacer(20))
        controls.append(stagger.wrap(revisit_section))
    stagger.play()

    fill_later(page, xp_fill, width=xp_fill.data)

    return ft.View(
        route="/hub",
        bgcolor=theme.bg,
        scroll=ft.ScrollMode.AUTO,
        padding=view_padding(page),
        controls=controls,
    )


def _build_revisit_later_section(page: ft.Page, theme, fs, state: AppState, engine) -> ft.Control | None:
    bookmarked_ids = state.progress.get_bookmarked_lesson_ids(state.language)
    exercises = [ex for eid in bookmarked_ids if (ex := engine.get(eid)) is not None]
    if not exercises:
        return None

    return card(theme, fs, "Revisit later", [
        ft.Text("Exercises you bookmarked -- one tap to jump back in.", size=fs(12), color=theme.text_muted),
        ft.Row(
            [
                button(ex.title, lambda _e, eid=ex.id: page.go(f"/lesson/{eid}"), theme, "ghost",
                       icon=ft.Icons.BOOKMARK_ROUNDED, height=38)
                for ex in exercises
            ],
            spacing=8, wrap=True,
        ),
    ], icon=ft.Icons.BOOKMARK_ROUNDED, accent=theme.warning, title_size=16)
