# Current verification — Claim 6: tight SGG composition

**Verdict: VERIFIED.** This page supersedes the four-configuration Monte Carlo
spot check on the page labeled **Historical rejected baseline**. It implements
the paper's Algorithm 7, reproduces the complete stated Figure 3 regime,
checks 72 additional SGG configurations, and uses independent deterministic
checks and failure-inducing controls.

## Exact claim contract

Lemma D.1 and Algorithm 7 state that the privacy random variable (PRV) of an
SGG mechanism can be discretized from its one-dimensional radial CDF and that
the exact composed hockey-stick curve can be computed by FFT convolution. The
paper states that this gives a practical tight accountant for the
`l2` mechanism, resolving the Joseph et al. open question.

Figure 3 fixes:

- `T=10`, `alpha=9`, `p=1` (the `l2` mechanism);
- total `(epsilon,delta)=(1,10^-5)`;
- `k in {2,4,8,16,32}` identical invocations;
- minimal per-invocation MSE under sequential allocation
  `(epsilon/k,delta/k)` versus Algorithm 7.

The stated outcome is a clear, growing MSE gap in favor of tight composition.

Source: arXiv:2606.08681v1, Section 4.4, Lemma D.1, Algorithm 7 (`alg7`),
Figure 3, and Appendix D. The HTML was retrieved on 2026-07-28 with an
explicit User-Agent; SHA-256:
`a02952f28208ebacabb7e555436985040f909dd881786f74d71cd4aee7841a38`.

## Algorithm implemented

The executable verifier follows Algorithm 7 line by line:

1. transform `t=beta*r^p`, giving a Gamma radial variable;
2. evaluate Lemma D.1 with generalized Gauss–Laguerre quadrature;
3. invert the monotone angular privacy-loss map on a dense lookup table;
4. obtain the single-step PRV mass by CDF differences;
5. perform linear FFT convolution, cropping after multiplication;
6. evaluate `(1-exp(epsilon-Z))_+` against the composed PRV.

For the bounded `l2` PRV, zero-padded FFT powering is algebraically identical
to repeated multiplication because the declared interval contains the full
composed support. The verifier checks that condition before using it.

## Figure 3 reproduction

| k | Sequential MSE | Algorithm 7 MSE | MSE reduction | FFT achieved delta |
|---:|---:|---:|---:|---:|
| 2 | 330.920 | 227.064 | 31.38% | `9.999997e-6` |
| 4 | 1,314.601 | 530.484 | 59.65% | `1.000000e-5` |
| 8 | 5,239.232 | 1,142.338 | 78.20% | `1.000000e-5` |
| 16 | 20,945.179 | 2,367.004 | 88.70% | `1.000001e-5` |
| 32 | 83,797.922 | 4,816.598 | 94.25% | `9.999994e-6` |

The gap is positive at all five paper configurations and grows monotonically
with `k`, directly reproducing the paper's stated Figure 3 conclusion.

## Robustness and independent checks

The broad suite crosses six SGG shapes—including `l2`, Gaussian, and two
low-dimensional generalized-Gamma choices—with three common dimensionless
sensitivities and `k in {2,4,8,16}`.

| Diagnostic | Result |
|---|---:|
| Additional SGG configurations | 72 |
| Maximum coarse/fine delta difference | `2.805e-3` |
| Maximum single-step truncated mass | `4.44e-16` |
| Maximum composed cropped mass | `7.62e-7` |
| Independent adaptive-CDF discrepancy | `3.249e-4` |
| Direct polynomial vs FFT delta difference | `7.37e-18` |
| Negative controls rejected | 3/3 |

The controls detect circular FFT aliasing without zero-padding (residual
`0.6090`), missing Gamma normalization (residual `362879`), and a reversed
privacy-loss axis (delta changes from `5.694e-4` to `1.754e-4`).

## Calibrated truncation, not a hidden success

The failed lineage is retained in the experiment record. An initial broad
sweep did not normalize scale across different `p`. After normalization, a
fixed `L=32` clipped 13.95% of the most extreme composed distribution.
Increasing to `L=64` reduced clipping to `6.64e-4`; the final independently
chosen `L=96` reduced it to `7.62e-7`, below the predeclared `2e-5` gate.
This calibrated horizon sequence is reported to avoid circularly selecting a
convenient finite example.

## Raw result and reproduction

| Field | Value |
|---|---:|
| Git SHA | `3c4970bd873cb9440d24713d14e4818fed78976f` |
| Seed | `20260728` |
| Backend / flavor | Hugging Face / `cpu-upgrade` |
| Estimated cores | 8 |
| Visible CPUs / worker processes | 64 / 8 |
| Estimated verifier runtime | 1,200 s |
| Measured verifier runtime | 14.507730 s |
| Hugging Face job duration reported by `orx` | 37 s |
| Cumulative suite | 11/11 passed |

The fixed command on every experiment node is:

```bash
uv run --frozen python repro/src/verify.py
```

Download the [complete raw JSON](../../../artifacts/claim6/raw_output.json),
[Figure 3 CSV](../../../artifacts/claim6/figure3.csv), and
[negative-control JSON](../../../artifacts/claim6/control_output.json).
The [Algorithm 7 source](../../../repro/src/algorithm7.py),
[independent checker](../../../repro/src/check_composition.py),
[cumulative entrypoint](../../../repro/src/verify.py), and
[claim contract](../../../artifacts/claim6/claim_contract.json) are directly
downloadable with the exact lockfile and failure behavior.

## Limitations

The paper does not publish Figure 3's numerical coordinates or its
`L,h,K,Nw,prec` settings, so coordinate-for-coordinate comparison is
impossible. This reproduction fixes and reports all settings, checks
coarse/fine convergence, and tests the exact stated regime. Numerical evidence
validates the implementation over the declared suite; it does not substitute
for the paper's composition theorem.
