"""Motion helpers, exercised without a Flet session: starting states are
what the builders rely on, and every helper must degrade gracefully when
there is no event loop (which is exactly the test situation)."""
import asyncio

import flet as ft

from app.ui.motion import Pulser, Stagger, confetti_layer, count_up, glow, hover_lift, prepare_pop, shadow
from app.ui.theme import get_preset

THEME = get_preset("aurora")


class NoLoopPage:
    """A page whose run_task fails, like a control built outside a session."""

    def run_task(self, *_a, **_k):
        raise RuntimeError("no loop")


class FakeEvent:
    def __init__(self, control, data):
        self.control = control
        self.data = data


def test_stagger_wrap_hides_then_play_reveals_without_a_loop():
    stagger = Stagger(NoLoopPage())
    a = stagger.wrap(ft.Text("a"))
    b = stagger.wrap(ft.Text("b"), col={"xs": 12})
    assert a.opacity == 0 and a.offset.y > 0
    assert b.col == {"xs": 12}
    stagger.play()  # falls back to revealing immediately
    assert a.opacity == 1 and a.offset.y == 0
    assert b.opacity == 1


def test_stagger_play_with_nothing_wrapped_is_a_noop():
    Stagger(NoLoopPage()).play()


def test_hover_lift_scales_and_glows_on_enter():
    container = ft.Container(content=ft.Text("x"))
    hover_lift(container, THEME, glow_color=THEME.accent)
    assert container.scale == 1.0
    rest_shadow = container.shadow
    container.update = lambda: None
    container.on_hover(FakeEvent(container, True))
    assert container.scale == 1.02
    assert container.shadow is not rest_shadow
    container.on_hover(FakeEvent(container, "false"))
    assert container.scale == 1.0
    assert container.shadow is rest_shadow


def test_prepare_pop_sets_spring_start_state():
    c = ft.Container()
    prepare_pop(c)
    assert c.scale == 0.85 and c.opacity == 0
    assert isinstance(c.animate_scale, ft.Animation)


def test_shadow_and_glow_are_box_shadows():
    assert isinstance(shadow(THEME), ft.BoxShadow)
    assert isinstance(glow(THEME.primary), ft.BoxShadow)


def test_confetti_layer_is_an_empty_edge_pinned_stack():
    layer = confetti_layer()
    assert isinstance(layer, ft.Stack)
    assert layer.controls == []
    assert (layer.left, layer.top, layer.right, layer.bottom) == (0, 0, 0, 0)


def test_count_up_ends_on_the_exact_value():
    text = ft.Text("+0 XP")
    text.update = lambda: None
    asyncio.run(count_up(text, 25, fmt="+{n} XP", duration=0.01, steps=5))
    assert text.value == "+25 XP"
    asyncio.run(count_up(text, 0, start=0, fmt="{n}"))
    assert text.value == "0"


def test_pulser_stop_resets_scale():
    class LoopPage:
        def run_task(self, coro, *a, **k):
            return None  # don't actually start the loop here

    control = ft.Container()
    pulser = Pulser(LoopPage(), control)
    pulser.start()
    control.scale = 1.04
    pulser.stop()
    assert control.scale == 1.0
