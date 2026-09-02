# Graph Report - coding-adventure  (2026-09-02)

## Corpus Check
- 98 files · ~223,688 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1117 nodes · 1436 edges · 219 communities (89 shown, 130 thin omitted)
- Extraction: 85% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 208 edges (avg confidence: 0.84)
- Token cost: 460,964 input · 0 output

## Community Hubs (Navigation)
- C++ Quiz Bank
- Progress Store (XP/Streaks/Badges)
- Python AI Category (ML/RAG/Agents/MCP)
- Settings & Platform Data Paths
- Language Content Authoring Workflow
- Lesson Engine Content Tests
- Lesson Screen UI
- Project Overview Docs
- Exercise Engine Core Logic
- ExecutionEngine Contract & RunHandle
- Track Hub UI
- Node.js Execution Tests
- Project Overview Docs (Architecture)
- Java Observability Exercises
- Spring Execution Engine
- Android In-Process Python Execution
- App State & Daily Refresher
- Quiz Screen UI
- Settings Screen UI
- Spring Quiz Bank
- Toolchain Auto-Install Scripts
- Quiz Engine Core Logic
- Python Thread Scheduling Exercises
- Python In-Process Engine Tests
- Category Metadata (categories.py)
- Android Watchdog (execution)
- C++ Sync vs Async Exercises
- Output Validator (engine)
- Java Execution Tests
- Node.js Stdlib Deep Dive
- Java Stdlib Deep Dive
- Node.js Recursion Exercises
- Node.js Sync vs Async Exercises
- C++ Data Structures
- Java Sync Vs Async
- Errors (execution)
- Java Packaging
- Category Levels (ui)
- C++ Concurrency Async
- Java Dependency Management
- Python Concurrency Async
- Python Recursion
- Daily Refresher (ui)
- Progress Screen (ui)
- Java Idioms Gotchas
- C++ Core Refresher
- C++ Concurrency Async
- Java Observability
- Python Dependency Management
- Python Observability
- Setup Wizard (ui)
- C++ Gotcha Gauntlet
- Java Core Refresher
- Node.js Functional Programming
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
- Node.js Deployment
- Node.js Deployment
- Node.js Quiz Bank
- Python Concurrency Async
- Python Core Refresher
- Python Data Structures
- Python Data Structures
- Python Data Structures
- Python Observability
- Python Packaging
- Python Packaging
- Project Overview Docs
- C++ Gotcha Gauntlet
- Java Stdlib Deep Dive
- Node.js Gotcha Gauntlet
- Python Gotcha Gauntlet
- Python Sync Vs Async
- Project Docs & Rationale
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
- Node.js Concurrency Async
- Node.js Concurrency Async
- Node.js Core Refresher
- Node.js Functional Programming
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
- Spring Dependency Injection
- Spring Dependency Injection
- Spring Events
- Project Docs & Rationale
- ExecutionResult
- ExecutionResult
- RunHandle
- Path
- AppState
- ExecutionResult
- RunHandle
- AppState
- Project Overview Docs
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
- Node.js Core Refresher
- Node.js Data Structures
- Node.js Deployment
- Node.js Deployment
- Node.js Functional Programming
- Node.js Idioms Gotchas
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
- Spring Dependency Injection
- Spring Events
- Spring Events
- Spring Events
- Spring Quiz Bank
- Control
- Project Docs & Rationale
- Project Docs & Rationale
- Project Docs & Rationale
- Project Docs & Rationale
- ExecutionEngine
- Exercise
- fixture
- Page
- pyproject.toml
- pom.xml
- requirements.txt
- requirements.txt
- requirements.txt
- requirements.txt
- RunHandle
- View

