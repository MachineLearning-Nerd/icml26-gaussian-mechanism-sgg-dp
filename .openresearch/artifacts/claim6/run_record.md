# Claim 6 run record

- Fixed command: `uv run --frozen python repro/src/verify.py`
- Scientific Git SHA: `3c4970bd873cb9440d24713d14e4818fed78976f`
- Seed: `20260728`
- Environment: repository `.venv`, Python 3.12, exact `uv.lock`
- Backend / flavor: Hugging Face / `cpu-upgrade`
- Core estimate / contracted allocation: 8 / 8 vCPU
- Container-visible CPUs / workers: 64 / 8
- Estimated / measured verifier runtime: 1,200 s / 14.507730 s
- `orx` job duration: 37 s
- Result: five Figure 3 settings and 72 broad settings passed; all independent
  checks passed and 3/3 negative controls were rejected
