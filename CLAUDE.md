# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

"Coding Adventure" — an offline, GUI-based coding refresher app for **professionals**, not beginners. Covers Python, Java, C++, and Spring, one track at a time, chosen from a language picker shown on every launch (not auto-skipped). Built as a sibling to `../python-adventure-kids` (a kids' Python-learning app), reusing its architecture patterns (YAML-as-content, subprocess execution engine, SQLite progress store, Flet route-dispatcher UI) but retargeted for a professional audience and multi-language from day one. Single UI stack: **Flet only** (the old app's CustomTkinter/Flet dual-stack was a migration artifact, not something worth repeating here).

## Commands

Run all from the repo root, using the project venv at `.venv\Scripts\python.exe` (created by `run.bat`/`run.sh` on first launch).

```powershell
# Run the app
.venv\Scripts\python.exe main.py

# Full test suite
.venv\Scripts\python.exe -m pytest tests\ -v

# A single test file / test
.venv\Scripts\python.exe -m pytest tests\test_lesson_engine.py -v
.venv\Scripts\python.exe -m pytest tests\test_lesson_engine.py::test_name -v
```

There is no linter or formatter configured in this repo (no ruff/flake8/black/mypy config) — don't invent commands for one.

## Architecture

### Content is data, not code

Exercises live as YAML files under `content/<language>/lessons/` (one file per exercise), loaded by `ExerciseEngine._load()` (`app/engine/lesson_engine.py`) into `Exercise` dataclass instances (`app/engine/exercise.py`). **Adding or changing an exercise never requires touching app code** — add a YAML file. One `ExerciseEngine` instance exists per language track (`AppState.exercise_engine()` builds and caches them lazily — see `app/ui/app_state.py`). Key `Exercise` fields beyond the obvious: `language` (which track it belongs to), `category`/`category_level` (topic-browser placement, 1-based position within category), `difficulty` (warmup/core/gotcha/deep_dive, purely descriptive), `expected_output` / `expected_output_pattern` (exact-match vs. regex, for exercises with non-deterministic output), `input_prompt` (stdin-fed answer box), `contains_patterns` (structural check via regex against raw source — a language-agnostic replacement for the kids app's Python-AST-only `ast_contains`, since this app needs the same field to work for Java/C++/Spring content too), `spring_test_code` (Spring-only: the fixed JUnit test class source that gates completion, since a Spring exercise isn't a single self-contained code string the way the others are — see the Execution section).

Quiz questions work the same way: `content/<language>/quiz/quiz_questions.yaml`, loaded by `QuizEngine` (`app/engine/quiz_engine.py`) into `QuizQuestion` instances (`app/engine/quiz.py`).

### One flat topic browser, no guided "main path" chaining

Unlike the kids app's "Today's Mission" (a strict `next_lesson_id`-chained sequence), this app has no single guided curriculum order. Two ways to reach an exercise:

1. **Daily Refresher** — `ExerciseEngine.daily_refresher()` computes a small (default 5) cross-topic set live on every call, round-robining the next unlocked/incomplete exercise from each category so a short daily session naturally touches every topic instead of grinding one at a time. Not stored anywhere — recomputed each visit based on current completion state.
2. **Practice by Topic / Gotcha Gauntlet** — every exercise has a `category` + 1-based `category_level`; `ExerciseEngine.categories()`/`lessons_in_category()` group and order them, `is_unlocked()` derives lock state purely from `completed_lesson_ids` (a level unlocks once every earlier `category_level` in the same category is complete — no separate unlock-tracking schema). Category display metadata (title/icon/color) is in `app/engine/categories.py`'s `CATEGORY_META`; a category with no entry falls back to `DEFAULT_META`, but the category itself still works since the real set of categories is derived entirely from what's present in lesson YAML. The "Gotcha Gauntlet" flagship debug-puzzle track is just a category (`gotcha_gauntlet`) that gets its own top-level card in the track hub instead of being buried in the plain category browser.

### Execution: real local toolchains, not a safety sandbox

`app/execution/` — one `ExecutionEngine` subclass per language (`app/execution/base.py` defines the ABC and the shared `ExecutionResult`/`RunHandle` contract). Framing is deliberately **crash-containment, not child safety**: exercises run the user's own code, on their own machine, on purpose — there's no adversarial threat model to defend against the way the kids app's AST-based builtins/import allowlist had to. A timeout and subprocess isolation exist so a runaway loop can't hang the UI, not to sandbox against malice. `ExecutionEngine.run()` also takes an optional `exercise: Optional[Exercise] = None` keyword param — unused by the single-file engines (Python/Java/C++), but required by `SpringEngine` to look up the exercise's fixed test source, since a Spring exercise isn't a single self-contained code string the way the others are. `lesson_screen.py` passes `self.exercise` on every call regardless of language.