## God Nodes (most connected - your core abstractions)
1. `AppState` - 41 edges
2. `ProgressStore` - 34 edges
3. `RunHandle` - 27 edges
4. `_ExerciseController` - 22 edges
5. `ExecutionResult` - 20 edges
6. `C++ Quiz Bank` - 20 edges
7. `ExecutionEngine` - 19 edges
8. `ExerciseEngine` - 16 edges
9. `_QuizController` - 16 edges
10. `Node.js Track` - 16 edges

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
- **Node.js Concurrency & Async Lesson Progression** — content_node_lessons_concurrency_async_01_callback_to_async_await_callback_style_to_async_await, content_node_lessons_concurrency_async_02_reading_before_resolved_reading_a_promise_s_result_before_it_resolves, content_node_lessons_concurrency_async_03_promise_all_vs_allsettled_one_rejection_sinks_promise_all, content_node_lessons_concurrency_async_04_sequential_await_loop_accidentally_serial_await_inside_a_loop, content_node_lessons_concurrency_async_05_unhandled_rejection_an_uncaught_rejection_inside_async_await [INFERRED 0.85]
- **Node.js Dependency Management Lesson Progression** — content_node_lessons_dependency_management_01_version_string_comparison_comparing_version_strings_lexicographically, content_node_lessons_dependency_management_02_caret_range_check_implementing_a_caret_range_check, content_node_lessons_dependency_management_03_package_json_optional_field_reading_an_optional_package_json_field_safely, content_node_lessons_dependency_management_04_require_resolve_feature_detection_detecting_an_optional_dependency_without_crashing, content_node_lessons_dependency_management_05_lock_file_exact_pin_why_a_lock_file_pins_an_exact_version [INFERRED 0.85]
- **Node.js Data Structures Lesson Progression** — content_node_lessons_data_structures_01_map_vs_object_a_plain_object_s_prototype_key_collision, content_node_lessons_data_structures_02_set_uniqueness_de_duplicating_with_set_instead_of_includes, content_node_lessons_data_structures_03_filter_map_reduce_a_manual_loop_to_filter_map_reduce, content_node_lessons_data_structures_04_nested_destructuring_defaults_nested_destructuring_with_defaults, content_node_lessons_data_structures_05_structured_clone_spread_s_shallow_copy_vs_structuredclone [INFERRED 0.80]
- **Node.js Deployment Lifecycle Practices** — content_node_lessons_deployment_02_boolean_env_var_truthy_string_every_non_empty_env_var_string_is_truthy, content_node_lessons_deployment_03_graceful_shutdown_signal_shutting_down_without_closing_anything, content_node_lessons_deployment_04_health_check_any_vs_all_health_check_that_passes_if_any_component_is_healthy, content_node_lessons_deployment_05_idempotent_deploy_step_deploy_step_that_isnt_safe_to_run_twice [INFERRED 0.75]
- **Functional Programming Principles in JavaScript** — content_node_lessons_functional_programming_01_pure_function_no_side_effects_function_that_mutates_what_it_was_given, content_node_lessons_functional_programming_02_closure_private_state_counter_factory_sharing_one_module_level_variable, content_node_lessons_functional_programming_03_pipe_composition_nested_calls_vs_a_pipe_helper, content_node_lessons_functional_programming_04_immutability_object_freeze_frozen_objects_mutation_fails_silently, content_node_lessons_functional_programming_05_partial_application_bind_wrapper_function_vs_partial_application_with_bind [INFERRED 0.80]
- **Gotcha Gauntlet Flagship Debug Puzzle Track** — content_node_lessons_gotcha_gauntlet_01_foreach_splice_skip_foreach_splice_the_silent_skip, content_node_lessons_gotcha_gauntlet_02_nan_self_comparison_nan_never_equals_itself, content_node_lessons_gotcha_gauntlet_03_shared_default_parameter_default_parameter_pointing_at_a_shared_array, content_node_lessons_gotcha_gauntlet_04_sort_mutates_in_place_sort_mutates_the_original_array, content_node_lessons_gotcha_gauntlet_05_reference_vs_structural_equality_reference_equality_on_two_identical_looking_arrays [INFERRED 0.80]
- **Node Recursion Category Progression** — content_node_lessons_recursion_01_missing_base_case_a_recursive_sum_with_no_base_case, content_node_lessons_recursion_02_no_tail_call_optimization_an_accumulator_doesnt_save_you_from_stack_overflow_in_node, content_node_lessons_recursion_03_mutual_recursion_wrong_base_case_mutual_recursion_with_the_wrong_base_case_value, content_node_lessons_recursion_04_object_nesting_depth_measuring_depth_without_actually_recursing_into_it, content_node_lessons_recursion_05_memoized_fibonacci_recomputing_the_same_fibonacci_call_millions_of_times [INFERRED 0.85]
- **Node Stdlib Deep-Dive Modern-Idiom Category** — content_node_lessons_stdlib_deep_dive_01_json_stringify_replacer_redacting_a_field_with_json_stringifys_replacer, content_node_lessons_stdlib_deep_dive_02_array_isarray_typeof_cant_tell_an_array_from_an_object, content_node_lessons_stdlib_deep_dive_03_object_entries_fromentries_transforming_every_value_with_entries_fromentries, content_node_lessons_stdlib_deep_dive_04_array_flat_flattening_a_nested_array_with_flat, content_node_lessons_stdlib_deep_dive_05_array_from_range_generating_a_range_with_array_from [INFERRED 0.85]
- **Node Event-Loop Timing Semantics Category** — content_node_lessons_sync_vs_async_01_blocking_call_delays_timers_a_blocking_call_delays_already_scheduled_timers, content_node_lessons_sync_vs_async_02_fire_and_forget_async_call_calling_an_async_function_without_awaiting_it, content_node_lessons_sync_vs_async_03_for_await_async_generator_for_of_cant_iterate_an_async_generator, content_node_lessons_sync_vs_async_04_nexttick_vs_promise_microtask_process_nexttick_jumps_the_promise_queue, content_node_lessons_sync_vs_async_05_throw_inside_settimeout_executor_a_deferred_throw_inside_a_promise_executor_isnt_caught [INFERRED 0.85]
- **RAG Pipeline Exercise Group (ai_06-ai_10)** — content_python_lessons_ai_06_cosine_similarity_vs_dot_product_cosine_similarity, content_python_lessons_ai_07_retrieval_top_k_sort_direction_top_k_retrieval, content_python_lessons_ai_08_chunking_without_overlap_chunk_overlap, content_python_lessons_ai_09_prompt_template_concatenation_prompt_template, content_python_lessons_ai_10_context_window_budget_context_window_budget [EXTRACTED 1.00]
- **Agentic Framework Exercise Group (ai_11-ai_15)** — content_python_lessons_ai_11_tool_dispatch_silent_fallthrough_tool_dispatch, content_python_lessons_ai_12_agent_loop_missing_max_iterations_max_steps_guard, content_python_lessons_ai_13_tool_call_missing_required_args_tool_arg_validation, content_python_lessons_ai_14_conversation_memory_drops_system_message_conversation_memory_trim, content_python_lessons_ai_15_agent_stop_condition_wrong_key_stop_condition_check [EXTRACTED 1.00]
- **MCP Protocol Exercise Group (ai_16-ai_20)** — content_python_lessons_ai_16_jsonrpc_request_missing_version_jsonrpc_version_field, content_python_lessons_ai_17_jsonrpc_response_both_result_and_error_result_error_exclusivity, content_python_lessons_ai_18_mcp_tool_registry_duplicate_names_tool_registry_dedup, content_python_lessons_ai_19_mcp_capability_negotiation_skipped_capability_negotiation, content_python_lessons_ai_20_mcp_response_correlation_by_arrival_order_request_response_correlation, content_python_lessons_ai_20_mcp_response_correlation_by_arrival_order_ai_master [EXTRACTED 1.00]
- **ExecutionEngine Subclass Implementations** — claude_pythonengine, claude_javaengine, claude_cppengine, claude_nodeengine, claude_springengine [EXTRACTED 1.00]
- **Standardized Packaging Metadata Parsing** — content_python_lessons_packaging_01_tomllib_parse_version_lesson, content_python_lessons_packaging_03_entry_point_registry_lesson, content_python_lessons_packaging_05_wheel_filename_parsing_lesson [INFERRED 0.70]
- **Blocking-Until-Ready Pattern Across Concurrency Models** — content_java_lessons_thread_scheduling_04_blocking_queue_blockingqueue, content_java_lessons_sync_vs_async_01_completablefuture_chaining_thenapply [INFERRED 0.75]
- **collections-module alternatives to manual dict/list bookkeeping** — content_python_lessons_data_structures_01_defaultdict_lesson, content_python_lessons_data_structures_02_counter_lesson, content_python_lessons_data_structures_03_deque_lesson [INFERRED 0.75]
- **Lock-based race-condition protection and timeout bounding** — content_python_lessons_concurrency_async_02_thread_lock_lesson, content_python_lessons_concurrency_async_04_asyncio_lock_lesson, content_python_lessons_concurrency_async_05_wait_for_timeout_lesson [INFERRED 0.75]
- **Java Concurrency Toolkit Progression** — content_java_lessons_concurrency_async_01_race_condition_synchronized_synchronized, content_java_lessons_concurrency_async_02_atomic_integer_atomicinteger, content_java_lessons_concurrency_async_03_executor_service_executorservice [INFERRED 0.75]
- **Core Observability Primitives** — content_python_lessons_observability_02_log_level_filtering_lesson, content_python_lessons_observability_03_correlation_id_contextvar_lesson, content_python_lessons_observability_04_metrics_counter_lesson, content_python_lessons_observability_05_timing_context_manager_lesson [INFERRED 0.75]
- **Configured Logging -> Level Filtering -> Correlation ID Pipeline** — content_java_lessons_observability_01_structured_logging_logger_handler_configuration, content_java_lessons_observability_02_log_level_filtering_two_stage_log_filtering, content_java_lessons_observability_03_correlation_id_threadlocal_threadlocal [INFERRED 0.75]
- **Python Thread Coordination and Identity Primitives** — content_python_lessons_thread_scheduling_01_reentrant_lock_exercise, content_python_lessons_thread_scheduling_02_thread_naming_exercise, content_python_lessons_thread_scheduling_03_daemon_flag_exercise, content_python_lessons_thread_scheduling_04_producer_consumer_queue_exercise, content_python_lessons_thread_scheduling_05_thread_local_storage_exercise [INFERRED 0.75]
- **Recursive Base-Case Bug Family** — content_python_lessons_recursion_01_missing_base_case_lesson, content_python_lessons_recursion_02_recursion_depth_limit_lesson, content_python_lessons_recursion_03_mutual_recursion_lesson [INFERRED 0.75]
- **Recursive Base-Case / Recursive-Case Correctness Failures** — content_java_lessons_recursion_01_missing_base_case_missing_base_case, content_java_lessons_recursion_03_mutual_recursion_wrong_base_case_value, content_java_lessons_recursion_04_recursive_tree_sum_missing_recursive_case [INFERRED 0.75]
- **Defensive Deployment Configuration Patterns** — content_java_lessons_deployment_01_env_var_defaults_exercise, content_java_lessons_deployment_02_case_insensitive_boolean_parsing_exercise, content_java_lessons_deployment_04_health_check_exercise, content_java_lessons_deployment_05_idempotent_deploy_step_exercise [INFERRED 0.75]
- **Spring Application Event Publish/Listen Mechanism Group** — content_spring_lessons_events_01_publish_forgotten_exercise, content_spring_lessons_events_02_missing_eventlistener_annotation_exercise, content_spring_lessons_events_03_multiple_listeners_fan_out_exercise, content_spring_lessons_events_04_conditional_event_listener_exercise, content_spring_lessons_events_05_custom_event_payload_exercise [INFERRED 0.80]
- **Language content verification workflow** — _claude_commands_verify_command, _claude_skills_add_language_content_skill_skill, concept_real_toolchain_verification [INFERRED 0.80]
- **std::async and std::future Pitfalls and Policies** — content_cpp_lessons_sync_vs_async_03_shared_future_multiple_waiters_sharedfuture, content_cpp_lessons_sync_vs_async_05_deferred_launch_runs_on_get_launchdeferred, content_cpp_lessons_thread_scheduling_04_explicit_async_launch_policy_launchasync [INFERRED 0.80]
- **Dependency Injection: Constructor vs. Field Injection Pattern Group** — content_spring_lessons_dependency_injection_01_field_injection_untestable_exercise, content_spring_lessons_dependency_injection_02_ambiguous_bean_no_qualifier_exercise, content_spring_lessons_dependency_injection_03_primary_bean_exercise, content_spring_lessons_dependency_injection_04_optional_dependency_exercise, content_spring_lessons_dependency_injection_05_constructor_injection_final_fields_exercise [INFERRED 0.80]
- **End-to-end dependency management curriculum arc** — content_python_lessons_dependency_management_01_detect_virtualenv_lesson, content_python_lessons_dependency_management_02_parse_requirement_line_lesson, content_python_lessons_dependency_management_03_version_string_comparison_lesson, content_python_lessons_dependency_management_04_importlib_metadata_lesson, content_python_lessons_dependency_management_05_lock_file_pin_lesson [INFERRED 0.80]
- **Functional Programming Lesson Sequence** — content_python_lessons_functional_programming_01_pure_functions_pure_functions, content_python_lessons_functional_programming_02_map_filter_map_filter_pipeline, content_python_lessons_functional_programming_03_function_composition_function_composition, content_python_lessons_functional_programming_04_immutability_immutable_namedtuple, content_python_lessons_functional_programming_05_partial_application_functools_partial [INFERRED 0.80]
- **Gotcha Gauntlet Lesson Sequence** — content_python_lessons_gotcha_gauntlet_01_off_by_one_slice_negative_slice_off_by_one, content_python_lessons_gotcha_gauntlet_02_exception_swallowing_bare_except_swallowing, content_python_lessons_gotcha_gauntlet_03_mutable_class_attribute_shared_class_attribute, content_python_lessons_gotcha_gauntlet_04_rounding_precision_decimal_rounding, content_python_lessons_gotcha_gauntlet_05_dict_mutation_during_iteration_dict_mutation_during_iteration, content_python_lessons_gotcha_gauntlet_06_missing_super_init_missing_super_init_call [INFERRED 0.80]
- **Idioms and Gotchas Lesson Sequence** — content_python_lessons_idioms_gotchas_01_mutable_default_arg_mutable_default_argument, content_python_lessons_idioms_gotchas_02_late_binding_closure_late_binding_closure, content_python_lessons_idioms_gotchas_03_is_vs_equals_identity_vs_equality, content_python_lessons_idioms_gotchas_04_float_precision_float_precision_isclose, content_python_lessons_idioms_gotchas_05_aliasing_vs_copying_aliasing_vs_copying, content_python_lessons_idioms_gotchas_06_sort_returns_none_sort_returns_none [INFERRED 0.80]
- **CompletableFuture Async Pipeline Pattern** — content_java_lessons_sync_vs_async_01_completablefuture_chaining_thenapply, content_java_lessons_sync_vs_async_02_completablefuture_combine_thencombine, content_java_lessons_sync_vs_async_03_completablefuture_exceptionally_exceptionally, content_java_lessons_sync_vs_async_04_supplyasync_custom_executor_supplyasyncexecutor, content_java_lessons_sync_vs_async_05_virtual_threads_virtualthreads [INFERRED 0.80]
- **Empty-Body / No-Op Stub Implementation Antipattern** — content_java_lessons_packaging_04_service_registry_stub_method_no_op_bug, content_java_lessons_observability_04_metrics_counter_stub_method_no_op_bug, content_java_lessons_observability_05_timing_instrumentation_stub_method_no_op_bug [INFERRED 0.80]
- **Numeric Version Comparison and Coordinate Parsing** — content_java_lessons_dependency_management_01_version_string_comparison_exercise, content_java_lessons_dependency_management_04_minimum_version_check_exercise, content_java_lessons_dependency_management_05_maven_coordinate_parsing_exercise [INFERRED 0.80]
- **Concurrent Execution With Preserved/Trade-off Ordering (gather vs Promise.all)** — content_python_lessons_concurrency_async_01_gather_order_asyncio_gather_input_order, content_python_lessons_concurrency_async_01_gather_order_sequential_await_loop_trap [INFERRED 0.85]
- **Busy-Wait Avoidance Techniques in C++ Threading** — content_cpp_lessons_thread_scheduling_01_sleep_for_not_busy_wait_sleepfor, content_cpp_lessons_thread_scheduling_02_this_thread_yield_yield, content_cpp_lessons_thread_scheduling_05_condition_variable_producer_consumer_conditionvariable [INFERRED 0.85]
- **Gotcha Gauntlet Puzzle Set** — content_java_lessons_gotcha_gauntlet_01_off_by_one_loop_exercise, content_java_lessons_gotcha_gauntlet_02_switch_fallthrough_exercise, content_java_lessons_gotcha_gauntlet_03_concurrent_modification_exercise, content_java_lessons_gotcha_gauntlet_04_integer_overflow_exercise, content_java_lessons_gotcha_gauntlet_05_equals_hashcode_contract_exercise [INFERRED 0.85]
- **Gotcha Gauntlet Category Progression** — content_cpp_lessons_gotcha_gauntlet_01_off_by_one_array_off_by_one_array_read, content_cpp_lessons_gotcha_gauntlet_02_uncaught_out_of_range_vector_at_out_of_range, content_cpp_lessons_gotcha_gauntlet_03_static_variable_persistence_static_variable_persistence, content_cpp_lessons_gotcha_gauntlet_04_integer_overflow_integer_overflow_wraparound, content_cpp_lessons_gotcha_gauntlet_05_missing_virtual_destructor_missing_virtual_destructor [INFERRED 0.85]
- **Resilience4j Decorator Pattern Group** — content_spring_lessons_resilience_01_circuit_breaker_opens_after_failures_exercise, content_spring_lessons_resilience_02_retry_until_success_exercise, content_spring_lessons_resilience_03_rate_limiter_rejects_excess_calls_exercise, content_spring_lessons_resilience_04_fallback_on_failure_exercise, content_spring_lessons_resilience_05_circuit_breaker_before_retry_exercise [INFERRED 0.85]
- **Spring AOP Advice Types Progression** — content_spring_lessons_aop_01_missing_aspect_annotation_exercise, content_spring_lessons_aop_02_pointcut_expression_wrong_method_exercise, content_spring_lessons_aop_03_afterreturning_captures_result_exercise, content_spring_lessons_aop_04_around_advice_modifying_result_exercise, content_spring_lessons_aop_05_self_invocation_bypasses_proxy_exercise [INFERRED 0.85]
- **Spring Bean Lifecycle Hooks Progression** — content_spring_lessons_bean_lifecycle_01_missing_component_annotation_exercise, content_spring_lessons_bean_lifecycle_02_singleton_shared_state_exercise, content_spring_lessons_bean_lifecycle_03_postconstruct_initialization_exercise, content_spring_lessons_bean_lifecycle_04_predestroy_cleanup_exercise, content_spring_lessons_bean_lifecycle_05_lazy_initialization_exercise [INFERRED 0.85]
- **Cast-the-Operand-Not-the-Result Principle** — content_cpp_lessons_idioms_gotchas_01_integer_division_truncation_integer_division_truncation, content_cpp_lessons_idioms_gotchas_04_unsigned_underflow_loop_unsigned_underflow_loop, content_cpp_lessons_gotcha_gauntlet_04_integer_overflow_integer_overflow_wraparound [INFERRED 0.90]

