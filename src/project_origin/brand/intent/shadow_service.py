"""Compare LLM interpretation without changing active Brand behavior."""

from project_origin.brand.intent.llm_interpreter import (
    LlmBrandIntentInterpreter,
)
from project_origin.brand.intent.models import BrandIntentShadowRecord
from project_origin.brand.intent.rule_based_interpreter import (
    RuleBasedBrandIntentInterpreter,
)
from project_origin.brand.models import FounderProfile


class BrandIntentShadowService:
    def __init__(
        self,
        rule_based: RuleBasedBrandIntentInterpreter | None = None,
        llm: LlmBrandIntentInterpreter | None = None,
    ) -> None:
        self.rule_based = rule_based or RuleBasedBrandIntentInterpreter()
        self.llm = llm

    def interpret(self, profile: FounderProfile) -> BrandIntentShadowRecord:
        rule_based_profile = self.rule_based.interpret(profile)
        llm_candidate = None
        llm_error = None

        if self.llm is not None:
            try:
                llm_candidate = self.llm.interpret(profile)
            # Shadow analysis must never interrupt the active rule-based path,
            # including when an external provider is unavailable.
            except Exception as error:
                llm_error = f"{type(error).__name__}: {error}"

        return BrandIntentShadowRecord(
            active=rule_based_profile,
            rule_based=rule_based_profile,
            llm_candidate=llm_candidate,
            llm_error=llm_error,
        )
