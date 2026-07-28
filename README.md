# Reproduction baseline: high-dimensional Gaussian mechanism and SGG

This repository is the reproducible research surface for arXiv:2606.08681.
The initial baseline preserves the scope of the previously judged 9/12
artifact: SGG definition/special cases, the low-dimensional improvement
configurations, and Table 2 remain regression-tested, while Theorem 3.1, Lemma
3.3, and Algorithm 7 are explicitly labeled historical weak checks until child
experiments add proof-level or full-grid evidence.

Fixed command:

```bash
uv run --frozen python repro/src/verify.py
```

The environment is locked by `uv.lock`; all formal experiment nodes inherit
this command unchanged.

## Source provenance

- Paper: arXiv:2606.08681v1, retrieved 2026-07-28 from ar5iv with an explicit
  User-Agent; SHA-256 `a02952f28208ebacabb7e555436985040f909dd881786f74d71cd4aee7841a38`.
- Previous judged Hugging Face Space revision:
  `DineshAI/82Wosp2Iu1@2d5f672ab576722614a3c86d48550e74fee2aca4`.
- Previous live judged score: 9/12. No score increase is claimed.
