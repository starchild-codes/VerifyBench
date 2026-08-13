#!/usr/bin/env python3
"""
VerifyBench three-layer sensitivity analysis.

Inputs
------
data/verifybench_primary_scores_canonical.csv
data/lenient_scores.csv
data/operationalized_scores.csv

Outputs
-------
results/sensitivity_results.csv
results/benchmark_level_sensitivity.csv

Reproduces total-score changes, Spearman rank correlations, and tied-rank
displacement statistics.
"""

import csv
from pathlib import Path
from statistics import mean, median
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

def read_scores(path):
    with path.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    out = {}
    for r in rows:
        total = int(float(r["Total Score"])) if r.get("Total Score") else sum(int(float(r[d])) for d in DIMENSIONS)
        out[r["Benchmark"]] = total
    return out

primary = read_scores(DATA / "verifybench_primary_scores_canonical.csv")
lenient = read_scores(DATA / "lenient_scores.csv")
oper = read_scores(DATA / "operationalized_scores.csv")

benchmarks = list(primary.keys())
p = np.array([primary[b] for b in benchmarks], dtype=float)
base_ranks = rankdata(-p, method="average")

summary_rows = []
detail_rows = []

def analyze(name, alt):
    a = np.array([alt[b] for b in benchmarks], dtype=float)
    diff = a - p
    absdiff = np.abs(diff)
    alt_ranks = rankdata(-a, method="average")
    disp = np.abs(alt_ranks - base_ranks)
    rho, pval = spearmanr(p, a)

    summary_rows.append({
        "Layer": name,
        "Mean Total": round(mean(a), 2),
        "Median Total": median(a),
        "Minimum": int(a.min()),
        "Maximum": int(a.max()),
        "Benchmarks 18-20": int(np.sum(a >= 18)),
        "Totals Changed": int(np.sum(diff != 0)),
        "Mean Absolute Score Change": round(float(absdiff.mean()), 2),
        "Median Absolute Score Change": round(float(np.median(absdiff)), 2),
        "Changed by >=2 Points": int(np.sum(absdiff >= 2)),
        "Changed by >=3 Points": int(np.sum(absdiff >= 3)),
        "Spearman Rho with Primary": round(float(rho), 3),
        "Two-sided P": round(float(pval), 3),
        "Mean Absolute Rank Displacement": round(float(disp.mean()), 2),
        "Median Absolute Rank Displacement": round(float(np.median(disp)), 2),
        "Maximum Absolute Rank Displacement": round(float(disp.max()), 2),
        "Increased": int(np.sum(diff > 0)),
        "Decreased": int(np.sum(diff < 0)),
        "Unchanged": int(np.sum(diff == 0)),
    })

    for i, b in enumerate(benchmarks):
        detail_rows.append({
            "Benchmark": b,
            "Layer": name,
            "Primary Total": int(p[i]),
            "Alternative Total": int(a[i]),
            "Score Change": int(diff[i]),
            "Primary Rank": float(base_ranks[i]),
            "Alternative Rank": float(alt_ranks[i]),
            "Absolute Rank Displacement": float(disp[i]),
        })

analyze("Lenient", lenient)
analyze("Operationalized", oper)

def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

write_csv(RESULTS / "sensitivity_results.csv", summary_rows)
write_csv(RESULTS / "benchmark_level_sensitivity.csv", detail_rows)

for r in summary_rows:
    print(r)
