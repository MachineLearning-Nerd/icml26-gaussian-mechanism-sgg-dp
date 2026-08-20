# Reproduction environment

Dependencies are pinned by [`pyproject.toml`](pyproject.toml) and [`uv.lock`](uv.lock). The fixed cumulative command is:

```bash
uv sync --frozen
uv run --frozen python repro/src/verify.py
```

Recorded environments include:

| Component | Value |
| --- | --- |
| Python | `3.12.11` |
| NumPy | `2.5.1` |
| Local short checks | CPU, one effective thread |
| Larger calibration/regression jobs | Hugging Face `cpu-upgrade` |
| GPU | None required |
| Claim 1 finite calibration | 16 dimensions × 4 epsilons × 4 radial laws = 256 cases |
| Claim 2 finite checker | 56 exact finite-group cases |
| Claim 6 broad sweep | 72 configurations |

The material command history is [`reports/reproduction/command-log.md`](reports/reproduction/command-log.md). The evidence-first verifier reads committed artifacts; it does not silently regenerate the larger jobs.
