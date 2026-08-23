# Development guide

Technical documentation for anyone digging into the code — architecture,
project layout, and implementation notes. For what the app actually does
and how to run it, see the main [README](../README.md).

## Status

Python and Java tracks are both fully built — same 14 topic categories
each, real execution against a local `python`/`javac`+`java` toolchain.
C++ and Spring are scaffolded (content directories exist, the
`ExecutionEngine` interface is defined) but not implemented — see
`app/execution/cpp_engine.py` / `spring_engine.py`. The app is
**desktop-only by design**, not by omission — see "Why no Android build"
below.

## Running it

**Easiest way (no terminal needed):** double-click `run.bat` (Windows) or
run `./run.sh` (git-bash/macOS/Linux). First run sets up a virtual
environment and installs dependencies automatically (takes a minute);
every run after that just launches the app straight away.

Manually, if you prefer:

```powershell
.venv\Scripts\python.exe main.py
```

Running Java exercises additionally needs a local JDK (`javac`/`java` on
PATH) — the language picker shows "Toolchain needed" instead of
"Available" if one isn't found, rather than failing confusingly the
first time someone tries to run code.

## Running the tests

```powershell
.venv\Scripts\python.exe -m pytest tests\ -v
```

Java-execution tests are skipped automatically (`pytest.mark.skipif`) on
a machine with no JDK on PATH, rather than failing.

## Project layout

```
app/
  ui/          # Flet screens: app_window (route dispatcher), app_state,
               # setup_wizard, language_select, track_hub, category_map,
               # category_levels, daily_refresher, lesson_screen,
               # quiz_screen, progress_screen, settings_screen,
               # code_editor, theme
  engine/      # Exercise/QuizQuestion dataclasses, YAML loaders
               # (ExerciseEngine, QuizEngine), category display metadata,
               # language registry, output validator
  execution/   # ExecutionEngine ABC + one concrete engine per language
               # (see "Execution engines" below), toolchain detection,
               # error-message translation
  progress/    # SQLite-backed progress, keyed per language track
  config/      # settings persistence + platform-appropriate data directory
content/
  python/
    lessons/   # one YAML file per exercise
    quiz/      # quiz_questions.yaml
  java/
    lessons/   # same shape, same category keys as python/lessons/
    quiz/
  cpp/
    lessons/   # empty (.gitkeep only) -- scaffolded, not built out
  spring/
    lessons/   # empty (.gitkeep only) -- scaffolded, not built out
docs/          # this file + ARCHITECTURE.md
tests/         # pytest suite, one file per module roughly mirroring app/
data/          # gitignored -- settings.json + progress.sqlite3, created
               # on first run (see "Data storage" below)
graphify-out/  # knowledge-graph snapshot of the codebase (see repo root
               # CLAUDE.md's graphify section) -- regenerate with the
               # graphify skill, not meant to be hand-edited
main.py        # Flet entry point (`ft.run(main)`)
run.bat/run.sh # first-run venv bootstrap + launch
```

## How it works

### Content is data, not code

Every exercise and quiz question lives as a YAML file under
`content/<language>/`, loaded by `ExerciseEngine`/`QuizEngine`
(`app/engine/lesson_engine.py`, `quiz_engine.py`). Adding, editing, or
removing one never requires an app-code change — the engines re-glob the
directory on next load. `AppState.exercise_engine()`/`quiz_engine()`
build one instance per language key, lazily, and cache it — so switching
tracks never reloads content that's already been read.

### Language picker, every launch

Unlike a typical app that remembers your last screen, `/languages` is
shown on **every** launch after first-run setup, not skipped based on
the previously selected track — an explicit product decision, not an
oversight (see `app/ui/language_select.py`'s module docstring). A
track's card shows "Available", "Toolchain needed" (content exists but
the local machine lacks the compiler/runtime — `app/execution/
toolchain_check.py`), or "Coming soon" (no content/engine yet).

