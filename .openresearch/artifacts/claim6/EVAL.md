# Claim C5 evaluation

Run:

```bash
uv run --frozen python repro/src/verify.py
```

The `C5-ALGORITHM7` record must pass the exact Figure 3 regime, all broad
coarse/fine comparisons, the adaptive-integral and direct-convolution
independent checks, and all three negative controls. Every retained claim must
also pass. Any failure causes a nonzero exit.
