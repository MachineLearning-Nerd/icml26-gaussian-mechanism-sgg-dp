"""Full-scope calibration and independent checks for Claim 6."""

from __future__ import annotations

import math
import os
from concurrent.futures import ProcessPoolExecutor

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import betainc, gammaln

from algorithm7 import (
    algorithm7_delta,
    angular_cdf,
    compose_exact_support_fft,
    discretize_single_prv,
)


FIGURE_K = (2, 4, 8, 16, 32)
EPSILON_TOTAL = 1.0
DELTA_TARGET = 1e-5


def _l2_conditional_cdf(t: float, q: float, z: float, dimension: int) -> float:
    if t + z <= 0.0:
        return 0.0
    if t <= 0.0 or q <= 0.0:
        return float(z >= q)
    threshold = ((t + z) ** 2 - t**2 - q**2) / (2.0 * t * q)
    return float(angular_cdf(threshold, dimension))


def adaptive_l2_cdf(z: float, q: float, dimension: int) -> tuple[float, float]:
    """Independent adaptive integral for Lemma D.1 in the l2 special case."""
    log_norm = gammaln(dimension)

    def integrand(t: float) -> float:
        if t == 0.0:
            return 0.0
        log_density = (dimension - 1.0) * math.log(t) - t - log_norm
        return math.exp(log_density) * _l2_conditional_cdf(t, q, z, dimension)

    value, error = quad(integrand, 0.0, np.inf, epsabs=2e-11, epsrel=2e-10, limit=300)
    return float(value), float(error)


def _solve_q(compositions: int, sequential: bool, step: float) -> tuple[float, dict]:
    epsilon = EPSILON_TOTAL / compositions if sequential else EPSILON_TOTAL
    target = DELTA_TARGET / compositions if sequential else DELTA_TARGET
    effective_k = 1 if sequential else compositions
    upper = min(2.0, 7.5 / effective_k)

    def residual(q: float) -> float:
        result = algorithm7_delta(
            alpha=9.0,
            beta=q,
            p=1.0,
            dimension=10,
            compositions=effective_k,
            epsilon=epsilon,
            truncation=8.0,
            step=step,
            radial_nodes=96,
            angular_nodes=4097,
            exact_bounded_support=True,
        )
        return result["delta"] - target

    if residual(upper) <= 0.0:
        raise RuntimeError("failed to bracket Figure 3 calibration")
    q = float(brentq(residual, 1e-5, upper, xtol=2e-7, rtol=2e-7))
    evidence = algorithm7_delta(
        alpha=9.0,
        beta=q,
        p=1.0,
        dimension=10,
        compositions=effective_k,
        epsilon=epsilon,
        truncation=8.0,
        step=step,
        radial_nodes=96,
        angular_nodes=4097,
        exact_bounded_support=True,
    )
    return q, evidence


def reproduce_figure3() -> list[dict]:
    rows = []
    for compositions in FIGURE_K:
        sequential_q, sequential = _solve_q(compositions, True, 0.001)
        fft_q, fft = _solve_q(compositions, False, 0.001)
        sequential_mse = 10.0 * 11.0 / sequential_q**2
        fft_mse = 10.0 * 11.0 / fft_q**2
        rows.append(
            {
                "dimension": 10,
                "alpha": 9.0,
                "p": 1.0,
                "compositions": compositions,
                "epsilon_total": EPSILON_TOTAL,
                "delta_target": DELTA_TARGET,
                "sequential_beta": sequential_q,
                "fft_beta": fft_q,
                "sequential_mse": sequential_mse,
                "fft_mse": fft_mse,
                "mse_reduction": (sequential_mse - fft_mse) / sequential_mse,
                "sequential_achieved_delta": sequential["delta"] * compositions,
                "fft_achieved_delta": fft["delta"],
                "fft_retained_mass": fft["retained_mass"],
            }
        )
    return rows


