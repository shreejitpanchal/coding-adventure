# Graph Report - coding-adventure  (2026-08-23)

## Corpus Check
- 43 files · ~65,872 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 843 nodes · 1533 edges · 67 communities (53 shown, 14 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 105 edges (avg confidence: 0.88)
- Token cost: 196,633 input · 0 output

## Community Hubs (Navigation)
- Concurrency & Async Lessons (Java/C++)
- Functional Programming Lessons
- Error Translation & Code Editor UI
- Progress Store & XP Leveling
- Exercise Content Model
- Packaging Lessons
- Observability Lessons
- Deployment Lessons
- Dependency Management Lessons
- Cross-Language Gotchas & Off-by-One Lessons
- Execution Engine Contract (ABC)
- App Data Directory Resolution
- Language Registry & Picker UI
- App Router & Category Levels UI
- Idioms/Aliasing/Static-Field Gotchas
- Recursion Lessons
- Sync vs Async Lessons
- C++ Type Conversion & String Parsing Lessons
- C++ Algorithms & Lambdas Lessons
- Category Display Metadata & Topic Browser UI
- Quiz Screen Controller
- Quiz Content Model
- CppEngine & C++ Execution Architecture
- AppState & Setup Wizard
- C++ Collections & Performance Lessons
- Output Validator & Tests
- JavaEngine & Toolchain Detection
- Java equals()/hashCode() Gotchas
- C++ RAII, Smart Pointers & Modern C++ Lessons
- Python Collections Lessons
- Stdlib Deep Dive & Exception Handling Lessons
- Settings Screen UI
- C++ Integer Overflow & Virtual Destructor Lessons
- Theme Presets & Quiz Bank UI
- C++ auto & Range-Based For Lessons
- Java Sorting & Comparator Lessons
- C++ Pass-by-Reference & Operator Gotchas
- Recursive Data Structure Lessons
- Float Precision Lessons
- Java Time/Duration Lesson
- Pathlib Lesson
- Memoization Lesson
- Comprehension Lesson
- Slicing Off-by-One Lesson
- run.sh Launcher Script
- RunHandle Subprocess Attachment
- Itertools Lesson
- Typing Hints Lesson
- Enum Lesson
- AppState (isolated ref)
- Control (Flet base class ref)
- Page (Flet base class ref)
- RunHandle (isolated ref)
- View (Flet base class ref)
- Project Root
- Flet Dependency
- Pytest Dependency
- PyYAML Dependency

## God Nodes (most connected - your core abstractions)
1. `Gotchas` - 76 edges
2. `AppState` - 39 edges
3. `Threading` - 38 edges
4. `ProgressStore` - 28 edges
5. `Concurrency` - 27 edges
6. `Observability` - 24 edges
7. `Recursion` - 21 edges
8. `ExerciseEngine` - 20 edges
9. `Functional Programming` - 20 edges
10. `_ExerciseController` - 20 edges

## Surprising Connections (you probably didn't know these)
- `Lesson: Cutting Boilerplate with @dataclass` --semantically_similar_to--> `Exercise`  [INFERRED] [semantically similar]
  content/python/lessons/core_refresher_05_dataclasses.yaml → app/engine/exercise.py
- `C++ Compiler/Runtime Error Translation (_translate_cpp_error, CPP_FRIENDLY)` --conceptually_related_to--> `_translate_cpp_error()`  [AMBIGUOUS]
  CLAUDE.md → app/execution/errors.py
- `Language-Agnostic contains_patterns Structural Validation` --conceptually_related_to--> `validate_contains()`  [INFERRED]
  CLAUDE.md → app/engine/validator.py
- `CppEngine (C++ Execution Engine)` --conceptually_related_to--> `CppEngine`  [INFERRED]
  docs/ARCHITECTURE.md → app/execution/cpp_engine.py
- `C++ has its own 6 categories (idioms_gotchas, core_refresher, data_structures, stdlib_deep_dive, concurrency_async, gotcha_gauntlet) instead of the shared Python/Java 14-category list, because categories like dependency_management/packaging/deployment/observability are ecosystem/tooling concepts that fit a package manager or framework better than bare C++ language/stdlib content -- ExerciseEngine.categories() derives the list purely from what's present in content/cpp/lessons/, so the smaller set required zero app-code changes` --rationale_for--> `Integer Division Truncates Silently`  [INFERRED]
  docs/DEVELOPMENT.md → content/cpp/lessons/idioms_gotchas_01_integer_division_truncation.yaml

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **C++ Concurrency Learning Progression** — content_cpp_lessons_concurrency_async_01_race_condition_mutex_exercise, content_cpp_lessons_concurrency_async_02_atomic_counter_exercise, content_cpp_lessons_concurrency_async_03_future_async_exercise, content_cpp_lessons_concurrency_async_04_thread_join_missing_exercise, content_cpp_lessons_concurrency_async_05_promise_future_signal_exercise [INFERRED 0.85]
- **Modern C++ Idioms Progression** — content_cpp_lessons_core_refresher_01_range_based_for_exercise, content_cpp_lessons_core_refresher_02_auto_type_deduction_exercise, content_cpp_lessons_core_refresher_03_lambda_expression_exercise, content_cpp_lessons_core_refresher_04_smart_pointer_unique_ptr_exercise, content_cpp_lessons_core_refresher_05_structured_bindings_exercise [INFERRED 0.85]
- **STL Container Selection Progression** — content_cpp_lessons_data_structures_01_sort_vector_exercise, content_cpp_lessons_data_structures_02_unordered_map_lookup_exercise, content_cpp_lessons_data_structures_03_deque_front_operations_exercise, content_cpp_lessons_data_structures_04_set_for_uniqueness_exercise, content_cpp_lessons_data_structures_05_priority_queue_exercise [INFERRED 0.85]
- **C++ Idioms & Gotchas Learning Progression** — content_cpp_lessons_idioms_gotchas_01_integer_division_truncation, content_cpp_lessons_idioms_gotchas_02_pass_by_value_no_mutation, content_cpp_lessons_idioms_gotchas_03_assignment_in_condition, content_cpp_lessons_idioms_gotchas_04_unsigned_underflow_loop, content_cpp_lessons_idioms_gotchas_05_char_digit_conversion [INFERRED 0.85]
- **C++ Standard Library Deep Dive Learning Progression** — content_cpp_lessons_stdlib_deep_dive_01_string_stream_parsing, content_cpp_lessons_stdlib_deep_dive_02_stoi_invalid_argument, content_cpp_lessons_stdlib_deep_dive_03_to_string, content_cpp_lessons_stdlib_deep_dive_04_algorithm_find, content_cpp_lessons_stdlib_deep_dive_05_optional_value [INFERRED 0.85]
- **C++ Track Documentation Set** — claude_overview, readme_overview, docs_architecture_overview, docs_development_overview, concept_cppengine [INFERRED 0.80]
- **Concurrency & Async Lesson Progression** — content_java_lessons_concurrency_async_01_race_condition_synchronized_lesson, content_java_lessons_concurrency_async_02_atomic_integer_lesson, content_java_lessons_concurrency_async_03_executor_service_lesson, content_java_lessons_concurrency_async_04_completable_future_lesson, content_java_lessons_concurrency_async_05_executor_await_termination_lesson, achievement_concurrency_async_master [EXTRACTED 0.95]
- **Core Language Refresher Lesson Progression** — content_java_lessons_core_refresher_01_lambda_expression_lesson, content_java_lessons_core_refresher_02_streams_filter_map_lesson, content_java_lessons_core_refresher_03_optional_lesson, content_java_lessons_core_refresher_04_record_class_lesson, content_java_lessons_core_refresher_05_try_with_resources_lesson, achievement_core_refresher_master [EXTRACTED 0.95]
- **Data Structures Lesson Progression** — content_java_lessons_data_structures_01_hashmap_iteration_order_lesson, content_java_lessons_data_structures_02_arraydeque_queue_lesson, content_java_lessons_data_structures_03_comparator_custom_sort_lesson, content_java_lessons_data_structures_04_treemap_sorted_keys_lesson, content_java_lessons_data_structures_05_priority_queue_lesson, achievement_data_structures_master [EXTRACTED 0.95]
- **Gotcha Gauntlet Lesson Sequence** — content_python_lessons_gotcha_gauntlet_02_exception_swallowing_lesson, content_python_lessons_gotcha_gauntlet_03_mutable_class_attribute_lesson, content_python_lessons_gotcha_gauntlet_04_rounding_precision_lesson, content_python_lessons_gotcha_gauntlet_05_dict_mutation_during_iteration_lesson, content_python_lessons_gotcha_gauntlet_06_missing_super_init_lesson [EXTRACTED 1.00]
- **Gotcha Gauntlet Lesson Series** — content_java_lessons_gotcha_gauntlet_01_off_by_one_loop_lesson, content_java_lessons_gotcha_gauntlet_02_switch_fallthrough_lesson, content_java_lessons_gotcha_gauntlet_03_concurrent_modification_lesson, content_java_lessons_gotcha_gauntlet_04_integer_overflow_lesson, content_java_lessons_gotcha_gauntlet_05_equals_hashcode_contract_lesson [EXTRACTED 1.00]
- **Idioms Gotchas Lesson Sequence** — content_python_lessons_idioms_gotchas_01_mutable_default_arg_lesson, content_python_lessons_idioms_gotchas_02_late_binding_closure_lesson, content_python_lessons_idioms_gotchas_03_is_vs_equals_lesson, content_python_lessons_idioms_gotchas_04_float_precision_lesson, content_python_lessons_idioms_gotchas_05_aliasing_vs_copying_lesson, content_python_lessons_idioms_gotchas_06_sort_returns_none_lesson [EXTRACTED 1.00]
- **Stdlib Deep Dive Lesson Sequence** — content_python_lessons_stdlib_deep_dive_01_itertools_chain_lesson, content_python_lessons_stdlib_deep_dive_02_lru_cache_lesson, content_python_lessons_stdlib_deep_dive_03_reduce_lesson, content_python_lessons_stdlib_deep_dive_04_pathlib_lesson, content_python_lessons_stdlib_deep_dive_05_typing_hints_lesson, content_python_lessons_stdlib_deep_dive_06_contextlib_suppress_lesson [EXTRACTED 1.00]
- **Deployment Lifecycle Operational Concerns** — content_java_lessons_deployment_03_shutdown_hook_lesson, content_java_lessons_deployment_04_health_check_lesson, content_java_lessons_deployment_05_idempotent_deploy_step_lesson [INFERRED 0.70]
- **Lessons Demonstrating Recursion-Misuse Failure Modes** — content_python_lessons_recursion_01_missing_base_case_lesson, content_python_lessons_recursion_02_recursion_depth_limit_lesson, content_python_lessons_thread_scheduling_01_reentrant_lock_lesson [INFERRED 0.75]
- **Java Equality & Hashing Pitfalls** — content_java_lessons_idioms_gotchas_01_string_equality_lesson, content_java_lessons_idioms_gotchas_02_integer_caching_lesson, content_java_lessons_gotcha_gauntlet_05_equals_hashcode_contract_lesson, content_java_lessons_stdlib_deep_dive_03_objects_equals_null_safe_lesson [INFERRED 0.80]
- **Logger/Handler Level Threshold Pattern** — content_java_lessons_observability_01_structured_logging_lesson, content_java_lessons_observability_02_log_level_filtering_lesson, concept_logging [INFERRED 0.80]
- **JVM Packaging and Build Artifact Progression** — content_java_lessons_packaging_01_manifest_main_class_lesson, content_java_lessons_packaging_02_package_naming_convention_lesson, content_java_lessons_packaging_03_semver_bump_lesson, content_java_lessons_packaging_04_service_registry_lesson, content_java_lessons_packaging_05_jar_filename_parsing_lesson [INFERRED 0.85]
- **Category-Capstone Lessons Awarding a Mastery Achievement** — content_python_lessons_packaging_05_wheel_filename_parsing_lesson, content_python_lessons_recursion_05_accumulator_pattern_lesson, content_python_lessons_sync_vs_async_05_async_for_generator_lesson, content_python_lessons_thread_scheduling_05_thread_local_storage_lesson [INFERRED 0.85]
- **CompletableFuture Async Pipeline Progression** — content_java_lessons_sync_vs_async_01_completablefuture_chaining_lesson, content_java_lessons_sync_vs_async_02_completablefuture_combine_lesson, content_java_lessons_sync_vs_async_03_completablefuture_exceptionally_lesson, content_java_lessons_sync_vs_async_04_supplyasync_custom_executor_lesson, content_java_lessons_sync_vs_async_05_virtual_threads_lesson [INFERRED 0.85]
- **Thread Lifecycle Management Progression** — content_java_lessons_thread_scheduling_01_thread_naming_lesson, content_java_lessons_thread_scheduling_02_daemon_flag_lesson, content_java_lessons_thread_scheduling_03_thread_priority_lesson, content_java_lessons_thread_scheduling_04_blocking_queue_lesson, content_java_lessons_thread_scheduling_05_interrupt_handling_lesson [INFERRED 0.85]
- **Lexicographic vs Numeric Version Comparison Pattern** — content_java_lessons_dependency_management_01_version_string_comparison_lesson, content_java_lessons_dependency_management_04_minimum_version_check_lesson, concept_versioning [INFERRED 0.85]
- **Dependency Management Lesson Progression** — content_python_lessons_dependency_management_01_detect_virtualenv_lesson, content_python_lessons_dependency_management_02_parse_requirement_line_lesson, content_python_lessons_dependency_management_03_version_string_comparison_lesson, content_python_lessons_dependency_management_04_importlib_metadata_lesson, content_python_lessons_dependency_management_05_lock_file_pin_lesson [INFERRED 0.95]
- **Deployment Lesson Progression** — content_python_lessons_deployment_01_env_var_defaults_lesson, content_python_lessons_deployment_02_feature_flag_boolean_parsing_lesson, content_python_lessons_deployment_03_graceful_shutdown_signal_lesson, content_python_lessons_deployment_04_health_check_lesson, content_python_lessons_deployment_05_idempotent_deploy_step_lesson [INFERRED 0.95]
- **Functional Programming Lesson Progression** — content_python_lessons_functional_programming_01_pure_functions_lesson, content_python_lessons_functional_programming_02_map_filter_lesson, content_python_lessons_functional_programming_03_function_composition_lesson, content_python_lessons_functional_programming_04_immutability_lesson, content_python_lessons_functional_programming_05_partial_application_lesson [INFERRED 0.95]

## Communities (67 total, 14 thin omitted)

### Community 0 - "Concurrency & Async Lessons (Java/C++)"
Cohesion: 0.05
Nodes (75): Achievement: concurrency_async_master, Async, std::atomic, CompletableFuture, Concurrency, Daemon Threads, Debugging, ExecutorService (+67 more)

### Community 1 - "Functional Programming Lessons"
Cohesion: 0.07
Nodes (45): Achievement: core_refresher_master, Core Language Refresher (category), Function Composition, Functional Interfaces, Functional Programming, Functional Programming Master (Achievement), Functools, Higher-Order Functions (+37 more)

### Community 2 - "Error Translation & Code Editor UI"
Cohesion: 0.08
Nodes (22): extract_error_line_number(), _last_exception_type(), Translates raw interpreter/compiler output into concise, professional…, _translate_cpp_error(), translate_error(), _translate_java_error(), make_code_editor(), make_read_only_code_block() (+14 more)

### Community 3 - "Progress Store & XP Leveling"
Cohesion: 0.08
Nodes (13): _level_from_xp(), _now(), PlayerLevel, ProgressStore, Path, SQLite-backed progress, gamification, and activity tracking -- one…, Returns True if newly awarded, False if already had it., Resets to 0 automatically once the exercise is passed -- powers the "keep… (+5 more)

### Community 4 - "Exercise Content Model"
Cohesion: 0.09
Nodes (10): Exercise, The Exercise data model. Content is data, not code -- see…, ExerciseEngine, Path, Loads one language track's exercises from YAML, kept separate from application…, category -> (done, total), done computed by the caller passing completed_ids in…, A small guided set for "today's refresher" -- round-robins the next unlocked,…, classes (+2 more)

### Community 5 - "Packaging Lessons"
Cohesion: 0.09
Nodes (33): Decorators, Entry Points, JAR Files, JAR Manifest, Module Api, Naming Conventions, Packaging, Pyproject Toml (+25 more)

### Community 6 - "Observability Lessons"
Cohesion: 0.12
Nodes (29): contextvars, Instrumentation, Logging, Metrics, Observability, Observability Master (Achievement), ThreadLocal, Tracing (+21 more)

### Community 7 - "Deployment Lessons"
Cohesion: 0.12
Nodes (28): Configuration, Deployment, Deployment Master (Achievement), Environment Variables, Graceful Shutdown, Health Checks, Idempotency, JVM (+20 more)

### Community 8 - "Dependency Management Lessons"
Cohesion: 0.11
Nodes (27): Classpath, Dependency Conflict Resolution, Dependency Management, Dependency Management Master (Achievement), importlib.metadata, Lock Files, Maven Coordinates, Reproducibility (+19 more)

### Community 9 - "Cross-Language Gotchas & Off-by-One Lessons"
Cohesion: 0.14
Nodes (23): Arrays, Closures, Fallthrough, Gotchas, Late Binding, Null, Off-by-One Error, Static Local Variables (+15 more)

### Community 10 - "Execution Engine Contract (ABC)"
Cohesion: 0.20
Nodes (13): ABC, ExecutionEngine, ExecutionResult, Shared execution contract every per-language engine implements. Framing is…, Lets the UI cancel a run that's in progress (e.g. an infinite loop)., One concrete subclass per language track (python_engine.PythonEngine,…, RunHandle, PythonEngine (+5 more)

### Community 11 - "App Data Directory Resolution"
Cohesion: 0.18
Nodes (17): Path, Resolves the writable directory this app's data lives in -- a `data/` folder…, Returns <repo_root>/data, creating it if it doesn't exist yet., resolve_platform_data_dir(), get_data_dir(), get_db_path(), get_settings_path(), is_first_run() (+9 more)

### Community 12 - "Language Registry & Picker UI"
Cohesion: 0.16
Nodes (17): get_language(), LanguageInfo, The set of language tracks the app knows about, and which ones have real…, _build_language_card(), build_language_select_view(), AppState, Control, Page (+9 more)

### Community 13 - "App Router & Category Levels UI"
Cohesion: 0.17
Nodes (16): main(), Page, Root Flet application: route-based navigation between full-screen views.…, build_category_levels_view(), build_exercise_list_view(), _build_row(), Control, Page (+8 more)

### Community 14 - "Idioms/Aliasing/Static-Field Gotchas"
Cohesion: 0.11
Nodes (19): Gotcha Gauntlet Master Achievement, Idioms Gotchas Master Achievement, Idioms Gotchas Progress Achievement, Aliasing, Classes, Copying, Functions, Lists (+11 more)

### Community 15 - "Recursion Lessons"
Cohesion: 0.19
Nodes (18): Accumulator, Base Case, Mutual Recursion, Recursion, Recursion Limit, The Countdown That Never Stopped, Hitting the Stack Limit, Mutual Recursion with a Wrong Base Case (+10 more)

### Community 16 - "Sync vs Async Lessons"
Cohesion: 0.18
Nodes (18): Asyncio, Context Managers, Generators, Sync Vs Async, timeouts, Lesson: Bounding How Long You'll Wait, with statement, Lesson: Turning Manual Cleanup into a Context Manager (+10 more)

### Community 17 - "C++ Type Conversion & String Parsing Lessons"
Cohesion: 0.18
Nodes (18): Chars, String Formatting, Integer Division, StringBuilder, Strings, Type Conversion, Integer Division Truncates Silently, The Digit Character That Wasn't a Digit (+10 more)

### Community 18 - "C++ Algorithms & Lambdas Lessons"
Cohesion: 0.15
Nodes (17): Achievement: data_structures_master, Algorithms, Lambdas, Priority Queue, Searching, Functor Struct to Lambda, Manual Search Loop to std::find, What can a lambda expression replace in most modern C++ code? (+9 more)

### Community 19 - "Category Display Metadata & Topic Browser UI"
Cohesion: 0.17
Nodes (13): CategoryMeta, get_category_meta(), Display metadata (title, icon, color) for exercise categories, used by the…, _build_category_card(), build_category_map_view(), Control, Page, View (+5 more)

### Community 20 - "Quiz Screen Controller"
Cohesion: 0.24
Nodes (4): Control, View, _QuizController, Button

### Community 21 - "Quiz Content Model"
Cohesion: 0.21
Nodes (7): Path, QuizEngine, Loads a language track's quiz questions from YAML. Adding a question means…, A freshly randomized set of questions for one quiz playthrough -- which…, QuizQuestion, The QuizQuestion data model. Quiz content is data, not code -- see…, Collection

### Community 22 - "CppEngine & C++ Execution Architecture"
Cohesion: 0.23
Nodes (13): CppEngine, _describe_crash(), ExecutionResult, C++ execution engine: compiles the submitted code with `g++`, then runs the…, CLAUDE.md Architecture Overview, C++ has its own 6 categories (idioms_gotchas, core_refresher, data_structures, stdlib_deep_dive, concurrency_async, gotcha_gauntlet) instead of the shared Python/Java 14-category list, because categories like dependency_management/packaging/deployment/observability are ecosystem/tooling concepts that fit a package manager or framework better than bare C++ language/stdlib content -- ExerciseEngine.categories() derives the list purely from what's present in content/cpp/lessons/, so the smaller set required zero app-code changes, CppEngine (C++ Execution Engine), Crash-containment, not a safety sandbox: execution exists to stop a runaway loop hanging the UI (timeout, temp-dir cwd, bare filename), not to defend against adversarial/malicious code, since a professional user runs their own code on their own machine (+5 more)

### Community 23 - "AppState & Setup Wizard"
Cohesion: 0.19
Nodes (6): AppState, Page, build_setup_wizard_view(), Page, View, First-run setup: just a display name, nothing else.

### Community 24 - "C++ Collections & Performance Lessons"
Cohesion: 0.27
Nodes (14): Collections, HashMap, Performance, Sets (std::set), Linear Search to unordered_map Lookup, O(1) Front Removal with deque, Manual Duplicate Checking to std::set, The Minimum Without a Full Sort (+6 more)

### Community 25 - "Output Validator & Tests"
Cohesion: 0.26
Nodes (11): Exercise validation: checks behavior/output, not exact code formatting., True if `code` contains every required pattern. Each pattern is matched as a…, Compares output, optionally substituting what the user typed into a template. -…, validate_contains(), validate_output(), Language-Agnostic contains_patterns Structural Validation, test_validate_contains_empty_patterns_always_true(), test_validate_contains_requires_all_patterns() (+3 more)

### Community 26 - "JavaEngine & Toolchain Detection"
Cohesion: 0.18
Nodes (10): _detect_class_name(), JavaEngine, ExecutionResult, RunHandle, Java execution engine: detects the submitted code's class name, compiles it…, check_toolchain(), Detects whether a language track's real local toolchain is on PATH. Used by the…, ToolchainStatus (+2 more)

### Community 27 - "Java equals()/hashCode() Gotchas"
Cohesion: 0.15
Nodes (13): Autoboxing, Equality, equals()/hashCode() Contract, HashSet, Identity, Integer Cache, Null Handling, java.util.Objects (+5 more)

### Community 28 - "C++ RAII, Smart Pointers & Modern C++ Lessons"
Cohesion: 0.24
Nodes (12): Modern C++, Optional, RAII (Resource Acquisition Is Initialization), Smart Pointers, Structured Bindings, Manual new/delete to unique_ptr, Iterator Members to Structured Bindings, Sentinel Value to std::optional (+4 more)

### Community 29 - "Python Collections Lessons"
Cohesion: 0.18
Nodes (11): Dictionaries, Iteration, Gotcha Gauntlet: The List That Changed While Being Read, collections module, Lesson: Grouping Without Manual Key Checks, counting, Lesson: Tallying with Counter, deque (+3 more)

### Community 30 - "Stdlib Deep Dive & Exception Handling Lessons"
Cohesion: 0.24
Nodes (10): Stdlib Deep Dive Master Achievement, Contextlib, Exceptions, finally Block, Reflection, Detecting an Optional Dependency Gracefully, Idioms & Gotchas: The finally Block That Ate the Return, What does Class.forName(name) throw if the class isn't on the classpath? (+2 more)

### Community 31 - "Settings Screen UI"
Cohesion: 0.47
Nodes (9): _build_font_card(), build_settings_view(), _build_theme_card(), _build_theme_option(), Control, Page, View, Settings: theme presets and code font size. (+1 more)

### Community 32 - "C++ Integer Overflow & Virtual Destructor Lessons"
Cohesion: 0.33
Nodes (10): Destructors, Inheritance, Integers, Overflow, Virtual Functions, The Overflow That Silently Wrapped, The Destructor That Never Ran, What actually happens when a signed int overflows past INT_MAX in C++ (on virtually all mainstream platforms)? (+2 more)

### Community 33 - "Theme Presets & Quiz Bank UI"
Cohesion: 0.28
Nodes (5): Quiz Bank: pick a question count, answer a randomized multiple-choice run, end…, get_preset(), Color/theme presets -- professional dark-IDE palettes plus one light option., resolve_font_scale(), ThemePreset

### Community 34 - "C++ auto & Range-Based For Lessons"
Cohesion: 0.32
Nodes (8): auto Type Deduction Keyword, Loops, Range-Based For Loop, Type Deduction, Index Loop to Range-Based For, Spelling Out a Type auto Could Deduce, What's the main advantage of a range-based for loop over an index-based one?, What does the `auto` keyword do in a variable declaration?

### Community 35 - "Java Sorting & Comparator Lessons"
Cohesion: 0.33
Nodes (7): Comparator, Sorting, TreeMap, Manual Bubble Sort to std::sort, Why prefer std::sort over a hand-written bubble sort in application code?, Sorting by a Custom Field with Comparator, Keys That Sort Themselves with TreeMap

### Community 36 - "C++ Pass-by-Reference & Operator Gotchas"
Cohesion: 0.43
Nodes (7): Operators, Pass By Reference, References, Pass-by-Value Silently Ignored the Caller, The if That Assigned Instead of Compared, Why doesn't a function taking `int x` (by value) modify the caller's variable?, What does `if (x = 1)` do, as opposed to `if (x == 1)`?

### Community 40 - "Recursive Data Structure Lessons"
Cohesion: 0.47
Nodes (6): Data Structures, Tree Structures, Summing an Unbalanced Tree, How do you correctly sum every value in a binary tree recursively?, Flattening an Arbitrarily Nested List, Why does flattening a nested list need recursion?

### Community 41 - "Float Precision Lessons"
Cohesion: 0.50
Nodes (5): Decimal, Floats, Precision, The Price That Rounded the Wrong Way, 0.1 + 0.2 Is Not Quite 0.3

### Community 42 - "Java Time/Duration Lesson"
Cohesion: 0.67
Nodes (3): Duration, java.time, Stdlib Deep Dive: Durations with java.time Instead of Raw Millis

### Community 43 - "Pathlib Lesson"
Cohesion: 0.67
Nodes (3): Filesystem, Pathlib, Paths as Objects, Not Strings

### Community 44 - "Memoization Lesson"
Cohesion: 1.00
Nodes (3): Memoization, Memoizing a Recursive Method by Hand, What's Java's equivalent of Python's @lru_cache decorator?

### Community 45 - "Comprehension Lesson"
Cohesion: 0.67
Nodes (3): comprehensions, lists, Lesson: Loop to Comprehension

### Community 46 - "Slicing Off-by-One Lesson"
Cohesion: 0.67
Nodes (3): off-by-one errors, slicing, Lesson: The Off-By-One Slice

## Ambiguous Edges - Review These
- `_translate_cpp_error()` → `C++ Compiler/Runtime Error Translation (_translate_cpp_error, CPP_FRIENDLY)`  [AMBIGUOUS]
  CLAUDE.md · relation: conceptually_related_to

## Knowledge Gaps
- **70 isolated node(s):** `run.sh script`, `coding-adventure`, `Autoboxing`, `Closures`, `equals()/hashCode() Contract` (+65 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **14 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `_translate_cpp_error()` and `C++ Compiler/Runtime Error Translation (_translate_cpp_error, CPP_FRIENDLY)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `Gotchas` connect `Cross-Language Gotchas & Off-by-One Lessons` to `Concurrency & Async Lessons (Java/C++)`, `C++ Integer Overflow & Virtual Destructor Lessons`, `Functional Programming Lessons`, `C++ Pass-by-Reference & Operator Gotchas`, `Packaging Lessons`, `Observability Lessons`, `Deployment Lessons`, `Dependency Management Lessons`, `Float Precision Lessons`, `Idioms/Aliasing/Static-Field Gotchas`, `Recursion Lessons`, `Slicing Off-by-One Lesson`, `C++ Type Conversion & String Parsing Lessons`, `Sync vs Async Lessons`, `C++ Collections & Performance Lessons`, `Java equals()/hashCode() Gotchas`, `Python Collections Lessons`, `Stdlib Deep Dive & Exception Handling Lessons`?**
  _High betweenness centrality (0.649) - this node is a cross-community bridge._
- **Why does `C++ has its own 6 categories (idioms_gotchas, core_refresher, data_structures, stdlib_deep_dive, concurrency_async, gotcha_gauntlet) instead of the shared Python/Java 14-category list, because categories like dependency_management/packaging/deployment/observability are ecosystem/tooling concepts that fit a package manager or framework better than bare C++ language/stdlib content -- ExerciseEngine.categories() derives the list purely from what's present in content/cpp/lessons/, so the smaller set required zero app-code changes` connect `CppEngine & C++ Execution Architecture` to `C++ Type Conversion & String Parsing Lessons`, `Category Display Metadata & Topic Browser UI`?**
  _High betweenness centrality (0.457) - this node is a cross-community bridge._
- **Why does `Integer Division Truncates Silently` connect `C++ Type Conversion & String Parsing Lessons` to `Cross-Language Gotchas & Off-by-One Lessons`, `C++ Pass-by-Reference & Operator Gotchas`, `CppEngine & C++ Execution Architecture`?**
  _High betweenness centrality (0.455) - this node is a cross-community bridge._
- **Are the 17 inferred relationships involving `AppState` (e.g. with `Settings` and `ExerciseEngine`) actually correct?**
  _`AppState` has 17 INFERRED edges - model-reasoned connections that need verification._
- **What connects `run.sh script`, `coding-adventure`, `Autoboxing` to the rest of the system?**
  _70 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Concurrency & Async Lessons (Java/C++)` be split into smaller, more focused modules?**
  _Cohesion score 0.05477477477477478 - nodes in this community are weakly interconnected._