# Current release report and score forecast

- Previous live judged score: `9/12`
- Conservative projected score range after this proposed change: `10–12/12`
- Best-supported possible new score: `12/12` — forecast only, not a judge result

Baseline HF Head and Judge Head:
`2d5f672ab576722614a3c86d48550e74fee2aca4`.

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

## Winning branch, run, compute, and cost

The winning branch is `orx/release-candidate-and-evaluator-red-team`.
Candidate commit `07d4bb32c1ee667e01a3180b170a952299a42000` was tested by
formal run `ad8cc069-72cf-403f-94fb-f5a1bcaa006e` with the unchanged command:

```bash
uv run --frozen python repro/src/verify.py
```

All 15 checks passed. Before launch, the estimate was 8 cores and 1,200 s, so
Hugging Face `cpu-upgrade` was selected. The contracted flavor allocation is
8 vCPUs; the container exposed 64 logical CPUs, the verifier used eight worker
processes with one native thread each, verifier runtime was 21.667505 s, and
`orx` reported 53 s end-to-end. The current official price is $0.0005/min
($0.03/hour); rounding this job up to one billed minute gives $0.0005.

The immediately preceding run
`e74ebc76-03e0-47fe-bb74-751a11299003` exited before verification because the
default image had no `uv`. It is retained as an environment failure. The
successful run used the pinned
`ghcr.io/astral-sh/uv:python3.12-bookworm-slim` image and did not change code,
configuration, or the fixed command.

## Experiment tree and evidence paths

The stacked lineage is: locked 9/12 baseline → Table 2 tolerance calibration →
Haar proof → Claim 2 visibility → Theorem 3.1 proof/calibration → Claim 1
visibility → Algorithm 7 → Claim 6 visibility → independent Claims 3–5 →
Claims 3–5 visibility → this release/red-team child. Failed Algorithm 7
calibrations remain on their provisional node and explain the final
independently selected truncation gate.

The six canonical evidence paths are
[Claim 1](#/current-claim1), [Claim 2](#/current-claim2),
[Claim 3](#/current-claim3), [Claim 4](#/current-claim4),
[Claim 5](#/current-claim5), and [Claim 6](#/current-claim6).
The [visibility matrix](#/current-visibility), [red-team record](#/current-red-team),
[exact upload allowlist](../../../UPLOAD_ALLOWLIST.txt),
[SHA-256 manifest](../../../SHA256SUMS.txt), and
[material command ledger](command-log.md) are evaluator-reachable.

The protected-subset audit checked 14/14 judged files. Every old hash occurs at
the same path or under `historical/judged-root/`; missing count is zero. The
current text-only upload contains 85 allowlisted files and 84 hashes (the hash
manifest cannot hash itself).

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
