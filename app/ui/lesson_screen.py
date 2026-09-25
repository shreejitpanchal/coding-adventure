"""The Explain -> Example -> Try It -> Run -> Result flow for a single
exercise -- or, for a purely conceptual exercise (Exercise.requires_code
is False, e.g. the `architecture` track), Explain -> Example ->
Comprehension Check instead, with no code editor, Run button, or
execution engine involved at all.

Every section is an accent-striped card with its own icon; the Run
button pulses while code executes; a pass fires a confetti burst, a
spring-in reward card and an XP count-up. The pass/fail decision itself
lives in app.engine.run_evaluation; this module only renders it."""
from __future__ import annotations

import asyncio
import logging
import time
from typing import Optional

import flet as ft

from app.config.clock import today_iso
from app.engine.categories import get_category_meta
from app.engine.exercise import Exercise
from app.engine.quiz import QuizQuestion
from app.engine.quiz_engine import shuffle_options
from app.engine.run_evaluation import RunOutcome, Verdict, evaluate_run
from app.execution.base import DEFAULT_TIMEOUT_SECONDS, RunHandle
from app.execution.toolchain_check import check_toolchain
from app.progress.achievements import evaluate_lesson_completion_achievements
from app.ui.app_state import AppState
from app.ui.code_editor import frame_editor, make_code_editor, make_read_only_code_block
from app.ui.components import (
    WHITE,
    MultipleChoiceCard,
    button,
    card,
    chip,
    difficulty_color,
    difficulty_label,
    format_duration,
    header_row,
    icon_button,
    icon_circle,
    is_compact,
    spacer,
    tint,
    view_padding,
)
from app.ui.motion import Pulser, Stagger, confetti, confetti_layer, count_up, pop_in, prepare_pop
from app.ui.shortcuts import Shortcuts
from app.ui.theme import CODE_FONT_FAMILY, scaled

logger = logging.getLogger(__name__)

_VERDICT_STYLE: dict[Verdict, tuple[ft.IconData, str]] = {
    Verdict.BLOCKED: (ft.Icons.ERROR_OUTLINE_ROUNDED, "danger"),
    Verdict.TIMED_OUT: (ft.Icons.TIMER_ROUNDED, "danger"),
    Verdict.ERROR: (ft.Icons.BUG_REPORT_ROUNDED, "danger"),
    Verdict.WRONG_OUTPUT: (ft.Icons.SPORTS_SCORE_ROUNDED, "warning"),
    Verdict.MISSING_PATTERNS: (ft.Icons.LIGHTBULB_ROUNDED, "warning"),
    Verdict.PASSED: (ft.Icons.CHECK_CIRCLE_ROUNDED, "success"),
}


def build_lesson_view(page: ft.Page, state: AppState, exercise_id: str) -> ft.View:
    theme = state.theme
    exercise = state.exercise_engine().get(exercise_id)

    if exercise is None:
        logger.warning("Lesson route for unknown exercise id %r in track %s", exercise_id, state.language)
        return ft.View(
            route=f"/lesson/{exercise_id}",
            bgcolor=theme.bg,
            padding=24,
            controls=[
                ft.Text(f"Couldn't find exercise '{exercise_id}'.", color=theme.danger),
                button("Back", lambda _e: page.go(state.lesson_return_route), theme, icon=ft.Icons.ARROW_BACK_ROUNDED),
            ],
        )

    return _ExerciseController(page, state, exercise).build_view()


