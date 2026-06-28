# Naming Engine

## Purpose

The Naming Engine is responsible for generating original, pronounceable, strategy-aligned brand name candidates.

Project Origin should not rely only on LLMs to invent names.

Instead, Project Origin should generate candidate names through its own naming logic, then use AI to evaluate and rank them.

---

# Core Idea

Most AI naming tools follow this pattern:

```text
Prompt
↓
LLM
↓
Name candidates
```

Project Origin follows a different pattern:

```text
Founder Profile
↓
Brand Strategy
↓
Semantic Themes
↓
Morphology Selection
↓
Name Generation
↓
Phonetic Filtering
↓
AI Evaluation
↓
Ranking
↓
Final Recommendations
```

The LLM should act as a judge, not the only creator.

---

# Design Principle

> Generate broadly. Filter aggressively. Explain clearly.

The Naming Engine should create many possible names, remove weak candidates, and explain why the remaining names are strategically valuable.

---

# Core Pipeline

## 1. Input

Primary input:

* FounderProfile
* BrandStrategyReport
* Brand DNA
* Target Audience
* Differentiation
* Core Principles

---

## 2. Semantic Theme Detection

The system identifies dominant strategic themes.

Example themes:

* AI
* Trust
* Strategy
* Premium
* Health
* Finance
* Security
* Discovery
* Creativity
* Education

Themes determine which morphology pools should be used.

---

## 3. Morphology Selection

Each theme maps to a set of brand-friendly morphemes.

Example:

AI / Technology

* syn
* nex
* io
* ora
* logic
* meta

Trust

* veri
* true
* cred
* fide
* clear

Premium

* aure
* vel
* elle
* luxe
* oria

Strategy

* axis
* vector
* scope
* signal
* align

---

## 4. Name Generation

The generator combines selected morphemes into candidate names.

Example patterns:

```text
prefix + suffix
root + vowel ending
theme root + premium ending
trust root + tech suffix
```

Example outputs:

* Verion
* Lumora
* Synova
* Nexora
* Orivex
* Velion

The goal is to create names that feel original but still pronounceable.

---

## 5. Phonetic Filtering

Generated names are filtered using phonetic rules.

Reject names that:

* Are too short
* Are too long
* Have no vowels
* Have too many consonants in a row
* Have too many vowels in a row
* Are difficult to pronounce
* Look visually awkward

---

## 6. Candidate Deduplication

The system removes:

* Duplicate names
* Near-duplicate names
* Names with only minor spelling differences

---

## 7. AI Evaluation

The LLM evaluates candidates using brand strategy context.

Evaluation criteria:

* Meaning
* Memorability
* Pronunciation
* Strategic Alignment
* Scalability
* Emotional Impact
* Founder Intent Fit

The LLM should not generate the names at this stage.

It should evaluate and rank candidates created by the Naming Engine.

---

## 8. Ranking

Candidates are ranked using a combined score.

Possible scoring sources:

* Phonetic score
* Strategic fit score
* Memorability score
* LLM evaluation score
* Future domain availability score
* Future trademark risk score

---

## 9. Final Output

The final output should include exactly five recommended names.

Each recommendation must include:

* Name
* Meaning
* Strategic Fit
* Strengths
* Weaknesses
* Score
* Score Reason

---

# Future Enhancements

## Domain Availability

Check whether related domains are available.

Examples:

* `.com`
* `.io`
* `.ai`
* `.co`
* `.kr`

---

## Trademark Search

Future versions may integrate trademark search.

For Korea:

* KIPRIS

For global markets:

* USPTO
* EUIPO
* WIPO

---

## Language Risk Check

Check whether a name has negative meanings in major languages.

Priority languages:

* Korean
* English
* Japanese
* Chinese
* Spanish
* French

---

## Industry-Specific Naming

Different industries should use different naming logic.

Examples:

Healthcare

* vita
* cura
* bio
* med

Finance

* cred
* fort
* prime
* axis

AI

* syn
* nex
* ora
* meta

Luxury

* aure
* vel
* elle
* luxe

---

# Architecture

```text
naming/

phonetics.py
morphology.py
generator.py
evaluator.py
ranker.py
filters.py
```

---

# Module Responsibilities

## morphology.py

Defines morpheme libraries.

---

## phonetics.py

Defines pronunciation and readability rules.

---

## generator.py

Generates original candidate names.

---

## evaluator.py

Evaluates names using strategic and linguistic criteria.

---

## ranker.py

Ranks candidates by score.

---

## filters.py

Removes weak, duplicate, or risky candidates.

---

# MVP Scope

For the first version, the Naming Engine should support:

* Theme-based morphology selection
* Candidate generation
* Phonetic filtering
* Deduplication
* Top candidate output

Excluded from MVP:

* Domain checks
* Trademark checks
* Multilingual risk checks
* Full AI ranking
* Web interface

---

# Success Criteria

Naming Engine v1 is successful if it can:

* Generate at least 100 original candidates
* Remove clearly unpronounceable names
* Produce candidates that are not simple word combinations
* Reflect the founder profile's strategic themes
* Provide enough candidates for later AI evaluation

---

# Philosophy

A strong brand name should feel:

* New
* Pronounceable
* Memorable
* Strategically aligned
* Expandable

Project Origin should not merely ask AI to invent names.

Project Origin should build a system that invents, filters, evaluates, and explains.
