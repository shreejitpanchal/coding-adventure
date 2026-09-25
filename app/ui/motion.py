"""Motion helpers: the handful of animation patterns every screen uses.

Flet animates a property when it changes *after* the control is on the
page, so each helper here is two halves -- set the starting state while
building, then flip to the end state from a page task a frame later.
Nothing in this module knows about exercises or progress; it only moves
controls.

Threading note: `page.run_task()` schedules its coroutine on the Flet
event loop with `run_coroutine_threadsafe`, while view builders run on a
worker thread. A task started during a build can therefore run *before*
the new view is mounted, and `control.update()` on an unmounted control
raises. Every helper here waits for its control to attach
(`_wait_attached`) and, if that never happens, falls back to the visible
end state so nothing can be left hidden. Updates go through
`page.update()`, which is always valid.

- `Stagger`     : wrap cards so they fade/slide in one after another.
- `hover_lift`  : scale + glow on mouse-over for clickable tiles.
- `pop_in`      : a control that springs from 85% to 100% (reward cards).
- `Pulser`      : gentle heartbeat on a control while something runs.
- `count_up`    : animate a number in a Text (XP, percentages).
- `confetti`    : a burst of coloured particles from the centre of a Stack.
"""
from __future__ import annotations

import asyncio
import logging
import math
import random
from typing import Optional, Sequence

import flet as ft

from app.ui.theme import ThemePreset

logger = logging.getLogger(__name__)

EASE_OUT = ft.AnimationCurve.EASE_OUT_CUBIC
SPRING = ft.AnimationCurve.EASE_OUT_BACK

ENTRANCE_MS = 420
STAGGER_STEP_S = 0.055
HOVER_MS = 160
_ATTACH_TIMEOUT_S = 3.0
_ATTACH_POLL_S = 0.03


def shadow(theme: ThemePreset, blur: int = 18, y: int = 8, alpha: float = 0.22, color: Optional[str] = None) -> ft.BoxShadow:
    return ft.BoxShadow(
        blur_radius=blur, spread_radius=0,
        color=ft.Colors.with_opacity(alpha, color or theme.shadow),
        offset=ft.Offset(0, y),
    )


def glow(color: str, alpha: float = 0.35, blur: int = 26) -> ft.BoxShadow:
    return ft.BoxShadow(blur_radius=blur, spread_radius=1, color=ft.Colors.with_opacity(alpha, color), offset=ft.Offset(0, 6))


def _page_of(control: ft.Control) -> Optional[ft.Page]:
    """The control's page, or None when it isn't mounted. Flet raises on
    `.page` for an unmounted control instead of returning None."""
    try:
        return control.page or None
    except Exception:
        return None


def _is_attached(control: ft.Control) -> bool:
    return _page_of(control) is not None


async def _wait_attached(control: ft.Control, timeout: float = _ATTACH_TIMEOUT_S) -> bool:
    """Poll until `control` is on a page (the view has been mounted)."""
    waited = 0.0
    while not _is_attached(control):
        if waited >= timeout:
            return False
        await asyncio.sleep(_ATTACH_POLL_S)
        waited += _ATTACH_POLL_S
    return True


def _safe_page_update(page: ft.Page) -> bool:
    try:
        page.update()
        return True
    except Exception:
        logger.debug("page.update() failed during an animation (view replaced?)", exc_info=True)
        return False


