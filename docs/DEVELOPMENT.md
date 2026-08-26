# Development guide

Technical documentation for anyone digging into the code — architecture,
project layout, and implementation notes. For what the app actually does
and how to run it, see the main [README](../README.md).

## Status

All five tracks are fully built. Python and Java share the same 14 topic
categories, real execution against a local `python`/`javac`+`java`
toolchain. C++ has its own 10 topic categories (a general-purpose
language subset rather than a framework), executed against a local
`g++` toolchain. Spring has its own 6 topic categories, executed against
a local Maven + JDK toolchain via a scaffolded Maven project run through
`mvn test` — see `app/execution/spring_engine.py` and "Execution
engines" below for how that differs from the other four. Node.js has its
own 6 topic categories (the same set as C++), executed directly against
a local `node` toolchain with no separate compile step. Primarily a
desktop app; there's also a Python-only Android build (`build_apk.sh`)
— see "Android build (Python-only)" below.

## Running it

**Easiest way (no terminal needed):** double-click `run_app_window_mode.bat`
(Windows) or run `./run_app_window_mode.sh` (git-bash/macOS/Linux). First
run sets up a virtual environment and installs dependencies automatically
(takes a minute); every run after that just launches the app straight
away, as a native desktop window (`main.py`).

Manually, if you prefer:

```powershell
.venv\Scripts\python.exe main.py
```

There's also a browser-preview entry point, `main_web.py` /
`run_app_web_ui.bat` / `run_app_web_ui.sh`, which opens the same UI in a
browser tab instead of a native window. It's a one-off way to look at the
screens (e.g. in Chrome, or on a machine with no display server) — not a
second supported way to run the app day to day, since exercises need a
real local subprocess (compiler/interpreter) a browser sandbox can't
provide; see "Android build (Python-only)" below for how the mobile
build works around that same underlying constraint, for Python only.
The port is configurable via the `CODING_ADVENTURE_WEB_PORT`
environment variable (default `8550`); the script echoes whichever port
it actually started on and opens the browser automatically.

It's served over HTTPS, not plain HTTP: `main_web.py` gets a plain
FastAPI ASGI app out of Flet via `ft.run(main, export_asgi_app=True)`
(rather than letting `ft.run` start its own, HTTP-only server) and serves
it directly with `uvicorn.run(app, ssl_certfile=..., ssl_keyfile=...)`,
since TLS termination can only be configured at that layer. The
certificate is self-signed (CN `coding-adventure`, ~2 year validity,
`localhost`/`127.0.0.1` in its SAN), generated on first use and cached in
`data/certs/` by `app/config/ssl_cert.py` — regenerated automatically
once it's within 7 days of expiring. Because it's self-signed rather than
CA-issued, browsers show a one-time "connection isn't private" warning on
first visit; that's expected for a local-only preview certificate.

Running Java exercises additionally needs a local JDK (`javac`/`java` on
PATH); running C++ exercises needs a local `g++` (e.g. MinGW-w64 on
Windows) on PATH; running Spring exercises needs a local JDK plus Maven
(`mvn` on PATH); running Node.js exercises needs a local `node` on PATH
— the language picker shows "Toolchain needed" instead of "Available" if
one isn't found, rather than failing confusingly the first time someone
tries to run code. The Spring track's first `mvn test` run needs network
access once, to download its dependencies into the local `~/.m2`
repository — every run after that is fully offline.

`run_app_window_mode.bat/.sh` and `run_app_web_ui.bat/.sh` all `call`/
`bash` a shared helper (`scripts/ensure_toolchains.bat` on Windows,
`scripts/ensure_toolchains.sh` elsewhere) right after the venv bootstrap,
on every launch. It checks for `javac` and `g++` on PATH and, only for
whichever is actually missing, asks a plain `[y/N]` question before
installing anything — `winget` on Windows, Homebrew/Xcode Command Line
Tools on macOS, `apt`/`dnf`/`pacman` (whichever is present) on Linux. It
never installs without that explicit "y", and it's a no-op once both
tools are already on PATH. (Node.js isn't part of this auto-install
helper -- install it manually from https://nodejs.org, or via your OS
package manager, before running Node.js exercises; the language
picker's "Toolchain needed" dialog for Node.js shows the same
OS-specific steps `get_install_guide()` returns for the other
languages.)
tools are already on PATH. Clicking a "Toolchain needed" card in the app
itself shows the same install steps for the detected OS as a dialog (see
`get_install_guide()` in `toolchain_check.py`), with a "Continue anyway"
escape hatch into the hub for anyone who'd rather install manually later.

