"""Build the exact text-only Hugging Face upload allowlist and hashes."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPACE = ROOT / "space"
ALLOWLIST = SPACE / "UPLOAD_ALLOWLIST.txt"
SHA256SUMS = SPACE / "SHA256SUMS.txt"
GENERATED = {ALLOWLIST.name, SHA256SUMS.name}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_text(path: Path) -> bool:
    if "__pycache__" in path.parts or path.suffix == ".pyc":
        return False
    try:
        path.read_text()
    except UnicodeDecodeError:
        return False
    return True


def main() -> None:
    relative = sorted(
        str(path.relative_to(SPACE))
        for path in SPACE.rglob("*")
        if path.is_file() and path.name not in GENERATED and is_text(path)
    )
    relative.extend(sorted(GENERATED))
    relative = sorted(relative)
    ALLOWLIST.write_text("\n".join(relative) + "\n")
    hashes = [
        f"{sha256(SPACE / path)}  {path}"
        for path in relative
        if path != SHA256SUMS.name
    ]
    SHA256SUMS.write_text(
        "# Every allowlisted text file except this self-referential manifest.\n"
        + "\n".join(hashes)
        + "\n"
    )
    print(f"release manifest: {len(relative)} allowlisted text files, {len(hashes)} hashes")


if __name__ == "__main__":
    main()
