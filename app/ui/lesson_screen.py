"""The Explain -> Example -> Try It -> Run -> Result flow for a single
exercise -- or, for a purely conceptual exercise (Exercise.requires_code
is False, e.g. the `architecture` track), Explain -> Example ->
Comprehension Check instead, with no code editor, Run button, or
execution engine involved at all."""
from __future__ import annotations

import asyncio
from typing import Optional

import flet as ft

from app.engine.categories import get_category_meta
from app.engine.exercise import Exercise
from app.engine.validator import validate_contains, validate_output
from app.execution.base import ExecutionResult, RunHandle
from app.execution.errors import extract_error_line_number, translate_error
from app.execution.registry import get_engine
from app.execution.toolchain_check import check_toolchain
from app.ui.app_state import AppState
from app.ui.code_editor import make_code_editor, make_read_only_code_block
from app.ui.theme import scaled


def build_lesson_view(page: ft.Page, state: AppState, exercise_id: str) -> ft.View:
    theme = state.theme
    exercise = state.exercise_engine().get(exercise_id)

    if exercise is None:
        return ft.View(
            route=f"/lesson/{exercise_id}",
            bgcolor=theme.bg,
            controls=[ft.Text(f"Couldn't find exercise '{exercise_id}'.", color=theme.danger)],
        )

    return _ExerciseController(page, state, exercise).build_view()


