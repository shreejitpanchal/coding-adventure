# Development guide

Technical documentation for anyone digging into the code — architecture,
project layout, and implementation notes. For what the app actually does
and how to run it, see the main [README](../README.md).

## Status

All seven tracks are fully built. Python and Java share the same 14 topic
categories, real execution against a local `python`/`javac`+`java`
toolchain. C++ has its own 10 topic categories (a general-purpose
language subset rather than a framework), executed against a local
`g++` toolchain. Spring has its own 6 topic categories, executed against
a local Maven + JDK toolchain via a scaffolded Maven project run through
`mvn test` — see `app/execution/spring_engine.py` and "Execution
engines" below for how that differs from the other four. Node.js has its
own 6 topic categories (the same set as C++), executed directly against
a local `node` toolchain with no separate compile step. AI is a full
top-level track (not a Python category) with 9 topic categories —
`ml_fundamentals`, `rag`, `agentic_frameworks`, `mcp`, `microsoft_agent_365`,
`langchain`, `langgraph`, `langsmith`, `solace_agent_mesh`, 50 exercises
each except `microsoft_agent_365`'s 5, 405 total — executing on the exact same Python engine instance as
the Python track, since its content is plain, dependency-free Python
under the hood (including the LangChain/LangGraph/LangSmith/Solace
Agent Mesh categories, which hand-roll each framework's core mechanic
rather than importing the real library). `microsoft_agent_365` is the
one no-code category in this
track (`requires_code: false`, a comprehension check instead of running
code), since Microsoft's Agent 365 product is enterprise governance
tooling with no hand-codeable mechanic — the same shape as every
Architecture exercise below. Architecture is the one entirely
conceptual, no-code track: 10 topic
categories — `event_driven_architecture`, `microservices`, `cqrs`,
`saga_pattern`, `strangler_fig`, `domain_driven_design`,
`hexagonal_architecture`, `api_gateway`, `circuit_breaker`,
`idempotency`, 5 exercises each — every exercise has `requires_code:
false` and gates completion on an inline multiple-choice comprehension
check instead of running code; both AI and Architecture are always
fully unlocked regardless of completion state (see "Progress and
unlocking" below). Primarily a desktop app; there's also a Python-only
Android build (`build_apk.sh`) — see "Android build (Python-only)"
below.

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

The mirrored task runners are the canonical way to run every gate --
they write a fresh plain-text log per task under `scripts/logs/` and
match `.github/workflows/ci.yml` command-for-command:

```powershell
# Windows
.\scripts\dev.ps1 all          # lint + test + coverage
.\scripts\dev.ps1 test         # just pytest
.\scripts\dev.ps1 content      # only the content-lint tests (fast, after editing YAML)

# git-bash / macOS / Linux
scripts/dev.sh all
```

Install the developer tools once with
`python -m pip install -r requirements-dev.txt` (pytest, coverage,
ruff). The raw commands, if you need them directly:

```powershell
.venv\Scripts\python.exe -m pytest tests\ -v
.venv\Scripts\python.exe -m ruff check app tests main.py main_web.py
```

Java-, C++-, Spring-, and Node.js-execution tests are skipped
automatically (`pytest.mark.skipif`) on a machine missing the relevant
toolchain (JDK / `g++` / Maven+JDK / `node`) on PATH, rather than
failing. The Spring tests additionally skip until the local Maven
repository holds the scaffold's dependencies, because `SpringEngine`
runs Maven offline (`-o`). Warm it once, with network access:

```powershell
mvn -f content\spring\scaffold\pom.xml dependency:go-offline
```

Timeouts kill the **whole process tree** (`taskkill /T` on Windows, the
process group elsewhere -- see `base._kill_and_release()`): the Windows
`java.exe` launcher re-executes itself as a grandchild that inherits the
pipes, so a plain `Popen.kill()` left the pipes open and the documented
`kill(); communicate()` pattern hung forever. CI runs on Ubuntu and Windows with a JDK and Node installed, so
those engine tests execute for real there; Spring skips (no warmed
`~/.m2`).

### Content lint

`tests/test_content_lint.py` is parametrized over every track in
`LANGUAGE_ORDER` and asserts the invariants the app relies on rather
than exact counts (so adding content never means editing a test): every
file loads into `Exercise`, ids and global `level`s are unique, each
category's `category_level`s run 1..N with no gaps, a code exercise has
an `expected_output` or `expected_output_pattern`, every
`contains_patterns` entry compiles as a regex, every category has a
`CATEGORY_META` entry, conceptual exercises carry at least two
four-option questions, and the quiz bank loads with unique ids.

Model-level validation happens at load time too: `Exercise.__post_init__`
parses `comprehension_check` mappings into `QuizQuestion`s (an out-of-
range `correct`, fewer than two options, or an unknown key raises with
the question id), rejects an unknown `difficulty`, and rejects
`requires_code: false` with no questions. `app/engine/content_loader.py`
wraps every loader error in a `ContentError` that names the file.

### UI kit and motion (`app/ui/components.py`, `app/ui/motion.py`)

Every screen is composed from the same small kit rather than raw Flet
literals, so a colour or shape decision is made once:

- `theme.py` -- presets carry `accent`, a `gradient` pair, `surface` and
  `shadow` on top of the base palette. Default is `aurora`; the classic
  IDE themes remain. `LanguageInfo.color` gives each track its signature
  hue (cards, hub banner, rings).
- `components.py` -- `button`/`icon_button` (rounded, optional icon,
  `ghost` variant), `card` (accent stripe + title icon + optional hover
  lift), `hero_banner`, `nav_tile`, `stat_pill`, `chip`, `level_badge`,
  `icon_circle`/`emoji_circle`, `progress_ring`, `xp_bar`, `header_row`
  (icon back button + title + subtitle), `empty_state`, and
  `MultipleChoiceCard` (lettered option rows, cross-fading questions via
  `AnimatedSwitcher`, slim progress bar).
- `motion.py` -- `Stagger` (wrap controls while building, `play()` fades
  and slides them in one after another; falls back to "visible now"
  when there is no event loop), `hover_lift` (scale + glow on
  `on_hover`), `prepare_pop`/`pop_in` (spring from 85%), `Pulser`
  (heartbeat while code runs), `count_up` (animated numbers), and
  `confetti_layer`/`confetti` (a particle burst over a view's own
  `ft.Stack`).

The pattern for any animation is the same two halves: set the start
state while building, flip to the end state from a `page.run_task`
coroutine after a tiny sleep so the first frame has landed. Views that
animate on entry (`track_hub`, `progress_screen`) therefore end with a
scheduled task, and every helper swallows the "control no longer
mounted" error that a fast navigation away can cause.

**Text size and compact layout.** Every screen builds a local
`fs = lambda base: scaled(base, state.font_scale)` and passes *all* text,
chip and icon sizes through it, so the Settings "Text size" choice
(`Settings.code_font_size`, historical key name; `FONT_SIZE_SCALES`
small/medium/large/xlarge = 0.85/1.0/1.2/1.4) rescales the whole UI,
not only code. `components.is_compact(page)` is True below
`COMPACT_WIDTH` (720 px, i.e. phones): `view_padding(page)` shrinks,
`header_row(..., compact=True)` drops trailing chips under the title,
and the hub banner splits into stacked rows so a long title never wraps
one letter per line. Fixed pixel widths are avoided on anything that
must fit a phone (option rows stretch to the card; the setup card and XP
bar are clamped to `page.width`).

**Flutter layout rules that blank a whole subtree silently** (the
client raises, Flet shows nothing, and only `page.on_error` -- wired in
`app_window.py` to `data/logs/app.log` -- says why):

- never use `CrossAxisAlignment.STRETCH` on a Row/ResponsiveRow that
  sits in a scrolling Column (its height is unbounded, so "stretch"
  means "to infinity"); the card accent stripe is an outer coloured
  container with left padding for exactly this reason;
- never put `expand=True` children in a Column whose own height is
  unbounded (a card body in a grid), nor inside a `wrap=True` Row;
- Stack children fill the Stack with `left/top/right/bottom=0`, not
  `expand=True`;
- a one-sided `Border` cannot be combined with `border_radius`.

Where the fun lives: the language picker and hub open with gradient
banners and staggered cards; category and level lists have progress
rings, level badges and hover lift; a passed exercise fires confetti, a
spring-in reward card and an XP count-up; a perfect quiz also fires
confetti. Tests: `tests/test_components.py`, `tests/test_motion.py`.

### Logging

Both entry points call `app/config/logging_setup.configure_logging()`,
which attaches a rotating file handler writing to
`data/logs/app.log` (1 MB x 3). Flet swallows exceptions inside event
handlers, so this file is the first place to look when a screen
misbehaves. Modules use `logging.getLogger(__name__)`; the log never
contains submitted code or secrets.

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
  ai/
    lessons/   # own 9 category keys, plain dependency-free Python content
    quiz/
  architecture/
    lessons/   # own 10 category keys, every exercise requires_code: false
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

### Cross-track overview

`language_select.py`'s `_build_overview_card()` renders a summary strip
above the per-language cards: total XP and best current streak summed/
maxed across every `available` track (via `ProgressStore.
get_player_level()`/`get_streak_days()` for each key in `LANGUAGE_ORDER`
— cheap SQL lookups, no YAML/content loading involved), plus a "Continue:
`<exercise title>` (`<language>`)" button for whichever track was used
last. It returns `None` (rendering nothing) on a brand-new profile with
zero XP and no in-progress exercise, rather than showing an empty card.

The "continue" link relies on `ProgressStore.set_current_exercise()`,
which `lesson_screen.py`'s `_ExerciseController.__init__` now calls on
every lesson view build (`state.progress.set_current_exercise(state.
language, exercise.id)`) — previously this store method existed but had
no caller anywhere in the app, so `get_current_exercise()` always
returned `None`. The overview only resolves the *last selected*
language's (`AppState.language`) current exercise, not all seven — doing
that for every track would force-load every language's `ExerciseEngine`
(hundreds of YAML files each) just to render the picker screen, for a
feature that only ever needs one.

### Practice by Topic — kept in parity across languages on purpose

Python and Java both define the same original 14 category keys
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
was adding matching Java content, not touching any app code. Category
parity across tracks was never enforced by the engine, only maintained
by convention where it made sense to — C++/Node use their own smaller
6-10 category sets, and AI/Architecture (below) define entirely
different category sets suited to their own subject matter.

### AI and Architecture — full top-level tracks, not Python categories

`ai` and `architecture` are full entries in `app/engine/languages.py`'s
`LANGUAGE_ORDER`, each with its own card on the language picker, its
own independent XP/streak/progress, and (for `ai`) its own execution
wiring — an earlier design considered nesting AI as a category inside
Python's content, but both subjects are language-agnostic enough (ML/
RAG/agentic-framework/MCP mechanics; system-design patterns) that a
dedicated top-level track was the better fit.

