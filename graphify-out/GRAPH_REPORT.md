# Graph Report - coding-adventure  (2026-08-26)

## Corpus Check
- 284 files · ~188,555 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1109 nodes · 1462 edges · 231 communities (94 shown, 137 thin omitted)
- Extraction: 85% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 211 edges (avg confidence: 0.86)
- Token cost: 1,306,002 input · 0 output

## Community Hubs (Navigation)
- Category Metadata & App State
- Error Translation & Lesson Screen
- Progress Store (XP/Streaks/Badges)
- Spring DI Concepts & Docs
- Settings & Platform Data Paths
- Exercise Engine Core Logic
- Language Content Authoring Workflow
- ExecutionEngine Contract & RunHandle
- Android In-Process Python Execution
- Quiz Screen UI
- Per-Language Execution Engines
- Project Overview Docs
- Java Observability Exercises
- Quiz Engine Core Logic
- Project Overview Docs
- Java Sync vs Async Exercises
- Toolchain Auto-Install Scripts
- Node.js Data Structures
- Python Thread Scheduling
- test_python_inprocess_engine.py
- C++ Sync Vs Async
- Validator (engine)
- test_execution_spring.py
- C++ Quiz Bank
- Java Stdlib Deep Dive
- C++ Data Structures
- Watchdog (execution)
- C++ Quiz Bank
- C++ Quiz Bank
- Java Packaging
- C++ Functional Programming
- Java Dependency Management
- Node.js Gotcha Gauntlet
- Node.js Gotcha Gauntlet
- Node.js Quiz Bank
- Python Concurrency Async
- Python Recursion
- Java Idioms Gotchas
- C++ Core Refresher
- C++ Concurrency Async
- C++ Functional Programming
- Java Observability
- Python Dependency Management
- Python Observability
- Project Docs & Rationale
- C++ Quiz Bank
- C++ Gotcha Gauntlet
- Java Core Refresher
- Node.js Core Refresher
- Node.js Data Structures
- Node.js Data Structures
- Node.js Gotcha Gauntlet
- Node.js Idioms Gotchas
- Node.js Idioms Gotchas
- Node.js Idioms Gotchas
- Node.js Idioms Gotchas
- Spring Aop
- build_apk.sh
- Java Data Structures
- Java Deployment
- Java Functional Programming
- Java Gotcha Gauntlet
- Java Idioms Gotchas
- Java Idioms Gotchas
- Java Idioms Gotchas
- Java Observability
- Java Packaging
- Java Recursion
- Node.js Data Structures
- Node.js Data Structures
- Node.js Gotcha Gauntlet
- Node.js Stdlib Deep Dive
- Node.js Stdlib Deep Dive
- Node.js Stdlib Deep Dive
- Python Core Refresher
- Python Data Structures
- Python Data Structures
- Python Data Structures
- Python Observability
- Python Packaging
- Python Packaging
- Project Overview Docs
- C++ Functional Programming
- C++ Gotcha Gauntlet
- Java Stdlib Deep Dive
- Python Gotcha Gauntlet
- Python Sync Vs Async
- Project Overview Docs
- C++ Stdlib Deep Dive
- C++ Sync Vs Async
- Java Data Structures
- Java Dependency Management
- Java Deployment
- Java Deployment
- Java Deployment
- Java Functional Programming
- Java Functional Programming
- Java Functional Programming
- Java Gotcha Gauntlet
- Java Gotcha Gauntlet
- Java Gotcha Gauntlet
- Java Gotcha Gauntlet
- Java Stdlib Deep Dive
- Python Core Refresher
- Python Core Refresher
- Python Core Refresher
- Python Core Refresher
- Python Dependency Management
- Python Dependency Management
- Python Deployment
- Python Deployment
- Python Functional Programming
- Python Functional Programming
- Python Gotcha Gauntlet
- Python Observability
- Python Observability
- Python Packaging
- Python Packaging
- Python Recursion
- Python Stdlib Deep Dive
- Python Stdlib Deep Dive
- Project Docs & Rationale
- Project Docs & Rationale
- Project Docs & Rationale
- ExecutionResult
- ExecutionResult
- RunHandle
- Page
- ExecutionResult
- RunHandle
- AppState
- C++ Gotcha Gauntlet
- C++ Gotcha Gauntlet
- C++ Idioms Gotchas
- C++ Idioms Gotchas
- C++ Idioms Gotchas
- C++ Recursion
- C++ Recursion
- C++ Recursion
- C++ Stdlib Deep Dive
- C++ Stdlib Deep Dive
- Java Quiz Bank
- Java Quiz Bank
- Java Quiz Bank
- Java Quiz Bank
- Java Quiz Bank
- Java Quiz Bank
- Java Quiz Bank
- Java Quiz Bank
- Java Quiz Bank
- Java Quiz Bank
- Java Quiz Bank
- Java Quiz Bank
- Java Quiz Bank
- Java Quiz Bank
- Java Quiz Bank
- Java Quiz Bank
- Java Quiz Bank
- Java Quiz Bank
- Java Quiz Bank
- Java Quiz Bank
- Java Quiz Bank
- Java Quiz Bank
- Java Quiz Bank
- Java Quiz Bank
- Java Quiz Bank
- Java Quiz Bank
- Java Quiz Bank
- Node.js Quiz Bank
- Node.js Quiz Bank
- Node.js Quiz Bank
- Python Deployment
- Python Deployment
- Python Deployment
- Python Functional Programming
- Python Functional Programming
- Python Gotcha Gauntlet
- Python Gotcha Gauntlet
- Python Gotcha Gauntlet
- Python Gotcha Gauntlet
- Python Idioms Gotchas
- Python Idioms Gotchas
- Python Quiz Bank
- Python Quiz Bank
- Python Quiz Bank
- Python Quiz Bank
- Python Quiz Bank
- Python Quiz Bank
- Python Quiz Bank
- Python Quiz Bank
- Python Quiz Bank
- Python Quiz Bank
- Python Quiz Bank
- Python Quiz Bank
- Python Quiz Bank
- Python Quiz Bank
- Python Quiz Bank
- Python Quiz Bank
- Python Quiz Bank
- Python Quiz Bank
- Python Quiz Bank
- Python Quiz Bank
- Python Quiz Bank
- Python Quiz Bank
- Python Quiz Bank
- Python Quiz Bank
- Python Quiz Bank
- Python Quiz Bank
- Python Quiz Bank
- Python Quiz Bank
- Python Quiz Bank
- Python Quiz Bank
- Python Quiz Bank
- Python Quiz Bank
- Spring Quiz Bank
- Control
- ExecutionEngine
- Exercise
- pyproject.toml
- pom.xml
- RunHandle
- View

