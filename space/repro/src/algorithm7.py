"""Paper-faithful implementation of Algorithm 7 (arXiv:2606.08681).

The single-step SGG privacy-loss CDF is evaluated by generalized
Gauss--Laguerre radial quadrature and an angular threshold lookup. The
discretized privacy random variable is then composed by FFT convolution with
cropping to the declared support after every multiplication.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.fft import irfft, next_fast_len, rfft
from scipy.signal import fftconvolve
from scipy.special import betainc, gamma, roots_genlaguerre


@dataclass(frozen=True)
class DiscretizedPRV:
    centers: np.ndarray
    pmf: np.ndarray
    left_tail: float
    right_tail: float
    monotonicity_residual: float


def angular_cdf(cosine: np.ndarray | float, dimension: int):
    """CDF of the first coordinate of a uniform point on S^(T-1)."""
    cosine = np.asarray(cosine, dtype=float)
    shape = (dimension - 1.0) / 2.0
    value = betainc(shape, shape, np.clip((cosine + 1.0) / 2.0, 0.0, 1.0))
    return np.where(cosine <= -1.0, 0.0, np.where(cosine >= 1.0, 1.0, value))


def _scaled_privacy_loss(
    scaled_radius: float,
    scaled_sensitivity: float,
    cosine: np.ndarray,
    alpha: float,
    p: float,
    dimension: int,
) -> np.ndarray:
    shifted = np.sqrt(
        np.maximum(
            scaled_radius**2
            + scaled_sensitivity**2
            + 2.0 * scaled_radius * scaled_sensitivity * cosine,
            1e-300,
        )
    )
    spatial_power = alpha + 1.0 - dimension
    return spatial_power * (
        math.log(max(scaled_radius, 1e-300)) - np.log(shifted)
    ) + shifted**p - scaled_radius**p


def sgg_prv_cdf(
    z: np.ndarray,
    *,
    alpha: float,
    beta: float,
    p: float,
    dimension: int,
    sensitivity: float = 1.0,
    radial_nodes: int = 80,
    angular_nodes: int = 4097,
) -> tuple[np.ndarray, float]:
    """Lemma D.1 / Eq. (17), using the paper's lookup interpolation."""
    if alpha > dimension - 1.0 + 1e-12:
        raise ValueError("Algorithm 7 monotone lookup requires alpha <= T-1")
    z = np.asarray(z, dtype=float)
    shape = (alpha + 1.0) / p
    nodes, weights = roots_genlaguerre(radial_nodes, shape - 1.0)
    weights = weights / gamma(shape)
    scaled_sensitivity = beta ** (1.0 / p) * sensitivity
    cosine_grid = np.linspace(-1.0, 1.0, angular_nodes)
    answer = np.zeros_like(z)
    worst_monotonicity = 0.0

    for node, weight in zip(nodes, weights, strict=True):
        scaled_radius = float(node ** (1.0 / p))
        loss_grid = _scaled_privacy_loss(
            scaled_radius,
            scaled_sensitivity,
            cosine_grid,
            alpha,
            p,
            dimension,
        )
        worst_monotonicity = min(
            worst_monotonicity, float(np.min(np.diff(loss_grid)))
        )
        if worst_monotonicity < -1e-9:
            raise RuntimeError("privacy-loss angular map is not monotone")
        threshold = np.interp(
            z,
            loss_grid,
            cosine_grid,
            left=-1.0,
            right=1.0,
        )
        answer += float(weight) * angular_cdf(threshold, dimension)

    answer = np.maximum.accumulate(np.clip(answer, 0.0, 1.0))
    return answer, worst_monotonicity


def discretize_single_prv(
    *,
    alpha: float,
    beta: float,
    p: float,
    dimension: int,
    truncation: float,
    step: float,
    sensitivity: float = 1.0,
    radial_nodes: int = 80,
    angular_nodes: int = 4097,
) -> DiscretizedPRV:
    """Algorithm 7 lines 2--6."""
    intervals = int(math.ceil(2.0 * truncation / step))
    if intervals % 2:
        intervals += 1
    step = 2.0 * truncation / intervals
    centers = np.linspace(-truncation, truncation, intervals + 1)
    edges = np.concatenate(
        ([centers[0] - step / 2.0], centers + step / 2.0)
    )
    cdf, monotonicity = sgg_prv_cdf(
        edges,
        alpha=alpha,
        beta=beta,
        p=p,
        dimension=dimension,
        sensitivity=sensitivity,
        radial_nodes=radial_nodes,
        angular_nodes=angular_nodes,
    )
    pmf = np.maximum(np.diff(cdf), 0.0)
    return DiscretizedPRV(
        centers=centers,
        pmf=pmf,
        left_tail=float(cdf[0]),
        right_tail=float(1.0 - cdf[-1]),
        monotonicity_residual=monotonicity,
    )