A toolchain installed mid-session (via the auto-installer above, or
manually) won't be picked up until whatever launched the app is
restarted — Windows doesn't push `PATH` changes into already-running
processes, so a freshly-installed compiler stays invisible to `shutil.
which()` until VS Code/the terminal is reopened. Both installer scripts
print this explicitly after a successful install.

## Running the tests

```powershell
.venv\Scripts\python.exe -m pytest tests\ -v
```

Java-, C++-, Spring-, and Node.js-execution tests are skipped
automatically (`pytest.mark.skipif`) on a machine missing the relevant
toolchain (JDK / `g++` / Maven+JDK / `node`) on PATH, rather than
failing.

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
  config/      # settings persistence + platform-appropriate data directory,
               # ssl_cert.py (self-signed cert for the browser preview)
content/
  python/
    lessons/   # one YAML file per exercise
    quiz/      # quiz_questions.yaml
  java/
    lessons/   # same shape, same category keys as python/lessons/
    quiz/
  cpp/
    lessons/   # own 10 category keys (not the full 14 -- see below)
    quiz/
  spring/
    lessons/   # own 6 category keys (not the full 14 -- see below)
    quiz/
    scaffold/pom.xml  # shared Maven project template, copied per run
  node/
    lessons/   # own 12 category keys -- C++'s 6 plus 6 more, see below
    quiz/
docs/          # this file + ARCHITECTURE.md
tests/         # pytest suite, one file per module roughly mirroring app/
data/          # gitignored -- settings.json + progress.sqlite3, created
               # on first run (see "Data storage" below)
graphify-out/  # knowledge-graph snapshot of the codebase (see repo root
               # CLAUDE.md's graphify section) -- regenerate with the
               # graphify skill, not meant to be hand-edited
main.py        # Flet entry point, native desktop window (`ft.run(main)`)
main_web.py    # Browser-preview entry point, served over HTTPS via uvicorn
               # + a self-signed cert; port via CODING_ADVENTURE_WEB_PORT
scripts/
  ensure_toolchains.bat/.sh  # shared toolchain auto-install helper, called
                             # from all 4 run_app_*.bat/.sh below
run_app_window_mode.bat/.sh # first-run venv bootstrap + launch (desktop window)
run_app_web_ui.bat/.sh      # first-run venv bootstrap + launch (browser preview)
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

