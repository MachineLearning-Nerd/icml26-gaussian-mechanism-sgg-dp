# Reproduction: Gaussian optimality and SGG mechanisms

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-82Wosp2Iu1-asymptotic-optimality-of-the-high-dimensional-gaussian-mechanism-and-improve/blob/main/notebooks/gaussian_sgg_reproduction.py)

This repository reproduces all six judged claims from
[arXiv:2606.08681](https://arxiv.org/abs/2606.08681),
*Asymptotic Optimality of the High-Dimensional Gaussian Mechanism and Improved
Low-Dimensional Mechanisms for Differential Privacy*.

The strongest empirical result is the paper's exact Figure 3 regime:
`T=10`, `alpha=9`, `p=1`, total `(epsilon,delta)=(1,10^-5)`, and
`k={2,4,8,16,32}`. Algorithm 7 reduces required per-invocation MSE by 31.4% at
`k=2`, rising monotonically to 94.3% at `k=32`, versus sequential composition.
Theorem 3.1 is addressed by a universal structured derivation plus a separate
256-case finite-\(T\) calibration; the finite sweep is not presented as proof.

Previous live judged score: **9/12**. Conservative post-release forecast:
**10–12/12**. A possible **12/12 is a forecast, not a judge result**.

- [Illustrated reproduction report](reports/reproduction/report.md)
- [Evidence-first marimo tutorial](notebooks/gaussian_sgg_reproduction.py)
- [Evaluator-facing candidate logbook](space/README.md)

## Results at a glance

| Claim | Paper result | Observed result | Assessment |
|---|---|---|---|
| Theorem 3.1 | Gaussian asymptotically minimax as `T→∞` | 12-step universal derivation; worst 256-case gap `2.70e-4` at `T=65536` | VERIFIED, MEDIUM confidence |
| Lemma 3.3 | Haar preserves MSE and cannot worsen privacy | universal algebra; 56/56 exact finite-group cases | VERIFIED |
| SGG family | normalized; contains Gaussian and `l2` | max integral error `3.55e-15`; MSE identities exact | VERIFIED |
| Figure 2 | up to 15%, shrinking with `T` | judged 15.0/12.6/10.5%; independent 14.87/11.98/10.02% | VERIFIED |
| Table 2 | seven threshold lower bounds | 7/7 pass analytic-derivative audit | VERIFIED |
| Algorithm 7 | growing tight-composition advantage | 31.4% → 94.3%; 72-case sweep; direct/FFT error `7.37e-18` | VERIFIED |

Substitutions and limitations: the paper publishes neither author code nor raw
Figure 2/3 coordinates or numerical settings. The reproduction uses a pinned
independent implementation, reports its settings and uncertainty, and keeps
the original judged Space revision intact. The proof certificates are
structured Python/SymPy derivations rather than formal proof-kernel objects.

## Reproduce

All experiment nodes inherit the same exact command:

```bash
uv run --frozen python repro/src/verify.py
```

Dependencies are pinned by `pyproject.toml` and `uv.lock` in one repository
`.venv`. Short checks used one-thread local CPU. Parallel or uncertain checks
used Hugging Face `cpu-upgrade` (64 CPUs visible, 8 workers); no GPU was used.

To explore the tutorial locally:

```bash
uv run marimo edit notebooks/gaussian_sgg_reproduction.py
uv run marimo run notebooks/gaussian_sgg_reproduction.py
```

## Experiment log

| Branch / experiment | Purpose or change | Exact run command | Assessment / outcome | Compute |
|---|---|---|---|---|
| `main` | Publication surface | Not run as an experiment (publication surface) | Mirrors the validated winning candidate after release | — |
| [`orx/locked-9-12-reproduction-baseline`](https://github.com/MachineLearning-Nerd/icml26-repro-82Wosp2Iu1-asymptotic-optimality-of-the-high-dimensional-gaussian-mechanism-and-improve/tree/orx/locked-9-12-reproduction-baseline) | Freeze judged-scope baseline | `uv run --frozen python repro/src/verify.py` | 5/6; exposed six-decimal Table 2 tolerance issue | local, 1 thread |
| [`orx/calibrated-table-2-rounding-tolerance`](https://github.com/MachineLearning-Nerd/icml26-repro-82Wosp2Iu1-asymptotic-optimality-of-the-high-dimensional-gaussian-mechanism-and-improve/tree/orx/calibrated-table-2-rounding-tolerance) | Calibrate published threshold rounding | `uv run --frozen python repro/src/verify.py` | 6/6 passed | local, 1 thread |
| [`orx/haar-lemma-symbolic-proof-certificate`](https://github.com/MachineLearning-Nerd/icml26-repro-82Wosp2Iu1-asymptotic-optimality-of-the-high-dimensional-gaussian-mechanism-and-improve/tree/orx/haar-lemma-symbolic-proof-certificate) | Universal Lemma 3.3 derivation | `uv run --frozen python repro/src/verify.py` | 7/7 passed; 3 controls rejected | local, 1 thread |
| [`orx/theorem-3-1-proof-and-finite-t-calibration`](https://github.com/MachineLearning-Nerd/icml26-repro-82Wosp2Iu1-asymptotic-optimality-of-the-high-dimensional-gaussian-mechanism-and-improve/tree/orx/theorem-3-1-proof-and-finite-t-calibration) | Universal theorem derivation plus asymptotic calibration | `uv run --frozen python repro/src/verify.py` | 10/10 passed; 256 finite-\(T\) cases | local, 1 thread |
| [`orx/algorithm-7-exact-composition-accountant`](https://github.com/MachineLearning-Nerd/icml26-repro-82Wosp2Iu1-asymptotic-optimality-of-the-high-dimensional-gaussian-mechanism-and-improve/tree/orx/algorithm-7-exact-composition-accountant) | Exact Algorithm 7 and Figure 3 | `uv run --frozen python repro/src/verify.py` | 11/11 passed; 72-case sweep | HF `cpu-upgrade`, 8 workers |
| [`orx/independent-regressions-for-claims-3-to-5`](https://github.com/MachineLearning-Nerd/icml26-repro-82Wosp2Iu1-asymptotic-optimality-of-the-high-dimensional-gaussian-mechanism-and-improve/tree/orx/independent-regressions-for-claims-3-to-5) | Independent QMC, quadrature, and derivative checks | `uv run --frozen python repro/src/verify.py` | 14/14 passed | HF `cpu-upgrade`, 8 workers |
| [`orx/release-candidate-and-evaluator-red-team`](https://github.com/MachineLearning-Nerd/icml26-repro-82Wosp2Iu1-asymptotic-optimality-of-the-high-dimensional-gaussian-mechanism-and-improve/tree/orx/release-candidate-and-evaluator-red-team) | Final visibility, reports, and release audit | `uv run --frozen python repro/src/verify.py` | 15/15 passed on hash-locked evidence commit `ef4cb61` | HF `cpu-upgrade`, 8 vCPU allocation, 8 workers |

## Source provenance

- Paper HTML retrieved 2026-07-28 with an explicit User-Agent; SHA-256
  `a02952f28208ebacabb7e555436985040f909dd881786f74d71cd4aee7841a38`.
- Protected judged Space:
  `DineshAI/82Wosp2Iu1@2d5f672ab576722614a3c86d48550e74fee2aca4`.
- Original validated baseline SHA:
  `55660297e858b03ca0dea5c0ed91d616ece44add`.
- [Material command ledger](reports/reproduction/command-log.md).
