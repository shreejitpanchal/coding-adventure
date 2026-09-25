from datetime import date

from app.config.clock import days_ago_iso, days_between, today, today_iso


def test_days_between():
    assert days_between("2026-01-01", "2026-01-02") == 1
    assert days_between("2026-01-02", "2026-01-01") == -1
    assert days_between("2025-12-31", "2026-01-01") == 1


def test_today_is_local_date():
    assert today() == date.fromisoformat(today_iso())


def test_days_ago_iso():
    assert days_between(days_ago_iso(3), today_iso()) == 3
