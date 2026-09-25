import pytest

from app.config.clock import today_iso
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


def test_current_exercise_round_trips_and_defaults_to_none(store):
    assert store.get_current_exercise("python") is None
    store.set_current_exercise("python", "ex1")
    assert store.get_current_exercise("python") == "ex1"
    store.set_current_exercise("python", "ex2")
    assert store.get_current_exercise("python") == "ex2"
    assert store.get_current_exercise("java") is None


def test_streak_same_day_is_a_noop(store):
    store.record_play_today("python")
    assert store.get_streak_days("python") == 1
    store.record_play_today("python")  # same day, no-op
    assert store.get_streak_days("python") == 1


def test_streak_increments_on_consecutive_days_and_resets_after_a_gap(store):
    store.record_play_today("python", today="2026-03-01")
    store.record_play_today("python", today="2026-03-02")
    assert store.get_streak_days("python", today="2026-03-02") == 2
    store.record_play_today("python", today="2026-03-05")  # skipped two days
    assert store.get_streak_days("python", today="2026-03-05") == 1


def test_streak_display_lapses_without_play(store):
    store.record_play_today("python", today="2026-03-01")
    store.record_play_today("python", today="2026-03-02")
    assert store.get_streak_days("python", today="2026-03-03") == 2  # yesterday still counts
    assert store.get_streak_days("python", today="2026-03-04") == 0  # lapsed
    assert store.get_streak_days("java") == 0  # never played


def test_streak_crosses_a_year_boundary(store):
    store.record_play_today("python", today="2025-12-31")
    store.record_play_today("python", today="2026-01-01")
    assert store.get_streak_days("python", today="2026-01-01") == 2


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


def test_import_rejects_unknown_column_without_touching_data(store):
    store.complete_lesson("python", "keep_me", xp_reward=10)
    hostile = {
        "version": 1,
        "tables": {"badges": [{"language": "python", "badge_id": "x", "earned_at": "t", "evil); DROP TABLE badges; --": 1}]},
    }
    with pytest.raises(ValueError, match="doesn't know"):
        store.import_progress(hostile)
    # The whole import rolled back -- existing progress is intact.
    assert store.is_lesson_completed("python", "keep_me")


def test_import_rejects_unknown_table_and_bad_shapes(store):
    with pytest.raises(ValueError, match="unknown tables"):
        store.import_progress({"version": 1, "tables": {"sqlite_master": []}})
    with pytest.raises(ValueError, match="list of rows"):
        store.import_progress({"version": 1, "tables": {"badges": {"not": "a list"}}})
    with pytest.raises(ValueError, match="JSON object"):
        store.import_progress([1, 2, 3])


def test_activity_since_rows_are_mappable_and_connection_row_factory_untouched(store):
    store.log_event("python", "ex1", "hint_used", "h")
    rows = store.get_activity_since("python", "2000-01-01")
    assert rows[0]["event_type"] == "hint_used"
    assert store._conn.row_factory is None


# -- streak freezes -----------------------------------------------------------

def _play_days(store, language, days):
    for d in days:
        store.record_play_today(language, today=d)


def test_freeze_token_earned_at_seven_and_bridges_one_missed_day(store):
    _play_days(store, "python", [f"2026-03-{d:02d}" for d in range(1, 8)])  # 7-day streak
    assert store.get_streak_days("python", today="2026-03-07") == 7
    assert store.get_freeze_tokens("python") == 1

    # Skip 03-08 entirely; the streak survives on display and on the next play.
    assert store.get_streak_days("python", today="2026-03-09") == 7
    store.record_play_today("python", today="2026-03-09")
    assert store.get_streak_days("python", today="2026-03-09") == 8
    assert store.get_freeze_tokens("python") == 0


def test_two_missed_days_break_the_streak_even_with_a_token(store):
    _play_days(store, "python", [f"2026-03-{d:02d}" for d in range(1, 8)])
    assert store.get_freeze_tokens("python") == 1
    assert store.get_streak_days("python", today="2026-03-10") == 0
    store.record_play_today("python", today="2026-03-10")
    assert store.get_streak_days("python", today="2026-03-10") == 1
    assert store.get_freeze_tokens("python") == 1  # not spent on a real break


