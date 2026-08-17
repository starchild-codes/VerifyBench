# VerifyBench

VerifyBench is a structured audit of **public verifiability** in responsible-AI benchmarks for language and foundation models.

The study evaluates 30 benchmarks across 10 public-verifiability dimensions using a 0–2 ordinal rubric, yielding 300 benchmark-dimension decisions per scoring layer. The repository contains the final primary/adjudicated scores, two complete post-hoc rescoring layers, reliability records, evidence summaries, analysis scripts, robustness analyses, generated figures, and supplementary materials used to reproduce the paper's reported results.

## Repository structure

```text
VerifyBench/
├── README.md
├── REPO_CONSISTENCY.md
├── LICENSE
├── CITATION.cff
├── requirements.txt
│
├── data/
│   ├── VerifyBench_Final_Primary_Adjudicated_30x10.xlsx
│   ├── verifybench_primary_scores_canonical.csv
│   ├── lenient_scores.csv
│   ├── operationalized_scores.csv
│   ├── benchmark_list.csv
│   └── evidence_log.csv
│
├── rubrics/
│   ├── primary_rubric.md
│   └── operationalized_rubric.md
│
├── reliability/
│   ├── coder1_primary.csv
│   ├── coder2_primary.csv
│   ├── primary_adjudicated.csv
│   ├── coder1_operationalized.csv
│   └── coder2_operationalized.csv
│
├── analysis/
│   ├── descriptive_analysis.py
│   ├── reliability_analysis.py
│   ├── sensitivity_analysis.py
│   ├── robustness_analysis.py
│   ├── monte_carlo_robustness.py
│   └── generate_figures.py
│
├── results/
│   ├── summary_statistics.csv
│   ├── dimension_means.csv
│   ├── category_means.csv
│   ├── reliability_results.csv
│   ├── operationalized_dimension_agreement.csv
│   ├── sensitivity_results.csv
│   ├── benchmark_level_sensitivity.csv
│   ├── leave_one_dimension_out.csv
│   ├── alternative_weighting.csv
│   └── monte_carlo_results.csv
│
├── figures/
│   ├── fig1.png
│   ├── fig2.png
│   ├── fig3.png
│   ├── fig4.png
│   └── fig5.png
│
└── supplement/
    ├── README.md
    └── verifybench_analysis_package.xlsx
```

## Canonical source of truth

The canonical primary score matrix is:

```text
data/verifybench_primary_scores_canonical.csv
```

It contains the final adjudicated 30 × 10 primary matrix used for the manuscript. It reproduces:

- mean total score: **16.03 / 20**
- median: **16**
- range: **11–19**
- benchmarks scoring 18–20: **5**

The final lenient and operationalized layers reproduce:

| Layer | Mean | Median | Range | Benchmarks scoring 18–20 |
|---|---:|---:|---:|---:|
| Primary | 16.03 | 16 | 11–19 | 5 |
| Lenient | 19.47 | 20 | 18–20 | 30 |
| Operationalized | 15.97 | 16 | 12–19 | 6 |

Do not substitute earlier working spreadsheets for the canonical primary matrix.

## Reliability

The same purposive 15-benchmark subset (150 benchmark-dimension decisions) was independently coded by the same coder pair under both rubrics.

Primary rubric:

- exact agreement: **76.0%**
- Cohen's κ: **0.490**
- linear-weighted κ: **0.508**

Operationalized rubric:

- exact agreement: **78.0%**
- Cohen's κ: **0.574**
- linear-weighted κ: **0.574**

The operationalized exercise occurred later, so the difference should not be interpreted as a causal estimate of the effect of rubric wording alone.

## Sensitivity analysis

Two complete post-hoc rescoring layers were applied to all 300 benchmark-dimension cells.

The lenient artifact-presence interpretation produced:

- mean: **19.47**
- 29 of 30 totals changed from primary
- Spearman's ρ with primary: **0.325**
- mean absolute rank displacement: **6.77**

The operationalized interpretation produced:

- mean: **15.97**
- 26 of 30 totals changed from primary
- Spearman's ρ with primary: **0.088**
- mean absolute rank displacement: **9.23**

## Deterministic robustness analysis

Leave-one-dimension-out analysis was recomputed from the final canonical 30 × 10 primary matrix using tied average ranks.

The most influential single-dimension removal was:

- removed dimension: **Evaluation Code Public**
- mean absolute rank displacement: **2.87 positions**
- Spearman's ρ with the full equal-weight totals: **0.916**

The explicit alternative-weighting stress tests in `analysis/robustness_analysis.py` produced rank correlations of **0.993–1.000** with the equal-weight primary ordering across the non-baseline scenarios.

These weighting scenarios are transparent sensitivity tests defined in the released reproducibility package; they are not empirically estimated importance weights.

## Monte Carlo robustness analysis

The Monte Carlo stress test uses the final adjudicated 30 × 10 primary matrix.

For each uncertainty level, independent zero-mean Gaussian perturbations are added to every cell, perturbed values are rounded to the nearest valid ordinal score and clipped to the 0–2 rubric range, and benchmark totals/ranks are recomputed.

The analysis uses:

- σ ∈ {0.10, 0.25, 0.50, 0.75, 1.00}
- 10,000 simulations per σ
- fixed random seed: `20260813`

Selected results:

- σ = 0.25: mean Spearman's ρ = **0.927**, mean absolute rank displacement = **1.96**
- σ = 0.50: mean Spearman's ρ = **0.664**, mean absolute rank displacement = **5.25**

The simulation is a model-based stress test, not an empirical estimate of the true distribution of coder error.

## Evidence log

`data/evidence_log.csv` contains one row for each of the 300 benchmark-dimension cells and links the three scoring layers to the available evidence record.

Fields include:

- benchmark and category
- dimension
- primary score
- lenient score
- operationalized score
- evidence source URLs
- general evidence note
- dimension-specific evidence summary
- lenient decision rationale
- operationalized decision rationale
- evidence-review date where available
- evidence status

Evidence summaries are provided as audit records. They should not be interpreted as complete reproductions of third-party benchmark documentation or as verbatim excerpts unless explicitly marked as such.

## Reproducing the analyses

Create an environment and install dependencies:

```bash
python -m venv .venv
```

Activate it using the command appropriate for your operating system, then run:

```bash
pip install -r requirements.txt
```

From the repository root:

```bash
python analysis/descriptive_analysis.py
python analysis/reliability_analysis.py
python analysis/sensitivity_analysis.py
python analysis/robustness_analysis.py
python analysis/monte_carlo_robustness.py
python analysis/generate_figures.py
```

Generated tables are written to `results/`; figures are written to `figures/`.

## Important methodological notes

The 30-benchmark sample is purposive and was intentionally capped to support manual evidence retrieval and cell-level assessment. It is not a representative census of all responsible-AI benchmarks.

The operationalized rescoring was post-hoc and involved renewed examination of public evidence. Differences from the primary layer may therefore reflect both changed evidentiary thresholds and newly located evidence.

The equal-weight total is a transparent descriptive summary rather than a validated latent measure. Benchmark-level ranks should not be interpreted as precise league-table positions.

## Third-party materials

This repository records public evidence about third-party benchmarks. It does not claim ownership of those benchmarks, their datasets, source code, documentation, or other third-party materials. Original licenses and terms continue to govern those materials.

## Citation

Citation metadata are provided in `CITATION.cff`.

