# Coding Adventure

A focused, offline coding refresher for working professionals — Python,
Java, C++, Spring, Node.js, AI, and Architecture, all seven fully built
out. One desktop app, no accounts, no cloud, nothing to sign up for.

## Who it's for

Developers who already know how to code and want to keep their instincts
sharp: real-world gotchas, idioms, and standard-library depth to work
through in a few focused minutes, not tutorials to sit through.

## What's inside

- **Language picker** — every session starts by choosing a track. All
  seven tracks (Python, Java, C++, Spring, Node.js, AI, Architecture) are
  fully built out. A track whose local toolchain isn't installed (e.g. no
  JDK, no g++, no Maven, no Node.js) shows "Toolchain needed" with an
  install hint instead of pretending it's ready. AI runs on the same
  Python interpreter as the Python track (no extra toolchain needed);
  Architecture needs no toolchain at all, since none of its exercises run
  code. A summary strip above the cards shows your total XP and best
  streak across every track, plus a "Continue where you left off" link
  straight back into whichever exercise you were last viewing.
- **Daily Refresher** — a short round-robin across every topic (five
  exercises by default, adjustable in Settings), so a quick daily session
  naturally touches everything instead of grinding one category at a
  time. One slot goes to the most overdue item from the Review Queue
  when something is due.
- **Weekly goal and streak freezes** — set how many exercises you want
  per week; the hub shows your count. Every 7-day streak earns a freeze
  (hold up to three) that is spent automatically to cover one missed
  day, so a single busy day doesn't erase months of habit.
- **Personal bests** — every pass is timed from opening the exercise;
  the reward card shows your time against your best, and lists show a
  "Best 1m 35s" chip per exercise.
- **Keyboard-first** — Ctrl+Enter runs, Ctrl+H hints, 1-4 answer quiz
  questions, digits open hub tiles, Esc goes back everywhere. Each
  screen shows its own shortcuts in a small help line.
- **Recurring errors** — the Progress screen groups your failed runs of
  the last 30 days by cause ("Null reference", "Index out of range")
  and offers a practice exercise for each.
- **Review Queue** — spaced repetition. Every exercise you pass comes
  back on a growing schedule (3 days, then a week, then longer each time
  you still get it right; a miss brings it back tomorrow). The hub tile
  shows what's due now and what's coming this week.
- **Search** — find any exercise by title, objective, or concept
  ("closures", "race conditions"), filterable by difficulty, once a
  track has hundreds of exercises spread across many categories.
