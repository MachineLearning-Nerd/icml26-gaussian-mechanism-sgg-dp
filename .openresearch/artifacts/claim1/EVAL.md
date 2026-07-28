# Claim C0 evaluation

Run:

```bash
uv run --frozen python repro/src/verify.py
```

The `C0-PROOF` record must verify the complete quantified derivation and reject
all three mutated claims. The separate `C0-FINITE-T` record must preserve the
mean constraint, satisfy the supporting-line lower bound, and show the exact
finite-sphere test approaching its Gaussian limit across every declared
privacy/radial-law configuration.
