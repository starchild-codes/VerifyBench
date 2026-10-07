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

The plots are generated with matplotlib only and intentionally avoid custom
style dependencies.
"""

import csv
from pathlib import Path
from collections import defaultdict
import numpy as np
import matplotlib

matplotlib.use("Agg")
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
XO = matrix(oper)
pt = totals(primary)
lt = totals(lenient)
ot = totals(oper)

# Fig. 1: primary and operationalized dimension profiles
primary_means = X.mean(axis=0)
oper_means = XO.mean(axis=0)
y = np.arange(len(DIMENSIONS))
height = 0.38
fig, ax = plt.subplots(figsize=(7.1, 5.2))
ax.barh(y + height / 2, primary_means, height, label="Primary", color="#32688E")
ax.barh(y - height / 2, oper_means, height, label="Operationalized", color="#D97732")
ax.set_yticks(y, DIMENSIONS, fontsize=8)
ax.invert_yaxis()
ax.set_xlim(0, 2.05)
ax.set_xticks(np.arange(0, 2.1, 0.5))
ax.set_xlabel("Mean dimension score (0–2)")
ax.legend(frameon=False, ncols=2, loc="lower center", bbox_to_anchor=(0.5, 1.01))
ax.grid(axis="x", color="#D9D9D9", linewidth=0.6)
ax.set_axisbelow(True)
fig.tight_layout()
fig.savefig(FIG / "fig1.png", dpi=300)
plt.close(fig)

# Fig. 2: primary score heatmap
short_dimensions = [
    "Items", "Labels", "Scoring", "Eval. code", "Construct",
    "Coverage", "Annotation", "Limitations", "Versioning", "License",
]
fig, ax = plt.subplots(figsize=(7.2, 7.8))
image = ax.imshow(X, aspect="auto", vmin=0, vmax=2, cmap="viridis")
cbar = fig.colorbar(image, ax=ax, ticks=[0, 1, 2], fraction=0.035, pad=0.02)
cbar.set_label(
    "Primary score: 0 = absent / not found; 1 = partial / incomplete; "
    "2 = primary full-credit criterion satisfied",
    fontsize=7,
)
ax.set_xticks(np.arange(len(DIMENSIONS)), short_dimensions, rotation=50, ha="right", fontsize=7)
ax.set_yticks(np.arange(len(primary)), [r["Benchmark"] for r in primary], fontsize=7)
fig.tight_layout()
fig.savefig(FIG / "fig2.png", dpi=300)
plt.close(fig)

# Fig. 3: category mean primary totals
grouped = defaultdict(list)
for r, total in zip(primary, pt):
    grouped[catmap[r["Benchmark"]]].append(total)

categories = sorted(grouped)
vals = [np.mean(grouped[c]) for c in categories]
fig, ax = plt.subplots(figsize=(7.1, 4.2))
bars = ax.bar(np.arange(len(categories)), vals, color="#32688E")
ax.set_xticks(np.arange(len(categories)), categories, rotation=35, ha="right", fontsize=8)
ax.set_ylabel("Mean primary total score (0–20)")
ax.set_ylim(0, 20)
ax.grid(axis="y", color="#D9D9D9", linewidth=0.6)
ax.set_axisbelow(True)
for bar, value in zip(bars, vals):
    ax.text(bar.get_x() + bar.get_width() / 2, value + 0.3, f"{value:.2f}", ha="center", fontsize=7)
fig.text(
    0.01,
    0.01,
    "Descriptive category means; the purposive sample has unequal category sizes.",
    fontsize=7,
)
fig.tight_layout(rect=(0, 0.04, 1, 1))
fig.savefig(FIG / "fig3.png", dpi=300)
plt.close(fig)

# Fig. 4: three-layer sensitivity overview
layer_names = ["Primary", "Lenient", "Operationalized"]
means = [pt.mean(), lt.mean(), ot.mean()]
upper = [np.sum(pt >= 18), np.sum(lt >= 18), np.sum(ot >= 18)]
lenient_change = lt - pt
oper_change = ot - pt

fig, axes = plt.subplots(3, 1, figsize=(7.2, 8.0), gridspec_kw={"height_ratios": [1, 1, 2.1]})
colors = ["#32688E", "#4C9F70", "#D97732"]

bars_a = axes[0].bar(layer_names, means, color=colors)
axes[0].set_ylabel("Mean total (0–20)")
axes[0].set_ylim(0, 22)
axes[0].set_title("A. Aggregate mean total score", loc="left", fontsize=10, fontweight="bold")
axes[0].bar_label(bars_a, labels=[f"{v:.2f}" for v in means], padding=2, fontsize=8)

bars_b = axes[1].bar(layer_names, upper, color=colors)
axes[1].set_ylabel("Benchmarks")
axes[1].set_ylim(0, 33)
axes[1].set_title("B. Benchmarks scoring 18–20", loc="left", fontsize=10, fontweight="bold")
axes[1].bar_label(bars_b, labels=[str(int(v)) for v in upper], padding=2, fontsize=8)

x = np.arange(len(primary))
width = 0.38
axes[2].bar(x - width / 2, lenient_change, width, label="Lenient − Primary", color="#4C9F70")
axes[2].bar(x + width / 2, oper_change, width, label="Operationalized − Primary", color="#D97732")
axes[2].axhline(0, color="black", linewidth=0.8)
axes[2].set_xticks(x, [r["Benchmark"] for r in primary], rotation=70, ha="right", fontsize=6)
axes[2].set_ylabel("Change in total score")
axes[2].set_title("C. Benchmark-level score change from primary", loc="left", fontsize=10, fontweight="bold")
axes[2].legend(frameon=False, ncols=2, fontsize=8, loc="upper left")

for ax in axes[:2]:
    ax.grid(axis="y", color="#D9D9D9", linewidth=0.6)
    ax.set_axisbelow(True)
fig.tight_layout()
fig.savefig(FIG / "fig4.png", dpi=300)
plt.close(fig)

print(f"Saved figures to {FIG.resolve()}")
