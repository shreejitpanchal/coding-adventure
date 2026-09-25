"""Topic browser: a responsive grid of category cards, each with its icon,
a mastery ring, and the next exercise to pick up -- not a winding
"adventure map" (this app's audience is professionals, not kids), but
it should still feel alive."""
from __future__ import annotations

import flet as ft

from app.engine.categories import get_category_meta
from app.ui.app_state import AppState
from app.ui.components import (
    RADIUS,
    chip,
    emoji_circle,
    header_row,
    progress_ring,
    route_handler,
    spacer,
    tint,
    view_padding,
)
from app.ui.motion import Stagger, hover_lift
from app.ui.theme import scaled

_CARD_COL = {"xs": 12, "sm": 6, "md": 4, "xl": 3}


def build_category_map_view(page: ft.Page, state: AppState) -> ft.View:
    theme = state.theme
    fs = lambda base: scaled(base, state.font_scale)  # noqa: E731
    engine = state.exercise_engine()
    completed_ids = set(state.progress.get_completed_lesson_ids(state.language))
    stagger = Stagger(page)

    categories = engine.categories()
    total = len(engine)
    done_total = len(completed_ids)
    header = header_row(
        theme, fs, "Practice by Topic", route_handler(page, "/hub"), back_label="← Hub",
        subtitle=f"{len(categories)} topics · {done_total}/{total} exercises complete",
        icon=ft.Icons.CATEGORY_ROUNDED,
    )

    cards = [
        stagger.wrap(_build_category_card(page, theme, fs, engine, category, completed_ids), col=_CARD_COL)
        for category in categories
    ]
    stagger.play()

    return ft.View(
        route="/categories",
        bgcolor=theme.bg,
        scroll=ft.ScrollMode.AUTO,
        padding=view_padding(page),
        controls=[header, spacer(20), ft.ResponsiveRow(cards, spacing=16, run_spacing=16)],
    )


def _build_category_card(page, theme, fs, engine, category: str, completed_ids: set[str]) -> ft.Control:
    meta = get_category_meta(category)
    items = engine.lessons_in_category(category)
    done = sum(1 for ex in items if ex.id in completed_ids)
    fraction = done / len(items) if items else 0.0
    next_up = engine.next_unlocked_in_category(category, completed_ids)

    if done and done == len(items):
        status = chip("Mastered", theme.success, fs, icon=ft.Icons.MILITARY_TECH_ROUNDED, filled=True)
    elif next_up is not None:
        status = chip(f"Next: {next_up.title}", meta.color, fs, icon=ft.Icons.PLAY_ARROW_ROUNDED)
    else:
        status = chip("Locked", theme.text_muted, fs, icon=ft.Icons.LOCK_ROUNDED)

    body = ft.Column(
        [
            ft.Row(
                [
                    emoji_circle(meta.icon, meta.color, fs, size=52, text_size=24),
                    ft.Container(expand=True),
                    progress_ring(theme, fs, fraction, meta.color, size=58, label=f"{round(100 * fraction)}%", stroke=6),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Text(meta.title, size=fs(16), weight=ft.FontWeight.BOLD, color=theme.text, max_lines=2,
                    overflow=ft.TextOverflow.ELLIPSIS),
            ft.Text(f"{done}/{len(items)} exercises", size=fs(12), color=theme.text_muted),
            status,
        ],
        spacing=8,
    )
    container = ft.Container(
        content=body,
        bgcolor=theme.card, border_radius=RADIUS, padding=18,
        border=ft.Border.all(1, tint(meta.color, 0.45)),
        on_click=route_handler(page, f"/categories/{category}"), ink=True,
    )
    return hover_lift(container, theme, glow_color=meta.color)
