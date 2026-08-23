# Coding Adventure

A focused, offline coding refresher for working professionals — Python,
Java, C++, and Spring. One desktop app, no accounts, no cloud, nothing to
sign up for.

## Who it's for

Developers who already know how to code and want to keep their instincts
sharp: real-world gotchas, idioms, and standard-library depth to work
through in a few focused minutes, not tutorials to sit through.

## What's inside (Python track — fully built)

- **Language picker** — every session starts by choosing a track. Python
  is fully built out; Java, C++, and Spring are visible as "coming soon"
  so the shape of the app doesn't change as they're added.
- **Daily Refresher** — a short, five-exercise round-robin across every
  topic, so a quick daily session naturally touches everything instead of
  grinding one category at a time.
- **Practice by Topic** — six categories, ~35 exercises: Idioms & Gotchas,
  Core Language Refresher, Data Structures & Algorithms, Standard Library
  Deep Dive, Concurrency & Async, and the flagship **Gotcha Gauntlet** —
  senior-engineer-trap debugging puzzles (mutable defaults, race
  conditions, float precision, silent exception swallowing, and more).
- **Quiz Bank** — 50 multiple-choice questions, reshuffled every session.
- **Progress** — per-track XP, levels, streaks, mastery-by-topic, and
  achievements. Every language track keeps its own independent progress.
- **Real execution** — Python exercises run against your actual local
  `python` interpreter in an isolated subprocess with a timeout, not a
  simulated sandbox.
- **100% offline and private** — everything runs and stays on your
  machine. No accounts, no network access, no data collection.

Java, C++, and Spring have their execution-engine interfaces defined and
content directories scaffolded (`content/java`, `content/cpp`,
`content/spring`), ready to fill in — see `app/execution/java_engine.py`,
`cpp_engine.py`, and `spring_engine.py` for what's left to implement.

## Getting started

**Easiest way (no terminal needed):** double-click `run.bat` (Windows) or
run `./run.sh` (git-bash/macOS/Linux). The first run takes a minute to set
itself up; every run after that launches straight into the app.

## For developers

```powershell
# Run the app
.venv\Scripts\python.exe main.py

# Full test suite
.venv\Scripts\python.exe -m pytest tests\ -v
```

- `app/engine/` — content model (`Exercise`, `QuizQuestion`), YAML
  loaders, category/unlock logic.
- `app/execution/` — one `ExecutionEngine` per language. Only
  `python_engine.py` is implemented; the others define the interface and
  raise `NotImplementedError` until built out.
- `app/progress/` — SQLite-backed XP/streaks/badges/activity log, keyed
  per language track.
- `app/ui/` — Flet screens.
- `content/<language>/lessons/*.yaml` — one exercise per file; adding or
  changing one never requires touching app code.