class _ExerciseController:
    def __init__(self, page: ft.Page, state: AppState, exercise: Exercise) -> None:
        self.page = page
        self.state = state
        self.exercise = exercise
        self.theme = state.theme
        self.scale = state.font_scale
        self.engine = get_engine(exercise.language) if exercise.requires_code else None

        self._running = False
        self._run_handle: Optional[RunHandle] = None
        self._hint_index = 0
        self._passed = False
        self._next_exercise_id: Optional[str] = None
        self._current_input_value: Optional[str] = None
        self.input_field: Optional[ft.TextField] = None
        self._check_index = 0
        self._check_wrong_count = 0

    def _fs(self, base: int) -> int:
        return scaled(base, self.scale)

    def build_view(self) -> ft.View:
        theme = self.theme
        exercise = self.exercise
        meta = get_category_meta(exercise.category)

        header = ft.Row(
            [
                ft.Button(
                    "← Back", on_click=self._on_menu, height=44,
                    style=ft.ButtonStyle(bgcolor=theme.text_muted, color="#FFFFFF"),
                ),
                ft.Text(exercise.title, size=self._fs(22), weight=ft.FontWeight.BOLD, color=theme.primary, expand=True),
                ft.Container(
                    content=ft.Text(exercise.difficulty.replace("_", " ").title(), size=self._fs(12), color="#FFFFFF"),
                    bgcolor=meta.color, border_radius=8, padding=ft.padding.Padding.symmetric(horizontal=10, vertical=4),
                ),
            ],
            spacing=12,
        )

        explanation_card = self._card("Objective", [
            ft.Text(exercise.objective.strip(), size=self._fs(15), weight=ft.FontWeight.BOLD, color=theme.text),
            ft.Text(exercise.explanation.strip(), size=self._fs(14), color=theme.text_muted),
        ])

        controls = [header, explanation_card]

        if exercise.example_code.strip():
            controls.append(self._card("Example", [
                make_read_only_code_block(exercise.example_code.strip(), scale=self.scale, theme=theme),
            ]))

        self._build_reward_card()

        if exercise.requires_code:
            if exercise.challenge.strip():
                controls.append(self._card("Your Task", [
                    ft.Text(exercise.challenge.strip(), size=self._fs(14), color=theme.text),
                ]))
            controls.append(self._build_code_card())
            controls.append(self._build_output_card())
        else:
            if exercise.challenge.strip():
                controls.append(self._card("Think About It", [
                    ft.Text(exercise.challenge.strip(), size=self._fs(14), color=theme.text),
                ]))
            controls.append(self._build_comprehension_card())

        controls.append(self.reward_card)

        self._content_column = ft.Column(controls, scroll=ft.ScrollMode.AUTO, spacing=10, expand=True)
        content = ft.Container(content=self._content_column, padding=24, expand=True)

        self.page.on_keyboard_event = self._on_keyboard
        return ft.View(route=f"/lesson/{exercise.id}", bgcolor=theme.bg, padding=0, controls=[content])

    def _card(self, title: str, children: list[ft.Control]) -> ft.Control:
        return ft.Container(
            content=ft.Column(
                [ft.Text(title, size=self._fs(17), weight=ft.FontWeight.BOLD, color=self.theme.text), *children],
                spacing=10,
            ),
            bgcolor=self.theme.card, border_radius=16, padding=20,
        )

    def _build_code_card(self) -> ft.Control:
        theme = self.theme
        exercise = self.exercise

        # Scale the editor to the starter code's actual length instead of a
        # fixed 260px -- a short snippet no longer sits in a mostly-empty
        # box, and a long one gets room before scrolling kicks in.
        starter_lines = exercise.starter_code.strip().count("\n") + 1
        editor_height = max(180, min(520, 32 * starter_lines + 60))
        self.editor = make_code_editor(
            exercise.starter_code.strip(), height=editor_height, scale=self.scale, theme=theme,
        )
        children: list[ft.Control] = [self.editor]

        if exercise.input_prompt:
            self.input_field = ft.TextField(hint_text="Type input...", width=260)
            children.append(
                ft.Column(
                    [ft.Text(exercise.input_prompt, size=self._fs(14), color=theme.text), self.input_field],
                    spacing=6,
                )
            )

        # Browsing an exercise (reading the explanation/example, looking at
        # the challenge, editing code) never needs the language's real
        # toolchain -- only actually running code does. Checked here,
        # proactively, so the Run button is disabled up front on a machine
        # (or platform, e.g. Android) that can't run this language,
        # instead of only failing after the click via ExecutionResult.blocked.
        toolchain_ready = check_toolchain(exercise.language).available

        self.run_button = ft.Button(
            "▶ Run" if toolchain_ready else "▶ Run (unavailable here)",
            on_click=self._on_run, height=48, disabled=not toolchain_ready,
            tooltip=(
                "Ctrl+Enter also runs your code"
                if toolchain_ready else "This language's compiler/runtime isn't available on this device."
            ),
            style=ft.ButtonStyle(bgcolor=theme.success, color="#FFFFFF"),
        )
        reset_button = ft.Button(
            "↺ Reset", on_click=self._on_reset, height=44,
            style=ft.ButtonStyle(bgcolor=theme.text_muted, color="#FFFFFF"),
        )
        self.hint_button = ft.Button(
            "💡 Hint", on_click=self._on_hint, disabled=not exercise.hints, height=44,
            style=ft.ButtonStyle(bgcolor=theme.warning, color="#FFFFFF"),
        )
        children.append(ft.Row([self.run_button, reset_button, self.hint_button], spacing=10, wrap=True))

        if not toolchain_ready:
            children.append(ft.Text(
                "Running is unavailable here -- this language's compiler/runtime isn't installed "
                "(or isn't supported on this device). You can still read through and edit the exercise.",
                size=self._fs(12), color=theme.warning,
            ))

        self.hint_text = ft.Text("", size=self._fs(13), color=theme.warning)
        children.append(self.hint_text)

        return self._card("Your Code", children)

    def _build_comprehension_card(self) -> ft.Control:
        """A short inline multiple-choice check that gates completion for a
        requires_code=False exercise -- same shape as a QuizQuestion, but
        embedded in the lesson flow instead of a standalone quiz session.
        Answering every question correctly in one pass calls _on_success();
        any wrong answer requires retrying the whole check from the start."""
        theme = self.theme

        self.check_progress_text = ft.Text("", size=self._fs(13), color=theme.text_muted)
        self.check_question_text = ft.Text("", size=self._fs(15), weight=ft.FontWeight.BOLD, color=theme.text)
        self.check_option_labels: list[ft.Text] = []
        self.check_option_buttons = [self._make_check_option_button(i) for i in range(4)]
        self.check_feedback_text = ft.Text("", size=self._fs(13))
        self.check_next_label = ft.Text("Next →", size=self._fs(14), color="#FFFFFF")
        self.check_next_button = ft.Button(
            content=self.check_next_label, on_click=self._on_check_next, visible=False, height=44,
            style=ft.ButtonStyle(bgcolor=theme.primary),
        )
        self.check_retry_button = ft.Button(
            "↺ Try Again", on_click=self._on_check_retry, visible=False, height=44,
            style=ft.ButtonStyle(bgcolor=theme.warning, color="#FFFFFF"),
        )

        self._render_check_question()

        return self._card("Comprehension Check", [
            self.check_progress_text,
            self.check_question_text,
            ft.Column(self.check_option_buttons, spacing=8),
            self.check_feedback_text,
            ft.Row([self.check_next_button, self.check_retry_button], spacing=10, wrap=True),
        ])

    def _make_check_option_button(self, index: int) -> ft.Button:
        label = ft.Text("", size=self._fs(14))
        self.check_option_labels.append(label)
        return ft.Button(
            content=label, on_click=lambda _e, i=index: self._on_check_select(i), height=48, width=560,
            style=ft.ButtonStyle(bgcolor=self.theme.bg),
        )

    def _render_check_question(self) -> None:
        theme = self.theme
        questions = self.exercise.comprehension_check
        q = questions[self._check_index]
        self.check_progress_text.value = f"Question {self._check_index + 1} of {len(questions)}"
        self.check_question_text.value = q["question"]
        for i, button in enumerate(self.check_option_buttons):
            button.visible = True
            self.check_option_labels[i].value = q["options"][i]
            self.check_option_labels[i].color = theme.text
            button.disabled = False
            button.style = ft.ButtonStyle(bgcolor=theme.bg)
        self.check_feedback_text.value = ""
        self.check_next_button.visible = False
        self.check_retry_button.visible = False

    def _on_check_select(self, index: int) -> None:
        theme = self.theme
        q = self.exercise.comprehension_check[self._check_index]
        correct_index = q["correct"]
        is_correct = index == correct_index
        if not is_correct:
            self._check_wrong_count += 1

        for i, button in enumerate(self.check_option_buttons):
            button.disabled = True
            if i == correct_index:
                button.style = ft.ButtonStyle(bgcolor=theme.success)
                self.check_option_labels[i].color = "#FFFFFF"
            elif i == index:
                button.style = ft.ButtonStyle(bgcolor=theme.danger)
                self.check_option_labels[i].color = "#FFFFFF"

        self.check_feedback_text.value = ("Correct. " if is_correct else "Not quite. ") + q.get("explanation", "")
        self.check_feedback_text.color = theme.success if is_correct else theme.danger
        is_last = self._check_index + 1 >= len(self.exercise.comprehension_check)
        self.check_next_label.value = "Finish" if is_last else "Next →"
        self.check_next_button.visible = True
        self.page.update()

    def _on_check_next(self, e) -> None:
        self._check_index += 1
        if self._check_index >= len(self.exercise.comprehension_check):
            if self._check_wrong_count == 0:
                self._on_success()
            else:
                self.check_progress_text.value = f"You missed {self._check_wrong_count} question(s) this time."
                self.check_question_text.value = ""
                for button in self.check_option_buttons:
                    button.visible = False
                self.check_feedback_text.value = "Review the explanations above, then try again."
                self.check_feedback_text.color = self.theme.warning
                self.check_next_button.visible = False
                self.check_retry_button.visible = True
                self.page.update()
        else:
            self._render_check_question()
            self.page.update()

    def _on_check_retry(self, e) -> None:
        self._check_index = 0
        self._check_wrong_count = 0
        self._render_check_question()
        self.page.update()

    def _build_output_card(self) -> ft.Control:
        theme = self.theme
        self.output_text = ft.Text("Press Run to see what happens.", size=self._fs(14), color=theme.text_muted)
        self.details_button = ft.TextButton(
            "Show raw output", on_click=self._toggle_details, visible=False,
            style=ft.ButtonStyle(color=theme.text_muted),
        )
        self.details_text = ft.Text("", size=self._fs(12), font_family="Consolas", color=theme.text, selectable=True)
        self.details_container = ft.Container(
            content=self.details_text, bgcolor=theme.card, border_radius=8, padding=12, visible=False,
        )
        self.practice_row = ft.Row([], spacing=8, wrap=True)
        self.practice_container = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Related practice:", size=self._fs(13), weight=ft.FontWeight.BOLD, color=theme.text),
                    self.practice_row,
                ],
                spacing=8,
            ),
            bgcolor=theme.card, border=ft.border.Border.all(1, theme.warning), border_radius=8, padding=12,
            visible=False,
        )
        return self._card("Output", [self.output_text, self.details_button, self.details_container, self.practice_container])

    def _build_reward_card(self) -> None:
        theme = self.theme
        self.reward_text = ft.Text("", size=self._fs(18), weight=ft.FontWeight.BOLD, color=theme.success)
        self.achievement_text = ft.Text("", size=self._fs(14), color=theme.text)
        self.next_button = ft.Button(
            "Next exercise →", on_click=self._on_next, height=48, visible=False,
            style=ft.ButtonStyle(bgcolor=theme.success, color="#FFFFFF"),
        )
        hub_button = ft.Button(
            "Back", on_click=self._on_menu, height=48,
            style=ft.ButtonStyle(bgcolor=theme.text_muted, color="#FFFFFF"),
        )
        self.reward_card = ft.Container(
            content=ft.Column(
                [
                    self.reward_text, self.achievement_text,
                    ft.Row([self.next_button, hub_button], spacing=10, wrap=True),
                ],
                spacing=8,
            ),
            bgcolor=theme.card, border=ft.border.Border.all(2, theme.success), border_radius=16, padding=20,
            visible=False,
        )

    # -- run flow -----------------------------------------------------
    async def _on_keyboard(self, e: ft.KeyboardEvent) -> None:
        if not self.exercise.requires_code:
            return
        if e.ctrl and e.key == "Enter" and not self.run_button.disabled and not self._running:
            await self._on_run(e)

    async def _on_run(self, e) -> None:
        if self._running:
            return
        self._running = True
        self.run_button.disabled = True
        self._hide_details()
        self.output_text.value = "Running..."
        self.output_text.color = self.theme.text_muted
        self.page.update()

        code = self.editor.value or ""
        handle = RunHandle()
        self._run_handle = handle

        input_value = self.input_field.value if self.input_field is not None else None
        self._current_input_value = input_value
        stdin_text = f"{input_value}\n" if input_value is not None else None

        result = await asyncio.to_thread(self.engine.run, code, 8.0, handle, stdin_text, self.exercise)
        self._on_run_complete(result)

    def _on_run_complete(self, result: ExecutionResult) -> None:
        self._running = False
        self.run_button.disabled = False

        if result.blocked:
            self._show_output(result.blocked_message or "This toolchain isn't available.", self.theme.danger)
            self.page.update()
            return

        if result.timed_out:
            self._show_output("Timed out -- check for a loop that never terminates.", self.theme.danger)
            self.state.progress.log_event(self.state.language, self.exercise.id, "attempt_timeout")
            self._maybe_show_practice()
            self.page.update()
            return

        if not result.success:
            friendly, hint = translate_error(result.stderr, self.exercise.language)
            line = extract_error_line_number(result.stderr, self.exercise.language)
            if line:
                friendly = f"{friendly} (line {line})"
            self._show_output(f"{friendly}\n{hint}", self.theme.danger, raw=result.stderr)
            self.state.progress.log_event(self.state.language, self.exercise.id, "attempt_error", result.stderr[-200:])
            self._maybe_show_practice()
            self.page.update()
            return

        output_ok = validate_output(
            result.stdout, self.exercise.expected_output,
            input_value=self._current_input_value,
            expected_output_pattern=self.exercise.expected_output_pattern,
        )
        contains_ok = (
            validate_contains(self.editor.value or "", self.exercise.contains_patterns)
            if self.exercise.contains_patterns else True
        )

        if output_ok and contains_ok:
            self._show_output(result.stdout or "(no output)", self.theme.success)
            self._on_success()
        elif output_ok and not contains_ok:
            self._show_output(
                f"{result.stdout or '(no output)'}\n\nOutput matches, but try using what this exercise is "
                "actually teaching -- not just a direct answer.",
                self.theme.warning,
            )
        else:
            self._show_output(
                f"{result.stdout or '(no output)'}\n\nNot quite the expected output yet.",
                self.theme.warning,
            )
            self.state.progress.log_event(self.state.language, self.exercise.id, "attempt_wrong_output", result.stdout[-200:])
            self._maybe_show_practice()
        self.page.update()

    def _on_reset(self, e) -> None:
        self.editor.value = self.exercise.starter_code.strip()
        if self.input_field is not None:
            self.input_field.value = ""
        self._hide_details()
        self.practice_container.visible = False
        self.output_text.value = "Press Run to see what happens."
        self.output_text.color = self.theme.text_muted
        self.reward_card.visible = False
        self._passed = False
        self.page.update()

    def _on_hint(self, e) -> None:
        if not self.exercise.hints:
            return
        hint = self.exercise.hints[self._hint_index % len(self.exercise.hints)]
        self.hint_text.value = f"Hint: {hint}"
        self.state.progress.log_event(self.state.language, self.exercise.id, "hint_used", hint)
        self._hint_index += 1
        self.page.update()

    # -- output helpers -------------------------------------------------
    def _show_output(self, text: str, color: str, raw: Optional[str] = None) -> None:
        self.output_text.value = text
        self.output_text.color = color
        if raw:
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

    _PRACTICE_THRESHOLD = 3

    def _maybe_show_practice(self) -> None:
        failures = self.state.progress.get_recent_failure_count(self.state.language, self.exercise.id)
        if failures < self._PRACTICE_THRESHOLD:
            return
        completed_ids = set(self.state.progress.get_completed_lesson_ids(self.state.language))
        suggestions = self.state.exercise_engine().recommend_practice(self.exercise.id, completed_ids)
        if not suggestions:
            return
        self.practice_row.controls = [
            ft.Button(
                ex.title, height=36,
                on_click=lambda _e, eid=ex.id: self.page.go(f"/lesson/{eid}"),
                style=ft.ButtonStyle(bgcolor=self.theme.warning, color="#FFFFFF"),
            )
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
        badge_awarded = False
        if self.exercise.achievement:
            badge_awarded = progress.award_badge(self.state.language, self.exercise.achievement)
        progress.record_play_today(self.state.language)

        self.reward_text.value = f"Nice work! +{self.exercise.xp_reward} XP"
        self.achievement_text.value = (
            f"Achievement unlocked: {self.exercise.achievement.replace('_', ' ').title()}"
            if badge_awarded else ""
        )

        completed_ids = set(progress.get_completed_lesson_ids(self.state.language))
        if self.state.lesson_return_route == "/daily":
            # Inside a Daily Refresher run, "next" means the next incomplete
            # item in TODAY's fixed set, not the next category level --
            # there may not even be a next level in this exercise's category.
            next_exercise = next(
                (ex for ex in self.state.daily_refresher_exercises() if ex.id not in completed_ids),
                None,
            )
        else:
            next_exercise = self.state.exercise_engine().next_unlocked_in_category(
                self.exercise.category, completed_ids,
            )
        self._next_exercise_id = next_exercise.id if next_exercise else None
        self.next_button.visible = next_exercise is not None

        self.reward_card.visible = True
        self.page.update()
        self.page.run_task(self._content_column.scroll_to, offset=-1, duration=400)

    def _on_next(self, e) -> None:
        if self._next_exercise_id:
            self.page.go(f"/lesson/{self._next_exercise_id}")

    def _on_menu(self, e) -> None:
        if self._run_handle is not None:
            self._run_handle.cancel()
        self.page.on_keyboard_event = None
        self.page.go(self.state.lesson_return_route)
