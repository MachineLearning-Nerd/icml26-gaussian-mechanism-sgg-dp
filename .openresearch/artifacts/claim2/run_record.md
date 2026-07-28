# Claim 2 run record

- Fixed command: `uv run --frozen python repro/src/verify.py`
- Scientific Git SHA: `7e4615a51d77686a55d43595bd13cff613949028`
- Seed: `20260728`
- Environment: repository `.venv`, Python 3.12, exact `uv.lock`
- Backend: local CPU, one effective native thread
- Core estimate / allocation: 1 / 1 effective (8 logical CPUs visible)
- Estimated / measured verifier runtime: 5 s / 0.896091333 s
- Result: universal certificate and 56/56 finite-group cases passed;
  3/3 negative controls rejected
