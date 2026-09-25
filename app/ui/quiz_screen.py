"""Quiz Bank: pick a question count, answer a randomized multiple-choice
run (questions cross-fade), end with an animated score ring, related-
practice suggestions and -- for a perfect run -- confetti."""
from __future__ import annotations

import flet as ft

from app.engine.quiz import QuizQuestion
from app.progress.achievements import evaluate_quiz_achievements
from app.ui.app_state import AppState
from app.ui.components import (
    WHITE,
    MultipleChoiceCard,
    button,
    card,
    chip,
    header_row,
    icon_circle,
    progress_ring,
    spacer,
    tint,
    view_padding,
)
from app.ui.motion import Stagger, confetti, confetti_layer, pop_in, prepare_pop
from app.ui.shortcuts import Shortcuts
from app.ui.theme import scaled

_COUNT_CHOICES = [5, 10, 15, 20, 25, 50]


def build_quiz_view(page: ft.Page, state: AppState) -> ft.View:
    return _QuizController(page, state).build_view()


class _QuizController:
    def __init__(self, page: ft.Page, state: AppState) -> None:
        self.page = page
        self.state = state
        self.theme = state.theme
        self.scale = state.font_scale
        self.missed_tags: set[str] = set()

    def _fs(self, base: int) -> int:
        return scaled(base, self.scale)

    def build_view(self) -> ft.View:
        theme = self.theme
        stagger = Stagger(self.page)
        available = len(self.state.quiz_engine())
        best = self.state.progress.get_best_quiz_score(self.state.language)
        header = header_row(
            theme, self._fs, "Quiz Bank", self._on_menu, back_label="← Hub", icon=ft.Icons.QUIZ_ROUNDED,
            subtitle=f"{available} questions · best score {best[0]}/{best[1]}" if best else f"{available} questions",
        )

        self.setup_card = self._build_setup_card()

        self.check = MultipleChoiceCard(
            self.page, theme, self._fs, "Question",
            on_answer=self._on_answer, on_complete=self._on_complete,
            final_label="See results", show_score=True, accent=theme.accent,
        )
        self.check.visible = False

        self.results_ring_holder = ft.Container()
        self.results_text = ft.Text("", size=self._fs(22), weight=ft.FontWeight.BOLD, color=WHITE)
        self.results_sub = ft.Text("", size=self._fs(13), color=tint(WHITE, 0.88))
        self.meta_achievement_row = ft.Row([], spacing=8, wrap=True)
        self.practice_heading = ft.Text("Practice these next:", size=self._fs(13), weight=ft.FontWeight.BOLD,
                                        color=WHITE, visible=False)
        self.practice_row = ft.Row([], spacing=8, wrap=True)
        self.retry_missed_button = button("Retry missed concepts", self._on_retry_missed, theme, "warning",
                                          icon=ft.Icons.REPLAY_ROUNDED, height=46, visible=False)
        self.results_card = ft.Container(
            content=ft.Row(
                [
                    self.results_ring_holder,
                    ft.Column(
                        [
                            self.results_text, self.results_sub, self.meta_achievement_row,
                            self.practice_heading, self.practice_row,
                            ft.Row(
                                [
                                    self.retry_missed_button,
                                    button("Play again", self._on_play_again, theme, "success", icon=ft.Icons.REFRESH_ROUNDED,
                                           height=46, bgcolor=tint(WHITE, 0.22)),
                                    button("Back to hub", self._on_menu, theme, "ghost", icon=ft.Icons.ARROW_BACK_ROUNDED,
                                           height=46),
                                ],
                                spacing=10, wrap=True,
                            ),
                        ],
                        spacing=10, expand=True,
                    ),
                ],
                spacing=22, vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            gradient=ft.LinearGradient(begin=ft.Alignment.TOP_LEFT, end=ft.Alignment.BOTTOM_RIGHT,
                                       colors=[theme.gradient[0], theme.gradient[1]]),
            border_radius=22, padding=24, visible=False,
        )
        prepare_pop(self.results_card)
        self.confetti = confetti_layer()

        keys_help = ft.Text(
            Shortcuts().describe(("1-4", "answer"), ("enter", "next"), ("escape", "back")),
            size=self._fs(11), color=theme.text_muted,
        )
        content = ft.Column(
            [header, spacer(8), stagger.wrap(self.setup_card), self.check.control, self.results_card, keys_help],
            scroll=ft.ScrollMode.AUTO, spacing=14, expand=True,
        )
        stagger.play()

        # No text field on this screen, so plain digits are safe to bind.
        shortcuts = Shortcuts().bind("escape", lambda: self._on_menu(None))
        for i in range(1, 9):
            shortcuts.bind(str(i), lambda i=i: self.check.select_option(i - 1))
        shortcuts.bind(["enter", "space", "right"], self.check.advance)
        shortcuts.install(self.page)
        return ft.View(
            route="/quiz", bgcolor=theme.bg, padding=0,
            controls=[ft.Stack(
                [ft.Container(content=content, padding=view_padding(self.page), left=0, top=0, right=0, bottom=0), self.confetti],
                expand=True,
            )],
        )

    def _build_setup_card(self) -> ft.Control:
        theme = self.theme
        available = len(self.state.quiz_engine())
        buttons = [
            button(f"{n} questions", lambda _e, n=n: self._on_pick_count(n), theme, "primary", height=46,
                   icon=ft.Icons.PLAY_ARROW_ROUNDED)
            for n in _COUNT_CHOICES if n <= available
        ]
        return card(theme, self._fs, "How long do you have?", [
            ft.Row(
                [
                    icon_circle(ft.Icons.TIMER_ROUNDED, theme.accent, size=48, icon_size=self._fs(24)),
                    ft.Text(
                        "Every run is a fresh random draw with shuffled options, so no two rounds look the same. "
                        "Each correct answer is worth 5 XP.",
                        size=self._fs(13), color=theme.text_muted, expand=True,
                    ),
                ],
                spacing=14, vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Row(buttons, wrap=True, spacing=10),
        ], icon=ft.Icons.QUIZ_ROUNDED, accent=theme.accent)

    def _begin(self, questions: list[QuizQuestion]) -> None:
        self.missed_tags = set()
        self.setup_card.visible = False
        self.results_card.visible = False
        prepare_pop(self.results_card)
        self.check.start(questions)
        self.page.update()

    def _on_pick_count(self, count: int) -> None:
        self._begin(self.state.quiz_engine().start_session(count))

    def _on_answer(self, question: QuizQuestion, is_correct: bool) -> None:
        if not is_correct:
            self.missed_tags.update(question.concept_tags)
        self.state.progress.record_quiz_answer(self.state.language, question.id, question.concept_tags, is_correct)

    def _on_complete(self, score: int, total: int) -> None:
        theme = self.theme
        self.state.progress.record_quiz_attempt(self.state.language, score, total)
        self.state.progress.record_play_today(self.state.language)
        percent = round(100 * score / total) if total else 0

        if percent == 100:
            headline = "Perfect round!"
        elif percent >= 80:
            headline = "Sharp. Very sharp."
        elif percent >= 50:
            headline = "Solid -- a few gaps to close."
        else:
            headline = "Good warm-up. Let's fix those gaps."
        self.results_text.value = headline
        self.results_sub.value = f"You scored {score} of {total} · +{score * 5} XP"
        self.results_ring_holder.content = progress_ring(
            theme, self._fs, percent / 100, WHITE, size=96, label=f"{percent}%", sublabel="correct", stroke=9,
        )

        earned_badges = evaluate_quiz_achievements(self.state.progress, self.state.language, score, total)
        self.meta_achievement_row.controls = [
            chip(b.replace("_", " ").title(), WHITE, self._fs, icon=ft.Icons.MILITARY_TECH_ROUNDED) for b in earned_badges
        ]

        completed_ids = set(self.state.progress.get_completed_lesson_ids(self.state.language))
        suggestions = self.state.exercise_engine().recommend_practice_for_tags(self.missed_tags, completed_ids)
        self.practice_heading.visible = bool(suggestions)
        self.practice_row.controls = [
            button(ex.title, lambda _e, eid=ex.id: self.page.go(f"/lesson/{eid}"), theme, "ghost", height=36,
                   icon=ft.Icons.SCHOOL_ROUNDED)
            for ex in suggestions
        ]
        self.retry_missed_button.visible = bool(self.missed_tags)

        self.check.visible = False
        self.results_card.visible = True
        self.page.update()
        pop_in(self.page, self.results_card)
        if total and score == total:
            confetti(self.page, self.confetti, theme)

    def _on_retry_missed(self, e) -> None:
        # Re-quiz on every question tagged with something just missed, not
        # just the exact questions themselves -- concept_tags already
        # groups related questions, so this pool is usually bigger than
        # "the ones you got wrong."
        self._begin(self.state.quiz_engine().start_session_for_tags(self.missed_tags))

    def _on_play_again(self, e) -> None:
        self.results_card.visible = False
        self.setup_card.visible = True
        self.page.update()

    def _on_menu(self, e) -> None:
        self.page.go("/hub")
