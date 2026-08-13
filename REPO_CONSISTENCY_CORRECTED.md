# VerifyBench Repository Consistency Note

This repository should use the following results as the final source of truth for the manuscript.

## Primary audit
- 30 benchmarks × 10 dimensions = 300 decisions
- Mean total score: 16.03 / 20
- Median: 16
- Range: 11–19
- Benchmarks scoring 18–20: 5

## Primary reliability
- Same purposive 15-benchmark subset, 150 paired decisions
- Exact agreement: 76.0%
- Cohen's kappa: 0.490
- Linear-weighted kappa: 0.508
- Primary disagreements were adjudicated; adjudicated values are used in the primary analysis.

## Operationalized reliability
- Same 15-benchmark subset and same coder pair
- Exact agreement: 78.0%
- Cohen's kappa: 0.574
- Linear-weighted kappa: 0.574

## Sensitivity analyses
- Full lenient mean: 19.47; median 20; range 18–20
- Lenient Spearman rho with primary: 0.325
- Lenient mean absolute rank displacement: 6.77
- Operationalized mean: 15.97; median 16; range 12–19
- Operationalized Spearman rho with primary: 0.088
- Operationalized mean absolute rank displacement: 9.23

## Deterministic robustness
Leave-one-dimension-out analysis was recomputed from the final canonical primary matrix using tied average ranks.

- Most influential removal: Evaluation Code Public
- Mean absolute rank displacement: 2.87 positions
- Spearman rho with the full equal-weight totals: 0.916

Alternative weighting stress tests currently released in `analysis/robustness_analysis.py` are explicit reproducibility-package scenarios rather than empirically estimated weights. Across the non-baseline scenarios, Spearman rho with the equal-weight primary ordering is 0.993–1.000.

## Monte Carlo robustness
10,000 simulations per uncertainty level using fixed seed 20260813. Independent Gaussian perturbations were added to primary cell scores, then rounded to the nearest ordinal category and clipped to 0–2.

- sigma = 0.10: mean Spearman rho ≈ 1.000; mean absolute rank displacement ≈ 0
- sigma = 0.25: mean Spearman rho = 0.927; 95% simulation interval 0.846–0.979; mean absolute rank displacement = 1.96
- sigma = 0.50: mean Spearman rho = 0.664; 95% simulation interval 0.454–0.834; mean absolute rank displacement = 5.25
- sigma = 0.75: mean Spearman rho = 0.517; 95% simulation interval 0.229–0.747; mean absolute rank displacement = 6.45
- sigma = 1.00: mean Spearman rho = 0.415; 95% simulation interval 0.101–0.686; mean absolute rank displacement = 7.21

The Monte Carlo analysis is a model-based stress test, not an empirical estimate of the true coder-error distribution.

## Evidence-record wording
The released evidence log contains dimension-specific evidence summaries and decision rationales. Unless a record is explicitly marked as verbatim, the repository and manuscript should not describe all 300 records as “verbatim evidence excerpts.”

## Important version-control rules
- Do not use earlier workbooks containing primary reliability values of 78.7% exact agreement or Cohen's kappa = 0.547 as final repository evidence.
- Do not use the earlier stale claim that removing License/Reuse Clear caused a mean absolute rank displacement of 6.1 positions.
- The current reproducible leave-one-dimension-out result is Evaluation Code Public, mean absolute rank displacement 2.87, rho 0.916.
- The canonical primary matrix remains `data/verifybench_primary_scores_canonical.csv`.
