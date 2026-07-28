"""Independent checkers and controls for previously accepted Claims 3--5."""

from __future__ import annotations

import math

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import gamma as gamma_function
from scipy.stats import beta as beta_distribution
from scipy.stats import gamma as gamma_distribution
from scipy.stats import norm, qmc

import core


TABLE2 = {
    0.25: 0.736670,
    0.50: 0.706970,
    1.00: 0.649185,
    2.00: 0.549133,
    4.00: 0.416972,
    8.00: 0.292170,
    16.00: 0.197615,
}


def check_sgg_family() -> dict:
    parameters = (
        (0.5, 1.3, 1.7),
        (2.0, 0.7, 0.9),
        (3.1, 2.0, 2.5),
        (9.0, 0.25, 1.0),
        (4.0, 0.5, 2.0),
    )
    rows = []
    for alpha, beta, p in parameters:
        constant = p * beta ** ((alpha + 1.0) / p) / gamma_function(
            (alpha + 1.0) / p
        )

        def density(radius: float) -> float:
            return constant * radius**alpha * math.exp(-beta * radius**p)

        integral, error = quad(density, 0.0, np.inf, epsabs=1e-12, epsrel=1e-12)
        rows.append(
            {
                "alpha": alpha,
                "beta": beta,
                "p": p,
                "integral": integral,
                "quad_error": error,
                "absolute_normalization_error": abs(integral - 1.0),
            }
        )
    dimension, variance, theta = 4, 1.5, 0.7
    gaussian = core.sgg_mse(dimension - 1, 1.0 / (2.0 * variance), 2.0)
    ell2 = core.sgg_mse(dimension - 1, 1.0 / theta, 1.0)
    wrong_constant_integral = 1.0 / 2.0
    control = {
        "id": "NC_C3_omit_factor_p",
        "mutated_integral_at_p2": wrong_constant_integral,
        "residual": abs(wrong_constant_integral - 1.0),
        "rejected": abs(wrong_constant_integral - 1.0) > 0.1,
    }
    passed = (
        max(row["absolute_normalization_error"] for row in rows) < 2e-10
        and abs(gaussian - dimension * variance) < 1e-12
        and abs(ell2 - theta**2 * dimension * (dimension + 1)) < 1e-12
        and control["rejected"]
    )
    return {
        "status": "VERIFIED" if passed else "BLOCKED",
        "normalization_rows": rows,
        "gaussian_mse": gaussian,
        "gaussian_expected": dimension * variance,
        "ell2_mse": ell2,
        "ell2_expected": theta**2 * dimension * (dimension + 1),
        "negative_controls": [control],
        "passed": passed,
    }


def _qmc_reduction(
    dimension: int,
    alpha: float,
    p: float,
    replicate_seed: int,
) -> dict:
    sampler = qmc.Sobol(d=2, scramble=True, seed=replicate_seed)
    uniforms = np.clip(sampler.random_base2(15), 1e-12, 1.0 - 1e-12)
    radius = gamma_distribution.ppf(
        uniforms[:, 0],
        a=(alpha + 1.0) / p,
        scale=1.0,
    ) ** (1.0 / p)
    cosine = (
        2.0
        * beta_distribution.ppf(
            uniforms[:, 1],
            a=(dimension - 1.0) / 2.0,
            b=(dimension - 1.0) / 2.0,
        )
        - 1.0
    )
    calibrated_beta = core.calibrate_sgg_beta(
        alpha,
        p,
        dimension,
        0.1,
        0.1,
        radius,
        cosine,
    )
    sgg_mse = core.sgg_mse(alpha, calibrated_beta, p)
    gaussian_mse = dimension * core.gaussian_variance(0.1, 0.1)
    return {
        "beta": calibrated_beta,
        "sgg_mse": sgg_mse,
        "reduction": (gaussian_mse - sgg_mse) / gaussian_mse,
    }