## God Nodes (most connected - your core abstractions)
1. `AppState` - 37 edges
2. `ExerciseEngine` - 35 edges
3. `RunHandle` - 30 edges
4. `ProgressStore` - 28 edges
5. `ExecutionResult` - 23 edges
6. `_ExerciseController` - 22 edges
7. `C++ Quiz Bank` - 20 edges
8. `ExecutionEngine` - 19 edges
9. `scaled()` - 18 edges
10. `_QuizController` - 16 edges

## Surprising Connections (you probably didn't know these)
- `/verify slash command` --references--> `test_loads_spring_content()`  [AMBIGUOUS]
  .claude/commands/verify.md → tests/test_lesson_engine.py
- `ExecutionEngine ABC` --conceptually_related_to--> `ExecutionEngine`  [EXTRACTED]
  .claude/skills/add-language-content/SKILL.md → app/execution/base.py
- `Toolchain detection (check_toolchain)` --conceptually_related_to--> `check_toolchain()`  [EXTRACTED]
  .claude/skills/add-language-content/SKILL.md → app/execution/toolchain_check.py
- `add-language-content skill` --references--> `LanguageInfo`  [EXTRACTED]
  .claude/skills/add-language-content/SKILL.md → app/engine/languages.py
- `test_cancel_stops_an_in_progress_loop()` --calls--> `RunHandle`  [EXTRACTED]
  tests/test_python_inprocess_engine.py → app/execution/base.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **C++ Concurrency & Async Category Progression** — content_cpp_lessons_concurrency_async_01_race_condition_mutex_exercise, content_cpp_lessons_concurrency_async_02_atomic_counter_exercise, content_cpp_lessons_concurrency_async_03_future_async_exercise, content_cpp_lessons_concurrency_async_04_thread_join_missing_exercise, content_cpp_lessons_concurrency_async_05_promise_future_signal_exercise [INFERRED 0.85]
