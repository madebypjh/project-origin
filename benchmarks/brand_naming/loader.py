"""Load and validate versioned Brand naming benchmark cases."""

import json
from pathlib import Path

from benchmarks.brand_naming.models import BrandNamingBenchmarkCase


DEFAULT_CASES_PATH = Path(__file__).with_name("cases.json")


def load_cases(
    path: Path = DEFAULT_CASES_PATH,
) -> tuple[BrandNamingBenchmarkCase, ...]:
    raw_cases = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw_cases, list):
        raise ValueError("Brand naming benchmark must be a JSON array")

    cases = tuple(
        BrandNamingBenchmarkCase.from_dict(item)
        for item in raw_cases
    )
    identifiers = [case.identifier for case in cases]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("Benchmark case ids must be unique")
    if not cases:
        raise ValueError("Benchmark must contain at least one case")
    return cases
