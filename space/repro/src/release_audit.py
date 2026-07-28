"""Machine-enforced evaluator-visible release audit.

The audit deliberately begins from the same three entrypoints available to an
evaluator. It does not consult OpenResearch logs or the experiment database.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import deque
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[2]
# In the GitHub reproduction repo, the candidate lives under ``space/``.
# In a downloaded Hugging Face Space, these same files are at repository root.
SPACE = ROOT / "space" if (ROOT / "space").is_dir() else ROOT
ENTRYPOINTS = ("README.md", "logbook.json", "pages/index.md")
CURRENT_PAGES = tuple(f"pages/current/claim{i}/page.md" for i in range(1, 7))
RELEASE_PAGES = (
    "pages/current/visibility/page.md",
    "pages/current/release/page.md",
    "pages/current/red-team/page.md",
)
REQUIRED_MARKERS = (
    "verdict: verified",
    "arxiv:2606.08681",
    "claim contract",
    "uv run --frozen python repro/src/verify.py",
    "uv.lock",
    "raw",
    "checker",
    "control",
    "limitation",
    "git sha",
    "seed",
    "cpu",
    "runtime",
)
SECRET_PATTERNS = {
    "hugging-face token": re.compile(r"\bhf_[A-Za-z0-9]{20,}\b"),
    "OpenAI key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "GitHub fine-grained token": re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    "GitHub classic token": re.compile(r"\bghp_[A-Za-z0-9]{20,}\b"),
}
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _logbook_map() -> dict[str, str]:
    payload = json.loads((SPACE / "logbook.json").read_text())
    mapping: dict[str, str] = {}

    def visit(node: dict) -> None:
        mapping[node["slug"]] = node["file"]
        for child in node.get("children", []):
            visit(child)

    visit(payload["root"])
    return mapping


def _resolve_link(source: Path, target: str, slugs: dict[str, str]) -> Path | None:
    clean = unquote(target.strip().split(maxsplit=1)[0]).strip("<>")
    if clean.startswith(("http://", "https://", "mailto:")):
        return None
    if clean.startswith("#/"):
        slug = clean[2:].split("/", maxsplit=1)[0]
        return SPACE / slugs[slug] if slug in slugs else SPACE / f"__missing_slug__/{slug}"
    clean = clean.split("#", maxsplit=1)[0]
    if not clean:
        return None
    return (source.parent / clean).resolve()


def _traverse() -> tuple[list[str], list[str]]:
    slugs = _logbook_map()
    queue: deque[Path] = deque((SPACE / entry).resolve() for entry in ENTRYPOINTS)
    queue.extend((SPACE / path).resolve() for path in slugs.values())
    opened: set[Path] = set()
    missing: list[str] = []
    while queue:
        path = queue.popleft()
        if path in opened:
            continue
        if not path.is_file() or SPACE.resolve() not in path.parents:
            missing.append(str(path))
            continue
        opened.add(path)
        if path.suffix.lower() != ".md":
            continue
        for target in LINK.findall(path.read_text()):
            resolved = _resolve_link(path, target, slugs)
            if resolved is not None:
                queue.append(resolved)
    relative = sorted(str(path.relative_to(SPACE.resolve())) for path in opened)
    return relative, sorted(set(missing))


def _protected_subset() -> tuple[list[dict], list[str]]:
    manifest = SPACE / "historical/judged-root/PROTECTED_MANIFEST.sha256"
    rows: list[dict] = []
    missing: list[str] = []
    for line in manifest.read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        expected, raw_path = line.split(maxsplit=1)
        relative = raw_path.removeprefix("./")
        candidates = (SPACE / relative, SPACE / "historical/judged-root" / relative)
        match = next(
            (path for path in candidates if path.is_file() and _sha256(path) == expected),
            None,
        )
        rows.append(
            {
                "original_path": relative,
                "sha256": expected,
                "candidate_path": (
                    str(match.relative_to(SPACE)) if match is not None else None
                ),
            }
        )
        if match is None:
            missing.append(relative)
    return rows, missing


def _manifest_audit() -> dict:
    allowlist_path = SPACE / "UPLOAD_ALLOWLIST.txt"
    sha_path = SPACE / "SHA256SUMS.txt"
    allowlist = [
        line for line in allowlist_path.read_text().splitlines() if line and not line.startswith("#")
    ]
    hashes: dict[str, str] = {}
    for line in sha_path.read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        digest, relative = line.split(maxsplit=1)
        hashes[relative] = digest
    missing = [path for path in allowlist if not (SPACE / path).is_file()]
    unhashed = [path for path in allowlist if path != "SHA256SUMS.txt" and path not in hashes]
    mismatched = [
        path
        for path, digest in hashes.items()
        if not (SPACE / path).is_file() or _sha256(SPACE / path) != digest
    ]
    unexpected_hashes = [path for path in hashes if path not in allowlist]
    return {
        "allowlisted_files": len(allowlist),
        "hashed_files": len(hashes),
        "missing": missing,
        "unhashed": unhashed,
        "mismatched": mismatched,
        "unexpected_hashes": unexpected_hashes,
        "passed": not (missing or unhashed or mismatched or unexpected_hashes),
    }


def run_release_audit() -> dict:
    opened, broken_links = _traverse()
    required_pages = set(CURRENT_PAGES + RELEASE_PAGES)
    unreachable = sorted(required_pages - set(opened))
    marker_failures: dict[str, list[str]] = {}
    for relative in CURRENT_PAGES:
        text = (SPACE / relative).read_text().lower()
        missing = [marker for marker in REQUIRED_MARKERS if marker not in text]
        if missing:
            marker_failures[relative] = missing

    subset_rows, subset_missing = _protected_subset()
    secret_hits: list[dict] = []
    for relative in opened:
        path = SPACE / relative
        try:
            content = path.read_text()
        except UnicodeDecodeError:
            continue
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(content):
                secret_hits.append({"path": relative, "pattern": label})

    manifest = _manifest_audit()
    matrix_text = (SPACE / RELEASE_PAGES[0]).read_text()
    matrix_rows = sum(
        1
        for line in matrix_text.splitlines()
        if re.match(r"^\|\s*[1-6]\s*\|", line)
    )
    passed = not (
        broken_links
        or unreachable
        or marker_failures
        or subset_missing
        or secret_hits
        or matrix_rows != 6
        or not manifest["passed"]
    )
    return {
        "passed": passed,
        "entrypoints": list(ENTRYPOINTS),
        "opened_files": opened,
        "broken_links": broken_links,
        "unreachable_required_pages": unreachable,
        "marker_failures": marker_failures,
        "visibility_matrix_rows": matrix_rows,
        "protected_revision": "2d5f672ab576722614a3c86d48550e74fee2aca4",
        "protected_files_checked": len(subset_rows),
        "protected_subset_missing": subset_missing,
        "protected_subset_map": subset_rows,
        "secret_pattern_hits": secret_hits,
        "upload_manifest": manifest,
    }
