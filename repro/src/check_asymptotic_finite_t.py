"""Independent finite-T calibration for the asymptotic step in Theorem 3.1."""

from __future__ import annotations

import math

import numpy as np
from scipy.special import betainc

import core


DIMENSIONS = tuple(2**power for power in range(1, 17))
EPSILONS = (0.25, 1.0, 4.0, 16.0)
DELTA = 1e-3


def sphere_coordinate_cdf(dimension: int, threshold: float) -> float:
    root = math.sqrt(dimension)
    if threshold <= -root:
        return 0.0
    if threshold >= root:
        return 1.0
    shape = (dimension - 1.0) / 2.0
    x = (threshold / root + 1.0) / 2.0
    return float(betainc(shape, shape, x))


def thresholds(u: float, dimension: int, epsilon: float, sensitivity: float = 1.0):
    root = math.sqrt(u)
    a = -epsilon * root / sensitivity + sensitivity / (2.0 * root)
    b = (
        -epsilon * root / sensitivity
        - sensitivity / (2.0 * root)
        - epsilon * sensitivity / (dimension * root)
    ) / (1.0 + 2.0 * epsilon / dimension)
    return a, b


def radial_laws(u0: float, dimension: int):
    rare = 1.0 / dimension
    low = 0.5 * u0
    high = (u0 - (1.0 - rare) * low) / rare
    return {
        "deterministic": [(1.0, u0)],
        "two_point": [(0.5, 0.5 * u0), (0.5, 1.5 * u0)],
        "heavy_tail_fixed": [(0.9, 0.1 * u0), (0.1, 9.1 * u0)],
        "rare_spike_T_dependent": [(1.0 - rare, low), (rare, high)],
    }


def run_finite_t_checker() -> dict:
    rows = []
    for epsilon in EPSILONS:
        u0 = core.gaussian_variance(DELTA, epsilon)
        for dimension in DIMENSIONS:
            for law_name, law in radial_laws(u0, dimension).items():
                mean_u = sum(weight * u for weight, u in law)
                gaussian_bound = sum(
                    weight * float(core.gaussian_delta(u, epsilon)) for weight, u in law
                )
                finite_test = 0.0
                for weight, u in law:
                    a, b = thresholds(u, dimension, epsilon)
                    finite_test += weight * (
                        sphere_coordinate_cdf(dimension, a)
                        - math.exp(epsilon) * sphere_coordinate_cdf(dimension, b)
                    )
                rows.append(
                    {
                        "epsilon": epsilon,
                        "delta": DELTA,
                        "dimension": dimension,
                        "radial_law": law_name,
                        "mean_u": mean_u,
                        "u0": u0,
                        "mean_constraint_residual": mean_u - u0,
                        "expected_gaussian_g": gaussian_bound,
                        "supporting_margin": gaussian_bound - DELTA,
                        "finite_T_test_lower_bound": finite_test,
                        "normal_limit_gap": finite_test - gaussian_bound,
                    }
                )

    last_rows = [row for row in rows if row["dimension"] == DIMENSIONS[-1]]
    first_rows = [row for row in rows if row["dimension"] == DIMENSIONS[0]]
    max_mean_residual = max(abs(row["mean_constraint_residual"]) for row in rows)
    min_supporting_margin = min(row["supporting_margin"] for row in rows)
    max_last_gap = max(abs(row["normal_limit_gap"]) for row in last_rows)
    max_first_gap = max(abs(row["normal_limit_gap"]) for row in first_rows)
    passed = (
        max_mean_residual < 1e-9
        and min_supporting_margin >= -1e-8
        and max_last_gap < 5e-4
        and max_last_gap < max_first_gap
    )
    return {
        "scope": {
            "dimensions": list(DIMENSIONS),
            "epsilons": list(EPSILONS),
            "delta": DELTA,
            "radial_laws": [
                "deterministic",
                "two_point",
                "heavy_tail_fixed",
                "rare_spike_T_dependent",
            ],
            "configuration_count": len(rows),
        },
        "rows": rows,
        "summary": {
            "max_mean_constraint_residual": max_mean_residual,
            "minimum_supporting_margin": min_supporting_margin,
            "max_abs_gap_T2": max_first_gap,
            "max_abs_gap_T65536": max_last_gap,
        },
        "passed": passed,
        "limitation": (
            "Scoped finite-T corroboration only. The universal claim is carried "
            "by the separate symbolic certificate."
        ),
    }
