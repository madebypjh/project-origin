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

The same cases also define intent-quality expectations through:

- `expected_intent_signals`: evidence-backed concepts the interpreter should
  recover from the founder profile;
- `known_bad_patterns`: semantic traps that should not appear in outputs;
- `evaluation_rubric`: human-readable criteria for blinded review.

`ProjectOriginIntentRunner` executes the active rule-based interpreter and,
optionally, an LLM candidate in Shadow Mode. `evaluate_intent_quality` checks
concept coverage, evidence-hint coverage, grounding against the original
founder input, and known bad pattern violations.

The initial five cases validate the harness. Expand to at least 20 reviewed
cases before drawing product conclusions.

`ProjectOriginNamingRunner` executes these cases without an LLM and records
candidate names, the selected option, rationale, latency, and estimated model
cost. `ProjectOriginIntentRunner` records active baseline signals and optional
shadow LLM signals without changing the product path. Direct-LLM and
multi-agent runners remain to be implemented.

Planned metrics:

- hard constraint violations;
- strategic relevance;
- pronunciation and memorability;
- candidate diversity;
- consistency across repeated runs;
- intent concept coverage;
- intent evidence grounding;
- evidence and reasoning trace completeness;
- cost and latency.
