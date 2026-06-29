# Research Pipeline

Version: Alpha 0.3

---

## Objective

Project Origin should continuously improve its Brand Intelligence Engine.

Rather than relying only on LLM creativity, Project Origin studies successful
brands and extracts reusable brand patterns.

---

## Research Flow

```text
Curated Brand List
    -> AI-assisted Brand List Candidate Expansion
    -> Rule-based Candidate Review
    -> Optional Human Review / Promotion
    -> Brand Analyzer
    -> Brand Genome JSON
    -> Pattern Extraction
    -> Pattern Database
    -> Naming Engine Evolution
```

---

## Research Components

### Brand List Expander

Uses an LLM to propose additional brand candidates by category.

The output is candidate-only and must not be treated as validated research
data. Proposed brands are written with the status
`candidate_only_requires_review`.

Candidates must be reviewed before they are promoted into `BrandCollector` or
used for Brand Genome analysis.

Run:

```powershell
$env:PYTHONPATH = "src"
.\venv\Scripts\python.exe -m research.brand_list_expander
```

---

### Brand List Candidate Reviewer

Validates AI-proposed brand candidates before analysis.

The reviewer rejects:

- duplicates already present in curated lists;
- duplicates across proposed categories;
- URL-like values;
- suspicious encoding artifacts;
- overly long values;
- legal entity names that are less useful as public-facing brand names.

It writes `dataset/analysis/brand_list_reviewed.json`, preserving both accepted
and rejected candidates with rejection reasons.

Run:

```powershell
$env:PYTHONPATH = "src"
.\venv\Scripts\python.exe -m research.brand_list_reviewer
```

---

### Brand Analyzer

Analyzes one or more famous brands.

Produces structured Brand Genome JSON.

Reviewed candidates can be analyzed in batches:

```powershell
$env:PYTHONPATH = "src"
.\venv\Scripts\python.exe -m research.analyze_brand_candidates --provider openai --category ai --batch-size 10 --max-brands 30
```

Use `--provider mock` only for local pipeline verification. Mock analysis files
must not be promoted into the Brand Genome dataset.

---

### Pattern Extractor

Finds recurring phonetic, semantic, and morphological patterns.

---

### Genome Builder

Combines analyzed brands into a searchable Brand Genome Database.

---

### Knowledge Compiler

Compiles extracted patterns into generator-friendly naming knowledge.

Low-sample knowledge must be treated as soft guidance, not hard generation
rules.

---

## Long-term Goal

Build one of the world's largest structured Brand Genome datasets.

This dataset becomes Project Origin's competitive advantage.

---

## Guiding Principle

Project Origin should learn from brands.

Not imitate them.