- **C++ Functional Programming Category Progression** — content_cpp_lessons_functional_programming_01_lambda_capture_by_value_in_loop_exercise, content_cpp_lessons_functional_programming_02_std_function_wrapping_lambda_exercise, content_cpp_lessons_functional_programming_03_std_transform_algorithm_exercise, content_cpp_lessons_functional_programming_04_std_accumulate_with_lambda_exercise, content_cpp_lessons_functional_programming_05_higher_order_function_returning_lambda_exercise [INFERRED 0.85]
- **ExecutionEngine Subclass Implementations** — claude_pythonengine, claude_javaengine, claude_cppengine, claude_nodeengine, claude_springengine [EXTRACTED 1.00]
- **Gotcha Gauntlet Category Progression** — content_cpp_lessons_gotcha_gauntlet_01_off_by_one_array_off_by_one_array_read, content_cpp_lessons_gotcha_gauntlet_02_uncaught_out_of_range_vector_at_out_of_range, content_cpp_lessons_gotcha_gauntlet_03_static_variable_persistence_static_variable_persistence, content_cpp_lessons_gotcha_gauntlet_04_integer_overflow_integer_overflow_wraparound, content_cpp_lessons_gotcha_gauntlet_05_missing_virtual_destructor_missing_virtual_destructor [INFERRED 0.85]
- **Cast-the-Operand-Not-the-Result Principle** — content_cpp_lessons_idioms_gotchas_01_integer_division_truncation_integer_division_truncation, content_cpp_lessons_idioms_gotchas_04_unsigned_underflow_loop_unsigned_underflow_loop, content_cpp_lessons_gotcha_gauntlet_04_integer_overflow_integer_overflow_wraparound [INFERRED 0.90]
- **Recursive Base Case Correctness Cluster** — content_cpp_lessons_recursion_01_missing_base_case_missing_base_case, content_cpp_lessons_recursion_02_off_by_one_base_case_off_by_one_base_case, content_cpp_lessons_recursion_05_mutual_recursion_mutual_recursion [INFERRED 0.80]
- **Busy-Wait Avoidance Techniques in C++ Threading** — content_cpp_lessons_thread_scheduling_01_sleep_for_not_busy_wait_sleepfor, content_cpp_lessons_thread_scheduling_02_this_thread_yield_yield, content_cpp_lessons_thread_scheduling_05_condition_variable_producer_consumer_conditionvariable [INFERRED 0.85]
- **std::async and std::future Pitfalls and Policies** — content_cpp_lessons_sync_vs_async_03_shared_future_multiple_waiters_sharedfuture, content_cpp_lessons_sync_vs_async_05_deferred_launch_runs_on_get_launchdeferred, content_cpp_lessons_thread_scheduling_04_explicit_async_launch_policy_launchasync [INFERRED 0.80]
- **Java Concurrency Toolkit Progression** — content_java_lessons_concurrency_async_01_race_condition_synchronized_synchronized, content_java_lessons_concurrency_async_02_atomic_integer_atomicinteger, content_java_lessons_concurrency_async_03_executor_service_executorservice [INFERRED 0.75]
- **Numeric Version Comparison and Coordinate Parsing** — content_java_lessons_dependency_management_01_version_string_comparison_exercise, content_java_lessons_dependency_management_04_minimum_version_check_exercise, content_java_lessons_dependency_management_05_maven_coordinate_parsing_exercise [INFERRED 0.80]
- **Defensive Deployment Configuration Patterns** — content_java_lessons_deployment_01_env_var_defaults_exercise, content_java_lessons_deployment_02_case_insensitive_boolean_parsing_exercise, content_java_lessons_deployment_04_health_check_exercise, content_java_lessons_deployment_05_idempotent_deploy_step_exercise [INFERRED 0.75]
- **Gotcha Gauntlet Puzzle Set** — content_java_lessons_gotcha_gauntlet_01_off_by_one_loop_exercise, content_java_lessons_gotcha_gauntlet_02_switch_fallthrough_exercise, content_java_lessons_gotcha_gauntlet_03_concurrent_modification_exercise, content_java_lessons_gotcha_gauntlet_04_integer_overflow_exercise, content_java_lessons_gotcha_gauntlet_05_equals_hashcode_contract_exercise [INFERRED 0.85]
- **Empty-Body / No-Op Stub Implementation Antipattern** — content_java_lessons_packaging_04_service_registry_stub_method_no_op_bug, content_java_lessons_observability_04_metrics_counter_stub_method_no_op_bug, content_java_lessons_observability_05_timing_instrumentation_stub_method_no_op_bug [INFERRED 0.80]
- **Configured Logging -> Level Filtering -> Correlation ID Pipeline** — content_java_lessons_observability_01_structured_logging_logger_handler_configuration, content_java_lessons_observability_02_log_level_filtering_two_stage_log_filtering, content_java_lessons_observability_03_correlation_id_threadlocal_threadlocal [INFERRED 0.75]
- **Recursive Base-Case / Recursive-Case Correctness Failures** — content_java_lessons_recursion_01_missing_base_case_missing_base_case, content_java_lessons_recursion_03_mutual_recursion_wrong_base_case_value, content_java_lessons_recursion_04_recursive_tree_sum_missing_recursive_case [INFERRED 0.75]
- **CompletableFuture Async Pipeline Pattern** — content_java_lessons_sync_vs_async_01_completablefuture_chaining_thenapply, content_java_lessons_sync_vs_async_02_completablefuture_combine_thencombine, content_java_lessons_sync_vs_async_03_completablefuture_exceptionally_exceptionally, content_java_lessons_sync_vs_async_04_supplyasync_custom_executor_supplyasyncexecutor, content_java_lessons_sync_vs_async_05_virtual_threads_virtualthreads [INFERRED 0.80]
- **Node Promise and async/await Concurrency Curriculum** — content_node_lessons_concurrency_async_01_callback_to_async_await_asyncawait, content_node_lessons_concurrency_async_02_reading_before_resolved_awaittiming, content_node_lessons_concurrency_async_03_promise_all_vs_allsettled_allsettled, content_node_lessons_concurrency_async_04_sequential_await_loop_promiseallparallel, content_node_lessons_concurrency_async_05_unhandled_rejection_trycatchawait [INFERRED 0.80]
- **Blocking-Until-Ready Pattern Across Concurrency Models** — content_java_lessons_thread_scheduling_04_blocking_queue_blockingqueue, content_node_lessons_concurrency_async_02_reading_before_resolved_awaittiming, content_java_lessons_sync_vs_async_01_completablefuture_chaining_thenapply [INFERRED 0.75]
- **Concurrent Execution With Preserved/Trade-off Ordering (gather vs Promise.all)** — content_python_lessons_concurrency_async_01_gather_order_asyncio_gather_input_order, content_python_lessons_concurrency_async_01_gather_order_sequential_await_loop_trap, content_node_quiz_quiz_questions_q28, content_node_quiz_quiz_questions_q29 [INFERRED 0.85]
- **NaN Self-Inequality Detection Pattern** — content_node_lessons_gotcha_gauntlet_02_nan_self_comparison_exercise, content_node_lessons_gotcha_gauntlet_02_nan_self_comparison_number_isnan, content_node_quiz_quiz_questions_q30 [INFERRED 0.95]
- **In-Place Array Mutation Pitfalls (forEach/splice and sort)** — content_node_lessons_gotcha_gauntlet_01_foreach_splice_skip_exercise, content_node_lessons_gotcha_gauntlet_04_sort_mutates_in_place_exercise, content_node_quiz_quiz_questions_q31, content_node_quiz_quiz_questions_q32 [INFERRED 0.85]
- **Lock-based race-condition protection and timeout bounding** — content_python_lessons_concurrency_async_02_thread_lock_lesson, content_python_lessons_concurrency_async_04_asyncio_lock_lesson, content_python_lessons_concurrency_async_05_wait_for_timeout_lesson [INFERRED 0.75]
- **End-to-end dependency management curriculum arc** — content_python_lessons_dependency_management_01_detect_virtualenv_lesson, content_python_lessons_dependency_management_02_parse_requirement_line_lesson, content_python_lessons_dependency_management_03_version_string_comparison_lesson, content_python_lessons_dependency_management_04_importlib_metadata_lesson, content_python_lessons_dependency_management_05_lock_file_pin_lesson [INFERRED 0.80]
- **collections-module alternatives to manual dict/list bookkeeping** — content_python_lessons_data_structures_01_defaultdict_lesson, content_python_lessons_data_structures_02_counter_lesson, content_python_lessons_data_structures_03_deque_lesson [INFERRED 0.75]
- **Functional Programming Lesson Sequence** — content_python_lessons_functional_programming_01_pure_functions_pure_functions, content_python_lessons_functional_programming_02_map_filter_map_filter_pipeline, content_python_lessons_functional_programming_03_function_composition_function_composition, content_python_lessons_functional_programming_04_immutability_immutable_namedtuple, content_python_lessons_functional_programming_05_partial_application_functools_partial [INFERRED 0.80]
- **Gotcha Gauntlet Lesson Sequence** — content_python_lessons_gotcha_gauntlet_01_off_by_one_slice_negative_slice_off_by_one, content_python_lessons_gotcha_gauntlet_02_exception_swallowing_bare_except_swallowing, content_python_lessons_gotcha_gauntlet_03_mutable_class_attribute_shared_class_attribute, content_python_lessons_gotcha_gauntlet_04_rounding_precision_decimal_rounding, content_python_lessons_gotcha_gauntlet_05_dict_mutation_during_iteration_dict_mutation_during_iteration, content_python_lessons_gotcha_gauntlet_06_missing_super_init_missing_super_init_call [INFERRED 0.80]
- **Idioms and Gotchas Lesson Sequence** — content_python_lessons_idioms_gotchas_01_mutable_default_arg_mutable_default_argument, content_python_lessons_idioms_gotchas_02_late_binding_closure_late_binding_closure, content_python_lessons_idioms_gotchas_03_is_vs_equals_identity_vs_equality, content_python_lessons_idioms_gotchas_04_float_precision_float_precision_isclose, content_python_lessons_idioms_gotchas_05_aliasing_vs_copying_aliasing_vs_copying, content_python_lessons_idioms_gotchas_06_sort_returns_none_sort_returns_none [INFERRED 0.80]
- **Recursive Base-Case Bug Family** — content_python_lessons_recursion_01_missing_base_case_lesson, content_python_lessons_recursion_02_recursion_depth_limit_lesson, content_python_lessons_recursion_03_mutual_recursion_lesson [INFERRED 0.75]
- **Standardized Packaging Metadata Parsing** — content_python_lessons_packaging_01_tomllib_parse_version_lesson, content_python_lessons_packaging_03_entry_point_registry_lesson, content_python_lessons_packaging_05_wheel_filename_parsing_lesson [INFERRED 0.70]
- **Core Observability Primitives** — content_python_lessons_observability_02_log_level_filtering_lesson, content_python_lessons_observability_03_correlation_id_contextvar_lesson, content_python_lessons_observability_04_metrics_counter_lesson, content_python_lessons_observability_05_timing_context_manager_lesson [INFERRED 0.75]
- **Spring AOP Advice Types Progression** — content_spring_lessons_aop_01_missing_aspect_annotation_exercise, content_spring_lessons_aop_02_pointcut_expression_wrong_method_exercise, content_spring_lessons_aop_03_afterreturning_captures_result_exercise, content_spring_lessons_aop_04_around_advice_modifying_result_exercise, content_spring_lessons_aop_05_self_invocation_bypasses_proxy_exercise [INFERRED 0.85]
- **Python Thread Coordination and Identity Primitives** — content_python_lessons_thread_scheduling_01_reentrant_lock_exercise, content_python_lessons_thread_scheduling_02_thread_naming_exercise, content_python_lessons_thread_scheduling_03_daemon_flag_exercise, content_python_lessons_thread_scheduling_04_producer_consumer_queue_exercise, content_python_lessons_thread_scheduling_05_thread_local_storage_exercise [INFERRED 0.75]
- **Spring Bean Lifecycle Hooks Progression** — content_spring_lessons_bean_lifecycle_01_missing_component_annotation_exercise, content_spring_lessons_bean_lifecycle_02_singleton_shared_state_exercise, content_spring_lessons_bean_lifecycle_03_postconstruct_initialization_exercise, content_spring_lessons_bean_lifecycle_04_predestroy_cleanup_exercise, content_spring_lessons_bean_lifecycle_05_lazy_initialization_exercise [INFERRED 0.85]
- **Resilience4j Decorator Pattern Group** — content_spring_lessons_resilience_01_circuit_breaker_opens_after_failures_exercise, content_spring_lessons_resilience_02_retry_until_success_exercise, content_spring_lessons_resilience_03_rate_limiter_rejects_excess_calls_exercise, content_spring_lessons_resilience_04_fallback_on_failure_exercise, content_spring_lessons_resilience_05_circuit_breaker_before_retry_exercise [INFERRED 0.85]
- **Dependency Injection: Constructor vs. Field Injection Pattern Group** — content_spring_lessons_dependency_injection_01_field_injection_untestable_exercise, content_spring_lessons_dependency_injection_02_ambiguous_bean_no_qualifier_exercise, content_spring_lessons_dependency_injection_03_primary_bean_exercise, content_spring_lessons_dependency_injection_04_optional_dependency_exercise, content_spring_lessons_dependency_injection_05_constructor_injection_final_fields_exercise [INFERRED 0.80]
- **Spring Application Event Publish/Listen Mechanism Group** — content_spring_lessons_events_01_publish_forgotten_exercise, content_spring_lessons_events_02_missing_eventlistener_annotation_exercise, content_spring_lessons_events_03_multiple_listeners_fan_out_exercise, content_spring_lessons_events_04_conditional_event_listener_exercise, content_spring_lessons_events_05_custom_event_payload_exercise [INFERRED 0.80]
- **Language content verification workflow** — _claude_commands_verify_command, _claude_skills_add_language_content_skill_skill, concept_real_toolchain_verification [INFERRED 0.80]

