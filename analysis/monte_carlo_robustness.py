#!/usr/bin/env python3
"""
VerifyBench Monte Carlo robustness analysis.

Protocol:
- Input: canonical primary/adjudicated 30 x 10 rubric matrix.
- Scores are ordinal {0,1,2}.
- For each simulation, independent Gaussian noise N(0, sigma) is added
  to every cell.
- Perturbed values are rounded to the nearest rubric category and clipped
  to [0,2].
- Benchmark totals and tied ranks are recomputed.
- Rank stability is measured by Spearman correlation against the
  unperturbed primary totals.
- 10,000 simulations are run at each sigma.
- Fixed seed: 20260813.
- A single NumPy Generator stream is consumed sequentially in SIGMAS order.

The sigma=0.43 setting is a heuristic calibration to the primary exercise's
24% coder-disagreement rate. For an interior ordinal category, Gaussian noise
with sigma approximately 0.43 crosses a +/-0.5 rounding threshold with
probability about 0.24. Boundary clipping makes perturbations asymmetric for
saturated dimensions, so this remains a model-based stress test rather than an
empirical model of coder error.
"""

import csv
import numpy as np
from scipy.stats import spearmanr, rankdata
from pathlib import Path

INPUT = Path("data/verifybench_primary_scores_canonical.csv")
OUTPUT = Path("results/monte_carlo_results.csv")
SIGMAS = [0.25, 0.43, 0.50, 0.75, 1.00]
N_SIMS = 10_000
SEED = 20260813

rows = list(csv.DictReader(INPUT.open(encoding="utf-8")))
score_cols = [
    "Items Public","Labels Public","Scoring Method Public","Evaluation Code Public",
    "Construct Defined","Coverage Documented","Annotation Process Clear",
    "Limitations Stated","Versioning/Maintenance","License/Reuse Clear"
]
X = np.array([[float(r[c]) for c in score_cols] for r in rows])
base_totals = X.sum(axis=1)
base_ranks = rankdata(-base_totals, method="average")

rng = np.random.default_rng(SEED)
results = []

for sigma in SIGMAS:
    rhos = np.empty(N_SIMS)
    mean_abs_disp = np.empty(N_SIMS)

    for i in range(N_SIMS):
        perturbed = np.rint(X + rng.normal(0, sigma, size=X.shape))
        perturbed = np.clip(perturbed, 0, 2)

        totals = perturbed.sum(axis=1)
        ranks = rankdata(-totals, method="average")

        rhos[i] = spearmanr(base_totals, totals).statistic
        mean_abs_disp[i] = np.mean(np.abs(ranks - base_ranks))

    results.append({
        "sigma": sigma,
        "mean_spearman_rho": np.mean(rhos),
        "median_spearman_rho": np.median(rhos),
        "rho_2.5_percentile": np.quantile(rhos, 0.025),
        "rho_97.5_percentile": np.quantile(rhos, 0.975),
        "mean_absolute_rank_displacement": np.mean(mean_abs_disp),
        "proportion_rho_below_0.80": np.mean(rhos < 0.80),
    })

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
with OUTPUT.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys(), lineterminator="\n")
    writer.writeheader()
    writer.writerows(results)

for r in results:
    print(
        f"sigma={r['sigma']:.2f}: "
        f"mean rho={r['mean_spearman_rho']:.3f}, "
        f"95% simulation interval="
        f"[{r['rho_2.5_percentile']:.3f}, {r['rho_97.5_percentile']:.3f}], "
        f"mean abs rank displacement="
        f"{r['mean_absolute_rank_displacement']:.2f}"
    )
