# VerifyBench Primary Public-Verifiability Rubric

This file reproduces the primary 10-dimension scoring rubric used in the VerifyBench audit.

Each benchmark-dimension pair receives an ordinal score of **0, 1, or 2**. The 10 dimension scores are summed with equal weight to produce a total Public Verifiability Score from **0 to 20**.

| Dimension | Score 0 | Score 1 | Score 2 | Coding note |
|---|---|---|---|---|
| Items Public | No benchmark items available | Partial examples only / access unclear | Full items/prompts/questions are publicly inspectable | For harmful/safety datasets, code as public if documented, but do not inspect raw harmful examples. |
| Labels Public | No labels/gold answers | Partial/unclear labels | Labels/gold answers are public | Includes gold labels, answers, toxicity scores, refusal labels, etc. |
| Scoring Method Public | No scoring method | Vague or partial scoring description | Clear metric/formula/procedure | Can another researcher understand how score is computed? |
| Evaluation Code Public | No code/tooling | Partial, stale, or third-party code only | Maintained official code/tooling | Do not require code to run during the primary audit; verify public presence. |
| Construct Defined | No definition of measured construct | Implied or vague construct | Explicit construct definition | Constructs include bias, fairness, toxicity, truthfulness, safety, etc. |
| Coverage Documented | No coverage information | Some categories listed | Clear groups/languages/harms/domains/categories | This dimension captures whether the benchmark's evaluated scope is publicly documented. |
| Annotation Process Clear | No annotation details | Partial annotator/process detail | Instructions/demographics/agreement or validation clear | If synthetic/no annotation, code based on provenance transparency. |
| Limitations Stated | No limitations | Generic limitations | Specific scope/use limitations | Important for responsible interpretation. |
| Versioning/Maintenance | No version/update info | Partial/unclear versioning | Clear versioning, releases, living benchmark, or maintained repo | GitHub releases or website updates count. |
| License/Reuse Clear | No license/reuse terms | Ambiguous/partial | Clear license or reuse terms | Legal auditability matters. |

## Interpretation

The primary rubric was designed as an exploratory instrument for broad evidence availability. A score of 2 indicates that the relevant evidence was sufficiently supported under the primary full-credit criterion; it does **not** imply that the benchmark is scientifically valid, high quality, legally unrestricted, or fully reproducible in every environment.

The primary rubric is retained as the original empirical baseline of the VerifyBench audit. A later operationalized rubric introduced more explicit dimension-specific evidentiary requirements and was used for sensitivity and reliability analyses.