def test_freeze_tokens_cap_at_three(store):
    from datetime import date, timedelta
    _play_days(store, "python", [(date(2026, 1, 1) + timedelta(days=i)).isoformat() for i in range(35)])
    assert store.get_freeze_tokens("python") == 3


def test_freeze_column_is_added_to_a_pre_existing_profile_table(tmp_path):
    import sqlite3
    path = tmp_path / "old.sqlite3"
    conn = sqlite3.connect(str(path))
    conn.execute("CREATE TABLE profile (language TEXT PRIMARY KEY, current_exercise_id TEXT, "
                 "streak_days INTEGER NOT NULL DEFAULT 0, last_played_date TEXT)")
    conn.execute("INSERT INTO profile (language, streak_days, last_played_date) VALUES ('python', 4, '2026-03-01')")
    conn.commit()
    conn.close()

    store = ProgressStore(path)
    try:
        assert store.get_freeze_tokens("python") == 0
        assert store.get_streak_days("python", today="2026-03-02") == 4
    finally:
        store.close()


# -- weekly goal --------------------------------------------------------------

def test_count_completions_this_week_counts_only_the_current_local_week(store):
    store.complete_lesson("python", "a", xp_reward=10)
    store.complete_lesson("python", "b", xp_reward=10)
    store.complete_lesson("java", "c", xp_reward=10)
    assert store.count_completions_this_week("python") == 2
    assert store.count_completions_this_week("java") == 1
    # Backdate one to last month -- it drops out.
    with store._conn:
        store._conn.execute("UPDATE lesson_completions SET completed_at = '2020-01-01T10:00:00+00:00' WHERE lesson_id = 'a'")
    assert store.count_completions_this_week("python") == 1


# -- recent errors --------------------------------------------------------------

def test_get_recent_errors_returns_error_tails_most_recent_first(store):
    store.log_event("python", "ex1", "attempt_error", "NameError: a")
    store.log_event("python", "ex1", "attempt_wrong_output", "not an error")
    store.log_event("python", "ex2", "attempt_error", "TypeError: b")
    store.log_event("java", "ex3", "attempt_error", "other track")
    assert store.get_recent_errors("python") == [("ex2", "TypeError: b"), ("ex1", "NameError: a")]
    assert store.get_recent_errors("python", limit=1) == [("ex2", "TypeError: b")]


# -- solve times ---------------------------------------------------------------

def test_solve_times_track_personal_bests(store):
    assert store.get_best_solve_time("python", "ex1") is None
    assert store.record_solve_time("python", "ex1", 120) is True   # first time counts as a best
    assert store.record_solve_time("python", "ex1", 150) is False
    assert store.record_solve_time("python", "ex1", 95) is True
    assert store.get_best_solve_time("python", "ex1") == 95
    store.record_solve_time("python", "ex2", 0)  # clamped to 1s, never 0
    assert store.get_best_solve_times("python") == {"ex1": 95, "ex2": 1}
    store.reset_progress("python")
    assert store.get_best_solve_times("python") == {}


# -- spaced repetition ------------------------------------------------------

def test_review_intervals_grow_on_passes_and_reset_on_a_fail(store):
    s1 = store.schedule_review("python", "ex1", passed=True, today="2026-03-01")
    assert (s1.interval_days, s1.due_date, s1.review_streak) == (3, "2026-03-04", 1)
    s2 = store.schedule_review("python", "ex1", passed=True, today="2026-03-04")
    assert (s2.interval_days, s2.due_date, s2.review_streak) == (7, "2026-03-11", 2)
    s3 = store.schedule_review("python", "ex1", passed=True, today="2026-03-11")
    assert s3.interval_days > 7 and s3.review_streak == 3
    assert s3.ease > s2.ease

    failed = store.schedule_review("python", "ex1", passed=False, today="2026-03-20")
    assert (failed.interval_days, failed.due_date, failed.review_streak) == (1, "2026-03-21", 0)
    assert failed.ease < s3.ease
    stored = store.get_review_state("python", "ex1")
    assert (stored.due_date, stored.interval_days, stored.review_streak) == ("2026-03-21", 1, 0)


