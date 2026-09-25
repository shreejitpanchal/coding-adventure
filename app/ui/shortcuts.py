"""Keyboard shortcuts: one tiny binding layer over `page.on_keyboard_event`.

A screen builds a `Shortcuts` table ("ctrl+enter" -> handler, "1" ->
handler, "escape" -> handler) and installs it; app_window clears the
page handler on every navigation, so nothing leaks between screens.

Key specs are lower-case, modifiers first, joined by "+": "enter",
"escape", "ctrl+h", "shift+ctrl+r", "1". Handlers may be sync or async.
Plain letter/digit keys must only be bound on screens without a text
field, since Flet delivers keyboard events globally even while typing --
the lesson screen therefore uses Ctrl-combos only."""
from __future__ import annotations

import inspect
from typing import Awaitable, Callable, Iterable, Union

import flet as ft

Handler = Callable[[], Union[None, Awaitable[None]]]

_KEY_ALIASES = {
    " ": "space",
    "arrow down": "down",
    "arrow up": "up",
    "arrow left": "left",
    "arrow right": "right",
}


def key_spec(e: ft.KeyboardEvent) -> str:
    """Normalise an event to a spec like "ctrl+enter" or "3"."""
    raw = e.key or ""
    key = _KEY_ALIASES.get(raw.lower(), raw.strip().lower())
    parts: list[str] = []
    if getattr(e, "ctrl", False):
        parts.append("ctrl")
    if getattr(e, "shift", False):
        parts.append("shift")
    if getattr(e, "alt", False):
        parts.append("alt")
    if getattr(e, "meta", False):
        parts.append("meta")
    parts.append(key)
    return "+".join(parts)


class Shortcuts:
    def __init__(self) -> None:
        self._bindings: dict[str, Handler] = {}

    def bind(self, spec: Union[str, Iterable[str]], handler: Handler) -> "Shortcuts":
        specs = [spec] if isinstance(spec, str) else list(spec)
        for s in specs:
            self._bindings[s.lower()] = handler
        return self

    def install(self, page: ft.Page) -> None:
        page.on_keyboard_event = self._dispatch

    async def _dispatch(self, e: ft.KeyboardEvent) -> None:
        handler = self._bindings.get(key_spec(e))
        if handler is None:
            return
        result = handler()
        if inspect.isawaitable(result):
            await result

    def describe(self, *labels: tuple[str, str]) -> str:
        """Render a help line from (spec, meaning) pairs: "Ctrl+Enter run · Esc back"."""
        pretty = {"ctrl": "Ctrl", "shift": "Shift", "alt": "Alt", "meta": "Cmd", "enter": "Enter",
                  "escape": "Esc", "space": "Space"}
        parts = []
        for spec, meaning in labels:
            keys = "+".join(pretty.get(p, p.upper() if len(p) == 1 else p.title()) for p in spec.split("+"))
            parts.append(f"{keys} {meaning}")
        return "  ·  ".join(parts)
