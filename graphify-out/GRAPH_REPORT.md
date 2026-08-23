# Graph Report - coding-adventure  (2026-08-23)

## Corpus Check
- 35 files · ~75,516 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 930 nodes · 1735 edges · 63 communities (42 shown, 21 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 107 edges (avg confidence: 0.88)
- Token cost: 198,889 input · 0 output

## Community Hubs (Navigation)
- Categories, Languages & App State
- Concurrency & Async Lessons (Java/C++)
- Execution Engine Contract & Exercise Model
- Data Structures & Algorithms Lessons
- Functional Programming Lessons
- Spring Configuration & Profiles + Deployment Lessons
- Progress Store & XP Leveling
- Exercise Content Model & Category Logic
- Tooling Docs & Output Validator
- Packaging Lessons
- Error Translation & Lesson Screen UI
- Observability Lessons
- Dependency Management Lessons
- Core Refresher Lessons (Java/C++)
- Spring Bean Lifecycle & Scopes
- App Data Directory Resolution
- Spring Dependency Injection
- Sync vs Async Lessons
- Quiz Screen Controller
- Cross-Language Gotchas (Switch/Closures/Vectors)
- Quiz Content Model
- Java equals()/hashCode() Gotchas
- Python Idioms & Static-Field Gotchas
- Python Collections Lessons
- Stdlib Deep Dive & Exception Handling Lessons
- Array & Off-by-One Gotchas
- C++ auto & Range-Based For Lessons
- C++ Virtual Destructor & Inheritance Gotchas
- C++ Type Conversion Lessons
- C++ Pass-by-Reference & Operator Gotchas
- Code Editor UI
- Float Precision Lessons
- C++ Integer Overflow Lessons
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
1. `Gotchas` - 84 edges
2. `AppState` - 39 edges
3. `Threading` - 38 edges
4. `ProgressStore` - 28 edges
5. `Concurrency` - 27 edges
6. `Exercise` - 26 edges
7. `Observability` - 24 edges
8. `_ExerciseController` - 23 edges
9. `Recursion` - 21 edges
10. `RunHandle` - 21 edges

## Surprising Connections (you probably didn't know these)
- `Lesson: Cutting Boilerplate with @dataclass` --semantically_similar_to--> `Exercise`  [INFERRED] [semantically similar]
  content/python/lessons/core_refresher_05_dataclasses.yaml → app/engine/exercise.py
- `/verify slash command` --references--> `test_loads_spring_content()`  [AMBIGUOUS]
  .claude/commands/verify.md → tests/test_lesson_engine.py
- `ExecutionEngine ABC` --conceptually_related_to--> `ExecutionEngine`  [EXTRACTED]
  .claude/skills/add-language-content/SKILL.md → app/execution/base.py
- `Required Property` --semantically_similar_to--> `Real-toolchain verification step`  [INFERRED] [semantically similar]
  content/spring/quiz/quiz_questions.yaml → .claude/skills/add-language-content/SKILL.md
- `contains_patterns structural gating` --conceptually_related_to--> `validate_contains()`  [EXTRACTED]
  .claude/skills/add-language-content/SKILL.md → app/engine/validator.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Dependency Injection Learning Progression** — content_spring_lessons_dependency_injection_01_field_injection_untestable_exercise, content_spring_lessons_dependency_injection_02_ambiguous_bean_no_qualifier_exercise, content_spring_lessons_dependency_injection_03_primary_bean_exercise, content_spring_lessons_dependency_injection_04_optional_dependency_exercise, content_spring_lessons_dependency_injection_05_constructor_injection_final_fields_exercise [INFERRED 0.85]
- **Bean Lifecycle Learning Progression** — content_spring_lessons_bean_lifecycle_01_missing_component_annotation_exercise, content_spring_lessons_bean_lifecycle_02_singleton_shared_state_exercise, content_spring_lessons_bean_lifecycle_03_postconstruct_initialization_exercise, content_spring_lessons_bean_lifecycle_04_predestroy_cleanup_exercise, content_spring_lessons_bean_lifecycle_05_lazy_initialization_exercise [INFERRED 0.85]
- **Field Injection Timing/Reflection Gotcha Pattern** — content_spring_lessons_dependency_injection_01_field_injection_untestable_exercise, content_spring_lessons_dependency_injection_05_constructor_injection_final_fields_exercise, content_spring_lessons_bean_lifecycle_03_postconstruct_initialization_exercise [INFERRED 0.75]
- **Configuration & Profiles learning progression** — content_spring_lessons_configuration_profiles_01_value_default_placeholder_exercise, content_spring_lessons_configuration_profiles_02_profile_specific_bean_exercise, content_spring_lessons_configuration_profiles_03_profile_negation_exercise, content_spring_lessons_configuration_profiles_04_environment_getproperty_exercise, content_spring_lessons_configuration_profiles_05_required_property_no_default_exercise [INFERRED 0.85]
- **Spring track documentation set** — claude_doc, readme_doc, docs_architecture_doc, docs_development_doc, concept_springengine [INFERRED 0.85]
- **Language content verification workflow** — _claude_commands_verify_command, _claude_skills_add_language_content_skill_skill, concept_real_toolchain_verification [INFERRED 0.80]
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
- **C++ Concurrency Learning Progression** — content_cpp_lessons_concurrency_async_01_race_condition_mutex_exercise, content_cpp_lessons_concurrency_async_02_atomic_counter_exercise, content_cpp_lessons_concurrency_async_03_future_async_exercise, content_cpp_lessons_concurrency_async_04_thread_join_missing_exercise, content_cpp_lessons_concurrency_async_05_promise_future_signal_exercise [INFERRED 0.85]
- **Modern C++ Idioms Progression** — content_cpp_lessons_core_refresher_01_range_based_for_exercise, content_cpp_lessons_core_refresher_02_auto_type_deduction_exercise, content_cpp_lessons_core_refresher_03_lambda_expression_exercise, content_cpp_lessons_core_refresher_04_smart_pointer_unique_ptr_exercise, content_cpp_lessons_core_refresher_05_structured_bindings_exercise [INFERRED 0.85]
- **STL Container Selection Progression** — content_cpp_lessons_data_structures_01_sort_vector_exercise, content_cpp_lessons_data_structures_02_unordered_map_lookup_exercise, content_cpp_lessons_data_structures_03_deque_front_operations_exercise, content_cpp_lessons_data_structures_04_set_for_uniqueness_exercise, content_cpp_lessons_data_structures_05_priority_queue_exercise [INFERRED 0.85]
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

## Communities (63 total, 21 thin omitted)

### Community 0 - "Categories, Languages & App State"
Cohesion: 0.05
Nodes (67): CategoryMeta, get_category_meta(), Display metadata (title, icon, color) for exercise categories, used by the…, get_language(), LanguageInfo, The set of language tracks the app knows about, and which ones have real…, AppState, Shared app state: settings, progress store, per-language exercise/quiz engines… (+59 more)

### Community 1 - "Concurrency & Async Lessons (Java/C++)"
Cohesion: 0.05
Nodes (75): Achievement: concurrency_async_master, Async, std::atomic, CompletableFuture, Concurrency, Daemon Threads, Debugging, ExecutorService (+67 more)

### Community 2 - "Execution Engine Contract & Exercise Model"
Cohesion: 0.05
Nodes (35): ABC, The Exercise data model. Content is data, not code -- see…, ExecutionEngine, ExecutionResult, Shared execution contract every per-language engine implements. Framing is…, Lets the UI cancel a run that's in progress (e.g. an infinite loop)., One concrete subclass per language track (python_engine.PythonEngine,…, exercise is unused by the single-file engines (Python/Java/C++) -- SpringEngine… (+27 more)

### Community 3 - "Data Structures & Algorithms Lessons"
Cohesion: 0.06
Nodes (65): Achievement: data_structures_master, Accumulator, Algorithms, Base Case, Collections, Comparator, Data Structures, HashMap (+57 more)

### Community 4 - "Functional Programming Lessons"
Cohesion: 0.06
Nodes (48): String Formatting, Function Composition, Functional Programming, Functional Programming Master (Achievement), Functools, Higher-Order Functions, Immutability, Lazy Evaluation (+40 more)

### Community 5 - "Spring Configuration & Profiles + Deployment Lessons"
Cohesion: 0.09
Nodes (46): configuration_profiles_master achievement, Configuration, Configuration & Profiles (Spring category), Deployment, Deployment Master (Achievement), Environment Abstraction, Environment-Specific Beans, Environment Variables (+38 more)

### Community 6 - "Progress Store & XP Leveling"
Cohesion: 0.08
Nodes (13): _level_from_xp(), _now(), PlayerLevel, ProgressStore, Path, SQLite-backed progress, gamification, and activity tracking -- one…, Returns True if newly awarded, False if already had it., Resets to 0 automatically once the exercise is passed -- powers the "keep… (+5 more)

### Community 7 - "Exercise Content Model & Category Logic"
Cohesion: 0.09
Nodes (10): Exercise, ExerciseEngine, Path, Loads one language track's exercises from YAML, kept separate from application…, category -> (done, total), done computed by the caller passing completed_ids in…, A small guided set for "today's refresher" -- round-robins the next unlocked,…, classes, dataclasses (+2 more)

### Community 8 - "Tooling Docs & Output Validator"
Cohesion: 0.09
Nodes (30): /verify slash command, add-language-content skill, CATEGORY_META dict (code), Exercise.spring_test_code field (code), Exercise validation: checks behavior/output, not exact code formatting., True if `code` contains every required pattern. Each pattern is matched as a…, Compares output, optionally substituting what the user typed into a template. -…, validate_contains() (+22 more)

### Community 9 - "Packaging Lessons"
Cohesion: 0.08
Nodes (36): Decorators, Entry Points, Functions, JAR Files, JAR Manifest, Module Api, Naming Conventions, Packaging (+28 more)

### Community 10 - "Error Translation & Lesson Screen UI"
Cohesion: 0.12
Nodes (13): extract_error_line_number(), _last_exception_type(), Translates raw interpreter/compiler output into concise, professional…, _translate_cpp_error(), translate_error(), _translate_java_error(), _translate_spring_error(), build_lesson_view() (+5 more)

### Community 11 - "Observability Lessons"
Cohesion: 0.11
Nodes (32): contextvars, Health Checks, Instrumentation, Logging, Metrics, Observability, Observability Master (Achievement), ThreadLocal (+24 more)

### Community 12 - "Dependency Management Lessons"
Cohesion: 0.11
Nodes (27): Classpath, Dependency Conflict Resolution, Dependency Management, Dependency Management Master (Achievement), importlib.metadata, Lock Files, Maven Coordinates, Reproducibility (+19 more)

### Community 13 - "Core Refresher Lessons (Java/C++)"
Cohesion: 0.13
Nodes (22): Achievement: core_refresher_master, Core Language Refresher (category), Functional Interfaces, Modern C++, Optional, RAII (Resource Acquisition Is Initialization), Records, Resource Management (+14 more)

### Community 14 - "Spring Bean Lifecycle & Scopes"
Cohesion: 0.16
Nodes (21): Bean Lifecycle, Bean Scope, Resource Cleanup, @Component Annotation, Initialization, Lazy Initialization, @PostConstruct, @PreDestroy (+13 more)

### Community 15 - "App Data Directory Resolution"
Cohesion: 0.18
Nodes (16): Path, Resolves the writable directory this app's data lives in -- a `data/` folder…, Returns <repo_root>/data, creating it if it doesn't exist yet., resolve_platform_data_dir(), get_data_dir(), get_db_path(), get_settings_path(), is_first_run() (+8 more)

### Community 16 - "Spring Dependency Injection"
Cohesion: 0.19
Nodes (19): Ambiguous Bean Resolution, Constructor Injection, Dependency Injection, Optional Dependency, @Primary Bean, @Qualifier, Testability, The Bean That Couldn't Be Unit Tested (+11 more)

### Community 17 - "Sync vs Async Lessons"
Cohesion: 0.18
Nodes (18): Asyncio, Context Managers, Generators, Sync Vs Async, timeouts, Lesson: Bounding How Long You'll Wait, with statement, Lesson: Turning Manual Cleanup into a Context Manager (+10 more)

### Community 18 - "Quiz Screen Controller"
Cohesion: 0.24
Nodes (4): Control, View, _QuizController, Button

### Community 19 - "Cross-Language Gotchas (Switch/Closures/Vectors)"
Cohesion: 0.15
Nodes (16): Closures, Fallthrough, Gotchas, Late Binding, Static Local Variables, switch Statement, std::vector, The Score Lookup That Crashed (+8 more)

### Community 20 - "Quiz Content Model"
Cohesion: 0.21
Nodes (7): Path, QuizEngine, Loads a language track's quiz questions from YAML. Adding a question means…, A freshly randomized set of questions for one quiz playthrough -- which…, QuizQuestion, The QuizQuestion data model. Quiz content is data, not code -- see…, Collection

### Community 21 - "Java equals()/hashCode() Gotchas"
Cohesion: 0.15
Nodes (13): Autoboxing, Equality, equals()/hashCode() Contract, HashSet, Identity, Integer Cache, Null Handling, java.util.Objects (+5 more)

### Community 22 - "Python Idioms & Static-Field Gotchas"
Cohesion: 0.17
Nodes (12): Idioms Gotchas Master Achievement, Idioms Gotchas Progress Achievement, Aliasing, Classes, Copying, Lists, Mutable Defaults, Static Fields (+4 more)

### Community 23 - "Python Collections Lessons"
Cohesion: 0.18
Nodes (11): Dictionaries, Iteration, Gotcha Gauntlet: The List That Changed While Being Read, collections module, Lesson: Grouping Without Manual Key Checks, counting, Lesson: Tallying with Counter, deque (+3 more)

### Community 24 - "Stdlib Deep Dive & Exception Handling Lessons"
Cohesion: 0.24
Nodes (10): Stdlib Deep Dive Master Achievement, Contextlib, Exceptions, finally Block, Reflection, Detecting an Optional Dependency Gracefully, Idioms & Gotchas: The finally Block That Ate the Return, What does Class.forName(name) throw if the class isn't on the classpath? (+2 more)

### Community 25 - "Array & Off-by-One Gotchas"
Cohesion: 0.29
Nodes (10): Arrays, Null, Off-by-One Error, Unsigned Integers, The Array Read That Went One Too Far, The Countdown Loop That Never Went Negative, Why can a loop like `for (size_t i = v.size() - 1; i >= 0; i--)` run forever or crash?, Why does `int arr[3]; ... arr[3]` compile and run instead of raising a clear error? (+2 more)

### Community 26 - "C++ auto & Range-Based For Lessons"
Cohesion: 0.32
Nodes (8): auto Type Deduction Keyword, Loops, Range-Based For Loop, Type Deduction, Index Loop to Range-Based For, Spelling Out a Type auto Could Deduce, What's the main advantage of a range-based for loop over an index-based one?, What does the `auto` keyword do in a variable declaration?

### Community 27 - "C++ Virtual Destructor & Inheritance Gotchas"
Cohesion: 0.43
Nodes (7): Gotcha Gauntlet Master Achievement, Destructors, Inheritance, Virtual Functions, The Destructor That Never Ran, Why does deleting a Derived object through a Base* pointer skip Derived's destructor when Base's destructor isn't virtual?, The Subclass That Forgot Its Parent

### Community 28 - "C++ Type Conversion Lessons"
Cohesion: 0.52
Nodes (7): Chars, Integer Division, Type Conversion, Integer Division Truncates Silently, The Digit Character That Wasn't a Digit, What does int / int produce in C++, even when assigned to a double?, What is the actual integer value of the char literal '7'?

### Community 29 - "C++ Pass-by-Reference & Operator Gotchas"
Cohesion: 0.43
Nodes (7): Operators, Pass By Reference, References, Pass-by-Value Silently Ignored the Caller, The if That Assigned Instead of Compared, Why doesn't a function taking `int x` (by value) modify the caller's variable?, What does `if (x = 1)` do, as opposed to `if (x == 1)`?

### Community 30 - "Code Editor UI"
Cohesion: 0.33
Nodes (5): make_code_editor(), make_read_only_code_block(), Control, A plain monospace multiline code editor -- no live syntax highlighting; Flet's…, TextField

### Community 31 - "Float Precision Lessons"
Cohesion: 0.50
Nodes (5): Decimal, Floats, Precision, The Price That Rounded the Wrong Way, 0.1 + 0.2 Is Not Quite 0.3

### Community 32 - "C++ Integer Overflow Lessons"
Cohesion: 0.70
Nodes (5): Integers, Overflow, The Overflow That Silently Wrapped, What actually happens when a signed int overflows past INT_MAX in C++ (on virtually all mainstream platforms)?, Gotcha Gauntlet: The Overflow That Never Threw an Error

### Community 33 - "Java Time/Duration Lesson"
Cohesion: 0.67
Nodes (3): Duration, java.time, Stdlib Deep Dive: Durations with java.time Instead of Raw Millis

### Community 34 - "Pathlib Lesson"
Cohesion: 0.67
Nodes (3): Filesystem, Pathlib, Paths as Objects, Not Strings

### Community 35 - "Comprehension Lesson"
Cohesion: 0.67
Nodes (3): comprehensions, lists, Lesson: Loop to Comprehension

## Ambiguous Edges - Review These
- `test_loads_spring_content()` → `/verify slash command`  [AMBIGUOUS]
  .claude/commands/verify.md · relation: references

## Knowledge Gaps
- **77 isolated node(s):** `run.sh script`, `coding-adventure`, `Achievement: concurrency_async_master`, `synchronized`, `futures` (+72 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **21 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `test_loads_spring_content()` and `/verify slash command`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **Why does `Gotchas` connect `Cross-Language Gotchas (Switch/Closures/Vectors)` to `Concurrency & Async Lessons (Java/C++)`, `Data Structures & Algorithms Lessons`, `Functional Programming Lessons`, `Spring Configuration & Profiles + Deployment Lessons`, `Packaging Lessons`, `Observability Lessons`, `Dependency Management Lessons`, `Spring Bean Lifecycle & Scopes`, `Spring Dependency Injection`, `Sync vs Async Lessons`, `Java equals()/hashCode() Gotchas`, `Python Idioms & Static-Field Gotchas`, `Python Collections Lessons`, `Stdlib Deep Dive & Exception Handling Lessons`, `Array & Off-by-One Gotchas`, `C++ Virtual Destructor & Inheritance Gotchas`, `C++ Type Conversion Lessons`, `C++ Pass-by-Reference & Operator Gotchas`, `Float Precision Lessons`, `C++ Integer Overflow Lessons`?**
  _High betweenness centrality (0.574) - this node is a cross-community bridge._
- **Why does `SpringEngine` connect `Execution Engine Contract & Exercise Model` to `Tooling Docs & Output Validator`?**
  _High betweenness centrality (0.291) - this node is a cross-community bridge._
- **Why does `Bean Lifecycle` connect `Spring Bean Lifecycle & Scopes` to `Tooling Docs & Output Validator`, `Spring Configuration & Profiles + Deployment Lessons`?**
  _High betweenness centrality (0.209) - this node is a cross-community bridge._
- **Are the 17 inferred relationships involving `AppState` (e.g. with `Settings` and `ExerciseEngine`) actually correct?**
  _`AppState` has 17 INFERRED edges - model-reasoned connections that need verification._
- **What connects `run.sh script`, `coding-adventure`, `Achievement: concurrency_async_master` to the rest of the system?**
  _77 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Categories, Languages & App State` be split into smaller, more focused modules?**
  _Cohesion score 0.054431960049937576 - nodes in this community are weakly interconnected._