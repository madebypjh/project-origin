"""
Project Origin - Name Ranker

Ranks evaluated brand name candidates.
"""

from project_origin.brand.naming.candidate import NameCandidate


class NameRanker:
    @staticmethod
    def rank(
        candidates: list[NameCandidate],
        limit: int = 20,
    ) -> list[NameCandidate]:
        ranked = sorted(
            candidates,
            key=lambda candidate: candidate.total_score,
            reverse=True,
        )

        selected = []
        seen_signatures = set()

        for candidate in ranked:
            signature = candidate.metadata.get("generation_signature")
            if signature and signature in seen_signatures:
                continue

            selected.append(candidate)
            if signature:
                seen_signatures.add(signature)

            if len(selected) == limit:
                return selected

        if len(selected) < limit:
            selected_names = {candidate.name.casefold() for candidate in selected}
            for candidate in ranked:
                if candidate.name.casefold() in selected_names:
                    continue
                selected.append(candidate)
                selected_names.add(candidate.name.casefold())
                if len(selected) == limit:
                    break

        return selected
