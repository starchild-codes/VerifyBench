#!/usr/bin/env python3
"""
VerifyBench deterministic robustness analyses.

Input
-----
data/verifybench_primary_scores_canonical.csv

Outputs
-------
results/leave_one_dimension_out.csv
results/alternative_weighting.csv

This script intentionally separates deterministic robustness analyses from
analysis/monte_carlo_robustness.py.

IMPORTANT
---------
The earlier manuscript draft stated that removing "License/Reuse Clear"
produced a mean absolute rank displacement of 6.1 positions. Recalculation
from the canonical final 30 x 10 primary matrix does NOT reproduce that
claim.

Using tied average ranks and the final canonical matrix:
    - Evaluation Code Public is the most influential single-dimension removal
    - mean absolute rank displacement = 2.87 positions
    - Spearman rho with the equal-weight primary totals = 0.916

The output of this script is therefore the reproducible source of truth.
"""

import csv
from pathlib import Path

import numpy as np
from scipy.stats import rankdata, spearmanr

DATA = Path("data")
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


def load_primary():
    with (DATA / "verifybench_primary_scores_canonical.csv").open(
        newline="", encoding="utf-8-sig"
    ) as f:
        rows = list(csv.DictReader(f))

    x = np.array(
        [[float(row[d]) for d in DIMENSIONS] for row in rows],
        dtype=float,
    )
    benchmarks = [row["Benchmark"] for row in rows]
    return benchmarks, x


benchmarks, X = load_primary()
base_totals = X.sum(axis=1)
base_ranks = rankdata(-base_totals, method="average")

# -------------------------------------------------------------------------
# Leave-one-dimension-out analysis
# -------------------------------------------------------------------------
loo_rows = []

for j, dimension in enumerate(DIMENSIONS):
    reduced_totals = base_totals - X[:, j]
    reduced_ranks = rankdata(-reduced_totals, method="average")
    displacement = np.abs(reduced_ranks - base_ranks)
    rho = spearmanr(base_totals, reduced_totals).statistic

    loo_rows.append({
        "Removed Dimension": dimension,
        "Spearman Rho with Primary": round(float(rho), 3),
        "Mean Absolute Rank Displacement": round(float(displacement.mean()), 2),
        "Median Absolute Rank Displacement": round(float(np.median(displacement)), 2),
        "Maximum Absolute Rank Displacement": round(float(displacement.max()), 2),
    })

# -------------------------------------------------------------------------
# Alternative weighting stress tests
# -------------------------------------------------------------------------
# These are explicit, fixed sensitivity scenarios defined for the released
# reproducibility package. They are not claimed to be empirically estimated
# importance weights.
#
# Dimension order follows DIMENSIONS above.
SCENARIOS = {
    "Equal weights": np.ones(10),
    "Access emphasis": np.array(
        [1.5, 1.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    ),
    "Reproducibility emphasis": np.array(
        [1.0, 1.0, 1.5, 1.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    ),
    "Documentation emphasis": np.array(
        [1.0, 1.0, 1.0, 1.0, 1.25, 1.25, 1.25, 1.25, 1.0, 1.0]
    ),
    "Lifecycle/reuse emphasis": np.array(
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.5, 1.5]
    ),
    "Reduced access weight": np.array(
        [0.5, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    ),
}

weight_rows = []

for name, weights in SCENARIOS.items():
    weighted_totals = (X * weights).sum(axis=1)
    weighted_ranks = rankdata(-weighted_totals, method="average")
    displacement = np.abs(weighted_ranks - base_ranks)
    rho = spearmanr(base_totals, weighted_totals).statistic

    weight_rows.append({
        "Scenario": name,
        "Spearman Rho with Primary": round(float(rho), 3),
        "Mean Absolute Rank Displacement": round(float(displacement.mean()), 2),
        "Median Absolute Rank Displacement": round(float(np.median(displacement)), 2),
        "Maximum Absolute Rank Displacement": round(float(displacement.max()), 2),
    })


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


write_csv(RESULTS / "leave_one_dimension_out.csv", loo_rows)
write_csv(RESULTS / "alternative_weighting.csv", weight_rows)

most_influential = max(
    loo_rows,
    key=lambda row: row["Mean Absolute Rank Displacement"],
)

print("Most influential single-dimension removal:")
print(most_influential)
print("\nAlternative weighting scenarios:")
for row in weight_rows:
    print(row)
