# Master Roadmap v3.0

## Mission

Build trusted AI systems that help people make better, explainable decisions.

Project Origin Brand is the first product and validation domain. ReconOS is the
second planned product and Security domain.

## Strategy

### Product validation first. Core boundaries from day one.

We build the smallest useful product, establish domain-neutral contracts early,
and generalize implementations only after evidence of reuse.

The report validates customer value. The benchmark validates technical value.
Both are required.

## Phase 1 — Foundation

Status: Completed

- Mission, vision, values, and Brand DNA
- Concierge MVP definition
- Brand report quality standard
- Initial Brand pipeline

## Phase 2 — Core boundary

Status: In progress

- Separate `project_origin.core` and `project_origin.brand`
- Define `IntentProfile`, `KnowledgePacket`, `ReasoningTrace`,
  `DecisionOption`, and `DecisionResult`
- Validate an evidence-backed Intent Interpreter contract in Brand Shadow Mode
- Keep Core independent from every domain
- Record architectural decisions through ADRs

Exit criterion: dependency direction is enforced by code structure and tests.

## Phase 3 — Brand pipeline validation

Status: In progress

- Complete Generator V2 knowledge integration
- Benchmark LLM intent interpretation before making it authoritative
- Keep `NameCandidate` structured through the whole pipeline
- Improve interview, reasoning, and report quality
- Validate research data before compilation
- Deliver Concierge reports to real founders

Exit criteria:

- repeatable report generation;
- report quality average of at least 22/25;
- evidence that target users would pay.

## Phase 4 — Decision benchmark

Compare the same Brand cases using:

1. a strong direct-LLM prompt;
2. a role-based multi-agent workflow;
3. the Project Origin structured pipeline.

Measure:

- expert-rated decision quality;
- consistency;
- evidence accuracy;
- trace completeness;
- cost and latency.

Exit criterion: Project Origin demonstrates a meaningful advantage in at least
one product-relevant dimension without unacceptable regressions elsewhere.

## Phase 5 — Structured reasoning and decision

- Implement one narrow Brand reasoning use case
- Produce an explicit `ReasoningTrace`
- Compare `DecisionOption` objects using testable criteria
- Return a validated `DecisionResult`
- Keep LLMs as replaceable assistants

Do not create a universal Reasoning or Decision Engine before the narrow case is
measurable.

## Phase 6 — Market validation

- Acquire the first paying customers
- Validate pricing, interview quality, report usefulness, and trust
- Improve the product from observed failures

Infrastructure such as accounts, payments, and a web application remains
secondary until it removes a proven operational constraint.

## Phase 7 — ReconOS validation

Implement ReconOS as a Security product on Project Origin Core.

Reuse:

- Core decision contracts;
- validated provider and validation patterns;
- proven reasoning and evaluation infrastructure.

Do not force reuse of Brand knowledge, policies, evaluators, workflows, or
outputs.

## Guiding questions

Before building:

- Does this improve a real decision or report?
- Can the improvement be measured?
- Is the abstraction already required by more than one use case?
- Does this preserve explainability and provider independence?
- Would a direct LLM or agent workflow solve this more simply?

If the last answer is yes and Origin adds no measurable value, do not add the
abstraction.
