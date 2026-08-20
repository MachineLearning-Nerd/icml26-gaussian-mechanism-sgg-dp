# Audit report

All six current claim contracts pass the cumulative release gate, with Claim 1 explicitly marked medium confidence and Claims 2–6 high confidence within their stated scopes.

- Theorem 3.1: structured derivation plus 256 finite-`T` calibrations; no proof-kernel artifact.
- Lemma 3.3: universal Haar/isometry certificate plus 56 exact finite-group checks and rejected assumption mutations.
- SGG definitions: normalization and special cases pass to `3.55e-15`.
- Figure 2: independent QMC finds `14.87%`, `11.98%`, and `10.02%` reductions.
- Table 2: all seven analytic threshold checks pass with published-rounding slack.
- Algorithm 7: 72-case sweep and direct/FFT agreement support the reported composition behavior.

The historical judged score is 9/12; the release forecast of 10–12/12 is not a current score. The complete illustrated report is [`reports/reproduction/report.md`](reports/reproduction/report.md), the claim pages are under [`space/pages/current`](space/pages/current), and the machine-readable verdicts are in [`claims.json`](claims.json).