## Communities (219 total, 130 thin omitted)

### Community 0 - "C++ Quiz Bank"
Cohesion: 0.05
Nodes (50): Closures / higher-order functions (function factories), Lambda capture-by-value vs. capture-by-reference, Lambda expressions (vs. functor structs), Memoization, Mutual Recursion, Recursion, std::accumulate (fold/reduce operation), std::function type erasure (+42 more)

### Community 1 - "Progress Store (XP/Streaks/Badges)"
Cohesion: 0.06
Nodes (14): _level_from_xp(), _now(), PlayerLevel, ProgressStore, SQLite-backed progress, gamification, and activity tracking -- one…, Owns the SQLite connection for progress data across every language track., The exercise ids fixed for this language on this date, or an empty list if…, Returns True if newly awarded, False if already had it. (+6 more)

### Community 2 - "Python AI Category (ML/RAG/Agents/MCP)"
Cohesion: 0.06
Nodes (43): Evaluating on Held-Out Test Data Instead of Training Data, Cosine Similarity vs Raw Dot Product, Top-K Retrieval Sort Direction, Chunking With Overlap to Preserve Boundary Phrases, Delimited RAG Prompt Template, Context Window Character Budget, Tool Dispatcher Failing Loudly on Unknown Tool, Agent Loop max_steps Guard (+35 more)

