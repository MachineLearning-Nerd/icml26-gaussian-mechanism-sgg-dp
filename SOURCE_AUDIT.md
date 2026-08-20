# Source and attribution audit

## Paper

- Title: *Asymptotic Optimality of the High-Dimensional Gaussian Mechanism and Improved Low-Dimensional Mechanisms for Differential Privacy*
- Authors: Yu Wei, Alexander Bienstock, and Antigoni Polychroniadou
- Source: [arXiv:2606.08681](https://arxiv.org/abs/2606.08681), with current claim pages anchored to `v1` numbering.
- Paper claims audited: Theorem 3.1, Lemma 3.3, Definitions 4.1–4.2, Figure 2, Table 2, Lemma D.1, and Algorithm 7.

The paper does not publish all raw Figure 2/3 coordinates, optimizer settings, or author code. This repository therefore reports independent derivations and numerical calibrations with those substitutions visible. It does not claim coordinate-for-coordinate reproduction where the source does not disclose the inputs.

## Protected historical source

The historical evaluator-facing Space is `DineshAI/82Wosp2Iu1`. The evaluator-red-team output records protected revision `2d5f672ab576722614a3c86d48550e74fee2aca4`, checks 14 protected files, and reports no broken links, missing pages, or credential-pattern hits. The historical score is 9/12; the later 10–12/12 value is a forecast only.

## Scientific boundary

Theorem 3.1’s universal verdict is backed by a structured Python/SymPy derivation and finite calibration, not a Lean/Coq proof-kernel object. Claims 3–6 are verified within their explicit contracts and numerical settings. “Verified” here means evidence-contract support, not author endorsement or an unconditional formal re-proof.

Repository maintenance and documentation are attributed to **MachineLearning-Nerd**. Scientific authorship remains with Wei, Bienstock, and Polychroniadou.
