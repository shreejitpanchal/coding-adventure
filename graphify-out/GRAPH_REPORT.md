# Graph Report - coding-adventure  (2026-08-23)

## Corpus Check
- Corpus is ~20,306 words - fits in a single context window. You may not need a graph.

## Summary
- 523 nodes · 1036 edges · 37 communities (33 shown, 4 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 74 edges (avg confidence: 0.93)
- Token cost: 129,420 input · 55,466 output

## Community Hubs (Navigation)
- Categories & Language Registry
- Exercise Content Model & Settings
- Execution Engine Contract
- Output Validation & Error Translation
- Progress Store & XP Leveling
- Cross-Cutting Language Concepts
- Quiz Screen UI
- Core Language Refresher Lessons
- App Data Directory Resolution
- Dict Grouping & Deque Lessons
- Quiz Engine
- Concurrency & Async Lessons
- Aliasing & Sorting Gotcha Lessons
- Dict Iteration & Collections Lessons
- Classes & Inheritance Gotcha Lessons
- Mutable Defaults & Decorators Lessons
- Exception Handling Lessons
- Float Precision Lessons
- Functools Memoization Lessons
- Heapq, Bisect & Sets Lessons
- Closures & Late Binding Lessons
- Identity vs Equality Lessons
- Toolchain Detection
- Context Manager Lessons
- Pathlib Lessons
- Itertools Lessons
- Typing Hints Lessons
- run.sh Launcher Script
- Project Root
- Flet Dependency
- Pytest Dependency

## God Nodes (most connected - your core abstractions)
1. `Python Idioms & Gotchas Quiz Bank` - 51 edges
2. `AppState` - 48 edges
3. `CLAUDE.md — Coding Adventure Architecture Guide` - 37 edges
4. `ExerciseEngine` - 30 edges
5. `ProgressStore` - 30 edges
6. `_ExerciseController` - 25 edges
7. `RunHandle` - 23 edges
8. `scaled()` - 23 edges
9. `Gotchas` - 21 edges
10. `Exercise` - 20 edges

## Surprising Connections (you probably didn't know these)
- `Lesson: Cutting Boilerplate with @dataclass` --semantically_similar_to--> `Exercise`  [INFERRED] [semantically similar]
  content/python/lessons/core_refresher_05_dataclasses.yaml → app/engine/exercise.py
- `CLAUDE.md — Coding Adventure Architecture Guide` --references--> `QuizQuestion`  [EXTRACTED]
  CLAUDE.md → app/engine/quiz.py
- `CLAUDE.md — Coding Adventure Architecture Guide` --references--> `QuizEngine`  [EXTRACTED]
  CLAUDE.md → app/engine/quiz_engine.py
- `CLAUDE.md — Coding Adventure Architecture Guide` --references--> `validate_contains()`  [EXTRACTED]
  CLAUDE.md → app/engine/validator.py
- `CLAUDE.md — Coding Adventure Architecture Guide` --references--> `validate_output()`  [EXTRACTED]
  CLAUDE.md → app/engine/validator.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Language execution engines implementing the ExecutionEngine ABC** — app_execution_base_executionengine, app_execution_python_engine_module, app_execution_java_engine_module, app_execution_cpp_engine_module, app_execution_spring_engine_module [EXTRACTED 1.00]
- **Concurrency & Async lesson category** — content_python_lessons_concurrency_async_01_gather_order_lesson, content_python_lessons_concurrency_async_02_thread_lock_lesson, content_python_lessons_concurrency_async_03_thread_pool_lesson, content_python_lessons_concurrency_async_04_asyncio_lock_lesson, content_python_lessons_concurrency_async_05_wait_for_timeout_lesson, readme_category_concurrency_async [EXTRACTED 1.00]
- **Data Structures & Algorithms lesson category** — content_python_lessons_data_structures_01_defaultdict_lesson, content_python_lessons_data_structures_02_counter_lesson, content_python_lessons_data_structures_03_deque_lesson, content_python_lessons_data_structures_04_heapq_lesson, content_python_lessons_data_structures_05_bisect_lesson, content_python_lessons_data_structures_06_set_operations_lesson, readme_category_data_structures_algorithms [EXTRACTED 1.00]
- **Gotcha Gauntlet Lesson Sequence** — content_python_lessons_gotcha_gauntlet_02_exception_swallowing_lesson, content_python_lessons_gotcha_gauntlet_03_mutable_class_attribute_lesson, content_python_lessons_gotcha_gauntlet_04_rounding_precision_lesson, content_python_lessons_gotcha_gauntlet_05_dict_mutation_during_iteration_lesson, content_python_lessons_gotcha_gauntlet_06_missing_super_init_lesson [EXTRACTED 1.00]
- **Idioms Gotchas Lesson Sequence** — content_python_lessons_idioms_gotchas_01_mutable_default_arg_lesson, content_python_lessons_idioms_gotchas_02_late_binding_closure_lesson, content_python_lessons_idioms_gotchas_03_is_vs_equals_lesson, content_python_lessons_idioms_gotchas_04_float_precision_lesson, content_python_lessons_idioms_gotchas_05_aliasing_vs_copying_lesson, content_python_lessons_idioms_gotchas_06_sort_returns_none_lesson [EXTRACTED 1.00]
- **Stdlib Deep Dive Lesson Sequence** — content_python_lessons_stdlib_deep_dive_01_itertools_chain_lesson, content_python_lessons_stdlib_deep_dive_02_lru_cache_lesson, content_python_lessons_stdlib_deep_dive_03_reduce_lesson, content_python_lessons_stdlib_deep_dive_04_pathlib_lesson, content_python_lessons_stdlib_deep_dive_05_typing_hints_lesson, content_python_lessons_stdlib_deep_dive_06_contextlib_suppress_lesson [EXTRACTED 1.00]

## Communities (37 total, 4 thin omitted)

### Community 0 - "Categories & Language Registry"
Cohesion: 0.06
Nodes (64): CategoryMeta, get_category_meta(), Display metadata (title, icon, color) for exercise categories, used by the…, get_language(), LanguageInfo, The set of language tracks the app knows about, and which ones have real…, AppState, Shared app state: settings, progress store, per-language exercise/quiz engines… (+56 more)

### Community 1 - "Exercise Content Model & Settings"
Cohesion: 0.06
Nodes (36): platform_paths.py, settings.py, CATEGORY_META, DEFAULT_META, Exercise, The Exercise data model. Content is data, not code -- see…, ExerciseEngine, Path (+28 more)

### Community 2 - "Execution Engine Contract"
Cohesion: 0.08
Nodes (30): ABC, ExecutionEngine, ExecutionResult, Shared execution contract every per-language engine implements. Framing is…, Lets the UI cancel a run that's in progress (e.g. an infinite loop)., One concrete subclass per language track (python_engine.PythonEngine,…, RunHandle, CppEngine (+22 more)

### Community 3 - "Output Validation & Error Translation"
Cohesion: 0.08
Nodes (25): Exercise validation: checks behavior/output, not exact code formatting., True if `code` contains every required pattern. Each pattern is matched as a…, Compares output, optionally substituting what the user typed into a template. -…, validate_contains(), validate_output(), extract_error_line_number(), _last_exception_type(), Translates raw interpreter/compiler output into concise, professional… (+17 more)

### Community 4 - "Progress Store & XP Leveling"
Cohesion: 0.08
Nodes (13): _level_from_xp(), _now(), PlayerLevel, ProgressStore, Path, SQLite-backed progress, gamification, and activity tracking -- one…, Returns True if newly awarded, False if already had it., Resets to 0 automatically once the exercise is passed -- powers the "keep… (+5 more)

### Community 5 - "Cross-Cutting Language Concepts"
Cohesion: 0.13
Nodes (23): Asyncio, Comprehensions, Concurrency, Enums, Futures, Locks, Race Conditions, Slicing (+15 more)

### Community 6 - "Quiz Screen UI"
Cohesion: 0.20
Nodes (6): build_quiz_view(), Control, Page, View, _QuizController, Button

### Community 7 - "Core Language Refresher Lessons"
Cohesion: 0.12
Nodes (18): comprehensions, lists, Lesson: Loop to Comprehension, args, functions, kwargs, Lesson: Accepting Any Number of Arguments, decorators (+10 more)

### Community 8 - "App Data Directory Resolution"
Cohesion: 0.21
Nodes (13): Path, Resolves the real, writable directory this app's data lives in., Returns the OS-appropriate writable data directory, creating it if it doesn't…, resolve_platform_data_dir(), get_data_dir(), get_db_path(), get_settings_path(), is_first_run() (+5 more)

### Community 9 - "Dict Grouping & Deque Lessons"
Cohesion: 0.17
Nodes (16): collections module, dictionaries, Lesson: Grouping Without Manual Key Checks, counting, Lesson: Tallying with Counter, deque, performance (algorithmic complexity), Lesson: O(1) Queue Operations with deque (+8 more)

### Community 10 - "Quiz Engine"
Cohesion: 0.21
Nodes (7): Path, QuizEngine, Loads a language track's quiz questions from YAML. Adding a question means…, A freshly randomized set of questions for one quiz playthrough -- which…, QuizQuestion, The QuizQuestion data model. Quiz content is data, not code -- see…, Collection

### Community 11 - "Concurrency & Async Lessons"
Cohesion: 0.27
Nodes (13): asyncio, concurrency, Lesson: Running Coroutines Concurrently, Keeping Order, race conditions, threading, Lesson: Protecting a Shared Counter with a Lock, futures, Lesson: Running I/O-Bound Work Concurrently (+5 more)

### Community 12 - "Aliasing & Sorting Gotcha Lessons"
Cohesion: 0.30
Nodes (12): Idioms Gotchas Master Achievement, Idioms Gotchas Progress Achievement, Aliasing, Copying, Lists, Sorting, The Backup That Wasn't, The Silent None: list.sort() Returns Nothing (+4 more)

### Community 13 - "Dict Iteration & Collections Lessons"
Cohesion: 0.23
Nodes (12): Collections, Counting, Deque, Dictionaries, Iteration, Performance, The Dict That Changed Size Mid-Loop, What does collections.defaultdict(list) do the first time a new key is accessed? (+4 more)

### Community 14 - "Classes & Inheritance Gotcha Lessons"
Cohesion: 0.29
Nodes (11): Gotcha Gauntlet Master Achievement, Classes, Dataclasses, Inheritance, The Shopping Cart Shared By Every Customer, The Subclass That Forgot Its Parent, What does @dataclass automatically generate from annotated fields?, A mutable list assigned directly in a class body (not in __init__) is: (+3 more)

### Community 15 - "Mutable Defaults & Decorators Lessons"
Cohesion: 0.24
Nodes (11): Args, Decorators, Functions, Kwargs, Mutable Defaults, The Sticky Shopping Cart, What's the risk of `def f(x=[])`?, When are Python default argument values evaluated? (+3 more)

### Community 16 - "Exception Handling Lessons"
Cohesion: 0.39
Nodes (9): Stdlib Deep Dive Master Achievement, Contextlib, Debugging, Exceptions, Gotchas, The Bare Except That Hid a Real Bug, Suppressing an Expected Exception Cleanly, What does `with contextlib.suppress(ValueError):` do? (+1 more)

### Community 17 - "Float Precision Lessons"
Cohesion: 0.50
Nodes (9): Decimal, Floats, Precision, The Price That Rounded the Wrong Way, 0.1 + 0.2 Is Not Quite 0.3, Why does `0.1 + 0.2 == 0.3` return False in Python?, What's the right way to compare floats for 'close enough' equality?, Why can round(2.675, 2) give 2.67 instead of the expected 2.68? (+1 more)

### Community 18 - "Functools Memoization Lessons"
Cohesion: 0.39
Nodes (8): Functools, Memoization, Recursion, Reduce, Memoizing a Recursive Function, Folding a List Into One Value, What does @lru_cache do to a function?, What does functools.reduce(func, iterable, initial) do?

### Community 19 - "Heapq, Bisect & Sets Lessons"
Cohesion: 0.29
Nodes (7): Algorithms, Bisect, Heapq, Sets, What does heapq.nsmallest(3, data) do compared to sorted(data)[:3]?, What does bisect.insort do?, What's the benefit of using a set for membership testing over a list?

### Community 20 - "Closures & Late Binding Lessons"
Cohesion: 0.80
Nodes (5): Closures, Late Binding, The Closure That Forgot Everything, Why does a lambda created inside a for-loop often capture the 'wrong' value?, How do you fix late-binding in a loop-created lambda?

### Community 21 - "Identity vs Equality Lessons"
Cohesion: 0.80
Nodes (5): Equality, Identity, Same Contents, Different Objects, What does `is` check in Python?, Two separately built lists with identical contents -- what does `a is b` return?

### Community 22 - "Toolchain Detection"
Cohesion: 0.67
Nodes (3): check_toolchain(), Detects whether a language track's real local toolchain is on PATH. Used by the…, ToolchainStatus

### Community 23 - "Context Manager Lessons"
Cohesion: 0.50
Nodes (4): Context Managers, With Statement, What two dunder methods make a class usable with `with`?, Does __exit__ still run if an exception is raised inside a with block?

### Community 24 - "Pathlib Lessons"
Cohesion: 0.83
Nodes (4): Filesystem, Pathlib, Paths as Objects, Not Strings, What's an advantage of pathlib.Path over manual string concatenation for paths?

### Community 25 - "Itertools Lessons"
Cohesion: 1.00
Nodes (3): Itertools, Chaining Iterables Without Concatenating, What does itertools.chain(a, b) do?

### Community 26 - "Typing Hints Lessons"
Cohesion: 1.00
Nodes (3): Typing, Adding Type Hints for Clarity and Tooling, Do Python type hints get enforced at runtime by default?

## Knowledge Gaps
- **67 isolated node(s):** `coding-adventure`, `run.sh script`, `Flet-only UI stack`, `YAML-as-content architecture pattern`, `Flat topic browser (no guided curriculum order)` (+62 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CLAUDE.md — Coding Adventure Architecture Guide` connect `Exercise Content Model & Settings` to `Categories & Language Registry`, `Execution Engine Contract`, `Output Validation & Error Translation`, `Progress Store & XP Leveling`, `Quiz Engine`?**
  _High betweenness centrality (0.200) - this node is a cross-community bridge._
- **Why does `AppState` connect `Categories & Language Registry` to `Exercise Content Model & Settings`, `Output Validation & Error Translation`, `Progress Store & XP Leveling`, `Quiz Screen UI`, `App Data Directory Resolution`, `Quiz Engine`?**
  _High betweenness centrality (0.184) - this node is a cross-community bridge._
- **Why does `README.md — Coding Adventure Project Overview` connect `Execution Engine Contract` to `Dict Grouping & Deque Lessons`, `Concurrency & Async Lessons`, `Core Language Refresher Lessons`?**
  _High betweenness centrality (0.108) - this node is a cross-community bridge._
- **Are the 22 inferred relationships involving `AppState` (e.g. with `Settings` and `ExerciseEngine`) actually correct?**
  _`AppState` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `ExerciseEngine` (e.g. with `Exercise` and `AppState`) actually correct?**
  _`ExerciseEngine` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `ProgressStore` (e.g. with `AppState` and `store()`) actually correct?**
  _`ProgressStore` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `coding-adventure`, `run.sh script`, `Flet-only UI stack` to the rest of the system?**
  _67 weakly-connected nodes found - possible documentation gaps or missing edges._