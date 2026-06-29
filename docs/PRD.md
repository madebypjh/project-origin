# Project Origin Brand — Product Requirement Document

Version: 0.2

Status: Active

Product role: First validation domain for Project Origin Core

## Overview

Project Origin Brand is an AI-assisted Brand Strategy product. It helps founders
turn mission, values, audience, and long-term goals into an explainable Brand
direction and professional report.

It is not a random name generator. Naming is one decision inside the report.

## Validation question

Would a founder pay for a Brand Strategy Report because it provides insight,
confidence, and decision support that a strong generic AI response does not?

## Target users

- startup founders and product builders;
- small teams defining a new company or product identity;
- agencies that need a repeatable strategic discovery process.

## Concierge MVP

```text
Founder interview
    -> operator-assisted CLI
    -> structured Brand analysis
    -> candidate generation and evaluation
    -> professional Brand Strategy Report
    -> founder feedback
```

The user does not need to interact with the internal software.

## Required output

- executive summary;
- founder and business insights;
- Brand identity, mission, vision, and values;
- target audience and positioning;
- Brand personality and narrative direction;
- naming strategy and five evaluated candidates;
- one explainable final recommendation.

## Quality requirements

- Claims must be grounded in interview or validated knowledge.
- Facts, inferences, and uncertainty must be distinguishable.
- Recommendations must include strengths, weaknesses, and rationale.
- Reports must target at least 22/25 under the Report Quality Standard.

## MVP exclusions

- accounts, authentication, and team collaboration;
- payment and public web application;
- automatic trademark or domain clearance;
- logo generation;
- universal cross-domain decision functionality.

These features require product evidence before implementation.

## Product success

- target founders consistently report non-generic strategic insight;
- target founders express willingness to pay;
- report quality is repeatable;
- the structured pipeline outperforms or complements a strong direct-LLM
  baseline in a measurable way.

## Relationship to Core and ReconOS

Brand is the first domain used to validate domain-neutral decision contracts.
ReconOS is a future Security product/domain that may reuse only the contracts
and implementations proven to be genuinely reusable.
