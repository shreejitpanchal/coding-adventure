---
name: add-language-content
description: "Use when adding exercises or quiz questions to an existing language track (content/<language>/lessons/*.yaml, content/<language>/quiz/quiz_questions.yaml), or when standing up a brand-new language track (new ExecutionEngine + content directory) in Coding Adventure. Encodes the repeatable schema, category/level conventions, the mandatory real-toolchain verification step, and every place that needs updating so a fresh clone doesn't have to rediscover these the hard way."
---

# Adding language content to Coding Adventure

Content lives entirely under `content/<language>/lessons/*.yaml` (one file
per exercise) and `content/<language>/quiz/quiz_questions.yaml`. This is
data, not code — adding or changing an exercise never requires an app-code
change, since `ExerciseEngine`/`QuizEngine` re-glob the directory on next
load.

## 1. Decide the scope

- **New exercises in an existing category**: add more YAML files with the
  next `category_level` in that category. No app-code change needed.
- **New category in an existing language**: same — `ExerciseEngine.
  categories()` derives the category *list* purely from what's present in
  that language's content directory. Add a `CATEGORY_META` entry (step 5)
  for a proper title/icon/color; without one it still works, just falls
  back to `DEFAULT_META`.
- **Brand-new language track** (the Spring-sized job): needs a new
  `ExecutionEngine` subclass in `app/execution/`, toolchain detection
  wired into `toolchain_check.py`, `app/engine/languages.py` flipped to
  `available=True`, and a first content batch. See step 8.

## 2. Category parity is a choice, not a rule

Python and Java deliberately share the exact same 14 category keys
(`idioms_gotchas`, `core_refresher`, `data_structures`, `stdlib_deep_dive`,
`concurrency_async`, `thread_scheduling`, `sync_vs_async`,
`functional_programming`, `recursion`, `dependency_management`,
`packaging`, `deployment`, `observability`, `gotcha_gauntlet`) so
switching between those two tracks doesn't change the shape of the app.
That parity is **not enforced by the engine** — nothing hardcodes which
categories a language "should" have. C++ deliberately ships its own
smaller 6-category set (`idioms_gotchas`, `core_refresher`,
`data_structures`, `stdlib_deep_dive`, `concurrency_async`,
`gotcha_gauntlet`) because categories like packaging/deployment/
observability are ecosystem/tooling concepts that fit a package manager
or framework better than bare C++ language/stdlib content. When adding a
new language, decide deliberately whether to chase the 14-category parity
list or define a smaller set that actually fits the language/framework —
don't assume parity is required.

The flagship **Gotcha Gauntlet** debug-puzzle track
(`app/engine/categories.GOTCHA_CATEGORY`) is expected in every language
that has one — it's just a category like any other, but gets its own
top-level card in the track hub.

## 3. The exercise YAML schema

Copy an existing file in the target language (or the closest sibling
language) as a template. Required fields: `id`, `title`, `language`,
`level` (global, unique-ish ordering hint — not load-bearing the way the
kids app's cross-category `level` is; category browsing uses
`category_level` instead), `objective`, `explanation`, `example_code`,
`starter_code`, `challenge`, `expected_output` (or `expected_output_pattern`
for genuinely non-deterministic output), `hints`, `xp_reward`,
`achievement` (`null` except on the **last** `category_level` in a
category — see below), `category`, `category_level` (1-based position
within category), `difficulty` (`warmup|core|gotcha|deep_dive`, purely
descriptive), `contains_patterns` (list of regexes checked against raw
submitted source — see step 4), `concept_tags` (free-form list, no fixed
vocabulary to keep in sync, unlike the kids app).

Filename convention: `<category>_<NN>_<short_desc>.yaml` where `NN` is the
zero-padded `category_level`. `id` convention: `<category>_<NN>` (no
language prefix — language is its own directory and YAML field).

`achievement` naming convention: `<category>_master`, set only on the
exercise whose `category_level` is the last one in that category (e.g. 5
of 5). **This has been miskeyed before** — double check it's on the last
file, not accidentally one level early.

## 4. `contains_patterns` — structural gating, use it when needed

