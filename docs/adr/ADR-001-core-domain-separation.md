# ADR-001: Core and Domain Separation

## Status
Accepted

## Context
Project Origin is intended to become an AI Decision Engine Platform, not only a Brand Strategy tool.

The Brand Engine is the first domain implementation used to validate the reusable Core architecture.

## Decision
We will separate reusable decision-making logic into `project_origin.core`, and domain-specific logic into domain packages such as `project_origin.brand`.

Core must not depend on Brand, Recon, or any future domain.

## Consequences
- Core can be reused by future domains.
- Brand remains a thin implementation layer.
- Domain logic should not leak into Core.