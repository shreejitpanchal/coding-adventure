"""SQLite-backed progress, gamification, and activity tracking -- one
XP/streak/level per language track, since a "professional" here is
plausibly juggling more than one track at once."""
from __future__ import annotations

import logging
import sqlite3
from contextlib import closing
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

from app.config.clock import days_between, today_iso

logger = logging.getLogger(__name__)

SCHEMA = """
CREATE TABLE IF NOT EXISTS profile (
    language TEXT PRIMARY KEY,
    current_exercise_id TEXT,
    streak_days INTEGER NOT NULL DEFAULT 0,
    last_played_date TEXT
);

CREATE TABLE IF NOT EXISTS lesson_completions (
    language TEXT NOT NULL,
    lesson_id TEXT NOT NULL,
    completed_at TEXT NOT NULL,
    PRIMARY KEY (language, lesson_id)
);

CREATE TABLE IF NOT EXISTS badges (
    language TEXT NOT NULL,
    badge_id TEXT NOT NULL,
    earned_at TEXT NOT NULL,
    PRIMARY KEY (language, badge_id)
);

CREATE TABLE IF NOT EXISTS activity_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    language TEXT NOT NULL,
    lesson_id TEXT,
    event_type TEXT NOT NULL,
    detail TEXT,
    timestamp TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS quiz_attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    language TEXT NOT NULL,
    score INTEGER NOT NULL,
    total INTEGER NOT NULL,
    completed_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS player_xp (
    language TEXT PRIMARY KEY,
    total_xp INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS daily_refresher_picks (
    language TEXT NOT NULL,
    pick_date TEXT NOT NULL,
    lesson_id TEXT NOT NULL,
    PRIMARY KEY (language, pick_date, lesson_id)
);

CREATE TABLE IF NOT EXISTS quiz_answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    language TEXT NOT NULL,
    question_id TEXT NOT NULL,
    concept_tags TEXT NOT NULL,
    is_correct INTEGER NOT NULL,
    answered_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS exercise_notes (
    language TEXT NOT NULL,
    lesson_id TEXT NOT NULL,
    note TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    PRIMARY KEY (language, lesson_id)
);

CREATE TABLE IF NOT EXISTS bookmarks (
    language TEXT NOT NULL,
    lesson_id TEXT NOT NULL,
    bookmarked_at TEXT NOT NULL,
    PRIMARY KEY (language, lesson_id)
);

CREATE TABLE IF NOT EXISTS solve_times (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    language TEXT NOT NULL,
    lesson_id TEXT NOT NULL,
    seconds INTEGER NOT NULL,
    recorded_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS review_schedule (
    language TEXT NOT NULL,
    lesson_id TEXT NOT NULL,
    interval_days INTEGER NOT NULL,
    ease REAL NOT NULL,
    due_date TEXT NOT NULL,
    last_reviewed TEXT NOT NULL,
    review_streak INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (language, lesson_id)
);
"""

# Completions recorded before the review_schedule table existed get a
# first review 14 days after completion (the old "spaced review" rule).
# INSERT OR IGNORE keeps this idempotent, so it can run on every start.
_BACKFILL_REVIEWS = """
INSERT OR IGNORE INTO review_schedule
    (language, lesson_id, interval_days, ease, due_date, last_reviewed, review_streak)
SELECT language, lesson_id, 14, 2.5, date(substr(completed_at, 1, 10), '+14 days'), completed_at, 1
FROM lesson_completions
"""

# Columns added to existing tables after the first release. Applied with
# ALTER TABLE only when PRAGMA table_info says they're missing, so an old
# progress.sqlite3 upgrades in place.
_COLUMN_MIGRATIONS: list[tuple[str, str, str]] = [
    ("profile", "freeze_tokens", "INTEGER NOT NULL DEFAULT 0"),
]

# Streak freezes: one token is earned each time the streak reaches a
# multiple of STREAK_FREEZE_EVERY days (held up to STREAK_FREEZE_MAX); a
# token is spent automatically to bridge exactly one missed day.
STREAK_FREEZE_EVERY = 7
STREAK_FREEZE_MAX = 3

# Spaced-repetition tuning (a simplified SM-2). Intervals are in days.
REVIEW_FIRST_INTERVAL = 3
REVIEW_SECOND_INTERVAL = 7
REVIEW_MAX_INTERVAL = 120
REVIEW_DEFAULT_EASE = 2.5
REVIEW_MIN_EASE = 1.3
REVIEW_MAX_EASE = 3.0
REVIEW_EASE_STEP = 0.15

