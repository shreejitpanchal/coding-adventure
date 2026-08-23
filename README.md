# Coding Adventure

A focused, offline coding refresher for working professionals — Python,
Java, C++, and Spring. One desktop app, no accounts, no cloud, nothing to
sign up for.

## Who it's for

Developers who already know how to code and want to keep their instincts
sharp: real-world gotchas, idioms, and standard-library depth to work
through in a few focused minutes, not tutorials to sit through.

## What's inside

- **Language picker** — every session starts by choosing a track. Python
  and Java are fully built out; C++ and Spring are visible as "coming
  soon" so the shape of the app doesn't change as they're added. A track
  whose local toolchain isn't installed (e.g. no JDK) shows "Toolchain
  needed" with an install hint instead of pretending it's ready.
- **Daily Refresher** — a short, five-exercise round-robin across every
  topic, so a quick daily session naturally touches everything instead of
  grinding one category at a time.
- **Practice by Topic**:
  - **Python** — 14 categories, 75 exercises: Idioms & Gotchas, Core
    Language Refresher, Data Structures & Algorithms, Standard Library
    Deep Dive, Concurrency & Async, Thread Scheduling, Sync vs Async,
    Functional Programming, Recursion, Dependency Management, Packaging,
    Deployment, Observability, and the flagship **Gotcha Gauntlet**.
  - **Java** — 6 categories, 30 exercises: Idioms & Gotchas, Core
    Language Refresher (streams, lambdas, records, try-with-resources),
    the Collections Framework, Standard Library Deep Dive, Concurrency
    (synchronized, ExecutorService, CompletableFuture), and its own
    **Gotcha Gauntlet** (off-by-one, switch fallthrough,
    ConcurrentModificationException, silent int overflow, the
    equals()/hashCode() contract).
- **Quiz Bank** — 87 Python questions, 35 Java questions, reshuffled
  every session.
- **Progress** — per-track XP, levels, streaks, mastery-by-topic, and
  achievements. Every language track keeps its own independent progress.
- **Real execution, not a simulated sandbox** — Python exercises run
  against your actual local `python` interpreter; Java exercises are
  compiled with `javac` and run with `java`, both in an isolated
  subprocess with a timeout.
- **100% offline and private** — everything runs and stays on your
  machine. No accounts, no network access, no data collection.

C++ and Spring have their execution-engine interfaces defined and
content directories scaffolded (`content/cpp`, `content/spring`), ready
to fill in — see `app/execution/cpp_engine.py` and `spring_engine.py`
for what's left to implement.

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
- `app/execution/` — one `ExecutionEngine` per language.
  `python_engine.py` and `java_engine.py` are implemented; `cpp_engine.py`
  and `spring_engine.py` define the interface and raise
  `NotImplementedError` until built out.
- `app/progress/` — SQLite-backed XP/streaks/badges/activity log, keyed
  per language track.
- `app/ui/` — Flet screens.
- `content/<language>/lessons/*.yaml` — one exercise per file; adding or
  changing one never requires touching app code.
