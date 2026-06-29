# ADR-002: Product-Driven Core Evolution

## Status

Accepted

## Context

Project Origin needs reusable decision architecture without building a
speculative universal platform before its product value is validated.

“Product First, Engine Later” can allow domain concepts to leak across
boundaries. An unrestricted “Core First” approach can create abstractions with
no proven use case.

## Decision

Project Origin will be product-driven and Core-aware.

- Product evidence determines development priority.
- Domain-neutral Core contracts are established early.
- Concrete behavior is first implemented against real domain use cases.
- An implementation moves into Core only after reuse is demonstrated.
- Core never depends on a domain.

## Consequences

- Brand remains the primary validation environment.
- Core initially contains contracts rather than a speculative universal engine.
- Some duplication may be tolerated until a reusable pattern is proven.
- Cross-domain reuse must be demonstrated by tests or benchmarks.
