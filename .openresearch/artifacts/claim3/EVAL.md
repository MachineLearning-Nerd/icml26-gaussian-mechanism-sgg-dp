# Claim C2 evaluation

Status: **VERIFIED**

Run the fixed command:

```bash
uv run --frozen python repro/src/verify.py
```

The verifier prints the raw result inline, writes `outputs/verdict.json`, and
exits nonzero on any failed identity. No limitation affects the exact family
definition; numerical evaluation is only used to represent the identities in
floating point.

