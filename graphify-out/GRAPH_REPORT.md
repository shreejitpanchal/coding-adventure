# Graph Report - coding-adventure  (2026-08-23)

## Corpus Check
- 41 files · ~40,922 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 681 nodes · 1227 edges · 45 communities (36 shown, 9 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 57 edges (avg confidence: 0.91)
- Token cost: 144,035 input · 61,729 output

## Community Hubs (Navigation)
- App State, Categories & Language Registry
- Concurrency & Async Lessons
- Execution Engine Contract
- Data Structures & Algorithms Lessons
- Core & Functional Programming Lessons
- Error Translation & Code Editor
- Progress Store & XP Leveling
- Exercise Content Model
- Deployment Lessons
- Packaging Lessons
- Dependency Management & Exception Lessons
- App Data Directory Resolution
- Language Registry & Toolchain Detection
- Quiz Screen UI
- Quiz Engine
- Output Validation & Tests
- Java Equals/HashCode Lessons
- Java String Handling Lessons
- Java Equality & Autoboxing Lessons
- Python Idioms & Gotchas Lessons
- Dict Grouping & Deque Lessons
- Java Static Fields & Inheritance Lessons
- Java Arrays & Off-by-One Lessons
- Closures & Slicing Lessons
- Float Precision Lessons
- build_apk.sh Script
- Java Time/Duration Lessons
- Java switch Fallthrough Lessons
- Java Integer Overflow Lessons
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
1. `Gotchas` - 54 edges
2. `AppState` - 42 edges
3. `ProgressStore` - 31 edges
4. `ExerciseEngine` - 24 edges
5. `Threading` - 23 edges
6. `_ExerciseController` - 21 edges
7. `Exercise` - 20 edges
8. `scaled()` - 18 edges
9. `_QuizController` - 16 edges
10. `Concurrency` - 16 edges

## Surprising Connections (you probably didn't know these)
- `Lesson: Cutting Boilerplate with @dataclass` --semantically_similar_to--> `Exercise`  [INFERRED] [semantically similar]
  content/python/lessons/core_refresher_05_dataclasses.yaml → app/engine/exercise.py
- `app_window.py (route dispatcher)` --references--> `AppState`  [EXTRACTED]
  CLAUDE.md → app/ui/app_state.py
- `One Flat Topic Browser, No Guided Main Path` --rationale_for--> `ExerciseEngine`  [EXTRACTED]
  CLAUDE.md → app/engine/lesson_engine.py
- `Settings` --references--> `platform_paths.py`  [EXTRACTED]
  app/config/settings.py → CLAUDE.md
- `Crash-Containment, Not a Safety Sandbox` --rationale_for--> `ExecutionEngine`  [EXTRACTED]
  CLAUDE.md → app/execution/base.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Concurrency & Async Lesson Progression** — content_java_lessons_concurrency_async_01_race_condition_synchronized_lesson, content_java_lessons_concurrency_async_02_atomic_integer_lesson, content_java_lessons_concurrency_async_03_executor_service_lesson, content_java_lessons_concurrency_async_04_completable_future_lesson, content_java_lessons_concurrency_async_05_executor_await_termination_lesson, achievement_concurrency_async_master [EXTRACTED 0.95]
- **Core Language Refresher Lesson Progression** — content_java_lessons_core_refresher_01_lambda_expression_lesson, content_java_lessons_core_refresher_02_streams_filter_map_lesson, content_java_lessons_core_refresher_03_optional_lesson, content_java_lessons_core_refresher_04_record_class_lesson, content_java_lessons_core_refresher_05_try_with_resources_lesson, achievement_core_refresher_master [EXTRACTED 0.95]
- **Data Structures Lesson Progression** — content_java_lessons_data_structures_01_hashmap_iteration_order_lesson, content_java_lessons_data_structures_02_arraydeque_queue_lesson, content_java_lessons_data_structures_03_comparator_custom_sort_lesson, content_java_lessons_data_structures_04_treemap_sorted_keys_lesson, content_java_lessons_data_structures_05_priority_queue_lesson, achievement_data_structures_master [EXTRACTED 0.95]
- **Java Equality & Hashing Pitfalls** — content_java_lessons_idioms_gotchas_01_string_equality_lesson, content_java_lessons_idioms_gotchas_02_integer_caching_lesson, content_java_lessons_gotcha_gauntlet_05_equals_hashcode_contract_lesson, content_java_lessons_stdlib_deep_dive_03_objects_equals_null_safe_lesson [INFERRED 0.80]
- **Gotcha Gauntlet Lesson Series** — content_java_lessons_gotcha_gauntlet_01_off_by_one_loop_lesson, content_java_lessons_gotcha_gauntlet_02_switch_fallthrough_lesson, content_java_lessons_gotcha_gauntlet_03_concurrent_modification_lesson, content_java_lessons_gotcha_gauntlet_04_integer_overflow_lesson, content_java_lessons_gotcha_gauntlet_05_equals_hashcode_contract_lesson [EXTRACTED 1.00]
- **Java Concurrency Toolkit Questions** — content_java_quiz_quiz_questions_q25, content_java_quiz_quiz_questions_q26, content_java_quiz_quiz_questions_q27, content_java_quiz_quiz_questions_q28, content_java_quiz_quiz_questions_q29, content_java_quiz_quiz_questions_q30 [INFERRED 0.85]
- **Gotcha Gauntlet Lesson Sequence** — content_python_lessons_gotcha_gauntlet_02_exception_swallowing_lesson, content_python_lessons_gotcha_gauntlet_03_mutable_class_attribute_lesson, content_python_lessons_gotcha_gauntlet_04_rounding_precision_lesson, content_python_lessons_gotcha_gauntlet_05_dict_mutation_during_iteration_lesson, content_python_lessons_gotcha_gauntlet_06_missing_super_init_lesson [EXTRACTED 1.00]
- **Idioms Gotchas Lesson Sequence** — content_python_lessons_idioms_gotchas_01_mutable_default_arg_lesson, content_python_lessons_idioms_gotchas_02_late_binding_closure_lesson, content_python_lessons_idioms_gotchas_03_is_vs_equals_lesson, content_python_lessons_idioms_gotchas_04_float_precision_lesson, content_python_lessons_idioms_gotchas_05_aliasing_vs_copying_lesson, content_python_lessons_idioms_gotchas_06_sort_returns_none_lesson [EXTRACTED 1.00]
- **Stdlib Deep Dive Lesson Sequence** — content_python_lessons_stdlib_deep_dive_01_itertools_chain_lesson, content_python_lessons_stdlib_deep_dive_02_lru_cache_lesson, content_python_lessons_stdlib_deep_dive_03_reduce_lesson, content_python_lessons_stdlib_deep_dive_04_pathlib_lesson, content_python_lessons_stdlib_deep_dive_05_typing_hints_lesson, content_python_lessons_stdlib_deep_dive_06_contextlib_suppress_lesson [EXTRACTED 1.00]
- **Lessons Demonstrating Recursion-Misuse Failure Modes** — content_python_lessons_recursion_01_missing_base_case_lesson, content_python_lessons_recursion_02_recursion_depth_limit_lesson, content_python_lessons_thread_scheduling_01_reentrant_lock_lesson [INFERRED 0.75]
- **Category-Capstone Lessons Awarding a Mastery Achievement** — content_python_lessons_packaging_05_wheel_filename_parsing_lesson, content_python_lessons_recursion_05_accumulator_pattern_lesson, content_python_lessons_sync_vs_async_05_async_for_generator_lesson, content_python_lessons_thread_scheduling_05_thread_local_storage_lesson [INFERRED 0.85]
- **Dependency Management Lesson Progression** — content_python_lessons_dependency_management_01_detect_virtualenv_lesson, content_python_lessons_dependency_management_02_parse_requirement_line_lesson, content_python_lessons_dependency_management_03_version_string_comparison_lesson, content_python_lessons_dependency_management_04_importlib_metadata_lesson, content_python_lessons_dependency_management_05_lock_file_pin_lesson [INFERRED 0.95]
- **Deployment Lesson Progression** — content_python_lessons_deployment_01_env_var_defaults_lesson, content_python_lessons_deployment_02_feature_flag_boolean_parsing_lesson, content_python_lessons_deployment_03_graceful_shutdown_signal_lesson, content_python_lessons_deployment_04_health_check_lesson, content_python_lessons_deployment_05_idempotent_deploy_step_lesson [INFERRED 0.95]
- **Functional Programming Lesson Progression** — content_python_lessons_functional_programming_01_pure_functions_lesson, content_python_lessons_functional_programming_02_map_filter_lesson, content_python_lessons_functional_programming_03_function_composition_lesson, content_python_lessons_functional_programming_04_immutability_lesson, content_python_lessons_functional_programming_05_partial_application_lesson [INFERRED 0.95]

## Communities (45 total, 9 thin omitted)

### Community 0 - "App State, Categories & Language Registry"
Cohesion: 0.06
Nodes (57): CategoryMeta, get_category_meta(), Display metadata (title, icon, color) for exercise categories, used by the…, AppState, Shared app state: settings, progress store, per-language exercise/quiz engines…, main(), Page, Root Flet application: route-based navigation between full-screen views.… (+49 more)

### Community 1 - "Concurrency & Async Lessons"
Cohesion: 0.06
Nodes (60): Achievement: concurrency_async_master, Async, Asyncio, Atomic Operations, CompletableFuture, Concurrency, Context Managers, Daemon Threads (+52 more)

### Community 2 - "Execution Engine Contract"
Cohesion: 0.07
Nodes (29): ABC, CATEGORY_META, ExecutionEngine, ExecutionResult, Shared execution contract every per-language engine implements. Framing is…, Lets the UI cancel a run that's in progress (e.g. an infinite loop)., One concrete subclass per language track (python_engine.PythonEngine,…, RunHandle (+21 more)

### Community 3 - "Data Structures & Algorithms Lessons"
Cohesion: 0.07
Nodes (45): Achievement: data_structures_master, Accumulator, Algorithms, Base Case, Collections, Comparator, Data Structures, HashMap (+37 more)

### Community 4 - "Core & Functional Programming Lessons"
Cohesion: 0.06
Nodes (44): Achievement: core_refresher_master, Core Language Refresher (category), Function Composition, Functional Interfaces, Functional Programming, Functional Programming Master (Achievement), Functools, Higher-Order Functions (+36 more)

### Community 5 - "Error Translation & Code Editor"
Cohesion: 0.08
Nodes (20): extract_error_line_number(), _last_exception_type(), Translates raw interpreter/compiler output into concise, professional…, translate_error(), _translate_java_error(), make_code_editor(), make_read_only_code_block(), Control (+12 more)

### Community 6 - "Progress Store & XP Leveling"
Cohesion: 0.08
Nodes (13): _level_from_xp(), _now(), PlayerLevel, ProgressStore, Path, SQLite-backed progress, gamification, and activity tracking -- one…, Returns True if newly awarded, False if already had it., Resets to 0 automatically once the exercise is passed -- powers the "keep… (+5 more)

### Community 7 - "Exercise Content Model"
Cohesion: 0.09
Nodes (11): Exercise, The Exercise data model. Content is data, not code -- see…, ExerciseEngine, Path, Loads one language track's exercises from YAML, kept separate from application…, category -> (done, total), done computed by the caller passing completed_ids in…, A small guided set for "today's refresher" -- round-robins the next unlocked,…, Content Is Data, Not Code (+3 more)

### Community 8 - "Deployment Lessons"
Cohesion: 0.08
Nodes (34): Configuration, contextvars, Deployment, Deployment Master (Achievement), Environment Variables, Graceful Shutdown, Health Checks, Idempotency (+26 more)

### Community 9 - "Packaging Lessons"
Cohesion: 0.11
Nodes (23): Decorators, Entry Points, Functions, Module Api, Packaging, Pyproject Toml, Semantic Versioning, Tomllib (+15 more)

### Community 10 - "Dependency Management & Exception Lessons"
Cohesion: 0.12
Nodes (22): Stdlib Deep Dive Master Achievement, Contextlib, Dependency Management, Dependency Management Master (Achievement), Exceptions, finally Block, importlib.metadata, Lock Files (+14 more)

### Community 11 - "App Data Directory Resolution"
Cohesion: 0.19
Nodes (14): platform_paths.py, Path, Resolves the real, writable directory this app's data lives in., Returns the OS-appropriate writable data directory, creating it if it doesn't…, resolve_platform_data_dir(), get_data_dir(), get_db_path(), get_settings_path() (+6 more)

### Community 12 - "Language Registry & Toolchain Detection"
Cohesion: 0.18
Nodes (13): get_language(), LanguageInfo, The set of language tracks the app knows about, and which ones have real…, check_toolchain(), Detects whether a language track's real local toolchain is on PATH. Used by the…, ToolchainStatus, _build_language_card(), build_language_select_view() (+5 more)

### Community 13 - "Quiz Screen UI"
Cohesion: 0.24
Nodes (4): Control, View, _QuizController, Button

### Community 14 - "Quiz Engine"
Cohesion: 0.21
Nodes (7): Path, QuizEngine, Loads a language track's quiz questions from YAML. Adding a question means…, A freshly randomized set of questions for one quiz playthrough -- which…, QuizQuestion, The QuizQuestion data model. Quiz content is data, not code -- see…, Collection

### Community 15 - "Output Validation & Tests"
Cohesion: 0.27
Nodes (10): Exercise validation: checks behavior/output, not exact code formatting., True if `code` contains every required pattern. Each pattern is matched as a…, Compares output, optionally substituting what the user typed into a template. -…, validate_contains(), validate_output(), test_validate_contains_empty_patterns_always_true(), test_validate_contains_requires_all_patterns(), test_validate_output_exact_match() (+2 more)

### Community 16 - "Java Equals/HashCode Lessons"
Cohesion: 0.31
Nodes (11): equals()/hashCode() Contract, Gotchas, HashSet, java.util.Objects, Versioning, Gotcha Gauntlet: equals() Without hashCode(), Stdlib Deep Dive: Null-Safe Comparison with Objects.equals, Quiz: Objects.equals Null Safety (+3 more)

### Community 17 - "Java String Handling Lessons"
Cohesion: 0.33
Nodes (11): String Formatting, Regular Expressions, StringBuilder, Strings, Stdlib Deep Dive: Building a String in a Loop, Stdlib Deep Dive: Structured Output with String.format, Stdlib Deep Dive: Validating a Pattern with a Regex, Quiz: StringBuilder vs += (+3 more)

### Community 18 - "Java Equality & Autoboxing Lessons"
Cohesion: 0.27
Nodes (10): Autoboxing, Equality, Identity, Integer Cache, Idioms & Gotchas: == vs .equals() for Strings, Idioms & Gotchas: Autoboxed Integer Comparison, Quiz: == vs equals() for Objects, Quiz: Boxed Integer == Comparison (+2 more)

### Community 19 - "Python Idioms & Gotchas Lessons"
Cohesion: 0.22
Nodes (9): Idioms Gotchas Master Achievement, Idioms Gotchas Progress Achievement, Aliasing, Copying, Lists, Mutable Defaults, The Shopping Cart Shared By Every Customer, The Backup That Wasn't (+1 more)

### Community 20 - "Dict Grouping & Deque Lessons"
Cohesion: 0.22
Nodes (9): Dictionaries, collections module, Lesson: Grouping Without Manual Key Checks, counting, Lesson: Tallying with Counter, deque, performance (algorithmic complexity), Lesson: O(1) Queue Operations with deque (+1 more)

### Community 21 - "Java Static Fields & Inheritance Lessons"
Cohesion: 0.38
Nodes (7): Gotcha Gauntlet Master Achievement, Classes, Inheritance, Static Fields, Idioms & Gotchas: The Counter Every Instance Shared, Quiz: Effect of static Field, The Subclass That Forgot Its Parent

### Community 22 - "Java Arrays & Off-by-One Lessons"
Cohesion: 0.48
Nodes (7): Arrays, Null, Off-by-One Error, Gotcha Gauntlet: The Loop That Ran One Step Too Far, Idioms & Gotchas: The Array Slot That Was Never Set, Quiz: Default Value of Array Slot, Quiz: <= vs < Against arr.length

### Community 23 - "Closures & Slicing Lessons"
Cohesion: 0.27
Nodes (6): Closures, Late Binding, off-by-one errors, slicing, Lesson: The Off-By-One Slice, The Closure That Forgot Everything

### Community 24 - "Float Precision Lessons"
Cohesion: 0.50
Nodes (5): Decimal, Floats, Precision, The Price That Rounded the Wrong Way, 0.1 + 0.2 Is Not Quite 0.3

### Community 26 - "Java Time/Duration Lessons"
Cohesion: 0.83
Nodes (4): Duration, java.time, Stdlib Deep Dive: Durations with java.time Instead of Raw Millis, Quiz: Duration.ofMillis().toMinutes()

### Community 27 - "Java switch Fallthrough Lessons"
Cohesion: 0.83
Nodes (4): Fallthrough, switch Statement, Gotcha Gauntlet: The switch That Fell Through Every Case, Quiz: Missing break in switch Case

### Community 28 - "Java Integer Overflow Lessons"
Cohesion: 0.83
Nodes (4): Integers, Integer Overflow, Gotcha Gauntlet: The Overflow That Never Threw an Error, Quiz: int Overflow Behavior

### Community 29 - "Pathlib Lessons"
Cohesion: 0.67
Nodes (3): Filesystem, Pathlib, Paths as Objects, Not Strings

### Community 30 - "Comprehension Lessons"
Cohesion: 0.67
Nodes (3): comprehensions, lists, Lesson: Loop to Comprehension

## Knowledge Gaps
- **60 isolated node(s):** `run.sh script`, `coding-adventure`, `with statement`, `counting`, `deque` (+55 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Gotchas` connect `Java Equals/HashCode Lessons` to `Concurrency & Async Lessons`, `Execution Engine Contract`, `Data Structures & Algorithms Lessons`, `Core & Functional Programming Lessons`, `Deployment Lessons`, `Packaging Lessons`, `Dependency Management & Exception Lessons`, `Java String Handling Lessons`, `Java Equality & Autoboxing Lessons`, `Python Idioms & Gotchas Lessons`, `Dict Grouping & Deque Lessons`, `Java Static Fields & Inheritance Lessons`, `Java Arrays & Off-by-One Lessons`, `Closures & Slicing Lessons`, `Float Precision Lessons`, `Java switch Fallthrough Lessons`, `Java Integer Overflow Lessons`?**
  _High betweenness centrality (0.563) - this node is a cross-community bridge._
- **Why does `ProgressStore` connect `Progress Store & XP Leveling` to `App State, Categories & Language Registry`, `Execution Engine Contract`, `App Data Directory Resolution`?**
  _High betweenness centrality (0.197) - this node is a cross-community bridge._
- **Why does `ExerciseEngine` connect `Exercise Content Model` to `App State, Categories & Language Registry`, `Execution Engine Contract`?**
  _High betweenness centrality (0.173) - this node is a cross-community bridge._
- **Are the 17 inferred relationships involving `AppState` (e.g. with `Settings` and `ExerciseEngine`) actually correct?**
  _`AppState` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `ExerciseEngine` (e.g. with `Exercise` and `AppState`) actually correct?**
  _`ExerciseEngine` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `run.sh script`, `coding-adventure`, `with statement` to the rest of the system?**
  _60 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `App State, Categories & Language Registry` be split into smaller, more focused modules?**
  _Cohesion score 0.06426906426906427 - nodes in this community are weakly interconnected._