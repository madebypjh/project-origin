# Project Origin Master Context

Version: Alpha 0.7
Status: Active  
Authority: Single source of truth

Every contributor and AI assistant must read this document before making
architectural decisions.

## 1. Identity

Project Origin is not a Brand Naming AI.

Project Origin is an **explainable AI Decision Engine Platform**. It aims to:

1. understand human intent;
2. retrieve and validate relevant knowledge;
3. produce structured reasoning;
4. compare explicit decision options;
5. return an explainable domain-specific result.

Brand Strategy is the first product and validation domain. ReconOS is a future
Security product implemented as another domain on the same Core.

## 2. Product-driven, Core-aware

Product evidence determines development priority. Core principles determine
architectural boundaries.

Project Origin therefore follows these rules:

- Define the minimum domain-neutral Core contracts early.
- Build concrete behavior against real Brand use cases.
- Promote implementations into Core only after reuse is demonstrated.
- Do not build a universal engine from hypothetical future requirements.
- Do not let working Brand shortcuts leak domain concepts into Core.

This replaces both unrestricted “Core First” abstraction and “Engine Later”
architecture drift.

## 3. Non-negotiable principles

### 3.1 Explainability

Every important decision must identify its intent, evidence, alternatives,
trade-offs, rationale, uncertainty, and confidence where available.

### 3.2 Data is a first-class asset

Research data must be versioned, normalized, validated, and benchmarked.
Research quality is held to the same standard as code quality.

### 3.3 Provider independence

No domain decision contract may depend on OpenAI, Anthropic, Google, or another
specific model provider.

### 3.4 LLMs assist; Project Origin owns the decision contract

LLMs may help expand meaning, critique reasoning, identify omissions, and write
reports. Their output must pass structured contracts and validation.

The long-term direction is to use deterministic or measurable components where
they are reliable, while retaining LLMs where semantic judgment adds value.

### 3.5 Single responsibility and dependency direction

```text
Infrastructure -> Core contracts
Domain         -> Core contracts
Core           -X-> Domain
```

Core must never import Brand, Recon, or another domain.

## 4. Target architecture

```text
Human Input
    -> Intent Engine
    -> IntentProfile
    -> Knowledge Engine
    -> KnowledgePacket
    -> Reasoning Engine
    -> ReasoningTrace
    -> Decision Engine
    -> DecisionOption[] / DecisionResult
    -> Domain Adapter
    -> Domain Output
```

Agents and LLM providers may participate inside engines as replaceable workers.
They do not replace the contracts, evidence, validation, or final decision
record.

## 5. Core contracts

The minimum Core vocabulary is:

- `IntentProfile`: domain-neutral representation of a desired outcome.
- `IntentSignal`: an open-ended concept with kind, weight, source evidence, and
  confidence.
- `KnowledgeItem`: one sourced unit of relevant knowledge.
- `KnowledgePacket`: knowledge selected for one decision context.
- `ReasoningStep`: one claim with rationale, evidence, and confidence.
- `ReasoningTrace`: ordered reasoning, assumptions, and uncertainty.
- `DecisionOption`: one comparable alternative with scores and trade-offs.
- `DecisionResult`: selected option, complete rationale, trace, and warnings.

Core contracts are stable boundaries. Complete universal engine
implementations are not assumed to exist yet.

## 6. Domain architecture

```text
Project Origin Core
|-- Brand domain
|-- Recon domain
|-- Business domain
|-- Product domain
`-- Future domains
```

Domains may have their own:

- input models and workflows;
- knowledge and policies;
- generators and evaluators;
- adapters and reports.

Only validated Core contracts and implementations are shared. It is not assumed
that only a single adapter changes between domains.

## 7. Brand domain

Current flow:

```text
Interview
    -> FounderProfile
    -> BrandKnowledge
    -> SemanticProfile
    -> BrandLanguage
    -> NameCandidate[]
    -> Filters
    -> Evaluator
    -> Ranker
    -> LLM-assisted Brand Report
```

Brand models remain in `project_origin.brand`. In particular,
`FounderProfile`, `BrandKnowledge`, `BrandLanguage`, and `NameCandidate` are not
Core models.

Generated names are structured `NameCandidate` objects throughout the pipeline,
not untyped strings.

## 8. Research and knowledge

```text
Brand Collector
    -> Brand Analyzer
    -> Normalizer
    -> Validator
    -> Genome Builder
    -> Pattern Extractor
    -> Brand Knowledge Compiler
    -> Brand Knowledge Loader
```

Brand knowledge is one domain knowledge source. It must not be presented as the
future Universal Knowledge Engine.

## 9. Current implementation state

Implemented:

- Brand Interview, Semantic, and Brand Language pipelines
- Structured naming candidate pipeline
- Rule-based filtering, evaluation, and ranking
- Brand-to-Core adapters for naming decisions
- Explainable rule-based Naming Decision Service
- Brand research and knowledge compilation pipeline
- Provider-independent LLM adapter
- JSON validation and Markdown report rendering
- Initial Core decision contracts
- Initial versioned Brand naming benchmark harness and Project Origin runner
- Core Intent Interpreter contract, evidence validator, and normalizer
- Brand LLM Intent Interpreter with rule-based fallback and Shadow Mode

In progress or not yet complete:

- Generator V2 knowledge integration
- evaluation and eventual promotion of LLM intent interpretation
- broader structured Reasoning Engine beyond naming selection
- Decision Engine
- completed comparison against direct LLM and multi-agent baselines
- Memory Engine

Documentation describes direction; automated tests and executable code determine
whether a feature is actually implemented.

## 10. Current priorities

1. Evaluate Shadow Mode intent quality, grounding, stability, cost, and latency.
2. Expand and review the Brand benchmark cases.
3. Implement direct-LLM and multi-agent benchmark runners.
4. Integrate validated intent and Brand knowledge into Generator V2 only after
   benchmark evidence.
5. Add blinded human evaluation for subjective decision quality.

## 11. Proof of value

Project Origin must demonstrate measurable improvement in at least one of:

- decision quality;
- consistency across repeated runs;
- evidence accuracy and trace completeness;
- learning from accumulated knowledge;
- provider independence;
- reuse across a second domain;
- cost or latency at comparable quality.

If a strong direct prompt or multi-agent workflow performs equally well with
less complexity, additional abstraction is not justified.

## 12. Documentation authority

When documents conflict, use this order:

1. Master Context
2. Accepted ADRs
3. Active architecture specifications
4. Domain specifications
5. Product roadmap and PRD
6. README
7. Generated outputs

Major architectural changes require an ADR and then an update to this document.

## 13. Final direction

Project Origin evolves from a Brand Naming Tool into an explainable AI Decision
Engine Platform by proving each reusable abstraction through real products.

Do not optimize only for Brand. Do not generalize without evidence. Build
valuable domain decisions on explicit, reusable contracts.
