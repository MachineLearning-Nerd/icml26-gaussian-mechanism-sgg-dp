# Current verification — Claim 3: the SGG family

**Verdict: VERIFIED.** Definitions 4.1–4.2 state that, for
`alpha>-1,beta>0,p>0`,

`f_R(r)=p beta^((alpha+1)/p) r^alpha exp(-beta r^p) /
Gamma((alpha+1)/p)`

is a normalized radial density. Gaussian noise is the
`alpha=T-1,p=2,beta=1/(2 sigma^2)` special case; spherical `l2` noise is
`alpha=T-1,p=1,beta=1/theta`.

Five independent adaptive integrals have maximum normalization error
`3.55e-15`. The special-case MSEs are exact:

| Check | Observed | Expected |
|---|---:|---:|
| Gaussian, `T=4,sigma^2=1.5` | 6.0 | 6.0 |
| `l2`, `T=4,theta=0.7` | 9.8 | 9.8 |

The negative control omits the leading `p`; at `p=2` its integral is `0.5`,
so it is rejected.

Source: arXiv:2606.08681v1, Definitions 4.1–4.2 and Proposition 4.1.
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
[raw JSON](../../../artifacts/claim3/raw_output.json),
[control output](../../../artifacts/claim3/control_output.json), and
[claim contract](../../../artifacts/claim3/claim_contract.json) are directly
downloadable. The analytic identity is primary; quadrature is an independent
executable regression.

## Limitations and deviations

The numerical integration is an independent regression, not the basis for the
closed-form normalization proof. No author code was available.
