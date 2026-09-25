from datetime import datetime, timedelta, timezone

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


def test_export_then_import_restores_everything(store, tmp_path):
    store.complete_lesson("python", "ex1", xp_reward=10)
    store.award_badge("python", "first_badge")
    store.record_quiz_attempt("java", 4, 5)
    store.save_daily_refresher_picks("node", "2026-01-01", ["a", "b"])
    store.record_play_today("python")
    store.record_quiz_answer("python", "q1", ["closures"], is_correct=True)
    store.save_note("python", "ex1", "a note worth keeping")
    store.set_bookmarked("python", "ex1", True)

    exported = store.export_progress()
    assert exported["version"] == 1
    assert "tables" in exported

    fresh = ProgressStore(tmp_path / "restored.sqlite3")
    try:
        fresh.import_progress(exported)
        assert fresh.get_player_level("python").total_xp == 10
        assert fresh.is_lesson_completed("python", "ex1")
        assert fresh.get_badges_with_dates("python")[0][0] == "first_badge"
        assert fresh.get_best_quiz_score("java") == (4, 5)
        assert fresh.get_daily_refresher_picks("node", "2026-01-01") == ["a", "b"]
        assert fresh.get_streak_days("python") == 1
        assert fresh.get_concept_accuracy("python")["closures"] == (1, 1)
        assert fresh.get_note("python", "ex1") == "a note worth keeping"
        assert fresh.is_bookmarked("python", "ex1")
    finally:
        fresh.close()


def test_import_overwrites_existing_progress(store):
    store.complete_lesson("python", "old_lesson", xp_reward=50)
    fresh_export = {
        "version": 1,
        "exported_at": "2026-01-01T00:00:00+00:00",
        "tables": {
            "profile": [], "lesson_completions": [], "badges": [],
            "activity_log": [], "quiz_attempts": [], "player_xp": [],
            "daily_refresher_picks": [],
        },
    }
    store.import_progress(fresh_export)
    assert not store.is_lesson_completed("python", "old_lesson")
    assert store.get_player_level("python").total_xp == 0


def test_import_rejects_incompatible_version(store):
    with pytest.raises(ValueError):
        store.import_progress({"version": 999, "tables": {}})


def _backdate_completion(store, language, lesson_id, days_ago):
    old_timestamp = (datetime.now(timezone.utc) - timedelta(days=days_ago)).isoformat()
    with store._conn:
        store._conn.execute(
            "UPDATE lesson_completions SET completed_at = ? WHERE language = ? AND lesson_id = ?",
            (old_timestamp, language, lesson_id),
        )


def test_get_lessons_due_for_review_only_returns_old_completions(store):
    store.complete_lesson("python", "old_lesson", xp_reward=10)
    store.complete_lesson("python", "recent_lesson", xp_reward=10)
    _backdate_completion(store, "python", "old_lesson", days_ago=20)

    due = store.get_lessons_due_for_review("python", min_age_days=14)
    assert due == ["old_lesson"]


def test_lessons_due_for_review_ordered_oldest_first(store):
    store.complete_lesson("python", "a", xp_reward=10)
    store.complete_lesson("python", "b", xp_reward=10)
    _backdate_completion(store, "python", "a", days_ago=15)
    _backdate_completion(store, "python", "b", days_ago=30)

    due = store.get_lessons_due_for_review("python", min_age_days=14)
    assert due == ["b", "a"]


def test_record_quiz_answer_and_concept_accuracy(store):
    store.record_quiz_answer("python", "q1", ["closures", "scope"], is_correct=True)
    store.record_quiz_answer("python", "q2", ["closures"], is_correct=False)
    store.record_quiz_answer("python", "q3", ["recursion"], is_correct=True)

    accuracy = store.get_concept_accuracy("python")
    assert accuracy["closures"] == (1, 2)
    assert accuracy["scope"] == (1, 1)
    assert accuracy["recursion"] == (1, 1)


def test_note_round_trip_and_clearing(store):
    assert store.get_note("python", "ex1") == ""
    store.save_note("python", "ex1", "remember the gotcha here")
    assert store.get_note("python", "ex1") == "remember the gotcha here"
    store.save_note("python", "ex1", "updated note")
    assert store.get_note("python", "ex1") == "updated note"
    store.save_note("python", "ex1", "   ")  # blank after stripping -- deletes the row
    assert store.get_note("python", "ex1") == ""


def test_bookmark_toggle_and_listing(store):
    assert not store.is_bookmarked("python", "ex1")
    store.set_bookmarked("python", "ex1", True)
    assert store.is_bookmarked("python", "ex1")
    store.set_bookmarked("python", "ex2", True)
    assert store.get_bookmarked_lesson_ids("python") == ["ex2", "ex1"]
    store.set_bookmarked("python", "ex1", False)
    assert not store.is_bookmarked("python", "ex1")
    assert store.get_bookmarked_lesson_ids("python") == ["ex2"]


def test_get_daily_activity_counts(store):
    store.log_event("python", "ex1", "lesson_completed")
    store.log_event("python", "ex1", "hint_used")
    counts = store.get_daily_activity_counts("python", days=7)
    today = datetime.now(timezone.utc).date().isoformat()
    assert counts[today] == 2


def test_reset_progress_clears_new_tables_too(store):
    store.record_quiz_answer("python", "q1", ["closures"], is_correct=True)
    store.save_note("python", "ex1", "a note")
    store.set_bookmarked("python", "ex1", True)

    store.reset_progress("python")

    assert store.get_concept_accuracy("python") == {}
    assert store.get_note("python", "ex1") == ""
    assert not store.is_bookmarked("python", "ex1")