`ai` (9 categories — `ml_fundamentals`, `rag`, `agentic_frameworks`,
`mcp`, `microsoft_agent_365`, `langchain`, `langgraph`, `langsmith`,
`solace_agent_mesh`, 50 exercises each except `microsoft_agent_365`'s
5, 405 exercises total) is plain,
hand-rolled, dependency-free Python under the hood (no numpy, no
network access, no LLM API calls, and — for the four framework
categories — no actual `langchain`/`langgraph`/`langsmith`/Solace
Agent Mesh package installed either), since
this app's "real execution, exact deterministic output" model has no
way to verify a live model call or network response, and the app is
explicitly 100% offline. Each of these four categories runs 50 levels,
with a `<category>_master` achievement on the final one; their first
five levels (each category's original scope before being expanded from
5 to 50) set up the foundational mechanics: `ml_fundamentals` covers a
train/test split that owns its own seeded `random.Random` instead of
depending on global state, data leakage from fitting a scaler on
combined train+test data, thresholding probabilities before computing
accuracy, gradient descent's sign convention, and evaluating on
held-out data instead of training data; `rag` covers cosine similarity
vs. raw dot product, top-k retrieval's sort direction, chunk overlap so
a boundary-straddling phrase survives intact, a delimited prompt
template instead of plain concatenation, and respecting a
context-window character budget; `agentic_frameworks` covers a tool
dispatcher that fails loudly instead of silently returning `None`, a
`max_steps` guard against an unbounded loop, validating a tool call's
required arguments before invoking it, preserving the system message
when trimming conversation history, and checking the correct
stop-condition key; `mcp` covers JSON-RPC's required `"jsonrpc": "2.0"`
field, `result`/`error` mutual exclusivity, detecting a duplicate tool
registration, checking a server's advertised capabilities before
calling a method, and correlating responses to requests by `id` rather
than arrival order. The remaining 45 levels in each category continue
into further mechanics with increasing granularity (e.g.
`ml_fundamentals` continues into cross-validation, regularization,
ensembling, and calibration; `mcp` continues into pagination,
resource/prompt/sampling mechanics, and connection-lifecycle handling)
— see the individual lesson YAML files under `content/ai/lessons/` for
the full list.