def test_review_interval_is_capped_and_ease_is_bounded(store):
    today = "2026-01-01"
    for _ in range(20):
        state = store.schedule_review("python", "ex1", passed=True, today=today)
        today = state.due_date
    assert state.interval_days <= 120
    assert state.ease <= 3.0
    for _ in range(20):
        state = store.schedule_review("python", "ex1", passed=False, today=today)
    assert state.ease >= 1.3


def test_due_reviews_are_most_overdue_first_and_respect_today(store):
    store.schedule_review("python", "later", passed=True, today="2026-03-10")   # due 03-13
    store.schedule_review("python", "sooner", passed=True, today="2026-03-01")  # due 03-04
    store.schedule_review("python", "future", passed=True, today="2026-03-20")  # due 03-23
    store.schedule_review("java", "other_track", passed=True, today="2026-03-01")

    assert store.get_due_reviews("python", today="2026-03-15") == ["sooner", "later"]
    assert store.get_due_reviews("python", today="2026-03-15", limit=1) == ["sooner"]
    assert store.count_due_reviews("python", today="2026-03-15") == 2
    assert store.count_upcoming_reviews("python", days=7, today="2026-03-15") == 0
    assert store.count_upcoming_reviews("python", days=10, today="2026-03-15") == 1
    assert store.get_due_reviews("python", today="2026-03-01") == []


def test_review_state_days_until_due(store):
    state = store.schedule_review("python", "ex1", passed=True, today="2026-03-01")
    assert state.days_until_due("2026-03-01") == 3
    assert state.days_until_due("2026-03-06") == -2
    assert store.get_review_state("python", "missing") is None


def test_legacy_completions_are_backfilled_into_the_schedule(tmp_path):
    path = tmp_path / "legacy.sqlite3"
    first = ProgressStore(path)
    first.complete_lesson("python", "old", xp_reward=10)
    with first._conn:
        first._conn.execute("DELETE FROM review_schedule")  # simulate a DB from before the table existed
        first._conn.execute(
            "UPDATE lesson_completions SET completed_at = ? WHERE lesson_id = ?",
            ("2026-01-01T09:30:00.123456+00:00", "old"),
        )
    first.close()

    reopened = ProgressStore(path)
    try:
        state = reopened.get_review_state("python", "old")
        assert state is not None
        assert state.due_date == "2026-01-15"  # completed + 14 days, the old rule
        assert "old" in reopened.get_due_reviews("python", today="2026-02-01")
    finally:
        reopened.close()


def test_reset_and_export_cover_the_review_schedule(store, tmp_path):
    store.schedule_review("python", "ex1", passed=True, today="2026-03-01")
    exported = store.export_progress()
    assert exported["tables"]["review_schedule"][0]["lesson_id"] == "ex1"

    fresh = ProgressStore(tmp_path / "restored.sqlite3")
    try:
        fresh.import_progress(exported)
        assert fresh.get_review_state("python", "ex1").due_date == "2026-03-04"
    finally:
        fresh.close()

    store.reset_progress("python")
    assert store.get_review_state("python", "ex1") is None


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


def test_get_daily_activity_counts_buckets_by_local_day(store):
    store.log_event("python", "ex1", "lesson_completed")
    store.log_event("python", "ex1", "hint_used")
    counts = store.get_daily_activity_counts("python", days=7)
    assert counts[today_iso()] == 2


def test_reset_progress_clears_new_tables_too(store):
    store.record_quiz_answer("python", "q1", ["closures"], is_correct=True)
    store.save_note("python", "ex1", "a note")
    store.set_bookmarked("python", "ex1", True)

    store.reset_progress("python")

    assert store.get_concept_accuracy("python") == {}
    assert store.get_note("python", "ex1") == ""
    assert not store.is_bookmarked("python", "ex1")
