# Core Architecture

Version: Alpha 0.2

---

## Purpose

Project Origin is not only a brand naming tool.

Project Origin is evolving into an AI Decision Engine Platform.

Brand naming is the first domain used to test and prove the core architecture.

---

## Core Idea

Project Origin should help humans make better decisions by transforming unclear intent into structured reasoning, domain knowledge, and explainable recommendations.

The long-term goal is not only to generate brand names.

The long-term goal is to build a reusable reasoning system.

---

## Current State

The current Brand Engine already contains early versions of the future Core.

```text
Founder Interview
        ↓
FounderProfile
        ↓
SemanticEngine
        ↓
SemanticProfile
        ↓
BrandLanguageEngine
        ↓
BrandLanguage
        ↓
NamingGenerator
        ↓
Evaluator
        ↓
Ranker
        ↓
Report
```

This works for the brand domain.

However, many components are still brand-specific.

---

## Future Core Structure

```text
User Input
        ↓
Intent Engine
        ↓
IntentProfile
        ↓
Knowledge Engine
        ↓
Reasoning Engine
        ↓
Decision Engine
        ↓
Domain Adapter
        ↓
Domain Output
```

---

## Core Components

### Intent Engine

Transforms raw human input into structured intent.

Current related components:

* InterviewSession
* FounderProfile
* SemanticEngine
* SemanticProfile

Future direction:

* Create a domain-neutral IntentProfile.
* Keep FounderProfile as a brand-specific input model.
* Convert FounderProfile into IntentProfile when needed.

---

### Knowledge Engine

Collects and provides relevant knowledge for reasoning.

Current related components:

* Brand Genome
* PatternExtractor
* KnowledgeCompiler
* NamingKnowledgeLoader

Future direction:

* Rename brand-specific knowledge components clearly.
* Treat Brand Knowledge as one knowledge source.
* Add other knowledge sources later:

  * Business Knowledge
  * Marketing Knowledge
  * Security Knowledge
  * Product Knowledge
  * User Memory

---

### Reasoning Engine

Combines intent and knowledge to produce structured reasoning.

Current status:

* Not yet fully implemented.

Current related components:

* PromptBuilder
* ReasoningFrameworks
* SemanticEngine

Future direction:

* Move reasoning out of prompts.
* Represent reasoning as structured data.
* Make reasoning reusable across domains.

---

### Decision Engine

Chooses the best strategic direction or recommendation.

Current status:

* Not yet implemented as a separate engine.

Current related components:

* NameEvaluator
* NameRanker
* ReportParser

Future direction:

* Separate evaluation from final decision.
* Create reusable decision models.
* Support trade-off analysis.

---

### Domain Adapter

Turns core reasoning into domain-specific outputs.

Current domain:

* Brand

Future domains:

* Product Strategy
* Business Strategy
* Security Strategy
* Marketing Strategy
* Naming
* Research Planning

---

## Brand as the First Domain

The current Brand Engine should not be discarded.

It should become the first domain implementation of Project Origin Core.

```text
Core
        ↓
Brand Domain
        ↓
Brand Strategy
        ↓
Naming Engine
        ↓
Brand Report
```

---

## What Should Move Later

### To Core

Potentially reusable components:

* SemanticProfile concept
* Intent extraction logic
* Reasoning framework structure
* Decision ranking logic
* LLM provider layer
* Validator patterns

---

### To Brand Domain

Brand-specific components:

* BrandLanguageEngine
* BrandLanguage
* NamingGenerator
* NameEvaluator
* NameRanker
* CandidateName
* Brand Genome
* Brand Research Pipeline
* Naming Knowledge

---

## Important Distinction

### Brand Knowledge

Brand-specific knowledge used to improve brand naming.

Examples:

* Naming patterns
* Brand Genome
* Phonetic patterns
* Industry naming styles

---

### Universal Knowledge Engine

A future core system that selects and provides knowledge from multiple domains.

Examples:

* Brand Knowledge
* Business Knowledge
* Security Knowledge
* Product Knowledge
* User Memory

---

## Migration Strategy

Do not move files immediately.

The current system works.

Instead:

1. Document the future structure.
2. Continue improving the Brand Engine.
3. Identify reusable abstractions.
4. Introduce `core/` only when the need becomes clear.
5. Move code gradually with tests.

---

## Design Principle

Brand Engine is not a detour.

Brand Engine is the first proof of the AI Decision Engine.

---

## Final Direction

Project Origin should evolve from:

```text
Brand Naming Tool
```

to:

```text
AI Decision Engine Platform
```

Brand naming remains the first and most important test case.

But the architecture must stay reusable beyond branding.