def _broad_case(case: tuple) -> dict:
    dimension, alpha, p, scaled_sensitivity, compositions = case
    beta = scaled_sensitivity**p
    coarse = algorithm7_delta(
        alpha=alpha,
        beta=beta,
        p=p,
        dimension=dimension,
        compositions=compositions,
        epsilon=1.0,
        truncation=32.0,
        step=0.04,
        radial_nodes=64,
        angular_nodes=2049,
    )
    fine = algorithm7_delta(
        alpha=alpha,
        beta=beta,
        p=p,
        dimension=dimension,
        compositions=compositions,
        epsilon=1.0,
        truncation=32.0,
        step=0.02,
        radial_nodes=96,
        angular_nodes=4097,
    )
    return {
        "dimension": dimension,
        "alpha": alpha,
        "p": p,
        "beta": beta,
        "scaled_sensitivity": scaled_sensitivity,
        "compositions": compositions,
        "coarse_delta": coarse["delta"],
        "fine_delta": fine["delta"],
        "absolute_grid_difference": abs(coarse["delta"] - fine["delta"]),
        "fine_retained_mass": fine["retained_mass"],
        "fine_cropped_mass": fine["cumulative_cropped_mass"],
        "single_tail_bound": fine["single_left_tail"] + fine["single_right_tail"],
    }


def broad_sgg_sweep() -> tuple[list[dict], int]:
    mechanisms = (
        (2, 1.0, 1.0),
        (10, 9.0, 1.0),
        (2, 1.0, 2.0),
        (10, 9.0, 2.0),
        (3, 2.0, 4.0),
        (5, 3.5, 6.0),
    )
    cases = [
        (dimension, alpha, p, beta, compositions)
        for dimension, alpha, p in mechanisms
        for scaled_sensitivity in (0.10, 0.25, 0.50)
        for compositions in (2, 4, 8, 16)
    ]
    workers = min(8, os.cpu_count() or 1)
    with ProcessPoolExecutor(max_workers=workers) as pool:
        rows = list(pool.map(_broad_case, cases))
    return rows, workers


def independent_checks() -> dict:
    cdf_rows = []
    for dimension, q in ((2, 0.25), (3, 0.5), (10, 0.25), (10, 0.75), (20, 0.5)):
        z_values = np.linspace(-0.9 * q, 0.9 * q, 9)
        discretized_cdf = []
        from algorithm7 import sgg_prv_cdf

        values, _ = sgg_prv_cdf(
            z_values,
            alpha=dimension - 1.0,
            beta=q,
            p=1.0,
            dimension=dimension,
            radial_nodes=160,
            angular_nodes=8193,
        )
        for z, quadrature_value in zip(z_values, values, strict=True):
            adaptive, adaptive_error = adaptive_l2_cdf(float(z), q, dimension)
            discretized_cdf.append(
                {
                    "dimension": dimension,
                    "beta": q,
                    "z": float(z),
                    "gauss_laguerre_cdf": float(quadrature_value),
                    "adaptive_quad_cdf": adaptive,
                    "adaptive_error_estimate": adaptive_error,
                    "absolute_difference": abs(float(quadrature_value) - adaptive),
                }
            )
        cdf_rows.extend(discretized_cdf)

    discrete = discretize_single_prv(
        alpha=2.0,
        beta=0.4,
        p=1.0,
        dimension=3,
        truncation=3.0,
        step=0.01,
        radial_nodes=96,
        angular_nodes=4097,
    )
    positive = np.flatnonzero(discrete.pmf > 0.0)
    base = discrete.pmf[positive[0] : positive[-1] + 1]
    direct = base.copy()
    for _ in range(3):
        direct = np.convolve(direct, base)
    step = float(discrete.centers[1] - discrete.centers[0])
    direct_centers = 4.0 * float(discrete.centers[positive[0]]) + step * np.arange(len(direct))
    direct_payoff = np.maximum(
        1.0 - np.exp(np.minimum(1.0 - direct_centers, 0.0)),
        0.0,
    )
    direct_delta = float(np.dot(direct, direct_payoff))
    fft = compose_exact_support_fft(discrete, 4, 1.0)
    return {
        "cdf_rows": cdf_rows,
        "maximum_cdf_difference": max(row["absolute_difference"] for row in cdf_rows),
        "direct_convolution_delta": direct_delta,
        "fft_convolution_delta": fft["delta"],
        "direct_fft_difference": abs(direct_delta - fft["delta"]),
    }


