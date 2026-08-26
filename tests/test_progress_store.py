import pytest

from app.progress.store import ProgressStore


@pytest.fixture
def store(tmp_path):
    s = ProgressStore(tmp_path / "progress.sqlite3")
    yield s
    s.close()


def test_complete_lesson_awards_xp_once(store):
    store.complete_lesson("python", "ex1", xp_reward=10)
    assert store.get_player_level("python").total_xp == 10
    store.complete_lesson("python", "ex1", xp_reward=10)
    assert store.get_player_level("python").total_xp == 10  # no double-award


def test_languages_track_independently(store):
    store.complete_lesson("python", "ex1", xp_reward=10)
    store.complete_lesson("java", "ex1", xp_reward=20)
    assert store.get_player_level("python").total_xp == 10
    assert store.get_player_level("java").total_xp == 20


def test_award_badge_only_once(store):
    assert store.award_badge("python", "first_badge") is True
    assert store.award_badge("python", "first_badge") is False


def test_recent_failure_count_resets_on_completion(store):
    store.log_event("python", "ex1", "attempt_error")
    store.log_event("python", "ex1", "attempt_error")
    assert store.get_recent_failure_count("python", "ex1") == 2
    store.complete_lesson("python", "ex1", xp_reward=5)
    assert store.get_recent_failure_count("python", "ex1") == 0


def test_streak_increments_on_consecutive_days(store):
    store.record_play_today("python")
    assert store.get_streak_days("python") == 1
    store.record_play_today("python")  # same day, no-op
    assert store.get_streak_days("python") == 1


def test_daily_refresher_picks_persist_for_the_day(store):
    assert store.get_daily_refresher_picks("python", "2026-01-01") == []
    store.save_daily_refresher_picks("python", "2026-01-01", ["ex1", "ex2", "ex3"])
    assert store.get_daily_refresher_picks("python", "2026-01-01") == ["ex1", "ex2", "ex3"]
    # A different day gets its own independent set.
    assert store.get_daily_refresher_picks("python", "2026-01-02") == []


def test_daily_refresher_picks_cleared_on_reset(store):
    store.save_daily_refresher_picks("python", "2026-01-01", ["ex1"])
    store.reset_progress("python")
    assert store.get_daily_refresher_picks("python", "2026-01-01") == []