- **`python_engine.py`** — a fast local `compile()` syntax pre-check, then `python -I <file>` in an isolated subprocess with a timeout (default 8s) and stdin piped through (always fed, even `""`, so a stray `input()` fails fast with `EOFError` instead of hanging). Cancelable mid-run via `RunHandle`.
- **`java_engine.py`** — detects the submitted code's class name (`public class X`, falling back to the first `class X` found, defaulting to `Solution`), writes it to `<ClassName>.java`, compiles with `javac` (a compile error returns the same `ExecutionResult` shape as a runtime failure — `success=False`, raw compiler output in `stderr`), then runs `java -cp <dir> <ClassName>` under the same timeout/`RunHandle`/stdin contract as the Python engine. Both `javac` and `java` run with `cwd` set to the temp dir and given only the bare filename/class name, so no host path ever leaks into a compiler error or stack trace.
- **`cpp_engine.py`** — compiles submitted code to a temp `main.cpp` with `g++ -O2 -std=c++17`, then runs the resulting binary under the same timeout/`RunHandle`/stdin contract as the other engines. A crashed C++ binary (segfault, div-by-zero, stack overflow, abort) usually prints nothing useful to stderr on its own — `_describe_crash(returncode)` translates the common Windows NTSTATUS codes (`0xC0000005` access violation, `0xC0000094` divide-by-zero, `0xC00000FD` stack overflow, `0xC0000409` abort/uncaught-exception, ...) and POSIX signal numbers (`SIGSEGV`/`SIGFPE`/`SIGABRT`/`SIGILL`) into a synthetic stderr line, but only when stderr is otherwise empty (an uncaught `std::exception`'s own `what()` output is left alone).
- **`spring_engine.py`** — the one engine that isn't a single-file compile-and-run. Copies the shared scaffold at `content/spring/scaffold/pom.xml` into a temp Maven project, writes the submitted code under `src/main/java/com/codingadventure/exercise/<DetectedClassName>.java` and the exercise's fixed `spring_test_code` under `src/test/.../<DetectedTestClassName>.java` (class names auto-detected the same way `java_engine.py` does), then runs `mvn.cmd -q -o test` (Windows needs the `.cmd` extension explicitly — `subprocess.Popen` can't launch a bare `.cmd`/batch file the way a shell can) via `Popen` so `RunHandle` cancellation still works. Uses plain Spring Framework (`spring-context`/`spring-test`/`spring-aop`+`aspectjweaver`), not Spring Boot — no embedded server or autoconfiguration to keep `mvn test` fast (~4s) and fully offline once the scaffold's dependencies are warmed into `~/.m2` once. Maven's own logger writes everything, including `[ERROR]` diagnostics, to **stdout** (never stderr) — `SpringEngine` routes that into `ExecutionResult.stderr` on failure to match the other engines' contract, and returns a synthetic `stdout="BUILD SUCCESS"` on success (every Spring exercise's `expected_output_pattern` is just `"BUILD SUCCESS"`, since the real surefire summary line has non-deterministic content like elapsed time that can't reliably `re.fullmatch`). `_sanitize_path()` strips the temp dir's absolute path out of compiler errors (Maven reports them in both backslash and a `/C:/...` forward-slash form), matching the "no host path leaks" rule the other engines follow structurally.
- **`app/execution/toolchain_check.py`** — `shutil.which()`-based detection of whether a language's real toolchain (javac/java, g++, mvn) is on PATH. `language_select.py` calls this per track to show "Toolchain needed" (with an install hint) instead of "Available" when a track has content but the local machine lacks the compiler/runtime — `JavaEngine.run()`/`CppEngine.run()`/`SpringEngine.run()` also check it themselves and return a `blocked` `ExecutionResult` rather than crashing if the compiler/runtime go missing mid-session. Python needs nothing (bundled with the app's own venv). Note: a toolchain installed mid-session (e.g. via winget) won't be visible to `shutil.which()` until whatever launched the app (VS Code, a terminal) is restarted — Windows doesn't push registry `PATH` changes into already-running processes.
- **`app/execution/errors.py`** — `translate_error(stderr, language)` maps raw interpreter/compiler output to a concise explanation, keyed off the last Python exception name (`PYTHON_FRIENDLY`) or, for Java, a compile-error-vs-runtime-exception split (`_JAVA_COMPILE_ERROR_RE` vs `_JAVA_EXCEPTION_RE` + `JAVA_FRIENDLY`), or, for C++, `_translate_cpp_error()` (compile error → uncaught `std::exception` with its `what()` text → the specific "thread destroyed while still joinable" `std::terminate` message → the synthetic crash-note line from `cpp_engine.py` → a generic fallback, checked in that order via `CPP_FRIENDLY` keyed by standard exception type), or, for Spring, `_translate_spring_error()` (compile error → JUnit `AssertionFailedError` with its expected/actual detail extracted → a known Spring DI exception type via `SPRING_FRIENDLY` — `NoSuchBeanDefinitionException`, `BeanCreationException`, etc. — → a generic fallback). `extract_error_line_number(stderr, language)` similarly branches on the Python `File "<exercise>", line N` frame, Java's `.java:N` pattern, C++'s `main.cpp:N:` pattern, or Spring's `.java:N` pattern (same regex as Java, but taking the **first** match rather than the last — JUnit's reflection-based test invocation appends `java.base` frames like `ArrayList.java:1596` *after* the actual test file's frame, so "last match" picks a JDK-internal line instead of the real one).

### Output validation

`app/engine/validator.py`: `validate_output()` compares sandboxed stdout against `Exercise.expected_output` (supports a `{input}` placeholder templated from what the user typed) or, for exercises with genuinely non-deterministic output, `expected_output_pattern` (a regex). `validate_contains()` is a language-agnostic replacement for the kids app's Python-AST-only structural check — plain regex search against the raw submitted source, checking `Exercise.contains_patterns` (e.g. requiring a specific stdlib call the exercise is actually teaching, not just a correct-by-coincidence answer).

### Data storage

Fully offline, no network/cloud/accounts. `settings.json` + `progress.sqlite3` live in a project-local `data/` folder (`app/config/platform_paths.py`), not an OS per-user directory — this app is run from a git checkout, not installed as a packaged product, so keeping progress alongside the code is more useful than platform convention. `app/config/settings.py`'s `get_data_dir()` migrates forward, once, from the old `%APPDATA%\CodingAdventure` location if anything is still there (never overwriting an existing file at the new location), so past progress isn't lost by the move. **Progress is tracked per language track** — every table in `app/progress/store.py`'s schema (`profile`, `lesson_completions`, `badges`, `activity_log`, `quiz_attempts`, `player_xp`) is keyed by a `language` column, so switching tracks never mixes XP/streaks/completions between them. `ProgressStore` methods all take `language` as their first argument accordingly (e.g. `complete_lesson(language, lesson_id, xp_reward)`, `get_player_level(language)`).

### UI shell

`app/ui/app_window.py` is the route dispatcher: `page.views.clear()` + `page.views.append(...)` on every route change, rebuilding exactly one view fresh each time (avoids ever showing stale XP/progress numbers from a view built earlier). A Python-side `history: list[str]` stands in for back-navigation since `page.views` is deliberately kept at length 1. `AppState` (`app/ui/app_state.py`) is built once in `main()` and threaded through every view-builder function as an explicit parameter — settings, progress store, and per-language exercise/quiz engines (lazily built and cached per language key). Routing always starts at `/setup` (first run only) then `/languages` — the language picker is shown on **every** launch, not auto-skipped based on the last-selected track (explicit product requirement, not an oversight).

### Directory layout

```
app/
  ui/          # Flet screens: app_window (router), app_state, language_select, track_hub,
               # category_map/category_levels, daily_refresher, lesson_screen, quiz_screen,
               # progress_screen, settings_screen, setup_wizard, theme, code_editor
  engine/      # Exercise/QuizQuestion dataclasses, YAML loaders, category logic, validator
  execution/   # ExecutionEngine ABC + per-language engines (all four implemented) + registry
  progress/    # SQLite-backed XP/streaks/badges/activity log, per-language
  config/      # settings persistence + platform-appropriate data directory resolution
content/
  <language>/lessons/       # one YAML file per exercise
  <language>/quiz/          # quiz_questions.yaml
  spring/scaffold/pom.xml   # shared Maven project template SpringEngine copies per run
  # all four language content directories have real content
tests/         # pytest suite, one file per module roughly mirroring app/
main.py        # Flet entry point (`ft.run(main)`)
run.bat/run.sh # first-run venv bootstrap + launch
```