## Communities (231 total, 137 thin omitted)

### Community 0 - "Category Metadata & App State"
Cohesion: 0.06
Nodes (58): CategoryMeta, get_category_meta(), Display metadata (title, icon, color) for exercise categories, used by the…, get_language(), LanguageInfo, The set of language tracks the app knows about, and which ones have real…, AppState, Shared app state: settings, progress store, per-language exercise/quiz engines… (+50 more)

### Community 1 - "Error Translation & Lesson Screen"
Cohesion: 0.09
Nodes (21): extract_error_line_number(), _last_exception_type(), Translates raw interpreter/compiler output into concise, professional…, _translate_cpp_error(), translate_error(), _translate_java_error(), _translate_node_error(), _translate_spring_error() (+13 more)

### Community 2 - "Progress Store (XP/Streaks/Badges)"
Cohesion: 0.08
Nodes (13): _level_from_xp(), _now(), PlayerLevel, ProgressStore, Path, SQLite-backed progress, gamification, and activity tracking -- one…, Returns True if newly awarded, False if already had it., Resets to 0 automatically once the exercise is passed -- powers the "keep… (+5 more)

### Community 3 - "Spring DI Concepts & Docs"
Cohesion: 0.07
Nodes (39): The Config Value That Must Not Have a Default, The Bean That Couldn't Be Unit Tested, Two Beans, One Interface, No Way to Choose, Picking a Default Among Equals, The Dependency That Might Not Exist, Every Dependency, Explicit and Immutable, The Event Nobody Published, The Listener That Never Registered (+31 more)

### Community 4 - "Settings & Platform Data Paths"
Cohesion: 0.10
Nodes (28): Path, Resolves the writable directory this app's data lives in. On desktop/web this…, Returns FLET_APP_STORAGE_DATA when set (packaged builds, e.g. Android),…, resolve_platform_data_dir(), get_data_dir(), get_db_path(), get_settings_path(), is_first_run() (+20 more)

### Community 5 - "Exercise Engine Core Logic"
Cohesion: 0.12
Nodes (20): ExerciseEngine, Exercise, Path, A small guided set for "today's refresher" -- round-robins the next unlocked,…, category -> (done, total), done computed by the caller passing completed_ids in…, test_categories_derived_from_content(), test_category_level_1_always_unlocked(), test_daily_refresher_spans_categories() (+12 more)

### Community 6 - "Language Content Authoring Workflow"
Cohesion: 0.10
Nodes (26): /verify slash command, add-language-content skill, CATEGORY_META dict (code), Loads one language track's exercises from YAML, kept separate from application…, is_android(), Detects whether this process is running on Android. `sys.getandroidapilevel` is…, check_toolchain(), get_install_guide() (+18 more)

### Community 7 - "ExecutionEngine Contract & RunHandle"
Cohesion: 0.15
Nodes (12): ExecutionResult, Lets the UI cancel a run that's in progress (e.g. an infinite loop). Every…, exercise is unused by the single-file engines (Python/Java/C++) -- SpringEngine…, RunHandle, CppEngine, _describe_crash(), C++ execution engine: compiles the submitted code with `g++`, then runs the…, _detect_class_name() (+4 more)