### Community 3 - "Settings & Platform Data Paths"
Cohesion: 0.10
Nodes (28): Path, Resolves the writable directory this app's data lives in. On desktop/web this…, Returns FLET_APP_STORAGE_DATA when set (packaged builds, e.g. Android),…, resolve_platform_data_dir(), get_data_dir(), get_db_path(), get_settings_path(), is_first_run() (+20 more)

### Community 4 - "Language Content Authoring Workflow"
Cohesion: 0.09
Nodes (29): /verify slash command, add-language-content skill, CATEGORY_META dict (code), get_language(), LanguageInfo, The set of language tracks the app knows about, and which ones have real…, Loads one language track's exercises from YAML, kept separate from application…, is_android() (+21 more)

### Community 5 - "Lesson Engine Content Tests"
Cohesion: 0.11
Nodes (26): Exercise, Pure lookup/generate step behind AppState.daily_refresher_exercises(), split…, Today's fixed Daily Refresher set -- generated once per calendar day and…, resolve_daily_refresher(), ExerciseEngine, engine(), progress(), fixture (+18 more)

### Community 6 - "Lesson Screen UI"
Cohesion: 0.12
Nodes (11): make_code_editor(), make_read_only_code_block(), Control, ThemePreset, A plain monospace multiline code editor -- no live syntax highlighting; Flet's…, _ExerciseController, Control, View (+3 more)

