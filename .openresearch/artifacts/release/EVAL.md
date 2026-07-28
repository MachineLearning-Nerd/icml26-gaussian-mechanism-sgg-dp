# Release-gate evaluation

Run the inherited fixed command:

```bash
uv run --frozen python repro/src/verify.py
```

`RELEASE-AUDIT` must pass alongside all 14 scientific checks. It requires six
complete visibility rows, no broken local links, 14/14 protected judged files,
an internally consistent text-only upload allowlist/hash manifest, and no known
credential patterns. Any failure exits nonzero.
