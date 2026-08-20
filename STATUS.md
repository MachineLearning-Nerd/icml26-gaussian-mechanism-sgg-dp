# Reproduction status

Overall status:

`ALL_C1_C6_VERIFIED_SCOPED_C1_MEDIUM_HISTORICAL_SCORE_9_OF_12_NO_CURRENT_SCORE`

All six current claim contracts pass the cumulative evidence package. The labels below describe the evidence scope, not a blanket replacement for the paper’s proofs.

| Claim | Current status | Confidence and boundary |
| --- | --- | --- |
| C1 | `VERIFIED_SCOPED_MEDIUM` | Theorem 3.1 has a structured symbolic derivation and 256 finite-`T` calibrations, but no formal proof-kernel artifact. |
| C2 | `VERIFIED_SCOPED_HIGH` | Haar symmetrization has universal algebra, 56 exact finite-group cases, and rejected non-Haar/nonorthogonal controls. |
| C3 | `VERIFIED_SCOPED_HIGH` | SGG normalization and Gaussian/`l2` special cases pass independent regressions. |
| C4 | `VERIFIED_SCOPED_HIGH` | Independent QMC reproduces low-dimensional existence reductions; raw paper coordinates/settings are unpublished. |
| C5 | `VERIFIED_SCOPED_HIGH` | All seven Table 2 thresholds pass analytic derivative and rounding-slack checks. |
| C6 | `VERIFIED_SCOPED_HIGH` | Algorithm 7 and the Figure 3 regime pass a 72-case sweep with direct/FFT agreement; exact unpublished coordinates remain unavailable. |

The historical judged score is **9/12**. The release pages’ `10–12/12` value is a forecast, not a current score. `current_score_claim=false`, `publication_allowed=false`, and `official_author_endorsement=false`.

See [`CLAIM_EVIDENCE.md`](CLAIM_EVIDENCE.md), [`SOURCE_AUDIT.md`](SOURCE_AUDIT.md), and [`REPORT.md`](REPORT.md).
