"""
Project Origin - File Writer

Handles saving generated outputs to the local filesystem.
"""

from pathlib import Path


class FileWriter:
    @staticmethod
    def save_markdown(content: str, filename: str = "brand_report.md") -> Path:
        project_root = Path(__file__).resolve().parents[2]
        output_dir = project_root / "output"
        output_dir.mkdir(exist_ok=True)

        file_path = output_dir / filename
        file_path.write_text(content, encoding="utf-8")

        return file_path

    @staticmethod
    def save_name_candidates(candidates, filename: str = "name_candidates.md") -> Path:
        project_root = Path(__file__).resolve().parents[2]
        output_dir = project_root / "output"
        output_dir.mkdir(exist_ok=True)

        file_path = output_dir / filename

        lines = ["# Generated Name Candidates", ""]

        for index, candidate in enumerate(candidates, start=1):
            lines.append(f"## {index}. {candidate.name}")
            lines.append("")
            lines.append(f"- Total Score: {candidate.total_score}/10")
            lines.append(f"- Pronunciation: {candidate.pronunciation_score}/10")
            lines.append(f"- Originality: {candidate.originality_score}/10")
            lines.append(f"- Strategy Fit: {candidate.strategy_score}/10")
            lines.append(f"- Memorability: {candidate.memorability_score}/10")
            lines.append(f"- Reason: {candidate.evaluation_reason}")
            lines.append("")

        file_path.write_text("\n".join(lines), encoding="utf-8")

        return file_path