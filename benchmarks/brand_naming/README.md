# Brand Naming Benchmark

This suite provides versioned founder cases for comparing:

1. a strong direct-LLM baseline;
2. a role-based multi-agent baseline;
3. the Project Origin structured pipeline.

`cases.json` contains inputs and evaluation constraints, not preferred answers.
Outputs should be evaluated blind so the evaluator does not know which approach
produced them.

Every approach must serialize results as `BrandNamingBenchmarkOutput`. Objective
checks such as candidate count and forbidden-term violations are evaluated
without an LLM judge. Subjective strategic quality will use a separate blinded
human rubric.

The benchmark also computes case-aware naming calibration metrics without an
LLM judge. These metrics use each case's required qualities, known bad
patterns, candidate evaluation traces, and score margins to flag outputs that
look acceptable but may be over-confident.

The same cases also define intent-quality expectations through:

- `expected_intent_signals`: evidence-backed concepts the interpreter should
  recover from the founder profile;
- `known_bad_patterns`: semantic traps that should not appear in outputs;
- `evaluation_rubric`: human-readable criteria for blinded review.

`ProjectOriginIntentRunner` executes the active rule-based interpreter and,
optionally, an LLM candidate in Shadow Mode. `evaluate_intent_quality` checks
strict concept coverage, relaxed concept coverage, evidence-hint coverage,
grounding against the original founder input, and known bad pattern violations.

The initial five cases validate the harness. Expand to at least 20 reviewed
cases before drawing product conclusions.

`ProjectOriginNamingRunner` executes these cases without an LLM and records
candidate names, the selected option, rationale, latency, and estimated model
cost. It also records candidate-level evaluation traces: component scores,
score weights, total score, and whether compiled naming knowledge influenced
the ranking. `ProjectOriginIntentRunner` records active baseline signals and
optional shadow LLM signals without changing the product path. Direct-LLM and
multi-agent runners remain to be implemented.

Run the current suite with deterministic mock LLM shadow comparison:

```bash
python research/run_brand_benchmark.py
```

The script writes `output/brand_benchmark_report.json`. Use
`--no-mock-llm` to measure only the active rule-based baseline.

Run an OpenAI shadow comparison when external API transmission is explicitly
approved:

```bash
python research/run_brand_benchmark.py --llm-provider openai --output output/brand_benchmark_report_openai.json
```

Recalculate metrics for an existing report without calling the provider again:

```bash
python research/run_brand_benchmark.py --reevaluate-report output/brand_benchmark_report_openai.json --output output/brand_benchmark_report_openai.json
```

Generate a blinded Markdown review packet for human scoring:

```bash
python research/run_brand_benchmark.py --reevaluate-report output/brand_benchmark_report_openai.json --output output/brand_benchmark_report_openai.json --markdown-output output/brand_blind_review.md
```

The Markdown report labels outputs as `Candidate Set A` and `Candidate Set B`
and places the approach mapping in an answer key at the end.

Planned metrics:

- hard constraint violations;
- strategic relevance;
- pronunciation and memorability;
- candidate diversity;
- consistency across repeated runs;
- intent concept coverage;
- relaxed intent concept coverage;
- intent evidence grounding;
- evidence and reasoning trace completeness;
- candidate-level evaluation trace completeness;
- naming knowledge guidance application rate;
- required quality coverage;
- known bad pattern risk;
- selected candidate risk score;
- low-confidence decision rate;
- score margin distribution;
- cost and latency.
