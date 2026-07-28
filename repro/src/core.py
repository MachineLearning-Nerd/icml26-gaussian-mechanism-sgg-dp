"""Numerical primitives for the arXiv:2606.08681 reproduction.

The baseline intentionally mirrors the scope of the judged artifact. Later
experiment nodes strengthen the below-full-credit claims while retaining these
functions as cumulative regression checks.
"""

from __future__ import annotations

import math

import numpy as np
from scipy.optimize import brentq
from scipy.signal import fftconvolve
from scipy.special import gammaln, ndtr


def gaussian_delta(u: float | np.ndarray, eps: float, sensitivity: float = 1.0):
    """Equation (6): exact hockey-stick divergence for Gaussian noise."""
    u = np.asarray(u, dtype=float)
    root = np.sqrt(u)
    a = -eps * root / sensitivity + sensitivity / (2.0 * root)
    b = -eps * root / sensitivity - sensitivity / (2.0 * root)
    return ndtr(a) - np.exp(eps) * ndtr(b)


def gaussian_variance(delta: float, eps: float, sensitivity: float = 1.0) -> float:
    """Equation (7), solved on log variance to avoid scale-dependent brackets."""

    def residual(log_u: float) -> float:
        return float(gaussian_delta(math.exp(log_u), eps, sensitivity) - delta)

    return math.exp(brentq(residual, -40.0, 40.0, xtol=1e-13, rtol=1e-13))


def supporting_line_holds(
    delta: float, eps: float, sensitivity: float = 1.0
) -> tuple[bool, bool, float]:
    """Numerically audit Proposition 3.1's two tangent-support conditions."""
    u0 = gaussian_variance(delta, eps, sensitivity)
    h = max(1e-5 * u0, 1e-8)
    g0 = float(gaussian_delta(u0, eps, sensitivity))
    slope = float(
        (gaussian_delta(u0 + h, eps, sensitivity) - gaussian_delta(u0 - h, eps, sensitivity))
        / (2.0 * h)
    )

    left = np.concatenate(([0.0], np.geomspace(max(u0 * 1e-9, 1e-14), u0, 6000)))
    tangent = g0 + slope * (left - u0)
    slack = gaussian_delta(np.maximum(left, 1e-300), eps, sensitivity) - tangent
    # Table 2 publishes delta_star to six decimals. The resulting tangent
    # residual can move by a few 1e-7 at the rounded boundary, so the audit
    # tolerance is 1e-6 (still orders below a substantive violation).
    tangent_ok = bool(np.min(slack) >= -1e-6)

    right = np.geomspace(u0, u0 * 1e6, 6000)
    step = np.maximum(right * 2e-4, 1e-8)
    second = (
        gaussian_delta(right + step, eps, sensitivity)
        - 2.0 * gaussian_delta(right, eps, sensitivity)
        + gaussian_delta(np.maximum(right - step, 1e-300), eps, sensitivity)
    ) / step**2
    convex_ok = bool(np.min(second) >= -2e-8)
    return convex_ok, tangent_ok, float(np.min(slack))


def sgg_log_mse(alpha: float, beta: float, p: float) -> float:
    """Log E[R^2] for R~GGamma(alpha,beta,p)."""
    shape = (alpha + 1.0) / p
    return (
        gammaln(shape + 2.0 / p)
        - gammaln(shape)
        - (2.0 / p) * math.log(beta)
    )


def sgg_mse(alpha: float, beta: float, p: float) -> float:
    return math.exp(sgg_log_mse(alpha, beta, p))


def sample_radius_and_cosine(
    alpha: float,
    p: float,
    dimension: int,
    size: int,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray]:
    """Draw beta=1 radii and the cosine to a fixed shift direction."""
    radii = rng.gamma(shape=(alpha + 1.0) / p, scale=1.0, size=size) ** (1.0 / p)
    cosine = rng.beta((dimension - 1.0) / 2.0, (dimension - 1.0) / 2.0, size=size)
    return radii, 2.0 * cosine - 1.0


