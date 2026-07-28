# Current release report and score forecast

- Previous live judged score: `9/12`
- Conservative projected score range after this proposed change: `10–12/12`
- Best-supported possible new score: `12/12` — forecast only, not a judge result

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
|---|---:|---:|---|---|---|
| 1 — Theorem 3.1 | 1 | 2 | MEDIUM | VERIFIED | Universal structured derivation plus a 256-case exact-CDF asymptotic calibration; remaining risk is that the certificate imports named probability theorems rather than using a formal proof kernel. |
| 2 — Lemma 3.3 | 1 | 2 | HIGH | VERIFIED | Universal orthogonality/Haar/convexity derivation, 56-case exact finite-group checker, and three rejected mutations. |
| 3 — SGG family | 2 | 2 | HIGH | VERIFIED | Analytic identities plus five independent adaptive integrals and a missing-normalizer control. |
| 4 — Figure 2 | 2 | 2 | HIGH | VERIFIED | Immutable judged values plus eight scrambled-Sobol replicates per point; author optimizer settings remain unpublished. |
| 5 — Table 2 | 2 | 2 | HIGH | VERIFIED | All seven printed thresholds pass an analytic-derivative checker; six-decimal publication slacks are explicit. |
| 6 — Algorithm 7 | 1 | 2 | HIGH | VERIFIED | Complete Figure 3 regime, 72-case SGG sweep, coarse/fine and direct-convolution checks, and three rejected mutations; paper coordinates/settings are unpublished. |

The current live total remains **9/12**. Claims 1, 2, and 6 changed since that
verdict; Claims 3–5 were independently rerun and remain current. No claim is
BLOCKED. The conservative projected range is **10–12/12** and the
best-supported possible total is **12/12**, both forecasts. Only the live
judge can change the score.

The exact publication action after every gate passes is: upload the text
allowlist to the existing `DineshAI/82Wosp2Iu1` Space using the Hugging Face
API, verify the returned revision by a fresh download, then fast-forward
GitHub `main` to the validated release-candidate branch and verify its remote
SHA. No second Space will be created.

## Pre-upload informational summary

| Claim | Status | Expected points | Confidence | Expected evaluator status |
|---|---|---:|---|---|
| 1 | VERIFIED | 1–2 | MEDIUM | Full review requested; proof-level reconstruction replaces the toy spot check |
| 2 | VERIFIED | 2 | HIGH | Full-credit evidence |
| 3 | VERIFIED | 2 | HIGH | Previously full credit; cumulative regression passes |
| 4 | VERIFIED | 2 | HIGH | Previously full credit; cumulative regression passes |
| 5 | VERIFIED | 2 | HIGH | Previously full credit; cumulative regression passes |
| 6 | VERIFIED | 2 | HIGH | Full paper regime and broad accountant validation replace the toy sweep |

Conservative projected total: **10–12/12**. Best-supported possible score:
**12/12**, still only a forecast. The remaining risk is chiefly evaluator
acceptance of Claim 1's structured proof certificate.
