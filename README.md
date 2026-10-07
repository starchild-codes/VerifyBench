# VerifyBench

VerifyBench is the camera-ready reproducibility package for *VerifyBench: Auditing Public Verifiability in Responsible-AI Benchmarks for Foundation Models* (IEEE TPS 2026). It audits 30 responsible-AI benchmarks across 10 public-verifiability dimensions using a 0–2 ordinal rubric, for 300 benchmark-dimension decisions per complete scoring layer.

The repository includes the adjudicated primary layer, post-hoc lenient artifact-presence and operationalized layers, reliability records, deterministic and Monte Carlo robustness analyses, evidence records, and the four camera-ready paper figures.

## Sampling scope

The 30-benchmark sample is purposive, cross-category, and predominantly language-focused. VHELM was deliberately included as a multimodal/foundation-model case. The study does not claim systematic coverage of multimodal evaluation or a representative census of responsible-AI benchmarks.

## Repository structure

```text
VerifyBench/
├── README.md
├── REPO_CONSISTENCY.md
├── CHANGELOG.md
├── CITATION.cff
├── requirements.txt
├── data/
│   ├── verifybench_primary_scores_canonical.csv
│   ├── lenient_scores.csv
│   ├── operationalized_scores.csv
│   ├── benchmark_list.csv
│   └── evidence_log.csv
├── reliability/
├── rubrics/
├── analysis/
│   ├── descriptive_analysis.py
│   ├── reliability_analysis.py
│   ├── sensitivity_analysis.py
│   ├── robustness_analysis.py
│   ├── monte_carlo_robustness.py
│   ├── generate_figures.py
│   └── validate_camera_ready.py
├── results/
├── figures/
│   ├── fig1.png
│   ├── fig2.png
│   ├── fig3.png
│   ├── fig4.png
│   └── legacy/fig5_draft_sensitivity_overview.png
└── supplement/
    ├── README.md
    ├── verifybench_analysis_package_camera_ready.xlsx
    └── verifybench_analysis_package.xlsx
```

The older workbook and draft figure are retained only as labeled legacy artifacts. They are not the camera-ready source of truth.

## Canonical score matrices

The canonical primary matrix is `data/verifybench_primary_scores_canonical.csv`. The complete alternative layers are `data/lenient_scores.csv` and `data/operationalized_scores.csv`.

| Layer | Mean | Median | Range | Benchmarks scoring 18–20 |
|---|---:|---:|---:|---:|
| Primary | 16.03 | 16 | 11–19 | 5 |
| Lenient | 19.47 | 20 | 18–20 | 30 |
| Operationalized | 15.97 | 16 | 12–19 | 6 |

## Reliability and analysis layers

The same purposive 15-benchmark subset (150 benchmark-dimension decisions) was independently coded by the same coder pair under both rubrics.

| Layer | Exact agreement | Cohen's κ | Linear-weighted κ |
|---|---:|---:|---:|
| Primary | 76.0% | 0.490 | 0.508 |
| Operationalized | 78.0% | 0.574 | 0.574 |

Primary disagreements in the double-coded subset were adjudicated, and those adjudicated values feed the complete primary analysis. In the operationalized exercise, Coder 2 ratings are used for reliability estimation only. Coder 1's frozen operationalized scores form the complete 30-benchmark operationalized analysis layer. Operationalized disagreements were not converted into a separate consensus or adjudicated layer; the remaining 15 operationalized benchmarks were single-coded.

## Post-hoc sensitivity layers

Both alternative scoring layers are post-hoc. The lenient layer was single-coded. The operationalized round occurred later and involved renewed examination of public sources. Primary-to-operationalized differences may therefore reflect changed evidentiary thresholds, newly located evidence, and coder familiarity. They are not a causal estimate of rubric wording alone.

The lenient layer changed 29 of 30 totals, with Spearman's ρ = 0.325 and mean absolute rank displacement = 6.77. The operationalized layer changed 26 of 30 totals (13 increased, 13 decreased, and 4 were unchanged), with Spearman's ρ = 0.088 and mean absolute rank displacement = 9.23.

## Deterministic robustness

The leave-one-dimension-out analysis uses tied average ranks. Removing Evaluation Code Public is most influential: mean absolute rank displacement = 2.87 and Spearman's ρ with the full equal-weight ordering = 0.916.

