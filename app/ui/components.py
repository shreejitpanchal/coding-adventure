"""Shared UI building blocks -- the visual language of every screen.

Everything takes its ThemePreset and font-scale function explicitly;
nothing reaches for global state. Motion primitives come from
app.ui.motion; this module composes them into named pieces:

- buttons (`button`, `icon_button`) with rounded shapes and icons
- `card` with an optional coloured accent stripe, title icon and hover lift
- `hero_banner`: gradient header block with big title and trailing stats
- `stat_pill`, `chip`, `level_badge`, `icon_circle`: small labelled bits
- `progress_ring`: ring with a centred label
- `nav_tile`: a clickable gradient-tinted tile with icon, text and chevron
- `header_row`: back icon-button + title + trailing controls
- `MultipleChoiceCard`: animated question walk-through (quiz + lessons)
"""
from __future__ import annotations

from typing import Callable, Literal, Optional, Sequence

import flet as ft

from app.engine.quiz import QuizQuestion
from app.ui.motion import glow, hover_lift, shadow
from app.ui.theme import ThemePreset

FontScale = Callable[[int], int]
ButtonVariant = Literal["primary", "secondary", "success", "warning", "danger", "ghost"]

WHITE = "#FFFFFF"
RADIUS = 18
RADIUS_SM = 12

OPTION_LETTERS = "ABCDEFGH"


# -- layout ------------------------------------------------------------------

def view_padding() -> ft.Padding:
    return ft.Padding.only(left=28, top=24, right=28, bottom=48)


def spacer(height: int = 12) -> ft.Control:
    return ft.Container(height=height)


def route_handler(page: ft.Page, route: str):
    return lambda _e: page.go(route)


def tint(color: str, alpha: float) -> str:
    return ft.Colors.with_opacity(alpha, color)


def difficulty_color(theme: ThemePreset, difficulty: str) -> str:
    return {
        "warmup": theme.success,
        "core": theme.primary,
        "gotcha": theme.warning,
        "deep_dive": theme.accent,
    }.get(difficulty, theme.text_muted)


def difficulty_label(difficulty: str) -> str:
    return difficulty.replace("_", " ").title()


def format_duration(seconds: int) -> str:
    """1 -> "1s", 95 -> "1m 35s", 3725 -> "1h 2m"."""
    seconds = max(0, int(seconds))
    if seconds < 60:
        return f"{seconds}s"
    minutes, secs = divmod(seconds, 60)
    if minutes < 60:
        return f"{minutes}m {secs:02d}s" if secs else f"{minutes}m"
    hours, minutes = divmod(minutes, 60)
    return f"{hours}h {minutes}m"


# -- buttons -----------------------------------------------------------------

def button_style(theme: ThemePreset, variant: ButtonVariant = "secondary", bgcolor: Optional[str] = None) -> ft.ButtonStyle:
    """One place that decides what a filled button looks like. `bgcolor`
    overrides the variant for the rare per-category / per-preset colour."""
    if variant == "ghost":
        return ft.ButtonStyle(
            bgcolor=tint(theme.text, 0.08), color=theme.text, elevation=0,
            shape=ft.RoundedRectangleBorder(radius=RADIUS_SM),
            padding=ft.Padding.symmetric(horizontal=16, vertical=10),
            overlay_color=tint(theme.text, 0.08),
        )
    colors = {
        "primary": theme.primary,
        "secondary": theme.text_muted,
        "success": theme.success,
        "warning": theme.warning,
        "danger": theme.danger,
    }
    return ft.ButtonStyle(
        bgcolor=bgcolor or colors[variant], color=WHITE, elevation=0,
        shape=ft.RoundedRectangleBorder(radius=RADIUS_SM),
        padding=ft.Padding.symmetric(horizontal=18, vertical=10),
        overlay_color=tint(WHITE, 0.14),
        animation_duration=150,
    )


def button(
    label: str,
    on_click,
    theme: ThemePreset,
    variant: ButtonVariant = "secondary",
    *,
    icon: Optional[ft.IconData] = None,
    height: int = 44,
    width: Optional[int] = None,
    disabled: bool = False,
    visible: bool = True,
    tooltip: Optional[str] = None,
    bgcolor: Optional[str] = None,
) -> ft.Button:
    return ft.Button(
        label, icon=icon, on_click=on_click, height=height, width=width, disabled=disabled, visible=visible,
        tooltip=tooltip, style=button_style(theme, variant, bgcolor),
    )


