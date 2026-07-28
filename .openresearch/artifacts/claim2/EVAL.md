# Claim C1 evaluation

Run the inherited fixed command:

```bash
uv run --frozen python repro/src/verify.py
```

Success requires the `C1-PROOF` record to report `VERIFIED`, all proof
obligations to pass, and all three negative controls to be rejected. Any failure
causes a nonzero process exit.