# Bumped only if a future schema change makes an old export incompatible
# with import_progress()'s column-list assumptions.
PROGRESS_EXPORT_VERSION = 1

_EXPORT_TABLES = [
    "profile", "lesson_completions", "badges", "activity_log",
    "quiz_attempts", "player_xp", "daily_refresher_picks",
    "quiz_answers", "exercise_notes", "bookmarks", "review_schedule", "solve_times",
]

# XP cost to clear level N is N * 100 (level 1->2 costs 100, 2->3 costs 200, ...).
_XP_PER_LEVEL_STEP = 100

# event_types that count as a struggling attempt for get_recent_failure_count().
_FAILURE_EVENT_TYPES = {"attempt_error", "attempt_wrong_output", "attempt_timeout", "attempt_blocked"}


def _level_from_xp(total_xp: int) -> tuple[int, int, int]:
    level = 1
    remaining = total_xp
    xp_needed = level * _XP_PER_LEVEL_STEP
    while remaining >= xp_needed:
        remaining -= xp_needed
        level += 1
        xp_needed = level * _XP_PER_LEVEL_STEP
    return level, remaining, xp_needed


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class PlayerLevel:
    level: int
    xp_into_level: int
    xp_needed_for_level: int
    total_xp: int


@dataclass
class WeeklySummary:
    lessons_completed: int
    quiz_attempts: int
    badges_earned: int
    active_days: int


@dataclass(frozen=True)
class ReviewState:
    """One exercise's place in the spaced-repetition schedule."""
    lesson_id: str
    interval_days: int
    ease: float
    due_date: str
    """Local ISO date the next review is due."""
    last_reviewed: str
    review_streak: int
    """Consecutive successful reviews; reset to 0 by a failed one."""

    def days_until_due(self, today: str) -> int:
        """Negative when overdue."""
        return days_between(today, self.due_date)


