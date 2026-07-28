# Material command ledger

This ledger contains every command that changed scientific/publication state
or launched formal compute. Read-only diagnostic searches and file views are
recorded by the red-team page's opened-file list.

## Fixed environment and verifier

```bash
uv sync --frozen
uv run --frozen python repro/src/verify.py
uv run --frozen marimo check --strict notebooks/gaussian_sgg_reproduction.py
uv run --frozen python repro/src/build_release_manifest.py
```

The second command is inherited verbatim by every experiment node.

## Formal compute

Short one-thread nodes:

```bash
orx exp run <experiment-id> --backend local
```

Every uncertain or parallel node:

```bash
orx exp run <experiment-id> --backend hf --flavor cpu-upgrade --timeout 30m
```

The release node pins an image that contains `uv`:

```bash
orx exp run e3d33981-edce-48f6-8d40-b96e88868407 --backend hf --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim --timeout 30m
```

Every launch is reconciled through:

```bash
orx exp wait <experiment-id> --timeout 480
orx logs <run-id> --head --bytes 1000000
```

## Publication

The allowlisted text is copied to a fresh empty staging directory and uploaded
through the Hugging Face API:

```bash
hf upload DineshAI/82Wosp2Iu1 <fresh-text-staging-dir> . --repo-type space --revision main --commit-message "Publish claim-by-claim reproduction evidence"
```

After exact-revision download and hash verification:

```bash
git push origin <validated-release-sha>:main
git ls-remote origin refs/heads/main
```

No GPU launch, second Space creation, token value, generated run wrapper,
unmanaged `pip`, conda, rebase, force-push, or destructive Git command is used.
