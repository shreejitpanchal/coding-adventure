import pytest

from app.engine.lesson_engine import ExerciseEngine
from app.progress.store import ProgressStore
from app.ui.app_state import resolve_daily_refresher


@pytest.fixture
def progress(tmp_path):
    s = ProgressStore(tmp_path / "progress.sqlite3")
    yield s
    s.close()


@pytest.fixture
def engine():
    return ExerciseEngine("python")


def test_daily_refresher_is_stable_across_calls_same_day(engine, progress):
    first = resolve_daily_refresher(engine, progress, "python", "2026-01-01")
    second = resolve_daily_refresher(engine, progress, "python", "2026-01-01")
    assert [ex.id for ex in first] == [ex.id for ex in second]


def test_daily_refresher_stays_fixed_after_completing_one(engine, progress):
    first = resolve_daily_refresher(engine, progress, "python", "2026-01-01")
    progress.complete_lesson("python", first[0].id, xp_reward=10)

    again = resolve_daily_refresher(engine, progress, "python", "2026-01-01")
    assert [ex.id for ex in again] == [ex.id for ex in first]
    completed_ids = set(progress.get_completed_lesson_ids("python"))
    done = sum(1 for ex in again if ex.id in completed_ids)
    assert done == 1


def test_daily_refresher_generates_a_new_set_the_next_day(engine, progress):
    day1 = resolve_daily_refresher(engine, progress, "python", "2026-01-01")
    for ex in day1:
        progress.complete_lesson("python", ex.id, xp_reward=10)

    day2 = resolve_daily_refresher(engine, progress, "python", "2026-01-02")
    assert day2
    assert {ex.id for ex in day2}.isdisjoint({ex.id for ex in day1})