### Practice by Topic — kept in parity across languages on purpose

Both Python and Java define the exact same 14 category keys
(`idioms_gotchas`, `core_refresher`, `data_structures`,
`stdlib_deep_dive`, `concurrency_async`, `thread_scheduling`,
`sync_vs_async`, `functional_programming`, `recursion`,
`dependency_management`, `packaging`, `deployment`, `observability`,
`gotcha_gauntlet`) — `app/engine/categories.py`'s `CATEGORY_META` is one
flat dict shared by every language track, since the same category
(e.g. "Concurrency & Async") means the same thing conceptually
regardless of which language's content fills it in. `ExerciseEngine.
categories()` derives the actual per-language category *list* from
whatever content exists in that language's `content/<language>/lessons/`
directory — nothing hardcodes which categories a language "should"
have, so adding an exercise in a new category is enough to make that
category show up in the topic browser. When Java's category list fell
behind Python's after a round of Python-only content additions, the fix
was adding matching Java content, not touching any app code.

Each language's content for a shared category is written idiomatically
for that language, not translated line-for-line — e.g. `sync_vs_async`
uses `asyncio`/`asyncio.gather` for Python but `CompletableFuture`/
virtual threads for Java (Java has no native async/await); `recursion`'s
memoization exercise uses `@lru_cache` for Python but a hand-rolled
`HashMap` cache for Java (no built-in memoization decorator exists).

### Daily Refresher

`ExerciseEngine.daily_refresher(completed_ids, count=5)` computes a
small cross-topic set live on every call — round-robining the next
unlocked, incomplete exercise from each category until `count` is
reached — rather than a stored, hand-authored sequence. This keeps a
short daily session naturally touching several topics instead of
grinding through one category at a time, and stays correct automatically
as exercises are added, removed, or reordered in content.

### Category browser and unlocking

Every exercise has a `category` and a 1-based `category_level`
(position within that category), set in its YAML.
`ExerciseEngine.lessons_in_category()` groups and sorts them;
`is_unlocked()` unlocks a level once every earlier level in the same
category is complete — derived entirely from `completed_lesson_ids`,
no separate unlock-tracking schema. The flagship **Gotcha Gauntlet**
debug-puzzle track is just a category like any other
(`app/engine/categories.GOTCHA_CATEGORY`), given its own card on the
track hub instead of being buried in the plain topic browser.

### Quiz Bank

A standalone multiple-choice question bank per language
(`content/<language>/quiz/quiz_questions.yaml`), loaded by `QuizEngine`.
`start_session(count)` returns a freshly shuffled subset each time —
both question order and each question's own answer-option order are
re-randomized — so no two playthroughs look the same and the correct
answer isn't always in the same position.

### Execution engines

`app/execution/base.py` defines the shared contract every language
implements: `ExecutionEngine.run(code, timeout, handle, stdin_text) ->
ExecutionResult` (`success`, `stdout`, `stderr`, `timed_out`, `blocked`,
`blocked_message`), plus `RunHandle` for mid-run cancellation (used when
navigating away from a lesson while code is still running — there's no
visible Stop button, since the fixed timeout already guarantees a
runaway run gets killed).

- **`python_engine.py`** — a fast local `compile()` syntax pre-check,
  then `python -I <file>` in an isolated subprocess with a timeout
  (default 8s) and stdin piped through.
- **`java_engine.py`** — detects the submitted code's class name
  (`public class X`, falling back to the first `class X` found), writes
  it to `<ClassName>.java`, compiles with `javac` (a compile error
  returns the same `ExecutionResult` shape as a runtime failure), then
  runs `java -cp <dir> <ClassName>` under the same timeout/cancel/stdin
  contract. `check_toolchain("java")` gates this — if `javac`/`java`
  aren't on PATH, `run()` returns a `blocked` result with an install
  hint instead of crashing.
- **`cpp_engine.py` / `spring_engine.py`** — interface defined, bodies
  raise `NotImplementedError`. Spring in particular needs a
  fundamentally different shape than the other three (a scaffolded
  Maven project per exercise, run via `mvn test`, not a single-file
  compile-and-run) — see the docstring in `spring_engine.py`.

**Framing is crash-containment, not child safety.** Unlike the sibling
kids' app this one's architecture is based on, there's no AST-based
builtins/import allowlist here — exercises run the user's own code, on
their own machine, on purpose. The timeout and subprocess isolation
exist so a runaway loop can't hang the UI, not to sandbox against
malicious input.

### Output validation

`app/engine/validator.py`: `validate_output()` compares stdout against
`Exercise.expected_output` (supporting a `{input}` placeholder templated
from what the user typed) or, for exercises with genuinely
non-deterministic output, `expected_output_pattern` (a regex).
`validate_contains()` checks `Exercise.contains_patterns` — plain regex
search against the raw submitted source — a language-agnostic
replacement for an AST-based structural check, so the same field works
whether the exercise is Python or Java. Several exercises are
"refactor" style rather than "fix a crash": the starter already produces
correct output, and `contains_patterns` is what actually gates
completion (e.g. requiring `map(` and `filter(` so a submission that
just resubmits the unmodified starter loop doesn't silently pass).

### Adaptive practice

After 3 failed attempts in a row on the same exercise
(`ProgressStore.get_recent_failure_count()`), a dismissible suggestion
offers up to 3 related exercises sharing a `concept_tags` value
(`ExerciseEngine.recommend_practice()`). It never blocks retrying,
hints, or continuing — purely additive. The quiz results screen offers
the same kind of suggestion from the union of tags across every question
missed that session (`recommend_practice_for_tags()`), tracked only in
memory for the session.

### Progress, XP, and streaks — one row per language

`ProgressStore` (`app/progress/store.py`) is fully language-scoped:
every table (`profile`, `lesson_completions`, `badges`, `activity_log`,
`quiz_attempts`, `player_xp`) carries a `language` column, and every
method takes `language` as its first argument
(`complete_lesson(language, lesson_id, xp_reward)`,
`get_player_level(language)`, ...). Switching tracks never mixes XP,
streaks, or completions between them — a user juggling both Python and
Java sees two entirely independent progress states. XP-to-level curve:
clearing level *N* costs `N * 100` XP, computed live from one stored
`total_xp` counter (no separate mutable level field to keep in sync).

### Why no Android build

`build_apk.sh` was briefly added (adapted from the sibling kids' app,
which does ship an Android build) and then deliberately removed. Both
`PythonEngine` and `JavaEngine` spawn real subprocess binaries
(`python -I`; `javac`/`java`) — Android doesn't allow an app to spawn
arbitrary sibling OS processes at all, and there's no JDK on-device for
Java regardless. The sibling app worked around this for Python
specifically by building a second, in-process execution engine (an AST
transform injects a cooperative watchdog into every loop, standing in
for the OS-level timeout Android won't allow). There's no equivalent
workaround for Java — no way to compile or run arbitrary Java without a
real JDK toolchain, and bundling one into a mobile app sandbox isn't
realistic. Rather than ship a build where "Run" doesn't work, this app
targets desktop only.

## Data storage

Everything lives locally and offline — no cloud, no accounts, no network
access at all. `settings.json` and `progress.sqlite3` live in a
project-local `data/` folder (gitignored), resolved by
`resolve_platform_data_dir()` (`app/config/platform_paths.py`) — this
app runs from a git checkout rather than being installed as a packaged
product, so progress lives next to the code instead of in an
OS-appropriate per-user directory. `app/config/settings.py`'s
`get_data_dir()` migrates forward, once, from the old
`%APPDATA%\CodingAdventure\` location if anything's still there from
before this change, never overwriting a file that already exists at the
new location.
