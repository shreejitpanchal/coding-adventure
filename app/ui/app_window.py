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

import logging
from typing import Callable

import flet as ft

from app.ui.app_state import AppState
from app.ui.category_levels import build_category_levels_view
from app.ui.category_map import build_category_map_view
from app.ui.daily_refresher import build_daily_refresher_view
from app.ui.language_select import build_language_select_view
from app.ui.lesson_screen import build_lesson_view
from app.ui.progress_screen import build_progress_view
from app.ui.quiz_screen import build_quiz_view
from app.ui.review_screen import build_review_view
from app.ui.search_screen import build_search_view
from app.ui.settings_screen import build_settings_view
from app.ui.setup_wizard import build_setup_wizard_view
from app.ui.shortcuts import Shortcuts
from app.ui.theme import scaled
from app.ui.track_hub import build_track_hub_view

logger = logging.getLogger(__name__)

ViewBuilder = Callable[[ft.Page, AppState], ft.View]
ParamViewBuilder = Callable[[ft.Page, AppState, str], ft.View]

# Exact-match routes. Adding a screen is one line here plus its module.
_ROUTES: dict[str, ViewBuilder] = {
    "/languages": build_language_select_view,
    "/hub": build_track_hub_view,
    "/daily": build_daily_refresher_view,
    "/review": build_review_view,
    "/categories": build_category_map_view,
    "/quiz": build_quiz_view,
    "/search": build_search_view,
    "/progress": build_progress_view,
    "/settings": build_settings_view,
    "/setup": build_setup_wizard_view,
}

# Prefix routes whose remainder is a single parameter.
_PARAM_ROUTES: dict[str, ParamViewBuilder] = {
    "/categories/": build_category_levels_view,
    "/lesson/": build_lesson_view,
}


ROOT_ROUTES = {"", "/"}
"""Flutter's own root route -- what the browser's initial URL and a fully
unwound back stack resolve to. It means "the start of the app", i.e. the
language picker (or setup on first run)."""


def build_view_for_route(page: ft.Page, state: AppState, route: str) -> ft.View:
    """Resolve a route to a freshly built view. An unknown route is a
    programming error (every page.go() target is one of ours), so it is
    logged and shown as such instead of silently landing on the picker."""
    if route in ROOT_ROUTES:
        route = "/setup" if not state.settings.setup_complete else "/languages"
    exact = _ROUTES.get(route)
    if exact is not None:
        return exact(page, state)
    for prefix, builder in _PARAM_ROUTES.items():
        if route.startswith(prefix):
            return builder(page, state, route.removeprefix(prefix))
    logger.error("Unknown route %r requested; known: %s + %s", route, sorted(_ROUTES), sorted(_PARAM_ROUTES))
    theme = state.theme
    return ft.View(
        route=route, bgcolor=theme.bg, padding=24,
        controls=[
            ft.Text(f"Unknown screen: {route}", size=scaled(18, state.font_scale), color=theme.danger),
            ft.Button("Back to tracks", on_click=lambda _e: page.go("/languages")),
        ],
    )


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
    logger.info("Session started (language=%s, theme=%s)", state.language, state.settings.theme)

    history: list[str] = []
    navigating_back = {"value": False}

    def route_change(_e: ft.RouteChangeEvent) -> None:
        route = page.route

        if (not navigating_back["value"] and page.views and page.views[-1].route != "/setup"
                and page.views[-1].route != route):
            history.append(page.views[-1].route)
        navigating_back["value"] = False

        # Remember where a lesson was entered FROM (but not lesson-to-lesson,
        # e.g. clicking "Next exercise" -- that keeps the original origin so
        # a whole Daily Refresher chain still returns to /daily at the end).
        if route.startswith("/lesson/") and page.views:
            previous_route = page.views[-1].route
            if not previous_route.startswith("/lesson/"):
                state.lesson_return_route = previous_route

        # Page-level handlers belong to the view that installed them. The
        # lesson screen binds Ctrl+Enter here; if the user leaves it by any
        # path other than its own Back button (system back, a "Related
        # practice" link, a bookmark on the hub) that handler would otherwise
        # keep pointing at a controller whose controls are no longer mounted.
        page.on_keyboard_event = None

        page.views.clear()
        page.views.append(build_view_for_route(page, state, route))

        # Screens that didn't install their own shortcuts still get Escape = back.
        if page.on_keyboard_event is None:
            Shortcuts().bind("escape", go_back).install(page)

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
            return
        # Nothing left to go back to. On desktop, back from the picker
        # closes the app. On Android/web there is no window to close (the
        # call is a no-op there), so land on the picker instead of letting
        # the client fall through to Flutter's root route.
        if page.route not in ("/languages", "/setup"):
            navigating_back["value"] = True
            page.go("/languages")
        elif not page.web and page.platform is not None and page.platform.is_desktop():
            page.run_task(page.window.close)

    def view_pop(_e: ft.ViewPopEvent) -> None:
        go_back()

    def on_session_end(_e: ft.ControlEvent) -> None:
        # Fires when the client disconnects (window closed, browser tab
        # gone). Releases the SQLite connection so the last write is
        # flushed and the file isn't held open past the process's intent.
        logger.info("Session ended")
        state.close()

    def on_client_error(e: ft.ControlEvent) -> None:
        # Flutter-side exceptions (a layout constraint violation, a bad
        # property combination) otherwise show up only as a blank area.
        logger.error("Client-side error on %s: %s", page.route, e.data)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.on_disconnect = on_session_end
    page.on_error = on_client_error

    page.go("/setup" if not state.settings.setup_complete else "/languages")
