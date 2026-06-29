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
|-- core/          # Domain-neutral decision contracts
|-- brand/         # Brand domain implementation
|   |-- naming/
|   `-- semantic/
|-- llm/           # Replaceable provider adapters
`-- main.py        # Brand CLI entry point

research/           # Brand research and knowledge compilation
dataset/            # Versioned research assets
tests/              # Automated verification
```

Core must never import Brand, Recon, or another domain.

## Current state

Implemented:

- Brand founder interview and structured profile
- Semantic and Brand Language pipelines
- Structured name candidate generation, filtering, evaluation, and ranking
- Brand research, validation, pattern extraction, and knowledge compilation
- Provider-independent LLM adapter
- JSON validation and Markdown report rendering
- Initial domain-neutral Core contracts

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

Run the deterministic naming benchmark with the same source path:

```powershell
$env:PYTHONPATH = "src"
.\venv\Scripts\python.exe -m research.benchmark
```

## Documentation order

1. `docs/00_PROJECT_ORIGIN_MASTER_CONTEXT.md`
2. `docs/adr/ADR-001-core-domain-separation.md`
3. `docs/adr/ADR-002-product-driven-core-evolution.md`
4. `docs/16_core_architecture.md`
5. `docs/12_architecture.md`
6. Domain and product specifications

When documents disagree, the Master Context and accepted ADRs take precedence.

## Standard

The project must prove that its structured pipeline improves decision quality,
consistency, explainability, or accumulated knowledge over a strong direct-LLM
or multi-agent baseline. Architecture alone is not evidence of value.