C++ deliberately does **not** chase the same 14-category list — several
of those categories (dependency management, packaging, deployment,
observability) are ecosystem/tooling concepts more naturally taught via
a package manager or framework than bare C++ language/stdlib content.
Instead C++ has its own 10 categories covering general-purpose-language
ground: `idioms_gotchas`, `core_refresher`, `data_structures`,
`stdlib_deep_dive`, `concurrency_async` (`std::thread`/`mutex`/`atomic`/
`async`/`promise`-`future` rather than `asyncio`/virtual threads),
`thread_scheduling` (`sleep_for`/`yield`/`condition_variable`, joining a
`vector<thread>`, explicit `std::launch::async`), `sync_vs_async`
(`std::future`/`shared_future` gotchas, exception propagation through
`.get()`, `std::launch::deferred`'s precisely-defined lazy execution),
`functional_programming` (lambda-capture-in-loop gotchas, `std::function`,
`std::transform`/`std::accumulate`, closures-as-values), `recursion`
(missing/off-by-one base cases, memoization, tail-recursion style via an
accumulator, mutual recursion), and `gotcha_gauntlet` (kept last in level
order so it stays the flagship's "final" position in the topic browser,
same as Python/Java). The four newer categories were chosen specifically
because they fit a single `g++`-compiled file with no external tooling;
categories like packaging/deployment/dependency-management were left out
because they'd need a real package manager or build system C++ doesn't
have here, which would have meant stretching the exercise's honesty
("real execution, not simulated") past what the engine can back up.
Nothing in the engine assumes a fixed category set across languages —
`ExerciseEngine.categories()` is still derived purely from what's present
in each language's own content directory, so C++ having a
different-sized set required zero app-code changes.

Spring goes further still: it's a framework, not a general-purpose
language, so even C++'s category shape doesn't fit. Its 6 categories —
`dependency_injection`, `bean_lifecycle`, `configuration_profiles`,
`events`, `aop`, `resilience` — are Spring-specific concerns with no
equivalent in the other tracks at all. All six deliberately stay within
plain Spring Framework territory (dependency injection, bean
scopes/lifecycle hooks, `@Value`/`@Profile` configuration,
`ApplicationEvent`/`@EventListener`,
`@Aspect`/`@Before`/`@AfterReturning`/`@Around` advice,
CircuitBreaker/Retry/RateLimiter/fallback decorators) rather than
reaching for Spring Boot's web/data layers or the parts of "Spring
Cloud" that are inherently multi-process (service discovery, API
gateway, config server) — those genuinely can't be exercised by a single
scaffolded Maven project running `mvn test`, since they need multiple
running services to mean anything, not just a library import. Resilience
patterns (`resilience` category) are the part of the "Spring Cloud"
umbrella that's actually just a library — Resilience4j's core decorators
(`CircuitBreaker.decorateSupplier`, `Retry.decorateSupplier`, etc.) wrap
a plain `Supplier<T>` in a single JVM, no network or second process
involved, so they fit this engine's execution model exactly the same way
AOP or events do. See "Execution engines" below for why Boot/multi-process
territory is out of scope. Adding `events`/`aop`/`resilience` only needed
new dependencies in the shared scaffold (`spring-aop`+`aspectjweaver` for
AOP, `resilience4j-all` for resilience — all plain-Spring/plain-Java, not
Boot-specific) and one scaffold tweak: the compiler plugin needed
`<parameters>true</parameters>` so `@EventListener`'s SpEL `condition`
expressions can resolve a listener parameter by name (e.g.
`#event.amount`) via reflection.

Node.js started with C++'s exact 6-category shape (`idioms_gotchas`,
`core_refresher`, `data_structures`, `stdlib_deep_dive`,
`concurrency_async`, `gotcha_gauntlet`) when the track first shipped, but
that reasoning didn't actually hold for JavaScript the way it holds for
C++: Node is a general-purpose, package-manager-heavy ecosystem language
like Python/Java, not a bare compiled language with no build tooling of
its own -- `npm`/`package.json`/`package-lock.json`, structured logging,
`process.env`-based configuration, and graceful shutdown are all things
a single `node <file>.js` execution model can exercise perfectly well,
unlike C++'s genuine lack of an equivalent. A later content pass added
6 more categories (`dependency_management`, `sync_vs_async`,
`functional_programming`, `recursion`, `observability`, `deployment`),
bringing Node to 12 categories total -- closer to Python/Java's 14 than
to C++/Spring's smaller sets, reflecting that Node is architecturally a
peer of Python/Java here, not of C++. `concurrency_async` content is
written idiomatically for Node's actual concurrency model rather than
translated from `asyncio`/`CompletableFuture`: the single-threaded event
loop's microtask (Promise) vs. macrotask (`setTimeout`) ordering,
callback- vs. Promise- vs. `async`/`await`-style APIs, and `Promise.all`
vs. `Promise.allSettled` are Node/JS-specific concerns with no direct
equivalent in the other tracks' concurrency models. The newer
`sync_vs_async` category goes a level deeper into the event loop itself
-- `process.nextTick`'s queue-jumping priority over Promise microtasks
(a Node-specific behavior, not part of the ECMAScript spec), a
synchronous blocking call delaying an already-scheduled timer, and
`for await...of` over async generators -- while `recursion` includes a
JS-specific trap the other tracks don't need: V8 never implemented
proper tail-call optimization despite it being in the ES2015 spec, so
even a tail-recursive accumulator pattern still overflows the stack on
deep input, unlike in a language that guarantees the optimization.

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
implements: `ExecutionEngine.run(code, timeout, handle, stdin_text,
exercise) -> ExecutionResult` (`success`, `stdout`, `stderr`,
`timed_out`, `blocked`, `blocked_message`), plus `RunHandle` for mid-run
cancellation (used when navigating away from a lesson while code is
still running — there's no visible Stop button, since the fixed timeout
already guarantees a runaway run gets killed). The `exercise` parameter
is unused by the four single-file engines but required by
`SpringEngine`, since a Spring exercise needs more than a code string to
run (see below) — `lesson_screen.py` passes it on every call regardless
of language, so only `SpringEngine` needed to change behavior when it
was added.

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
- **`cpp_engine.py`** — compiles the submitted code to a temp `main.cpp`
  with `g++ -O2 -std=c++17`, then runs the resulting binary under the
  same timeout/cancel/stdin contract. `check_toolchain("cpp")` gates
  this the same way Java's does. A crashed C++ binary (segfault,
  div-by-zero, stack overflow, abort) usually prints nothing to stderr
  on its own, so `_describe_crash(returncode)` translates the common
  Windows NTSTATUS codes and POSIX signal numbers into a synthetic
  stderr line whenever stderr would otherwise be empty — an uncaught
  `std::exception`'s own `what()` text is left untouched since it's
  already useful.
