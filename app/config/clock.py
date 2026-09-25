"""Calendar-day helpers.

Two different notions of "now" exist in this app and they are kept apart
on purpose:

- **Timestamps** (activity log rows, completion times, badge dates) are
  stored as timezone-aware UTC ISO strings via ProgressStore's `_now()`.
  They sort lexicographically and never shift when the user travels.
- **Calendar days** -- "did you play *today*", "today's Daily Refresher
  set" -- follow the user's local clock. A streak that flipped at 08:00
  local time because the server-style UTC day rolled over was the bug
  this module exists to remove.

Everything that needs a day boundary calls `today_iso()`; nothing else
in the app should call `date.today()` or `datetime.now(...).date()`
directly, so the choice lives in exactly one place."""
from __future__ import annotations

from datetime import date, datetime, timedelta


def today() -> date:
    """The user's local calendar date."""
    return datetime.now().astimezone().date()


def today_iso() -> str:
    return today().isoformat()


def days_between(earlier_iso: str, later_iso: str) -> int:
    """Whole days from one ISO date to another (negative if reversed)."""
    return (date.fromisoformat(later_iso) - date.fromisoformat(earlier_iso)).days


def days_ago_iso(days: int) -> str:
    return (today() - timedelta(days=days)).isoformat()