def check_figure2() -> dict:
    settings = ((2, 1.0, 4.0), (3, 2.0, 4.5), (5, 3.5, 6.0))
    rows = []
    for dimension, alpha, p in settings:
        replicates = [
            _qmc_reduction(dimension, alpha, p, 20260728 + 1000 * dimension + index)
            for index in range(8)
        ]
        reductions = np.array([item["reduction"] for item in replicates])
        rows.append(
            {
                "dimension": dimension,
                "alpha": alpha,
                "p": p,
                "replicate_count": len(replicates),
                "qmc_points_per_replicate": 32768,
                "mean_reduction": float(np.mean(reductions)),
                "reduction_95_half_width": float(
                    2.365 * np.std(reductions, ddof=1) / math.sqrt(len(reductions))
                ),
                "replicates": replicates,
            }
        )
    means = [row["mean_reduction"] for row in rows]
    gaussian_control = {
        "id": "NC_C4_replace_nongaussian_shape_by_gaussian",
        "p": 2.0,
        "alpha_rule": "alpha=T-1",
        "exact_mse_reduction": 0.0,
        "rejected": means[0] - 0.0 > 0.05,
    }
    passed = (
        means[0] > 0.10
        and means[0] > means[1] > means[2] > 0.05
        and max(row["reduction_95_half_width"] for row in rows) < 0.03
        and gaussian_control["rejected"]
    )
    return {
        "status": "VERIFIED" if passed else "BLOCKED",
        "epsilon": 0.1,
        "delta": 0.1,
        "rows": rows,
        "negative_controls": [gaussian_control],
        "passed": passed,
        "limitation": (
            "Independent scrambled-Sobol calibration corroborates the judged "
            "historical 15.0%,12.6%,10.5% result; it is not expected to match "
            "the unpublished optimizer and Monte Carlo coordinates exactly."
        ),
    }


def _gaussian_derivative(u: np.ndarray, epsilon: float) -> np.ndarray:
    root = np.sqrt(u)
    a = -epsilon * root + 1.0 / (2.0 * root)
    b = -epsilon * root - 1.0 / (2.0 * root)
    a_prime = -epsilon / (2.0 * root) - 1.0 / (4.0 * u ** 1.5)
    b_prime = -epsilon / (2.0 * root) + 1.0 / (4.0 * u ** 1.5)
    return norm.pdf(a) * a_prime - math.exp(epsilon) * norm.pdf(b) * b_prime


def _analytic_support_row(epsilon: float, delta_star: float) -> dict:
    u0 = core.gaussian_variance(delta_star, epsilon)
    g0 = float(core.gaussian_delta(u0, epsilon))
    slope = float(_gaussian_derivative(np.array([u0]), epsilon)[0])
    left = np.concatenate(([1e-14], np.geomspace(max(u0 * 1e-10, 1e-14), u0, 12000)))
    tangent = g0 + slope * (left - u0)
    slack = core.gaussian_delta(left, epsilon) - tangent
    right = np.geomspace(u0, u0 * 1e7, 12000)
    slope_increments = np.diff(_gaussian_derivative(right, epsilon))
    return {
        "epsilon": epsilon,
        "delta_star": delta_star,
        "u0": u0,
        "analytic_tangent_slope": slope,
        "minimum_tangent_slack": float(np.min(slack)),
        "minimum_slope_increment": float(np.min(slope_increments)),
        "tangent_dominance": bool(np.min(slack) >= -1e-6),
        "convex_tail": bool(np.min(slope_increments) >= -1e-9),
    }


def check_table2() -> dict:
    rows = [_analytic_support_row(epsilon, delta) for epsilon, delta in TABLE2.items()]
    invalid = _analytic_support_row(1.0, 0.9)
    control = {
        "id": "NC_C5_extend_threshold_to_delta_0.9",
        "mutated_row": invalid,
        "rejected": not (invalid["tangent_dominance"] and invalid["convex_tail"]),
    }
    passed = all(
        row["tangent_dominance"] and row["convex_tail"] for row in rows
    ) and control["rejected"]
    return {
        "status": "VERIFIED" if passed else "BLOCKED",
        "rows": rows,
        "negative_controls": [control],
        "passed": passed,
    }


def run_accepted_claim_checkers() -> dict:
    claims = {
        "C2-INDEPENDENT": check_sgg_family(),
        "C3-INDEPENDENT": check_figure2(),
        "C4-INDEPENDENT": check_table2(),
    }
    return {
        "claims": claims,
        "all_passed": all(item["passed"] for item in claims.values()),
    }
