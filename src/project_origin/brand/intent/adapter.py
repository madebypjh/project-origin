"""Adapt FounderProfile into domain-neutral Core intent input."""

from project_origin.brand.models import FounderProfile
from project_origin.core import IntentProfile, IntentSignal


class BrandIntentAdapter:
    @staticmethod
    def source_text(profile: FounderProfile) -> str:
        return "\n".join(
            [
                profile.problem,
                profile.audience,
                profile.vision,
                profile.principles,
                profile.differentiation,
            ]
        )

    @staticmethod
    def to_intent_profile(
        profile: FounderProfile,
        signals: tuple[IntentSignal, ...] = (),
        unresolved_signals: tuple[str, ...] = (),
    ) -> IntentProfile:
        return IntentProfile(
            domain="brand",
            objective=(
                f"Build a strategically aligned brand for {profile.audience} "
                f"that addresses {profile.problem}."
            ),
            constraints=(profile.principles,),
            preferences={
                "vision": profile.vision,
                "differentiation": profile.differentiation,
            },
            context={
                "problem": profile.problem,
                "audience": profile.audience,
            },
            signals=signals,
            unresolved_signals=unresolved_signals,
        )
