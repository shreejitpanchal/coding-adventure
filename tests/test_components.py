"""The UI kit, driven without a real Flet session -- controls are plain
objects until mounted, and the widgets only need `page.update()` (and,
for Stagger, a `run_task` that may be absent) to exist."""
import flet as ft

from app.engine.quiz import QuizQuestion
from app.ui.components import (
    MultipleChoiceCard,
    button,
    button_style,
    card,
    chip,
    difficulty_color,
    header_row,
    level_badge,
    nav_tile,
    progress_ring,
    stat_pill,
    xp_bar,
)
from app.ui.theme import THEME_PRESETS, get_preset

THEME = get_preset("aurora")


class FakePage:
    def __init__(self):
        self.updates = 0
        self.routes = []

    def update(self):
        self.updates += 1

    def go(self, route):
        self.routes.append(route)


def _fs(n: int) -> int:
    return n


def _questions():
    return [
        QuizQuestion(id="q1", question="one?", options=["a", "b", "c"], correct=1, explanation="B."),
        QuizQuestion(id="q2", question="two?", options=["x", "y"], correct=0, explanation="X."),
    ]


def test_every_preset_has_the_fields_the_kit_needs():
    for preset in THEME_PRESETS.values():
        assert preset.accent.startswith("#")
        assert len(preset.gradient) == 2
        assert preset.surface.startswith("#")


def test_button_variants_map_to_theme_colors():
    assert button_style(THEME, "primary").bgcolor == THEME.primary
    assert button_style(THEME, "danger").bgcolor == THEME.danger
    assert button_style(THEME, bgcolor="#123456").bgcolor == "#123456"
    assert button_style(THEME, "ghost").color == THEME.text
    b = button("Go", None, THEME, "success", disabled=True, icon=ft.Icons.PLAY_ARROW_ROUNDED)
    assert b.disabled and b.style.bgcolor == THEME.success
    assert b.icon == ft.Icons.PLAY_ARROW_ROUNDED


def test_format_duration():
    from app.ui.components import format_duration
    assert format_duration(7) == "7s"
    assert format_duration(60) == "1m"
    assert format_duration(95) == "1m 35s"
    assert format_duration(3725) == "1h 2m"
    assert format_duration(-3) == "0s"


def test_difficulty_colors_are_distinct():
    colors = {difficulty_color(THEME, d) for d in ("warmup", "core", "gotcha", "deep_dive")}
    assert len(colors) == 4
    assert difficulty_color(THEME, "unknown") == THEME.text_muted


def test_card_with_and_without_title_and_accent():
    with_title = card(THEME, _fs, "Title", [])
    assert len(with_title.content.controls) == 1  # just the title row
    without = card(THEME, _fs, None, [], border_color=THEME.primary)
    assert without.content.controls == []
    assert without.border is not None
    striped = card(THEME, _fs, "T", [ft.Text("x")], accent=THEME.accent, hover=True)
    assert striped.bgcolor == THEME.accent  # the stripe is the outer colour showing through left padding
    assert striped.padding.left == 5
    assert striped.content.bgcolor == THEME.card
    assert striped.on_hover is not None  # hover lift wired


def test_small_pieces_build():
    c = chip("Gotcha", THEME.warning, _fs, icon=ft.Icons.BOLT, filled=True)
    assert c.bgcolor == THEME.warning
    pill = stat_pill(THEME, _fs, ft.Icons.BOLT, "120", "XP", THEME.warning)
    assert "120" in [t.value for t in pill.content.controls[1].controls]
    badge = level_badge(7, THEME.primary, _fs)
    assert badge.content.value == "7"
    ring = progress_ring(THEME, _fs, 1.7, THEME.success, label="100%")  # clamps
    assert ring.controls[0].value == 1.0
    track, fill = xp_bar(THEME, 0.5, width=200)
    assert fill.width == 0 and fill.data == 100  # starts empty, target stored for the animation
    assert track.width == 200


