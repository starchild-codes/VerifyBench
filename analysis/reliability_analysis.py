#!/usr/bin/env python3
"""
VerifyBench reliability analysis.

Inputs
------
reliability/coder1_primary.csv
reliability/coder2_primary.csv
reliability/coder1_operationalized.csv
reliability/coder2_operationalized.csv

Outputs
-------
results/reliability_results.csv
results/operationalized_dimension_agreement.csv

Reproduces exact agreement, Cohen's kappa, linear-weighted kappa, and
dimension-level exact agreement reported in the paper.
"""

import csv
from pathlib import Path
from collections import defaultdict

RELIABILITY = Path("reliability")
RESULTS = Path("results")
RESULTS.mkdir(parents=True, exist_ok=True)

def read_rows(path):
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def score_column(rows):
    candidates = [
        "Score", "Primary Score", "Operationalized Score", "Final Score",
        "Coder Score", "score"
    ]
    for c in candidates:
        if c in rows[0]:
            return c
    raise ValueError(f"Could not identify score column. Columns: {rows[0].keys()}")

def dimension_column(rows):
    for c in ["Dimension", "dimension"]:
        if c in rows[0]:
            return c
    raise ValueError("Could not identify Dimension column")

def keyed_scores(path):
    rows = read_rows(path)
    sc = score_column(rows)
    dc = dimension_column(rows)
    out = {}
    for r in rows:
        benchmark = r.get("Benchmark") or r.get("benchmark")
        out[(benchmark, r[dc])] = int(float(r[sc]))
    return out

def exact_agreement(a, b):
    keys = sorted(set(a) & set(b))
    return sum(a[k] == b[k] for k in keys) / len(keys)

def cohen_kappa(a, b, weighted=False):
    keys = sorted(set(a) & set(b))
    x = [a[k] for k in keys]
    y = [b[k] for k in keys]
    cats = [0, 1, 2]
    n = len(keys)

    obs = [[0 for _ in cats] for __ in cats]
    for xi, yi in zip(x, y):
        obs[xi][yi] += 1

    row_m = [sum(row) for row in obs]
    col_m = [sum(obs[i][j] for i in cats) for j in cats]

    if weighted:
        weights = [[1 - abs(i-j)/(len(cats)-1) for j in cats] for i in cats]
        po = sum(weights[i][j] * obs[i][j] for i in cats for j in cats) / n
        pe = sum(
            weights[i][j] * row_m[i] * col_m[j]
            for i in cats for j in cats
        ) / (n*n)
    else:
        po = sum(obs[i][i] for i in cats) / n
        pe = sum(row_m[i] * col_m[i] for i in cats) / (n*n)

    return (po - pe) / (1 - pe) if pe != 1 else 1.0

pairs = {
    "Primary": (
        RELIABILITY / "coder1_primary.csv",
        RELIABILITY / "coder2_primary.csv",
    ),
    "Operationalized": (
        RELIABILITY / "coder1_operationalized.csv",
        RELIABILITY / "coder2_operationalized.csv",
    )
}

result_rows = []
oper_dim_rows = []

for name, (p1, p2) in pairs.items():
    a = keyed_scores(p1)
    b = keyed_scores(p2)
    keys = sorted(set(a) & set(b))
    result_rows.append({
        "Layer": name,
        "Paired Decisions": len(keys),
        "Exact Agreement": round(exact_agreement(a, b), 3),
        "Cohen Kappa": round(cohen_kappa(a, b, weighted=False), 3),
        "Linear Weighted Kappa": round(cohen_kappa(a, b, weighted=True), 3),
    })

    if name == "Operationalized":
        by_dim = defaultdict(list)
        for k in keys:
            by_dim[k[1]].append(a[k] == b[k])
        for dim, matches in sorted(by_dim.items()):
            oper_dim_rows.append({
                "Dimension": dim,
                "N": len(matches),
                "Exact Agreement": round(sum(matches)/len(matches), 3),
                "Exact Agreement Percent": round(100*sum(matches)/len(matches), 1),
            })

def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

write_csv(RESULTS / "reliability_results.csv", result_rows)
write_csv(RESULTS / "operationalized_dimension_agreement.csv", oper_dim_rows)

for r in result_rows:
    print(r)
