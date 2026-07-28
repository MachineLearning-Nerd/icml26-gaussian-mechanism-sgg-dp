# Claim 1 run record

- Fixed command: `uv run --frozen python repro/src/verify.py`
- Scientific Git SHA: `bc38201f53d152cffbd52c2756f0ee8cd62c37e7`
- Seed: `20260728`
- Environment: repository `.venv`, Python 3.12, exact `uv.lock`
- Backend: local CPU, one effective native thread
- Core estimate / allocation: 1 / 1 effective (8 logical CPUs visible)
- Estimated / measured verifier runtime: 10 s / 0.990255167 s
- Result: 12/12 proof-DAG steps and 256/256 finite-\(T\) cases passed;
  3/3 negative controls rejected