class Stagger:
    """Collects controls during a build; `play()` reveals them in order.

    Usage in a view builder:
        stagger = Stagger(page)
        column.controls = [stagger.wrap(card) for card in cards]
        stagger.play()          # schedule -- safe to call before the view is mounted
    """

    def __init__(self, page: ft.Page, step: float = STAGGER_STEP_S) -> None:
        self.page = page
        self.step = step
        self._items: list[ft.Container] = []

    def wrap(self, control: ft.Control, *, distance: float = 0.06, expand: Optional[bool] = None,
             col: Optional[dict] = None) -> ft.Container:
        wrapper = ft.Container(
            content=control,
            opacity=0,
            offset=ft.Offset(0, distance),
            animate_opacity=ft.Animation(ENTRANCE_MS, EASE_OUT),
            animate_offset=ft.Animation(ENTRANCE_MS, EASE_OUT),
        )
        if expand is not None:
            wrapper.expand = expand
        if col is not None:
            wrapper.col = col
        self._items.append(wrapper)
        return wrapper

    def _reveal_all(self) -> None:
        for item in self._items:
            item.opacity = 1
            item.offset = ft.Offset(0, 0)

    def play(self) -> None:
        if not self._items:
            return
        try:
            self.page.run_task(self._play)
        except Exception:
            # No running loop (e.g. building a view in a unit test): show
            # everything immediately rather than leaving it invisible.
            self._reveal_all()

    async def _play(self) -> None:
        try:
            if not await _wait_attached(self._items[0]):
                logger.warning("Stagger: view never mounted; revealing all items without animation")
                self._reveal_all()
                _safe_page_update(self.page)
                return
            await asyncio.sleep(0.02)  # let the initial (hidden) frame land first
            for item in self._items:
                item.opacity = 1
                item.offset = ft.Offset(0, 0)
                if not _safe_page_update(self.page):
                    return  # view was replaced mid-animation
                await asyncio.sleep(self.step)
        except Exception:
            logger.exception("Stagger reveal failed; forcing everything visible")
            self._reveal_all()
            _safe_page_update(self.page)


def hover_lift(container: ft.Container, theme: ThemePreset, *, scale: float = 1.02,
               glow_color: Optional[str] = None) -> ft.Container:
    """Give a Container a scale + shadow lift on hover. Sets `on_hover`,
    so use it on tiles whose click handler lives on the same container."""
    rest_shadow = container.shadow if container.shadow is not None else shadow(theme)
    hover_shadow = glow(glow_color or theme.primary) if glow_color or theme.is_dark else shadow(theme, blur=28, y=12, alpha=0.3)
    container.shadow = rest_shadow
    container.scale = 1.0
    container.animate_scale = ft.Animation(HOVER_MS, EASE_OUT)

    def on_hover(e: ft.ControlEvent) -> None:
        hovered = e.data in (True, "true", "True")
        e.control.scale = scale if hovered else 1.0
        e.control.shadow = hover_shadow if hovered else rest_shadow
        try:
            e.control.update()
        except Exception:
            page = _page_of(e.control)
            if page is not None:
                _safe_page_update(page)

    container.on_hover = on_hover
    return container


def prepare_pop(control: ft.Control) -> None:
    """Starting state for pop_in(): call while building."""
    control.scale = 0.85
    control.opacity = 0
    control.animate_scale = ft.Animation(420, SPRING)
    control.animate_opacity = ft.Animation(260, ft.AnimationCurve.EASE_OUT)


def _show_popped(control: ft.Control) -> None:
    control.scale = 1.0
    control.opacity = 1


def pop_in(page: ft.Page, control: ft.Control) -> None:
    """Make a (prepared, now visible) control spring to full size."""
    async def _go() -> None:
        try:
            if not await _wait_attached(control):
                logger.warning("pop_in: control never mounted; showing it without animation")
            else:
                await asyncio.sleep(0.02)
            _show_popped(control)
            _safe_page_update(page)
        except Exception:
            logger.exception("pop_in failed; forcing control visible")
            _show_popped(control)
            _safe_page_update(page)

    try:
        page.run_task(_go)
    except Exception:
        _show_popped(control)


class Pulser:
    """Heartbeat a control (scale 1.0 <-> 1.04) until stopped."""

    def __init__(self, page: ft.Page, control: ft.Control, period: float = 0.55) -> None:
        self.page = page
        self.control = control
        self.period = period
        self._running = False
        control.animate_scale = ft.Animation(int(period * 1000), ft.AnimationCurve.EASE_IN_OUT)

    def start(self) -> None:
        if self._running:
            return
        self._running = True
        try:
            self.page.run_task(self._loop)
        except Exception:
            self._running = False

    def stop(self) -> None:
        self._running = False
        self.control.scale = 1.0

    async def _loop(self) -> None:
        big = True
        while self._running:
            self.control.scale = 1.04 if big else 1.0
            if not _is_attached(self.control) or not _safe_page_update(self.page):
                return
            big = not big
            await asyncio.sleep(self.period)


