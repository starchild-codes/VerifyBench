# Supplementary Materials

This directory contains supplementary documentation supporting the VerifyBench audit.

Recommended contents include:

- reconstructed benchmark-discovery record;
- inclusion and exclusion criteria;
- known exclusions;
- category-assignment notes;
- additional robustness tables or outputs that do not appear in the main paper;
- archived methodological notes needed to interpret the released scoring layers.

## Scope

The VerifyBench benchmark sample is purposive rather than statistically representative. Candidate discovery and screening were iterative and were not conducted under a preregistered systematic-review protocol. The discovery record is therefore a reconstructed transparency artifact rather than a claim of exhaustive search coverage.

## Source-of-truth rule

The final primary scores should always be taken from:

```text
../data/verifybench_primary_scores_canonical.csv
```

Reliability results should be regenerated from the files in:

```text
../reliability/
```

Sensitivity and robustness outputs should be regenerated from the scripts in:

```text
../analysis/
```

Earlier exploratory or pre-adjudication files should not be treated as canonical results.

## Evidence and third-party rights

Supplementary evidence records may contain URLs, short evidence summaries, and audit rationales referring to third-party benchmark materials. Those references do not transfer ownership or licensing rights over the underlying third-party resources.
