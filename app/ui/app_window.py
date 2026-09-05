"""Root Flet application: route-based navigation between full-screen views.

page.views.clear() + page.views.append(...) on every route change, rebuilding
exactly one view fresh each time -- avoids ever showing stale progress/XP
numbers on a view built earlier. `history` is a small Python-side back
stack since page.views is deliberately kept at length 1.

Because there's only ever one view, each view's `can_pop` is set to False
so Flutter can't silently pop (and, with nothing beneath it in the
Navigator, exit the app on Android's hardware/gesture back button) --
`on_confirm_pop` is the hook Flutter actually solicits on every back
attempt when can_pop is False, so that's where go_back() runs, not
`page.on_view_pop` (which per Flet's own docs/examples only fires *after*
a pop the framework was allowed to perform itself -- never true here).
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
    # Windows-only (per Flet's own docs on this property); a no-op elsewhere.
    # Android/iOS/web/macOS app icons come from assets/icon.jpg instead, via
    # `flet build`'s own icon pipeline (flutter_launcher_icons).
    page.window.icon = "icon.ico"
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
        # would pop this lone view straight off the stack and exit the app.
        # can_pop=False blocks that native pop instead, which is what makes
        # Flutter solicit on_confirm_pop below on every back attempt (system
        # back, app-bar back, or otherwise) rather than acting on it itself.
        view = page.views[-1]
        view.can_pop = False

        async def on_confirm_pop(_e: ft.Event) -> None:
            go_back()
            # We already handle "back" ourselves via go_back()'s page.go()
            # above (which clears+rebuilds page.views with the previous
            # route) -- confirm_pop(False) just tells Flutter not to *also*
            # pop this (now-superseded) view natively on top of that.
            await view.confirm_pop(False)

        view.on_confirm_pop = on_confirm_pop

        page.bgcolor = state.theme.bg
        page.theme_mode = ft.ThemeMode.DARK if state.theme.is_dark else ft.ThemeMode.LIGHT
        page.update()

    def go_back() -> None:
        if history:
            previous_route = history.pop()
            navigating_back["value"] = True
            page.go(previous_route)
        else:
            page.run_task(page.window.close)

    def view_pop(_e: ft.ViewPopEvent) -> None:
        go_back()

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go("/setup" if not state.settings.setup_complete else "/languages")