Some exercises are "refactor" style rather than "fix a crash": the buggy
starter already produces the *correct* output, so `expected_output`
alone can't gate completion — a submission that just resubmits the
unmodified starter would silently pass. `contains_patterns` is a
language-agnostic (plain regex over raw source, not an AST check) way to
require the specific construct the exercise is actually teaching (e.g.
requiring `std::sort` so a hand-rolled bubble sort that happens to produce
the right output doesn't count). Every "replace X with Y" style exercise
in this codebase uses this pattern — check a same-category sibling file
for the shape.

## 5. `CATEGORY_META` (only for a genuinely new category key)

`app/engine/categories.py`'s `CATEGORY_META` is **one flat dict shared
across every language** — "Concurrency & Async" means the same thing
whether it's filled with Python, Java, or C++ content, so it is not
namespaced per language. Add `title`/`icon`/`color` once; every language
that uses that category key picks it up automatically.

## 6. Quiz bank

A standalone multiple-choice bank per language
(`content/<language>/quiz/quiz_questions.yaml`), loaded by `QuizEngine`.
Schema: top-level `questions:` list, each with `id` (`qNN`, sequential),
`question`, `options` (list of 4), `correct` (0-based index), `explanation`,
`concept_tags` (should overlap with the exercises' tags it's meant to
reinforce — quiz results link back to related exercises via shared tags).
Match the density already established for sibling languages (roughly one
question per taught concept — Python has 87, Java 70, C++ 35 for its
smaller category set) rather than a fixed count.

## 7. Verify before finalizing — against the REAL local toolchain

This is the most important step and has caught real bugs every time it's
been skipped. For every new/changed exercise:

1. Write out the "fixed" solution code for the exercise (the
   `challenge`-solved version, not the starter).
2. Run it through the real engine for that language
   (`app.execution.<language>_engine.<Lang>Engine().run(code)`), not a
   guess at what the output would be.
3. Assert `result.success`, that `result.stdout` matches
   `expected_output` (or `expected_output_pattern`), and that
   `contains_patterns` matches against the solution source.
4. Separately run the **unedited starter code** through the same engine
   and confirm it does *not* silently pass validation — it should fail
   via wrong output, a runtime error, a timeout, OR (for refactor-style
   exercises) fail the `contains_patterns` check even if output already
   happens to be correct.

A throwaway verification script (build a `SOLUTIONS: dict[str, str]`
keyed by exercise id, loop over the YAML files, run both starter and
solution through the engine) is the fastest way to do this in bulk — see
git history for the C++ track's addition for the exact pattern. Toolchain
gotchas seen so far: Java/C++ crash messages sometimes don't match the
first regex you'd guess (verify the *actual* stderr text, don't assume);
unsigned-integer wraparound loops can time out instead of crashing
depending on the platform — write the exercise's explanation to match
what the sandbox actually observes, not what you'd expect in the
abstract.

Then run `/verify` (full suite + launch check).

## 8. New language track only

- Implement `app/execution/<language>_engine.py` following the
  `ExecutionEngine` ABC (`run(code, timeout, handle, stdin_text) ->
  ExecutionResult`). Gate it with `check_toolchain(language)` at the top
  of `run()` so a missing compiler/runtime returns a `blocked`
  `ExecutionResult` with an install hint instead of crashing.
- Add the toolchain's binaries to `app/execution/toolchain_check.py`.
- Add a `translate_error()` branch and friendly-message table in
  `app/execution/errors.py` for that language's error output shape.
- Flip `available=True` for the language in `app/engine/languages.py`
  once content exists (keep it `False` while only the engine interface
  is defined — a "coming soon" card that then silently does nothing on
  Run is worse than an honest "not built yet").
- Add `tests/test_execution_<language>.py` mirroring the existing
  per-language execution tests, `pytest.mark.skipif`'d on the toolchain
  binaries being missing from PATH.
- Add a `test_loads_<language>_content` case to
  `tests/test_lesson_engine.py` asserting the exercise/category counts.
- Update `README.md`, `CLAUDE.md`, `docs/DEVELOPMENT.md`, and
  `docs/ARCHITECTURE.md` — grep them for the language's name first; they
  describe stub/scaffolded languages explicitly (e.g. "interface defined,
  raises NotImplementedError") and need that language flipped to
  "implemented" in every place it's mentioned, including the Mermaid
  diagrams in ARCHITECTURE.md.
- Run `/graphify` (or the graphify skill's `--update` flow) afterward so
  the knowledge graph picks up the new engine/content — it's incremental
  and only re-extracts changed files.