- **Practice by Topic** — Java and Python both cover the original 14
  categories: Idioms & Gotchas, Core Language Refresher, Data Structures
  & Algorithms, Standard Library Deep Dive, Concurrency & Async, Thread
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
  Patterns), and Node.js covers 12 (the same 6 as C++ — Idioms & Gotchas,
  Core Language Refresher, Data Structures, Standard Library Deep Dive,
  Concurrency & Async, Gotcha Gauntlet — plus Dependency Management,
  Sync vs Async, Functional Programming, Recursion, Observability, and
  Deployment, since JavaScript is a general-purpose, package-manager-
  heavy ecosystem language like Python/Java, not a bare compiled
  language the way C++ is here). **AI** and **Architecture** are their
  own dedicated tracks with their own category sets entirely — see below.
  - **Python** — 455 exercises: the seven broad categories (Idioms &
    Gotchas, Core Language Refresher, Data Structures & Algorithms,
    Standard Library Deep Dive, Gotcha Gauntlet, Concurrency & Async,
    Functional Programming) at 50 exercises each, and the seven narrower
    categories (Packaging, Deployment, Observability, Dependency
    Management, Thread Scheduling, Sync vs Async, Recursion) at 15 each
    (mutable defaults, race conditions, float precision, silent exception
    swallowing, GIL vs true parallelism, and far more).
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
  - **Node.js** — 60 exercises (loose vs. strict equality, `var`'s
    function-scoped closures, floating-point precision, detached-method
    `this` binding, destructuring/spread/optional chaining, `Map`/`Set`
    vs. plain objects, `filter`/`map`/`reduce` pipelines, the
    microtask/macrotask event-loop ordering behind `Promise` vs.
    `setTimeout`, `process.nextTick`'s queue-jumping priority,
    `Promise.all` vs. `allSettled`, sequential `await` in a loop vs.
    concurrent `Promise.all`, `for await...of` over async generators,
    semver/`package.json`/`package-lock.json` version resolution,
    closures for private state, `pipe()` composition, `Object.freeze`'s
    silent-failure mutation, partial application via `bind()`, recursion
    without tail-call optimization (V8 never implemented it), memoized
    Fibonacci, `AsyncLocalStorage` for correlation IDs, structured JSON
    logging, `process.env`'s string-only typing, graceful `SIGTERM`
    shutdown, and more), run directly with `node` (no separate compile
    step, unlike Java/C++).
  - **AI** — 405 exercises across 9 categories (ML Fundamentals,
    Retrieval-Augmented Generation, Agentic Frameworks, Model Context
    Protocol, Microsoft Agent 365, LangChain, LangGraph, LangSmith,
    Solace Agent Mesh — 50 exercises each except Microsoft Agent 365's
    5) — hand-rolled, dependency-free Python covering
    reproducible train/test splits, data leakage, gradient descent's
    sign convention, cosine similarity vs. raw dot product, chunk
    overlap, prompt templating, tool-dispatch loops with max-iteration
    guards, conversation-memory windows, JSON-RPC's message shape,
    request/response correlation, Runnable composition and
    RunnableParallel merges, prompt templates and JSON output parsing, a
    graph executor with conditional edges and cycles, checkpointing,
    span-tree tracing, run status logging, regression detection between
    evaluation runs, entrypoint payload translation, agent-card
    capability matching, hierarchical topic-based message delivery, an
    agent reasoning loop that threads tool results back in, and
    isolating one misbehaving tool from crashing an entire batch — kept
    fully offline and deterministic like every other exercise in the
    app, with no network calls, API keys, or ML/framework libraries
    required. Executes on the exact same Python interpreter as the
    Python track. Microsoft Agent 365's category is the one exception
    with no code to run at all -- it covers Microsoft's AI Agent Control
    Tower (agent identity, access, observability, lifecycle governance)
    as an inline comprehension check instead, the same shape as the
    Architecture track below.
  - **Architecture** — 50 exercises across 10 categories (Event-Driven
    Architecture, Microservices, CQRS, Saga Pattern, Strangler Fig,
    Domain-Driven Design, Hexagonal Architecture, API Gateway, Circuit
    Breaker, Idempotency), 5 exercises each running low-to-high-level
    within a topic — e.g. Circuit Breaker goes from the core
    open/closed/half-open state machine through fallback strategies,
    bulkheads, and threshold tuning, before closing on a deliberate "when
    this pattern is overkill" lesson. This is the one track with no code
    to run at all — every exercise instead gates completion on an inline
    multiple-choice comprehension check, and every category and level is
    unlocked from the start.
- **Quiz Bank** — 87 Python questions, 70 Java questions, 55 C++
  questions, 44 Spring questions, 63 Node.js questions, 45 AI questions,
  and 20 Architecture questions, reshuffled every session.
- **Progress** — per-track XP, levels, streaks, mastery-by-topic,
  achievements, a 12-week activity heatmap, and a "Weakest concepts"
  panel built from your actual quiz answer history (each with a direct
  "Practice" link). Achievements include per-exercise ones plus
  cross-cutting meta-achievements (a streak milestone, a fully-completed
  category, a perfect quiz, your first-ever completion). Every language
  track keeps its own independent progress.
- **Notes and bookmarks** — jot a note on any exercise, or bookmark one
  to "Revisit later" from the track hub.
