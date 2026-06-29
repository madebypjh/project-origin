# ADR-003: LLM-Assisted Intent Interpretation

## Status

Accepted

## Context

The original Brand semantic pipeline classifies founder input through a small,
hardcoded keyword taxonomy. This is deterministic but cannot represent
open-ended concepts such as medical humility, creator ownership, or industrial
traceability without continuous developer updates.

Allowing an LLM to freely own classification would create different problems:
unstable labels, unsupported inference, provider dependence, and semantic data
that cannot be reliably compared or reused.

## Decision

Project Origin will use LLMs as replaceable intent interpreters under
domain-neutral Core contracts.

- Core owns `IntentSignal`, `IntentProfile`, normalization, validation, and the
  `IntentInterpreter` protocol.
- Every signal must contain source evidence, weight, and confidence.
- Signal concepts remain open-ended; Core contains no Brand category taxonomy.
- Brand owns the interpretation policy and adapts `FounderProfile` into Core
  intent contracts.
- The rule-based interpreter remains the active fallback and benchmark.
- The LLM interpreter initially runs in Shadow Mode and cannot change naming or
  report decisions.
- Provider or validation failures must not interrupt the active product path.

## Consequences

- Project Origin can discover intent beyond developer-authored keyword lists.
- Evidence-backed outputs can be accumulated and evaluated across providers.
- LLM calls add cost, latency, privacy considerations, and nondeterminism.
- Shadow results require benchmark review before promotion to the active path.
- Domain-specific use of interpreted intent remains outside Core.
