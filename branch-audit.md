# Branch audit

Repository: [MachineLearning-Nerd/icml26-gaussian-mechanism-sgg-dp](https://github.com/MachineLearning-Nerd/icml26-gaussian-mechanism-sgg-dp)

The repository was renamed from `icml26-repro-82Wosp2Iu1-asymptotic-optimality-of-the-high-dimensional-gaussian-mechanism-and-improve`. The old branch names were challenge/workflow labels; the live names below describe the evidence role.

## Old-to-new mapping

| Former branch | Clean branch | Role in the evidence lineage |
|---|---|---|
| `orx/locked-9-12-reproduction-baseline` | `historical/judged-baseline` | Frozen judged-scope baseline and starting score record |
| `orx/calibrated-table-2-rounding-tolerance` | `audit/table2-rounding-tolerance` | Calibrates the published six-decimal Table 2 thresholds |
| `orx/haar-lemma-symbolic-proof-certificate` | `audit/lemma33-haar-proof` | Universal Lemma 3.3 algebra and finite-group controls |
| `orx/theorem-3-1-proof-and-finite-t-calibration` | `audit/theorem31-finite-calibration` | Theorem 3.1 derivation and 256-case finite-(T) calibration |
| `orx/algorithm-7-exact-composition-accountant` | `audit/algorithm7-composition` | Algorithm 7, FFT accountant, and Figure 3 regime |
| `orx/independent-regressions-for-claims-3-to-5` | `audit/claims3-5-independent` | Independent Claims 3–5 numerical regressions |
| `orx/evaluator-visible-claim-1-milestone` | `release/claim1-visibility` | Evaluator-visible Claim 1 contract and artifacts |
| `orx/evaluator-visible-claim-2-milestone` | `release/claim2-visibility` | Evaluator-visible Claim 2 contract and artifacts |
| `orx/evaluator-visible-claim-6-milestone` | `release/claim6-visibility` | Evaluator-visible Claim 6 contract and artifacts |
| `orx/evaluator-visible-claims-3-to-5-milestone` | `release/claims3-5-visibility` | Evaluator-visible Claims 3–5 contracts and artifacts |
| `orx/release-candidate-and-evaluator-red-team` | `release/evaluator-red-team` | Cumulative release candidate and adversarial visibility review |
| `orx/standalone-space-root-execution` | `release/standalone-space-root` | Confirms the audit works from a downloaded Space root |
| `orx/final-publication-metadata` | `release/publication-metadata` | Final publication metadata and release surface |

`main` is the canonical publication surface. The former remote `orx/*` branches are deleted after the clean branches are pushed; their reachable commit content is retained in the corresponding histories.

## Claim lineage

| Claim | Primary branch evidence | Canonical files |
|---|---|---|
| 1 — Theorem 3.1 | `audit/theorem31-finite-calibration` | `repro/src/proof_gaussian_optimality.py`, `repro/src/check_asymptotic_finite_t.py`, `space/pages/current/claim1/` |
| 2 — Lemma 3.3 | `audit/lemma33-haar-proof` | `repro/src/proof_haar.py`, `repro/src/check_haar_independent.py`, `space/pages/current/claim2/` |
| 3 — SGG family | `audit/claims3-5-independent` | `repro/src/check_accepted_claims.py`, `space/pages/current/claim3/` |
| 4 — Figure 2 | `audit/claims3-5-independent` | `space/artifacts/claim4/`, `space/pages/current/claim4/` |
| 5 — Table 2 | `audit/table2-rounding-tolerance` and `audit/claims3-5-independent` | `space/artifacts/claim5/`, `space/pages/current/claim5/` |
| 6 — Algorithm 7 | `audit/algorithm7-composition` | `repro/src/algorithm7.py`, `repro/src/check_composition.py`, `space/pages/current/claim6/` |

## Attribution and verification policy

- Clean maintenance commits use `MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>`.
- The branch rename changes labels and links, not the scientific evidence or its recorded limitations.
- `historical/judged-baseline` remains explicitly historical; its score must not be presented as a new evaluation.
- Release branches are candidate publication surfaces until the external evaluator runs them.
