# Brand Domain Architecture

Version: 2.0

Status: Active

## Purpose

This document describes the first domain implementation of Project Origin. The
domain validates the Core contracts through Brand Strategy and naming
decisions.

The Brand package may depend on Core. Core must never depend on Brand.

## Current flow

```text
InterviewSession
    -> FounderProfile
    -> Intent Shadow Analysis
       |-> RuleBasedBrandIntentInterpreter (active baseline)
       `-> LlmBrandIntentInterpreter (non-authoritative candidate)
    -> KnowledgeBuilder / BrandKnowledge
    -> SemanticEngine / SemanticProfile
    -> BrandLanguageEngine / BrandLanguage
    -> NamingGenerator / NameCandidate[]
    -> NameFilterPipeline
    -> NameEvaluator
    -> NameRanker
    -> NamingDecisionService / DecisionResult
    -> PromptBuilder
    -> LLMProvider
    -> ReportValidator
    -> ReportParser / BrandStrategyReport
    -> MarkdownReportGenerator
```

## Package responsibilities

```text
project_origin/
|-- core/                  # Domain-neutral contracts
|-- brand/
|   |-- application.py     # Brand workflow orchestration
|   |-- models.py          # Brand-only models
|   |-- intent/            # Brand interpretation policy and implementations
|   |-- semantic/          # Meaning and theme extraction
|   |-- naming/            # Candidate generation and evaluation
|   |-- decision/          # Brand-to-Core adapters and decisions
|   |-- prompt_builder.py  # Brand report request construction
|   |-- validator.py       # Brand report schema validation
|   `-- markdown_report.py # Brand presentation
|-- llm/                   # Provider adapters
`-- main.py                # CLI entry point
```

### `project_origin.core`

Owns only domain-neutral decision contracts. It contains no Brand terminology,
prompt templates, provider clients, or report formatting.

### `project_origin.brand`

Owns founder interviews, Brand knowledge, semantic language, naming, report
schemas, and presentation.

### `project_origin.llm`

Provides replaceable text-generation adapters. Providers return text; domain
validators determine whether that text is acceptable.

### `research`

Collects and validates Brand Genome data, extracts patterns, and compiles
Brand-specific naming knowledge. It is not the Universal Knowledge Engine.

## Data model rule

Generated names remain `NameCandidate` objects from generation through ranking.
Downstream code must not reduce them to strings except at an external
serialization boundary.

## LLM boundary

The LLM may assist semantic judgment, critique, and report writing. It does not
own the system’s decision schema or validation rules.

All LLM report output must:

1. use the required JSON structure;
2. pass `ReportValidator`;
3. become a typed domain model before presentation.

## Known transitional gaps

- Brand models are not yet mapped into all Core contracts.
- Generator V2 does not yet consume all compiled naming knowledge.
- The naming path is mapped to Core contracts, but other Brand decisions are
  not.
- LLM intent interpretation is still non-authoritative Shadow output.
- Report prose is LLM-assisted, while its candidates and final recommendation
  are constrained by `DecisionResult`.
- The benchmark harness exists, but direct LLM, multi-agent, and blinded human
  comparison runs are not yet complete.

These are explicit migration targets, not reasons to put Brand logic into Core.