### Community 7 - "Project Overview Docs"
Cohesion: 0.09
Nodes (29): One Rejection Sinks Promise.all, Accidentally Serial: await Inside a Loop, Array Destructuring with Rest, Merging Objects with Spread, Optional Chaining and Nullish Coalescing, A Plain Object's Prototype Key Collision, A Manual Loop to filter/map/reduce, Comparing Version Strings Lexicographically (+21 more)

### Community 8 - "Exercise Engine Core Logic"
Cohesion: 0.23
Nodes (5): ExerciseEngine, Exercise, Path, A small guided set for "today's refresher" -- round-robins the next unlocked,…, category -> (done, total), done computed by the caller passing completed_ids in…

### Community 9 - "ExecutionEngine Contract & RunHandle"
Cohesion: 0.16
Nodes (10): ExecutionResult, Lets the UI cancel a run that's in progress (e.g. an infinite loop). Every…, exercise is unused by the single-file engines (Python/Java/C++) -- SpringEngine…, RunHandle, CppEngine, _describe_crash(), C++ execution engine: compiles the submitted code with `g++`, then runs the…, PythonEngine (+2 more)

### Community 10 - "Track Hub UI"
Cohesion: 0.16
Nodes (14): main(), Page, Root Flet application: route-based navigation between full-screen views.…, build_lesson_view(), Exercise, Page, build_track_hub_view(), _card() (+6 more)

