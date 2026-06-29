# Project Origin

> Reveal What Matters.

Project Origin is an explainable AI Decision Engine Platform. It transforms
human intent and domain knowledge into structured reasoning and traceable
decisions.

Brand Strategy is the first product and validation domain. It is not the final
scope of the platform.

## Development principle

Project Origin is **product-driven and Core-aware**:

- Product evidence determines what to build next.
- Core contracts define dependency boundaries from the beginning.
- Reusable implementations move into Core only after real domain validation.
- LLMs are replaceable assistants, not owners of the decision contract.

## Architecture

```text
Human Input
    -> IntentProfile
    -> KnowledgePacket
    -> ReasoningTrace
    -> DecisionOption[]
    -> DecisionResult
    -> Domain Output
```

Current source layout:

```text
src/project_origin/
|-- core/          # Domain-neutral decision and intent contracts
|   `-- intent/    # Signals, interpreter protocol, validation, normalization
|-- brand/         # Brand domain implementation
|   |-- intent/    # Brand policy, LLM/rule interpreters, Shadow Mode
|   |-- naming/
|   `-- semantic/
|-- llm/           # Replaceable provider adapters
`-- main.py        # Brand CLI entry point

research/           # Brand research and knowledge compilation
dataset/            # Versioned research assets
benchmarks/         # Versioned cross-approach evaluation cases
tests/              # Automated verification
```

Core must never import Brand, Recon, or another domain.

## Current state

Implemented:

- Brand founder interview and structured profile
- Semantic and Brand Language pipelines
- Structured name candidate generation, filtering, evaluation, and ranking
- Brand-to-Core adapters and an explainable Naming Decision Service
- Brand research, validation, pattern extraction, and knowledge compilation
- Provider-independent LLM adapter
- JSON validation and Markdown report rendering
- Initial domain-neutral Core contracts
- Initial Brand naming benchmark cases and objective constraint metrics
- Deterministic Project Origin runner for the Brand naming benchmark
- Evidence-backed LLM Intent Interpreter running behind a Shadow Mode flag
- Experimental intent-shadow naming path available behind an environment flag

Not yet implemented as complete engines:

- Structured Reasoning Engine
- Decision Engine
- Memory Engine
- Cross-domain benchmark

## Running tests

```powershell
.\venv\Scripts\python.exe -m pytest -q
```

## Running the Brand CLI

Create a local `.env` containing `OPENAI_API_KEY`, then run:

```powershell
$env:PYTHONPATH = "src"
.\venv\Scripts\python.exe -m project_origin.main
```

Generated reports are written to `output/` and are intentionally not versioned.

Enable LLM intent interpretation in non-authoritative Shadow Mode:

```powershell
$env:PROJECT_ORIGIN_INTENT_SHADOW = "true"
```

Shadow output is written to `output/intent_shadow.json`. By default, the naming
pipeline continues to use the rule-based semantic path.

Run the experimental intent-shadow naming path, equivalent to the benchmark's
Candidate Set B:

```powershell
$env:PROJECT_ORIGIN_NAMING_PATH = "intent_shadow"
```

This option uses LLM-interpreted intent to build Brand Language before naming.
It is still experimental and should be compared against benchmark evidence
before becoming the default.

Run the deterministic naming benchmark with the same source path:

```powershell
$env:PYTHONPATH = "src"
.\venv\Scripts\python.exe -m research.benchmark
```

## Documentation order

1. `docs/00_PROJECT_ORIGIN_MASTER_CONTEXT.md`
2. `docs/adr/ADR-001-core-domain-separation.md`
3. `docs/adr/ADR-002-product-driven-core-evolution.md`
4. `docs/adr/ADR-003-llm-assisted-intent-interpretation.md`
5. `docs/16_core_architecture.md`
6. `docs/12_architecture.md`
6. Domain and product specifications

When documents disagree, the Master Context and accepted ADRs take precedence.

## Standard

The project must prove that its structured pipeline improves decision quality,
consistency, explainability, or accumulated knowledge over a strong direct-LLM
or multi-agent baseline. Architecture alone is not evidence of value.
