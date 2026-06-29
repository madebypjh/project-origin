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

        return ranked[:limit]