### Community 11 - "Node.js Execution Tests"
Cohesion: 0.18
Nodes (8): ABC, ExecutionEngine, Shared execution contract every per-language engine implements. Framing is…, One concrete subclass per language track (python_engine.PythonEngine,…, NodeEngine, Node.js execution engine: runs submitted JavaScript with `node`, no separate…, get_engine(), Maps a language key to its ExecutionEngine instance.

### Community 12 - "Project Overview Docs (Architecture)"
Cohesion: 0.17
Nodes (16): app_window.py route dispatcher, AppState, categories.py CATEGORY_META, CppEngine (cpp_engine.py), errors.py translate_error(), ExecutionEngine ABC, Exercise dataclass, ExerciseEngine (+8 more)

### Community 13 - "Java Observability Exercises"
Cohesion: 0.13
Nodes (16): A Minimal Metrics Counter, Map.merge Increment Idiom, Empty-Body increment() Stub Bug, AutoCloseable + try-with-resources Timing, Instrumenting a Block's Duration, Empty close() Stub Bug, Validating a Package Name Convention, Java Package Naming Convention (+8 more)

### Community 14 - "Spring Execution Engine"
Cohesion: 0.22
Nodes (12): Exercise, The Exercise data model. Content is data, not code -- see…, _detect_class_name(), Spring execution engine: unlike the single-file engines, a Spring exercise…, Maven reports absolute paths (both backslash and the forward-slash form it uses…, _sanitize_path(), SpringEngine, _exercise() (+4 more)

### Community 15 - "Android In-Process Python Execution"
Cohesion: 0.17
Nodes (11): _make_input(), PythonInProcessEngine, In-process Python execution engine, used specifically on Android in place of…, Mirrors how a real stdin pipe behaves: a trailing newline marks the end of the…, Same ExecutionResult/RunHandle contract as PythonEngine, but runs code in-…, _split_stdin(), Raised inside exec()'d code when it runs past its deadline or is cancelled.…, Watchdog (+3 more)

### Community 16 - "App State & Daily Refresher"
Cohesion: 0.17
Nodes (6): AppState, ThemePreset, build_quiz_view(), Page, Quiz Bank: pick a question count, answer a randomized multiple-choice run, end…, QuizEngine

### Community 17 - "Quiz Screen UI"
Cohesion: 0.24
Nodes (4): Control, View, _QuizController, Button

### Community 18 - "Settings Screen UI"
Cohesion: 0.29
Nodes (12): _build_font_card(), build_settings_view(), _build_theme_card(), _build_theme_option(), Control, Page, View, Settings: theme presets and code font size. (+4 more)

### Community 19 - "Spring Quiz Bank"
Cohesion: 0.14
Nodes (15): The Config Value That Must Not Have a Default, The Gateway That Kept Calling a Dead Service, Giving a Flaky Call a Second (and Third) Chance, The Call That Wasn't Allowed to Happen Yet, Degrading Gracefully Instead of Failing Loudly, The Retry That Kept Hammering a Circuit That Should Have Stopped It, What does a Resilience4j CircuitBreaker do once its failure rate threshold is crossed within its sliding window?, What kind of failure is Resilience4j's Retry decorator meant to address? (+7 more)

### Community 20 - "Toolchain Auto-Install Scripts"
Cohesion: 0.19
Nodes (8): is_python_process(), run_app_web_ui.sh script, run_app_window_mode.sh script, _confirm(), ensure_cpp(), ensure_java(), ensure_toolchains.sh script, _windows_path_add()

### Community 21 - "Quiz Engine Core Logic"
Cohesion: 0.23
Nodes (7): Path, QuizEngine, Loads a language track's quiz questions from YAML. Adding a question means…, A freshly randomized set of questions for one quiz playthrough -- which…, QuizQuestion, The QuizQuestion data model. Quiz content is data, not code -- see…, Collection

### Community 22 - "Python Thread Scheduling Exercises"
Cohesion: 0.15
Nodes (14): The Lock That Locked Itself Out, Naming Threads for Debuggable Logs, Marking a Background Thread as Daemon, A Producer/Consumer Handoff with queue.Queue, Per-Thread State with threading.local(), The Class Spring Never Knew About, The 'Two' Instances That Were Actually One, Initializing Before Your Dependencies Arrive (+6 more)

### Community 24 - "Category Metadata (categories.py)"
Cohesion: 0.22
Nodes (10): CategoryMeta, get_category_meta(), Display metadata (title, icon, color) for exercise categories, used by the…, _build_category_card(), build_category_map_view(), Control, Page, View (+2 more)

### Community 25 - "Android Watchdog (execution)"
Cohesion: 0.21
Nodes (9): compile_with_watchdog(), _LoopTickInjector, Cooperative timeout mechanism for PythonInProcessEngine (Android). A…, Inserts a call to __codingadventure_tick__() as the first statement in every…, Parses source, injects watchdog ticks into every loop, and compiles the result.…, AST, Expr, For (+1 more)

### Community 26 - "C++ Sync vs Async Exercises"
Cohesion: 0.22
Nodes (13): Shared Future for Multiple Waiters, Synchronous Wrapper Over Async API, Deferred Launch Runs On get(), sleep_for Instead of Busy-Wait, this_thread::yield in a Spin Loop, Joining All Threads in a Vector, Explicit std::launch::async Policy, Condition Variable Producer/Consumer (+5 more)

### Community 27 - "Output Validator (engine)"
Cohesion: 0.27
Nodes (10): Exercise validation: checks behavior/output, not exact code formatting., True if `code` contains every required pattern. Each pattern is matched as a…, Compares output, optionally substituting what the user typed into a template. -…, validate_contains(), validate_output(), test_validate_contains_empty_patterns_always_true(), test_validate_contains_requires_all_patterns(), test_validate_output_exact_match() (+2 more)

### Community 28 - "Java Execution Tests"
Cohesion: 0.20
Nodes (3): _detect_class_name(), JavaEngine, Java execution engine: detects the submitted code's class name, compiles it…

### Community 29 - "Node.js Stdlib Deep Dive"
Cohesion: 0.17
Nodes (12): Redacting a Field with JSON.stringify's Replacer, typeof Can't Tell an Array from an Object, Transforming Every Value with entries/fromEntries, Flattening a Nested Array with flat(), Generating a Range with Array.from, Quiz Q21: JSON.stringify Replacer for Redaction, Quiz Q22: typeof Cannot Distinguish Arrays, Quiz Q23: entries/fromEntries Pipeline (+4 more)

### Community 30 - "Java Stdlib Deep Dive"
Cohesion: 0.25
Nodes (11): The Countdown That Never Stopped, Missing Base Case, StackOverflowError, Recursion-to-Iteration Conversion, JVM Has No Tail-Call Optimization, Hitting the Stack Limit, Building a String in a Loop, O(n^2) String Concatenation Bug (+3 more)

### Community 31 - "Node.js Recursion Exercises"
Cohesion: 0.18
Nodes (11): A Recursive Sum With No Base Case, An Accumulator Doesn't Save You From Stack Overflow in Node, Mutual Recursion With the Wrong Base Case Value, Measuring Depth Without Actually Recursing Into It, Recomputing the Same Fibonacci Call Millions of Times, Quiz Q49: Recursion With No Base Case, Quiz Q50: Tail-Call Form Doesn't Protect From Stack Overflow, Quiz Q51: Mutual Recursion Base Case Determines Result (+3 more)

### Community 32 - "Node.js Sync vs Async Exercises"
Cohesion: 0.18
Nodes (11): A Blocking Call Delays Already-Scheduled Timers, Calling an async Function Without Awaiting It, for...of Can't Iterate an Async Generator, process.nextTick Jumps the Promise Queue, A Deferred throw Inside a Promise Executor Isn't Caught, Quiz Q39: Synchronous Work Delays Scheduled Timers, Quiz Q40: Calling async Without Awaiting, Quiz Q41: for...of Cannot Consume Async Generators (+3 more)

### Community 33 - "C++ Data Structures"
Cohesion: 0.20
Nodes (10): std::deque (O(1) front/back ops), std::priority_queue (heap), std::set (uniqueness by construction), std::sort (introsort), std::unordered_map (hash table O(1) lookup), Manual Bubble Sort to std::sort, Linear Search to unordered_map Lookup, O(1) Front Removal with deque (+2 more)

### Community 34 - "Java Sync Vs Async"
Cohesion: 0.22
Nodes (10): CompletableFuture.thenApply Chaining, CompletableFuture.thenCombine, CompletableFuture.exceptionally Recovery, supplyAsync with Custom ExecutorService, Virtual Threads vs Fixed Platform-Thread Pool, Naming Threads for Debuggable Logs, Marking a Background Thread as Daemon, Thread Scheduling Priority as a Hint (+2 more)

### Community 35 - "Errors (execution)"
Cohesion: 0.36
Nodes (7): _last_exception_type(), Translates raw interpreter/compiler output into concise, professional…, _translate_cpp_error(), translate_error(), _translate_java_error(), _translate_node_error(), _translate_spring_error()

### Community 36 - "Java Packaging"
Cohesion: 0.28
Nodes (9): Cascading Reset Rule, Bumping a Semantic Version, Semantic Versioning (major.minor.patch), Unchanged-Passthrough Stub Bug, artifact-version.jar Filename Convention, lastIndexOf Boundary Parsing, Parsing a JAR Filename, Unparsed-Passthrough Stub Bug (+1 more)

### Community 37 - "Category Levels (ui)"
Cohesion: 0.39
Nodes (7): build_category_levels_view(), build_exercise_list_view(), _build_row(), Control, Page, View, A plain list of exercises -- shared renderer for a single category's levels and…

### Community 38 - "C++ Concurrency Async"
Cohesion: 0.32
Nodes (8): std::atomic lock-free operations, std::mutex + std::lock_guard, Race Condition (unsynchronized shared counter), RAII (Resource Acquisition Is Initialization), std::unique_ptr smart pointer, The Counter Two Threads Corrupted (mutex/lock_guard), std::atomic Instead of a Manually Locked Counter, Manual new/delete to unique_ptr

### Community 39 - "Java Dependency Management"
Cohesion: 0.25
Nodes (8): Comparing Version Numbers as Strings, Numeric Part-by-Part Version Comparison, The Classpath Conflict That Picked the Older Version, Compare-Before-Overwrite Classpath Resolution, Does This Version Satisfy the Minimum?, Minimum-Version Satisfaction Check, Parsing a Maven Coordinate, groupId:artifactId:version Coordinate Parsing

### Community 40 - "Python Concurrency Async"
Cohesion: 0.25
Nodes (8): Protecting a Shared Counter with a Lock, threading.Lock critical-section pattern, Running I/O-Bound Work Concurrently, ThreadPoolExecutor concurrent map/submit, asyncio.Lock read-await-write protection, The Async Equivalent of a Race Condition, asyncio.wait_for deadline pattern, Bounding How Long You'll Wait

### Community 41 - "Python Recursion"
Cohesion: 0.25
Nodes (8): Hitting Python's Recursion Limit, Python Recursion Limit / No Tail-Call Optimization, Accumulator Pattern, Reversing a List with an Accumulator, Memoizing a Recursive Function, functools.lru_cache Memoization, Folding a List Into One Value, functools.reduce

### Community 42 - "Daily Refresher (ui)"
Cohesion: 0.29
Nodes (5): Shared app state: settings, progress store, per-language exercise/quiz engines…, build_daily_refresher_view(), Page, View, Daily Refresher: a short cross-topic set (app.engine.lesson_engine.…

### Community 43 - "Progress Screen (ui)"
Cohesion: 0.38
Nodes (6): build_progress_view(), _describe_activity(), Page, View, Per-track dashboard: streak, XP, mastery by topic, achievements., _relative_time()

### Community 44 - "Java Idioms Gotchas"
Cohesion: 0.38
Nodes (7): Autoboxing, JVM Integer Cache (-128..127), Autoboxed Integer Comparison, Reference Equality vs .equals(), Null-Safe Comparison with Objects.equals, Null-Safe Equality Checking, java.util.Objects.equals

### Community 47 - "C++ Core Refresher"
Cohesion: 0.33
Nodes (6): auto type deduction, Range-based for loop, Structured bindings (C++17), Index Loop to Range-Based For, Spelling Out a Type auto Could Deduce, Iterator Members to Structured Bindings

### Community 48 - "C++ Concurrency Async"
Cohesion: 0.40
Nodes (6): std::promise/std::future one-shot channel, std::async / std::future asynchronous computation, std::thread join()/detach() joinability, Running a Computation Asynchronously (std::async/future), The Thread That Was Never Joined, Signaling a Result with promise/future

### Community 49 - "Java Observability"
Cohesion: 0.33
Nodes (6): Bypassing Logging Infrastructure with println, java.util.logging, Using the Logger That's Already Configured, Logger/Handler/Formatter Configuration, The Log Level Set Too High, Two-Stage Log Level Filtering (Logger + Handler)

### Community 50 - "Python Dependency Management"
Cohesion: 0.33
Nodes (6): Parsing a requirements.txt Pin, str.partition requirement-line parsing, Comparing Version Numbers as Strings, Integer-tuple version comparison, Exact-pin lock-file reproducibility, Why an Exact Pin Guarantees Reproducibility

### Community 51 - "Python Observability"
Cohesion: 0.33
Nodes (6): contextvars.ContextVar, Threading a Correlation ID Through Log Lines, Cooperative Event Loop Yielding, The Blocking Call That Froze the Event Loop, Running Blocking I/O Without Blocking the Loop, asyncio.to_thread

### Community 52 - "Setup Wizard (ui)"
Cohesion: 0.40
Nodes (4): build_setup_wizard_view(), Page, View, First-run setup: just a display name, nothing else.

### Community 53 - "C++ Gotcha Gauntlet"
Cohesion: 0.40
Nodes (5): Off-By-One Array Read (i <= size), Uncaught std::out_of_range from vector::at(), Recursion Missing a Base Case, Base Case That Only Matches Exact Equality, std::stoi Throwing std::invalid_argument

### Community 54 - "Java Core Refresher"
Cohesion: 0.40
Nodes (5): Anonymous Class to Lambda Expression, Filter and Transform with Streams, Optional Instead of Manual Null Check, Boilerplate Class to record, Manual close() to try-with-resources

### Community 55 - "Node.js Functional Programming"
Cohesion: 0.40
Nodes (5): A Counter Factory Sharing One Module-Level Variable, var's Shared Loop Variable, Replacing Plain console.log with Structured Logging, A Logger With Levels That Never Actually Filters, Threading a Correlation ID Through Every Function Call

### Community 56 - "Spring Aop"
Cohesion: 0.60
Nodes (5): The Advice That Was Never An Aspect, The Pointcut Watching the Wrong Method, The Advice That Couldn't See the Answer, The Advice That Could Change the Answer, The Call That Skipped Its Own Proxy

### Community 58 - "Java Data Structures"
Cohesion: 0.67
Nodes (4): HashMap's Unreliable Iteration Order, O(1) Queue Operations with ArrayDeque, Sorting by Custom Field with Comparator, Keys That Sort Themselves with TreeMap

### Community 59 - "Java Deployment"
Cohesion: 0.50
Nodes (4): Configuration with a Safe Default, System.getenv().getOrDefault Fallback Pattern, equalsIgnoreCase for Config Booleans, The Feature Flag That Only Worked in Lowercase

### Community 60 - "Java Functional Programming"
Cohesion: 0.50
Nodes (4): Lambda to Method Reference, Method Reference Forms (unbound/static/bound), Function.andThen/compose Composition, Composing Functions with andThen

### Community 61 - "Java Gotcha Gauntlet"
Cohesion: 0.50
Nodes (4): equals()/hashCode() Contract, equals() Without hashCode(): The Broken Contract, == vs .equals() for Strings, String Reference Identity vs Content Equality

### Community 62 - "Java Idioms Gotchas"
Cohesion: 0.67
Nodes (4): finally Block Semantics, The finally Block That Ate the Return, Return-in-finally Antipattern, try-with-resources

### Community 63 - "Java Idioms Gotchas"
Cohesion: 0.67
Nodes (4): Array Default Values, The Array Slot That Was Never Set, NullPointerException, Object vs Primitive Array Defaults

### Community 64 - "Java Idioms Gotchas"
Cohesion: 0.67
Nodes (4): Instance Fields, The Counter Every Instance Shared, Shared Mutable State Bug, Static Fields

### Community 65 - "Java Observability"
Cohesion: 0.83
Nodes (4): Threading a Correlation ID Through Log Lines, MDC (Mapped Diagnostic Context), Per-Thread Isolation, ThreadLocal

### Community 66 - "Java Packaging"
Cohesion: 0.50
Nodes (4): JAR MANIFEST.MF Format, Reading Main-Class Out of a Manifest, Nested String.split Parsing, What does a JAR manifest's Main-Class entry specify?

### Community 67 - "Node.js Deployment"
Cohesion: 0.50
Nodes (4): Every Non-Empty Env Var String Is Truthy, NaN Never Equals Itself, Reference Equality on Two Identical-Looking Arrays, Loose Equality's Coercion Trap

### Community 68 - "Node.js Deployment"
Cohesion: 0.50
Nodes (4): A Deploy Step That Isn't Safe to Run Twice, A Function That Mutates What It Was Given, A Frozen Object's Mutation Fails Silently, A Default Parameter Pointing at a Shared Array

### Community 69 - "Node.js Quiz Bank"
Cohesion: 0.50
Nodes (3): Incrementing a Metric That Was Never Initialized, A Timer That Never Actually Records the Duration, Quiz Q57: metrics[name]++ and NaN

### Community 70 - "Python Concurrency Async"
Cohesion: 0.83
Nodes (4): asyncio.as_completed Completion Order, asyncio.gather Concurrent + Input-Order Results, asyncio.gather Preserves Input Order, Sequential await-in-loop Trap

### Community 71 - "Python Core Refresher"
Cohesion: 0.50
Nodes (4): *args / **kwargs variable arity, Accepting Any Number of Arguments, Decorator function-wrapping pattern, Wrapping a Function with a Decorator

### Community 72 - "Python Data Structures"
Cohesion: 0.50
Nodes (4): collections.defaultdict factory-on-miss, Grouping Without Manual Key Checks, collections.Counter tallying, Tallying with Counter

### Community 73 - "Python Data Structures"
Cohesion: 0.50
Nodes (4): collections.deque O(1) double-ended ops, O(1) Queue Operations with deque, Finding Overlap with Set Operations, Set intersection/union O(1) membership

### Community 74 - "Python Data Structures"
Cohesion: 0.50
Nodes (4): heapq.nsmallest/nlargest partial selection, The k Smallest Items Without a Full Sort, bisect.insort binary-search insertion, Inserting Into a Sorted List Without Re-Sorting

### Community 75 - "Python Observability"
Cohesion: 0.50
Nodes (4): Instrumenting a Block's Duration, Timer Context Manager, contextlib.suppress, Suppressing an Expected Exception Cleanly

### Community 76 - "Python Packaging"
Cohesion: 0.50
Nodes (4): Reading a Version Out of pyproject.toml, tomllib Module, Packaging Entry Points, Building a Plugin Registry with a Decorator

### Community 77 - "Python Packaging"
Cohesion: 0.50
Nodes (4): __all__ Public API Declaration, Controlling a Package's Public API with __all__, Adding Type Hints for Clarity and Tooling, Type Hints (PEP 484)

### Community 78 - "Project Overview Docs"
Cohesion: 0.67
Nodes (3): android_platform.py (is_android), python_inprocess_engine.py, watchdog.py (AST loop-tick injector)

### Community 79 - "C++ Gotcha Gauntlet"
Cohesion: 0.67
Nodes (3): Signed Integer Overflow Wraparound, Integer Division Truncation, Unsigned Integer Underflow in a Countdown Loop

### Community 80 - "Java Stdlib Deep Dive"
Cohesion: 1.00
Nodes (3): Format Placeholder Options (%d, %.2f, %-10s), Structured Output with String.format, String.format Templating

### Community 81 - "Node.js Gotcha Gauntlet"
Cohesion: 0.67
Nodes (3): forEach + splice: The Silent Skip, sort() Mutates the Original Array, Array.sort()'s String-First Default

### Community 82 - "Python Gotcha Gauntlet"
Cohesion: 0.67
Nodes (3): Mutable Class Attribute Shared Across Instances, Mutable Default Argument Trap, Late-Binding Closures in Loops

### Community 83 - "Python Sync Vs Async"
Cohesion: 0.67
Nodes (3): Calling an Async Function Without Awaiting It, The Async Analog of a Context Manager, Iterating an Async Generator

### Community 84 - "Project Docs & Rationale"
Cohesion: 0.67
Nodes (3): Crash-Containment, Not a Safety Sandbox, Execution Engine Architecture Diagram, Execution Engines Overview

## Ambiguous Edges - Review These
- `/verify slash command` → `test_loads_spring_content()`  [AMBIGUOUS]
  .claude/commands/verify.md · relation: references
- `The Class Spring Never Knew About` → `One Interface, a Different Bean Per Environment`  [AMBIGUOUS]
  content/spring/lessons/bean_lifecycle_01_missing_component_annotation.yaml · relation: references
- `HashMap's Unreliable Iteration Order` → `Keys That Sort Themselves with TreeMap`  [AMBIGUOUS]
  content/java/lessons/data_structures_04_treemap_sorted_keys.yaml · relation: conceptually_related_to

## Knowledge Gaps
- **340 isolated node(s):** `coding-adventure`, `com.codingadventure:exercise`, `PYTHONUTF8`, `build_apk.sh script`, `What naming convention do Java package names conventionally follow?` (+335 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **130 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `/verify slash command` and `test_loads_spring_content()`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **What is the exact relationship between `The Class Spring Never Knew About` and `One Interface, a Different Bean Per Environment`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **What is the exact relationship between `HashMap's Unreliable Iteration Order` and `Keys That Sort Themselves with TreeMap`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `AppState` connect `App State & Daily Refresher` to `Progress Store (XP/Streaks/Badges)`, `Category Levels (ui)`, `Lesson Engine Content Tests`, `Lesson Screen UI`, `Daily Refresher (ui)`, `Track Hub UI`, `Progress Screen (ui)`, `Quiz Screen UI`, `Settings Screen UI`, `Setup Wizard (ui)`, `Category Metadata (categories.py)`?**
  _High betweenness centrality (0.046) - this node is a cross-community bridge._
- **Why does `ProgressStore` connect `Progress Store (XP/Streaks/Badges)` to `App State & Daily Refresher`, `Daily Refresher (ui)`, `Lesson Engine Content Tests`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Why does `_QuizController` connect `Quiz Screen UI` to `App State & Daily Refresher`?**
  _High betweenness centrality (0.013) - this node is a cross-community bridge._
- **Are the 16 inferred relationships involving `AppState` (e.g. with `ProgressStore` and `build_category_levels_view()`) actually correct?**
  _`AppState` has 16 INFERRED edges - model-reasoned connections that need verification._