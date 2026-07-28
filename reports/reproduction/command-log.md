# Material command ledger

This ledger records the exact commands that changed scientific or publication
state, launched formal compute, or established release evidence. Read-only
diagnostic `git`, `sed`, `rg`, `find`, and `orx status/logs` invocations are
described by purpose rather than fabricated from shell history.

## Fixed environment and verifier

```bash
uv sync --frozen
uv run --frozen python repro/src/verify.py
uv run --frozen marimo check --strict notebooks/gaussian_sgg_reproduction.py
uv run --frozen python repro/src/build_release_manifest.py
```

The second command is the fixed project command inherited verbatim by every
experiment node. No environment-prefixed alternative was used.

## Formal experiment launches

Short, one-thread nodes used:

```bash
orx exp run <experiment-id> --backend local
```

This applied to the locked baseline, Table 2 calibration, Haar certificate,
evaluator-visible Claim 2, Theorem 3.1 certificate/calibration, and
evaluator-visible Claim 1 nodes.

Every Algorithm 7, Claims 3–5, and release-candidate run used:

```bash
orx exp run <experiment-id> --backend hf --flavor cpu-upgrade --timeout 30m
```

The release candidate's default HF image lacked `uv` and exited before the
verifier. Its successful relaunch used the same fixed command with:

```bash
orx exp run e3d33981-edce-48f6-8d40-b96e88868407 --backend hf --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim --timeout 30m
```

Every launch was followed by:

```bash
orx exp wait <experiment-id> --timeout 480
orx logs <run-id> --head --bytes 1000000
```

## Publication commands

The text-only Space staging directory is constructed from
`space/UPLOAD_ALLOWLIST.txt`, then uploaded in one Hugging Face API commit:

```bash
hf upload DineshAI/82Wosp2Iu1 <fresh-text-staging-dir> . --repo-type space --revision main --commit-message "Publish claim-by-claim reproduction evidence"
```

After post-upload hash verification, GitHub publication is:

```bash
git push origin <validated-release-sha>:main
git ls-remote origin refs/heads/main
```

No token value, generated run wrapper, direct training command, GPU command,
second Space creation, rebase, force-push, or destructive Git command is
included or used.
