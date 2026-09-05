"""SQLite-backed progress, gamification, and activity tracking -- one
XP/streak/level per language track, since a "professional" here is
plausibly juggling more than one track at once."""
from __future__ import annotations

import sqlite3
from contextlib import closing
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

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
"""

# Bumped only if a future schema change makes an old export incompatible
# with import_progress()'s column-list assumptions.
PROGRESS_EXPORT_VERSION = 1

_EXPORT_TABLES = [
    "profile", "lesson_completions", "badges", "activity_log",
    "quiz_attempts", "player_xp", "daily_refresher_picks",
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

    def record_play_today(self, language: str) -> None:
        self._ensure_profile(language)
        today = datetime.now(timezone.utc).date().isoformat()
        with closing(self._conn.cursor()) as cur:
            cur.execute("SELECT last_played_date, streak_days FROM profile WHERE language = ?", (language,))
            last_played, streak = cur.fetchone()
        if last_played == today:
            return
        if last_played is not None:
            gap_days = (
                datetime.fromisoformat(today) - datetime.fromisoformat(last_played)
            ).days
            streak = streak + 1 if gap_days == 1 else 1
        else:
            streak = 1
        with self._conn:
            self._conn.execute(
                "UPDATE profile SET last_played_date = ?, streak_days = ? WHERE language = ?",
                (today, streak, language),
            )

    def get_streak_days(self, language: str) -> int:
        with closing(self._conn.cursor()) as cur:
            cur.execute("SELECT streak_days FROM profile WHERE language = ?", (language,))
            row = cur.fetchone()
            return row[0] if row else 0

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

    def get_activity_since(self, language: str, cutoff_iso: str) -> list[sqlite3.Row]:
        conn = self._conn
        conn.row_factory = sqlite3.Row
        with closing(conn.cursor()) as cur:
            cur.execute(
                "SELECT * FROM activity_log WHERE language = ? AND timestamp >= ? ORDER BY id DESC",
                (language, cutoff_iso),
            )
            rows = cur.fetchall()
        conn.row_factory = None
        return rows

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

    # -- Reset ---------------------------------------------------------
    def reset_progress(self, language: str) -> None:
        with self._conn:
            self._conn.execute("DELETE FROM lesson_completions WHERE language = ?", (language,))
            self._conn.execute("DELETE FROM badges WHERE language = ?", (language,))
            self._conn.execute("DELETE FROM activity_log WHERE language = ?", (language,))
            self._conn.execute("DELETE FROM quiz_attempts WHERE language = ?", (language,))
            self._conn.execute("DELETE FROM daily_refresher_picks WHERE language = ?", (language,))
            self._conn.execute(
                "UPDATE profile SET current_exercise_id = NULL, streak_days = 0, last_played_date = NULL "
                "WHERE language = ?",
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
        conn = self._conn
        conn.row_factory = sqlite3.Row
        try:
            tables: dict[str, list[dict]] = {}
            with closing(conn.cursor()) as cur:
                for table in _EXPORT_TABLES:
                    cur.execute(f"SELECT * FROM {table}")
                    tables[table] = [dict(row) for row in cur.fetchall()]
        finally:
            conn.row_factory = None
        return {"version": PROGRESS_EXPORT_VERSION, "exported_at": _now(), "tables": tables}

    def import_progress(self, data: dict) -> None:
        """Replaces EVERY progress table with the given export's data, for
        EVERY language track -- a full overwrite, not a merge. The caller
        (the Settings screen) is responsible for confirming with the user
        first, since whatever progress currently exists is discarded the
        moment this runs, and there's no undo once it does. Runs as one
        transaction: if anything here fails, SQLite rolls the whole import
        back rather than leaving some tables overwritten and others not.
        """
        version = data.get("version")
        if version != PROGRESS_EXPORT_VERSION:
            raise ValueError(
                f"Can't import this file -- it was exported by a different, incompatible "
                f"version of this app (got version {version!r}, expected {PROGRESS_EXPORT_VERSION})."
            )
        tables = data.get("tables", {})
        with self._conn:
            for table in _EXPORT_TABLES:
                self._conn.execute(f"DELETE FROM {table}")
            for table in _EXPORT_TABLES:
                for row in tables.get(table, []):
                    columns = list(row.keys())
                    placeholders = ", ".join("?" for _ in columns)
                    self._conn.execute(
                        f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})",
                        [row[c] for c in columns],
                    )