class _ExerciseController:
    _PRACTICE_THRESHOLD = 3

    def __init__(self, page: ft.Page, state: AppState, exercise: Exercise) -> None:
        self.page = page
        self.state = state
        self.exercise = exercise
        self.theme = state.theme
        self.scale = state.font_scale
        self.meta = get_category_meta(exercise.category)
        self.accent = self.meta.color
        self.engine = state.execution_engine(exercise.language) if exercise.requires_code else None

        self._running = False
        self._run_handle: Optional[RunHandle] = None
        self._hint_index = 0
        self._passed = False
        self._next_exercise_id: Optional[str] = None
        self.input_field: Optional[ft.TextField] = None
        self._pulser: Optional[Pulser] = None
        # A failed attempt only counts against the review schedule when
        # this exercise had already been passed before (i.e. it's a review).
        self._was_completed = state.progress.is_lesson_completed(state.language, exercise.id)
        self._review_state = state.progress.get_review_state(state.language, exercise.id)
        self._review_failed = False
        # Personal-best timer: from opening the exercise to the passing run.
        self._opened_at = time.monotonic()
        self._best_seconds = state.progress.get_best_solve_time(state.language, exercise.id)

        state.progress.set_current_exercise(state.language, exercise.id)

    def _fs(self, base: int) -> int:
        return scaled(base, self.scale)

    def _card(self, title: Optional[str], children, **kwargs) -> ft.Container:
        kwargs.setdefault("accent", self.accent)
        return card(self.theme, self._fs, title, children, **kwargs)

    # -- view -------------------------------------------------------------
    def build_view(self) -> ft.View:
        theme = self.theme
        exercise = self.exercise
        stagger = Stagger(self.page, step=0.05)

        is_bookmarked = self.state.progress.is_bookmarked(self.state.language, exercise.id)
        self.bookmark_button = icon_button(
            ft.Icons.BOOKMARK_BORDER_ROUNDED, self._on_toggle_bookmark, theme,
            selected=is_bookmarked, selected_icon=ft.Icons.BOOKMARK_ROUNDED,
            color=theme.warning, tooltip="Bookmark this exercise",
        )
        trailing: list[ft.Control] = [
            chip(difficulty_label(exercise.difficulty), difficulty_color(theme, exercise.difficulty), self._fs),
            chip(f"{exercise.xp_reward} XP", theme.warning, self._fs, icon=ft.Icons.BOLT),
        ]
        if self._best_seconds is not None:
            trailing.insert(0, chip(f"Best {format_duration(self._best_seconds)}", theme.success, self._fs,
                                    icon=ft.Icons.TIMER_ROUNDED))
        if self._review_state is not None:
            days = self._review_state.days_until_due(today_iso())
            if days <= 0:
                trailing.insert(0, chip("Review due", theme.accent, self._fs, icon=ft.Icons.REPLAY_ROUNDED, filled=True))
            else:
                trailing.insert(0, chip(f"Review in {days}d", theme.accent, self._fs, icon=ft.Icons.REPLAY_ROUNDED))
        trailing.append(self.bookmark_button)
        header = header_row(
            theme, self._fs, exercise.title, self._on_menu,
            subtitle=f"{self.meta.icon} {self.meta.title} · level {exercise.category_level}",
            trailing=trailing, title_size=22, compact=is_compact(self.page),
        )

        explanation_card = self._card("Objective", [
            ft.Text(exercise.objective.strip(), size=self._fs(15), weight=ft.FontWeight.BOLD, color=theme.text),
            ft.Text(exercise.explanation.strip(), size=self._fs(14), color=theme.text_muted),
        ], icon=ft.Icons.FLAG_ROUNDED)

        sections: list[ft.Control] = [explanation_card]

        if exercise.example_code.strip():
            example_children: list[ft.Control] = [
                make_read_only_code_block(exercise.example_code.strip(), scale=self.scale, theme=theme, filename="example"),
            ]
            if exercise.requires_code:
                example_children.append(ft.Row([
                    button("Copy example into editor", self._on_copy_example, theme, "ghost",
                           icon=ft.Icons.CONTENT_COPY_ROUNDED, height=38),
                ]))
            sections.append(self._card("Example", example_children, icon=ft.Icons.MENU_BOOK_ROUNDED))

        self._build_reward_card()

        if exercise.requires_code:
            if exercise.challenge.strip():
                sections.append(self._card("Your Task", [
                    ft.Text(exercise.challenge.strip(), size=self._fs(14), color=theme.text),
                ], icon=ft.Icons.ROCKET_LAUNCH, accent=theme.primary))
            sections.append(self._build_code_card())
            sections.append(self._build_output_card())
        else:
            if exercise.challenge.strip():
                sections.append(self._card("Think About It", [
                    ft.Text(exercise.challenge.strip(), size=self._fs(14), color=theme.text),
                ], icon=ft.Icons.PSYCHOLOGY, accent=theme.primary))
            sections.append(self._build_comprehension_card())

        sections.append(self._build_notes_card())

        controls: list[ft.Control] = [header, spacer(8)]
        controls.extend(stagger.wrap(section) for section in sections)
        controls.append(self.reward_card)
        stagger.play()

        self._content_column = ft.Column(controls, scroll=ft.ScrollMode.AUTO, spacing=14, expand=True)
        # Inside a Stack, children fill the area via edge positioning (not `expand`).
        content = ft.Container(content=self._content_column, padding=view_padding(self.page),
                               left=0, top=0, right=0, bottom=0)
        self.confetti = confetti_layer()

        # Installed here, removed by app_window.route_change() on every
        # navigation (not only via our own Back button). Ctrl-combos only:
        # plain letters would fire while typing in the editor.
        shortcuts = Shortcuts().bind("escape", lambda: self._on_menu(None))
        shortcuts.bind("ctrl+b", lambda: self._on_toggle_bookmark(None))
        shortcuts.bind("ctrl+n", lambda: self._on_next(None))
        if exercise.requires_code:
            shortcuts.bind("ctrl+enter", self._run_from_keyboard)
            shortcuts.bind("ctrl+h", lambda: self._on_hint(None))
            shortcuts.bind("ctrl+r", lambda: self._on_reset(None))
        shortcuts.install(self.page)
        return ft.View(
            route=f"/lesson/{exercise.id}", bgcolor=theme.bg, padding=0,
            controls=[ft.Stack([content, self.confetti], expand=True)],
        )

    # -- cards ------------------------------------------------------------
    def _build_code_card(self) -> ft.Control:
        theme = self.theme
        exercise = self.exercise

        # Scale the editor to the starter code's actual length instead of a
        # fixed 260px -- a short snippet no longer sits in a mostly-empty
        # box, and a long one gets room before scrolling kicks in.
        starter_lines = exercise.starter_code.strip().count("\n") + 1
        editor_height = max(180, min(520, 30 * starter_lines + 50))
        self.editor = make_code_editor(exercise.starter_code.strip(), height=editor_height, scale=self.scale, theme=theme)
        children: list[ft.Control] = [
            frame_editor(self.editor, theme, filename=f"solution.{_extension(exercise.language)}", scale=self.scale),
        ]

        if exercise.input_prompt:
            self.input_field = ft.TextField(
                hint_text="Type input...", width=280, border_radius=12, prefix_icon=ft.Icons.KEYBOARD_RETURN_ROUNDED,
                bgcolor=theme.surface, border_color=tint(theme.text, 0.12), focused_border_color=self.accent,
            )
            children.append(ft.Column(
                [ft.Text(exercise.input_prompt, size=self._fs(14), color=theme.text), self.input_field],
                spacing=6,
            ))

        # Browsing an exercise (reading the explanation/example, looking at
        # the challenge, editing code) never needs the language's real
        # toolchain -- only actually running code does. Checked here,
        # proactively, so the Run button is disabled up front on a machine
        # (or platform, e.g. Android) that can't run this language,
        # instead of only failing after the click via ExecutionResult.blocked.
        toolchain_ready = check_toolchain(exercise.language).available

        self.run_button = button(
            "Run" if toolchain_ready else "Run (unavailable here)", self._on_run, theme, "success",
            icon=ft.Icons.PLAY_ARROW_ROUNDED, height=48, disabled=not toolchain_ready,
            tooltip=(
                "Ctrl+Enter also runs your code"
                if toolchain_ready else "This language's compiler/runtime isn't available on this device."
            ),
        )
        self.run_wrap = ft.Container(content=self.run_button)
        self._pulser = Pulser(self.page, self.run_wrap)
        reset_button = button("Reset", self._on_reset, theme, "ghost", icon=ft.Icons.REFRESH_ROUNDED)
        self.hint_button = button("Hint", self._on_hint, theme, "warning", icon=ft.Icons.LIGHTBULB_ROUNDED,
                                  disabled=not exercise.hints)
        keys_help = Shortcuts().describe(
            ("ctrl+enter", "run"), ("ctrl+h", "hint"), ("ctrl+r", "reset"), ("ctrl+b", "bookmark"), ("escape", "back"),
        )
        children.append(ft.Row(
            [self.run_wrap, reset_button, self.hint_button],
            spacing=10, wrap=True, vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ))
        children.append(ft.Text(keys_help, size=self._fs(11), color=theme.text_muted))

        if not toolchain_ready:
            children.append(ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.ERROR_OUTLINE_ROUNDED, color=theme.warning, size=self._fs(18)),
                    ft.Text(
                        "Running is unavailable here -- this language's compiler/runtime isn't installed "
                        "(or isn't supported on this device). You can still read through and edit the exercise.",
                        size=self._fs(12), color=theme.warning, expand=True,
                    ),
                ], spacing=8),
                bgcolor=tint(theme.warning, 0.10), border_radius=10, padding=10,
            ))

        self.hint_text = ft.Text("", size=self._fs(13), color=theme.warning)
        self.hint_box = ft.Container(
            content=ft.Row([ft.Icon(ft.Icons.LIGHTBULB_ROUNDED, color=theme.warning, size=self._fs(18)), self.hint_text],
                           spacing=8, vertical_alignment=ft.CrossAxisAlignment.START),
            bgcolor=tint(theme.warning, 0.10), border_radius=10, padding=10, visible=False,
            animate_opacity=ft.Animation(250, ft.AnimationCurve.EASE_OUT),
        )
        children.append(self.hint_box)

        return self._card("Your Code", children, icon=ft.Icons.CODE_ROUNDED, accent=theme.success)

    def _build_comprehension_card(self) -> ft.Control:
        """A short inline multiple-choice check that gates completion for a
        requires_code=False exercise. Answering every question correctly in
        one pass calls _on_success(); any wrong answer requires retrying the
        whole check from the start."""
        self.check = MultipleChoiceCard(
            self.page, self.theme, self._fs, "Comprehension Check",
            on_complete=self._on_check_complete, final_label="Finish", accent=self.accent,
        )
        self._start_check()
        return self.check.control

    def _start_check(self) -> None:
        questions: list[QuizQuestion] = [shuffle_options(q) for q in self.exercise.comprehension_check]
        self.check.start(questions)

    def _on_check_complete(self, score: int, total: int) -> None:
        if score == total:
            self._on_success()
            return
        retry = button("Try Again", lambda _e: (self._start_check(), self.page.update()), self.theme, "warning",
                       icon=ft.Icons.REPLAY_ROUNDED)
        self.check.show_summary(
            f"You missed {total - score} of {total}. Review the explanations, then try again.",
            self.theme.warning, actions=[retry],
        )

    def _build_output_card(self) -> ft.Control:
        theme = self.theme
        self.output_icon = ft.Icon(ft.Icons.TERMINAL, color=theme.text_muted, size=self._fs(22))
        self.output_text = ft.Text("Press Run to see what happens.", size=self._fs(14), color=theme.text_muted,
                                   font_family=CODE_FONT_FAMILY, selectable=True, expand=True)
        self.output_box = ft.Container(
            content=ft.Row([self.output_icon, self.output_text], spacing=12, vertical_alignment=ft.CrossAxisAlignment.START),
            bgcolor=theme.surface, border_radius=12, padding=14,
            border=ft.Border.all(1, tint(theme.text, 0.08)),
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
        )
        self.details_button = button("Show raw output", self._toggle_details, theme, "ghost", visible=False, height=36,
                                     icon=ft.Icons.TERMINAL)
        self.details_text = ft.Text("", size=self._fs(12), font_family=CODE_FONT_FAMILY, color=theme.text, selectable=True)
        self.details_container = ft.Container(
            content=self.details_text, bgcolor=theme.surface, border_radius=10, padding=12, visible=False,
        )
        self.practice_row = ft.Row([], spacing=8, wrap=True)
        self.practice_container = ft.Container(
            content=ft.Column(
                [
                    ft.Row([ft.Icon(ft.Icons.SCHOOL_ROUNDED, color=theme.warning, size=self._fs(18)),
                            ft.Text("Stuck? Related practice:", size=self._fs(13), weight=ft.FontWeight.BOLD, color=theme.text)],
                           spacing=8),
                    self.practice_row,
                ],
                spacing=8,
            ),
            bgcolor=tint(theme.warning, 0.08), border=ft.Border.all(1, tint(theme.warning, 0.4)), border_radius=10,
            padding=12, visible=False,
        )
        return self._card("Output", [self.output_box, self.details_button, self.details_container, self.practice_container],
                          icon=ft.Icons.TERMINAL, accent=theme.text_muted)

    def _build_notes_card(self) -> ft.Control:
        theme = self.theme
        existing_note = self.state.progress.get_note(self.state.language, self.exercise.id)
        self.notes_field = ft.TextField(
            value=existing_note, multiline=True, min_lines=3, max_lines=8, height=150, border_radius=12,
            hint_text="Jot down anything worth remembering about this exercise...",
            bgcolor=theme.surface, border_color=tint(theme.text, 0.12), focused_border_color=self.accent,
        )
        self.notes_status_text = ft.Text("", size=self._fs(12), color=theme.success)
        save_button = button("Save note", self._on_save_note, theme, "primary", icon=ft.Icons.SAVE_ROUNDED, height=40)
        return self._card("Your Notes", [
            self.notes_field, ft.Row([save_button, self.notes_status_text], spacing=10),
        ], icon=ft.Icons.EDIT_NOTE_ROUNDED, accent=theme.accent)

    def _build_reward_card(self) -> None:
        theme = self.theme
        self.reward_xp_text = ft.Text("+0 XP", size=self._fs(26), weight=ft.FontWeight.BOLD, color=WHITE)
        self.reward_title = ft.Text("Nice work!", size=self._fs(20), weight=ft.FontWeight.BOLD, color=WHITE)
        self.reward_review_text = ft.Text("", size=self._fs(12), color=tint(WHITE, 0.9))
        self.achievement_row = ft.Row([], spacing=8, wrap=True)
        self.next_button = button("Next exercise", self._on_next, theme, "success", icon=ft.Icons.ARROW_FORWARD_ROUNDED,
                                  height=46, visible=False, bgcolor=tint(WHITE, 0.22))
        back_button = button("Back", self._on_menu, theme, "ghost", icon=ft.Icons.ARROW_BACK_ROUNDED, height=46)
        self.reward_card = ft.Container(
            content=ft.Row(
                [
                    icon_circle(ft.Icons.EMOJI_EVENTS, WHITE, size=64, icon_size=self._fs(34)),
                    ft.Column(
                        [
                            self.reward_title,
                            self.reward_xp_text,
                            self.reward_review_text,
                            self.achievement_row,
                            ft.Row([self.next_button, back_button], spacing=10, wrap=True),
                        ],
                        spacing=8, expand=True,
                    ),
                ],
                spacing=18, vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            gradient=ft.LinearGradient(begin=ft.Alignment.TOP_LEFT, end=ft.Alignment.BOTTOM_RIGHT,
                                       colors=[theme.success, theme.gradient[1]]),
            border_radius=22, padding=22, visible=False,
        )
        prepare_pop(self.reward_card)

    # -- run flow -----------------------------------------------------
    async def _run_from_keyboard(self) -> None:
        if not self.run_button.disabled and not self._running:
            await self._on_run(None)

    async def _on_run(self, e) -> None:
        if self._running or self.engine is None:
            return
        self._running = True
        self.run_button.disabled = True
        self.run_button.content = "Running…"
        self.run_button.icon = ft.Icons.HOURGLASS_TOP_ROUNDED
        self._hide_details()
        self._set_output(ft.Icons.HOURGLASS_TOP_ROUNDED, "Running your code…", self.theme.text_muted)
        self.page.update()
        if self._pulser:
            self._pulser.start()

        code = self.editor.value or ""
        handle = RunHandle()
        self._run_handle = handle

        input_value = self.input_field.value if self.input_field is not None else None
        stdin_text = f"{input_value}\n" if input_value is not None else None

        try:
            result = await asyncio.to_thread(
                self.engine.run, code, DEFAULT_TIMEOUT_SECONDS, handle, stdin_text, self.exercise,
            )
        except Exception:
            logger.exception("Engine %s raised while running exercise %s", self.exercise.language, self.exercise.id)
            self._finish_running()
            self._set_output(ft.Icons.ERROR_OUTLINE_ROUNDED,
                             "The runner hit an internal error. Details were written to the app log.", self.theme.danger)
            self.page.update()
            return

        outcome = evaluate_run(result, self.exercise, code, input_value)
        self._render_outcome(outcome)

    def _finish_running(self) -> None:
        self._running = False
        if self._pulser:
            self._pulser.stop()
        self.run_button.disabled = False
        self.run_button.content = "Run"
        self.run_button.icon = ft.Icons.PLAY_ARROW_ROUNDED

    def _render_outcome(self, outcome: RunOutcome) -> None:
        self._finish_running()
        theme = self.theme
        icon, tone = _VERDICT_STYLE[outcome.verdict]
        color = {"success": theme.success, "warning": theme.warning, "danger": theme.danger}[tone]
        self._set_output(icon, outcome.message, color, raw=outcome.raw, details_label=outcome.details_label)

        if outcome.passed:
            self._on_success()
        elif outcome.event_type:
            self.state.progress.log_event(self.state.language, self.exercise.id, outcome.event_type, outcome.event_detail)
            self._record_review_failure()
            self._maybe_show_practice()
        self.page.update()

    def _record_review_failure(self) -> None:
        """A wrong attempt at an exercise that was already passed once is a
        failed review: bring it back tomorrow. Only the first failure per
        visit is counted, so retrying in the same sitting isn't punished."""
        if not self._was_completed or self._review_failed:
            return
        self._review_failed = True
        self.state.progress.schedule_review(self.state.language, self.exercise.id, passed=False)

    def _on_reset(self, e) -> None:
        self.editor.value = self.exercise.starter_code.strip()
        if self.input_field is not None:
            self.input_field.value = ""
        self._hide_details()
        self.practice_container.visible = False
        self._set_output(ft.Icons.TERMINAL, "Press Run to see what happens.", self.theme.text_muted)
        self.reward_card.visible = False
        prepare_pop(self.reward_card)
        self._passed = False
        self.page.update()

    def _on_copy_example(self, e) -> None:
        self.editor.value = self.exercise.example_code.strip()
        self.page.update()

    def _on_toggle_bookmark(self, e) -> None:
        progress = self.state.progress
        now_bookmarked = not progress.is_bookmarked(self.state.language, self.exercise.id)
        progress.set_bookmarked(self.state.language, self.exercise.id, now_bookmarked)
        self.bookmark_button.selected = now_bookmarked
        self.page.update()

    def _on_save_note(self, e) -> None:
        self.state.progress.save_note(self.state.language, self.exercise.id, self.notes_field.value or "")
        self.notes_status_text.value = "Saved."
        self.page.update()

    def _on_hint(self, e) -> None:
        if not self.exercise.hints:
            return
        hint = self.exercise.hints[self._hint_index % len(self.exercise.hints)]
        self.hint_text.value = f"Hint {self._hint_index % len(self.exercise.hints) + 1} of {len(self.exercise.hints)}: {hint}"
        self.hint_box.visible = True
        self.state.progress.log_event(self.state.language, self.exercise.id, "hint_used", hint)
        self._hint_index += 1
        self.page.update()

    # -- output helpers -------------------------------------------------
    def _set_output(self, icon: ft.IconData, text: str, color: str, raw: Optional[str] = None,
                    details_label: str = "Show raw output") -> None:
        self.output_icon.icon = icon
        self.output_icon.color = color
        self.output_text.value = text
        self.output_text.color = color
        self.output_box.border = ft.Border.all(1, tint(color, 0.45))
        self.output_box.bgcolor = tint(color, 0.06) if color != self.theme.text_muted else self.theme.surface
        if raw:
            self.details_button.content = details_label
            self.details_button.visible = True
            self.details_text.value = raw
        else:
            self._hide_details()

    def _toggle_details(self, e) -> None:
        self.details_container.visible = not self.details_container.visible
        self.page.update()

    def _hide_details(self) -> None:
        self.details_button.visible = False
        self.details_container.visible = False

    def _maybe_show_practice(self) -> None:
        failures = self.state.progress.get_recent_failure_count(self.state.language, self.exercise.id)
        if failures < self._PRACTICE_THRESHOLD:
            return
        completed_ids = set(self.state.progress.get_completed_lesson_ids(self.state.language))
        suggestions = self.state.exercise_engine().recommend_practice(self.exercise.id, completed_ids)
        if not suggestions:
            return
        self.practice_row.controls = [
            button(ex.title, lambda _e, eid=ex.id: self.page.go(f"/lesson/{eid}"), self.theme, "warning", height=36,
                   icon=ft.Icons.SCHOOL_ROUNDED)
            for ex in suggestions
        ]
        self.practice_container.visible = True

    # -- success --------------------------------------------------------
    def _on_success(self) -> None:
        if self._passed:
            return
        self._passed = True

        progress = self.state.progress
        progress.complete_lesson(self.state.language, self.exercise.id, self.exercise.xp_reward)
        # record_play_today() runs BEFORE the meta-achievement check below,
        # since a streak milestone badge needs streak_days to already
        # reflect today's play.
        progress.record_play_today(self.state.language)

        earned_badges: list[str] = []
        if self.exercise.achievement and progress.award_badge(self.state.language, self.exercise.achievement):
            earned_badges.append(self.exercise.achievement)
        earned_badges.extend(evaluate_lesson_completion_achievements(
            progress, self.state.exercise_engine(), self.state.language, self.exercise.category,
        ))
        logger.info("Completed %s/%s (+%d XP, badges=%s)", self.state.language, self.exercise.id,
                    self.exercise.xp_reward, earned_badges)

        review = progress.schedule_review(self.state.language, self.exercise.id, passed=True)
        elapsed = int(time.monotonic() - self._opened_at)
        is_best = progress.record_solve_time(self.state.language, self.exercise.id, elapsed)
        if self._best_seconds is None:
            time_note = f"Solved in {format_duration(elapsed)}"
        elif is_best:
            time_note = f"Solved in {format_duration(elapsed)} -- new personal best (was {format_duration(self._best_seconds)})"
        else:
            time_note = f"Solved in {format_duration(elapsed)} · best {format_duration(self._best_seconds)}"
        self.reward_review_text.value = (
            f"{time_note}\nNext review in {review.interval_days} day{'s' if review.interval_days != 1 else ''} "
            f"({review.due_date}) · review streak {review.review_streak}"
        )
        if earned_badges:
            self.reward_title.value = "Achievement unlocked!"
        elif is_best and self._best_seconds is not None:
            self.reward_title.value = "New personal best!"
        else:
            self.reward_title.value = "Still got it!" if self._was_completed else "Nice work!"
        self._best_seconds = elapsed if self._best_seconds is None else min(self._best_seconds, elapsed)
        self.reward_xp_text.value = "+0 XP"
        self.achievement_row.controls = [
            chip(b.replace("_", " ").title(), WHITE, self._fs, icon=ft.Icons.MILITARY_TECH_ROUNDED)
            for b in earned_badges
        ]

        completed_ids = set(progress.get_completed_lesson_ids(self.state.language))
        if self.state.lesson_return_route == "/daily":
            # Inside a Daily Refresher run, "next" means the next incomplete
            # item in TODAY's fixed set, not the next category level --
            # there may not even be a next level in this exercise's category.
            next_exercise = next(
                (ex for ex in self.state.daily_refresher_exercises() if ex.id not in completed_ids),
                None,
            )
        elif self.state.lesson_return_route == "/review":
            # Inside the Review Queue, "next" is the next due review (this
            # one was just rescheduled, so it no longer appears in the list).
            next_exercise = next((ex for ex in self.state.due_review_exercises() if ex.id != self.exercise.id), None)
        else:
            next_exercise = self.state.exercise_engine().next_unlocked_in_category(
                self.exercise.category, completed_ids,
            )
        self._next_exercise_id = next_exercise.id if next_exercise else None
        self.next_button.visible = next_exercise is not None

        self.reward_card.visible = True
        self.page.update()
        pop_in(self.page, self.reward_card)
        confetti(self.page, self.confetti, self.theme)
        self.page.run_task(count_up, self.reward_xp_text, self.exercise.xp_reward, fmt="+{n} XP", duration=0.9)
        self.page.run_task(self._content_column.scroll_to, offset=-1, duration=500)

    def _on_next(self, e) -> None:
        if self._next_exercise_id:
            self.page.go(f"/lesson/{self._next_exercise_id}")

    def _on_menu(self, e) -> None:
        if self._run_handle is not None:
            self._run_handle.cancel()
        if self._pulser:
            self._pulser.stop()
        self.page.go(self.state.lesson_return_route)


def _extension(language: str) -> str:
    return {"python": "py", "ai": "py", "java": "java", "spring": "java", "cpp": "cpp", "node": "js"}.get(language, "txt")
