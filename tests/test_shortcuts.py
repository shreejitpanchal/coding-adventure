import asyncio

from app.ui.shortcuts import Shortcuts, key_spec


class Ev:
    def __init__(self, key, ctrl=False, shift=False, alt=False, meta=False):
        self.key, self.ctrl, self.shift, self.alt, self.meta = key, ctrl, shift, alt, meta


class FakePage:
    on_keyboard_event = None


def test_key_spec_normalises_case_modifiers_and_aliases():
    assert key_spec(Ev("Enter", ctrl=True)) == "ctrl+enter"
    assert key_spec(Ev("H", ctrl=True, shift=True)) == "ctrl+shift+h"
    assert key_spec(Ev("3")) == "3"
    assert key_spec(Ev(" ")) == "space"
    assert key_spec(Ev("Arrow Right")) == "right"


def test_dispatch_calls_sync_and_async_handlers_and_ignores_unbound():
    hits = []

    async def go_next():
        hits.append("next")

    page = FakePage()
    Shortcuts().bind("escape", lambda: hits.append("back")).bind(["enter", "space"], go_next).install(page)
    asyncio.run(page.on_keyboard_event(Ev("Escape")))
    asyncio.run(page.on_keyboard_event(Ev(" ")))
    asyncio.run(page.on_keyboard_event(Ev("Q")))  # unbound -> nothing
    assert hits == ["back", "next"]


def test_describe_renders_a_help_line():
    line = Shortcuts().describe(("ctrl+enter", "run"), ("escape", "back"), ("1-4", "answer"))
    assert line == "Ctrl+Enter run  ·  Esc back  ·  1-4 answer"
