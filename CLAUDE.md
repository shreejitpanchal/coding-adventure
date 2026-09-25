# CLAUDE.md

Guidance for Claude Code when working in this repository. This file holds
the conventions that apply to every task. The mechanics of each subsystem
live in [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) and the design in
[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md); read the relevant section
there before extending a subsystem, and update it in the same change.

## What this is

"Coding Adventure" is an offline, Flet-only desktop app: a coding
refresher for **professionals**, not beginners. Seven tracks (Python,
Java, C++, Spring, Node.js, AI, Architecture), picked from a language
picker shown on **every** launch by design. Exercises run the user's own
code with the real local toolchain; the framing is crash-containment,
never a safety sandbox.

## Commands

Run from the repo root with the project venv (`.venv\Scripts\python.exe`,
created by `run_app_window_mode.bat`/`.sh` on first launch).

```powershell
.venv\Scripts\python.exe main.py            # desktop window
.venv\Scripts\python.exe main_web.py        # browser preview (needs requirements-web.txt)

.\scripts\dev.ps1 all                       # lint + test + coverage  (bash: scripts/dev.sh all)
.\scripts\dev.ps1 test                      # pytest only
.\scripts\dev.ps1 content                   # content-lint tests only
.venv\Scripts\python.exe -m pytest tests\test_lesson_engine.py::test_name -v
```

Linting is `ruff check` with the rule set in `pyproject.toml`; there is
no formatter. Developer tools come from `requirements-dev.txt`. Do not
run the gates yourself -- ask the user to run `.\scripts\dev.ps1 all`
and read `scripts\logs\*.log`.

## Architecture in one screen

- **Content is data.** One YAML file per exercise under
  `content/<language>/lessons/`; quiz banks in `content/<language>/quiz/`.
  Adding or changing an exercise never touches app code. User-added
  content overlays from `data/custom/<language>/lessons/`. All content is
  validated at load time (`app/engine/content_loader.py`,
  `Exercise.__post_init__`) and by `tests/test_content_lint.py`.
- **Engines.** `app/engine/` loads content and holds every decision that
  is not rendering: unlock rules, daily refresher, search,
  `run_evaluation.evaluate_run()` (pass/fail as a pure function).
- **Execution.** `app/execution/` has one `ExecutionEngine` per language
  on top of `base.run_subprocess()`. `registry.py` exposes factories;
  `AppState.execution_engine()` owns the instances. `ai` reuses Python's
  engine class; `architecture` has none (every exercise is
  `requires_code: false` and completes via a comprehension check).
- **Progress.** `app/progress/store.py` is SQLite, every table keyed by
  `language`. Timestamps are UTC; calendar days ("played today", daily
  picks, heatmap) are the user's local date via `app/config/clock.py`.
  Streaks are recorded only on completion, never on opening a screen;
  a freeze token (earned every 7 days, max 3) bridges one missed day.
  Schema additions to existing tables go through `_COLUMN_MIGRATIONS`.
  Passed exercises enter a spaced-repetition schedule
  (`review_schedule`, `schedule_review()`); a failed attempt counts
  against it only if the exercise was already completed before.
- **UI.** `app/ui/app_window.py` is a route table that rebuilds exactly
  one view per navigation and clears page-level handlers first.
  `AppState` is threaded explicitly into every view builder -- no module
  globals. Shared widgets (buttons, cards, hero banners, nav tiles,
  chips, rings, `MultipleChoiceCard`) live in `app/ui/components.py`;
  animation helpers (`Stagger`, `hover_lift`, `pop_in`, `Pulser`,
  `count_up`, `confetti`) in `app/ui/motion.py`. Use them instead of
  inline `ft.ButtonStyle(...)` or hand-rolled animations. Colours come
  only from the `ThemePreset` (plus `LanguageInfo.color` /
  `CATEGORY_META.color`).
- **Config.** `app/config/paths.py` is the single definition of the repo
  layout; `logging_setup.py` writes `data/logs/app.log`; `settings.py`
  quarantines a corrupt settings file instead of silently resetting.

## Conventions for changes

- **Adding a screen**: one module in `app/ui/` plus one line in
  `app_window.py`'s route table. Build it from `components.py`.
- **Adding a language**: follow the `add-language-content` skill; it is
  content + one engine + one `ENGINE_FACTORIES` entry + a
  `toolchain_check` entry + `CATEGORY_META` entries.
- **Adding content**: run `.\scripts\dev.ps1 content`. Category levels
  must run 1..N without gaps; code exercises need `expected_output` or
  `expected_output_pattern`; conceptual ones need at least two
  four-option questions.
- **Errors**: say what failed, which file/value, and what to do. Content
  errors must carry the file path (`ContentError`). Never let a
  structural problem surface as an `IndexError` at click time.
- **Tests**: mirror the source layout; cover what you touch, including
  the error path. Do not assert exact content counts -- assert
  invariants (see `test_content_lint.py`).
- **Docs**: behaviour changes update `docs/DEVELOPMENT.md` (mechanics)
  and, if a design rule changed, `docs/ARCHITECTURE.md` §7. Keep this
  file to conventions and pointers.
- **Dependencies**: runtime pins in `requirements.txt`, dev pins in
  `requirements-dev.txt`, web-preview pins in `requirements-web.txt`,
  loose specs in `pyproject.toml`. A bump is its own change.
- **Knowledge graph**: `graphify-out/` exists. Query it before grepping
  for cross-file questions; after code changes ask the user to run
  `python -m graphify update .` (never rebuild to answer a question).

## Product decisions that look like bugs but are not

- The language picker is shown on every launch; `last_selected_language`
  only pre-highlights a card.
- `ai` and `architecture` are fully unlocked from the start
  (`ALWAYS_UNLOCKED_LANGUAGES`). Java/C++/Spring/Node are fully unlocked
  on Android only, because they can never run there.
- Progress lives in a project-local `data/` folder on desktop (the app
  runs from a checkout), and in `FLET_APP_STORAGE_DATA` on Android.
- Spring exercises validate against the synthetic stdout
  `"BUILD SUCCESS"`; Maven's real summary is non-deterministic.
