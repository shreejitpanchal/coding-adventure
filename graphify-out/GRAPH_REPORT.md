# Graph Report - coding-adventure  (2026-08-23)

## Corpus Check
- 43 files · ~51,567 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 735 nodes · 1336 edges · 52 communities (44 shown, 8 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 69 edges (avg confidence: 0.87)
- Token cost: 114,593 input · 49,110 output

## Community Hubs (Navigation)
- Categories & Language Registry
- Execution Engine Contract
- Core Refresher & Functional Programming Lessons
- Data Structures & Recursion Lessons
- Error Translation & Code Editor
- Progress Store & XP Leveling
- Exercise Content Model
- Packaging Lessons
- Observability Lessons
- Deployment Lessons
- Thread Scheduling Lessons
- Idioms, Gotchas & Equality Lessons
- App Data Directory Resolution
- Sync vs Async Lessons
- Concurrency Lessons
- Language Registry & Toolchain Detection
- Quiz Screen UI
- Quiz Engine
- Dependency Management Lessons
- Output Validation & Tests
- Dict Grouping & Iteration Lessons
- Stdlib Deep Dive & Reflection Lessons
- Producer/Consumer & Virtual Threads Lessons
- Classes & Static Fields Lessons
- Race Conditions & Atomics Lessons
- Maven Coordinate Lessons
- Aliasing & Copying Lessons
- Array & Off-by-One Lessons
- Float Precision Lessons
- String Formatting & Regex Lessons
- Classpath Conflict Lessons
- Java Time/Duration Lessons
- Switch Fallthrough Lessons
- Pathlib Lessons
- Integer Overflow Lessons
- Thread Priority Lessons
- Concurrency & Async Lessons
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
1. `Gotchas` - 52 edges
2. `AppState` - 42 edges
3. `ProgressStore` - 30 edges
4. `Threading` - 28 edges
5. `Observability` - 25 edges
6. `ExerciseEngine` - 23 edges
7. `_ExerciseController` - 21 edges
8. `Recursion` - 21 edges
9. `Functional Programming` - 21 edges
10. `Exercise` - 20 edges

## Surprising Connections (you probably didn't know these)
- `Lesson: Cutting Boilerplate with @dataclass` --semantically_similar_to--> `Exercise`  [INFERRED] [semantically similar]
  content/python/lessons/core_refresher_05_dataclasses.yaml → app/engine/exercise.py
- `app_window.py (route dispatcher)` --references--> `AppState`  [EXTRACTED]
  CLAUDE.md → app/ui/app_state.py
- `Settings` --references--> `platform_paths.py`  [EXTRACTED]
  app/config/settings.py → CLAUDE.md
- `One Flat Topic Browser, No Guided Main Path` --rationale_for--> `ExerciseEngine`  [EXTRACTED]
  CLAUDE.md → app/engine/lesson_engine.py
- `Crash-Containment, Not a Safety Sandbox` --rationale_for--> `ExecutionEngine`  [EXTRACTED]
  CLAUDE.md → app/execution/base.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Lexicographic vs Numeric Version Comparison Pattern** — content_java_lessons_dependency_management_01_version_string_comparison_lesson, content_java_lessons_dependency_management_04_minimum_version_check_lesson, concept_versioning [INFERRED 0.85]
- **Logger/Handler Level Threshold Pattern** — content_java_lessons_observability_01_structured_logging_lesson, content_java_lessons_observability_02_log_level_filtering_lesson, concept_logging [INFERRED 0.80]
- **Deployment Lifecycle Operational Concerns** — content_java_lessons_deployment_03_shutdown_hook_lesson, content_java_lessons_deployment_04_health_check_lesson, content_java_lessons_deployment_05_idempotent_deploy_step_lesson [INFERRED 0.70]
- **CompletableFuture Async Pipeline Progression** — content_java_lessons_sync_vs_async_01_completablefuture_chaining_lesson, content_java_lessons_sync_vs_async_02_completablefuture_combine_lesson, content_java_lessons_sync_vs_async_03_completablefuture_exceptionally_lesson, content_java_lessons_sync_vs_async_04_supplyasync_custom_executor_lesson, content_java_lessons_sync_vs_async_05_virtual_threads_lesson [INFERRED 0.85]
- **Thread Lifecycle Management Progression** — content_java_lessons_thread_scheduling_01_thread_naming_lesson, content_java_lessons_thread_scheduling_02_daemon_flag_lesson, content_java_lessons_thread_scheduling_03_thread_priority_lesson, content_java_lessons_thread_scheduling_04_blocking_queue_lesson, content_java_lessons_thread_scheduling_05_interrupt_handling_lesson [INFERRED 0.85]
- **JVM Packaging and Build Artifact Progression** — content_java_lessons_packaging_01_manifest_main_class_lesson, content_java_lessons_packaging_02_package_naming_convention_lesson, content_java_lessons_packaging_03_semver_bump_lesson, content_java_lessons_packaging_04_service_registry_lesson, content_java_lessons_packaging_05_jar_filename_parsing_lesson [INFERRED 0.85]
- **Concurrency & Async Lesson Progression** — content_java_lessons_concurrency_async_01_race_condition_synchronized_lesson, content_java_lessons_concurrency_async_02_atomic_integer_lesson, content_java_lessons_concurrency_async_03_executor_service_lesson, content_java_lessons_concurrency_async_04_completable_future_lesson, content_java_lessons_concurrency_async_05_executor_await_termination_lesson, achievement_concurrency_async_master [EXTRACTED 0.95]
- **Core Language Refresher Lesson Progression** — content_java_lessons_core_refresher_01_lambda_expression_lesson, content_java_lessons_core_refresher_02_streams_filter_map_lesson, content_java_lessons_core_refresher_03_optional_lesson, content_java_lessons_core_refresher_04_record_class_lesson, content_java_lessons_core_refresher_05_try_with_resources_lesson, achievement_core_refresher_master [EXTRACTED 0.95]
- **Data Structures Lesson Progression** — content_java_lessons_data_structures_01_hashmap_iteration_order_lesson, content_java_lessons_data_structures_02_arraydeque_queue_lesson, content_java_lessons_data_structures_03_comparator_custom_sort_lesson, content_java_lessons_data_structures_04_treemap_sorted_keys_lesson, content_java_lessons_data_structures_05_priority_queue_lesson, achievement_data_structures_master [EXTRACTED 0.95]
- **Gotcha Gauntlet Lesson Sequence** — content_python_lessons_gotcha_gauntlet_02_exception_swallowing_lesson, content_python_lessons_gotcha_gauntlet_03_mutable_class_attribute_lesson, content_python_lessons_gotcha_gauntlet_04_rounding_precision_lesson, content_python_lessons_gotcha_gauntlet_05_dict_mutation_during_iteration_lesson, content_python_lessons_gotcha_gauntlet_06_missing_super_init_lesson [EXTRACTED 1.00]
- **Gotcha Gauntlet Lesson Series** — content_java_lessons_gotcha_gauntlet_01_off_by_one_loop_lesson, content_java_lessons_gotcha_gauntlet_02_switch_fallthrough_lesson, content_java_lessons_gotcha_gauntlet_03_concurrent_modification_lesson, content_java_lessons_gotcha_gauntlet_04_integer_overflow_lesson, content_java_lessons_gotcha_gauntlet_05_equals_hashcode_contract_lesson [EXTRACTED 1.00]
- **Idioms Gotchas Lesson Sequence** — content_python_lessons_idioms_gotchas_01_mutable_default_arg_lesson, content_python_lessons_idioms_gotchas_02_late_binding_closure_lesson, content_python_lessons_idioms_gotchas_03_is_vs_equals_lesson, content_python_lessons_idioms_gotchas_04_float_precision_lesson, content_python_lessons_idioms_gotchas_05_aliasing_vs_copying_lesson, content_python_lessons_idioms_gotchas_06_sort_returns_none_lesson [EXTRACTED 1.00]
- **Stdlib Deep Dive Lesson Sequence** — content_python_lessons_stdlib_deep_dive_01_itertools_chain_lesson, content_python_lessons_stdlib_deep_dive_02_lru_cache_lesson, content_python_lessons_stdlib_deep_dive_03_reduce_lesson, content_python_lessons_stdlib_deep_dive_04_pathlib_lesson, content_python_lessons_stdlib_deep_dive_05_typing_hints_lesson, content_python_lessons_stdlib_deep_dive_06_contextlib_suppress_lesson [EXTRACTED 1.00]
- **Lessons Demonstrating Recursion-Misuse Failure Modes** — content_python_lessons_recursion_01_missing_base_case_lesson, content_python_lessons_recursion_02_recursion_depth_limit_lesson, content_python_lessons_thread_scheduling_01_reentrant_lock_lesson [INFERRED 0.75]
- **Java Equality & Hashing Pitfalls** — content_java_lessons_idioms_gotchas_01_string_equality_lesson, content_java_lessons_idioms_gotchas_02_integer_caching_lesson, content_java_lessons_gotcha_gauntlet_05_equals_hashcode_contract_lesson, content_java_lessons_stdlib_deep_dive_03_objects_equals_null_safe_lesson [INFERRED 0.80]
- **Category-Capstone Lessons Awarding a Mastery Achievement** — content_python_lessons_packaging_05_wheel_filename_parsing_lesson, content_python_lessons_recursion_05_accumulator_pattern_lesson, content_python_lessons_sync_vs_async_05_async_for_generator_lesson, content_python_lessons_thread_scheduling_05_thread_local_storage_lesson [INFERRED 0.85]
- **Dependency Management Lesson Progression** — content_python_lessons_dependency_management_01_detect_virtualenv_lesson, content_python_lessons_dependency_management_02_parse_requirement_line_lesson, content_python_lessons_dependency_management_03_version_string_comparison_lesson, content_python_lessons_dependency_management_04_importlib_metadata_lesson, content_python_lessons_dependency_management_05_lock_file_pin_lesson [INFERRED 0.95]
- **Deployment Lesson Progression** — content_python_lessons_deployment_01_env_var_defaults_lesson, content_python_lessons_deployment_02_feature_flag_boolean_parsing_lesson, content_python_lessons_deployment_03_graceful_shutdown_signal_lesson, content_python_lessons_deployment_04_health_check_lesson, content_python_lessons_deployment_05_idempotent_deploy_step_lesson [INFERRED 0.95]
- **Functional Programming Lesson Progression** — content_python_lessons_functional_programming_01_pure_functions_lesson, content_python_lessons_functional_programming_02_map_filter_lesson, content_python_lessons_functional_programming_03_function_composition_lesson, content_python_lessons_functional_programming_04_immutability_lesson, content_python_lessons_functional_programming_05_partial_application_lesson [INFERRED 0.95]

## Communities (52 total, 8 thin omitted)

### Community 0 - "Categories & Language Registry"
Cohesion: 0.06
Nodes (57): CategoryMeta, get_category_meta(), Display metadata (title, icon, color) for exercise categories, used by the…, AppState, Shared app state: settings, progress store, per-language exercise/quiz engines…, main(), Page, Root Flet application: route-based navigation between full-screen views.… (+49 more)

### Community 1 - "Execution Engine Contract"
Cohesion: 0.07
Nodes (29): ABC, CATEGORY_META, ExecutionEngine, ExecutionResult, Shared execution contract every per-language engine implements. Framing is…, Lets the UI cancel a run that's in progress (e.g. an infinite loop)., One concrete subclass per language track (python_engine.PythonEngine,…, RunHandle (+21 more)

### Community 2 - "Core Refresher & Functional Programming Lessons"
Cohesion: 0.06
Nodes (50): Achievement: core_refresher_master, Core Language Refresher (category), Function Composition, Functional Interfaces, Functional Programming, Functional Programming Master (Achievement), Functools, Higher-Order Functions (+42 more)

### Community 3 - "Data Structures & Recursion Lessons"
Cohesion: 0.07
Nodes (49): Achievement: data_structures_master, Accumulator, Algorithms, Base Case, Collections, Comparator, Data Structures, HashMap (+41 more)

### Community 4 - "Error Translation & Code Editor"
Cohesion: 0.08
Nodes (20): extract_error_line_number(), _last_exception_type(), Translates raw interpreter/compiler output into concise, professional…, translate_error(), _translate_java_error(), make_code_editor(), make_read_only_code_block(), Control (+12 more)

### Community 5 - "Progress Store & XP Leveling"
Cohesion: 0.08
Nodes (13): _level_from_xp(), _now(), PlayerLevel, ProgressStore, Path, SQLite-backed progress, gamification, and activity tracking -- one…, Returns True if newly awarded, False if already had it., Resets to 0 automatically once the exercise is passed -- powers the "keep… (+5 more)

### Community 6 - "Exercise Content Model"
Cohesion: 0.09
Nodes (11): Exercise, The Exercise data model. Content is data, not code -- see…, ExerciseEngine, Path, Loads one language track's exercises from YAML, kept separate from application…, category -> (done, total), done computed by the caller passing completed_ids in…, A small guided set for "today's refresher" -- round-robins the next unlocked,…, Content Is Data, Not Code (+3 more)

### Community 7 - "Packaging Lessons"
Cohesion: 0.08
Nodes (36): Decorators, Entry Points, Functions, JAR Files, JAR Manifest, Module Api, Naming Conventions, Packaging (+28 more)

### Community 8 - "Observability Lessons"
Cohesion: 0.11
Nodes (31): contextvars, Health Checks, Instrumentation, Logging, Metrics, Observability, Observability Master (Achievement), ThreadLocal (+23 more)

### Community 9 - "Deployment Lessons"
Cohesion: 0.14
Nodes (25): Configuration, Deployment, Deployment Master (Achievement), Environment Variables, Graceful Shutdown, Idempotency, JVM, Shutdown Hooks (+17 more)

### Community 10 - "Thread Scheduling Lessons"
Cohesion: 0.16
Nodes (20): Daemon Threads, Debugging, Thread Interruption, Locks, Thread Local Storage, Threading, Naming Threads for Debuggable Logs, Marking a Background Thread as Daemon (+12 more)

### Community 11 - "Idioms, Gotchas & Equality Lessons"
Cohesion: 0.13
Nodes (19): Autoboxing, Closures, Equality, equals()/hashCode() Contract, Gotchas, HashSet, Identity, Integer Cache (+11 more)

### Community 12 - "App Data Directory Resolution"
Cohesion: 0.19
Nodes (14): platform_paths.py, Path, Resolves the real, writable directory this app's data lives in., Returns the OS-appropriate writable data directory, creating it if it doesn't…, resolve_platform_data_dir(), get_data_dir(), get_db_path(), get_settings_path() (+6 more)

### Community 13 - "Sync vs Async Lessons"
Cohesion: 0.18
Nodes (18): Asyncio, Context Managers, Generators, Sync Vs Async, timeouts, Lesson: Bounding How Long You'll Wait, with statement, Lesson: Turning Manual Cleanup into a Context Manager (+10 more)

### Community 14 - "Concurrency Lessons"
Cohesion: 0.30
Nodes (16): Achievement: concurrency_async_master, Async, CompletableFuture, Concurrency, ExecutorService, ExecutorService Instead of Raw Threads, Async Computation with CompletableFuture, shutdown() Doesn't Wait -- awaitTermination() Does (+8 more)

### Community 15 - "Language Registry & Toolchain Detection"
Cohesion: 0.18
Nodes (13): get_language(), LanguageInfo, The set of language tracks the app knows about, and which ones have real…, check_toolchain(), Detects whether a language track's real local toolchain is on PATH. Used by the…, ToolchainStatus, _build_language_card(), build_language_select_view() (+5 more)

### Community 16 - "Quiz Screen UI"
Cohesion: 0.24
Nodes (4): Control, View, _QuizController, Button

### Community 17 - "Quiz Engine"
Cohesion: 0.21
Nodes (7): Path, QuizEngine, Loads a language track's quiz questions from YAML. Adding a question means…, A freshly randomized set of questions for one quiz playthrough -- which…, QuizQuestion, The QuizQuestion data model. Quiz content is data, not code -- see…, Collection

### Community 18 - "Dependency Management Lessons"
Cohesion: 0.21
Nodes (15): Dependency Management, importlib.metadata, requirements.txt, Versioning, Virtual Environments, Comparing Version Numbers as Strings, Does This Version Satisfy the Minimum?, Why is String.compareTo unreliable for comparing version numbers like "10.0.0... (+7 more)

### Community 19 - "Output Validation & Tests"
Cohesion: 0.27
Nodes (10): Exercise validation: checks behavior/output, not exact code formatting., True if `code` contains every required pattern. Each pattern is matched as a…, Compares output, optionally substituting what the user typed into a template. -…, validate_contains(), validate_output(), test_validate_contains_empty_patterns_always_true(), test_validate_contains_requires_all_patterns(), test_validate_output_exact_match() (+2 more)

### Community 20 - "Dict Grouping & Iteration Lessons"
Cohesion: 0.18
Nodes (11): Dictionaries, Iteration, Gotcha Gauntlet: The List That Changed While Being Read, collections module, Lesson: Grouping Without Manual Key Checks, counting, Lesson: Tallying with Counter, deque (+3 more)

### Community 21 - "Stdlib Deep Dive & Reflection Lessons"
Cohesion: 0.24
Nodes (10): Stdlib Deep Dive Master Achievement, Contextlib, Exceptions, finally Block, Reflection, Detecting an Optional Dependency Gracefully, Idioms & Gotchas: The finally Block That Ate the Return, What does Class.forName(name) throw if the class isn't on the classpath? (+2 more)

### Community 22 - "Producer/Consumer & Virtual Threads Lessons"
Cohesion: 0.33
Nodes (9): Producer Consumer, Queue, Virtual Threads, Virtual Threads Instead of a Scarce Fixed Pool, A Producer/Consumer Handoff with BlockingQueue, Why is BlockingQueue.take() safer than ArrayDeque.poll() for a producer/consu..., What's the benefit of virtual threads over a small fixed platform-thread pool?, A Producer/Consumer Handoff with queue.Queue (+1 more)

### Community 23 - "Classes & Static Fields Lessons"
Cohesion: 0.25
Nodes (8): Gotcha Gauntlet Master Achievement, Classes, Inheritance, Mutable Defaults, Static Fields, Idioms & Gotchas: The Counter Every Instance Shared, The Shopping Cart Shared By Every Customer, The Subclass That Forgot Its Parent

### Community 24 - "Race Conditions & Atomics Lessons"
Cohesion: 0.25
Nodes (8): Atomic Operations, Race Conditions, synchronized, The Counter Two Threads Corrupted, AtomicInteger Instead of Manual Synchronization, Lesson: Protecting a Shared Counter with a Lock, locks, Lesson: The Async Equivalent of a Race Condition

### Community 25 - "Maven Coordinate Lessons"
Cohesion: 0.29
Nodes (8): Dependency Management Master (Achievement), Lock Files, Maven Coordinates, Reproducibility, Parsing a Maven Coordinate, What's the shape of a Maven coordinate string?, Why an Exact Pin Guarantees Reproducibility, Why does a lock file matter for reproducibility?

### Community 26 - "Aliasing & Copying Lessons"
Cohesion: 0.29
Nodes (7): Idioms Gotchas Master Achievement, Idioms Gotchas Progress Achievement, Aliasing, Copying, Lists, The Backup That Wasn't, The Silent None: list.sort() Returns Nothing

### Community 27 - "Array & Off-by-One Lessons"
Cohesion: 0.40
Nodes (5): Arrays, Null, Off-by-One Error, Gotcha Gauntlet: The Loop That Ran One Step Too Far, Idioms & Gotchas: The Array Slot That Was Never Set

### Community 28 - "Float Precision Lessons"
Cohesion: 0.50
Nodes (5): Decimal, Floats, Precision, The Price That Rounded the Wrong Way, 0.1 + 0.2 Is Not Quite 0.3

### Community 29 - "String Formatting & Regex Lessons"
Cohesion: 0.40
Nodes (5): String Formatting, Regular Expressions, Strings, Stdlib Deep Dive: Structured Output with String.format, Stdlib Deep Dive: Validating a Pattern with a Regex

### Community 30 - "Classpath Conflict Lessons"
Cohesion: 0.67
Nodes (4): Classpath, Dependency Conflict Resolution, The Classpath Conflict That Picked the Older Version, Why should a classpath conflict resolver check versions instead of always kee...

### Community 31 - "Java Time/Duration Lessons"
Cohesion: 0.67
Nodes (3): Duration, java.time, Stdlib Deep Dive: Durations with java.time Instead of Raw Millis

### Community 32 - "Switch Fallthrough Lessons"
Cohesion: 0.67
Nodes (3): Fallthrough, switch Statement, Gotcha Gauntlet: The switch That Fell Through Every Case

### Community 33 - "Pathlib Lessons"
Cohesion: 0.67
Nodes (3): Filesystem, Pathlib, Paths as Objects, Not Strings

### Community 34 - "Integer Overflow Lessons"
Cohesion: 0.67
Nodes (3): Integers, Integer Overflow, Gotcha Gauntlet: The Overflow That Never Threw an Error

### Community 35 - "Thread Priority Lessons"
Cohesion: 1.00
Nodes (3): Thread Priority, Setting a Thread's Scheduling Priority, Is Thread.setPriority() a guarantee of execution order?

### Community 36 - "Concurrency & Async Lessons"
Cohesion: 0.67
Nodes (3): Lesson: Running Coroutines Concurrently, Keeping Order, futures, Lesson: Running I/O-Bound Work Concurrently

### Community 37 - "Comprehension Lessons"
Cohesion: 0.67
Nodes (3): comprehensions, lists, Lesson: Loop to Comprehension

## Knowledge Gaps
- **78 isolated node(s):** `run.sh script`, `coding-adventure`, `futures`, `locks`, `timeouts` (+73 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Gotchas` connect `Idioms, Gotchas & Equality Lessons` to `Switch Fallthrough Lessons`, `Core Refresher & Functional Programming Lessons`, `Data Structures & Recursion Lessons`, `Integer Overflow Lessons`, `Packaging Lessons`, `Observability Lessons`, `Deployment Lessons`, `Thread Scheduling Lessons`, `Sync vs Async Lessons`, `Dependency Management Lessons`, `Dict Grouping & Iteration Lessons`, `Stdlib Deep Dive & Reflection Lessons`, `Classes & Static Fields Lessons`, `Aliasing & Copying Lessons`, `Array & Off-by-One Lessons`, `Float Precision Lessons`, `String Formatting & Regex Lessons`?**
  _High betweenness centrality (0.178) - this node is a cross-community bridge._
- **Why does `AppState` connect `Categories & Language Registry` to `Execution Engine Contract`, `Progress Store & XP Leveling`, `Exercise Content Model`, `App Data Directory Resolution`, `Quiz Screen UI`, `Quiz Engine`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **Why does `Threading` connect `Thread Scheduling Lessons` to `Thread Priority Lessons`, `Concurrency & Async Lessons`, `Sync vs Async Lessons`, `Concurrency Lessons`, `Producer/Consumer & Virtual Threads Lessons`, `Race Conditions & Atomics Lessons`?**
  _High betweenness centrality (0.050) - this node is a cross-community bridge._
- **Are the 17 inferred relationships involving `AppState` (e.g. with `Settings` and `ExerciseEngine`) actually correct?**
  _`AppState` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `Observability` (e.g. with `Logging` and `Metrics`) actually correct?**
  _`Observability` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `run.sh script`, `coding-adventure`, `futures` to the rest of the system?**
  _78 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Categories & Language Registry` be split into smaller, more focused modules?**
  _Cohesion score 0.06426906426906427 - nodes in this community are weakly interconnected._