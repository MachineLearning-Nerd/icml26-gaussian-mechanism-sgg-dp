# Current verification — Claim 4: low-dimensional SGG improvement

**Verdict: VERIFIED.** Figure 2 claims that at
`epsilon=0.1,delta=0.1`, selected SGG mechanisms improve MSE by up to about
15% in dimensions 2–5, with the advantage shrinking as dimension grows. This
is an existence claim, not uniform SGG dominance.

The immutable judged reproduction remains reachable and reports 15.0%,
12.6%, and 10.5%. A new independent checker uses eight independently
scrambled Sobol replicates of 32,768 points per configuration:

| T | alpha | p | Mean MSE reduction | 95% half-width |
|---:|---:|---:|---:|---:|
| 2 | 1.0 | 4.0 | 14.8687% | 0.00172 pp |
| 3 | 2.0 | 4.5 | 11.9777% | 0.00158 pp |
| 5 | 3.5 | 6.0 | 10.0228% | 0.00386 pp |

The independent values corroborate the reported magnitude and strict
dimension trend without pretending to recover unpublished optimizer settings.
The negative control replaces the non-Gaussian shapes by the exact Gaussian
special case (`p=2,alpha=T-1`), whose MSE reduction is exactly zero.

Source: arXiv:2606.08681v1, Figure 2 and Section 4.3. Retrieved
2026-07-28; HTML SHA-256
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
[raw replicate JSON](../../../artifacts/claim4/raw_output.json),
[CSV](../../../artifacts/claim4/figure2_qmc.csv),
[control output](../../../artifacts/claim4/control_output.json), and
[claim contract](../../../artifacts/claim4/claim_contract.json) are directly
downloadable. Limitation: paper code, seeds, raw points, and optimizer settings
are unpublished.

## Limitations and deviations

The paper's optimizer settings and raw Figure 2 coordinates are unpublished.
The independent QMC configurations test the stated existence, magnitude, and
dimension trend; they do not claim coordinate-for-coordinate recovery.
