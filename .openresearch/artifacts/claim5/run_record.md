# Claim 5 run record

- Fixed command: `uv run --frozen python repro/src/verify.py`
- Scientific Git SHA: `3a38e9ec8587c59f15192c21428de092059b781f`
- Seed: `20260728`
- Environment: repository `.venv`, Python 3.12, exact `uv.lock`
- Backend / flavor: Hugging Face / `cpu-upgrade`
- Core estimate / contracted allocation: 8 / 8 vCPU
- Container-visible CPUs / workers: 64 / 8
- Estimated / measured cumulative verifier runtime: 1,200 s / 15.488085 s
- Result: 7/7 Table 2 rows passed; the out-of-domain threshold control failed
  both required conditions as intended