class ProgressStore:
    """Owns the SQLite connection for progress data across every language track."""

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._conn = sqlite3.connect(str(db_path))
        self._conn.execute("PRAGMA foreign_keys = ON")
        self._init_schema()

    def _init_schema(self) -> None:
        with self._conn:
            self._conn.executescript(SCHEMA)
            for table, column, decl in _COLUMN_MIGRATIONS:
                if column not in self._table_columns(table):
                    self._conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {decl}")
                    logger.info("Migrated %s: added column %s", table, column)
            self._conn.execute(_BACKFILL_REVIEWS)

    def close(self) -> None:
        self._conn.close()

    def _ensure_profile(self, language: str) -> None:
        with self._conn:
            self._conn.execute(
                "INSERT OR IGNORE INTO profile (language) VALUES (?)", (language,)
            )
            self._conn.execute(
                "INSERT OR IGNORE INTO player_xp (language, total_xp) VALUES (?, 0)", (language,)
            )

    # -- Profile -----------------------------------------------------
    def set_current_exercise(self, language: str, exercise_id: str) -> None:
        self._ensure_profile(language)
        with self._conn:
            self._conn.execute(
                "UPDATE profile SET current_exercise_id = ? WHERE language = ?", (exercise_id, language)
            )

    def get_current_exercise(self, language: str) -> Optional[str]:
        with closing(self._conn.cursor()) as cur:
            cur.execute("SELECT current_exercise_id FROM profile WHERE language = ?", (language,))
            row = cur.fetchone()
            return row[0] if row else None

    def record_play_today(self, language: str, today: Optional[str] = None) -> None:
        """Mark the user's LOCAL calendar day as played and advance the
        streak. Call this only when something was actually accomplished
        (an exercise completed, a quiz finished) -- opening a screen is not
        playing. `today` is injectable for tests; production callers leave
        it to app.config.clock.

        Streak freezes: a gap of exactly one missed day is bridged
        automatically when the user holds a freeze token (spending it);
        reaching a multiple of STREAK_FREEZE_EVERY earns one, up to
        STREAK_FREEZE_MAX."""
        self._ensure_profile(language)
        today = today or today_iso()
        with closing(self._conn.cursor()) as cur:
            cur.execute("SELECT last_played_date, streak_days, freeze_tokens FROM profile WHERE language = ?", (language,))
            last_played, streak, tokens = cur.fetchone()
        if last_played == today:
            return
        gap = days_between(last_played, today) if last_played is not None else None
        if gap == 1:
            streak += 1
        elif gap == 2 and tokens > 0:
            tokens -= 1
            streak += 1
            self.log_event(language, None, "streak_freeze_used", f"streak={streak}")
        else:
            streak = 1
        if streak > 0 and streak % STREAK_FREEZE_EVERY == 0 and tokens < STREAK_FREEZE_MAX:
            tokens += 1
            self.log_event(language, None, "streak_freeze_earned", f"streak={streak}")
        with self._conn:
            self._conn.execute(
                "UPDATE profile SET last_played_date = ?, streak_days = ?, freeze_tokens = ? WHERE language = ?",
                (today, streak, tokens, language),
            )

    def get_streak_days(self, language: str, today: Optional[str] = None) -> int:
        """The streak as it stands *now*: the stored count while the last
        play was today or yesterday (or the day before, if a freeze token
        would bridge it), otherwise 0. The stored value is only ever
        rewritten on the next play, so without this check a screen would
        keep showing a 7-day streak a fortnight after it lapsed."""
        today = today or today_iso()
        with closing(self._conn.cursor()) as cur:
            cur.execute("SELECT streak_days, last_played_date, freeze_tokens FROM profile WHERE language = ?", (language,))
            row = cur.fetchone()
        if row is None or row[1] is None:
            return 0
        streak, last_played, tokens = row
        gap = days_between(last_played, today)
        if gap <= 1 or (gap == 2 and tokens > 0):
            return streak
        return 0

    def get_freeze_tokens(self, language: str) -> int:
        with closing(self._conn.cursor()) as cur:
            cur.execute("SELECT freeze_tokens FROM profile WHERE language = ?", (language,))
            row = cur.fetchone()
            return row[0] if row else 0

    # -- Weekly goal -----------------------------------------------------
    def count_completions_this_week(self, language: str, today: Optional[str] = None) -> int:
        """Exercises completed since Monday of the user's current local
        week (completed_at is UTC, so rows are bucketed in Python)."""
        today_date = date.fromisoformat(today or today_iso())
        week_start = today_date - timedelta(days=today_date.weekday())
        # Pull one extra day so a UTC timestamp just before local Monday 00:00 is still considered.
        cutoff = (datetime.combine(week_start, datetime.min.time(), tzinfo=timezone.utc) - timedelta(days=1)).isoformat()
        with closing(self._conn.cursor()) as cur:
            cur.execute(
                "SELECT completed_at FROM lesson_completions WHERE language = ? AND completed_at >= ?",
                (language, cutoff),
            )
            stamps = [row[0] for row in cur.fetchall()]
        return sum(
            1 for stamp in stamps
            if week_start <= datetime.fromisoformat(stamp).astimezone().date() <= today_date
        )

    # -- Solve times -------------------------------------------------------
    def record_solve_time(self, language: str, lesson_id: str, seconds: int) -> bool:
        """Store one timed solve. Returns True when it is a new personal
        best for this exercise (or the first recorded time)."""
        seconds = max(1, int(seconds))
        previous_best = self.get_best_solve_time(language, lesson_id)
        with self._conn:
            self._conn.execute(
                "INSERT INTO solve_times (language, lesson_id, seconds, recorded_at) VALUES (?, ?, ?, ?)",
                (language, lesson_id, seconds, _now()),
            )
        return previous_best is None or seconds < previous_best

    def get_best_solve_time(self, language: str, lesson_id: str) -> Optional[int]:
        with closing(self._conn.cursor()) as cur:
            cur.execute("SELECT MIN(seconds) FROM solve_times WHERE language = ? AND lesson_id = ?", (language, lesson_id))
            row = cur.fetchone()
            return row[0] if row and row[0] is not None else None

    def get_best_solve_times(self, language: str) -> dict[str, int]:
        """lesson_id -> best seconds, for list screens (one query, not one per row)."""
        with closing(self._conn.cursor()) as cur:
            cur.execute("SELECT lesson_id, MIN(seconds) FROM solve_times WHERE language = ? GROUP BY lesson_id", (language,))
            return {row[0]: row[1] for row in cur.fetchall()}

    # -- Exercises -------------------------------------------------------
    def complete_lesson(self, language: str, lesson_id: str, xp_reward: int) -> None:
        self._ensure_profile(language)
        first_time = not self.is_lesson_completed(language, lesson_id)
        with self._conn:
            self._conn.execute(
                """INSERT INTO lesson_completions (language, lesson_id, completed_at)
                   VALUES (?, ?, ?)
                   ON CONFLICT(language, lesson_id) DO UPDATE SET completed_at = excluded.completed_at""",
                (language, lesson_id, _now()),
            )
        self.log_event(language, lesson_id, "lesson_completed", f"xp={xp_reward}")
        if first_time:
            self.add_xp(language, xp_reward)

    def is_lesson_completed(self, language: str, lesson_id: str) -> bool:
        with closing(self._conn.cursor()) as cur:
            cur.execute(
                "SELECT 1 FROM lesson_completions WHERE language = ? AND lesson_id = ?", (language, lesson_id)
            )
            return cur.fetchone() is not None

    def get_completed_lesson_ids(self, language: str) -> list[str]:
        with closing(self._conn.cursor()) as cur:
            cur.execute("SELECT lesson_id FROM lesson_completions WHERE language = ?", (language,))
            return [row[0] for row in cur.fetchall()]

    # -- Daily Refresher -----------------------------------------------
    def get_daily_refresher_picks(self, language: str, pick_date: str) -> list[str]:
        """The exercise ids fixed for this language on this date, or an
        empty list if today's set hasn't been generated/saved yet -- the
        set is saved once per day so it stays a stable, finishable
        checklist instead of silently reshuffling as items complete."""
        with closing(self._conn.cursor()) as cur:
            cur.execute(
                "SELECT lesson_id FROM daily_refresher_picks WHERE language = ? AND pick_date = ? ORDER BY rowid",
                (language, pick_date),
            )
            return [row[0] for row in cur.fetchall()]

    def save_daily_refresher_picks(self, language: str, pick_date: str, lesson_ids: list[str]) -> None:
        with self._conn:
            self._conn.executemany(
                "INSERT OR IGNORE INTO daily_refresher_picks (language, pick_date, lesson_id) VALUES (?, ?, ?)",
                [(language, pick_date, lesson_id) for lesson_id in lesson_ids],
            )

    # -- Spaced repetition -----------------------------------------------
    def schedule_review(self, language: str, lesson_id: str, passed: bool, today: Optional[str] = None) -> ReviewState:
        """Record a pass/fail on an exercise and compute its next due date
        (a simplified SM-2):

        - first pass -> due in REVIEW_FIRST_INTERVAL days; second -> in
          REVIEW_SECOND_INTERVAL; after that interval *= ease (ease creeps
          up by REVIEW_EASE_STEP per pass, capped), interval capped at
          REVIEW_MAX_INTERVAL;
        - a fail -> due tomorrow, ease drops by REVIEW_EASE_STEP (floored),
          review_streak resets.

        Called on every successful completion and on a failed attempt at an
        exercise that had previously been completed (i.e. a review that went
        wrong). Returns the new state."""
        today = today or today_iso()
        current = self.get_review_state(language, lesson_id)
        ease = current.ease if current else REVIEW_DEFAULT_EASE
        streak = current.review_streak if current else 0

        if passed:
            streak += 1
            if streak <= 1:
                interval = REVIEW_FIRST_INTERVAL
            elif streak == 2:
                interval = REVIEW_SECOND_INTERVAL
            else:
                interval = min(REVIEW_MAX_INTERVAL, max(REVIEW_SECOND_INTERVAL + 1, round(current.interval_days * ease)))
            ease = min(REVIEW_MAX_EASE, ease + REVIEW_EASE_STEP)
        else:
            streak = 0
            interval = 1
            ease = max(REVIEW_MIN_EASE, ease - REVIEW_EASE_STEP)

        due_date = (date.fromisoformat(today) + timedelta(days=interval)).isoformat()
        with self._conn:
            self._conn.execute(
                """INSERT INTO review_schedule
                       (language, lesson_id, interval_days, ease, due_date, last_reviewed, review_streak)
                   VALUES (?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(language, lesson_id) DO UPDATE SET
                       interval_days = excluded.interval_days, ease = excluded.ease,
                       due_date = excluded.due_date, last_reviewed = excluded.last_reviewed,
                       review_streak = excluded.review_streak""",
                (language, lesson_id, interval, ease, due_date, _now(), streak),
            )
        return ReviewState(lesson_id, interval, ease, due_date, _now(), streak)

    def get_review_state(self, language: str, lesson_id: str) -> Optional[ReviewState]:
        with closing(self._conn.cursor()) as cur:
            cur.execute(
                "SELECT lesson_id, interval_days, ease, due_date, last_reviewed, review_streak "
                "FROM review_schedule WHERE language = ? AND lesson_id = ?",
                (language, lesson_id),
            )
            row = cur.fetchone()
        return ReviewState(*row) if row else None

    def get_due_reviews(self, language: str, today: Optional[str] = None, limit: Optional[int] = None) -> list[str]:
        """Lesson ids whose review is due on or before `today`, most
        overdue first -- the Review queue, and the source of the Daily
        Refresher's review slot."""
        today = today or today_iso()
        sql = "SELECT lesson_id FROM review_schedule WHERE language = ? AND due_date <= ? ORDER BY due_date ASC, lesson_id"
        params: list = [language, today]
        if limit is not None:
            sql += " LIMIT ?"
            params.append(limit)
        with closing(self._conn.cursor()) as cur:
            cur.execute(sql, params)
            return [row[0] for row in cur.fetchall()]

    def count_due_reviews(self, language: str, today: Optional[str] = None) -> int:
        today = today or today_iso()
        with closing(self._conn.cursor()) as cur:
            cur.execute("SELECT COUNT(*) FROM review_schedule WHERE language = ? AND due_date <= ?", (language, today))
            return cur.fetchone()[0]

    def count_upcoming_reviews(self, language: str, days: int, today: Optional[str] = None) -> int:
        """Reviews falling due after today and within the next `days` days."""
        today = today or today_iso()
        horizon = (date.fromisoformat(today) + timedelta(days=days)).isoformat()
        with closing(self._conn.cursor()) as cur:
            cur.execute(
                "SELECT COUNT(*) FROM review_schedule WHERE language = ? AND due_date > ? AND due_date <= ?",
                (language, today, horizon),
            )
            return cur.fetchone()[0]

    # -- Badges/achievements ----------------------------------------------
    def award_badge(self, language: str, badge_id: str) -> bool:
        """Returns True if newly awarded, False if already had it."""
        with self._conn:
            cur = self._conn.execute(
                "INSERT OR IGNORE INTO badges (language, badge_id, earned_at) VALUES (?, ?, ?)",
                (language, badge_id, _now()),
            )
            newly_awarded = cur.rowcount > 0
        if newly_awarded:
            self.log_event(language, None, "badge_earned", badge_id)
        return newly_awarded

    def get_badges_with_dates(self, language: str) -> list[tuple[str, str]]:
        with closing(self._conn.cursor()) as cur:
            cur.execute(
                "SELECT badge_id, earned_at FROM badges WHERE language = ? ORDER BY earned_at", (language,)
            )
            return [(row[0], row[1]) for row in cur.fetchall()]

    # -- Quiz --------------------------------------------------------------
    def record_quiz_attempt(self, language: str, score: int, total: int) -> None:
        self._ensure_profile(language)
        with self._conn:
            self._conn.execute(
                "INSERT INTO quiz_attempts (language, score, total, completed_at) VALUES (?, ?, ?, ?)",
                (language, score, total, _now()),
            )
        self.log_event(language, None, "quiz_completed", f"score={score}/{total}")
        # Every attempt is a freshly randomized session, so unlike exercises
        # there's no first-time-only gate.
        self.add_xp(language, score * 5)

    def record_quiz_answer(self, language: str, question_id: str, concept_tags: list[str], is_correct: bool) -> None:
        """One row per question answered, independent of record_quiz_attempt()'s
        per-session score/total summary -- powers get_concept_accuracy()'s
        "Weakest concepts" panel, which needs per-question, per-tag detail
        that a session-level score can't provide."""
        with self._conn:
            self._conn.execute(
                "INSERT INTO quiz_answers (language, question_id, concept_tags, is_correct, answered_at) "
                "VALUES (?, ?, ?, ?, ?)",
                (language, question_id, ",".join(concept_tags), 1 if is_correct else 0, _now()),
            )

    def get_concept_accuracy(self, language: str) -> dict[str, tuple[int, int]]:
        """tag -> (correct, total) across every recorded quiz answer whose
        question carries that tag. A question with several tags counts
        toward each of them independently."""
        with closing(self._conn.cursor()) as cur:
            cur.execute("SELECT concept_tags, is_correct FROM quiz_answers WHERE language = ?", (language,))
            rows = cur.fetchall()
        accuracy: dict[str, list[int]] = {}
        for tags_str, is_correct in rows:
            for tag in tags_str.split(","):
                if not tag:
                    continue
                bucket = accuracy.setdefault(tag, [0, 0])
                bucket[1] += 1
                if is_correct:
                    bucket[0] += 1
        return {tag: (correct, total) for tag, (correct, total) in accuracy.items()}

    def get_best_quiz_score(self, language: str) -> Optional[tuple[int, int]]:
        with closing(self._conn.cursor()) as cur:
            cur.execute(
                "SELECT score, total FROM quiz_attempts WHERE language = ? "
                "ORDER BY (score * 1.0 / total) DESC, score DESC LIMIT 1",
                (language,),
            )
            row = cur.fetchone()
            return (row[0], row[1]) if row else None

    # -- XP / leveling -------------------------------------------------------
    def add_xp(self, language: str, amount: int) -> PlayerLevel:
        self._ensure_profile(language)
        if amount:
            with self._conn:
                self._conn.execute(
                    "UPDATE player_xp SET total_xp = total_xp + ? WHERE language = ?", (amount, language)
                )
        return self.get_player_level(language)

    def get_player_level(self, language: str) -> PlayerLevel:
        self._ensure_profile(language)
        with closing(self._conn.cursor()) as cur:
            cur.execute("SELECT total_xp FROM player_xp WHERE language = ?", (language,))
            row = cur.fetchone()
            total_xp = row[0] if row else 0
        level, xp_into_level, xp_needed = _level_from_xp(total_xp)
        return PlayerLevel(
            level=level, xp_into_level=xp_into_level, xp_needed_for_level=xp_needed, total_xp=total_xp,
        )

    # -- Activity log ------------------------------------------------------
    def log_event(self, language: str, lesson_id: Optional[str], event_type: str, detail: str = "") -> None:
        with self._conn:
            self._conn.execute(
                "INSERT INTO activity_log (language, lesson_id, event_type, detail, timestamp) VALUES (?, ?, ?, ?, ?)",
                (language, lesson_id, event_type, detail, _now()),
            )

    def _row_cursor(self) -> sqlite3.Cursor:
        """A cursor yielding sqlite3.Row, set on the cursor rather than the
        shared connection so a query in flight elsewhere never sees its
        row type flip underneath it."""
        cur = self._conn.cursor()
        cur.row_factory = sqlite3.Row
        return cur

    def get_activity_since(self, language: str, cutoff_iso: str) -> list[sqlite3.Row]:
        with closing(self._row_cursor()) as cur:
            cur.execute(
                "SELECT * FROM activity_log WHERE language = ? AND timestamp >= ? ORDER BY id DESC",
                (language, cutoff_iso),
            )
            return cur.fetchall()

    def get_recent_errors(self, language: str, days: int = 30, limit: int = 500) -> list[tuple[Optional[str], str]]:
        """(lesson_id, stderr_tail) for every attempt_error in the last
        `days` days, most recent first -- input to
        app.engine.error_insights.summarize_errors()."""
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        with closing(self._conn.cursor()) as cur:
            cur.execute(
                "SELECT lesson_id, detail FROM activity_log "
                "WHERE language = ? AND event_type = 'attempt_error' AND timestamp >= ? ORDER BY id DESC LIMIT ?",
                (language, cutoff, limit),
            )
            return [(row[0], row[1] or "") for row in cur.fetchall()]

    def get_recent_failure_count(self, language: str, lesson_id: str) -> int:
        """Resets to 0 automatically once the exercise is passed -- powers
        the "keep struggling? here's related practice" nudge."""
        with closing(self._conn.cursor()) as cur:
            cur.execute(
                "SELECT event_type FROM activity_log WHERE language = ? AND lesson_id = ? ORDER BY id DESC",
                (language, lesson_id),
            )
            rows = cur.fetchall()
        count = 0
        for (event_type,) in rows:
            if event_type == "lesson_completed":
                break
            if event_type in _FAILURE_EVENT_TYPES:
                count += 1
        return count

    def get_daily_activity_counts(self, language: str, days: int = 84) -> dict[str, int]:
        """Local ISO date -> count of activity_log events that day, for the
        last `days` days (84 = 12 weeks) -- powers the Progress screen's
        activity heatmap. Timestamps are stored in UTC; they're bucketed
        into the user's local day here so an evening session doesn't show
        up on "tomorrow" for anyone east of Greenwich."""
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days + 1)).isoformat()
        with closing(self._conn.cursor()) as cur:
            cur.execute(
                "SELECT timestamp FROM activity_log WHERE language = ? AND timestamp >= ?",
                (language, cutoff),
            )
            stamps = [row[0] for row in cur.fetchall()]
        counts: dict[str, int] = {}
        for stamp in stamps:
            local_day = datetime.fromisoformat(stamp).astimezone().date().isoformat()
            counts[local_day] = counts.get(local_day, 0) + 1
        return counts

    def get_weekly_summary(self, language: str) -> WeeklySummary:
        cutoff = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
        rows = self.get_activity_since(language, cutoff)

        lessons_completed = 0
        quiz_attempts = 0
        badges_earned = 0
        active_dates: set[str] = set()

        for row in rows:
            event_type = row["event_type"]
            active_dates.add(row["timestamp"][:10])
            if event_type == "lesson_completed":
                lessons_completed += 1
            elif event_type == "quiz_completed":
                quiz_attempts += 1
            elif event_type == "badge_earned":
                badges_earned += 1

        return WeeklySummary(
            lessons_completed=lessons_completed,
            quiz_attempts=quiz_attempts,
            badges_earned=badges_earned,
            active_days=len(active_dates),
        )

    # -- Notes and bookmarks ------------------------------------------------
    def get_note(self, language: str, lesson_id: str) -> str:
        with closing(self._conn.cursor()) as cur:
            cur.execute(
                "SELECT note FROM exercise_notes WHERE language = ? AND lesson_id = ?", (language, lesson_id)
            )
            row = cur.fetchone()
            return row[0] if row else ""

    def save_note(self, language: str, lesson_id: str, note: str) -> None:
        """An emptied note is deleted outright rather than kept as a stored
        blank row, so "never wrote one" and "wrote one, then cleared it"
        look identical to every reader (get_note, export, a future
        has-a-note indicator)."""
        note = note.strip()
        with self._conn:
            if note:
                self._conn.execute(
                    """INSERT INTO exercise_notes (language, lesson_id, note, updated_at)
                       VALUES (?, ?, ?, ?)
                       ON CONFLICT(language, lesson_id) DO UPDATE SET note = excluded.note, updated_at = excluded.updated_at""",
                    (language, lesson_id, note, _now()),
                )
            else:
                self._conn.execute(
                    "DELETE FROM exercise_notes WHERE language = ? AND lesson_id = ?", (language, lesson_id)
                )

    def is_bookmarked(self, language: str, lesson_id: str) -> bool:
        with closing(self._conn.cursor()) as cur:
            cur.execute(
                "SELECT 1 FROM bookmarks WHERE language = ? AND lesson_id = ?", (language, lesson_id)
            )
            return cur.fetchone() is not None

    def set_bookmarked(self, language: str, lesson_id: str, bookmarked: bool) -> None:
        with self._conn:
            if bookmarked:
                self._conn.execute(
                    "INSERT OR IGNORE INTO bookmarks (language, lesson_id, bookmarked_at) VALUES (?, ?, ?)",
                    (language, lesson_id, _now()),
                )
            else:
                self._conn.execute(
                    "DELETE FROM bookmarks WHERE language = ? AND lesson_id = ?", (language, lesson_id)
                )

    def get_bookmarked_lesson_ids(self, language: str) -> list[str]:
        with closing(self._conn.cursor()) as cur:
            cur.execute(
                "SELECT lesson_id FROM bookmarks WHERE language = ? ORDER BY bookmarked_at DESC, rowid DESC", (language,)
            )
            return [row[0] for row in cur.fetchall()]

    # -- Reset ---------------------------------------------------------
    def reset_progress(self, language: str) -> None:
        with self._conn:
            self._conn.execute("DELETE FROM lesson_completions WHERE language = ?", (language,))
            self._conn.execute("DELETE FROM badges WHERE language = ?", (language,))
            self._conn.execute("DELETE FROM activity_log WHERE language = ?", (language,))
            self._conn.execute("DELETE FROM quiz_attempts WHERE language = ?", (language,))
            self._conn.execute("DELETE FROM daily_refresher_picks WHERE language = ?", (language,))
            self._conn.execute("DELETE FROM quiz_answers WHERE language = ?", (language,))
            self._conn.execute("DELETE FROM exercise_notes WHERE language = ?", (language,))
            self._conn.execute("DELETE FROM bookmarks WHERE language = ?", (language,))
            self._conn.execute("DELETE FROM review_schedule WHERE language = ?", (language,))
            self._conn.execute("DELETE FROM solve_times WHERE language = ?", (language,))
            self._conn.execute(
                "UPDATE profile SET current_exercise_id = NULL, streak_days = 0, last_played_date = NULL, "
                "freeze_tokens = 0 WHERE language = ?",
                (language,),
            )
            self._conn.execute("UPDATE player_xp SET total_xp = 0 WHERE language = ?", (language,))

    # -- Export / Import -------------------------------------------------
    def export_progress(self) -> dict:
        """Serializes every progress table, across every language track,
        into a plain JSON-safe dict -- the Settings screen's Export
        Progress feature is a full backup/restore, not scoped to just the
        currently-selected track, so switching tracks later never loses
        what a restore brought back."""
        tables: dict[str, list[dict]] = {}
        with closing(self._row_cursor()) as cur:
            for table in _EXPORT_TABLES:
                cur.execute(f"SELECT * FROM {table}")
                tables[table] = [dict(row) for row in cur.fetchall()]
        return {"version": PROGRESS_EXPORT_VERSION, "exported_at": _now(), "tables": tables}

    def _table_columns(self, table: str) -> set[str]:
        with closing(self._conn.cursor()) as cur:
            cur.execute(f"PRAGMA table_info({table})")
            return {row[1] for row in cur.fetchall()}

    def import_progress(self, data: dict) -> None:
        """Replaces EVERY progress table with the given export's data, for
        EVERY language track -- a full overwrite, not a merge. The caller
        (the Settings screen) is responsible for confirming with the user
        first, since whatever progress currently exists is discarded the
        moment this runs, and there's no undo once it does. Runs as one
        transaction: if anything here fails, SQLite rolls the whole import
        back rather than leaving some tables overwritten and others not.

        The file is user-supplied, so nothing from it reaches SQL text
        unchecked: table names come from our own _EXPORT_TABLES list and
        every column name is validated against the live schema before it
        is interpolated. Values are always bound parameters.
        """
        if not isinstance(data, dict):
            raise ValueError("Can't import this file -- expected a JSON object at the top level.")
        version = data.get("version")
        if version != PROGRESS_EXPORT_VERSION:
            raise ValueError(
                f"Can't import this file -- it was exported by a different, incompatible "
                f"version of this app (got version {version!r}, expected {PROGRESS_EXPORT_VERSION})."
            )
        tables = data.get("tables", {})
        if not isinstance(tables, dict):
            raise ValueError("Can't import this file -- `tables` must be a JSON object.")
        unknown_tables = sorted(set(tables) - set(_EXPORT_TABLES))
        if unknown_tables:
            raise ValueError(f"Can't import this file -- it contains unknown tables {unknown_tables}.")

        schema = {table: self._table_columns(table) for table in _EXPORT_TABLES}
        with self._conn:
            for table in _EXPORT_TABLES:
                self._conn.execute(f"DELETE FROM {table}")
            for table in _EXPORT_TABLES:
                rows = tables.get(table, [])
                if not isinstance(rows, list):
                    raise ValueError(f"Can't import this file -- `tables.{table}` must be a list of rows.")
                for row in rows:
                    if not isinstance(row, dict):
                        raise ValueError(f"Can't import this file -- a row in `{table}` isn't a JSON object.")
                    columns = list(row.keys())
                    bad = sorted(set(columns) - schema[table])
                    if bad:
                        raise ValueError(
                            f"Can't import this file -- table `{table}` has columns {bad} this app "
                            f"doesn't know (expected a subset of {sorted(schema[table])})."
                        )
                    placeholders = ", ".join("?" for _ in columns)
                    self._conn.execute(
                        f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})",
                        [row[c] for c in columns],
                    )
        logger.info("Imported progress export from %s", data.get("exported_at"))
