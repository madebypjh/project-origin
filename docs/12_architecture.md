# Project Origin Architecture

> **Design the reasoning. Not the answer.**

Version: 1.0

---

# Purpose

This document defines the core architecture of Project Origin.

The objective is not to describe implementation details.

The objective is to define responsibilities.

Every module should have one responsibility.

Every layer should be replaceable.

---

# Core Philosophy

Project Origin is **not an AI naming generator.**

Project Origin is an **AI Decision Intelligence System.**

The AI model is not the product.

The reasoning process is the product.

The report is the product delivered to users.

---

# Design Principles

## Single Responsibility

Each module has exactly one responsibility.

No module should perform multiple unrelated tasks.

---

## Provider Independence

The system must never depend on a specific LLM.

OpenAI is one provider.

Claude is one provider.

Gemini is one provider.

The architecture must support replacing providers without changing business logic.

---

## Framework First

Business reasoning should never be hardcoded.

Instead, reasoning should be expressed as reusable strategic frameworks.

Examples:

* Golden Circle
* Brand DNA
* Positioning
* Brand Archetypes
* Value Proposition
* Naming Evaluation

---

## Output First

The user's experience is the report.

Everything exists to produce a higher-quality report.

---

# High-Level Architecture

```text
Founder Interview
        │
        ▼
FounderProfile
        │
        ▼
PromptBuilder
        │
        ▼
Reasoning Frameworks
        │
        ▼
LLM Provider
        │
        ▼
JSON Validator
        │
        ▼
Report Parser
        │
        ▼
Brand Strategy Report
        │
        ▼
Markdown Template
        │
        ▼
PDF Report
```

---

# Module Responsibilities

## interview.py

Responsibility

Collect founder information.

Output

FounderProfile

Never performs reasoning.

---

## models.py

Responsibility

Define domain models.

Contains:

* FounderProfile
* BrandStrategyReport
* Future domain models

No business logic.

---

## frameworks.py

Responsibility

Define strategic reasoning frameworks.

Contains:

* Golden Circle
* Brand DNA
* Positioning
* Archetypes
* Value Proposition
* Naming Evaluation

Frameworks describe how the AI should think.

Frameworks do not generate conclusions.

---

## prompt_builder.py

Responsibility

Construct the complete reasoning prompt.

Responsibilities include:

* Founder context
* Strategic frameworks
* Output schema
* Constraints
* Quality instructions

PromptBuilder designs the AI's thinking process.

---

## llm/

Responsibility

Provide provider-independent LLM access.

Architecture

```
llm/

base.py

factory.py

openai_provider.py

anthropic_provider.py

gemini_provider.py

ollama_provider.py
```

Business logic must never depend on OpenAI directly.

---

## validator.py

Responsibility

Validate LLM output.

Checks include:

* Valid JSON
* Required fields
* Type validation
* Missing sections

Invalid responses should never reach users.

---

## report_parser.py

Responsibility

Convert validated JSON into domain objects.

Output

BrandStrategyReport

No formatting.

---

## markdown_report.py

Responsibility

Render reports into Markdown.

Uses Jinja2 templates.

No business logic.

---

## pdf_report.py

Responsibility

Generate professional PDF reports.

PDF generation is a presentation layer.

---

# Data Flow

```text
Interview

↓

FounderProfile

↓

PromptBuilder

↓

Reasoning Frameworks

↓

LLM

↓

Validated JSON

↓

BrandStrategyReport

↓

Markdown

↓

PDF
```

---

# What Each Layer Knows

Interview

Knows user input.

---

PromptBuilder

Knows how to ask the AI.

---

Frameworks

Know how experts think.

---

LLM

Knows how to reason.

---

Parser

Knows how to structure.

---

Template

Knows how to present.

---

# What Must Never Happen

The following are architecture violations.

❌ Hardcoded business conclusions

❌ LLM-specific logic inside business modules

❌ Formatting inside PromptBuilder

❌ Prompt generation inside Frameworks

❌ Business logic inside templates

❌ PDF generation inside Parser

---

# Long-Term Evolution

The architecture is intentionally designed for multiple products.

Current product

Project Origin

Future products

* ReconOS
* Security Intelligence
* Decision Intelligence
* AI Research Assistant

Only the frameworks and prompts should change.

The architecture should remain identical.

---

# Architecture Motto

> Code should be replaceable.

> Reasoning should be reusable.

> Reports should be valuable.

---

# Final Principle

Users never buy prompts.

Users never buy Python code.

Users buy better decisions.

Every architectural decision should move Project Origin closer to that goal.
