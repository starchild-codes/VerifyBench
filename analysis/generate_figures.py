#!/usr/bin/env python3
"""
Generate VerifyBench figures from repository data.

Inputs
------
data/verifybench_primary_scores_canonical.csv
data/benchmark_list.csv
data/lenient_scores.csv
data/operationalized_scores.csv

Outputs
-------
figures/fig1.png
figures/fig2.png
figures/fig3.png
figures/fig4.png
figures/fig5.png

The plots are generated with matplotlib only and intentionally avoid custom
style dependencies.
"""

import csv
from pathlib import Path
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt

DATA = Path("data")
FIG = Path("figures")
FIG.mkdir(parents=True, exist_ok=True)

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

def matrix(rows):
    return np.array([[float(r[d]) for d in DIMENSIONS] for r in rows])

def totals(rows):
    return np.array([
        float(r["Total Score"]) if r.get("Total Score") else sum(float(r[d]) for d in DIMENSIONS)
        for r in rows
    ])

primary = read_rows(DATA / "verifybench_primary_scores_canonical.csv")
lenient = read_rows(DATA / "lenient_scores.csv")
oper = read_rows(DATA / "operationalized_scores.csv")
benchlist = read_rows(DATA / "benchmark_list.csv")
catmap = {r["Benchmark"]: r["Category"] for r in benchlist}

X = matrix(primary)
pt = totals(primary)
lt = totals(lenient)
ot = totals(oper)

# Fig. 1: score distribution
plt.figure(figsize=(6.4, 4.0))
bins = np.arange(pt.min()-0.5, pt.max()+1.5, 1)
plt.hist(pt, bins=bins, edgecolor="black")
plt.xlabel("Total Public Verifiability Score")
plt.ylabel("Number of Benchmarks")
plt.tight_layout()
plt.savefig(FIG / "fig1.png", dpi=300)
plt.close()

# Fig. 2: dimension means
means = X.mean(axis=0)
plt.figure(figsize=(7.2, 4.4))
y = np.arange(len(DIMENSIONS))
plt.barh(y, means)
plt.yticks(y, DIMENSIONS)
plt.xlim(0, 2)
plt.xlabel("Mean Score")
plt.tight_layout()
plt.savefig(FIG / "fig2.png", dpi=300)
plt.close()

# Fig. 3: heatmap
plt.figure(figsize=(8.6, 8.8))
plt.imshow(X, aspect="auto", vmin=0, vmax=2)
plt.colorbar(label="Score")
plt.xticks(np.arange(len(DIMENSIONS)), DIMENSIONS, rotation=60, ha="right", fontsize=7)
plt.yticks(np.arange(len(primary)), [r["Benchmark"] for r in primary], fontsize=7)
plt.tight_layout()
plt.savefig(FIG / "fig3.png", dpi=300)
plt.close()

# Fig. 4: category mean totals
grouped = defaultdict(list)
for r, total in zip(primary, pt):
    grouped[catmap[r["Benchmark"]]].append(total)

categories = sorted(grouped)
vals = [np.mean(grouped[c]) for c in categories]
plt.figure(figsize=(7.2, 4.2))
plt.bar(np.arange(len(categories)), vals)
plt.xticks(np.arange(len(categories)), categories, rotation=40, ha="right")
plt.ylabel("Mean Total Score")
plt.tight_layout()
plt.savefig(FIG / "fig4.png", dpi=300)
plt.close()

# Fig. 5: sensitivity overview
layer_names = ["Primary", "Lenient", "Operationalized"]
means = [pt.mean(), lt.mean(), ot.mean()]
upper = [np.sum(pt >= 18), np.sum(lt >= 18), np.sum(ot >= 18)]
changed = [0, np.sum(lt != pt), np.sum(ot != pt)]

x = np.arange(len(layer_names))
width = 0.25
plt.figure(figsize=(7.2, 4.4))
plt.bar(x - width, means, width, label="Mean total")
plt.bar(x, upper, width, label="Benchmarks scoring 18-20")
plt.bar(x + width, changed, width, label="Totals changed from primary")
plt.xticks(x, layer_names)
plt.legend()
plt.tight_layout()
plt.savefig(FIG / "fig5.png", dpi=300)
plt.close()

print(f"Saved figures to {FIG.resolve()}")
