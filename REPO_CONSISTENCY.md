# VerifyBench Repository Consistency Note

This repository should use the following results as the final source of truth for the manuscript.

## Primary audit
- 30 benchmarks x 10 dimensions = 300 decisions
- Mean total score: 16.03 / 20
- Median: 16
- Range: 11-19
- Benchmarks scoring 18-20: 5

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
- Full lenient mean: 19.47; median 20; range 18-20; Spearman rho with primary: 0.325
- Operationalized mean: 15.97; median 16; range 12-19; Spearman rho with primary: 0.088

## Monte Carlo robustness
10,000 simulations per uncertainty level using fixed seed 20260813. Independent Gaussian perturbations were added to primary cell scores, then rounded to the nearest ordinal category and clipped to 0-2.

- sigma = 0.25: mean Spearman rho = 0.927; 95% simulation interval 0.846-0.979; mean absolute rank displacement = 1.96
- sigma = 0.50: mean Spearman rho = 0.664; 95% simulation interval 0.454-0.834; mean absolute rank displacement = 5.25

## Important version-control rule
Do not use earlier workbooks containing primary reliability values of 78.7% exact agreement or Cohen's kappa = 0.547 as final repository evidence. Those values are superseded by the final reliability files and the current manuscript.