def icon_button(icon: ft.IconData, on_click, theme: ThemePreset, *, color: Optional[str] = None,
                bgcolor: Optional[str] = None, tooltip: Optional[str] = None, size: int = 22,
                selected: Optional[bool] = None, selected_icon: Optional[ft.IconData] = None) -> ft.IconButton:
    return ft.IconButton(
        icon=icon, on_click=on_click, icon_color=color or theme.text, icon_size=size,
        bgcolor=bgcolor or tint(theme.text, 0.08), tooltip=tooltip,
        selected=selected, selected_icon=selected_icon,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=RADIUS_SM), padding=10),
    )


# -- small bits --------------------------------------------------------------

def icon_circle(icon: ft.IconData, color: str, *, size: int = 44, icon_size: Optional[int] = None) -> ft.Container:
    return ft.Container(
        content=ft.Icon(icon, color=color, size=icon_size or int(size * 0.5)),
        width=size, height=size, shape=ft.BoxShape.CIRCLE, bgcolor=tint(color, 0.16),
        alignment=ft.Alignment.CENTER,
    )


def emoji_circle(emoji: str, color: str, fs: FontScale, *, size: int = 56, text_size: int = 26) -> ft.Container:
    return ft.Container(
        content=ft.Text(emoji, size=fs(text_size)),
        width=size, height=size, shape=ft.BoxShape.CIRCLE, bgcolor=tint(color, 0.18),
        alignment=ft.Alignment.CENTER,
    )


