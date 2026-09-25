import pytest

from app.engine.lesson_engine import ExerciseEngine
from app.progress.achievements import (
    evaluate_lesson_completion_achievements,
    evaluate_quiz_achievements,
)
from app.progress.store import ProgressStore


@pytest.fixture
def progress(tmp_path):
    s = ProgressStore(tmp_path / "progress.sqlite3")
    yield s
    s.close()


@pytest.fixture
def engine():
    return ExerciseEngine("python")


def test_first_completion_badge_awarded_once(progress, engine):
    progress.complete_lesson("python", "idioms_gotchas_01", xp_reward=10)
    awarded = evaluate_lesson_completion_achievements(progress, engine, "python", "idioms_gotchas")
    assert "first_completion" in awarded

    progress.complete_lesson("python", "idioms_gotchas_02", xp_reward=10)
    awarded_again = evaluate_lesson_completion_achievements(progress, engine, "python", "idioms_gotchas")
    assert "first_completion" not in awarded_again


def test_category_complete_badge_awarded_when_every_level_done(progress, engine):
    # "recursion" is one of the smaller (15-exercise) categories.
    items = engine.lessons_in_category("recursion")
    for ex in items[:-1]:
        progress.complete_lesson("python", ex.id, xp_reward=10)
    mid_awards = evaluate_lesson_completion_achievements(progress, engine, "python", "recursion")
    assert "category_complete_recursion" not in mid_awards

    progress.complete_lesson("python", items[-1].id, xp_reward=10)
    final_awards = evaluate_lesson_completion_achievements(progress, engine, "python", "recursion")
    assert "category_complete_recursion" in final_awards

    # Idempotent: re-evaluating after it's already been awarded doesn't re-award it.
    repeat_awards = evaluate_lesson_completion_achievements(progress, engine, "python", "recursion")
    assert "category_complete_recursion" not in repeat_awards


def test_streak_milestone_badge(progress, engine):
    progress.record_play_today("python")  # ensures the profile row exists
    with progress._conn:
        progress._conn.execute("UPDATE profile SET streak_days = 3 WHERE language = ?", ("python",))

    progress.complete_lesson("python", "idioms_gotchas_01", xp_reward=10)
    awarded = evaluate_lesson_completion_achievements(progress, engine, "python", "idioms_gotchas")
    assert "streak_3" in awarded


def test_streak_not_at_a_milestone_awards_nothing(progress, engine):
    progress.record_play_today("python")
    with progress._conn:
        progress._conn.execute("UPDATE profile SET streak_days = 4 WHERE language = ?", ("python",))

    progress.complete_lesson("python", "idioms_gotchas_01", xp_reward=10)
    awarded = evaluate_lesson_completion_achievements(progress, engine, "python", "idioms_gotchas")
    assert not any(b.startswith("streak_") for b in awarded)


def test_perfect_quiz_badge(progress):
    awarded = evaluate_quiz_achievements(progress, "python", 5, 5)
    assert "perfect_quiz" in awarded

    not_perfect = evaluate_quiz_achievements(progress, "python", 4, 5)
    assert "perfect_quiz" not in not_perfect
