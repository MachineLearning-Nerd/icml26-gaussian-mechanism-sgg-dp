# Claim-to-evidence ledger

The current six-claim mapping follows the repository README and the evaluator-visible Space pages. Historical spot checks remain preserved inside the artifacts; the current verdicts below come from the cumulative release package.

| Claim | Paper surface | How the claim is produced | Current result | Boundary |
| --- | --- | --- | --- | --- |
| C1 | Theorem 3.1, asymptotic Gaussian optimality | Reconstruct the structured symbolic derivation, validate its algebraic DAG and negative controls, then calibrate the finite-`T` step over 256 configurations. | 12-step derivation passes; worst finite calibration gap `2.697e-4`. | Medium confidence; no proof-kernel certificate. |
| C2 | Lemma 3.3, Haar symmetrization | Check exact isometry/convexity algebra, then enumerate 56 exact finite C4-group analogues and mutate Haar/orthogonality assumptions. | Universal certificate and 56/56 finite cases pass; three negative controls reject. | Finite group is an independent checker, not a substitute for the universal proof. |
| C3 | Definitions 4.1–4.2, SGG family and special cases | Evaluate five adaptive normalization integrals, Gaussian and `l2` identities, and the factor-`p` negative control. | Maximum normalization error `3.55e-15`; special-case identities pass. | Numerical regression of the published definitions. |
| C4 | Figure 2, low-dimensional SGG improvement | Use deterministic common-random-number and independent scrambled-Sobol QMC calibrations for the published existence configurations. | Independent reductions `14.87%`, `11.98%`, and `10.02%`. | Raw paper coordinates and optimizer settings are not published; this is not coordinate-for-coordinate recovery. |
| C5 | Table 2, supporting-line threshold bounds | Recompute analytic tangent slopes, convex-tail conditions, and tangent dominance for all seven printed thresholds, retaining six-decimal rounding slack. | 7/7 rows pass; the `epsilon=1, delta=0.9` negative control fails as expected. | Threshold regression under the displayed values. |
| C6 | Lemma D.1 and Algorithm 7, tight SGG composition | Implement the paper-faithful FFT accountant, compare with direct computation, test the exact Figure 3 regime, and run a 72-case broad sweep. | Figure 3 reduction rises `31.4%` to `94.3%`; direct/FFT agreement reaches `7.37e-18`. | Unpublished Figure 3 coordinates/settings prevent exact coordinate matching. |

## Evidence chain

Each claim follows:

`paper anchor → claim contract → executable derivation/checker → raw JSON/CSV → negative control → cumulative verifier → evaluator-facing page/report`

Primary routes:

- [`repro/src/proof_gaussian_optimality.py`](repro/src/proof_gaussian_optimality.py) and [`check_asymptotic_finite_t.py`](repro/src/check_asymptotic_finite_t.py) — C1.
- [`repro/src/proof_haar.py`](repro/src/proof_haar.py) and [`check_haar_independent.py`](repro/src/check_haar_independent.py) — C2.
- [`repro/src/check_accepted_claims.py`](repro/src/check_accepted_claims.py) — C3–C5.
- [`repro/src/algorithm7.py`](repro/src/algorithm7.py) and [`check_composition.py`](repro/src/check_composition.py) — C6.
- [`repro/src/verify.py`](repro/src/verify.py) — cumulative gate.

Branch roles are documented in [`branch-audit.md`](branch-audit.md); release branches expose evidence for evaluation but do not add independent scientific claims.
