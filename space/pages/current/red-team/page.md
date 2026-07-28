# Evaluator-blind pre-publication red-team review

The review used only the downloaded candidate artifact and the evaluator
rubric. It began at `README.md`, `logbook.json`, and `pages/index.md`; no
OpenResearch logs, dashboard files, unpublished branches, or repository
knowledge supplied missing evidence.

## First pass

Files opened, in order:

1. `README.md`
2. `logbook.json`
3. `pages/index.md`
4. `pages/current/claim1/page.md` through
   `pages/current/claim6/page.md`
5. each linked `claim_contract.json`, raw JSON/CSV, control JSON, checker,
   `pyproject.toml`, and `uv.lock`
6. `historical/judged-root/PROTECTED_MANIFEST.sha256`

Two presentation gaps were found: the original judged `pages/index.md` had
not been copied into the explicit historical archive, and Claims 3–5 did not
state estimated CPU/runtime and pinned package versions inline. Both were
fixed. No scientific verdict changed.

## Repeated pass after fixes

The same traversal was repeated mechanically by
`repro/src/release_audit.py`. It verifies:

- all current pages are reachable from the canonical entrypoints;
- every claim page contains the required claim, source, code, command,
  environment, inline data, raw link, checker, control, limitation,
  provenance, and CPU/runtime markers;
- every local Markdown link resolves;
- each file from judged revision
  `2d5f672ab576722614a3c86d48550e74fee2aca4` is present byte-for-byte either
  at its original path or under `historical/judged-root/`;
- the upload allowlist and hashes are internally consistent;
- no known credential pattern appears in evaluator-visible text.

The repeated review has no missing visibility-matrix cells. Historical
`verify` and `overview` pages remain labeled **Historical rejected baseline**;
the six current pages precede them in navigation and state which verifier
supersedes the old one.

Formal HF run `d06e3203-e897-4da2-b8e8-8b81bd960475` independently executed
the same audit from hash-locked evidence commit
`ef4cb61d7584835c1836b3b924a4bfd9eff703bd`: 15/15 cumulative checks passed,
including the release audit.
