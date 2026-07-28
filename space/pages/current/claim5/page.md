# Current verification — Claim 5: Table 2 thresholds

**Verdict: VERIFIED.** Table 2 gives seven empirical lower bounds on the
high-privacy threshold `delta_star`. At each published pair, Proposition 3.1
requires the Gaussian privacy curve to dominate its tangent on `[0,u0]` and
to be convex on `[u0,infinity)`.

An independent checker uses the analytic first derivative—not the retained
second finite difference—to test tangent dominance and derivative monotonicity
on 12,000 points per interval:

| epsilon | delta_star | Minimum tangent slack | Result |
|---:|---:|---:|---|
| 0.25 | 0.736670 | `0` | pass |
| 0.50 | 0.706970 | `-3.944e-7` | pass |
| 1 | 0.649185 | `0` | pass |
| 2 | 0.549133 | `0` | pass |
| 4 | 0.416972 | `-2.462e-7` | pass |
| 8 | 0.292170 | `-4.179e-7` | pass |
| 16 | 0.197615 | `0` | pass |

The sub-`1e-6` negative slacks arise from the paper's six-decimal published
thresholds and are reported, not rounded away. The negative control extends
the claim to `epsilon=1,delta=0.9`; it fails both conditions, with tangent
slack `-0.1080`.

Source: arXiv:2606.08681v1, Table 2, Section 3, and Proposition 3.1.
Retrieved 2026-07-28; HTML SHA-256
`a02952f28208ebacabb7e555436985040f909dd881786f74d71cd4aee7841a38`.

Run:

```bash
uv run --frozen python repro/src/verify.py
```

Formal run `9c41004b-5557-456c-85f4-c18da9b20634`, Git SHA
`3a38e9ec8587c59f15192c21428de092059b781f`, seed `20260728`, Hugging Face
`cpu-upgrade`, estimated 8 cores and 1,200 s, 64 CPUs actually visible,
8 workers, and 15.488085 s cumulative verifier runtime. The pinned environment
is Python 3.12.11, NumPy 2.5.1, SciPy 1.18.0, and SymPy 1.14.0 from
`uv.lock`.

[Executable checker](../../../repro/src/check_accepted_claims.py),
[raw JSON](../../../artifacts/claim5/raw_output.json),
[Table 2 CSV](../../../artifacts/claim5/table2.csv),
[control output](../../../artifacts/claim5/control_output.json), and
[claim contract](../../../artifacts/claim5/claim_contract.json) are directly
downloadable.

## Limitations and deviations

Table 2 prints six decimal places. The checker therefore reports the observed
sub-`1e-6` boundary slacks and applies the independently declared publication-
rounding tolerance rather than silently rounding them away.
