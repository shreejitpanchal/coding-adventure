"""Root Flet application: route-based navigation between full-screen views.

page.views.clear() + page.views.append(...) on every route change, rebuilding
exactly one view fresh each time -- avoids ever showing stale progress/XP
numbers on a view built earlier. `history` is a small Python-side back
stack since page.views is deliberately kept at length 1.
"""
from __future__ import annotations

import flet as ft

from app.ui.app_state import AppState
from app.ui.category_levels import build_category_levels_view
from app.ui.category_map import build_category_map_view
from app.ui.daily_refresher import build_daily_refresher_view
from app.ui.language_select import build_language_select_view
from app.ui.lesson_screen import build_lesson_view
from app.ui.progress_screen import build_progress_view
from app.ui.quiz_screen import build_quiz_view
from app.ui.settings_screen import build_settings_view
from app.ui.setup_wizard import build_setup_wizard_view
from app.ui.track_hub import build_track_hub_view


def main(page: ft.Page) -> None:
    page.title = "Coding Adventure"
    page.window.width = 1280
    page.window.height = 860
    page.window.min_width = 1024
    page.window.min_height = 700
    page.window.maximized = True
    page.padding = 0

    state = AppState()

    history: list[str] = []
    navigating_back = {"value": False}

    def route_change(_e: ft.RouteChangeEvent) -> None:
        route = page.route

        if not navigating_back["value"] and page.views and page.views[-1].route != "/setup":
            history.append(page.views[-1].route)
        navigating_back["value"] = False

        # Remember where a lesson was entered FROM (but not lesson-to-lesson,
        # e.g. clicking "Next exercise" -- that keeps the original origin so
        # a whole Daily Refresher chain still returns to /daily at the end).
        if route.startswith("/lesson/") and page.views:
            previous_route = page.views[-1].route
            if not previous_route.startswith("/lesson/"):
                state.lesson_return_route = previous_route

        page.views.clear()

        if route == "/languages":
            page.views.append(build_language_select_view(page, state))
        elif route == "/hub":
            state.progress.record_play_today(state.language)
            page.views.append(build_track_hub_view(page, state))
        elif route == "/daily":
            page.views.append(build_daily_refresher_view(page, state))
        elif route.startswith("/categories/"):
            category = route.removeprefix("/categories/")
            page.views.append(build_category_levels_view(page, state, category))
        elif route == "/categories":
            page.views.append(build_category_map_view(page, state))
        elif route == "/quiz":
            page.views.append(build_quiz_view(page, state))
        elif route == "/progress":
            page.views.append(build_progress_view(page, state))
        elif route == "/settings":
            page.views.append(build_settings_view(page, state))
        elif route.startswith("/lesson/"):
            exercise_id = route.removeprefix("/lesson/")
            page.views.append(build_lesson_view(page, state, exercise_id))
        elif route == "/setup":
            page.views.append(build_setup_wizard_view(page, state))
        else:
            page.views.append(build_language_select_view(page, state))

        # Since page.views is deliberately kept at length 1 (see module
        # docstring), Flutter's Navigator has nothing else to pop -- with
        # the default can_pop=True, Android's hardware/gesture back button
        # would pop this lone view straight off the stack and exit the app
        # instead of running our own history-based back navigation below.
        # can_pop=False makes Flutter intercept that system back action and
        # route it through on_view_pop/view_pop() instead, same as tapping
        # an in-app back button already does.
        page.views[-1].can_pop = False

        page.bgcolor = state.theme.bg
        page.theme_mode = ft.ThemeMode.DARK if state.theme.is_dark else ft.ThemeMode.LIGHT
        page.update()

    def view_pop(_e: ft.ViewPopEvent) -> None:
        if history:
            previous_route = history.pop()
            navigating_back["value"] = True
            page.go(previous_route)
        else:
            page.run_task(page.window.close)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go("/setup" if not state.settings.setup_complete else "/languages")