def _privacy_delta(centers: np.ndarray, mass: np.ndarray, epsilon: float) -> float:
    payoff = np.maximum(
        1.0 - np.exp(np.minimum(epsilon - centers, 0.0)),
        0.0,
    )
    return float(np.dot(mass, payoff))


def compose_with_cropping(
    discretized: DiscretizedPRV,
    compositions: int,
    epsilon: float,
) -> dict:
    """Algorithm 7 lines 7--9, retaining rather than hiding cropped mass."""
    centers = discretized.centers
    pmf = discretized.pmf
    current = pmf.copy()
    cropped_mass = 0.0
    midpoint = (len(centers) - 1) // 2
    for _ in range(1, compositions):
        full = fftconvolve(current, pmf, mode="full")
        full = np.maximum(full, 0.0)
        cropped = full[midpoint : midpoint + len(centers)]
        cropped_mass += max(float(full.sum() - cropped.sum()), 0.0)
        current = cropped
    return {
        "delta": _privacy_delta(centers, current, epsilon),
        "retained_mass": float(current.sum()),
        "cumulative_cropped_mass": cropped_mass,
        "single_left_tail": discretized.left_tail,
        "single_right_tail": discretized.right_tail,
        "angular_monotonicity_residual": discretized.monotonicity_residual,
        "grid_size": len(centers),
        "step": float(centers[1] - centers[0]),
    }


def compose_exact_support_fft(
    discretized: DiscretizedPRV,
    compositions: int,
    epsilon: float,
) -> dict:
    """Linear FFT power used when the composed bounded support is not cropped.

    This is algebraically identical to Algorithm 7's repeated convolutions
    when its truncation interval contains the complete composed support.
    """
    positive = np.flatnonzero(discretized.pmf > 0.0)
    if len(positive) == 0:
        raise RuntimeError("empty discretized PRV")
    lo, hi = int(positive[0]), int(positive[-1])
    base = discretized.pmf[lo : hi + 1]
    output_length = compositions * (len(base) - 1) + 1
    transform_length = next_fast_len(output_length)
    convolved = irfft(rfft(base, transform_length) ** compositions, transform_length)
    convolved = np.maximum(convolved[:output_length], 0.0)
    step = float(discretized.centers[1] - discretized.centers[0])
    first_center = compositions * float(discretized.centers[lo])
    centers = first_center + step * np.arange(output_length)
    return {
        "delta": _privacy_delta(centers, convolved, epsilon),
        "retained_mass": float(convolved.sum()),
        "cumulative_cropped_mass": 0.0,
        "single_left_tail": discretized.left_tail,
        "single_right_tail": discretized.right_tail,
        "angular_monotonicity_residual": discretized.monotonicity_residual,
        "grid_size": len(discretized.centers),
        "composed_grid_size": output_length,
        "step": step,
        "crop_equivalent_by_bounded_support": True,
    }


def algorithm7_delta(
    *,
    alpha: float,
    beta: float,
    p: float,
    dimension: int,
    compositions: int,
    epsilon: float,
    truncation: float,
    step: float,
    sensitivity: float = 1.0,
    radial_nodes: int = 80,
    angular_nodes: int = 4097,
    exact_bounded_support: bool = False,
) -> dict:
    discretized = discretize_single_prv(
        alpha=alpha,
        beta=beta,
        p=p,
        dimension=dimension,
        truncation=truncation,
        step=step,
        sensitivity=sensitivity,
        radial_nodes=radial_nodes,
        angular_nodes=angular_nodes,
    )
    if exact_bounded_support:
        if not (abs(alpha - (dimension - 1.0)) < 1e-12 and abs(p - 1.0) < 1e-12):
            raise ValueError("bounded-support optimization is specific to the l2 mechanism")
        scaled_sensitivity = beta * sensitivity
        if compositions * scaled_sensitivity > truncation - step:
            raise ValueError("declared truncation does not contain composed support")
        return compose_exact_support_fft(discretized, compositions, epsilon)
    return compose_with_cropping(discretized, compositions, epsilon)
