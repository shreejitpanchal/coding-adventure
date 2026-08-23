# Graph Report - coding-adventure  (2026-08-23)

## Corpus Check
- 44 files · ~31,298 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 580 nodes · 1050 edges · 42 communities (34 shown, 8 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 67 edges (avg confidence: 0.93)
- Token cost: 122,521 input · 52,509 output

## Community Hubs (Navigation)
- Categories & Language Registry
- Execution Engine Contract & Config
- Output Validation & Error Translation
- Progress Store & XP Leveling
- Exercise Content Model
- Functional Programming Lessons
- Packaging Lessons
- Dependency Management Lessons
- Gotcha Gauntlet & Idioms Concepts
- App Data Directory Resolution
- Recursion Lessons
- Thread Scheduling Lessons
- Quiz Screen UI
- Sync vs Async Lessons
- Quiz Engine
- Deployment Lessons
- Observability Lessons
- App Feature Overview
- Dict Grouping & Deque Lessons
- Concurrency & Async Lessons
- Aliasing & Sorting Gotcha Lessons
- Heapq, Bisect & Sets Lessons
- Exception Handling Lessons
- Float Precision Lessons
- Toolchain Detection
- Correlation ID Tracing
- Pathlib Lessons
- Comprehension Lessons
- run.sh Launcher Script
- Itertools Lessons
- Typing Hints Lessons
- Enum Lessons
- Project Root
- Flet Dependency
- Pytest Dependency
- PyYAML Dependency

## God Nodes (most connected - your core abstractions)
1. `AppState` - 48 edges
2. `CLAUDE.md — Coding Adventure Architecture Guide` - 37 edges
3. `ProgressStore` - 30 edges
4. `Gotchas` - 27 edges
5. `_ExerciseController` - 25 edges
6. `RunHandle` - 23 edges
7. `scaled()` - 23 edges
8. `ExerciseEngine` - 21 edges
9. `content/<language>/lessons/*.yaml` - 21 edges
10. `Exercise` - 20 edges

## Surprising Connections (you probably didn't know these)
- `Lesson: Cutting Boilerplate with @dataclass` --semantically_similar_to--> `Exercise`  [INFERRED] [semantically similar]
  content/python/lessons/core_refresher_05_dataclasses.yaml → app/engine/exercise.py
- `CLAUDE.md — Coding Adventure Architecture Guide` --references--> `AppState`  [EXTRACTED]
  CLAUDE.md → app/ui/app_state.py
- `CLAUDE.md — Coding Adventure Architecture Guide` --references--> `Exercise`  [EXTRACTED]
  CLAUDE.md → app/engine/exercise.py
- `CLAUDE.md — Coding Adventure Architecture Guide` --references--> `ExerciseEngine`  [EXTRACTED]
  CLAUDE.md → app/engine/lesson_engine.py
- `CLAUDE.md — Coding Adventure Architecture Guide` --references--> `QuizEngine`  [EXTRACTED]
  CLAUDE.md → app/engine/quiz_engine.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Dependency Management Lesson Progression** — content_python_lessons_dependency_management_01_detect_virtualenv_lesson, content_python_lessons_dependency_management_02_parse_requirement_line_lesson, content_python_lessons_dependency_management_03_version_string_comparison_lesson, content_python_lessons_dependency_management_04_importlib_metadata_lesson, content_python_lessons_dependency_management_05_lock_file_pin_lesson [INFERRED 0.95]
- **Deployment Lesson Progression** — content_python_lessons_deployment_01_env_var_defaults_lesson, content_python_lessons_deployment_02_feature_flag_boolean_parsing_lesson, content_python_lessons_deployment_03_graceful_shutdown_signal_lesson, content_python_lessons_deployment_04_health_check_lesson, content_python_lessons_deployment_05_idempotent_deploy_step_lesson [INFERRED 0.95]
- **Functional Programming Lesson Progression** — content_python_lessons_functional_programming_01_pure_functions_lesson, content_python_lessons_functional_programming_02_map_filter_lesson, content_python_lessons_functional_programming_03_function_composition_lesson, content_python_lessons_functional_programming_04_immutability_lesson, content_python_lessons_functional_programming_05_partial_application_lesson [INFERRED 0.95]
- **Category-Capstone Lessons Awarding a Mastery Achievement** — content_python_lessons_packaging_05_wheel_filename_parsing_lesson, content_python_lessons_recursion_05_accumulator_pattern_lesson, content_python_lessons_sync_vs_async_05_async_for_generator_lesson, content_python_lessons_thread_scheduling_05_thread_local_storage_lesson [INFERRED 0.85]
- **Lessons Demonstrating Recursion-Misuse Failure Modes** — content_python_lessons_recursion_01_missing_base_case_lesson, content_python_lessons_recursion_02_recursion_depth_limit_lesson, content_python_lessons_thread_scheduling_01_reentrant_lock_lesson [INFERRED 0.75]
- **Language execution engines implementing the ExecutionEngine ABC** — app_execution_base_executionengine, app_execution_python_engine_module, app_execution_java_engine_module, app_execution_cpp_engine_module, app_execution_spring_engine_module [EXTRACTED 1.00]
- **Gotcha Gauntlet Lesson Sequence** — content_python_lessons_gotcha_gauntlet_02_exception_swallowing_lesson, content_python_lessons_gotcha_gauntlet_03_mutable_class_attribute_lesson, content_python_lessons_gotcha_gauntlet_04_rounding_precision_lesson, content_python_lessons_gotcha_gauntlet_05_dict_mutation_during_iteration_lesson, content_python_lessons_gotcha_gauntlet_06_missing_super_init_lesson [EXTRACTED 1.00]
- **Idioms Gotchas Lesson Sequence** — content_python_lessons_idioms_gotchas_01_mutable_default_arg_lesson, content_python_lessons_idioms_gotchas_02_late_binding_closure_lesson, content_python_lessons_idioms_gotchas_03_is_vs_equals_lesson, content_python_lessons_idioms_gotchas_04_float_precision_lesson, content_python_lessons_idioms_gotchas_05_aliasing_vs_copying_lesson, content_python_lessons_idioms_gotchas_06_sort_returns_none_lesson [EXTRACTED 1.00]
- **Stdlib Deep Dive Lesson Sequence** — content_python_lessons_stdlib_deep_dive_01_itertools_chain_lesson, content_python_lessons_stdlib_deep_dive_02_lru_cache_lesson, content_python_lessons_stdlib_deep_dive_03_reduce_lesson, content_python_lessons_stdlib_deep_dive_04_pathlib_lesson, content_python_lessons_stdlib_deep_dive_05_typing_hints_lesson, content_python_lessons_stdlib_deep_dive_06_contextlib_suppress_lesson [EXTRACTED 1.00]

## Communities (42 total, 8 thin omitted)

### Community 0 - "Categories & Language Registry"
Cohesion: 0.06
Nodes (66): CategoryMeta, get_category_meta(), Display metadata (title, icon, color) for exercise categories, used by the…, get_language(), LanguageInfo, The set of language tracks the app knows about, and which ones have real…, AppState, Shared app state: settings, progress store, per-language exercise/quiz engines… (+58 more)

### Community 1 - "Execution Engine Contract & Config"
Cohesion: 0.06
Nodes (43): ABC, platform_paths.py, settings.py, CATEGORY_META, DEFAULT_META, ExecutionEngine, ExecutionResult, Shared execution contract every per-language engine implements. Framing is… (+35 more)

### Community 2 - "Output Validation & Error Translation"
Cohesion: 0.08
Nodes (25): Exercise validation: checks behavior/output, not exact code formatting., True if `code` contains every required pattern. Each pattern is matched as a…, Compares output, optionally substituting what the user typed into a template. -…, validate_contains(), validate_output(), extract_error_line_number(), _last_exception_type(), Translates raw interpreter/compiler output into concise, professional… (+17 more)

### Community 3 - "Progress Store & XP Leveling"
Cohesion: 0.08
Nodes (13): _level_from_xp(), _now(), PlayerLevel, ProgressStore, Path, SQLite-backed progress, gamification, and activity tracking -- one…, Returns True if newly awarded, False if already had it., Resets to 0 automatically once the exercise is passed -- powers the "keep… (+5 more)

### Community 4 - "Exercise Content Model"
Cohesion: 0.10
Nodes (10): Exercise, The Exercise data model. Content is data, not code -- see…, ExerciseEngine, Path, Loads one language track's exercises from YAML, kept separate from application…, category -> (done, total), done computed by the caller passing completed_ids in…, A small guided set for "today's refresher" -- round-robins the next unlocked,…, classes (+2 more)

### Community 5 - "Functional Programming Lessons"
Cohesion: 0.11
Nodes (23): Function Composition, Functional Programming, Functional Programming Master (Achievement), Functools, Higher-Order Functions, Immutability, Memoization, Partial Application (+15 more)

### Community 6 - "Packaging Lessons"
Cohesion: 0.11
Nodes (22): Decorators, Entry Points, Functions, Module Api, Packaging, Pyproject Toml, Semantic Versioning, Tomllib (+14 more)

### Community 7 - "Dependency Management Lessons"
Cohesion: 0.17
Nodes (18): Dependency Management, Dependency Management Master (Achievement), importlib.metadata, Lock Files, Reproducibility, requirements.txt, Versioning, Virtual Environments (+10 more)

### Community 8 - "Gotcha Gauntlet & Idioms Concepts"
Cohesion: 0.13
Nodes (17): Gotcha Gauntlet Master Achievement, Classes, Closures, Equality, Gotchas, Identity, Inheritance, Late Binding (+9 more)

### Community 9 - "App Data Directory Resolution"
Cohesion: 0.21
Nodes (13): Path, Resolves the real, writable directory this app's data lives in., Returns the OS-appropriate writable data directory, creating it if it doesn't…, resolve_platform_data_dir(), get_data_dir(), get_db_path(), get_settings_path(), is_first_run() (+5 more)

### Community 10 - "Recursion Lessons"
Cohesion: 0.17
Nodes (17): Accumulator, Base Case, Data Structures, Mutual Recursion, Performance, Recursion, Recursion Limit, The Countdown That Never Stopped (+9 more)

### Community 11 - "Thread Scheduling Lessons"
Cohesion: 0.15
Nodes (17): Daemon Threads, Debugging, Locks, Producer Consumer, Queue, Thread Local Storage, Threading, The Lock That Locked Itself Out (+9 more)

### Community 12 - "Quiz Screen UI"
Cohesion: 0.24
Nodes (4): Control, View, _QuizController, Button

### Community 13 - "Sync vs Async Lessons"
Cohesion: 0.22
Nodes (16): Asyncio, Context Managers, Generators, Sync Vs Async, with statement, Lesson: Turning Manual Cleanup into a Context Manager, The Blocking Call That Froze the Event Loop, Running Blocking I/O Without Blocking the Loop (+8 more)

### Community 14 - "Quiz Engine"
Cohesion: 0.21
Nodes (7): Path, QuizEngine, Loads a language track's quiz questions from YAML. Adding a question means…, A freshly randomized set of questions for one quiz playthrough -- which…, QuizQuestion, The QuizQuestion data model. Quiz content is data, not code -- see…, Collection

### Community 15 - "Deployment Lessons"
Cohesion: 0.19
Nodes (15): Configuration, Deployment, Deployment Master (Achievement), Environment Variables, Graceful Shutdown, Idempotency, Signals, Configuration with a Safe Default (+7 more)

### Community 16 - "Observability Lessons"
Cohesion: 0.18
Nodes (15): Health Checks, Instrumentation, Logging, Metrics, Observability, Observability Master (Achievement), A Health Check That Ignores Its Own Dependencies, Replacing print() Debugging with logging (+7 more)

### Community 17 - "App Feature Overview"
Cohesion: 0.15
Nodes (13): app/engine/ (content model), app/execution/ (ExecutionEngine), app/progress/ (SQLite XP/streaks), app/ui/ (Flet screens), Coding Adventure (README), Daily Refresher, Gotcha Gauntlet, Language Picker (+5 more)

### Community 18 - "Dict Grouping & Deque Lessons"
Cohesion: 0.20
Nodes (10): Dictionaries, Iteration, collections module, Lesson: Grouping Without Manual Key Checks, counting, Lesson: Tallying with Counter, deque, performance (algorithmic complexity) (+2 more)

### Community 19 - "Concurrency & Async Lessons"
Cohesion: 0.24
Nodes (10): concurrency, Lesson: Running Coroutines Concurrently, Keeping Order, race conditions, Lesson: Protecting a Shared Counter with a Lock, futures, Lesson: Running I/O-Bound Work Concurrently, locks, Lesson: The Async Equivalent of a Race Condition (+2 more)

### Community 20 - "Aliasing & Sorting Gotcha Lessons"
Cohesion: 0.25
Nodes (8): Idioms Gotchas Master Achievement, Idioms Gotchas Progress Achievement, Aliasing, Copying, Lists, Sorting, The Backup That Wasn't, The Silent None: list.sort() Returns Nothing

### Community 21 - "Heapq, Bisect & Sets Lessons"
Cohesion: 0.33
Nodes (7): algorithms, heapq, Lesson: The k Smallest Items Without a Full Sort, bisect, Lesson: Inserting Into a Sorted List Without Re-Sorting, sets, Lesson: Finding Overlap with Set Operations

### Community 22 - "Exception Handling Lessons"
Cohesion: 0.50
Nodes (5): Stdlib Deep Dive Master Achievement, Contextlib, Exceptions, The Bare Except That Hid a Real Bug, Suppressing an Expected Exception Cleanly

### Community 23 - "Float Precision Lessons"
Cohesion: 0.50
Nodes (5): Decimal, Floats, Precision, The Price That Rounded the Wrong Way, 0.1 + 0.2 Is Not Quite 0.3

### Community 24 - "Toolchain Detection"
Cohesion: 0.67
Nodes (3): check_toolchain(), Detects whether a language track's real local toolchain is on PATH. Used by the…, ToolchainStatus

### Community 25 - "Correlation ID Tracing"
Cohesion: 0.67
Nodes (4): contextvars, Tracing, Threading a Correlation ID Through Log Lines, What problem does contextvars.ContextVar solve for correlation/request IDs?

### Community 26 - "Pathlib Lessons"
Cohesion: 0.67
Nodes (3): Filesystem, Pathlib, Paths as Objects, Not Strings

### Community 27 - "Comprehension Lessons"
Cohesion: 0.67
Nodes (3): comprehensions, lists, Lesson: Loop to Comprehension

## Knowledge Gaps
- **84 isolated node(s):** `run.sh script`, `coding-adventure`, `platform_paths.py`, `settings.py`, `CATEGORY_META` (+79 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `AppState` connect `Categories & Language Registry` to `Execution Engine Contract & Config`, `Output Validation & Error Translation`, `Progress Store & XP Leveling`, `Exercise Content Model`, `App Data Directory Resolution`, `Quiz Screen UI`, `Quiz Engine`?**
  _High betweenness centrality (0.116) - this node is a cross-community bridge._
- **Why does `Gotchas` connect `Gotcha Gauntlet & Idioms Concepts` to `Functional Programming Lessons`, `Dependency Management Lessons`, `Recursion Lessons`, `Thread Scheduling Lessons`, `Sync vs Async Lessons`, `Deployment Lessons`, `Observability Lessons`, `Dict Grouping & Deque Lessons`, `Aliasing & Sorting Gotcha Lessons`, `Exception Handling Lessons`, `Float Precision Lessons`?**
  _High betweenness centrality (0.096) - this node is a cross-community bridge._
- **Why does `CLAUDE.md — Coding Adventure Architecture Guide` connect `Execution Engine Contract & Config` to `Categories & Language Registry`, `Output Validation & Error Translation`, `Progress Store & XP Leveling`, `Exercise Content Model`, `Quiz Engine`?**
  _High betweenness centrality (0.087) - this node is a cross-community bridge._
- **Are the 22 inferred relationships involving `AppState` (e.g. with `Settings` and `ExerciseEngine`) actually correct?**
  _`AppState` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `ProgressStore` (e.g. with `AppState` and `store()`) actually correct?**
  _`ProgressStore` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `_ExerciseController` (e.g. with `Exercise` and `ExecutionResult`) actually correct?**
  _`_ExerciseController` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `run.sh script`, `coding-adventure`, `platform_paths.py` to the rest of the system?**
  _84 weakly-connected nodes found - possible documentation gaps or missing edges._