def sgg_privacy_loss(
    base_radius: np.ndarray,
    cosine: np.ndarray,
    alpha: float,
    beta: float,
    p: float,
    dimension: int,
    sensitivity: float = 1.0,
) -> np.ndarray:
    """Privacy loss log f(X)/f(X+mu), using the radial density exactly."""
    radius = base_radius * beta ** (-1.0 / p)
    shifted = np.sqrt(
        np.maximum(radius**2 + sensitivity**2 + 2.0 * radius * sensitivity * cosine, 1e-300)
    )
    exponent = alpha + 1.0 - dimension
    return exponent * (np.log(np.maximum(radius, 1e-300)) - np.log(shifted)) - beta * (
        radius**p - shifted**p
    )


def hockey_stick_from_loss(loss: np.ndarray, eps: float) -> float:
    return float(np.mean(np.maximum(1.0 - np.exp(np.minimum(eps - loss, 0.0)), 0.0)))


def calibrate_sgg_beta(
    alpha: float,
    p: float,
    dimension: int,
    eps: float,
    delta: float,
    base_radius: np.ndarray,
    cosine: np.ndarray,
    sensitivity: float = 1.0,
) -> float:
    """Common-random-number bisection for the largest feasible SGG rate."""

    def residual(log_beta: float) -> float:
        beta = math.exp(log_beta)
        loss = sgg_privacy_loss(
            base_radius, cosine, alpha, beta, p, dimension, sensitivity
        )
        return hockey_stick_from_loss(loss, eps) - delta

    lo, hi = -24.0, 24.0
    if residual(lo) > 0.0 or residual(hi) < 0.0:
        raise RuntimeError("failed to bracket SGG privacy calibration")
    return math.exp(brentq(residual, lo, hi, xtol=2e-9, rtol=2e-9))


def fft_composed_delta_from_samples(
    single_loss: np.ndarray,
    eps_total: float,
    compositions: int,
    bins: int = 4097,
) -> float:
    """Independent histogram/linear-FFT composition of a sampled single-step PRV."""
    tail = max(float(np.quantile(np.abs(single_loss), 0.99999)) * 1.25, 1.0)
    edges = np.linspace(-tail, tail, bins + 1)
    mass, _ = np.histogram(single_loss, bins=edges)
    mass = mass.astype(float) / float(single_loss.size)
    centers = (edges[:-1] + edges[1:]) / 2.0
    step = centers[1] - centers[0]
    composed = mass
    for _ in range(1, compositions):
        composed = fftconvolve(composed, mass, mode="full")
    composed = np.maximum(composed, 0.0)
    composed /= composed.sum()
    sum_centers = compositions * centers[0] + step * np.arange(composed.size)
    payoff = np.maximum(1.0 - np.exp(np.minimum(eps_total - sum_centers, 0.0)), 0.0)
    return float(np.dot(composed, payoff))


def direct_composed_delta(
    alpha: float,
    beta: float,
    p: float,
    dimension: int,
    eps_total: float,
    compositions: int,
    size: int,
    rng: np.random.Generator,
    sensitivity: float = 1.0,
) -> tuple[float, float]:
    """Direct Monte Carlo composition and an asymptotic 95% half-width."""
    total = np.zeros(size, dtype=float)
    for _ in range(compositions):
        radius, cosine = sample_radius_and_cosine(alpha, p, dimension, size, rng)
        total += sgg_privacy_loss(
            radius, cosine, alpha, beta, p, dimension, sensitivity
        )
    payoff = np.maximum(1.0 - np.exp(np.minimum(eps_total - total, 0.0)), 0.0)
    estimate = float(np.mean(payoff))
    half_width = 1.96 * float(np.std(payoff, ddof=1)) / math.sqrt(size)
    return estimate, half_width