- **Real execution, not a simulated sandbox** — Python exercises run
  against your actual local `python` interpreter; Java exercises are
  compiled with `javac` and run with `java`; C++ exercises are compiled
  with `g++` and run as a native binary; Spring exercises run against a
  scaffolded Maven project via `mvn test`; Node.js exercises run directly
  with `node` (no separate compile step) — all in an isolated subprocess
  with a timeout. AI exercises run on that exact same Python interpreter
  (no separate toolchain of its own). Architecture exercises run no code
  at all — every one gates completion on an inline comprehension check
  instead.
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
one-off preview only, not a supported way to actually run exercises,
since running Java/C++/Spring code needs a real local compiler/
interpreter subprocess a browser sandbox can't provide (see
[docs/DEVELOPMENT.md](docs/DEVELOPMENT.md#android-build-python-only)
for how the Android build works around the same restriction, for Python
only). It's served over HTTPS with a self-signed
certificate (CN `coding-adventure`, generated automatically on first run
and cached in `data/certs/`) rather than plain HTTP — your browser will
show a one-time "connection isn't private" warning the first time you
visit, since the certificate isn't from a trusted CA; click "Advanced"
then "Proceed to localhost" to continue, this is expected for a
self-signed, local-only certificate. The script prints the port it
started on and opens your browser automatically
(`https://localhost:8550` by default); to use a different port, set
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

**Android (Python execution only):** `./build_apk.sh` builds a real APK
via `flet build apk` (needs a Flutter + Android SDK/NDK install first —
see [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md#android-build-python-only)).
Java, C++, Spring, and Node.js need a real local compiler/runtime a phone
can't provide, so on Android their Run button is disabled — but every
other part of the app, including those four tracks' content, still
works: browsing categories, reading explanations/examples, and editing
code in the editor. Since there's no legitimate way to "complete" an
exercise in those tracks on a phone, every category and level is
unlocked from the start there instead of gating progression behind an
unreachable prerequisite. Python and AI both actually *run* exercises on
Android, via an in-process execution engine instead of the desktop app's
usual subprocess (AI shares that exact engine instance, since its
content is plain Python). Architecture needs no execution at all on any
platform, so it's unaffected by this restriction, and — like AI — is
always fully unlocked regardless of platform.

## For developers

```powershell
# Run the app (native desktop window)
.venv\Scripts\python.exe main.py

# Run the app (browser preview, default port 8550; needs requirements-web.txt)
.venv\Scripts\python.exe main_web.py

# Developer gates (lint + tests + coverage), logs under scripts\logs\
.venv\Scripts\python.exe -m pip install -r requirements-dev.txt   # once
.\scripts\dev.ps1 all          # or: scripts/dev.sh all
.\scripts\dev.ps1 test         # just the test suite
.\scripts\dev.ps1 content      # only the content-lint tests, after editing YAML
```

CI (`.github/workflows/ci.yml`) runs the same commands on Ubuntu and
Windows for every push and pull request. Dependencies are split into
`requirements.txt` (runtime, pinned), `requirements-dev.txt` (pytest,
coverage, ruff) and `requirements-web.txt` (uvicorn + cryptography for
the browser preview only). The app writes a rotating log to
`data/logs/app.log`.

- `app/engine/` — content model (`Exercise`, `QuizQuestion`), YAML
  loaders, category/unlock logic, and `run_evaluation.py` (the pure
  pass/fail decision the lesson screen renders).
- `app/execution/` — one `ExecutionEngine` per language, all five
  implemented (`python_engine.py`, `java_engine.py`, `cpp_engine.py`,
  `spring_engine.py`, `node_engine.py`), plus `python_inprocess_engine.py`
  (used instead of `python_engine.py` specifically on Android, where
  subprocess spawning isn't available). `ai` reuses the exact same
  Python engine instance rather than needing its own; `architecture` has
  no engine at all, since none of its exercises run code.
- `app/progress/` — SQLite-backed XP/streaks/badges/activity log, keyed
  per language track, plus JSON export/import for backing up or
  restoring progress across every track at once.
- `app/ui/` — Flet screens, plus `components.py` (themed buttons, cards,
  hero banners, tiles, rings, chips, the shared multiple-choice widget)
  and `motion.py` (staggered reveals, hover lift, pop-in, pulse,
  count-up, confetti).
- `app/config/` — settings, data-directory resolution, `paths.py`
  (repo layout), `clock.py` (local calendar days), `logging_setup.py`.
- `content/<language>/lessons/*.yaml` — one exercise per file; adding or
  changing one never requires touching app code. All seven tracks
  (including `ai` and `architecture`) follow this same layout.

For a deeper dive:

- [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) — project layout, how each
  subsystem works, running it/testing it.
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — system context, class
  diagrams, sequence diagrams, the persistence model, and the design
  decisions behind them.
