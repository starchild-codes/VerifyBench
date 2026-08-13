#!/usr/bin/env python3
"""
VerifyBench robustness analysis excluding Monte Carlo perturbation.

Inputs
------
data/verifybench_primary_scores_canonical.csv

Outputs
-------
results/leave_one_dimension_out.csv
results/alternative_weighting.csv

Notes
-----
The leave-one-dimension-out analysis is fully specified and reproducible.

The weighting scenarios below are explicit, transparent stress tests. If the
paper ultimately reports a different historical set of weighting scenarios,
replace SCENARIOS with those exact frozen weights and regenerate the output.
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

with (DATA / "verifybench_primary_scores_canonical.csv").open(
    newline="", encoding="utf-8-sig"
) as f:
    rows = list(csv.DictReader(f))

benchmarks = [r["Benchmark"] for r in rows]
X = np.array([[float(r[d]) for d in DIMENSIONS] for r in rows])

base_totals = X.sum(axis=1)
base_ranks = rankdata(-base_totals, method="average")

loo_rows = []
for j, dim in enumerate(DIMENSIONS):
    totals = X.sum(axis=1) - X[:, j]
    ranks = rankdata(-totals, method="average")
    disp = np.abs(ranks - base_ranks)
    rho = spearmanr(base_totals, totals).statistic
    loo_rows.append({
        "Removed Dimension": dim,
        "Spearman Rho with Primary": round(float(rho), 3),
        "Mean Absolute Rank Displacement": round(float(disp.mean()), 2),
        "Median Absolute Rank Displacement": round(float(np.median(disp)), 2),
        "Maximum Absolute Rank Displacement": round(float(disp.max()), 2),
    })

# Explicit sensitivity scenarios around equal weighting.
# Each vector follows the DIMENSIONS order above.
SCENARIOS = {
    "Equal weights": np.ones(10),
    "Access emphasis": np.array([1.5,1.5,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]),
    "Reproducibility emphasis": np.array([1.0,1.0,1.5,1.5,1.0,1.0,1.0,1.0,1.0,1.0]),
    "Documentation emphasis": np.array([1.0,1.0,1.0,1.0,1.25,1.25,1.25,1.25,1.0,1.0]),
    "Lifecycle/reuse emphasis": np.array([1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.5,1.5]),
    "Reduced access weight": np.array([0.5,0.5,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]),
}

weight_rows = []
for name, w in SCENARIOS.items():
    totals = (X * w).sum(axis=1)
    ranks = rankdata(-totals, method="average")
    rho = spearmanr(base_totals, totals).statistic
    disp = np.abs(ranks - base_ranks)
    weight_rows.append({
        "Scenario": name,
        "Spearman Rho with Primary": round(float(rho), 3),
        "Mean Absolute Rank Displacement": round(float(disp.mean()), 2),
        "Median Absolute Rank Displacement": round(float(np.median(disp)), 2),
        "Maximum Absolute Rank Displacement": round(float(disp.max()), 2),
    })

def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

write_csv(RESULTS / "leave_one_dimension_out.csv", loo_rows)
write_csv(RESULTS / "alternative_weighting.csv", weight_rows)

print("Most influential dimension removal:")
print(max(loo_rows, key=lambda r: r["Mean Absolute Rank Displacement"]))
print("\nWeighting scenarios:")
for r in weight_rows:
    print(r)
