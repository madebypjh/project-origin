# Brand Language

> Transition note: the fixed theme taxonomy in this document describes the
> deterministic baseline. Project Origin now also runs an evidence-backed,
> open-ended LLM Intent Interpreter in non-authoritative Shadow Mode. The
> baseline remains active until benchmark evidence supports promotion.

## Purpose

Brand names should not begin with words.

They should begin with meaning.

The purpose of the Brand Language Engine is to transform a founder's intent into a semantic language that the Naming Engine can understand.

Rather than generating names directly from interview answers, Project Origin first builds an internal Brand Language.

That language becomes the foundation for every generated name.

---

# Philosophy

Names are compressed meaning.

A strong brand name is not simply a collection of letters.

It is the smallest possible representation of a much larger idea.

Project Origin therefore models meaning before generating names.

---

# Overall Pipeline

```text
Founder Interview
        │
        ▼
Founder Intent
        │
        ▼
Brand Strategy
        │
        ▼
Brand Language
        │
        ▼
Morphology Selection
        │
        ▼
Name Generation
        │
        ▼
Evaluation
```

---

# Brand Language

Brand Language is an internal semantic representation of a brand.

It is not shown directly to the user.

Instead, it guides every downstream decision.

---

# Semantic Expansion

Interview answers are expanded into richer concepts.

Example

Founder Input

```text
Truth
```

Brand Language

```text
Truth

Integrity

Honesty

Transparency

Authenticity

Reliability

Confidence

Precision
```

Another example

Founder Input

```text
AI
```

Brand Language

```text
Reasoning

Knowledge

Inference

Decision

Learning

Logic

Pattern

Automation

Structure

Intelligence
```

The goal is to capture meaning rather than words.

---

# Semantic Categories

Every expanded concept belongs to one or more semantic categories.

Examples

## Trust

Integrity

Reliability

Confidence

Authenticity

Transparency

Safety

Verification

---

## Intelligence

Reasoning

Learning

Knowledge

Logic

Inference

Analysis

Thinking

Decision

---

## Innovation

Future

Vision

Discovery

Creation

Transformation

Possibility

Experimentation

Novelty

---

## Premium

Luxury

Elegance

Craftsmanship

Quality

Timelessness

Sophistication

Prestige

Refinement

---

## Strategy

Direction

Planning

Focus

Structure

Alignment

Execution

Priority

Framework

---

# Theme Extraction

The engine identifies dominant themes.

Example

Founder answers

```text
AI

Reasoning

Quality

Truth
```

↓

Detected themes

```text
Technology

Trust

Strategy
```

↓

Theme weights

```text
Technology : 0.45

Trust : 0.35

Strategy : 0.20
```

These weights influence morphology selection.

---

# Morphology Mapping

Themes map to different morphology pools.

Technology

```text
syn

nex

io

ora

logic

meta
```

Trust

```text
ver

cred

true

fide

clar
```

Premium

```text
aure

vel

elle

oria

lux
```

Strategy

```text
axis

vector

scope

align

signal
```

The Naming Engine uses weighted selection instead of random selection.

---

# Brand Vocabulary

The Brand Language Engine produces a vocabulary.

Example

```text
Precision

Insight

Structure

Signal

Trust

Decision

Future

Vision

Logic

Framework
```

This vocabulary becomes the semantic DNA of the brand.

---

# Design Principles

Meaning before words.

Language before morphology.

Strategy before aesthetics.

Evaluation before recommendation.

---

# Why This Matters

Most AI naming tools work like this

```text
Prompt

↓

LLM

↓

Names
```

Project Origin works differently.

```text
Founder

↓

Meaning

↓

Language

↓

Morphology

↓

Names

↓

Evaluation
```

The LLM becomes an evaluator rather than the only creative engine.

---

# Future Enhancements

Future versions may include:

* Semantic Graphs
* Knowledge Graph Expansion
* Industry-specific vocabularies
* Multilingual semantic mapping
* Emotional language modeling
* Cultural language adaptation

---

# Success Criteria

Brand Language v1 is successful if it can:

* Expand founder intent into richer concepts.
* Detect strategic themes.
* Produce a reusable semantic vocabulary.
* Guide morphology selection.
* Improve the originality and relevance of generated names.

---

# Philosophy

The best brand names are not invented from letters.

They are discovered from meaning.

Project Origin therefore builds meaning first, and names second.
