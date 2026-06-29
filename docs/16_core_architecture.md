# Core Architecture

Version: Alpha 0.4

Status: Active

## Purpose

Project Origin Core defines reusable contracts for explainable decisions. It
does not attempt to be a complete universal reasoning engine before product
evidence exists.

## Dependency rule

```text
Brand ----\
Recon -----+--> Core
Future ---/

Core -X-> any domain
```

Provider clients and presentation formats are infrastructure concerns. Brand
knowledge and naming concepts are domain concerns.

## Current Core contracts

### `IntentProfile`

Captures a domain-neutral objective, constraints, preferences, and context.
`FounderProfile` remains a Brand model and may later be adapted into this
contract.

### `IntentSignal`

Captures an open-ended intent concept with a general kind, normalized weight,
source evidence, confidence, and optional metadata. Core does not define a
Brand-specific semantic taxonomy.

### Intent interpretation contracts

`IntentInterpreter` is provider-independent. `IntentNormalizer` merges and
normalizes concepts, while `IntentValidator` rejects evidence not grounded in
the source input. LLM provider usage belongs to infrastructure or a domain
implementation, never Core.

### `KnowledgeItem` and `KnowledgePacket`

Represent sourced knowledge selected for a decision. Brand Genome and naming
patterns are Brand knowledge sources, not universal Core knowledge.

### `ReasoningStep` and `ReasoningTrace`

Represent claims, rationales, evidence, assumptions, uncertainty, and
confidence as inspectable data.

### `DecisionOption`

Represents one comparable alternative with explicit scores, strengths,
weaknesses, and metadata.

### `DecisionResult`

References one selected option and preserves the complete trace, rationale,
confidence, and warnings.

## What Core does not currently contain

- a universal prompt builder;
- an LLM-specific provider abstraction;
- a Brand-specific intent taxonomy;
- Brand naming or report models;
- a completed Reasoning Engine;
- a completed Decision Engine;
- speculative adapters for future domains.

This absence is intentional. Contracts come first; generalized implementations
require evidence.

## Evolution strategy

1. Define the smallest stable contract required by a real product decision.
2. Implement the behavior in the domain.
3. Benchmark quality, consistency, evidence, cost, and latency.
4. Identify reuse in a second use case or domain.
5. Promote only the proven reusable implementation into Core.
6. Preserve tests at both the Core and domain boundaries.

## Brand relationship

Brand is the first validation domain:

```text
FounderProfile
    -> Brand decision adapter
    -> IntentProfile

BrandKnowledge
    -> Brand decision adapter
    -> KnowledgePacket

NameCandidate
    -> Brand decision adapter
    -> DecisionOption
```

These adapters are implemented for the first structured Brand naming decision.
They preserve Brand-specific information in domain records and option metadata.
Other Brand decisions should add adapters only when their contracts are proven.

## Agents and LLMs

Agents and LLMs are replaceable workers that may research, critique, or write.
Core owns the contracts needed to verify and retain their work.

A multi-agent workflow is not itself a Decision Engine unless it produces
validated evidence, options, reasoning traces, and a final decision record.

## Success criterion

Core is valuable only when it improves measurable decision behavior or is
demonstrably reused. A larger abstraction surface is not progress by itself.