def negative_controls() -> list[dict]:
    # NC1: circular convolution without zero padding aliases upper-tail mass.
    pmf = np.array([0.55, 0.0, 0.0, 0.45])
    direct = pmf.copy()
    for _ in range(3):
        direct = np.convolve(direct, pmf)
    circular = np.fft.ifft(np.fft.fft(pmf) ** 4).real
    alias_residual = float(np.sum(np.abs(direct[:4] - circular)))

    # NC2: omit Gamma normalization from generalized Laguerre weights.
    normalization_residual = abs(float(math.gamma(10.0)) - 1.0)

    # NC3: reverse the privacy-loss axis for a real l2 PRV.
    discrete = discretize_single_prv(
        alpha=9.0,
        beta=0.6,
        p=1.0,
        dimension=10,
        truncation=2.0,
        step=0.005,
        radial_nodes=96,
        angular_nodes=4097,
    )
    correct = compose_exact_support_fft(discrete, 4, 1.0)["delta"]
    reversed_prv = type(discrete)(
        centers=discrete.centers,
        pmf=discrete.pmf[::-1],
        left_tail=discrete.right_tail,
        right_tail=discrete.left_tail,
        monotonicity_residual=discrete.monotonicity_residual,
    )
    reversed_delta = compose_exact_support_fft(reversed_prv, 4, 1.0)["delta"]
    sign_residual = abs(correct - reversed_delta)
    return [
        {
            "id": "NC1_circular_fft_without_padding",
            "residual": alias_residual,
            "rejected": alias_residual > 0.1,
        },
        {
            "id": "NC2_unnormalized_radial_quadrature",
            "residual": normalization_residual,
            "rejected": normalization_residual > 1.0,
        },
        {
            "id": "NC3_reverse_privacy_loss_sign",
            "correct_delta": correct,
            "mutated_delta": reversed_delta,
            "residual": sign_residual,
            "rejected": sign_residual > 1e-4,
        },
    ]


def run_composition_checker() -> dict:
    figure = reproduce_figure3()
    broad, workers = broad_sgg_sweep()
    independent = independent_checks()
    controls = negative_controls()
    reductions = [row["mse_reduction"] for row in figure]
    max_grid_difference = max(row["absolute_grid_difference"] for row in broad)
    max_tail = max(row["single_tail_bound"] for row in broad)
    max_cropped = max(row["fine_cropped_mass"] for row in broad)
    passed = (
        all(row["fft_mse"] < row["sequential_mse"] for row in figure)
        and reductions[-1] > reductions[0]
        and max_grid_difference < 0.015
        and max_tail < 2e-6
        and max_cropped < 2e-5
        and independent["maximum_cdf_difference"] < 1e-3
        and independent["direct_fft_difference"] < 1e-10
        and all(control["rejected"] for control in controls)
    )
    return {
        "status": "VERIFIED" if passed else "BLOCKED",
        "exact_scope": {
            "algorithm": "Algorithm 7 lines 1-9",
            "figure_3": "T=10, alpha=9, p=1, epsilon_total=1, delta_target=1e-5, k={2,4,8,16,32}",
            "broad_sweep_configurations": len(broad),
        },
        "figure3": figure,
        "broad_sgg_sweep": broad,
        "summary": {
            "figure3_min_mse_reduction": min(reductions),
            "figure3_max_mse_reduction": max(reductions),
            "maximum_coarse_fine_delta_difference": max_grid_difference,
            "maximum_single_tail_mass": max_tail,
            "maximum_cropped_mass": max_cropped,
            "independent_maximum_cdf_difference": independent["maximum_cdf_difference"],
            "independent_direct_fft_difference": independent["direct_fft_difference"],
            "worker_processes": workers,
            "visible_cpu_allocation": os.cpu_count(),
        },
        "independent_checker": independent,
        "negative_controls": controls,
        "all_negative_controls_rejected": all(control["rejected"] for control in controls),
        "passed": passed,
        "limitation": (
            "The paper does not publish Figure 3's numeric coordinates or its "
            "L,h,K,Nw,precision settings. We reproduce the exact stated regime "
            "and report convergence, but cannot compare unpublished coordinates."
        ),
    }
