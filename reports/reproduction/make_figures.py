"""Render the five evidence figures used by the public reproduction report."""

from __future__ import annotations

import json
import os
from pathlib import Path

for name in (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
    "NUMEXPR_NUM_THREADS",
):
    os.environ[name] = "1"

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
IMAGES = Path(__file__).parent / "images"
IMAGES.mkdir(parents=True, exist_ok=True)
COLORS = {"navy": "#17324d", "blue": "#2c7fb8", "gold": "#f0a202", "red": "#c44536"}


def load_claim(path: str, identifier: str):
    payload = json.loads((ROOT / path).read_text())
    claims = payload.get("claims", [])
    if "claim" in payload:
        claims = [payload["claim"]]
    return next(item for item in claims if item["id"] == identifier)


def finish(name: str):
    plt.tight_layout()
    plt.savefig(IMAGES / name, dpi=180, bbox_inches="tight")
    plt.close()


composition = load_claim(
    "space/artifacts/claim6/raw_output.json", "C5-ALGORITHM7"
)["evidence"]["figure3"]
k = np.array([row["compositions"] for row in composition])
seq = np.array([row["sequential_mse"] for row in composition])
fft = np.array([row["fft_mse"] for row in composition])
plt.figure(figsize=(8.5, 4.8))
plt.plot(k, seq, "o-", color=COLORS["red"], linewidth=2.4, label="Sequential")
plt.plot(k, fft, "o-", color=COLORS["blue"], linewidth=2.4, label="Algorithm 7")
plt.yscale("log")
plt.xticks(k)
plt.xlabel("Number of invocations k")
plt.ylabel("Required per-invocation MSE (log scale)")
plt.title("Tight composition sharply lowers the noise required")
plt.grid(alpha=0.22)
plt.legend(frameon=False)
finish("headline-composition.png")


figure2 = load_claim(
    "space/artifacts/claim4/raw_output.json", "C3-INDEPENDENT"
)["evidence"]["rows"]
dims = np.array([row["dimension"] for row in figure2])
means = 100 * np.array([row["mean_reduction"] for row in figure2])
half = 100 * np.array([row["reduction_95_half_width"] for row in figure2])
plt.figure(figsize=(7.2, 4.5))
plt.errorbar(
    dims,
    means,
    yerr=half,
    fmt="o-",
    capsize=5,
    color=COLORS["blue"],
    linewidth=2.4,
)
plt.axhline(0, color="black", linewidth=0.8)
plt.xticks(dims)
plt.xlabel("Dimension T")
plt.ylabel("MSE reduction vs Gaussian (%)")
plt.title("The low-dimensional SGG advantage shrinks with dimension")
plt.grid(alpha=0.22)
finish("figure2-qmc.png")


theorem = load_claim(
    "space/artifacts/claim1/raw_output.json", "C0-FINITE-T"
)["evidence"]["rows"]
by_dimension: dict[int, float] = {}
for row in theorem:
    dimension = int(row["dimension"])
    by_dimension[dimension] = max(
        by_dimension.get(dimension, 0.0), abs(row["normal_limit_gap"])
    )
tdims = np.array(sorted(by_dimension))
gaps = np.array([by_dimension[value] for value in tdims])
plt.figure(figsize=(7.5, 4.5))
plt.loglog(tdims, gaps, "o-", color=COLORS["navy"], linewidth=2.2, markersize=4)
plt.axhline(5e-4, color=COLORS["gold"], linestyle="--", label="Declared final gate")
plt.xlabel("Dimension T")
plt.ylabel("Worst absolute finite-sphere / Gaussian gap")
plt.title("The exact finite-sphere test approaches its Gaussian limit")
plt.grid(alpha=0.22, which="both")
plt.legend(frameon=False)
finish("theorem-convergence.png")


eps = np.array([0.25, 0.5, 1, 2, 4, 8, 16])
delta_star = np.array([0.736670, 0.706970, 0.649185, 0.549133, 0.416972, 0.292170, 0.197615])
plt.figure(figsize=(7.2, 4.5))
plt.semilogx(eps, delta_star, "o-", color=COLORS["blue"], linewidth=2.3)
plt.xlabel("epsilon (log scale)")
plt.ylabel("Published lower bound on delta-star")
plt.title("All seven Table 2 thresholds pass the supporting-line audit")
plt.grid(alpha=0.22)
finish("table2-thresholds.png")


windows = np.array([32, 64, 96])
cropped = np.array([0.13951135987808705, 0.0006640385199706555, 7.622384852190578e-7])
plt.figure(figsize=(7.2, 4.5))
plt.semilogy(windows, cropped, "o-", color=COLORS["gold"], linewidth=2.3)
plt.axhline(2e-5, color=COLORS["red"], linestyle="--", label="Predeclared clipping gate")
plt.xticks(windows)
plt.xlabel("Composition truncation half-width L")
plt.ylabel("Worst cropped mass (log scale)")
plt.title("Calibrated truncation exposes and removes FFT clipping")
plt.grid(alpha=0.22, which="both")
plt.legend(frameon=False)
finish("truncation-calibration.png")