- **`spring_engine.py`** — the fundamentally different one: a Spring
  exercise isn't a single self-contained code string, since completion
  is gated by a fixed JUnit test class (`Exercise.spring_test_code`),
  not just `expected_output`. Each run copies the shared scaffold at
  `content/spring/scaffold/pom.xml` into a fresh temp Maven project,
  writes the submitted code and the exercise's fixed test class under
  `src/main`/`src/test` (both class names auto-detected the same way
  `java_engine.py` does), then runs `mvn.cmd -q -o test` via `Popen` (the
  `.cmd` extension is required on Windows — `subprocess.Popen` can't
  launch a bare `.cmd`/batch file the way a shell can) under the usual
  `RunHandle`/timeout contract, though with its own longer internal
  timeout (`MVN_TIMEOUT_SECONDS = 45.0`) rather than the 8s the UI
  passes in, since JVM+Maven+Spring context startup needs more headroom.
  Deliberately uses plain Spring Framework (`spring-context`/
  `spring-test`/`spring-aop`+`aspectjweaver`/`resilience4j-all`), not Spring Boot — no embedded server or
  autoconfiguration to boot, which keeps a cold `mvn -o test` run around
  4 seconds and fully offline once the scaffold's dependencies are
  warmed into `~/.m2` once. Maven's own logger writes everything
  (including `[ERROR]` diagnostics) to **stdout**, never stderr, so a
  failing run's output is routed into `ExecutionResult.stderr` to match
  the other engines' contract; a passing run returns a synthetic,
  deterministic `stdout="BUILD SUCCESS"` rather than the real surefire
  summary line, since that line's elapsed-time/class-name content is
  non-deterministic and can't reliably satisfy `validate_output()`'s
  `re.fullmatch()`. `_sanitize_path()` strips the temp dir's absolute
  path (Maven reports it in both a backslash and a `/C:/...`
  forward-slash form) out of compiler errors before they reach the UI.
- **`node_engine.py`** — the simplest of the five: no separate compile
  step at all (unlike Java/C++), since Node runs source directly —
  submitted code is written to a temp `exercise.js` and run with
  `node <file>` under the same timeout/cancel/stdin contract as the
  other single-file engines. `check_toolchain("node")` gates this the
  same way Java's/C++'s does. A syntax error just surfaces as Node's own
  stderr output when the file is run (no separate compiler pass to catch
  it earlier), the same way a Python syntax error does. Stdin is always
  fed (even `""`), though idiomatic Node code reads it asynchronously via
  `readline` rather than a blocking call the way Python's `input()`/
  Java's `Scanner` do — a script that never wires up `readline` simply
  never consumes the piped stdin, which is fine since `communicate()`
  doesn't require it to be read.

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

### Android build (Python-only)

`build_apk.sh` builds a real Android APK via `flet build apk` (a real
Flutter SDK + Android SDK/NDK under the hood — see
https://flet.dev/docs/publish/android for first-time toolchain setup;
the script assumes that's already installed). Support is deliberately
**Python-only**: `PythonEngine`, `JavaEngine`, `CppEngine`, and
`SpringEngine` all spawn real subprocess binaries (`python -I`;
`javac`/`java`; `g++`; `mvn`) on desktop/web, but a non-rooted Android
app can't spawn a sibling OS process at all, and there's no JDK/g++/
Maven on-device for the other three regardless — bundling a real compiler
toolchain into a mobile app sandbox isn't realistic (this exact tradeoff
is why an Android build was skipped entirely for a long time — see git
history — until the sibling kids' app's approach below was ported over
for Python specifically).

