# ICML 2026 — Gaussian Mechanism and SGG Differential Privacy

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-gaussian-mechanism-sgg-dp/blob/main/notebooks/gaussian_sgg_reproduction.py)

Independent claim-by-claim reproduction audit for [arXiv:2606.08681](https://arxiv.org/abs/2606.08681), *Asymptotic Optimality of the High-Dimensional Gaussian Mechanism and Improved Low-Dimensional Mechanisms for Differential Privacy*.

The repository was renamed from `icml26-repro-82Wosp2Iu1-asymptotic-optimality-of-the-high-dimensional-gaussian-mechanism-and-improve` to `icml26-gaussian-mechanism-sgg-dp` so the public URL describes the paper rather than the challenge identifier.

## What the paper does

The paper studies additive-noise mechanisms for differential privacy in two regimes:

1. It gives an asymptotic optimality argument for Gaussian noise as the query dimension grows under strong privacy settings.
2. It introduces the Spherical Generalized Gamma (SGG) family, which contains the Gaussian and `l2` mechanisms, and identifies low-dimensional members that improve mean-squared error in selected settings.
3. It gives a tight composition procedure for the SGG family, including the paper's Algorithm 7 comparison against sequential composition.

This repository turns those contributions into executable evidence, negative controls, source-linked claim contracts, and a cumulative verifier. The report is a reproduction audit, not a claim that the paper's theorems have been formally re-proved in a proof assistant.

## Claim and evidence ledger

All six judged claims are currently marked `VERIFIED` by the cumulative evidence package. “Verified” here means that the stated contract is supported by the documented derivation and executable checks; the confidence and limitations below remain part of the result.

| Claim | Paper anchor | Evidence path | Current assessment |
|---|---|---|---|
| 1 | Theorem 3.1 — asymptotic Gaussian optimality | [`proof_gaussian_optimality.py`](repro/src/proof_gaussian_optimality.py), [`check_asymptotic_finite_t.py`](repro/src/check_asymptotic_finite_t.py), [claim page](space/pages/current/claim1/page.md) | `VERIFIED`, medium confidence: universal structured derivation plus 256 finite-(T) calibrations; imported probability limit facts and the absence of a formal proof kernel remain limitations |
| 2 | Lemma 3.3 — Haar symmetrization | [`proof_haar.py`](repro/src/proof_haar.py), [`check_haar_independent.py`](repro/src/check_haar_independent.py), [claim page](space/pages/current/claim2/page.md) | `VERIFIED`, high confidence: universal algebra, 56 exact finite-group cases, and rejected non-Haar/nonorthogonal controls |
| 3 | Definitions 4.1–4.2 — SGG family and special cases | [`check_accepted_claims.py`](repro/src/check_accepted_claims.py), [claim page](space/pages/current/claim3/page.md) | `VERIFIED`, high confidence: normalization error at most (3.55\times10^{-15}) and exact Gaussian/(l_2) identities |
| 4 | Figure 2 — low-dimensional SGG improvement | [`check_accepted_claims.py`](repro/src/check_accepted_claims.py), [`figure2_qmc.csv`](space/artifacts/claim4/figure2_qmc.csv), [claim page](space/pages/current/claim4/page.md) | `VERIFIED`, high confidence: judged values retained and independent replicated QMC gives 14.87%, 11.98%, and 10.02% reductions; the paper does not publish raw coordinates or optimizer settings |
| 5 | Table 2 — supporting-line threshold bounds | [`check_accepted_claims.py`](repro/src/check_accepted_claims.py), [`table2.csv`](space/artifacts/claim5/table2.csv), [claim page](space/pages/current/claim5/page.md) | `VERIFIED`, high confidence: all seven printed thresholds pass an analytic-derivative audit with explicit rounding slack |
| 6 | Lemma D.1 and Algorithm 7 — tight SGG composition | [`algorithm7.py`](repro/src/algorithm7.py), [`check_composition.py`](repro/src/check_composition.py), [claim page](space/pages/current/claim6/page.md) | `VERIFIED`, high confidence: complete Figure 3 regime, 72-case sweep, and direct/FFT agreement to (7.37\times10^{-18}) |

### How each claim is produced

Each claim follows the same evidence chain:

`paper anchor → claim contract → executable derivation/checker → raw JSON/CSV → negative control → cumulative verifier → human-readable report`

Run the cumulative gate with:

```bash
uv run --frozen python repro/src/verify.py
```

The public evidence pages under [`space/pages/current`](space/pages/current) expose the exact contract, assumptions, source anchor, command, raw result, control, and limitation for each claim. The illustrated synthesis is [`reports/reproduction/report.md`](reports/reproduction/report.md); the reproducible tutorial is [`notebooks/gaussian_sgg_reproduction.py`](notebooks/gaussian_sgg_reproduction.py).

## Results at a glance

| Result | Evidence |
|---|---|
| Theorem 3.1 | 12-step structured derivation; worst finite-(T) calibration gap (2.697\times10^{-4}) at (T=65{,}536) |
| Lemma 3.3 | MSE-preserving Haar algebra and 56/56 exact finite-group cases |
| SGG family | Five adaptive integrals; maximum normalization error (3.55\times10^{-15}) |
| Figure 2 | Judged 15.0/12.6/10.5% reductions; independent QMC 14.87/11.98/10.02% |
| Table 2 | 7/7 analytic-derivative checks pass |
| Algorithm 7 | 31.4% reduction at (k=2) rising to 94.3% at (k=32); 72-case sweep |

The previous live judged score recorded by the evidence package is `9/12`. The `10–12/12` value in the release pages is a forecast, not a new judge result.

## Reproduce locally

Dependencies are pinned by [`pyproject.toml`](pyproject.toml) and [`uv.lock`](uv.lock). No GPU is required.

```bash
uv run --frozen python repro/src/verify.py
uv run marimo edit notebooks/gaussian_sgg_reproduction.py
```

Short checks use a one-thread local CPU. The larger calibration and regression jobs used Hugging Face `cpu-upgrade`; their commands, durations, and cost estimates are recorded in [`reports/reproduction/command-log.md`](reports/reproduction/command-log.md).

## Branch map

The current public branch names describe their role:

| Branch family | Purpose |
|---|---|
| [`historical/judged-baseline`](https://github.com/MachineLearning-Nerd/icml26-gaussian-mechanism-sgg-dp/tree/historical/judged-baseline) | Preserve the locked 9/12 judged-scope baseline |
| [`audit/table2-rounding-tolerance`](https://github.com/MachineLearning-Nerd/icml26-gaussian-mechanism-sgg-dp/tree/audit/table2-rounding-tolerance) | Calibrate six-decimal Table 2 publication rounding |
| [`audit/lemma33-haar-proof`](https://github.com/MachineLearning-Nerd/icml26-gaussian-mechanism-sgg-dp/tree/audit/lemma33-haar-proof) | Reconstruct and test the universal Haar argument |
| [`audit/theorem31-finite-calibration`](https://github.com/MachineLearning-Nerd/icml26-gaussian-mechanism-sgg-dp/tree/audit/theorem31-finite-calibration) | Reconstruct Theorem 3.1 and calibrate its finite-(T) asymptotic step |
| [`audit/algorithm7-composition`](https://github.com/MachineLearning-Nerd/icml26-gaussian-mechanism-sgg-dp/tree/audit/algorithm7-composition) | Implement and test Algorithm 7 and the Figure 3 regime |
| [`audit/claims3-5-independent`](https://github.com/MachineLearning-Nerd/icml26-gaussian-mechanism-sgg-dp/tree/audit/claims3-5-independent) | Independently rerun Claims 3–5 with QMC, quadrature, and derivative checks |
| [`release/claim1-visibility`](https://github.com/MachineLearning-Nerd/icml26-gaussian-mechanism-sgg-dp/tree/release/claim1-visibility) | Make Claim 1 evidence evaluator-visible |
| [`release/claim2-visibility`](https://github.com/MachineLearning-Nerd/icml26-gaussian-mechanism-sgg-dp/tree/release/claim2-visibility) | Make Claim 2 evidence evaluator-visible |
| [`release/claim6-visibility`](https://github.com/MachineLearning-Nerd/icml26-gaussian-mechanism-sgg-dp/tree/release/claim6-visibility) | Make Claim 6 evidence evaluator-visible |
| [`release/claims3-5-visibility`](https://github.com/MachineLearning-Nerd/icml26-gaussian-mechanism-sgg-dp/tree/release/claims3-5-visibility) | Make Claims 3–5 evidence evaluator-visible |
| [`release/evaluator-red-team`](https://github.com/MachineLearning-Nerd/icml26-gaussian-mechanism-sgg-dp/tree/release/evaluator-red-team) | Final visibility and evaluator red-team gate |
| [`release/standalone-space-root`](https://github.com/MachineLearning-Nerd/icml26-gaussian-mechanism-sgg-dp/tree/release/standalone-space-root) | Verify the same audit from a downloaded Space root |
| [`release/publication-metadata`](https://github.com/MachineLearning-Nerd/icml26-gaussian-mechanism-sgg-dp/tree/release/publication-metadata) | Publication metadata and final release surface |

[`branch-audit.md`](branch-audit.md) records the exact old-to-new branch mapping and how each branch contributes to the claim lineage.

## Repository contents

- `repro/src/` — executable proof certificates, mechanism definitions, checkers, controls, and release verification.
- `reports/reproduction/` — illustrated report, figures, and command ledger.
- `space/` — evaluator-facing claim pages, contracts, raw artifacts, controls, and historical judged snapshot.
- `notebooks/` — interactive evidence-first reproduction tutorial.
- `release/` — Space upload allowlists and release hashes.

## Scope and limitations

- The paper does not publish author code, raw Figure 2/3 coordinates, or all numerical settings; this audit uses a pinned independent implementation and preserves those substitutions explicitly.
- Theorem 3.1 is supported by a structured Python/SymPy derivation plus finite calibration, not a Lean/Coq proof-kernel object.
- The figures and tables establish the stated reproduction targets; they do not imply uniform SGG dominance in every dimension or privacy configuration.
- The original judged Space revision and its score are preserved as historical evidence; later release branches are candidates until independently evaluated.

## Citation

```bibtex
@misc{wei2026asymptotic,
  title         = {Asymptotic Optimality of the High-Dimensional Gaussian Mechanism and Improved Low-Dimensional Mechanisms for Differential Privacy},
  author        = {Wei, Yu and Bienstock, Alexander and Polychroniadou, Antigoni},
  year          = {2026},
  eprint        = {2606.08681},
  archivePrefix = {arXiv},
  primaryClass  = {cs.CR},
  url           = {https://arxiv.org/abs/2606.08681}
}
```

## Thank you

Thank you to Yu Wei, Alexander Bienstock, and Antigoni Polychroniadou for the clear theoretical framing of Gaussian optimality, the SGG mechanism family, and tight composition. This independent audit is intended to make those claims easier to inspect and reproduce.

## Attribution

Repository maintenance commits in the cleaned branch histories use:

`MachineLearning-Nerd <37579156+MachineLearning-Nerd@users.noreply.github.com>`

The paper and its authors remain the source of the research claims; this repository contains an independent reproduction and audit record.