def chip(text: str, color: str, fs: FontScale, *, icon: Optional[ft.IconData] = None, filled: bool = False) -> ft.Container:
    fg = WHITE if filled else color
    children: list[ft.Control] = []
    if icon is not None:
        children.append(ft.Icon(icon, color=fg, size=fs(14)))
    children.append(ft.Text(text, size=fs(12), weight=ft.FontWeight.BOLD, color=fg))
    return ft.Container(
        content=ft.Row(children, spacing=6, tight=True, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor=color if filled else tint(color, 0.16),
        border_radius=999, padding=ft.Padding.symmetric(horizontal=10, vertical=5),
    )


def stat_pill(theme: ThemePreset, fs: FontScale, icon: ft.IconData, value: str, label: str, color: str) -> ft.Container:
    """A rounded stat with a coloured icon, a bold value and a muted label."""
    return ft.Container(
        content=ft.Row(
            [
                icon_circle(icon, color, size=38, icon_size=fs(20)),
                ft.Column(
                    [
                        ft.Text(value, size=fs(16), weight=ft.FontWeight.BOLD, color=theme.text),
                        ft.Text(label, size=fs(11), color=theme.text_muted),
                    ],
                    spacing=0, tight=True,
                ),
            ],
            spacing=10, tight=True, vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=tint(theme.text, 0.06), border_radius=999,
        padding=ft.Padding.only(left=6, right=16, top=6, bottom=6),
    )


def level_badge(number: int, color: str, fs: FontScale, *, size: int = 36) -> ft.Container:
    return ft.Container(
        content=ft.Text(str(number), size=fs(14), weight=ft.FontWeight.BOLD, color=WHITE),
        width=size, height=size, shape=ft.BoxShape.CIRCLE, bgcolor=color, alignment=ft.Alignment.CENTER,
    )


def progress_ring(theme: ThemePreset, fs: FontScale, value: float, color: str, *, size: int = 72,
                  label: Optional[str] = None, sublabel: Optional[str] = None, stroke: int = 7) -> ft.Stack:
    """A ring with a centred label ("64%", "3/5")."""
    value = max(0.0, min(1.0, value))
    centre: list[ft.Control] = []
    if label is not None:
        centre.append(ft.Text(label, size=fs(15 if size >= 64 else 12), weight=ft.FontWeight.BOLD, color=theme.text))
    if sublabel is not None:
        centre.append(ft.Text(sublabel, size=fs(10), color=theme.text_muted))
    return ft.Stack(
        [
            ft.ProgressRing(value=value, stroke_width=stroke, color=color, bgcolor=tint(color, 0.18),
                            width=size, height=size),
            ft.Container(
                content=ft.Column(centre, spacing=0, tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                width=size, height=size, alignment=ft.Alignment.CENTER,
            ),
        ],
        width=size, height=size,
    )


def xp_bar(theme: ThemePreset, fraction: float, *, width: int = 320, height: int = 10,
           color: Optional[str] = None) -> tuple[ft.Container, ft.Container]:
    """A track + fill pair. The fill starts at 0 and is meant to be widened
    from a page task (`fill.width = width * fraction; fill.update()`) so it
    animates in. Returns (track, fill)."""
    fill = ft.Container(
        width=0, height=height, border_radius=999,
        gradient=ft.LinearGradient(colors=[color or theme.gradient[0], theme.gradient[1]]),
        animate=ft.Animation(700, ft.AnimationCurve.EASE_OUT_CUBIC),
    )
    fill.data = max(0.0, min(1.0, fraction)) * width  # target width, read by the caller
    track = ft.Container(
        content=ft.Row([fill], spacing=0), width=width, height=height, border_radius=999,
        bgcolor=tint(theme.text, 0.12),
    )
    return track, fill


# -- cards -------------------------------------------------------------------

def section_title(theme: ThemePreset, fs: FontScale, title: str, *, icon: Optional[ft.IconData] = None,
                  color: Optional[str] = None, size: int = 17) -> ft.Row:
    children: list[ft.Control] = []
    if icon is not None:
        children.append(ft.Icon(icon, color=color or theme.primary, size=fs(size + 3)))
    children.append(ft.Text(title, size=fs(size), weight=ft.FontWeight.BOLD, color=theme.text, expand=True))
    return ft.Row(children, spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER)


def card(
    theme: ThemePreset,
    fs: FontScale,
    title: Optional[str],
    children: Sequence[ft.Control],
    *,
    icon: Optional[ft.IconData] = None,
    accent: Optional[str] = None,
    border_color: Optional[str] = None,
    border_width: int = 1,
    visible: bool = True,
    margin_top: Optional[int] = None,
    spacing: int = 12,
    title_size: int = 17,
    hover: bool = False,
    on_click=None,
    padding: int = 22,
    bgcolor: Optional[str] = None,
    gradient: Optional[ft.LinearGradient] = None,
) -> ft.Container:
    """The rounded content card used everywhere.

    `accent` draws a coloured stripe down the left edge and colours the
    title icon; `hover` adds the lift/glow effect for clickable cards.
    `title=None` omits the heading row."""
    controls: list[ft.Control] = []
    if title:
        controls.append(section_title(theme, fs, title, icon=icon, color=accent, size=title_size))
    controls.extend(children)
    body = ft.Column(controls, spacing=spacing)

    outer_kwargs = dict(
        visible=visible,
        margin=ft.Margin.only(top=margin_top) if margin_top is not None else None,
        shadow=shadow(theme, blur=14, y=6, alpha=0.18),
        on_click=on_click, ink=on_click is not None,
    )
    if accent:
        # Accent stripe = the outer container's colour showing through a
        # 5px left padding. (A Row with CrossAxisAlignment.STRETCH would
        # need a bounded height, which a scrolling Column never provides,
        # and a one-sided Border can't be combined with a border radius.)
        inner = ft.Container(
            content=body,
            bgcolor=None if gradient else (bgcolor or theme.card), gradient=gradient,
            border_radius=ft.BorderRadius.only(
                top_left=RADIUS - 6, bottom_left=RADIUS - 6, top_right=RADIUS, bottom_right=RADIUS,
            ),
            padding=padding,
            border=ft.Border.all(border_width, border_color) if border_color else None,
        )
        container = ft.Container(
            content=inner, bgcolor=accent, border_radius=RADIUS, padding=ft.Padding.only(left=5),
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS, **outer_kwargs,
        )
    else:
        container = ft.Container(
            content=body,
            bgcolor=None if gradient else (bgcolor or theme.card), gradient=gradient,
            border_radius=RADIUS, padding=padding,
            border=ft.Border.all(border_width, border_color) if border_color else None,
            **outer_kwargs,
        )
    if hover:
        hover_lift(container, theme, glow_color=accent)
    return container


def hero_banner(
    theme: ThemePreset,
    fs: FontScale,
    title: str,
    subtitle: str,
    *,
    leading: Optional[ft.Control] = None,
    trailing: Sequence[ft.Control] = (),
    below: Sequence[ft.Control] = (),
    gradient: Optional[tuple[str, str]] = None,
    title_size: int = 30,
) -> ft.Container:
    """Gradient header block: [leading] title/subtitle ... [trailing], then
    an optional row of controls underneath (stat pills, buttons)."""
    start, end = gradient or theme.gradient
    text_column = ft.Column(
        [
            ft.Text(title, size=fs(title_size), weight=ft.FontWeight.BOLD, color=WHITE),
            ft.Text(subtitle, size=fs(14), color=tint(WHITE, 0.85)),
        ],
        spacing=4, expand=True,
    )
    top_children: list[ft.Control] = []
    if leading is not None:
        top_children.append(leading)
    top_children.append(text_column)
    top_children.extend(trailing)
    rows: list[ft.Control] = [ft.Row(top_children, spacing=18, vertical_alignment=ft.CrossAxisAlignment.CENTER)]
    if below:
        rows.append(ft.Row(list(below), spacing=12, wrap=True, vertical_alignment=ft.CrossAxisAlignment.CENTER))
    return ft.Container(
        content=ft.Column(rows, spacing=18),
        gradient=ft.LinearGradient(begin=ft.Alignment.TOP_LEFT, end=ft.Alignment.BOTTOM_RIGHT, colors=[start, end]),
        border_radius=RADIUS + 6, padding=ft.Padding.symmetric(horizontal=28, vertical=26),
        shadow=glow(start, alpha=0.35, blur=32),
    )


def nav_tile(
    page: ft.Page,
    theme: ThemePreset,
    fs: FontScale,
    *,
    icon: ft.IconData,
    title: str,
    subtitle: str,
    status: str,
    route: str,
    color: str,
    extra: Optional[ft.Control] = None,
) -> ft.Container:
    """A clickable tile: tinted icon circle, title, subtitle, a bold status
    line (progress), optional extra control (e.g. a mini bar) and a chevron."""
    body = ft.Row(
        [
            icon_circle(icon, color, size=52, icon_size=fs(26)),
            ft.Column(
                [
                    ft.Text(title, size=fs(18), weight=ft.FontWeight.BOLD, color=theme.text),
                    ft.Text(subtitle, size=fs(12), color=theme.text_muted, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
                    ft.Text(status, size=fs(12), weight=ft.FontWeight.BOLD, color=color),
                    *([extra] if extra is not None else []),
                ],
                spacing=4, expand=True,
            ),
            ft.Icon(ft.Icons.CHEVRON_RIGHT_ROUNDED, color=theme.text_muted, size=fs(24)),
        ],
        spacing=16, vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )
    tile = ft.Container(
        content=body, bgcolor=theme.card, border_radius=RADIUS, padding=20,
        border=ft.Border.all(1, tint(color, 0.35)),
        on_click=route_handler(page, route), ink=True,
    )
    return hover_lift(tile, theme, glow_color=color)


def header_row(
    theme: ThemePreset,
    fs: FontScale,
    title: str,
    on_back,
    *,
    back_label: str = "← Back",
    trailing: Sequence[ft.Control] = (),
    title_size: int = 24,
    subtitle: Optional[str] = None,
    icon: Optional[ft.IconData] = None,
) -> ft.Row:
    """Back icon-button + title (+ optional subtitle) + trailing controls."""
    title_children: list[ft.Control] = [
        ft.Text(title, size=fs(title_size), weight=ft.FontWeight.BOLD, color=theme.text, max_lines=2,
                overflow=ft.TextOverflow.ELLIPSIS),
    ]
    if subtitle:
        title_children.append(ft.Text(subtitle, size=fs(12), color=theme.text_muted))
    leading: list[ft.Control] = [
        icon_button(ft.Icons.ARROW_BACK_ROUNDED, on_back, theme, tooltip=back_label.replace("← ", "Back to ")),
    ]
    if icon is not None:
        leading.append(ft.Icon(icon, color=theme.primary, size=fs(title_size + 2)))
    return ft.Row(
        [*leading, ft.Column(title_children, spacing=2, expand=True), *trailing],
        spacing=14, vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )


def empty_state(theme: ThemePreset, fs: FontScale, icon: ft.IconData, title: str, body: str) -> ft.Container:
    return ft.Container(
        content=ft.Column(
            [
                icon_circle(icon, theme.text_muted, size=64, icon_size=fs(30)),
                ft.Text(title, size=fs(16), weight=ft.FontWeight.BOLD, color=theme.text),
                ft.Text(body, size=fs(13), color=theme.text_muted, text_align=ft.TextAlign.CENTER),
            ],
            spacing=8, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=32, alignment=ft.Alignment.CENTER,
    )


# -- multiple choice -----------------------------------------------------------

class MultipleChoiceCard:
    """Walks through a list of QuizQuestions one at a time inside a card:
    lettered option rows, correct/incorrect highlighting, the explanation,
    a slim progress bar and a Next/finish button. Questions cross-fade via
    an AnimatedSwitcher. Reports each answer and the final tally through
    callbacks; the owner decides what a finished run means.

    `control` is the card to place in a view. Call `start(questions)` to
    (re)begin, and `show_summary(...)` to replace the question area with a
    message plus any follow-up actions (e.g. a Try Again button)."""

    def __init__(
        self,
        page: ft.Page,
        theme: ThemePreset,
        fs: FontScale,
        title: str,
        *,
        on_answer: Optional[Callable[[QuizQuestion, bool], None]] = None,
        on_complete: Optional[Callable[[int, int], None]] = None,
        final_label: str = "Finish",
        show_score: bool = False,
        accent: Optional[str] = None,
    ) -> None:
        self.page = page
        self.theme = theme
        self.fs = fs
        self._on_answer = on_answer
        self._on_complete = on_complete
        self._final_label = final_label
        self._show_score = show_score
        self.accent = accent or theme.primary

        self.questions: list[QuizQuestion] = []
        self.index = 0
        self.score = 0
        self._answered = False

        self.progress_text = ft.Text("", size=fs(13), color=theme.text_muted)
        self.progress_bar = ft.ProgressBar(value=0, color=self.accent, bgcolor=tint(self.accent, 0.15),
                                           bar_height=6, border_radius=999)
        self.question_text = ft.Text("", size=fs(17), weight=ft.FontWeight.BOLD, color=theme.text)
        self.options_column = ft.Column([], spacing=10)
        self.body = ft.Column([self.question_text, self.options_column], spacing=16)
        self.switcher = ft.AnimatedSwitcher(
            content=self.body, duration=260, reverse_duration=160,
            transition=ft.AnimatedSwitcherTransition.FADE,
            switch_in_curve=ft.AnimationCurve.EASE_OUT, switch_out_curve=ft.AnimationCurve.EASE_IN,
        )
        self.feedback_icon = ft.Icon(ft.Icons.LIGHTBULB_ROUNDED, color=theme.text_muted, size=fs(20), visible=False)
        self.feedback_text = ft.Text("", size=fs(13), expand=True)
        self.feedback_row = ft.Row([self.feedback_icon, self.feedback_text], spacing=10,
                                   vertical_alignment=ft.CrossAxisAlignment.START)
        self.next_button = button("Next →", self._on_next, theme, "primary", visible=False,
                                  icon=ft.Icons.ARROW_FORWARD_ROUNDED)
        self.actions_row = ft.Row([self.next_button], spacing=10, wrap=True)

        self.control = card(theme, fs, title, [
            ft.Row([self.progress_text], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            self.progress_bar,
            self.switcher,
            self.feedback_row,
            self.actions_row,
        ], icon=ft.Icons.PSYCHOLOGY, accent=self.accent)

    # -- public API -----------------------------------------------------
    @property
    def visible(self) -> bool:
        return bool(self.control.visible)

    @visible.setter
    def visible(self, value: bool) -> None:
        self.control.visible = value

    @property
    def total(self) -> int:
        return len(self.questions)

    def start(self, questions: Sequence[QuizQuestion]) -> None:
        self.questions = list(questions)
        self.index = 0
        self.score = 0
        self.actions_row.controls = [self.next_button]
        self.control.visible = True
        self._render_question(fresh=False)

    def show_summary(self, message: str, color: str, actions: Sequence[ft.Control] = ()) -> None:
        self.progress_text.value = message
        self.progress_text.color = color
        self.question_text.value = ""
        self.options_column.controls = []
        self.feedback_text.value = ""
        self.feedback_icon.visible = False
        self.next_button.visible = False
        self.actions_row.controls = [self.next_button, *actions]

    # Keyboard entry points (see app.ui.shortcuts): pick an option by index,
    # or advance when the current question has been answered.
    def select_option(self, index: int) -> None:
        if self.questions and 0 <= index < len(self.options_column.controls):
            self._on_select(index)

    def advance(self) -> None:
        if self.questions and self._answered and self.next_button.visible:
            self._on_next(None)

    # -- rendering ------------------------------------------------------
    def _progress_label(self) -> str:
        label = f"Question {self.index + 1} of {self.total}"
        if self._show_score:
            label += f"  ·  Score {self.score}"
        return label

    def _option_row(self, index: int, text: str) -> ft.Container:
        theme = self.theme
        letter = ft.Container(
            content=ft.Text(OPTION_LETTERS[index % len(OPTION_LETTERS)], size=self.fs(13),
                            weight=ft.FontWeight.BOLD, color=self.accent),
            width=32, height=32, shape=ft.BoxShape.CIRCLE, bgcolor=tint(self.accent, 0.16),
            alignment=ft.Alignment.CENTER,
        )
        label = ft.Text(text, size=self.fs(14), color=theme.text, expand=True)
        row = ft.Container(
            content=ft.Row([letter, label], spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=theme.surface, border_radius=RADIUS_SM, padding=ft.Padding.symmetric(horizontal=14, vertical=10),
            border=ft.Border.all(1, tint(theme.text, 0.08)),
            on_click=lambda _e, i=index: self._on_select(i), ink=True,
            animate=ft.Animation(220, ft.AnimationCurve.EASE_OUT),
            animate_scale=ft.Animation(220, ft.AnimationCurve.EASE_OUT_BACK), scale=1.0,
        )
        row.data = {"letter": letter, "label": label}
        return row

    def _render_question(self, fresh: bool = True) -> None:
        theme = self.theme
        question = self.questions[self.index]
        self.progress_text.value = self._progress_label()
        self.progress_text.color = theme.text_muted
        self.progress_bar.value = self.index / max(1, self.total)

        self.question_text = ft.Text(question.question, size=self.fs(17), weight=ft.FontWeight.BOLD, color=theme.text)
        self.options_column = ft.Column(
            [self._option_row(i, text) for i, text in enumerate(question.options)], spacing=10,
        )
        self.body = ft.Column([self.question_text, self.options_column], spacing=16)
        # Reassigning the switcher's content is what triggers the cross-fade.
        self.switcher.content = self.body

        self.feedback_text.value = ""
        self.feedback_icon.visible = False
        self.next_button.visible = False
        self._answered = False

    def _paint_option(self, row: ft.Container, color: str) -> None:
        row.bgcolor = color
        row.border = ft.Border.all(1, color)
        row.data["label"].color = WHITE
        row.data["letter"].bgcolor = tint(WHITE, 0.25)
        row.data["letter"].content.color = WHITE

    def _on_select(self, index: int) -> None:
        if self._answered:
            return
        self._answered = True
        theme = self.theme
        question = self.questions[self.index]
        is_correct = index == question.correct
        if is_correct:
            self.score += 1

        for i, row in enumerate(self.options_column.controls):
            row.on_click = None
            row.ink = False
            if i == question.correct:
                self._paint_option(row, theme.success)
                row.scale = 1.02
            elif i == index:
                self._paint_option(row, theme.danger)
            else:
                row.opacity = 0.55

        self.feedback_icon.icon = ft.Icons.CHECK_CIRCLE_ROUNDED if is_correct else ft.Icons.ERROR_OUTLINE_ROUNDED
        self.feedback_icon.color = theme.success if is_correct else theme.danger
        self.feedback_icon.visible = True
        self.feedback_text.value = ("Correct. " if is_correct else "Not quite. ") + question.explanation
        self.feedback_text.color = theme.success if is_correct else theme.danger
        is_last = self.index + 1 >= self.total
        self.next_button.content = self._final_label if is_last else "Next →"
        self.next_button.icon = ft.Icons.FLAG_ROUNDED if is_last else ft.Icons.ARROW_FORWARD_ROUNDED
        self.next_button.visible = True
        self.progress_text.value = self._progress_label()
        self.progress_bar.value = (self.index + 1) / max(1, self.total)

        if self._on_answer is not None:
            self._on_answer(question, is_correct)
        self.page.update()

    def _on_next(self, _e) -> None:
        self.index += 1
        if self.index >= self.total:
            if self._on_complete is not None:
                self._on_complete(self.score, self.total)
        else:
            self._render_question()
        self.page.update()
