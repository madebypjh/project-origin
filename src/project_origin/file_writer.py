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