# Coding Adventure

A focused, offline coding refresher for working professionals — Python,
Java, C++, and Spring. One desktop app, no accounts, no cloud, nothing to
sign up for.

## Who it's for

Developers who already know how to code and want to keep their instincts
sharp: real-world gotchas, idioms, and standard-library depth to work
through in a few focused minutes, not tutorials to sit through.

## What's inside

- **Language picker** — every session starts by choosing a track. Python,
  Java, and C++ are fully built out; Spring is visible as "coming soon"
  so the shape of the app doesn't change as it's added. A track whose
  local toolchain isn't installed (e.g. no JDK, no g++) shows "Toolchain
  needed" with an install hint instead of pretending it's ready.
- **Daily Refresher** — a short, five-exercise round-robin across every
  topic, so a quick daily session naturally touches everything instead of
  grinding one category at a time.
- **Practice by Topic** — Python and Java both cover the same 14
  categories, so switching tracks doesn't change the shape of the app:
  Idioms & Gotchas, Core Language Refresher, Data Structures &
  Algorithms, Standard Library Deep Dive, Concurrency & Async, Thread
  Scheduling, Sync vs Async, Functional Programming, Recursion,
  Dependency Management, Packaging, Deployment, Observability, and the
  flagship **Gotcha Gauntlet**. C++ covers its own 6 categories (a
  general-purpose-language subset, not framework-specific): Idioms &
  Gotchas, Core Language Refresher, Data Structures, Standard Library
  Deep Dive, Concurrency & Async, and Gotcha Gauntlet.
  - **Python** — 75 exercises (mutable defaults, race conditions, float
    precision, silent exception swallowing, GIL vs true parallelism, and
    more).
  - **Java** — 70 exercises, each idiomatically Java rather than a
    literal port (streams/lambdas/records, the Collections Framework,
    virtual threads and CompletableFuture for concurrency,
    ConcurrentModificationException, silent int overflow, the
    equals()/hashCode() contract, and more).
  - **C++** — 30 exercises (integer division/overflow, pass-by-value vs
    pass-by-reference, unsigned wraparound, RAII/smart pointers, STL
    containers and algorithms, std::thread/mutex/atomic/async, missing
    virtual destructors, and more).
- **Quiz Bank** — 87 Python questions, 70 Java questions, 35 C++
  questions, reshuffled every session.
- **Progress** — per-track XP, levels, streaks, mastery-by-topic, and
  achievements. Every language track keeps its own independent progress.
- **Real execution, not a simulated sandbox** — Python exercises run
  against your actual local `python` interpreter; Java exercises are
  compiled with `javac` and run with `java`; C++ exercises are compiled
  with `g++` and run as a native binary — all three in an isolated
  subprocess with a timeout.
- **100% offline and private** — everything runs and stays on your
  machine. No accounts, no network access, no data collection.

Spring has its execution-engine interface defined and a content
directory scaffolded (`content/spring`), ready to fill in — see
`app/execution/spring_engine.py` for what's left to implement (a
scaffolded Maven project per exercise, run via `mvn test`, rather than a
single-file compile-and-run).

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
  `python_engine.py`, `java_engine.py`, and `cpp_engine.py` are
  implemented; `spring_engine.py` defines the interface and raises
  `NotImplementedError` until built out.
- `app/progress/` — SQLite-backed XP/streaks/badges/activity log, keyed
  per language track.
- `app/ui/` — Flet screens.
- `content/<language>/lessons/*.yaml` — one exercise per file; adding or
  changing one never requires touching app code.

For a deeper dive:

- [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) — project layout, how each
  subsystem works, running it/testing it.
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — system context, class
  diagrams, sequence diagrams, the persistence model, and the design
  decisions behind them.
