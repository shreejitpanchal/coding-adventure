# Graph Report - coding-adventure  (2026-08-24)

## Corpus Check
- 44 files · ~87,407 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 951 nodes · 1827 edges · 76 communities (54 shown, 22 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 135 edges (avg confidence: 0.89)
- Token cost: 315,351 input · 0 output

## Community Hubs (Navigation)
- Spring AOP & Bean Lifecycle Docs
- Functional Programming Lessons (Python/C++)
- Data Structures & Algorithms Lessons
- Progress Store & XP Leveling
- Exercise Content Model & Category Logic
- Error Translation (All Languages)
- Configuration & Deployment Lessons
- Observability Lessons
- Packaging Lessons
- Dependency Management Lessons
- Concurrency Coordination Lessons (Threads/Locks/Signals)
- App Data Directory Resolution
- Recursion: Base Case & Mutual Recursion
- Language Registry & Picker UI
- App Router & Category Levels UI
- C++ Sync vs Async Lessons
- Cross-Language Idioms & Off-by-One Gotchas
- Sync vs Async Lessons (Python)
- Java Concurrency Lessons
- Execution Engine Contract (All Languages)
- Python Idioms & Aliasing Gotchas
- Category Display Metadata & Topic Browser UI
- Quiz Screen Controller
- Quiz Content Model
- C++ Gotcha Gauntlet & Category Ordering
- Stdlib Deep Dive & Exception Handling Lessons
- AppState & Setup Wizard
- Tooling Docs & Toolchain Detection
- SpringEngine & RunHandle
- Recursion: Memoization & Tail Recursion
- Java equals()/hashCode() Gotchas
- Output Validator & Tests
- Spring Dependency Injection
- CppEngine & C++ Execution Tests
- Python Collections Lessons
- Settings Screen UI
- C++ Thread Scheduling Lessons
- C++ String/Stdlib Parsing Lessons
- Theme Presets & Quiz Bank UI
- Race Conditions & Atomics Lessons
- Exercise & ExecutionEngine Base Classes
- Code Editor UI
- Spring Execution Engine Tests
- Float Precision Lessons
- Java Time/Duration Lesson
- Pathlib Lesson
- Comprehension Lesson
- run.sh Launcher Script
- Itertools Lesson
- Typing Hints Lesson
- Enum Lesson
- ExecutionResult (isolated ref)
- ExecutionResult (isolated ref)
- RunHandle (isolated ref)
- AppState (isolated ref)
- Control (Flet base class ref)
- ExecutionResult (isolated ref)
- Page (Flet base class ref)
- RunHandle (isolated ref)
- View (Flet base class ref)
- ExecutionEngine (isolated ref)
- Exercise (isolated ref)
- Project Root
- Spring Maven Scaffold Artifact
- Flet Dependency
- Pytest Dependency
- PyYAML Dependency
- RunHandle (isolated ref)

## God Nodes (most connected - your core abstractions)
1. `Gotchas` - 93 edges
2. `Threading` - 42 edges
3. `AppState` - 39 edges
4. `Recursion` - 32 edges
5. `ProgressStore` - 28 edges
6. `Exercise` - 26 edges
7. `Observability` - 24 edges
8. `Functional Programming` - 24 edges
9. `_ExerciseController` - 23 edges
10. `Concurrency` - 23 edges

## Surprising Connections (you probably didn't know these)
- `Lesson: Cutting Boilerplate with @dataclass` --semantically_similar_to--> `Exercise`  [INFERRED] [semantically similar]
  content/python/lessons/core_refresher_05_dataclasses.yaml → app/engine/exercise.py
- `/verify slash command` --references--> `test_loads_spring_content()`  [AMBIGUOUS]
  .claude/commands/verify.md → tests/test_lesson_engine.py
- `ExecutionEngine ABC` --conceptually_related_to--> `ExecutionEngine`  [EXTRACTED]
  .claude/skills/add-language-content/SKILL.md → app/execution/base.py
- `add-language-content skill` --references--> `LanguageInfo`  [EXTRACTED]
  .claude/skills/add-language-content/SKILL.md → app/engine/languages.py
- `C++ track category expansion rationale` --conceptually_related_to--> `Recursion`  [AMBIGUOUS]
  docs/DEVELOPMENT.md → content/cpp/quiz/quiz_questions.yaml

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **thread_scheduling Category Progression** — content_cpp_lessons_thread_scheduling_01_sleep_for_not_busy_wait_exercise, content_cpp_lessons_thread_scheduling_02_this_thread_yield_exercise, content_cpp_lessons_thread_scheduling_03_joining_all_threads_in_a_vector_exercise, content_cpp_lessons_thread_scheduling_04_explicit_async_launch_policy_exercise, content_cpp_lessons_thread_scheduling_05_condition_variable_producer_consumer_exercise [INFERRED 0.85]
- **sync_vs_async Category Progression** — content_cpp_lessons_sync_vs_async_01_future_get_called_twice_exercise, content_cpp_lessons_sync_vs_async_02_exception_propagation_through_future_exercise, content_cpp_lessons_sync_vs_async_03_shared_future_multiple_waiters_exercise, content_cpp_lessons_sync_vs_async_04_synchronous_wrapper_over_async_api_exercise, content_cpp_lessons_sync_vs_async_05_deferred_launch_runs_on_get_exercise [INFERRED 0.85]
- **functional_programming Category Progression** — content_cpp_lessons_functional_programming_01_lambda_capture_by_value_in_loop_exercise, content_cpp_lessons_functional_programming_02_std_function_wrapping_lambda_exercise, content_cpp_lessons_functional_programming_03_std_transform_algorithm_exercise, content_cpp_lessons_functional_programming_04_std_accumulate_with_lambda_exercise, content_cpp_lessons_functional_programming_05_higher_order_function_returning_lambda_exercise [INFERRED 0.85]
- **C++ Recursion Exercise Progression** — content_cpp_lessons_recursion_01_missing_base_case_exercise, content_cpp_lessons_recursion_02_off_by_one_base_case_exercise, content_cpp_lessons_recursion_03_memoization_with_unordered_map_exercise, content_cpp_lessons_recursion_04_tail_recursion_accumulator_exercise, content_cpp_lessons_recursion_05_mutual_recursion_exercise, concept_recursion [EXTRACTED 1.00]
- **Spring Events Exercise Progression** — content_spring_lessons_events_01_publish_forgotten_exercise, content_spring_lessons_events_02_missing_eventlistener_annotation_exercise, content_spring_lessons_events_03_multiple_listeners_fan_out_exercise, content_spring_lessons_events_04_conditional_event_listener_exercise, content_spring_lessons_events_05_custom_event_payload_exercise, concept_events [EXTRACTED 1.00]
- **C++ Gotcha Gauntlet Exercise Progression** — content_cpp_lessons_gotcha_gauntlet_01_off_by_one_array_exercise, content_cpp_lessons_gotcha_gauntlet_02_uncaught_out_of_range_exercise, content_cpp_lessons_gotcha_gauntlet_03_static_variable_persistence_exercise, content_cpp_lessons_gotcha_gauntlet_04_integer_overflow_exercise, content_cpp_lessons_gotcha_gauntlet_05_missing_virtual_destructor_exercise, concept_gotchas [EXTRACTED 1.00]
- **AOP Exercise Progression (aop_01-aop_05)** — content_spring_lessons_aop_01_missing_aspect_annotation, content_spring_lessons_aop_02_pointcut_expression_wrong_method, content_spring_lessons_aop_03_afterreturning_captures_result, content_spring_lessons_aop_04_around_advice_modifying_result, content_spring_lessons_aop_05_self_invocation_bypasses_proxy [EXTRACTED 1.00]
- **Spring Track Expansion Documentation** — claude, readme, docs_architecture, docs_development, concept_spring_category_expansion [INFERRED 0.85]
- **AOP Quiz-Exercise Reinforcement Cluster** — content_spring_quiz_quiz_questions_q27, content_spring_quiz_quiz_questions_q28, content_spring_quiz_quiz_questions_q29, content_spring_quiz_quiz_questions_q30, content_spring_quiz_quiz_questions_q31, content_spring_quiz_quiz_questions_q32, content_spring_quiz_quiz_questions_q33, content_spring_quiz_quiz_questions_q34, content_spring_lessons_aop_01_missing_aspect_annotation, content_spring_lessons_aop_02_pointcut_expression_wrong_method, content_spring_lessons_aop_03_afterreturning_captures_result, content_spring_lessons_aop_04_around_advice_modifying_result, content_spring_lessons_aop_05_self_invocation_bypasses_proxy [INFERRED 0.85]
- **Concurrency & Async Lesson Progression** — content_java_lessons_concurrency_async_01_race_condition_synchronized_lesson, content_java_lessons_concurrency_async_02_atomic_integer_lesson, content_java_lessons_concurrency_async_03_executor_service_lesson, content_java_lessons_concurrency_async_04_completable_future_lesson, content_java_lessons_concurrency_async_05_executor_await_termination_lesson, achievement_concurrency_async_master [EXTRACTED 0.95]
- **Core Language Refresher Lesson Progression** — content_java_lessons_core_refresher_01_lambda_expression_lesson, content_java_lessons_core_refresher_02_streams_filter_map_lesson, content_java_lessons_core_refresher_03_optional_lesson, content_java_lessons_core_refresher_04_record_class_lesson, content_java_lessons_core_refresher_05_try_with_resources_lesson, achievement_core_refresher_master [EXTRACTED 0.95]
- **Data Structures Lesson Progression** — content_java_lessons_data_structures_01_hashmap_iteration_order_lesson, content_java_lessons_data_structures_02_arraydeque_queue_lesson, content_java_lessons_data_structures_03_comparator_custom_sort_lesson, content_java_lessons_data_structures_04_treemap_sorted_keys_lesson, content_java_lessons_data_structures_05_priority_queue_lesson, achievement_data_structures_master [EXTRACTED 0.95]
- **Gotcha Gauntlet Lesson Sequence** — content_python_lessons_gotcha_gauntlet_02_exception_swallowing_lesson, content_python_lessons_gotcha_gauntlet_03_mutable_class_attribute_lesson, content_python_lessons_gotcha_gauntlet_04_rounding_precision_lesson, content_python_lessons_gotcha_gauntlet_05_dict_mutation_during_iteration_lesson, content_python_lessons_gotcha_gauntlet_06_missing_super_init_lesson [EXTRACTED 1.00]
- **Gotcha Gauntlet Lesson Series** — content_java_lessons_gotcha_gauntlet_01_off_by_one_loop_lesson, content_java_lessons_gotcha_gauntlet_02_switch_fallthrough_lesson, content_java_lessons_gotcha_gauntlet_03_concurrent_modification_lesson, content_java_lessons_gotcha_gauntlet_04_integer_overflow_lesson, content_java_lessons_gotcha_gauntlet_05_equals_hashcode_contract_lesson [EXTRACTED 1.00]
- **Idioms Gotchas Lesson Sequence** — content_python_lessons_idioms_gotchas_01_mutable_default_arg_lesson, content_python_lessons_idioms_gotchas_02_late_binding_closure_lesson, content_python_lessons_idioms_gotchas_03_is_vs_equals_lesson, content_python_lessons_idioms_gotchas_04_float_precision_lesson, content_python_lessons_idioms_gotchas_05_aliasing_vs_copying_lesson, content_python_lessons_idioms_gotchas_06_sort_returns_none_lesson [EXTRACTED 1.00]
- **Stdlib Deep Dive Lesson Sequence** — content_python_lessons_stdlib_deep_dive_01_itertools_chain_lesson, content_python_lessons_stdlib_deep_dive_02_lru_cache_lesson, content_python_lessons_stdlib_deep_dive_03_reduce_lesson, content_python_lessons_stdlib_deep_dive_04_pathlib_lesson, content_python_lessons_stdlib_deep_dive_05_typing_hints_lesson, content_python_lessons_stdlib_deep_dive_06_contextlib_suppress_lesson [EXTRACTED 1.00]
- **Deployment Lifecycle Operational Concerns** — content_java_lessons_deployment_03_shutdown_hook_lesson, content_java_lessons_deployment_04_health_check_lesson, content_java_lessons_deployment_05_idempotent_deploy_step_lesson [INFERRED 0.70]
- **Field Injection Timing/Reflection Gotcha Pattern** — content_spring_lessons_dependency_injection_01_field_injection_untestable_exercise, content_spring_lessons_dependency_injection_05_constructor_injection_final_fields_exercise, content_spring_lessons_bean_lifecycle_03_postconstruct_initialization_exercise [INFERRED 0.75]
- **Lessons Demonstrating Recursion-Misuse Failure Modes** — content_python_lessons_recursion_01_missing_base_case_lesson, content_python_lessons_recursion_02_recursion_depth_limit_lesson, content_python_lessons_thread_scheduling_01_reentrant_lock_lesson [INFERRED 0.75]
- **Language content verification workflow** — _claude_commands_verify_command, _claude_skills_add_language_content_skill_skill, concept_real_toolchain_verification [INFERRED 0.80]
- **Java Equality & Hashing Pitfalls** — content_java_lessons_idioms_gotchas_01_string_equality_lesson, content_java_lessons_idioms_gotchas_02_integer_caching_lesson, content_java_lessons_gotcha_gauntlet_05_equals_hashcode_contract_lesson, content_java_lessons_stdlib_deep_dive_03_objects_equals_null_safe_lesson [INFERRED 0.80]
- **Logger/Handler Level Threshold Pattern** — content_java_lessons_observability_01_structured_logging_lesson, content_java_lessons_observability_02_log_level_filtering_lesson, concept_logging [INFERRED 0.80]
- **Configuration & Profiles learning progression** — content_spring_lessons_configuration_profiles_01_value_default_placeholder_exercise, content_spring_lessons_configuration_profiles_02_profile_specific_bean_exercise, content_spring_lessons_configuration_profiles_03_profile_negation_exercise, content_spring_lessons_configuration_profiles_04_environment_getproperty_exercise, content_spring_lessons_configuration_profiles_05_required_property_no_default_exercise [INFERRED 0.85]
- **C++ Concurrency Learning Progression** — content_cpp_lessons_concurrency_async_01_race_condition_mutex_exercise, content_cpp_lessons_concurrency_async_02_atomic_counter_exercise, content_cpp_lessons_concurrency_async_03_future_async_exercise, content_cpp_lessons_concurrency_async_04_thread_join_missing_exercise, content_cpp_lessons_concurrency_async_05_promise_future_signal_exercise [INFERRED 0.85]
- **Modern C++ Idioms Progression** — content_cpp_lessons_core_refresher_01_range_based_for_exercise, content_cpp_lessons_core_refresher_02_auto_type_deduction_exercise, content_cpp_lessons_core_refresher_03_lambda_expression_exercise, content_cpp_lessons_core_refresher_04_smart_pointer_unique_ptr_exercise, content_cpp_lessons_core_refresher_05_structured_bindings_exercise [INFERRED 0.85]
- **STL Container Selection Progression** — content_cpp_lessons_data_structures_01_sort_vector_exercise, content_cpp_lessons_data_structures_02_unordered_map_lookup_exercise, content_cpp_lessons_data_structures_03_deque_front_operations_exercise, content_cpp_lessons_data_structures_04_set_for_uniqueness_exercise, content_cpp_lessons_data_structures_05_priority_queue_exercise [INFERRED 0.85]
- **Bean Lifecycle Learning Progression** — content_spring_lessons_bean_lifecycle_01_missing_component_annotation_exercise, content_spring_lessons_bean_lifecycle_02_singleton_shared_state_exercise, content_spring_lessons_bean_lifecycle_03_postconstruct_initialization_exercise, content_spring_lessons_bean_lifecycle_04_predestroy_cleanup_exercise, content_spring_lessons_bean_lifecycle_05_lazy_initialization_exercise [INFERRED 0.85]
- **Dependency Injection Learning Progression** — content_spring_lessons_dependency_injection_01_field_injection_untestable_exercise, content_spring_lessons_dependency_injection_02_ambiguous_bean_no_qualifier_exercise, content_spring_lessons_dependency_injection_03_primary_bean_exercise, content_spring_lessons_dependency_injection_04_optional_dependency_exercise, content_spring_lessons_dependency_injection_05_constructor_injection_final_fields_exercise [INFERRED 0.85]
- **C++ Idioms & Gotchas Learning Progression** — content_cpp_lessons_idioms_gotchas_01_integer_division_truncation, content_cpp_lessons_idioms_gotchas_02_pass_by_value_no_mutation, content_cpp_lessons_idioms_gotchas_03_assignment_in_condition, content_cpp_lessons_idioms_gotchas_04_unsigned_underflow_loop, content_cpp_lessons_idioms_gotchas_05_char_digit_conversion [INFERRED 0.85]
- **JVM Packaging and Build Artifact Progression** — content_java_lessons_packaging_01_manifest_main_class_lesson, content_java_lessons_packaging_02_package_naming_convention_lesson, content_java_lessons_packaging_03_semver_bump_lesson, content_java_lessons_packaging_04_service_registry_lesson, content_java_lessons_packaging_05_jar_filename_parsing_lesson [INFERRED 0.85]
- **Category-Capstone Lessons Awarding a Mastery Achievement** — content_python_lessons_packaging_05_wheel_filename_parsing_lesson, content_python_lessons_recursion_05_accumulator_pattern_lesson, content_python_lessons_sync_vs_async_05_async_for_generator_lesson, content_python_lessons_thread_scheduling_05_thread_local_storage_lesson [INFERRED 0.85]
- **C++ Standard Library Deep Dive Learning Progression** — content_cpp_lessons_stdlib_deep_dive_01_string_stream_parsing, content_cpp_lessons_stdlib_deep_dive_02_stoi_invalid_argument, content_cpp_lessons_stdlib_deep_dive_03_to_string, content_cpp_lessons_stdlib_deep_dive_04_algorithm_find, content_cpp_lessons_stdlib_deep_dive_05_optional_value [INFERRED 0.85]
- **CompletableFuture Async Pipeline Progression** — content_java_lessons_sync_vs_async_01_completablefuture_chaining_lesson, content_java_lessons_sync_vs_async_02_completablefuture_combine_lesson, content_java_lessons_sync_vs_async_03_completablefuture_exceptionally_lesson, content_java_lessons_sync_vs_async_04_supplyasync_custom_executor_lesson, content_java_lessons_sync_vs_async_05_virtual_threads_lesson [INFERRED 0.85]
- **Thread Lifecycle Management Progression** — content_java_lessons_thread_scheduling_01_thread_naming_lesson, content_java_lessons_thread_scheduling_02_daemon_flag_lesson, content_java_lessons_thread_scheduling_03_thread_priority_lesson, content_java_lessons_thread_scheduling_04_blocking_queue_lesson, content_java_lessons_thread_scheduling_05_interrupt_handling_lesson [INFERRED 0.85]
- **Lexicographic vs Numeric Version Comparison Pattern** — content_java_lessons_dependency_management_01_version_string_comparison_lesson, content_java_lessons_dependency_management_04_minimum_version_check_lesson, concept_versioning [INFERRED 0.85]
- **Dependency Management Lesson Progression** — content_python_lessons_dependency_management_01_detect_virtualenv_lesson, content_python_lessons_dependency_management_02_parse_requirement_line_lesson, content_python_lessons_dependency_management_03_version_string_comparison_lesson, content_python_lessons_dependency_management_04_importlib_metadata_lesson, content_python_lessons_dependency_management_05_lock_file_pin_lesson [INFERRED 0.95]
- **Deployment Lesson Progression** — content_python_lessons_deployment_01_env_var_defaults_lesson, content_python_lessons_deployment_02_feature_flag_boolean_parsing_lesson, content_python_lessons_deployment_03_graceful_shutdown_signal_lesson, content_python_lessons_deployment_04_health_check_lesson, content_python_lessons_deployment_05_idempotent_deploy_step_lesson [INFERRED 0.95]
- **Functional Programming Lesson Progression** — content_python_lessons_functional_programming_01_pure_functions_lesson, content_python_lessons_functional_programming_02_map_filter_lesson, content_python_lessons_functional_programming_03_function_composition_lesson, content_python_lessons_functional_programming_04_immutability_lesson, content_python_lessons_functional_programming_05_partial_application_lesson [INFERRED 0.95]

## Communities (76 total, 22 thin omitted)

### Community 0 - "Spring AOP & Bean Lifecycle Docs"
Cohesion: 0.06
Nodes (62): @AfterReturning advice, Aspect-Oriented Programming (AOP), ApplicationEventPublisher, @Around advice, @Aspect annotation, Bean Lifecycle, Bean Scope, @Before advice (+54 more)

### Community 1 - "Functional Programming Lessons (Python/C++)"
Cohesion: 0.06
Nodes (56): Achievement: core_refresher_master, Closures, Core Language Refresher (category), Function Composition, Functional Interfaces, Functional Programming, Functional Programming Master (Achievement), Functools (+48 more)

### Community 2 - "Data Structures & Algorithms Lessons"
Cohesion: 0.06
Nodes (52): Achievement: data_structures_master, Algorithms, auto Type Deduction Keyword, Collections, Comparator, Data Structures, Fold/Reduce (Functional), Loops (+44 more)

### Community 3 - "Progress Store & XP Leveling"
Cohesion: 0.08
Nodes (13): _level_from_xp(), _now(), PlayerLevel, ProgressStore, Path, SQLite-backed progress, gamification, and activity tracking -- one…, Returns True if newly awarded, False if already had it., Resets to 0 automatically once the exercise is passed -- powers the "keep… (+5 more)

### Community 4 - "Exercise Content Model & Category Logic"
Cohesion: 0.09
Nodes (10): Exercise, ExerciseEngine, Path, Loads one language track's exercises from YAML, kept separate from application…, category -> (done, total), done computed by the caller passing completed_ids in…, A small guided set for "today's refresher" -- round-robins the next unlocked,…, classes, dataclasses (+2 more)

### Community 5 - "Error Translation (All Languages)"
Cohesion: 0.12
Nodes (13): extract_error_line_number(), _last_exception_type(), Translates raw interpreter/compiler output into concise, professional…, _translate_cpp_error(), translate_error(), _translate_java_error(), _translate_spring_error(), build_lesson_view() (+5 more)

### Community 6 - "Configuration & Deployment Lessons"
Cohesion: 0.12
Nodes (32): configuration_profiles_master achievement, Configuration, Configuration & Profiles (Spring category), Deployment, Deployment Master (Achievement), Environment Variables, Graceful Shutdown, Idempotency (+24 more)

### Community 7 - "Observability Lessons"
Cohesion: 0.11
Nodes (32): contextvars, Health Checks, Instrumentation, Logging, Metrics, Observability, Observability Master (Achievement), ThreadLocal (+24 more)

### Community 8 - "Packaging Lessons"
Cohesion: 0.10
Nodes (31): Decorators, Entry Points, JAR Files, JAR Manifest, Module Api, Naming Conventions, Packaging, Pyproject Toml (+23 more)

### Community 9 - "Dependency Management Lessons"
Cohesion: 0.10
Nodes (30): Classpath, Dependency Conflict Resolution, Dependency Management, Dependency Management Master (Achievement), importlib.metadata, Lock Files, Maven Coordinates, Reflection (+22 more)

### Community 10 - "Concurrency Coordination Lessons (Threads/Locks/Signals)"
Cohesion: 0.12
Nodes (29): std::condition_variable, Daemon Threads, Thread Interruption, Locks, Producer Consumer, std::promise / std::future Signaling, Queue, Thread Local Storage (+21 more)

### Community 11 - "App Data Directory Resolution"
Cohesion: 0.18
Nodes (17): Path, Resolves the writable directory this app's data lives in -- a `data/` folder…, Returns <repo_root>/data, creating it if it doesn't exist yet., resolve_platform_data_dir(), get_data_dir(), get_db_path(), get_settings_path(), is_first_run() (+9 more)

### Community 12 - "Recursion: Base Case & Mutual Recursion"
Cohesion: 0.16
Nodes (21): Base Case, Mutual Recursion, Recursion, Recursion Limit, Recursion Master Achievement, Two Functions, Taking Turns, Quiz q51: Recursion With No Base Case, Quiz q52: Exact-Equality Base Case vs Range Check (+13 more)

### Community 13 - "Language Registry & Picker UI"
Cohesion: 0.16
Nodes (17): get_language(), LanguageInfo, The set of language tracks the app knows about, and which ones have real…, _build_language_card(), build_language_select_view(), AppState, Control, Page (+9 more)

### Community 14 - "App Router & Category Levels UI"
Cohesion: 0.17
Nodes (16): main(), Page, Root Flet application: route-based navigation between full-screen views.…, build_category_levels_view(), build_exercise_list_view(), _build_row(), Control, Page (+8 more)

### Community 15 - "C++ Sync vs Async Lessons"
Cohesion: 0.27
Nodes (20): API Design, Async, std::launch::deferred, std::future, std::launch Policy, std::shared_future, Running a Computation Asynchronously, std::future::get() Called Twice (+12 more)

### Community 16 - "Cross-Language Idioms & Off-by-One Gotchas"
Cohesion: 0.16
Nodes (20): Arrays, Fallthrough, Gotchas, Null, Off-by-One Error, switch Statement, The Array Read That Went One Too Far, Integer Division Truncates Silently (+12 more)

### Community 17 - "Sync vs Async Lessons (Python)"
Cohesion: 0.16
Nodes (20): Asyncio, Context Managers, Generators, Sync Vs Async, locks, Lesson: The Async Equivalent of a Race Condition, timeouts, Lesson: Bounding How Long You'll Wait (+12 more)

### Community 18 - "Java Concurrency Lessons"
Cohesion: 0.21
Nodes (19): Achievement: concurrency_async_master, CompletableFuture, Concurrency, ExecutorService, Virtual Threads, ExecutorService Instead of Raw Threads, Async Computation with CompletableFuture, shutdown() Doesn't Wait -- awaitTermination() Does (+11 more)

### Community 19 - "Execution Engine Contract (All Languages)"
Cohesion: 0.22
Nodes (12): ExecutionEngine, ExecutionResult, One concrete subclass per language track (python_engine.PythonEngine,…, exercise is unused by the single-file engines (Python/Java/C++) -- SpringEngine…, CppEngine, _detect_class_name(), JavaEngine, Java execution engine: detects the submitted code's class name, compiles it… (+4 more)

### Community 20 - "Python Idioms & Aliasing Gotchas"
Cohesion: 0.12
Nodes (17): Idioms Gotchas Master Achievement, Idioms Gotchas Progress Achievement, Aliasing, Classes, Copying, Functions, Lists, Mutable Defaults (+9 more)

### Community 21 - "Category Display Metadata & Topic Browser UI"
Cohesion: 0.17
Nodes (13): CategoryMeta, get_category_meta(), Display metadata (title, icon, color) for exercise categories, used by the…, _build_category_card(), build_category_map_view(), Control, Page, View (+5 more)

### Community 22 - "Quiz Screen Controller"
Cohesion: 0.24
Nodes (4): Control, View, _QuizController, Button

### Community 23 - "Quiz Content Model"
Cohesion: 0.21
Nodes (7): Path, QuizEngine, Loads a language track's quiz questions from YAML. Adding a question means…, A freshly randomized set of questions for one quiz playthrough -- which…, QuizQuestion, The QuizQuestion data model. Quiz content is data, not code -- see…, Collection

### Community 24 - "C++ Gotcha Gauntlet & Category Ordering"
Cohesion: 0.18
Nodes (15): Category Level Ordering, Destructors, Gotcha Gauntlet Master Achievement, Inheritance, Integers, Integer Overflow, Static Local Variables, std::vector (+7 more)

### Community 25 - "Stdlib Deep Dive & Exception Handling Lessons"
Cohesion: 0.18
Nodes (14): Stdlib Deep Dive Master Achievement, Contextlib, Debugging, Exceptions, finally Block, Idioms & Gotchas: The finally Block That Ate the Return, Recovering from a Failed Async Computation, Naming Threads for Debuggable Logs (+6 more)

### Community 26 - "AppState & Setup Wizard"
Cohesion: 0.19
Nodes (6): AppState, Page, build_setup_wizard_view(), Page, View, First-run setup: just a display name, nothing else.

### Community 27 - "Tooling Docs & Toolchain Detection"
Cohesion: 0.18
Nodes (12): /verify slash command, add-language-content skill, CATEGORY_META dict (code), check_toolchain(), Detects whether a language track's real local toolchain is on PATH. Used by the…, ToolchainStatus, CATEGORY_META display metadata, Category parity across language tracks (+4 more)

### Community 28 - "SpringEngine & RunHandle"
Cohesion: 0.21
Nodes (8): Lets the UI cancel a run that's in progress (e.g. an infinite loop)., RunHandle, _detect_class_name(), Spring execution engine: unlike the single-file engines, a Spring exercise…, Maven reports absolute paths (both backslash and the forward-slash form it uses…, _sanitize_path(), SpringEngine, Popen

### Community 29 - "Recursion: Memoization & Tail Recursion"
Cohesion: 0.22
Nodes (13): Accumulator, HashMap, Memoization, Performance, Tail Recursion, Remembering What You've Already Computed, Carrying the Answer Along Instead of Building It on the Way Back, Quiz q53: Memoization in Recursive Fibonacci (+5 more)

### Community 30 - "Java equals()/hashCode() Gotchas"
Cohesion: 0.15
Nodes (13): Autoboxing, Equality, equals()/hashCode() Contract, HashSet, Identity, Integer Cache, Null Handling, java.util.Objects (+5 more)

### Community 31 - "Output Validator & Tests"
Cohesion: 0.27
Nodes (10): Exercise validation: checks behavior/output, not exact code formatting., True if `code` contains every required pattern. Each pattern is matched as a…, Compares output, optionally substituting what the user typed into a template. -…, validate_contains(), validate_output(), test_validate_contains_empty_patterns_always_true(), test_validate_contains_requires_all_patterns(), test_validate_output_exact_match() (+2 more)

### Community 32 - "Spring Dependency Injection"
Cohesion: 0.27
Nodes (12): Ambiguous Bean Resolution, Constructor Injection, Dependency Injection, Optional Dependency, @Primary Bean, @Qualifier, Testability, The Bean That Couldn't Be Unit Tested (+4 more)

### Community 34 - "Python Collections Lessons"
Cohesion: 0.18
Nodes (11): Dictionaries, Iteration, Gotcha Gauntlet: The List That Changed While Being Read, collections module, Lesson: Grouping Without Manual Key Checks, counting, Lesson: Tallying with Counter, deque (+3 more)

### Community 35 - "Settings Screen UI"
Cohesion: 0.47
Nodes (9): _build_font_card(), build_settings_view(), _build_theme_card(), _build_theme_option(), Control, Page, View, Settings: theme presets and code font size. (+1 more)

### Community 36 - "C++ Thread Scheduling Lessons"
Cohesion: 0.33
Nodes (10): Busy-Waiting, Thread Join, sleep_for (Thread Wait), std::this_thread::yield, sleep_for vs Busy-Wait, std::this_thread::yield in a Spin Loop, Joining All Threads in a Vector, Quiz q36: Busy-Wait vs sleep_for (+2 more)

### Community 37 - "C++ String/Stdlib Parsing Lessons"
Cohesion: 0.24
Nodes (10): String Formatting, Regular Expressions, StringBuilder, Strings, Manual Digit Parsing to stringstream, The Crash from Parsing a Non-Numeric String, stringstream to std::to_string, Stdlib Deep Dive: Building a String in a Loop (+2 more)

### Community 38 - "Theme Presets & Quiz Bank UI"
Cohesion: 0.28
Nodes (5): Quiz Bank: pick a question count, answer a randomized multiple-choice run, end…, get_preset(), Color/theme presets -- professional dark-IDE palettes plus one light option., resolve_font_scale(), ThemePreset

### Community 39 - "Race Conditions & Atomics Lessons"
Cohesion: 0.25
Nodes (9): std::atomic, Mutex (std::mutex / lock_guard), Race Conditions, synchronized, The Counter Two Threads Corrupted, std::atomic Instead of a Manually Locked Counter, The Counter Two Threads Corrupted, AtomicInteger Instead of Manual Synchronization (+1 more)

### Community 40 - "Exercise & ExecutionEngine Base Classes"
Cohesion: 0.33
Nodes (4): ABC, The Exercise data model. Content is data, not code -- see…, Shared execution contract every per-language engine implements. Framing is…, The Explain -> Example -> Try It -> Run -> Result flow for a single exercise.

### Community 43 - "Code Editor UI"
Cohesion: 0.33
Nodes (5): make_code_editor(), make_read_only_code_block(), Control, A plain monospace multiline code editor -- no live syntax highlighting; Flet's…, TextField

### Community 44 - "Spring Execution Engine Tests"
Cohesion: 0.60
Nodes (5): _exercise(), test_compile_error_surfaces_in_stderr(), test_failing_assertion_surfaces_in_stderr(), test_missing_test_definition_fails_cleanly(), test_successful_run()

### Community 45 - "Float Precision Lessons"
Cohesion: 0.50
Nodes (5): Decimal, Floats, Precision, The Price That Rounded the Wrong Way, 0.1 + 0.2 Is Not Quite 0.3

### Community 46 - "Java Time/Duration Lesson"
Cohesion: 0.67
Nodes (3): Duration, java.time, Stdlib Deep Dive: Durations with java.time Instead of Raw Millis

### Community 47 - "Pathlib Lesson"
Cohesion: 0.67
Nodes (3): Filesystem, Pathlib, Paths as Objects, Not Strings

### Community 48 - "Comprehension Lesson"
Cohesion: 0.67
Nodes (3): comprehensions, lists, Lesson: Loop to Comprehension

## Ambiguous Edges - Review These
- `Recursion` → `C++ track category expansion rationale`  [AMBIGUOUS]
  docs/DEVELOPMENT.md · relation: conceptually_related_to
- `/verify slash command` → `test_loads_spring_content()`  [AMBIGUOUS]
  .claude/commands/verify.md · relation: references

## Knowledge Gaps
- **100 isolated node(s):** `run.sh script`, `coding-adventure`, `Achievement: concurrency_async_master`, `Mutex (std::mutex / lock_guard)`, `std::promise / std::future Signaling` (+95 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **22 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Recursion` and `C++ track category expansion rationale`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `/verify slash command` and `test_loads_spring_content()`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **Why does `Gotchas` connect `Cross-Language Idioms & Off-by-One Gotchas` to `Spring AOP & Bean Lifecycle Docs`, `Functional Programming Lessons (Python/C++)`, `Data Structures & Algorithms Lessons`, `Python Collections Lessons`, `C++ Thread Scheduling Lessons`, `C++ String/Stdlib Parsing Lessons`, `Configuration & Deployment Lessons`, `Observability Lessons`, `Dependency Management Lessons`, `Concurrency Coordination Lessons (Threads/Locks/Signals)`, `Recursion: Base Case & Mutual Recursion`, `Float Precision Lessons`, `C++ Sync vs Async Lessons`, `Sync vs Async Lessons (Python)`, `Python Idioms & Aliasing Gotchas`, `C++ Gotcha Gauntlet & Category Ordering`, `Stdlib Deep Dive & Exception Handling Lessons`, `Java equals()/hashCode() Gotchas`?**
  _High betweenness centrality (0.265) - this node is a cross-community bridge._
- **Why does `Threading` connect `Concurrency Coordination Lessons (Threads/Locks/Signals)` to `C++ Thread Scheduling Lessons`, `Race Conditions & Atomics Lessons`, `Recursion: Base Case & Mutual Recursion`, `C++ Sync vs Async Lessons`, `Sync vs Async Lessons (Python)`, `Java Concurrency Lessons`, `Stdlib Deep Dive & Exception Handling Lessons`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **Why does `Functional Programming` connect `Functional Programming Lessons (Python/C++)` to `Data Structures & Algorithms Lessons`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Are the 17 inferred relationships involving `AppState` (e.g. with `Settings` and `ExerciseEngine`) actually correct?**
  _`AppState` has 17 INFERRED edges - model-reasoned connections that need verification._
- **What connects `run.sh script`, `coding-adventure`, `Achievement: concurrency_async_master` to the rest of the system?**
  _100 weakly-connected nodes found - possible documentation gaps or missing edges._