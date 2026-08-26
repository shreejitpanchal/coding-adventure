"""Quiz Bank: pick a question count, answer a randomized multiple-choice
run, end with a score summary and related-practice suggestions."""
from __future__ import annotations

import flet as ft

from app.ui.app_state import AppState
from app.ui.theme import scaled

_OPTION_COUNT = 4
_COUNT_CHOICES = [5, 10, 15, 20, 25, 50]


def build_quiz_view(page: ft.Page, state: AppState) -> ft.View:
    return _QuizController(page, state).build_view()


class _QuizController:
    def __init__(self, page: ft.Page, state: AppState) -> None:
        self.page = page
        self.state = state
        self.theme = state.theme
        self.scale = state.font_scale

        self.questions: list = []
        self.total = 0
        self.index = 0
        self.score = 0
        self.answered = False
        self.missed_tags: set[str] = set()

    def _fs(self, base: int) -> int:
        return scaled(base, self.scale)

    def build_view(self) -> ft.View:
        theme = self.theme
        header = ft.Row(
            [
                ft.Button(
                    "← Hub", on_click=self._on_menu, height=44,
                    style=ft.ButtonStyle(bgcolor=theme.text_muted, color="#FFFFFF"),
                ),
                ft.Text("Quiz Bank", size=self._fs(24), weight=ft.FontWeight.BOLD, color=theme.primary, expand=True),
            ],
            spacing=12,
        )

        self.setup_card = self._build_setup_card()

        self.progress_text = ft.Text("", size=self._fs(13), color=theme.text_muted)
        self.question_text = ft.Text("", size=self._fs(17), weight=ft.FontWeight.BOLD, color=theme.text)
        self.option_labels: list[ft.Text] = []
        self.option_buttons = [self._make_option_button(i) for i in range(_OPTION_COUNT)]
        self.feedback_text = ft.Text("", size=self._fs(13))
        self.next_label = ft.Text("Next →", size=self._fs(15), color="#FFFFFF")
        self.next_button = ft.Button(
            content=self.next_label, on_click=self._on_next, visible=False, height=44,
            style=ft.ButtonStyle(bgcolor=theme.primary),
        )

        self.question_card = self._card("Question", [
            self.progress_text, self.question_text, ft.Column(self.option_buttons, spacing=8),
            self.feedback_text, self.next_button,
        ])
        self.question_card.visible = False

        self.results_text = ft.Text("", size=self._fs(20), weight=ft.FontWeight.BOLD, color=theme.text)
        self.practice_heading = ft.Text("Practice these next:", size=self._fs(14), weight=ft.FontWeight.BOLD, color=theme.text, visible=False)
        self.practice_row = ft.Row([], spacing=8, wrap=True)
        self.results_card = ft.Container(
            content=ft.Column(
                [
                    self.results_text, self.practice_heading, self.practice_row,
                    ft.Row(
                        [
                            ft.Button(
                                "Play again", on_click=self._on_play_again, height=48,
                                style=ft.ButtonStyle(bgcolor=theme.success, color="#FFFFFF"),
                            ),
                            ft.Button(
                                "Back to hub", on_click=self._on_menu, height=48,
                                style=ft.ButtonStyle(bgcolor=theme.text_muted, color="#FFFFFF"),
                            ),
                        ],
                        spacing=10,
                    ),
                ],
                spacing=12,
            ),
            bgcolor=theme.card, border=ft.border.Border.all(2, theme.primary), border_radius=16, padding=20, visible=False,
        )

        return ft.View(
            route="/quiz",
            bgcolor=theme.bg,
            scroll=ft.ScrollMode.AUTO,
            padding=ft.padding.Padding.only(left=24, top=24, right=24, bottom=40),
            controls=[header, self.setup_card, self.question_card, self.results_card],
        )

    def _build_setup_card(self) -> ft.Control:
        available = len(self.state.quiz_engine())
        buttons = [
            ft.Button(
                f"{n}", on_click=lambda _e, n=n: self._on_pick_count(n), width=80, height=48,
                style=ft.ButtonStyle(bgcolor=self.theme.primary, color="#FFFFFF"),
            )
            for n in _COUNT_CHOICES if n <= available
        ]
        return self._card("How many questions?", [
            ft.Text(f"{available} available.", size=self._fs(13), color=self.theme.text_muted),
            ft.Row(buttons, wrap=True, spacing=10),
        ])

    def _card(self, title: str, children: list[ft.Control]) -> ft.Control:
        return ft.Container(
            content=ft.Column(
                [ft.Text(title, size=self._fs(16), weight=ft.FontWeight.BOLD, color=self.theme.text), *children],
                spacing=10,
            ),
            bgcolor=self.theme.card, border_radius=16, padding=20,
        )

    def _make_option_button(self, index: int) -> ft.Button:
        label = ft.Text("", size=self._fs(14))
        self.option_labels.append(label)
        return ft.Button(
            content=label, on_click=lambda _e, i=index: self._on_select(i), height=52, width=560,
            style=ft.ButtonStyle(bgcolor=self.theme.bg),
        )

    def _on_pick_count(self, count: int) -> None:
        self.questions = self.state.quiz_engine().start_session(count)
        self.total = len(self.questions)
        self.index = 0
        self.score = 0
        self.missed_tags = set()
        self.setup_card.visible = False
        self.question_card.visible = True
        self._render_question()

    def _render_question(self) -> None:
        theme = self.theme
        question = self.questions[self.index]
        self.progress_text.value = f"Question {self.index + 1} of {self.total} · Score: {self.score}"
        self.question_text.value = question.question
        for i, button in enumerate(self.option_buttons):
            self.option_labels[i].value = question.options[i]
            self.option_labels[i].color = theme.text
            button.disabled = False
            button.style = ft.ButtonStyle(bgcolor=theme.bg)
        self.feedback_text.value = ""
        self.next_button.visible = False
        self.answered = False
        self.page.update()

    def _on_select(self, index: int) -> None:
        if self.answered:
            return
        self.answered = True
        theme = self.theme
        question = self.questions[self.index]
        correct = index == question.correct
        if correct:
            self.score += 1
        else:
            self.missed_tags.update(question.concept_tags)

        for i, button in enumerate(self.option_buttons):
            button.disabled = True
            if i == question.correct:
                button.style = ft.ButtonStyle(bgcolor=theme.success)
                self.option_labels[i].color = "#FFFFFF"
            elif i == index:
                button.style = ft.ButtonStyle(bgcolor=theme.danger)
                self.option_labels[i].color = "#FFFFFF"

        self.feedback_text.value = ("Correct. " if correct else "Not quite. ") + question.explanation
        self.feedback_text.color = theme.success if correct else theme.danger
        self.next_label.value = "Next →" if self.index + 1 < self.total else "See results"
        self.next_button.visible = True
        self.progress_text.value = f"Question {self.index + 1} of {self.total} · Score: {self.score}"
        self.page.update()

    def _on_next(self, e) -> None:
        self.index += 1
        if self.index >= self.total:
            self._show_results()
        else:
            self._render_question()

    def _show_results(self) -> None:
        self.state.progress.record_quiz_attempt(self.state.language, self.score, self.total)
        self.state.progress.record_play_today(self.state.language)
        percent = round(100 * self.score / self.total)
        self.results_text.value = f"You scored {self.score} / {self.total} ({percent}%)"

        completed_ids = set(self.state.progress.get_completed_lesson_ids(self.state.language))
        suggestions = self.state.exercise_engine().recommend_practice_for_tags(self.missed_tags, completed_ids)
        self.practice_heading.visible = bool(suggestions)
        self.practice_row.controls = [
            ft.Button(
                ex.title, height=36,
                on_click=lambda _e, eid=ex.id: self.page.go(f"/lesson/{eid}"),
                style=ft.ButtonStyle(bgcolor=self.theme.warning, color="#FFFFFF"),
            )
            for ex in suggestions
        ]

        self.question_card.visible = False
        self.results_card.visible = True
        self.page.update()

    def _on_play_again(self, e) -> None:
        self.results_card.visible = False
        self.setup_card.visible = True
        self.page.update()

    def _on_menu(self, e) -> None:
        self.page.go("/hub")