Table III uses the following transparent sensitivity scenarios. All unspecified dimensions retain weight 1.00; these settings are not empirically estimated importance weights.

| Scenario | Changed weights | Spearman's ρ with primary |
|---|---|---:|
| Baseline | all dimensions = 1.00 | 1.000 |
| Reproduction | Items, Labels, Scoring Method, Evaluation Code = 1.25 | 0.994 |
| Documentation | Construct, Coverage, Annotation, Limitations = 1.25 | 0.993 |
| Lifecycle/reuse | Versioning/Maintenance, License/Reuse = 1.50 | 0.997 |
| Artifact access | Items, Labels = 1.50 | 1.000 |
| Operational completeness | Scoring Method, Evaluation Code, Limitations, Versioning/Maintenance, License/Reuse = 1.25 | 0.993 |

## Monte Carlo robustness

The Monte Carlo stress test adds independent zero-mean Gaussian noise to every cell of the adjudicated primary 30 × 10 matrix, rounds to the nearest ordinal category, clips scores to [0, 2], and recomputes tied average ranks. Spearman correlation is measured against the unperturbed primary totals. Each sigma uses 10,000 simulations, fixed seed `20260813`, and the central 95% simulation interval.

The camera-ready grid is σ ∈ {0.25, 0.43, 0.50, 0.75, 1.00}. Sigma 0.43 is a heuristic calibration to the primary exercise's 24% coder-disagreement rate: for an interior ordinal category, Gaussian noise crosses a ±0.5 rounding threshold with probability about 0.24 when σ is approximately 0.43. Sigma 0.10 was removed because it almost never changes a rounded ordinal score.

Boundary clipping at 0 and 2 makes perturbations asymmetric for saturated dimensions. This analysis is therefore a model-based stress test, not an empirical model of coder error. The observed primary-to-operationalized ρ of 0.088 is substantially lower than the Monte Carlo mean ρ at σ = 1.00 (about 0.414), so the tested random-noise model does not explain the implemented protocol shift.

The deterministic repository implementation uses one NumPy `default_rng` stream, consumed sequentially in the sigma order above. Its regenerated results are:

| Sigma | Mean ρ | Central 95% simulation interval | Mean absolute rank displacement |
|---:|---:|---:|---:|
| 0.25 | 0.928 | 0.848–0.979 | 1.95 |
| 0.43 | 0.716 | 0.519–0.863 | 4.77 |
| 0.50 | 0.664 | 0.454–0.834 | 5.25 |
| 0.75 | 0.517 | 0.229–0.747 | 6.45 |
| 1.00 | 0.415 | 0.101–0.686 | 7.21 |

These deterministic values differ slightly from several manuscript-rounded entries; the generated CSV is not hand-edited. See `REPO_CONSISTENCY.md` for the explicit discrepancy note.

## Camera-ready figures

- `figures/fig1.png`: primary and operationalized mean scores across all 10 dimensions.
- `figures/fig2.png`: 30 × 10 primary score heatmap.
- `figures/fig3.png`: descriptive category mean primary total scores.
- `figures/fig4.png`: three-layer aggregate and benchmark-level sensitivity overview.

The camera-ready paper uses these four figures. `figures/legacy/fig5_draft_sensitivity_overview.png` preserves the older draft mapping and is not a paper figure.

## Reproducing the analyses

Create and activate a Python 3.10+ environment, then install dependencies:

```bash
python -m venv .venv
pip install -r requirements.txt
```

From the repository root, run one command per script:

```bash
python analysis/descriptive_analysis.py
python analysis/reliability_analysis.py
python analysis/sensitivity_analysis.py
python analysis/robustness_analysis.py
python analysis/monte_carlo_robustness.py
python analysis/generate_figures.py
python analysis/validate_camera_ready.py
```

Generated tables are written to `results/`; figures are written to `figures/`. The validator checks the published headline values, weighting scenarios, Monte Carlo grid, and four canonical figures.

## Evidence records and interpretation

`data/evidence_log.csv` contains one record per benchmark-dimension cell linking the three scoring layers to available public evidence and decision rationales. These summaries are audit records, not complete reproductions of third-party documentation and not verbatim excerpts unless explicitly marked.

The equal-weight total is a transparent descriptive summary rather than a validated latent measure. Benchmark ranks should not be interpreted as precise league-table positions. Original licenses and terms govern all third-party benchmark materials.

## Citation

Citation metadata are provided in `CITATION.cff`.
