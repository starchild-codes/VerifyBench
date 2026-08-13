#!/usr/bin/env python3
"""
VerifyBench descriptive analysis.

Inputs
------
data/verifybench_primary_scores_canonical.csv
data/lenient_scores.csv
data/operationalized_scores.csv
data/benchmark_list.csv

Outputs
-------
results/summary_statistics.csv
results/dimension_means.csv
results/category_means.csv

The script is intended to reproduce the headline descriptive statistics
reported in the paper.
"""

import csv
from pathlib import Path
from collections import defaultdict
from statistics import mean, median

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

def read_rows(path):
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def normalize_score_rows(rows):
    out = []
    for r in rows:
        row = dict(r)
        for d in DIMENSIONS:
            row[d] = int(float(row[d]))
        if "Total Score" in row and row["Total Score"] not in ("", None):
            row["Total Score"] = int(float(row["Total Score"]))
        else:
            row["Total Score"] = sum(row[d] for d in DIMENSIONS)
        out.append(row)
    return out

primary = normalize_score_rows(read_rows(DATA / "verifybench_primary_scores_canonical.csv"))
lenient = normalize_score_rows(read_rows(DATA / "lenient_scores.csv"))
oper = normalize_score_rows(read_rows(DATA / "operationalized_scores.csv"))
benchmark_list = read_rows(DATA / "benchmark_list.csv")
category_map = {r["Benchmark"]: r["Category"] for r in benchmark_list}

layers = {
    "Primary": primary,
    "Lenient": lenient,
    "Operationalized": oper,
}

summary_rows = []
dimension_rows = []
category_rows = []

for layer_name, rows in layers.items():
    totals = [r["Total Score"] for r in rows]
    summary_rows.append({
        "Layer": layer_name,
        "N Benchmarks": len(rows),
        "Mean Total": round(mean(totals), 2),
        "Median Total": median(totals),
        "Minimum Total": min(totals),
        "Maximum Total": max(totals),
        "Benchmarks 18-20": sum(v >= 18 for v in totals),
    })

    for d in DIMENSIONS:
        vals = [r[d] for r in rows]
        dimension_rows.append({
            "Layer": layer_name,
            "Dimension": d,
            "Mean Score": round(mean(vals), 2),
        })

    grouped = defaultdict(list)
    for r in rows:
        grouped[category_map[r["Benchmark"]]].append(r["Total Score"])
    for category, vals in sorted(grouped.items()):
        category_rows.append({
            "Layer": layer_name,
            "Category": category,
            "N": len(vals),
            "Mean Total": round(mean(vals), 2),
        })

def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

write_csv(RESULTS / "summary_statistics.csv", summary_rows)
write_csv(RESULTS / "dimension_means.csv", dimension_rows)
write_csv(RESULTS / "category_means.csv", category_rows)

print("Primary:", summary_rows[0])
print("Lenient:", summary_rows[1])
print("Operationalized:", summary_rows[2])
