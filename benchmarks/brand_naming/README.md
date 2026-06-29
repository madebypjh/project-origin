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

The initial five cases validate the harness. Expand to at least 20 reviewed
cases before drawing product conclusions.

`ProjectOriginNamingRunner` executes these cases without an LLM and records
candidate names, the selected option, rationale, latency, and estimated model
cost. Direct-LLM and multi-agent runners remain to be implemented.

Planned metrics:

- hard constraint violations;
- strategic relevance;
- pronunciation and memorability;
- candidate diversity;
- consistency across repeated runs;
- evidence and reasoning trace completeness;
- cost and latency.
