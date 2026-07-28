# Current evaluator visibility matrix

This page is the release gate for discoverability. Starting only from
`README.md`, `logbook.json`, or `pages/index.md`, every current claim below is
reachable. “Complete” means that the canonical page itself exposes the exact
claim contract and source quantifiers, assumptions, executable source, fixed
command, pinned environment, inline numbers, raw downloads, independent
checker, failure-inducing control, limitations, Git SHA, seed, and CPU/runtime
record.

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | [Theorem 3.1](#/current-claim1) | Complete | Complete | [JSON](../../../artifacts/claim1/raw_output.json) | [finite-\(T\)](../../../repro/src/check_asymptotic_finite_t.py) | [3/3](../../../artifacts/claim1/control_output.json) | Complete | VERIFIED |
| 2 | [Lemma 3.3](#/current-claim2) | Complete | Complete | [JSON](../../../artifacts/claim2/raw_output.json) | [finite group](../../../repro/src/check_haar_independent.py) | [3/3](../../../artifacts/claim2/control_output.json) | Complete | VERIFIED |
| 3 | [SGG family](#/current-claim3) | Complete | Complete | [JSON](../../../artifacts/claim3/raw_output.json) | [quadrature](../../../repro/src/check_accepted_claims.py) | [omitted factor](../../../artifacts/claim3/control_output.json) | Complete | VERIFIED |
| 4 | [Figure 2](#/current-claim4) | Complete | Complete | [CSV](../../../artifacts/claim4/figure2_qmc.csv) | [replicated QMC](../../../repro/src/check_accepted_claims.py) | [Gaussian identity](../../../artifacts/claim4/control_output.json) | Complete | VERIFIED |
| 5 | [Table 2](#/current-claim5) | Complete | Complete | [CSV](../../../artifacts/claim5/table2.csv) | [analytic derivative](../../../repro/src/check_accepted_claims.py) | [out-of-domain threshold](../../../artifacts/claim5/control_output.json) | Complete | VERIFIED |
| 6 | [Algorithm 7](#/current-claim6) | Complete | Complete | [CSV](../../../artifacts/claim6/figure3.csv) | [independent convolution](../../../repro/src/check_composition.py) | [3/3](../../../artifacts/claim6/control_output.json) | Complete | VERIFIED |

The fixed command is `uv run --frozen python repro/src/verify.py`; it exits
nonzero when any proof obligation, experiment gate, independent checker,
negative control, preservation check, link check, or visibility check fails.
The exact environment is pinned by [pyproject.toml](../../../pyproject.toml)
and [uv.lock](../../../uv.lock).