`PythonInProcessEngine` (`app/execution/python_inprocess_engine.py`),
ported from the sibling kids' app's `app/sandbox/inprocess_runner.py` +
`watchdog.py`, works around the subprocess restriction by running
submitted code with `exec()` in the same process, using an AST transform
(`app/execution/watchdog.py`) that injects a cooperative watchdog tick
into every `for`/`while` loop body — standing in for the
`process.kill()` an OS-level subprocess timeout would normally provide.
Deliberately does **not** port the sibling app's AST-based builtins/
import allowlist — that's a kid-safety sandbox this app never needed in
the first place (see `app/execution/base.py`'s docstring); only the
loop-cancellation *mechanism* needed porting, since it solves a
structural "no OS process to kill" problem that has nothing to do with
the trust model. `app/execution/registry.py` swaps to it automatically
whenever `android_platform.is_android()` is true (checked via `hasattr
(sys, "getandroidapilevel")`, an Android-only CPython attribute —
`platform.system()` can't distinguish Android from a Linux desktop on
its own, since both report `"Linux"`); every other platform keeps using
the normal subprocess-based `PythonEngine`.

Java/C++/Spring still register their normal (subprocess) engines on
Android — there's no separate mobile variant of those — so
`check_toolchain()` correctly reports their compiler/runtime as missing
there, same as it would on any desktop machine lacking one. Rather than
block those tracks outright, `language_select.py` detects `is_android()`
and still lets the user into the hub with the same "Available" badge as
any other track (its subtitle explains that running code needs a desktop
computer) instead of the normal "Toolchain needed" install-guide dialog
(whose desktop OS-specific winget/brew/apt steps would be actively wrong
advice on a phone with nowhere to run them) — browsing an exercise's
explanation, example, and challenge, and editing code in the editor,
never needs a real toolchain, only actually *running* code does.
`lesson_screen.py` checks `check_toolchain(exercise.language)` itself and
disables the Run button specifically (with an explanatory note
underneath) when it's unavailable, instead of only surfacing the problem
after a click via `ExecutionResult.blocked` — this disabling isn't
Android-specific either; it applies identically on a desktop machine
that's simply missing a toolchain, so browsing content there works the
same way even before the toolchain is installed.

Since Run is permanently unavailable for Java/C++/Spring on Android (no
javac/g++/mvn can ever exist in the app sandbox), the normal
completion-gated category progression would leave a mobile user
permanently stuck on `category_level` 1 of every category in those three
tracks — there's no legitimate way to "complete" an exercise there to
unlock the next one. `ExerciseEngine.is_unlocked()`
(`app/engine/lesson_engine.py`) special-cases this: when `self.language`
is one of `{"java", "cpp", "spring"}` (`MOBILE_ALWAYS_UNLOCKED_LANGUAGES`)
and `is_android()` is true, every exercise reports unlocked regardless of
`completed_ids`, so a phone user can freely browse every level of every
category. Python is excluded from this bypass since it genuinely runs
(and can genuinely be completed) on Android via the in-process engine.

## Data storage

Everything lives locally and offline — no cloud, no accounts, no network
access at all. `settings.json` and `progress.sqlite3` live in a
project-local `data/` folder (gitignored), resolved by
`resolve_platform_data_dir()` (`app/config/platform_paths.py`) — this
app runs from a git checkout rather than being installed as a packaged
product, so progress lives next to the code instead of in an
OS-appropriate per-user directory. That doesn't hold on Android at all
(no repo checkout a packaged APK runs from, and the app bundle itself
may not be reliably writable), so `resolve_platform_data_dir()` checks
`FLET_APP_STORAGE_DATA` first — a real per-app writable directory
Flet's own runtime sets on every packaged target, Android included —
before falling back to `<repo_root>/data`. `app/config/settings.py`'s
`get_data_dir()` migrates forward, once, from the old
`%APPDATA%\CodingAdventure\` location if anything's still there from
before this change, never overwriting a file that already exists at the
new location.
