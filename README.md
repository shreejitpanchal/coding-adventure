# Coding Adventure

A focused, offline coding refresher for working professionals — Python,
Java, C++, and Spring, all four fully built out. One desktop app, no
accounts, no cloud, nothing to sign up for.

## Who it's for

Developers who already know how to code and want to keep their instincts
sharp: real-world gotchas, idioms, and standard-library depth to work
through in a few focused minutes, not tutorials to sit through.

## What's inside

- **Language picker** — every session starts by choosing a track. All
  four tracks (Python, Java, C++, Spring) are fully built out. A track
  whose local toolchain isn't installed (e.g. no JDK, no g++, no Maven)
  shows "Toolchain needed" with an install hint instead of pretending
  it's ready.
- **Daily Refresher** — a short, five-exercise round-robin across every
  topic, so a quick daily session naturally touches everything instead of
  grinding one category at a time.
- **Practice by Topic** — Python and Java both cover the same 14
  categories, so switching tracks doesn't change the shape of the app:
  Idioms & Gotchas, Core Language Refresher, Data Structures &
  Algorithms, Standard Library Deep Dive, Concurrency & Async, Thread
  Scheduling, Sync vs Async, Functional Programming, Recursion,
  Dependency Management, Packaging, Deployment, Observability, and the
  flagship **Gotcha Gauntlet**. C++ and Spring each define their own
  smaller category sets instead, since chasing full 14-category parity
  doesn't fit a bare language or a DI framework the same way it fits two
  general-purpose languages: C++ covers 10 (the same 6 as before plus
  Thread Scheduling, Sync vs Async, Functional Programming, and
  Recursion — categories that genuinely fit a single compiled file, unlike
  packaging/deployment/observability which assume a package manager or
  framework C++ doesn't have here), Spring covers 6 (Dependency
  Injection, Bean Lifecycle & Scopes, Configuration & Profiles,
  Application Events, Aspect-Oriented Programming, and Resilience
  Patterns).
  - **Python** — 75 exercises (mutable defaults, race conditions, float
    precision, silent exception swallowing, GIL vs true parallelism, and
    more).
  - **Java** — 70 exercises, each idiomatically Java rather than a
    literal port (streams/lambdas/records, the Collections Framework,
    virtual threads and CompletableFuture for concurrency,
    ConcurrentModificationException, silent int overflow, the
    equals()/hashCode() contract, and more).
  - **C++** — 50 exercises (integer division/overflow, pass-by-value vs
    pass-by-reference, unsigned wraparound, RAII/smart pointers, STL
    containers and algorithms, std::thread/mutex/atomic/async, missing
    virtual destructors, sleep_for/yield/condition_variable scheduling,
    future/shared_future/launch-policy sync-vs-async gotchas, lambda
    closures and std::transform/accumulate, memoization and mutual
    recursion, and more).
  - **Spring** — 30 exercises (constructor vs field injection, ambiguous
    beans and @Qualifier/@Primary, singleton vs prototype scope,
    @PostConstruct/@PreDestroy, @Lazy, @Value placeholder resolution,
    @Profile-gated beans, ApplicationEvent/@EventListener including
    conditional SpEL listeners, Spring AOP's @Before/@AfterReturning/
    @Around advice including the classic self-invocation-bypasses-the-
    proxy gotcha, and Resilience4j's CircuitBreaker/Retry/RateLimiter/
    fallback decorators including the non-obvious decoration-order gotcha
    when combining a circuit breaker with a retry, and more), using plain
    Spring Framework (spring-context/spring-test/spring-aop/
    resilience4j-all) rather than Spring Boot, so `mvn test` stays fast
    and fully offline after the shared scaffold's dependencies are
    warmed once.
- **Quiz Bank** — 87 Python questions, 70 Java questions, 55 C++
  questions, 44 Spring questions, reshuffled every session.
- **Progress** — per-track XP, levels, streaks, mastery-by-topic, and
  achievements. Every language track keeps its own independent progress.
- **Real execution, not a simulated sandbox** — Python exercises run
  against your actual local `python` interpreter; Java exercises are
  compiled with `javac` and run with `java`; C++ exercises are compiled
  with `g++` and run as a native binary; Spring exercises run against a
  scaffolded Maven project via `mvn test` — all in an isolated subprocess
  with a timeout.
- **100% offline and private** — everything runs and stays on your
  machine. No accounts, no network access (beyond the one-time Maven
  dependency download for the Spring track), no data collection.

## Getting started

**Easiest way (no terminal needed):** double-click `run_app_window_mode.bat`
(Windows) or run `./run_app_window_mode.sh` (git-bash/macOS/Linux). The
first run takes a minute to set itself up; every run after that launches
straight into the native desktop window.

**Browser preview:** `run_app_web_ui.bat` / `./run_app_web_ui.sh` launches
the same UI in your default browser instead of a native window — handy for
a quick look at the screens without a desktop window, e.g. from a machine
without a display server, or just to poke around in Chrome. It's a
one-off preview only, not a supported way to actually run exercises: the
app is desktop-only by design (see [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md#why-no-android-build)) since
running code needs a real local compiler/interpreter subprocess a browser
sandbox can't provide. The script prints the port it started on
(`http://localhost:8550` by default); to use a different port, set
`CODING_ADVENTURE_WEB_PORT` before running it:

```powershell
# Windows (PowerShell)
$env:CODING_ADVENTURE_WEB_PORT = "9000"
run_app_web_ui.bat
```

```bash
# git-bash/macOS/Linux
CODING_ADVENTURE_WEB_PORT=9000 ./run_app_web_ui.sh
```

## For developers

```powershell
# Run the app (native desktop window)
.venv\Scripts\python.exe main.py

# Run the app (browser preview, default port 8550)
.venv\Scripts\python.exe main_web.py

# Full test suite
.venv\Scripts\python.exe -m pytest tests\ -v
```

- `app/engine/` — content model (`Exercise`, `QuizQuestion`), YAML
  loaders, category/unlock logic.
- `app/execution/` — one `ExecutionEngine` per language, all four
  implemented (`python_engine.py`, `java_engine.py`, `cpp_engine.py`,
  `spring_engine.py`).
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