def test_header_row_and_nav_tile_route():
    page = FakePage()
    row = header_row(THEME, _fs, "Progress", lambda _e: page.go("/hub"), subtitle="sub", icon=ft.Icons.INSIGHTS)
    row.controls[0].on_click(None)
    assert page.routes == ["/hub"]
    # Compact mode drops trailing controls onto a second row so the title keeps its width.
    trailing = [chip("Core", THEME.primary, _fs), chip("10 XP", THEME.warning, _fs)]
    compact = header_row(THEME, _fs, "A long exercise title", lambda _e: None, trailing=trailing, compact=True)
    assert isinstance(compact, ft.Column) and len(compact.controls) == 2
    assert compact.controls[1].controls == trailing
    wide = header_row(THEME, _fs, "Title", lambda _e: None, trailing=trailing, compact=False)
    assert isinstance(wide, ft.Row)
    tile = nav_tile(page, THEME, _fs, icon=ft.Icons.QUIZ_ROUNDED, title="Quiz", subtitle="s", status="3 left",
                    route="/quiz", color=THEME.accent)
    tile.on_click(None)
    assert page.routes[-1] == "/quiz"
    assert tile.on_hover is not None


def test_is_compact_and_padding_follow_page_width():
    from app.ui.components import is_compact, view_padding

    class Narrow:
        width = 390

    class Wide:
        width = 1280

    assert is_compact(Narrow()) and not is_compact(Wide()) and not is_compact(None)
    assert view_padding(Narrow()).left == 16
    assert view_padding(Wide()).left == 28
    assert view_padding(None).left == 28


def test_font_scale_steps_are_visibly_distinct():
    from app.ui.theme import FONT_SIZE_SCALES, resolve_font_scale, scaled
    values = [FONT_SIZE_SCALES[k] for k in ("small", "medium", "large", "xlarge")]
    assert values == sorted(values) and values[-1] - values[0] >= 0.5
    assert scaled(14, resolve_font_scale("xlarge")) > scaled(14, resolve_font_scale("large")) > scaled(14, 1.0)
    assert resolve_font_scale("nonsense") == 1.0


def test_multiple_choice_walkthrough_reports_answers_and_completion():
    page = FakePage()
    answers = []
    completed = []
    widget = MultipleChoiceCard(
        page, THEME, _fs, "Check",
        on_answer=lambda q, ok: answers.append((q.id, ok)),
        on_complete=lambda score, total: completed.append((score, total)),
        final_label="Finish",
    )
    widget.start(_questions())
    assert widget.progress_text.value == "Question 1 of 2"
    assert len(widget.options_column.controls) == 3  # renders as many rows as options
    assert widget.progress_bar.value == 0

    widget._on_select(0)  # wrong
    assert answers == [("q1", False)]
    assert widget.feedback_text.value.startswith("Not quite. B.")
    assert widget.feedback_icon.visible
    assert widget.next_button.visible and widget.next_button.content == "Next →"
    assert widget.options_column.controls[1].bgcolor == THEME.success  # correct answer highlighted
    assert widget.options_column.controls[0].bgcolor == THEME.danger
    widget._on_select(1)  # second click on the same question is ignored
    assert answers == [("q1", False)]

    widget._on_next(None)
    assert len(widget.options_column.controls) == 2
    assert widget.switcher.content is widget.body  # question body swapped through the switcher
    widget._on_select(0)  # right
    assert answers[-1] == ("q2", True)
    assert widget.next_button.content == "Finish"
    assert widget.progress_bar.value == 1.0

    widget._on_next(None)
    assert completed == [(1, 2)]
    assert page.updates > 0


def test_keyboard_entry_points_select_and_advance():
    page = FakePage()
    completed = []
    widget = MultipleChoiceCard(page, THEME, _fs, "Check", on_complete=lambda s, t: completed.append((s, t)))
    widget.advance()  # nothing started -> no-op
    widget.start(_questions())
    widget.advance()  # unanswered -> no-op
    assert widget.index == 0
    widget.select_option(9)  # out of range -> ignored
    widget.select_option(1)  # correct
    widget.advance()
    assert widget.index == 1
    widget.select_option(0)
    widget.advance()
    assert completed == [(2, 2)]


def test_show_summary_replaces_question_area_and_start_restores_it():
    page = FakePage()
    widget = MultipleChoiceCard(page, THEME, _fs, "Check")
    widget.start(_questions())
    retry = button("Retry", None, THEME)
    widget.show_summary("Missed one.", THEME.warning, actions=[retry])
    assert widget.options_column.controls == []
    assert retry in widget.actions_row.controls
    widget.start(_questions())
    assert retry not in widget.actions_row.controls
    assert widget.options_column.controls
