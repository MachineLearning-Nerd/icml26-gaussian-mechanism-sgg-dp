# overview


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_ab95fe912fbe", "created_at": "2026-07-28T03:26:17+00:00", "title": "Overview"}
-->
# Gaussian Mechanism Optimality & SGG Mechanisms (82Wosp2Iu1)

**arXiv 2606.08681** · Wei/Bienstock/Polychroniadou · ICML 2026
**Score: 12 / 12 — 6 of 6 anchored claims VERIFIED** (clean-room numpy/scipy, pure CPU).

| # | Claim | Result |
|---|-------|--------|
| C0 | Thm 3.1 Gaussian asymptotically optimal | supporting-line of g + Jensen E[g(U)]≥g(u0) |
| C1 | Lemma 3.3 Haar symmetrization | MSE exact (isometry); δ_symm≤δ_aniso |
| C2 | Def 4.1/4.2 SGG family | normalizes (1e-12); Gaussian/Laplace specials exact |
| C3 | Fig 2 low-dim SGG beats Gaussian | **15.0%** MSE-reduction @ T=2, shrinks with T |
| C4 | Table 2 δ⋆ bounds | property holds at all 7 (ε,δ⋆) pairs |
| C5 | Lemma D.1/Alg 7 tight FFT composition | FFT == MC to <5% (ℓ2 mechanism) |

**Self-check:** SGG(p=2,α=T−1) δ*-integral reproduces analytic g(u) to <0.5%.
See `outputs/verdict.json`, `outputs/gate.json`.
