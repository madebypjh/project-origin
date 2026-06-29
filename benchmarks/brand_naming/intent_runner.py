"""Run benchmark cases through the Brand intent shadow pipeline."""

from time import perf_counter

from benchmarks.brand_naming.models import BrandNamingBenchmarkCase
from benchmarks.brand_naming.results import (
    BrandIntentBenchmarkOutput,
    IntentBenchmarkSignal,
)
from project_origin.brand.intent import (
    BrandIntentShadowService,
    LlmBrandIntentInterpreter,
    RuleBasedBrandIntentInterpreter,
)
from project_origin.core import IntentProfile


class ProjectOriginIntentRunner:
    def __init__(
        self,
        rule_based: RuleBasedBrandIntentInterpreter | None = None,
        llm: LlmBrandIntentInterpreter | None = None,
    ) -> None:
        self.service = BrandIntentShadowService(
            rule_based=rule_based,
            llm=llm,
        )

    def run(
        self,
        case: BrandNamingBenchmarkCase,
    ) -> BrandIntentBenchmarkOutput:
        started_at = perf_counter()
        record = self.service.interpret(case.profile)
        latency_ms = round((perf_counter() - started_at) * 1000, 3)

        return BrandIntentBenchmarkOutput(
            case_id=case.identifier,
            approach="project_origin_intent_shadow",
            active_signals=_signals(record.active),
            active_unresolved_signals=record.active.unresolved_signals,
            llm_candidate_signals=_signals(record.llm_candidate),
            llm_unresolved_signals=(
                record.llm_candidate.unresolved_signals
                if record.llm_candidate is not None
                else ()
            ),
            llm_error=record.llm_error,
            latency_ms=latency_ms,
            estimated_cost_usd=0.0 if record.llm_candidate is None else None,
        )


def _signals(
    profile: IntentProfile | None,
) -> tuple[IntentBenchmarkSignal, ...]:
    if profile is None:
        return ()
    return tuple(
        IntentBenchmarkSignal(
            kind=signal.kind,
            concept=signal.concept,
            weight=signal.weight,
            confidence=signal.confidence,
            evidence=signal.evidence,
        )
        for signal in profile.signals
    )
