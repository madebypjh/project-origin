import json
from pathlib import Path

from research.validator import BrandGenomeValidator


def main():
    path = Path("dataset/analysis/brand_genome_sample.json")

    data = json.loads(path.read_text(encoding="utf-8"))
    errors = BrandGenomeValidator.validate_many(data)

    if not errors:
        print("Brand genome validation passed.")
        return

    print("Brand genome validation failed:\n")

    for error in errors:
        print(error)


if __name__ == "__main__":
    main()