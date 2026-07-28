# Current verification — Claim 1: asymptotic Gaussian optimality

**Verdict: VERIFIED.** This page supersedes the one-parameter supporting-line
spot check on the page labeled **Historical rejected baseline**. The universal
claim is addressed by an independently reconstructed symbolic derivation. A
separate 256-configuration finite-\(T\) study calibrates the limiting step and
is not presented as proof.

## Exact claim contract

Fix every `epsilon >= 0` and sensitivity `s > 0`. Theorem 3.1 asserts that
there exists `delta_star in (0,1)` such that, for every
`delta in (0,delta_star]`, if `u0` is the minimum Gaussian variance achieving
`(epsilon, delta)` privacy, then every sequence of arbitrary additive noises
`X_T in R^T` with

`E||X_T||_2^2 = T*u0`

satisfies

`liminf_(T→infinity) delta_(M_T,u0)(epsilon) >= delta`,

where privacy is the worst-direction hockey-stick divergence over all shifts
of norm at most `s`.

Source: arXiv:2606.08681v1, Theorem 3.1 (`S3.Thmtheorem1`), Lemmas
3.1–3.3, Proposition 3.1, Theorem B.1, and Appendix B. The HTML was retrieved
on 2026-07-28 with an explicit User-Agent; SHA-256:
`a02952f28208ebacabb7e555436985040f909dd881786f74d71cd4aee7841a38`.

## What was verified

The 12-step proof certificate checks the complete implication:

1. Haar symmetrization converts arbitrary noise to spherical noise without
   changing MSE or worsening privacy.
2. Spherical noise has the representation `R_T U_T`, with
   `E[R_T^2/T] = u0`.
3. SymPy verifies the exact finite-\(T\) threshold algebra for the paper's
   test set `S_T`.
4. The uniform-sphere coordinate converges uniformly in CDF to `N(0,1)`,
   producing the paper's `E[g(R_T^2/T)] + o(1)` lower bound.
5. The verified global supporting line and the exact mean identity yield
   `E[g(R_T^2/T)] >= g(u0) = delta`.
6. The eventual-convexity and vanishing-intercept asymptotics establish the
   non-vacuous high-privacy interval required by the theorem.

All dependencies are checked before a step can be used. Three mutations that
remove an essential assumption—equal MSE, the high-privacy regime, or the
asymptotic qualifier—are all rejected.

## Independent finite-\(T\) calibration

The independent checker evaluates the exact beta CDF of a spherical
coordinate, not Monte Carlo. It covers:

- `T = 2, 4, ..., 65,536`;
- `epsilon in {0.25, 1, 4, 16}` at `delta = 10^-3`;
- deterministic, two-point, fixed heavy-tail, and `T`-dependent rare-spike
  radial laws;
- 256 total configurations, each with the exact mean constraint.

| Diagnostic | Result |
|---|---:|
| Maximum mean-constraint residual | `8.88e-16` |
| Minimum supporting-line margin | `-5.21e-18` |
| Maximum absolute normal-limit gap at `T=2` | `4.8225e4` |
| Maximum absolute normal-limit gap at `T=65,536` | `2.6972e-4` |

The very large small-\(T\) discrepancy is retained rather than hidden: at
large `epsilon`, the finite test contains an `exp(epsilon)` multiplier and is
not a useful finite-dimensional approximation. The large-\(T\) result directly
answers the earlier criticism that no asymptotic behavior was shown.

## Raw result and reproduction

| Field | Value |
|---|---:|
| Scientific Git SHA | `bc38201f53d152cffbd52c2756f0ee8cd62c37e7` |
| Seed | `20260728` |
| Backend / flavor | local / local-single-core |
| Estimated cores | 1 |
| Visible CPUs / effective threads | 8 / 1 |
| Estimated verifier runtime | 10 s |
| Measured verifier runtime | 0.990255167 s |
| Proof DAG | 12/12 steps accepted |
| Negative controls | 3/3 rejected |
| Finite-\(T\) configurations | 256/256 passed |
| Cumulative suite | 10/10 passed |
| Certificate SHA-256 | `14933993fcfb120a32618b5734465ca6d46e8f8298c00274914688f6b496011e` |

The fixed command on every experiment node is:

```bash
uv run --frozen python repro/src/verify.py
```

Download the [complete raw JSON](../../../artifacts/claim1/raw_output.json) and
[negative-control JSON](../../../artifacts/claim1/control_output.json).
Executable source, the exact lockfile, and the claim contract are included in
this candidate.

## Limitations

The certificate is a structured SymPy/Python derivation, not a Lean/Coq kernel
proof. It imports standard probability results—Gaussian representation of a
uniform sphere coordinate, Slutsky, Pólya's theorem, and mixture/data-processing
properties of hockey-stick divergence—and names them explicitly. The paper
gives no numerical `T0` or convergence rate. The finite-\(T\) sweep is scoped
corroboration and is never used to establish the universal minimax statement.