`langchain`, `langgraph`, `langsmith`, and `solace_agent_mesh` each
hand-roll that framework's own core mechanic in pure Python, high-level
to low-level across their 50 levels the same way `architecture`'s
categories run low-to-high (see below) — just labeled from the
opposite end, since these start from "the framework's foundational
idea" and end at "its most granular implementation detail," with a
`<category>_master` achievement on the final (`category_level=50`)
exercise. Their first five levels (the category's original scope
before each was expanded from 5 to 50) set up the framework's
foundational mechanics: `langchain` covers a minimal `Runnable`/`__or__`
chain-composition pipe, a `PromptTemplate` that fails loudly on a
missing variable, extracting a JSON object embedded in surrounding
prose, the mutable-default-argument trap resurfacing in a
`ConversationMemory` class, and `RunnableParallel` branch merging
without a key collision. `langgraph` covers a minimal node/edge graph
executor, merging into shared state instead of replacing it, a
conditional edge's fallback route, a retry cycle's max-iteration guard,
and checkpoint timing (snapshot after a node completes, not before).
`langsmith` covers a tracer's before/after timing pair, nesting spans
into a real tree via an active-span stack, keeping a run's status field
consistent with what actually happened in its exception handler,
normalizing both sides of an exact-match evaluator, and per-example
regression detection between two evaluation runs (not just comparing
aggregate scores). `solace_agent_mesh` (based on
https://docs.solace.com/Agent-Mesh/agent-mesh.htm) covers an entrypoint
dispatcher that must translate every transport into one common task
shape, agent-card capability matching for delegation (rather than
picking any registered agent), hierarchical topic-based A2A message
delivery (a parent-topic subscriber must still receive a more specific
child topic's messages, not just an exact match), an agent reasoning
loop that has to thread a tool's result back into the conversation or
it re-requests the same tool call forever, and isolating one
misbehaving tool call (via `try`/`except` per call) so it can't abort
an entire batch — a hand-rolled stand-in for Solace's real Secure Tool
Runtime's subprocess-level sandboxing. The remaining 45 levels in each
category go on to cover further mechanics of that same framework in
increasing granularity (e.g. `langchain` continues into retries,
fallbacks, batching, streaming, caching, and tool-argument coercion;
`solace_agent_mesh` continues into entrypoint auth, wildcard topic
matching, delegation trust boundaries, and Secure Tool Runtime session
isolation) — see the individual lesson YAML files under
`content/ai/lessons/` for the full list.

`microsoft_agent_365` is the one **`requires_code=False`** category in
this track — Microsoft's Agent 365 and its AI Agent Control Tower are
enterprise governance tooling (agent identity/registry, access control,
observability, lifecycle management) with no mechanic to hand-code, so
it's conceptual, comprehension-check content instead, the same shape as
every `architecture` exercise (see "Comprehension-check exercises"
below). Its 5 exercises run broadest-to-most-concrete: the agent-sprawl
problem, the four governance pillars as a framework, first-class agent
identity, observability/anomaly detection, and a full lifecycle
walkthrough of one concrete agent.

`app/execution/registry.py` maps `"ai"` to the same engine *class* as
`"python"` (`ENGINE_FACTORIES["ai"]` is the same factory as
`ENGINE_FACTORIES["python"]`) rather than a separate implementation,
since there's nothing language-specific to execute differently;
`app/execution/errors.py`'s `translate_error()` treats `"ai"`
identically to `"python"` for the same reason. The registry holds no
instances -- `create_engine(language)` builds one and
`AppState.execution_engine(language)` caches it per session, the same
way `AppState` already owns the per-language `ExerciseEngine`/
`QuizEngine`. This one factory serves the track's other 8 categories
fine even though `microsoft_agent_365` never asks for it —
`requires_code` is checked per-exercise, not per-track (see
"Comprehension-check exercises").

`architecture` (10 categories — `event_driven_architecture`,
`microservices`, `cqrs`, `saga_pattern`, `strangler_fig`,
`domain_driven_design`, `hexagonal_architecture`, `api_gateway`,
`circuit_breaker`, `idempotency`, 5 exercises each, 50 exercises total)
is the one track with **`requires_code=False`** on every exercise — see
"Comprehension-check exercises" below for what that changes about
`lesson_screen.py`. Each of the 10 topics runs low-to-high-level across
its 5 exercises rather than being a single overview page: `category_
level` 1 introduces the pattern, 2-4 go progressively deeper into its
real mechanics and failure modes, and `category_level` 5 (carrying that
topic's `<category>_master` achievement) is always a deliberate "when
this pattern is overkill" capstone — a recurring theme across this
track's content, since every pattern here earns its cost only once its
specific underlying problem is actually present.

### Comprehension-check exercises (`requires_code=False`)

`Exercise.requires_code: bool = True` and `Exercise.comprehension_check:
list[QuizQuestion]` (in `app/engine/exercise.py`) exist for any exercise
where the user reads an explanation/example but never edits or runs
code — every exercise in the `architecture` track, plus the `ai`
track's `microsoft_agent_365` category. The YAML supplies plain
mappings (`question`/`options`/`correct`/`explanation`); `Exercise.
__post_init__` parses them into the same `QuizQuestion` dataclass the
Quiz Bank uses (ids derived as `<exercise_id>_check_<n>`), so a
malformed question fails when the file loads, with the exercise id in
the error, not when a button is clicked. `lesson_screen.py`'s
`_ExerciseController` branches on `exercise.requires_code` per exercise
in `__init__` (not per track): when `True`, it builds the code editor +
Run button + Output card and calls `state.execution_engine(exercise.
language)`; when `False`, `self.engine` is set to `None`, no engine or
`check_toolchain()` lookup happens at all, and `build_view()` renders a
"Comprehension Check" card instead — the shared `app/ui/components.
MultipleChoiceCard` widget, the same one `quiz_screen.py` renders, with
each question's options shuffled via `quiz_engine.shuffle_options()`.
Answering every question correctly in one pass calls the same
`_on_success()` every code exercise uses (same XP/achievement/category-
unlock flow); any wrong answer requires retrying the whole check from
the start via a "Try Again" button. This is why `architecture` needs no
entry at all in `app/execution/registry.py`'s `ENGINE_FACTORIES` —
nothing in the app ever attempts to execute its content. `ai`'s
`microsoft_agent_365` category doesn't need its own registry entry
either, but for a different reason: it simply never asks for an engine,
even though `"ai"` already has a (shared) factory the track's other 8
categories depend on.

### Run evaluation (`app/engine/run_evaluation.py`)

"Did the user pass?" is a pure function, `evaluate_run(result,
exercise, code, input_value) -> RunOutcome`, with no Flet in it. It
folds `ExecutionResult` flags, `translate_error()`/
`extract_error_line_number()`, `validate_output()`,
`validate_contains()` and `diff_output()` into one `Verdict`
(`BLOCKED`, `TIMED_OUT`, `ERROR`, `WRONG_OUTPUT`, `MISSING_PATTERNS`,
`PASSED`) plus the message, expandable raw detail, and the
`activity_log` event type to record (only the three genuine failure
verdicts map to one). `lesson_screen.py`'s `_render_outcome()` just
paints it. `tests/test_run_evaluation.py` covers every verdict.

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

The engine call itself is pure and stateless; `app/ui/app_state.py`'s
`resolve_daily_refresher()` is the layer that makes "today's refresher"
actually stable across visits — it checks `ProgressStore.
get_daily_refresher_picks(language, today)` first and only calls the
engine (then persists the result via `save_daily_refresher_picks`) when
nothing's been picked yet for that calendar day. `count` is read from
`Settings.daily_refresher_size` (configurable from the Settings screen,
`_build_daily_refresher_card`), defaulting to 5; changing it only
affects the *next* freshly-generated set, since an already-persisted
day's picks are returned unchanged regardless of the current setting.

**Spaced review slot.** `resolve_daily_refresher()` also reserves up to
`_REVIEW_SLOT_COUNT` (1) of the set's slots for the most overdue item
from the spaced-repetition queue (below) before filling the rest with
fresh, never-completed picks from the engine. The reservation only
happens when something is actually due — `review_slots = min
(_REVIEW_SLOT_COUNT, count)`, but `fresh_count = count - len
(review_exercises)`, so a freshly-started track fills every slot with
fresh picks, unaffected. A review pick is, by definition, already in
`completed_ids`, so it shows as done the moment it appears in that
day's set — the value is the re-exposure, and passing it again pushes
its next review further out.

### Root route and back navigation

Flutter's own root route `/` (the browser's initial URL, or where a
fully unwound back stack lands on Android) is mapped by
`app_window.build_view_for_route()` to the picker, or to `/setup` on a
first run. `go_back()` with an empty Python history stack goes to the
picker if not already there; only on desktop (not web, not mobile) does
a further back close the window, since there is no window to close
elsewhere. Anything else unknown still logs and shows the "Unknown
screen" view. Tests: `tests/test_app_window_routes.py`.

### Keyboard shortcuts (`app/ui/shortcuts.py`)

`Shortcuts().bind(spec, handler).install(page)` sets
`page.on_keyboard_event` to a dispatcher keyed by a normalised spec
(`key_spec()`: lower-case key, modifiers first -- "ctrl+enter", "3",
"escape"; handlers may be sync or async). `app_window.route_change()`
clears the page handler before building every view and, if the view
installed none, binds a default **Escape = back**. Bindings today:

- Lesson: Ctrl+Enter run, Ctrl+H hint, Ctrl+R reset, Ctrl+B bookmark,
  Ctrl+N next exercise (after a pass), Esc back. Ctrl-combos only, since
  plain keys would fire while typing in the editor.
- Quiz: 1-8 pick an option (`MultipleChoiceCard.select_option()`),
  Enter / Space / Right advance (`advance()`), Esc back.
- Hub: 1-7 open the tiles in display order, Esc to the track picker.
- Everywhere else: Esc back.

Each of those screens prints its bindings in a muted help line built by
`Shortcuts.describe()`. Tests: `tests/test_shortcuts.py`.

### Recurring errors (`app/engine/error_insights.py`)

`ProgressStore.get_recent_errors(language, days)` returns the
`(lesson_id, stderr_tail)` of every `attempt_error` row in the window;
`summarize_errors(rows, engine, language)` buckets them by the same
friendly one-liner `translate_error()` shows in the lesson, counts each
bucket, and collects the affected exercises' concept tags. The Progress
screen's "Recurring errors, last 30 days" card lists the top five with
a count badge and a Practice button (an unlocked, unfinished exercise
sharing the bucket's top tags; else the most recently affected
exercise). Pure function, tested in `tests/test_error_insights.py`.

### Weekly goal and streak freezes

`Settings.weekly_goal` (default 10, chosen on the Settings screen) is
the number of exercises per local Monday-to-Sunday week. `ProgressStore.
count_completions_this_week(language)` buckets `lesson_completions`
into local days in Python (timestamps are UTC) and counts the current
week; the hub banner shows `done/goal` as a pill and the Progress
screen's "This week" card shows it as a ring.

Streak freezes live in `profile.freeze_tokens` (added by
`_COLUMN_MIGRATIONS` via `ALTER TABLE` when missing). `record_play_today()`
earns one token each time the streak reaches a multiple of
`STREAK_FREEZE_EVERY` (7), holding at most `STREAK_FREEZE_MAX` (3), and
spends one automatically when the gap since the last play is exactly
two days -- the streak continues as if the missed day had been played.
`get_streak_days()` applies the same rule for display, so a streak the
user can still rescue is never shown as 0. Both events are written to
`activity_log` (`streak_freeze_earned` / `streak_freeze_used`). A gap of
three or more days breaks the streak and keeps the tokens.

### Personal-best timer

`lesson_screen.py` notes `time.monotonic()` when an exercise opens and,
on a pass, stores the elapsed whole seconds via `ProgressStore.
record_solve_time()` (`solve_times` table, one row per solve; returns
True for a new best). The header shows a "Best 1m 35s" chip when a time
exists, the reward card shows this solve's time against the best, and
list screens (`build_exercise_list_view`) show the best per row using
one `get_best_solve_times(language)` query rather than one per row.
`components.format_duration()` renders seconds as `7s` / `1m 35s` /
`1h 2m`.

### Spaced repetition (`review_schedule`, `/review`)

Every passed exercise enters a per-track review schedule -- a
simplified SM-2 kept in `ProgressStore`'s `review_schedule` table
(`interval_days`, `ease`, `due_date` as a *local* ISO date,
`review_streak`). `schedule_review(language, lesson_id, passed)`:

- pass -> streak+1; interval is `REVIEW_FIRST_INTERVAL` (3 days) on the
  first pass, `REVIEW_SECOND_INTERVAL` (7) on the second, then
  `round(previous * ease)` capped at `REVIEW_MAX_INTERVAL` (120); ease
  creeps up by `REVIEW_EASE_STEP` to at most `REVIEW_MAX_EASE`;
- fail -> streak 0, due tomorrow, ease drops by `REVIEW_EASE_STEP` to
  at least `REVIEW_MIN_EASE`.

`lesson_screen.py` calls it with `passed=True` from `_on_success()`
(the reward card then shows "Next review in N days") and with
`passed=False` from `_render_outcome()` on the first genuine failure
of a visit **only if the exercise had already been completed before**
(`_was_completed`) -- a first attempt at new material never counts as a
failed review. The header shows a "Review due" / "Review in Nd" chip
when a schedule row exists.

Reads: `get_due_reviews(language, today, limit)` (most overdue first),
`count_due_reviews()`, `count_upcoming_reviews(days)`,
`get_review_state()`. `AppState.due_review_exercises()` maps the due
ids to `Exercise`s. Surfaces: the hub's **Review Queue** tile (count
due / this week), the `/review` screen (`app/ui/review_screen.py`,
built on `build_exercise_list_view` with a summary card; "Next
exercise" after a pass there advances to the next due item), the
Progress screen's "Review schedule" card and banner pill, and the Daily
Refresher's review slot.

Databases created before this table existed are backfilled once on
open (`_BACKFILL_REVIEWS`, `INSERT OR IGNORE`): every existing
completion gets its first review 14 days after `completed_at`, the old
age-based rule, so nothing silently disappears from review. The table
is exported/imported and cleared by `reset_progress()` like every other.
Tests: `tests/test_progress_store.py` (spaced repetition section),
`tests/test_app_state.py`.

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

`app/engine/lesson_engine.py`'s `ALWAYS_UNLOCKED_LANGUAGES =
{"architecture", "ai"}` is checked unconditionally as the very first
branch inside `is_unlocked()`, before even the Android-specific
`MOBILE_ALWAYS_UNLOCKED_LANGUAGES` check — every exercise in both
tracks is unlocked and completable in any order from the start,
regardless of platform. This is a deliberate product decision distinct
from the Android bypass: neither track's content has a genuine
prerequisite-chain reason to gate progression (Architecture's 5-page
topics build low-to-high conceptually, but nothing about the app
mechanics requires finishing page 2 before browsing page 4), so gating
them the normal way would have added friction with no corresponding
benefit.

### Quiz Bank

A standalone multiple-choice question bank per language
(`content/<language>/quiz/quiz_questions.yaml`), loaded by `QuizEngine`.
`start_session(count)` returns a freshly shuffled subset each time —
both question order and each question's own answer-option order are
re-randomized — so no two playthroughs look the same and the correct
answer isn't always in the same position. `start_session_for_tags
(tags, count)` is the same shuffle, narrowed to questions sharing at
least one of `tags` — `quiz_screen.py`'s "Retry missed concepts" button
(visible only when at least one question was missed) calls this
directly with the session's accumulated `missed_tags`.

`quiz_screen.py`'s `_on_select()` calls `ProgressStore.
record_quiz_answer(language, question_id, concept_tags, is_correct)`
for every question answered — a separate, per-question record from
`record_quiz_attempt()`'s per-session score/total summary, since a
per-concept breakdown needs finer granularity than a session total can
provide. `ProgressStore.get_concept_accuracy(language)` aggregates
these into `tag -> (correct, total)`, powering the Progress screen's
"Weakest concepts" panel (`_build_weakest_concepts_card` in
`progress_screen.py`) — concepts below `_MIN_CONCEPT_SAMPLES` (2)
recorded answers are excluded, so a single unlucky miss on a
rarely-asked concept doesn't look identical to a genuinely weak spot;
the worst `_WEAKEST_CONCEPTS_LIMIT` (5) surface, each with a "Practice"
button via `recommend_practice_for_tags()`.

### Exercise search

`ExerciseEngine.search(query, difficulty=None, limit=50)`
(`app/ui/search_screen.py`, routed at `/search`, linked from the track
hub) is a flat, case-insensitive substring match across `title`,
`objective`, and `concept_tags`, optionally narrowed to one
`difficulty`, in the engine's own level order. An empty query with no
difficulty filter matches everything (capped at `limit`) rather than
nothing, so browsing by difficulty alone works without typing anything.
Results reuse `is_unlocked()`/`completed_ids` the same way the category
browser does, rendering a locked result as non-clickable and dimmed
rather than omitting it — a search hit for something not yet reachable
is still useful information (the user still went looking for it, they
just haven't unlocked it yet).

### Meta-achievements

`app/progress/achievements.py` awards cross-cutting badges — earned
from milestones spanning multiple exercises/sessions, not one
exercise's own YAML-declared `achievement` field — through the exact
same idempotent `ProgressStore.award_badge()` exercise-declared
achievements use, so the Progress screen's badge list and export/import
never need to know which kind a given badge is.
`evaluate_lesson_completion_achievements(progress, engine, language,
category)`, called from `lesson_screen.py`'s `_on_success()` right
after `record_play_today()` (streak-based badges need `streak_days` to
already reflect today; `record_play_today()` is only ever called from
the two completion paths -- finishing an exercise or a quiz -- never
from merely opening a screen), checks for: `first_completion` (this
language's very first lesson ever completed), `category_complete_
<category>` (every level in `category` now complete), and `streak_<N>`
for `N` in `STREAK_MILESTONES` (`[3, 7, 14, 30, 100]`).
`evaluate_quiz_achievements(progress, language, score, total)`, called
from `quiz_screen.py`'s `_show_results()`, awards `perfect_quiz` when
`score == total`. Both return the ids of whatever was *newly* awarded
this call, which the caller folds into the same "Achievement unlocked"
text an exercise-declared achievement already shows.

### Notes and bookmarks

Two small per-`(language, lesson_id)` tables: `exercise_notes` (a
free-text `note`, upserted via `ProgressStore.save_note()` — an
emptied note is deleted outright rather than kept as a stored blank
row, so "never wrote one" and "wrote one, then cleared it" look
identical to every reader) and `bookmarks` (`is_bookmarked()`/
`set_bookmarked()`/`get_bookmarked_lesson_ids()`, ordered most-recently
bookmarked first). `lesson_screen.py` renders a "★ Bookmarked"/"☆
Bookmark" toggle button in the header and a collapsible "Your Notes"
card with a multiline field and an explicit Save button (no
autosave-on-blur, to keep the write path simple and visible). The track
hub's "📌 Revisit later" section (`_build_revisit_later_section` in
`track_hub.py`) lists every bookmarked exercise for the current
language, hidden entirely when there are none.

### Activity heatmap

`ProgressStore.get_daily_activity_counts(language, days=84)` groups
`activity_log` rows by day (`substr(timestamp, 1, 10)`) into `date ->
count`, for the last `days` days (84 = 12 weeks). `progress_screen.py`'s
`_build_activity_heatmap_card` renders this as a GitHub-style grid —
one `ft.Column` of 7 small colored squares per week, aligned so each
column is a genuine Monday-to-Sunday week (`start -= timedelta(days=
start.weekday())`) — with `_heatmap_color()` mapping a day's event
count to one of four existing theme colors (no new palette needed):
`theme.bg` for zero, `theme.text_muted` for one, `theme.primary` for
2-3, `theme.success` for 4+.

### User content overlay

`ExerciseEngine.__init__` also accepts `custom_content_dir` (defaulting
to `<data_dir>/custom/<language>/lessons`, via `app/config/
platform_paths.py`'s `resolve_platform_data_dir()`), loaded strictly
*after* `content_dir` in `_load()`. Since `data/` is already gitignored
(progress.sqlite3/settings.json already live there), anything dropped
into `data/custom/<language>/lessons/*.yaml` survives a `git pull`
untouched, letting a user add personal exercises without ever touching
the tracked `content/` tree. Both directories share one id namespace —
`_load()` tracks which path each id came from and raises `ValueError`
immediately on a collision (built-in vs. custom, or two custom files),
rather than letting one silently shadow the other depending on
directory iteration order.

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

`diff_output(expected, actual)` builds a readable expected-vs-actual
comparison for a failed `validate_output()` — every space/tab rendered
as a visible character (`·`/`→`) and the first genuinely differing line
called out up front, via `difflib.unified_diff()` — surfaced in
`lesson_screen.py`'s "Show expected vs. actual" details panel instead of
leaving a wrong-output failure as a bare pass/fail. Only computed when
the exercise uses a fixed `expected_output` string, not
`expected_output_pattern` (a diff against a regex wouldn't mean
anything).

### Adaptive practice

After 3 failed attempts in a row on the same exercise
(`ProgressStore.get_recent_failure_count()`), a dismissible suggestion
offers up to 3 related exercises sharing a `concept_tags` value
(`ExerciseEngine.recommend_practice()`). It never blocks retrying,
hints, or continuing — purely additive. The quiz results screen offers
the same kind of suggestion from the union of tags across every question
missed that session (`recommend_practice_for_tags()`), tracked only in
memory for the session. A "Retry missed concepts" button on the results
screen (visible only when at least one question was missed) re-runs
`QuizEngine.start_session_for_tags(missed_tags)` directly — a full quiz
session over every question sharing a missed tag, not just the exact
questions gotten wrong, since `concept_tags` usually groups more than
one related question together.

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

### Export and import progress

The Settings screen (`app/ui/settings_screen.py`'s `_build_backup_card`)
lets a user back up or restore progress as a single JSON file, covering
every language track at once. `ProgressStore.export_progress()`
(`app/progress/store.py`) reads every row of every table listed in
`_EXPORT_TABLES` via `sqlite3.Row` and dynamic column names (so the
export/import code never hardcodes the schema twice), producing
`{"version": PROGRESS_EXPORT_VERSION, "exported_at": ..., "tables":
{...}}`. `import_progress()` checks the version field first (refusing
to import a file from a future/incompatible export format) and then
replaces every table's contents — `DELETE` all rows, re-`INSERT` every
row from the file — inside one atomic transaction, so an import is
always all rows or none, never a partial merge.

On desktop, clicking Export goes straight to `ft.FilePicker().
save_file(...)`. On mobile (`page.platform.is_mobile()`), a choice
dialog offers "Save to Device" (the same `save_file` picker) or
"Share…" (`ft.Share().share_files([ft.ShareFile.from_bytes(...)])`),
which hands the exported JSON to the OS's native share sheet — Gmail
included, if the user has it installed — rather than the app trying to
target Gmail specifically, since Flet's `Share` service has no API to
name a particular destination app; letting the user pick from the real
OS share sheet is both the only available mechanism and arguably the
better UX anyway. Import always shows a blocking confirmation dialog
first (explicitly warning that current progress will be permanently
overwritten) before calling `import_progress()`; on success it
navigates to `/languages`, forcing every view to rebuild against the
newly-imported data rather than leaving any stale in-memory progress
numbers visible from before the import.

### Android build (Python-only)

`build_apk.sh` builds a real Android APK via `flet build apk`. A Flutter
SDK and JDK are **not** prerequisites: when neither is on PATH (or in
`FLUTTER_HOME`), `flet build` downloads the Flutter version pinned by the
installed flet (`flet.version.flutter_version`, 3.44.8 today) into
`~/flutter/<version>` and a JDK into `~/java` on the first run -- several
minutes and roughly a gigabyte, reused by every later build. The Android
SDK/NDK is fetched by the Flutter toolchain the same way; see
https://flet.dev/docs/publish/android for the details. Support is deliberately
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