async def count_up(text: ft.Text, end: int, *, start: int = 0, duration: float = 0.8,
                   fmt: str = "{n}", steps: int = 24) -> None:
    """Animate `text.value` from start to end using `fmt` ("{n}" placeholder)."""
    def push() -> None:
        page = _page_of(text)
        if page is not None:
            _safe_page_update(page)
        else:
            try:
                text.update()
            except Exception:
                pass

    if end == start or steps <= 0:
        text.value = fmt.format(n=end)
        push()
        return
    for i in range(1, steps + 1):
        t = i / steps
        eased = 1 - (1 - t) ** 3
        text.value = fmt.format(n=round(start + (end - start) * eased))
        push()
        await asyncio.sleep(duration / steps)


def confetti_layer() -> ft.Stack:
    """An empty overlay to put on top of a view's content (inside an outer
    Stack). Fills the parent via edge positioning -- `expand` is not valid
    for a Stack child. Particles are added and removed by `confetti()`."""
    return ft.Stack([], left=0, top=0, right=0, bottom=0, alignment=ft.Alignment.CENTER)


def confetti(page: ft.Page, layer: ft.Stack, theme: ThemePreset, *, count: int = 28) -> None:
    """Burst `count` particles outward from the layer's centre, then clear."""
    palette = [theme.primary, theme.accent, theme.success, theme.warning, theme.danger, theme.gradient[0], theme.gradient[1]]
    particles: list[ft.Container] = []
    for i in range(count):
        size = random.choice([8, 10, 12])
        particles.append(ft.Container(
            width=size, height=size, border_radius=3 if i % 2 else size,
            bgcolor=palette[i % len(palette)],
            offset=ft.Offset(0, 0), opacity=1, rotate=0,
            animate_offset=ft.Animation(900, EASE_OUT),
            animate_opacity=ft.Animation(900, ft.AnimationCurve.EASE_IN),
            animate_rotation=ft.Animation(900, ft.AnimationCurve.LINEAR),
        ))
    layer.controls = particles

    async def _burst() -> None:
        try:
            if not _safe_page_update(page):
                return
            await asyncio.sleep(0.03)
            for p in particles:
                angle = random.uniform(0, 2 * math.pi)
                radius = random.uniform(14, 42)  # in multiples of the particle's own size
                p.offset = ft.Offset(math.cos(angle) * radius, math.sin(angle) * radius * 0.7 - 6)
                p.opacity = 0
                p.rotate = random.uniform(-6, 6)
            if not _safe_page_update(page):
                return
            await asyncio.sleep(1.0)
            layer.controls = []
            _safe_page_update(page)
        except Exception:
            logger.debug("confetti aborted (view replaced?)", exc_info=True)

    try:
        page.run_task(_burst)
    except Exception:
        layer.controls = []


def fill_later(page: ft.Page, control: ft.Control, *, width: float, delay: float = 0.25) -> None:
    """Widen `control` to `width` once mounted (used by the XP bar), so the
    `animate` on the control plays from its initial 0."""
    async def _go() -> None:
        try:
            if await _wait_attached(control):
                await asyncio.sleep(delay)
            control.width = width
            _safe_page_update(page)
        except Exception:
            logger.debug("fill_later aborted (view replaced?)", exc_info=True)

    try:
        page.run_task(_go)
    except Exception:
        control.width = width


def reveal_all(controls: Sequence[ft.Control]) -> None:
    """Test helper / fallback: make Stagger-wrapped controls visible now."""
    for c in controls:
        if isinstance(c, ft.Container):
            c.opacity = 1
            c.offset = ft.Offset(0, 0)
