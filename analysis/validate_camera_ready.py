#!/usr/bin/env python3
"""Validate generated VerifyBench camera-ready outputs.

Run this script from the repository root after regenerating all analyses and
figures. It reads generated outputs and fails with a non-zero exit code when a
camera-ready invariant drifts.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def close(actual: float, expected: float, tolerance: float, label: str) -> None:
    require(
        math.isclose(actual, expected, abs_tol=tolerance, rel_tol=0.0),
        f"{label}: expected {expected} +/- {tolerance}, found {actual}",
    )


summary = {row["Layer"]: row for row in read_csv(RESULTS / "summary_statistics.csv")}
close(float(summary["Primary"]["Mean Total"]), 16.03, 0.005, "Primary mean")
close(float(summary["Lenient"]["Mean Total"]), 19.47, 0.005, "Lenient mean")
close(float(summary["Operationalized"]["Mean Total"]), 15.97, 0.005, "Operationalized mean")

reliability = {row["Layer"]: row for row in read_csv(RESULTS / "reliability_results.csv")}
close(float(reliability["Primary"]["Exact Agreement"]), 0.760, 0.0005, "Primary agreement")
close(float(reliability["Primary"]["Cohen Kappa"]), 0.490, 0.0005, "Primary kappa")
close(float(reliability["Operationalized"]["Exact Agreement"]), 0.780, 0.0005, "Operationalized agreement")
close(float(reliability["Operationalized"]["Cohen Kappa"]), 0.574, 0.0005, "Operationalized kappa")

sensitivity = {row["Layer"]: row for row in read_csv(RESULTS / "sensitivity_results.csv")}
close(float(sensitivity["Operationalized"]["Spearman Rho with Primary"]), 0.088, 0.0005, "Primary-to-operationalized rho")
close(float(sensitivity["Lenient"]["Spearman Rho with Primary"]), 0.325, 0.0005, "Primary-to-lenient rho")

loo_rows = read_csv(RESULTS / "leave_one_dimension_out.csv")
most_influential = max(loo_rows, key=lambda row: float(row["Mean Absolute Rank Displacement"]))
require(most_influential["Removed Dimension"] == "Evaluation Code Public", "Unexpected most influential leave-one-out dimension")
close(float(most_influential["Spearman Rho with Primary"]), 0.916, 0.0005, "Leave-one-out rho")
close(float(most_influential["Mean Absolute Rank Displacement"]), 2.87, 0.005, "Leave-one-out MAD")

expected_weighting_rhos = {
    "Baseline": 1.000,
    "Reproduction": 0.994,
    "Documentation": 0.993,
    "Lifecycle/reuse": 0.997,
    "Artifact access": 1.000,
    "Operational completeness": 0.993,
}
weighting = {row["Scenario"]: row for row in read_csv(RESULTS / "alternative_weighting.csv")}
require(set(weighting) == set(expected_weighting_rhos), f"Unexpected weighting scenarios: {sorted(weighting)}")
for scenario, expected_rho in expected_weighting_rhos.items():
    close(float(weighting[scenario]["Spearman Rho with Primary"]), expected_rho, 0.0005, f"{scenario} rho")

monte_carlo = read_csv(RESULTS / "monte_carlo_results.csv")
sigmas = {round(float(row["sigma"]), 2) for row in monte_carlo}
require(sigmas == {0.25, 0.43, 0.50, 0.75, 1.00}, f"Unexpected Monte Carlo sigma grid: {sorted(sigmas)}")
require(0.10 not in sigmas, "Canonical Monte Carlo output still contains sigma=0.10")
expected_mc_means = {
    0.25: 0.9276144141,
    0.43: 0.7163891850,
    0.50: 0.6635566923,
    0.75: 0.5168601003,
    1.00: 0.4148242676,
}
for row in monte_carlo:
    sigma = round(float(row["sigma"]), 2)
    close(float(row["mean_spearman_rho"]), expected_mc_means[sigma], 1e-9, f"Monte Carlo mean rho at sigma={sigma:.2f}")

for number in range(1, 5):
    figure = FIGURES / f"fig{number}.png"
    require(figure.is_file() and figure.stat().st_size > 0, f"Missing camera-ready figure: {figure}")

print("Camera-ready validation passed.")