### Community 8 - "Android In-Process Python Execution"
Cohesion: 0.15
Nodes (14): _make_input(), PythonInProcessEngine, In-process Python execution engine, used specifically on Android in place of…, Mirrors how a real stdin pipe behaves: a trailing newline marks the end of the…, Same ExecutionResult/RunHandle contract as PythonEngine, but runs code in-…, _split_stdin(), compile_with_watchdog(), Cooperative timeout mechanism for PythonInProcessEngine (Android). A… (+6 more)

### Community 9 - "Quiz Screen UI"
Cohesion: 0.20
Nodes (6): build_quiz_view(), Control, Page, View, _QuizController, Button

### Community 10 - "Per-Language Execution Engines"
Cohesion: 0.19
Nodes (13): ABC, ExecutionEngine, Shared execution contract every per-language engine implements. Framing is…, One concrete subclass per language track (python_engine.PythonEngine,…, NodeEngine, Node.js execution engine: runs submitted JavaScript with `node`, no separate…, get_engine(), Maps a language key to its ExecutionEngine instance. (+5 more)

### Community 11 - "Project Overview Docs"
Cohesion: 0.17
Nodes (16): app_window.py route dispatcher, AppState, categories.py CATEGORY_META, CppEngine (cpp_engine.py), errors.py translate_error(), ExecutionEngine ABC, Exercise dataclass, ExerciseEngine (+8 more)

### Community 12 - "Java Observability Exercises"
Cohesion: 0.13
Nodes (16): A Minimal Metrics Counter, Map.merge Increment Idiom, Empty-Body increment() Stub Bug, AutoCloseable + try-with-resources Timing, Instrumenting a Block's Duration, Empty close() Stub Bug, Validating a Package Name Convention, Java Package Naming Convention (+8 more)

### Community 13 - "Quiz Engine Core Logic"
Cohesion: 0.21
Nodes (7): Path, QuizEngine, Loads a language track's quiz questions from YAML. Adding a question means…, A freshly randomized set of questions for one quiz playthrough -- which…, QuizQuestion, The QuizQuestion data model. Quiz content is data, not code -- see…, Collection

### Community 14 - "Project Overview Docs"
Cohesion: 0.16
Nodes (15): Coding Adventure Architecture Overview, std::atomic lock-free operations, std::mutex + std::lock_guard, Race Condition (unsynchronized shared counter), RAII (Resource Acquisition Is Initialization), std::unique_ptr smart pointer, The Counter Two Threads Corrupted (mutex/lock_guard), std::atomic Instead of a Manually Locked Counter (+7 more)

### Community 15 - "Java Sync vs Async Exercises"
Cohesion: 0.18
Nodes (15): CompletableFuture.thenApply Chaining, CompletableFuture.thenCombine, CompletableFuture.exceptionally Recovery, supplyAsync with Custom ExecutorService, Virtual Threads vs Fixed Platform-Thread Pool, Naming Threads for Debuggable Logs, Marking a Background Thread as Daemon, Thread Scheduling Priority as a Hint (+7 more)

### Community 16 - "Toolchain Auto-Install Scripts"
Cohesion: 0.19
Nodes (8): is_python_process(), run_app_web_ui.sh script, run_app_window_mode.sh script, _confirm(), ensure_cpp(), ensure_java(), ensure_toolchains.sh script, _windows_path_add()

### Community 17 - "Node.js Data Structures"
Cohesion: 0.23
Nodes (14): filter/map/reduce Pipeline, Array.filter(), Array.map(), Array.reduce(), forEach + splice Silent Skip, filter() Rebuild Instead of Mutate, forEach/splice Mutation-During-Iteration, Transforming Values with entries/fromEntries (+6 more)

### Community 18 - "Python Thread Scheduling"
Cohesion: 0.15
Nodes (14): The Lock That Locked Itself Out, Naming Threads for Debuggable Logs, Marking a Background Thread as Daemon, A Producer/Consumer Handoff with queue.Queue, Per-Thread State with threading.local(), The Class Spring Never Knew About, The 'Two' Instances That Were Actually One, Initializing Before Your Dependencies Arrive (+6 more)

### Community 21 - "C++ Sync Vs Async"
Cohesion: 0.22
Nodes (13): Shared Future for Multiple Waiters, Synchronous Wrapper Over Async API, Deferred Launch Runs On get(), sleep_for Instead of Busy-Wait, this_thread::yield in a Spin Loop, Joining All Threads in a Vector, Explicit std::launch::async Policy, Condition Variable Producer/Consumer (+5 more)

### Community 22 - "Validator (engine)"
Cohesion: 0.27
Nodes (10): Exercise validation: checks behavior/output, not exact code formatting., True if `code` contains every required pattern. Each pattern is matched as a…, Compares output, optionally substituting what the user typed into a template. -…, validate_contains(), validate_output(), test_validate_contains_empty_patterns_always_true(), test_validate_contains_requires_all_patterns(), test_validate_output_exact_match() (+2 more)

### Community 23 - "test_execution_spring.py"
Cohesion: 0.31
Nodes (8): Exercise, The Exercise data model. Content is data, not code -- see…, Runs submitted Python code: a fast local syntax pre-check, then an isolated…, _exercise(), test_compile_error_surfaces_in_stderr(), test_failing_assertion_surfaces_in_stderr(), test_missing_test_definition_fails_cleanly(), test_successful_run()

### Community 24 - "C++ Quiz Bank"
Cohesion: 0.18
Nodes (11): Quiz q36: Busy-Wait vs sleep_for, Quiz q37: this_thread::yield in a Spin Loop, Quiz q38: Joining Every Thread in a Vector, Quiz q39: Default std::async Launch Policy, Quiz q40: condition_variable vs Busy-Wait Polling, Quiz q41: future::get() Called Twice, Quiz q42: Exceptions Inside an Async Task, Quiz q43: Why a Plain future Can't Be Read Twice (+3 more)

### Community 25 - "Java Stdlib Deep Dive"
Cohesion: 0.25
Nodes (11): The Countdown That Never Stopped, Missing Base Case, StackOverflowError, Recursion-to-Iteration Conversion, JVM Has No Tail-Call Optimization, Hitting the Stack Limit, Building a String in a Loop, O(n^2) String Concatenation Bug (+3 more)

### Community 26 - "C++ Data Structures"
Cohesion: 0.20
Nodes (10): std::deque (O(1) front/back ops), std::priority_queue (heap), std::set (uniqueness by construction), std::sort (introsort), std::unordered_map (hash table O(1) lookup), Manual Bubble Sort to std::sort, Linear Search to unordered_map Lookup, O(1) Front Removal with deque (+2 more)

### Community 27 - "Watchdog (execution)"
Cohesion: 0.28
Nodes (6): _LoopTickInjector, Inserts a call to __codingadventure_tick__() as the first statement in every…, AST, Expr, For, While

### Community 28 - "C++ Quiz Bank"
Cohesion: 0.28
Nodes (9): Mutual Recursion, Quiz q55: What Mutual Recursion Is, Mutual Recursion with a Wrong Base Case, Wrong Base Case Value, What is mutual recursion?, Recursive Base Case, The Countdown That Never Stopped, Mutual Recursion with a Wrong Base Case (+1 more)

### Community 29 - "C++ Quiz Bank"
Cohesion: 0.22
Nodes (9): Recursion, Tail Recursion, Quiz q51: Recursion With No Base Case, Quiz q52: Exact-Equality Base Case vs Range Check, Quiz q54: What Makes a Recursive Call a Tail Call, What happens to a recursive function with no base case?, Does Python optimize tail-recursive calls?, Why does flattening a nested list need recursion? (+1 more)

### Community 30 - "Java Packaging"
Cohesion: 0.28
Nodes (9): Cascading Reset Rule, Bumping a Semantic Version, Semantic Versioning (major.minor.patch), Unchanged-Passthrough Stub Bug, artifact-version.jar Filename Convention, lastIndexOf Boundary Parsing, Parsing a JAR Filename, Unparsed-Passthrough Stub Bug (+1 more)

### Community 31 - "C++ Functional Programming"
Cohesion: 0.32
Nodes (8): Closures / higher-order functions (function factories), Lambda expressions (vs. functor structs), std::function type erasure, Functor Struct to Lambda, The Function Pointer That Couldn't Hold a Lambda, A Function Factory, Not Just a Function, Quiz q47: Capturing Lambda vs Function Pointer, Quiz q50: Closure Factory Returning std::function

### Community 32 - "Java Dependency Management"
Cohesion: 0.25
Nodes (8): Comparing Version Numbers as Strings, Numeric Part-by-Part Version Comparison, The Classpath Conflict That Picked the Older Version, Compare-Before-Overwrite Classpath Resolution, Does This Version Satisfy the Minimum?, Minimum-Version Satisfaction Check, Parsing a Maven Coordinate, groupId:artifactId:version Coordinate Parsing

### Community 33 - "Node.js Gotcha Gauntlet"
Cohesion: 0.39
Nodes (8): sort() Mutates the Original Array, Array.sort() In-Place Mutation, Spread-Copy Before Sort, Array.sort()'s String-First Default, sort() Lexicographic Default, Numeric Comparator (a,b)=>a-b, Quiz: What does Array.prototype.sort() do with no comparator?, Quiz: Why does Array.prototype.sort() surprise callers?

### Community 34 - "Node.js Gotcha Gauntlet"
Cohesion: 0.39
Nodes (8): Reference Equality on Identical-Looking Arrays, JSON.stringify Structural Compare, === Reference Equality on Objects/Arrays, Copy-Then-Delete Field Removal, Redacting a Field with JSON.stringify's Replacer, JSON.stringify Replacer Function, Quiz: Why does JSON.stringify's replacer work for redaction?, Quiz: Why is [1,2,3] === [1,2,3] false?

### Community 35 - "Node.js Quiz Bank"
Cohesion: 0.32
Nodes (8): Quiz: Why doesn't async function throw synchronously?, Quiz: setTimeout vs Promise.then ordering?, Quiz: Why does Promise.all reject entirely on one rejection?, Quiz: Why is sequential await-in-a-loop slower than necessary?, asyncio.as_completed Completion Order, asyncio.gather Concurrent + Input-Order Results, asyncio.gather Preserves Input Order, Sequential await-in-loop Trap

### Community 36 - "Python Concurrency Async"
Cohesion: 0.25
Nodes (8): Protecting a Shared Counter with a Lock, threading.Lock critical-section pattern, Running I/O-Bound Work Concurrently, ThreadPoolExecutor concurrent map/submit, asyncio.Lock read-await-write protection, The Async Equivalent of a Race Condition, asyncio.wait_for deadline pattern, Bounding How Long You'll Wait

### Community 37 - "Python Recursion"
Cohesion: 0.25
Nodes (8): Hitting Python's Recursion Limit, Python Recursion Limit / No Tail-Call Optimization, Accumulator Pattern, Reversing a List with an Accumulator, Memoizing a Recursive Function, functools.lru_cache Memoization, Folding a List Into One Value, functools.reduce

### Community 38 - "Java Idioms Gotchas"
Cohesion: 0.38
Nodes (7): Autoboxing, JVM Integer Cache (-128..127), Autoboxed Integer Comparison, Reference Equality vs .equals(), Null-Safe Comparison with Objects.equals, Null-Safe Equality Checking, java.util.Objects.equals

### Community 40 - "C++ Core Refresher"
Cohesion: 0.33
Nodes (6): auto type deduction, Range-based for loop, Structured bindings (C++17), Index Loop to Range-Based For, Spelling Out a Type auto Could Deduce, Iterator Members to Structured Bindings

### Community 41 - "C++ Concurrency Async"
Cohesion: 0.40
Nodes (6): std::promise/std::future one-shot channel, std::async / std::future asynchronous computation, std::thread join()/detach() joinability, Running a Computation Asynchronously (std::async/future), The Thread That Was Never Joined, Signaling a Result with promise/future

### Community 42 - "C++ Functional Programming"
Cohesion: 0.33
Nodes (6): std::accumulate (fold/reduce operation), std::transform (map operation), Manual Mapping to std::transform, Manual Folding to std::accumulate, Quiz q48: What std::transform Does, Quiz q49: std::accumulate with a Custom Lambda

### Community 43 - "Java Observability"
Cohesion: 0.33
Nodes (6): Bypassing Logging Infrastructure with println, java.util.logging, Using the Logger That's Already Configured, Logger/Handler/Formatter Configuration, The Log Level Set Too High, Two-Stage Log Level Filtering (Logger + Handler)

### Community 44 - "Python Dependency Management"
Cohesion: 0.33
Nodes (6): Parsing a requirements.txt Pin, str.partition requirement-line parsing, Comparing Version Numbers as Strings, Integer-tuple version comparison, Exact-pin lock-file reproducibility, Why an Exact Pin Guarantees Reproducibility

### Community 45 - "Python Observability"
Cohesion: 0.33
Nodes (6): contextvars.ContextVar, Threading a Correlation ID Through Log Lines, Cooperative Event Loop Yielding, The Blocking Call That Froze the Event Loop, Running Blocking I/O Without Blocking the Loop, asyncio.to_thread

### Community 46 - "Project Docs & Rationale"
Cohesion: 0.33
Nodes (6): Crash-Containment, Not a Safety Sandbox, Derived State Over Stored State, Per-Language Progress Isolation via Column, System Context (Offline, Single-User), flet dependency, pyyaml dependency

### Community 48 - "C++ Quiz Bank"
Cohesion: 0.60
Nodes (5): Memoization, Quiz q53: Memoization in Recursive Fibonacci, HashMap Cache Pattern, Memoizing a Recursive Method by Hand, What's Java's equivalent of Python's @lru_cache decorator?

### Community 49 - "C++ Gotcha Gauntlet"
Cohesion: 0.40
Nodes (5): Off-By-One Array Read (i <= size), Uncaught std::out_of_range from vector::at(), Recursion Missing a Base Case, Base Case That Only Matches Exact Equality, std::stoi Throwing std::invalid_argument

### Community 50 - "Java Core Refresher"
Cohesion: 0.40
Nodes (5): Anonymous Class to Lambda Expression, Filter and Transform with Streams, Optional Instead of Manual Null Check, Boilerplate Class to record, Manual close() to try-with-resources

### Community 51 - "Node.js Core Refresher"
Cohesion: 0.40
Nodes (5): Array Destructuring with Rest, Merging Objects with Spread, String Concatenation to Template Literal, Manual Fallback to a Default Parameter, Optional Chaining and Nullish Coalescing

### Community 52 - "Node.js Data Structures"
Cohesion: 0.80
Nodes (5): Plain Object Prototype Key Collision, Map (JS), Plain Object as Hash Map, Prototype Property Collision, Quiz: Why is a plain object risky as a string-keyed map?

### Community 53 - "Node.js Data Structures"
Cohesion: 0.60
Nodes (5): Per-Level Destructuring Defaults, Nested Destructuring with Defaults, Nested Destructuring Pattern, Quiz: What does array rest destructuring do?, Quiz: What is the outer = {} in nested destructuring for?

### Community 54 - "Node.js Gotcha Gauntlet"
Cohesion: 0.60
Nodes (5): Default Param Referencing Shared Object, Default Parameter Pointing at Shared Array, Array-Literal Default Allocates Fresh, Python Mutable Default Argument Trap (referenced), Quiz: When does a default parameter value get used?

### Community 55 - "Node.js Idioms Gotchas"
Cohesion: 0.70
Nodes (5): Loose Equality's Coercion Trap, == Type Coercion, === Strict Equality, Quiz: Why does 0 == "0" evaluate to true?, Quiz: What does null == undefined evaluate to?

### Community 56 - "Node.js Idioms Gotchas"
Cohesion: 0.70
Nodes (5): var's Shared Loop Variable, let Per-Iteration Binding, var Function-Scoping, Quiz: Why do var closures share the final loop value?, Quiz: What does let do differently in a for-loop?

### Community 57 - "Node.js Idioms Gotchas"
Cohesion: 0.70
Nodes (5): Comparing Floats Without Epsilon, IEEE-754 Float Precision, Number.EPSILON Tolerance Compare, Quiz: Why does 0.1 + 0.2 === 0.3 evaluate to false?, Quiz: Standard idiom for comparing floats?

### Community 58 - "Node.js Idioms Gotchas"
Cohesion: 0.70
Nodes (5): A Detached Method Loses this, Function.prototype.bind(), Detached Method Loses this, Quiz: Why does a detached class method misbehave?, Quiz: What does Function.prototype.bind(obj) do?

### Community 59 - "Spring Aop"
Cohesion: 0.60
Nodes (5): The Advice That Was Never An Aspect, The Pointcut Watching the Wrong Method, The Advice That Couldn't See the Answer, The Advice That Could Change the Answer, The Call That Skipped Its Own Proxy

### Community 61 - "Java Data Structures"
Cohesion: 0.67
Nodes (4): HashMap's Unreliable Iteration Order, O(1) Queue Operations with ArrayDeque, Sorting by Custom Field with Comparator, Keys That Sort Themselves with TreeMap

### Community 62 - "Java Deployment"
Cohesion: 0.50
Nodes (4): Configuration with a Safe Default, System.getenv().getOrDefault Fallback Pattern, equalsIgnoreCase for Config Booleans, The Feature Flag That Only Worked in Lowercase

### Community 63 - "Java Functional Programming"
Cohesion: 0.50
Nodes (4): Lambda to Method Reference, Method Reference Forms (unbound/static/bound), Function.andThen/compose Composition, Composing Functions with andThen

### Community 64 - "Java Gotcha Gauntlet"
Cohesion: 0.50
Nodes (4): equals()/hashCode() Contract, equals() Without hashCode(): The Broken Contract, == vs .equals() for Strings, String Reference Identity vs Content Equality

### Community 65 - "Java Idioms Gotchas"
Cohesion: 0.67
Nodes (4): finally Block Semantics, The finally Block That Ate the Return, Return-in-finally Antipattern, try-with-resources

### Community 66 - "Java Idioms Gotchas"
Cohesion: 0.67
Nodes (4): Array Default Values, The Array Slot That Was Never Set, NullPointerException, Object vs Primitive Array Defaults

### Community 67 - "Java Idioms Gotchas"
Cohesion: 0.67
Nodes (4): Instance Fields, The Counter Every Instance Shared, Shared Mutable State Bug, Static Fields

### Community 68 - "Java Observability"
Cohesion: 0.83
Nodes (4): Threading a Correlation ID Through Log Lines, MDC (Mapped Diagnostic Context), Per-Thread Isolation, ThreadLocal

### Community 69 - "Java Packaging"
Cohesion: 0.50
Nodes (4): JAR MANIFEST.MF Format, Reading Main-Class Out of a Manifest, Nested String.split Parsing, What does a JAR manifest's Main-Class entry specify?

### Community 70 - "Java Recursion"
Cohesion: 0.67
Nodes (4): Binary Tree Recursion, Summing an Unbalanced Tree, Missing Recursive Case (Ignoring Children), How do you correctly sum every value in a binary tree recursively?

### Community 71 - "Node.js Data Structures"
Cohesion: 0.83
Nodes (4): Set Dedup vs includes() Loop, Manual includes() Dedup Loop, Set (JS), Quiz: What does [...new Set(arr)] accomplish?

### Community 72 - "Node.js Data Structures"
Cohesion: 0.83
Nodes (4): Spread Shallow Copy vs structuredClone, Object Spread Shallow Copy, structuredClone(), Quiz: Why does mutating a spread-copied nested prop affect original?

### Community 73 - "Node.js Gotcha Gauntlet"
Cohesion: 0.83
Nodes (4): NaN Never Equals Itself, NaN Self-Inequality (IEEE-754), Number.isNaN(), Quiz: Why does NaN === NaN evaluate to false?

### Community 74 - "Node.js Stdlib Deep Dive"
Cohesion: 0.83
Nodes (4): Array.isArray(), typeof Can't Tell Array from Object, typeof 'object' Ambiguity, Quiz: Why can't typeof distinguish array from object?

### Community 75 - "Node.js Stdlib Deep Dive"
Cohesion: 0.83
Nodes (4): Array.prototype.flat(), Flattening a Nested Array with flat(), Manual isArray + Inner Loop Flatten, Quiz: What does [1,[2,3],[4],5].flat() return?

### Community 76 - "Node.js Stdlib Deep Dive"
Cohesion: 0.83
Nodes (4): Array.from({length},mapper), Generating a Range with Array.from, Manual Push-Loop Accumulator, Quiz: What does Array.from({length:5},(_, i)=>i*i) produce?

### Community 77 - "Python Core Refresher"
Cohesion: 0.50
Nodes (4): *args / **kwargs variable arity, Accepting Any Number of Arguments, Decorator function-wrapping pattern, Wrapping a Function with a Decorator

### Community 78 - "Python Data Structures"
Cohesion: 0.50
Nodes (4): collections.defaultdict factory-on-miss, Grouping Without Manual Key Checks, collections.Counter tallying, Tallying with Counter

### Community 79 - "Python Data Structures"
Cohesion: 0.50
Nodes (4): collections.deque O(1) double-ended ops, O(1) Queue Operations with deque, Finding Overlap with Set Operations, Set intersection/union O(1) membership

### Community 80 - "Python Data Structures"
Cohesion: 0.50
Nodes (4): heapq.nsmallest/nlargest partial selection, The k Smallest Items Without a Full Sort, bisect.insort binary-search insertion, Inserting Into a Sorted List Without Re-Sorting

### Community 81 - "Python Observability"
Cohesion: 0.50
Nodes (4): Instrumenting a Block's Duration, Timer Context Manager, contextlib.suppress, Suppressing an Expected Exception Cleanly

### Community 82 - "Python Packaging"
Cohesion: 0.50
Nodes (4): Reading a Version Out of pyproject.toml, tomllib Module, Packaging Entry Points, Building a Plugin Registry with a Decorator

### Community 83 - "Python Packaging"
Cohesion: 0.50
Nodes (4): __all__ Public API Declaration, Controlling a Package's Public API with __all__, Adding Type Hints for Clarity and Tooling, Type Hints (PEP 484)

### Community 84 - "Project Overview Docs"
Cohesion: 0.67
Nodes (3): android_platform.py (is_android), python_inprocess_engine.py, watchdog.py (AST loop-tick injector)

### Community 85 - "C++ Functional Programming"
Cohesion: 0.67
Nodes (3): Lambda capture-by-value vs. capture-by-reference, The Lambdas That All Remembered the Same Number, Quiz q46: Capturing a Loop Variable by Reference

### Community 86 - "C++ Gotcha Gauntlet"
Cohesion: 0.67
Nodes (3): Signed Integer Overflow Wraparound, Integer Division Truncation, Unsigned Integer Underflow in a Countdown Loop

### Community 87 - "Java Stdlib Deep Dive"
Cohesion: 1.00
Nodes (3): Format Placeholder Options (%d, %.2f, %-10s), Structured Output with String.format, String.format Templating

### Community 88 - "Python Gotcha Gauntlet"
Cohesion: 0.67
Nodes (3): Mutable Class Attribute Shared Across Instances, Mutable Default Argument Trap, Late-Binding Closures in Loops

### Community 89 - "Python Sync Vs Async"
Cohesion: 0.67
Nodes (3): Calling an Async Function Without Awaiting It, The Async Analog of a Context Manager, Iterating an Async Generator

## Ambiguous Edges - Review These
- `/verify slash command` → `test_loads_spring_content()`  [AMBIGUOUS]
  .claude/commands/verify.md · relation: references
- `HashMap's Unreliable Iteration Order` → `Keys That Sort Themselves with TreeMap`  [AMBIGUOUS]
  content/java/lessons/data_structures_04_treemap_sorted_keys.yaml · relation: conceptually_related_to
- `The Class Spring Never Knew About` → `One Interface, a Different Bean Per Environment`  [AMBIGUOUS]
  content/spring/lessons/bean_lifecycle_01_missing_component_annotation.yaml · relation: references

## Knowledge Gaps
- **300 isolated node(s):** `coding-adventure`, `com.codingadventure:exercise`, `When can a lambda be replaced by a method reference?`, `What does Stream.reduce(identity, accumulator) do?`, `Why does calling .add() on a List.of(...) result throw UnsupportedOperationEx...` (+295 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **137 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `/verify slash command` and `test_loads_spring_content()`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **What is the exact relationship between `HashMap's Unreliable Iteration Order` and `Keys That Sort Themselves with TreeMap`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `The Class Spring Never Knew About` and `One Interface, a Different Bean Per Environment`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **Why does `ProgressStore` connect `Progress Store (XP/Streaks/Badges)` to `Category Metadata & App State`, `Settings & Platform Data Paths`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Why does `RunHandle` connect `ExecutionEngine Contract & RunHandle` to `Error Translation & Lesson Screen`, `Android In-Process Python Execution`, `Per-Language Execution Engines`, `test_python_inprocess_engine.py`, `test_execution_spring.py`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Why does `ExerciseEngine` connect `Exercise Engine Core Logic` to `Category Metadata & App State`, `Language Content Authoring Workflow`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Are the 17 inferred relationships involving `AppState` (e.g. with `Settings` and `ExerciseEngine`) actually correct?**
  _`AppState` has 17 INFERRED edges - model-reasoned connections that need verification._