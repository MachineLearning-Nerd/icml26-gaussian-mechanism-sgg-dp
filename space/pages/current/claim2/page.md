# Current verification — Claim 2: Haar symmetrization

**Verdict: VERIFIED.** This page supersedes the single-anisotropic-Gaussian
spot check on the page labeled **Historical rejected baseline**. It tests the
exact universally quantified Lemma 3.3 by an independently reconstructed
symbolic derivation; no finite sweep is presented as a proof.

## Exact claim contract

For every integer `T >= 2`, every `epsilon >= 0`, every `s > 0`, every
`R^T`-valued random vector `X` with finite second moment, and an independent
Haar-uniform `M` on the orthogonal group `O(T)`, define `X' = MX`. Then:

1. `X'` is spherically symmetric;
2. `E||X'||_2^2 = E||X||_2^2`;
3. `sup_{||v||<=s} H_epsilon(X',X'+v) <=
   sup_{||v||<=s} H_epsilon(X,X+v)`.

Source: arXiv:2606.08681v1, Lemma 3.3, anchors `S3.Thmlemma3` and
`A2.6`. The HTML was retrieved on 2026-07-28 with an explicit User-Agent;
SHA-256:
`a02952f28208ebacabb7e555436985040f909dd881786f74d71cd4aee7841a38`.

## What was verified

The certificate has 13 dependency-checked steps:

- orthogonality gives `||Mx||^2=||x||^2` pointwise, hence equal MSE;
- Haar left invariance gives `QMX =_d MX` for every `Q in O(T)`;
- convexity of the positive-part function gives joint convexity of
  hockey-stick divergence under mixtures;
- conditioning on `M`, applying the bijection `M^T`, and using
  `||M^Tv||=||v||` bounds every shift by the original worst-direction
  supremum.

The symbolic isometry identity and both exhaustive sign cases for
positive-part convexity passed. Three deliberately invalid mutations were all
rejected. An independent exact finite-group checker is run separately as
corroboration and is explicitly not substituted for the universal proof.

## Raw result

| Field | Value |
|---|---:|
| Git SHA | `7e4615a51d77686a55d43595bd13cff613949028` |
| Seed | `20260728` |
| Backend / flavor | local / local-single-core |
| Estimated cores | 1 |
| Visible CPUs / effective threads | 8 / 1 |
| Estimated verifier runtime | 5 s |
| Measured verifier runtime | 0.896091333 s |
| Proof DAG | 13/13 steps accepted |
| Negative controls | 3/3 rejected |
| Cumulative suite | 7/7 passed |
| Certificate SHA-256 | `e99822a1dc9af3da55718f9076e993b144ca7b7e7cf31216d1bfaa8d561af35b` |

Download [raw JSON](../../../artifacts/claim2/raw_output.json) and
[negative-control JSON](../../../artifacts/claim2/control_output.json).

## Reproduce

The fixed command is identical on every experiment node:

```bash
uv run --frozen python repro/src/verify.py
```

The candidate contains the exact locked `pyproject.toml`, `uv.lock`, cumulative
verifier, proof verifier, and independent checker. The process exits nonzero if
any proof obligation, independent check, negative control, or retained
full-credit regression fails.

## Limitations

This is a machine-checked structured derivation, not a Lean/Coq kernel proof.
The standard imported facts—Haar left invariance, orthogonal isometry, and
hockey-stick invariance under measurable bijections—are listed explicitly.
The previous Gaussian instance is preserved only as historical corroboration
and is not the current verifier.

