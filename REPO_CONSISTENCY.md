# VerifyBench Camera-Ready Consistency Note

This file records the camera-ready source of truth for IEEE TPS 2026.

## Canonical matrices

- Primary: `data/verifybench_primary_scores_canonical.csv`
- Lenient: `data/lenient_scores.csv`
- Operationalized: `data/operationalized_scores.csv`

Do not alter these matrices to make derived results fit.

## Headline results

| Layer | Mean | Median | Range | Benchmarks scoring 18–20 | Totals changed from primary | Spearman ρ with primary | Mean absolute rank displacement |
|---|---:|---:|---:|---:|---:|---:|---:|
| Primary | 16.03 | 16 | 11–19 | 5 | — | 1.000 | 0.00 |
| Lenient | 19.47 | 20 | 18–20 | 30 | 29 | 0.325 | 6.77 |
| Operationalized | 15.97 | 16 | 12–19 | 6 | 26 | 0.088 | 9.23 |

Operationalized changes comprise 13 increases, 13 decreases, and 4 unchanged totals.

## Reliability and adjudication

- Primary, 150 paired decisions: 76.0% exact agreement; Cohen's κ = 0.490; linear-weighted κ = 0.508.
- Operationalized, the same 150 paired decisions: 78.0% exact agreement; Cohen's κ = 0.574; linear-weighted κ = 0.574.

Primary disagreements were adjudicated, and adjudicated values feed the primary analysis. For the operationalized layer, Coder 2 is used only for reliability estimation. Coder 1's frozen scores feed the complete 30-benchmark analysis. Operationalized disagreements were not converted into a consensus layer; the other 15 operationalized benchmarks were single-coded.

## Deterministic robustness

Removing Evaluation Code Public is the most influential leave-one-dimension-out test: mean absolute rank displacement = 2.87 and Spearman ρ with the full equal-weight ordering = 0.916.

Camera-ready Table III uses these five non-baseline scenarios; all unspecified dimensions retain weight 1.00:

| Scenario | Changed weights | Spearman ρ |
|---|---|---:|
| Reproduction | Items, Labels, Scoring Method, Evaluation Code = 1.25 | 0.994 |
| Documentation | Construct, Coverage, Annotation, Limitations = 1.25 | 0.993 |
| Lifecycle/reuse | Versioning/Maintenance, License/Reuse = 1.50 | 0.997 |
| Artifact access | Items, Labels = 1.50 | 1.000 |
| Operational completeness | Scoring Method, Evaluation Code, Limitations, Versioning/Maintenance, License/Reuse = 1.25 | 0.993 |

These are transparent sensitivity settings, not empirically estimated weights.

## Monte Carlo robustness

The canonical sigma grid is `{0.25, 0.43, 0.50, 0.75, 1.00}` with 10,000 simulations per sigma and seed `20260813`. Independent Gaussian cell perturbations are rounded to the nearest ordinal category and clipped to [0, 2]. Tied average ranks, Spearman correlation with unperturbed primary totals, mean absolute rank displacement, and the central 95% simulation interval are reported.

Sigma 0.43 heuristically calibrates the ±0.5 threshold-crossing probability to the primary exercise's 24% coder-disagreement rate. Sigma 0.10 is excluded because it almost never changes a rounded score. Boundary clipping is asymmetric at 0 and 2, so this is a model-based stress test rather than an empirical coder-error model.

The observed primary-to-operationalized ρ = 0.088 is much lower than the Monte Carlo mean ρ at σ = 1.00 (about 0.414). The tested random-noise model therefore cannot explain the implemented protocol shift.

The repository implementation uses one NumPy `default_rng` stream consumed sequentially in sigma order. Regeneration produces:

| Sigma | Mean ρ | Central 95% interval | Mean absolute rank displacement |
|---:|---:|---:|---:|
| 0.25 | 0.928 | 0.848–0.979 | 1.95 |
| 0.43 | 0.716 | 0.519–0.863 | 4.77 |
| 0.50 | 0.664 | 0.454–0.834 | 5.25 |
| 0.75 | 0.517 | 0.229–0.747 | 6.45 |
| 1.00 | 0.415 | 0.101–0.686 | 7.21 |

The manuscript-rounded targets for the first three rows were 0.927 (0.847–0.980; 1.95), 0.719 (0.529–0.861; 4.75), and 0.662 (0.444–0.830; 5.25). The mismatch is retained and disclosed rather than resolved by hand-editing generated numbers.

## Figures

The camera-ready paper maps to four canonical outputs: `figures/fig1.png` through `figures/fig4.png`. Any older fifth figure is legacy and not part of the final paper mapping.
