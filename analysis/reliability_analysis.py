#!/usr/bin/env python3
"""
VerifyBench reliability analysis.

Inputs
------
reliability/coder1_primary.csv
reliability/coder2_primary.csv
reliability/coder1_operationalized.csv
reliability/coder2_operationalized.csv

The reliability files are stored in WIDE format:
one row per benchmark, with the 10 rubric dimensions as score columns.

Outputs
-------
results/reliability_results.csv
results/operationalized_dimension_agreement.csv

Expected headline results
-------------------------
Primary:
    exact agreement = 76.0%
    Cohen's kappa = 0.490
    linear-weighted kappa = 0.508

Operationalized:
    exact agreement = 78.0%
    Cohen's kappa = 0.574
    linear-weighted kappa = 0.574
"""

import csv
from pathlib import Path

RELIABILITY = Path("reliability")
RESULTS = Path("results")
RESULTS.mkdir(parents=True, exist_ok=True)

DIMENSIONS = [
    "Items Public",
    "Labels Public",
    "Scoring Method Public",
    "Evaluation Code Public",
    "Construct Defined",
    "Coverage Documented",
    "Annotation Process Clear",
    "Limitations Stated",
    "Versioning/Maintenance",
    "License/Reuse Clear",
]


def read_wide_scores(path):
    """Return {(benchmark, dimension): ordinal_score} from a wide CSV."""
    with path.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    missing = [d for d in DIMENSIONS if d not in rows[0]]
    if missing:
        raise ValueError(f"{path} is missing score columns: {missing}")

    scores = {}
    for row in rows:
        benchmark = row["Benchmark"]
        for dimension in DIMENSIONS:
            scores[(benchmark, dimension)] = int(float(row[dimension]))
    return scores


def exact_agreement(a, b):
    keys = sorted(set(a) & set(b))
    if not keys:
        raise ValueError("No overlapping benchmark-dimension decisions.")
    return sum(a[k] == b[k] for k in keys) / len(keys)


def cohen_kappa(a, b, weighted=False):
    """
    Cohen's kappa on ordinal categories {0,1,2}.

    weighted=True uses linear agreement weights:
        1.0 for exact agreement
        0.5 for a one-category difference
        0.0 for a two-category difference
    """
    keys = sorted(set(a) & set(b))
    if not keys:
        raise ValueError("No overlapping benchmark-dimension decisions.")

    cats = [0, 1, 2]
    obs = [[0.0 for _ in cats] for __ in cats]

    for key in keys:
        obs[a[key]][b[key]] += 1.0

    n = float(len(keys))
    row_marginals = [sum(row) for row in obs]
    col_marginals = [sum(obs[i][j] for i in cats) for j in cats]

    if weighted:
        weights = [
            [1.0 - abs(i - j) / (len(cats) - 1) for j in cats]
            for i in cats
        ]
        p_observed = sum(
            weights[i][j] * obs[i][j]
            for i in cats for j in cats
        ) / n
        p_expected = sum(
            weights[i][j] * row_marginals[i] * col_marginals[j]
            for i in cats for j in cats
        ) / (n * n)
    else:
        p_observed = sum(obs[i][i] for i in cats) / n
        p_expected = sum(
            row_marginals[i] * col_marginals[i] for i in cats
        ) / (n * n)

    return (p_observed - p_expected) / (1.0 - p_expected) if p_expected != 1 else 1.0


pairs = {
    "Primary": (
        RELIABILITY / "coder1_primary.csv",
        RELIABILITY / "coder2_primary.csv",
    ),
    "Operationalized": (
        RELIABILITY / "coder1_operationalized.csv",
        RELIABILITY / "coder2_operationalized.csv",
    ),
}

result_rows = []
dimension_rows = []

for layer, (coder1_path, coder2_path) in pairs.items():
    coder1 = read_wide_scores(coder1_path)
    coder2 = read_wide_scores(coder2_path)
    keys = sorted(set(coder1) & set(coder2))

    result_rows.append({
        "Layer": layer,
        "Paired Decisions": len(keys),
        "Exact Agreement": round(exact_agreement(coder1, coder2), 3),
        "Exact Agreement Percent": round(100 * exact_agreement(coder1, coder2), 1),
        "Cohen Kappa": round(cohen_kappa(coder1, coder2, weighted=False), 3),
        "Linear Weighted Kappa": round(cohen_kappa(coder1, coder2, weighted=True), 3),
    })

    if layer == "Operationalized":
        for dimension in DIMENSIONS:
            dim_keys = [k for k in keys if k[1] == dimension]
            agreement = sum(coder1[k] == coder2[k] for k in dim_keys) / len(dim_keys)
            dimension_rows.append({
                "Dimension": dimension,
                "N": len(dim_keys),
                "Exact Agreement": round(agreement, 3),
                "Exact Agreement Percent": round(100 * agreement, 1),
            })


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


write_csv(RESULTS / "reliability_results.csv", result_rows)
write_csv(RESULTS / "operationalized_dimension_agreement.csv", dimension_rows)

for row in result_rows:
    print(row)
