---
description: Run the full test suite and a quick Flet launch sanity check.
---

Run these checks, in order, and report the results:

1. Full pytest suite:
   ```
   .venv\Scripts\python.exe -m pytest tests\ -v
   ```
   This repo has no linter/formatter configured — don't invent one. If
   anything fails, investigate and fix the root cause rather than skipping
   or loosening the failing test. Execution-engine tests for a language
   whose local toolchain (`javac`/`java`, `g++`) isn't on PATH are skipped
   automatically (`pytest.mark.skipif`) rather than failing — that's
   expected, not a problem to fix.

2. Quick launch sanity check (this app is Flet-only — no CustomTkinter
   dual-stack to check separately):
   ```
   timeout 8 .venv\Scripts\python.exe main.py
   ```
   Should open without raising. A few seconds is enough to confirm the
   language picker renders, then stop it.

If exercise YAML content changed, also spot-check that the affected
language's exercise/quiz counts in `tests/test_lesson_engine.py` match
what's actually on disk (`test_loads_<language>_content`) — a stale count
assertion passes silently wrong if content was added without updating it.
