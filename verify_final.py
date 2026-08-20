#!/usr/bin/env python3
"""Verify the published documentation, evidence, and provenance contract."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED_STATUS = "ALL_C1_C6_VERIFIED_SCOPED_C1_MEDIUM_HISTORICAL_SCORE_9_OF_12_NO_CURRENT_SCORE"
EXPECTED_BRANCHES = {
    "audit/algorithm7-composition",
    "audit/claims3-5-independent",
    "audit/lemma33-haar-proof",
    "audit/table2-rounding-tolerance",
    "audit/theorem31-finite-calibration",
    "historical/judged-baseline",
    "main",
    "release/claim1-visibility",
    "release/claim2-visibility",
    "release/claim6-visibility",
    "release/claims3-5-visibility",
    "release/evaluator-red-team",
    "release/publication-metadata",
    "release/standalone-space-root",
}
EXPECTED_COMMITS = 35
CANONICAL_IDENTITY = "MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>"


def load(path: str):
    return json.loads((ROOT / path).read_text())


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"verification failed: {message}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def published_branches() -> set[str]:
    remote = {
        name.removeprefix("origin/")
        for name in git(
            "for-each-ref", "refs/remotes/origin", "--format=%(refname:short)"
        ).splitlines()
        if name.startswith("origin/") and name != "origin/HEAD"
    }
    if remote:
        return remote
    return set(git("for-each-ref", "refs/heads", "--format=%(refname:short)").splitlines())


def main() -> None:
    claims = load("claims.json")
    verdicts = load("reproduction_verdicts.json")
    manifest = load("EVIDENCE_MANIFEST.json")
    state = load("AUTONOMOUS_STATE.json")
    final = load(".openresearch/artifacts/release/final_run_output.json")
    red = load(".openresearch/artifacts/release/red_team_output.json")
    raw = [load(f".openresearch/artifacts/claim{n}/raw_output.json") for n in range(1, 7)]
    README = (ROOT / "README.md").read_text()
    CFF = (ROOT / "CITATION.cff").read_text()

    expected_statuses = {
        "C1": "VERIFIED_SCOPED_MEDIUM",
        "C2": "VERIFIED_SCOPED_HIGH",
        "C3": "VERIFIED_SCOPED_HIGH",
        "C4": "VERIFIED_SCOPED_HIGH",
        "C5": "VERIFIED_SCOPED_HIGH",
        "C6": "VERIFIED_SCOPED_HIGH",
    }
    require(claims["overall_status"] == EXPECTED_STATUS, "claims overall status")
    require(state["overall_status"] == EXPECTED_STATUS, "state overall status")
    require(verdicts["claim_statuses"] == expected_statuses, "verdict statuses")
    require({claim["id"]: claim["status"] for claim in claims["claims"]} == expected_statuses, "claim statuses")
    require(all((ROOT / path).exists() for path in manifest["required_paths"]), "manifest paths")
    for artifact in manifest["artifacts"]:
        require(sha256(ROOT / artifact["path"]) == artifact["sha256"], f"artifact digest {artifact['path']}")
    require(claims["paper"]["arxiv"] == manifest["source"]["arxiv"] == "2606.08681", "paper source")
    require("https://arxiv.org/abs/2606.08681" in CFF, "citation source")
    require(EXPECTED_STATUS in README, "README status")
    require(verdicts["historical_external_result"]["score"] == "9/12", "historical score")
    require(verdicts["historical_external_result"]["current_score_claim"] is False, "current score claim")
    require(verdicts["publication"]["publication_allowed"] is False, "publication state")
    require(verdicts["publication"]["author_endorsement_claimed"] is False, "author endorsement state")
    require(final["all_passed"] is True, "cumulative release result")
    require(red["passed"] is True, "red-team result")
    require(red["broken_links"] == [] and red["protected_files_checked"] == 14, "red-team visibility")
    require(red["upload_manifest"]["passed"] is True, "upload manifest")
    require(all(item["status"] == "PASS" for item in final["claims"]), "final claim statuses")

    claim1 = raw[0]
    require(claim1["all_passed"] is True, "Claim 1 raw result")
    require(any(item["id"] == "C0-PROOF" and item["status"] == "PASS" for item in claim1["claims"]), "Claim 1 proof certificate")
    require(any(item["id"] == "C0-FINITE-T" and item["status"] == "PASS" for item in claim1["claims"]), "Claim 1 finite calibration")
    claim2 = raw[1]
    require(claim2["status"] == "VERIFIED" and claim2["proof_dag_passed"] is True and claim2["negative_controls_rejected"] == 3, "Claim 2 certificate")
    claim3 = raw[2]["claim"]
    require(raw[2]["all_passed"] is True and max(row["absolute_normalization_error"] for row in claim3["evidence"]["normalization_rows"]) <= 4e-15, "Claim 3 normalization")
    claim4 = raw[3]["claim"]
    require(raw[3]["all_passed"] is True and min(row["mean_reduction"] for row in claim4["evidence"]["rows"]) > 0.09, "Claim 4 reductions")
    claim5 = raw[4]["claim"]
    require(raw[4]["all_passed"] is True and len(claim5["evidence"]["rows"]) == 7, "Claim 5 thresholds")
    require(all(row["tangent_dominance"] and row["convex_tail"] for row in claim5["evidence"]["rows"]), "Claim 5 conditions")
    claim6 = raw[5]["claim"]
    require(raw[5]["all_passed"] is True and len(claim6["evidence"]["figure3"]) == 5, "Claim 6 Figure 3")
    require(max(row["mse_reduction"] for row in claim6["evidence"]["figure3"]) > 0.94, "Claim 6 composition gain")
    require(len(claim6["evidence"]["broad_sgg_sweep"]) == 72, "Claim 6 broad sweep")

    branches = published_branches()
    require(branches == EXPECTED_BRANCHES, "published branches")
    require(not any(branch.startswith("orx/") for branch in branches), "legacy orx branch")
    require(int(git("rev-list", "--all", "--count")) == EXPECTED_COMMITS, "reachable commit count")
    identities = git("log", "--all", "--format=%an <%ae>\n%cn <%ce>").splitlines()
    require(identities and all(identity == CANONICAL_IDENTITY for identity in identities), "canonical commit identity")

    print(
        "FINAL_AUDIT=VERIFIED "
        f"branches={len(branches)} commits={EXPECTED_COMMITS} "
        "claims=C1_medium_scoped,C2:C6_high_scoped historical_score=9/12 "
        "current_score_claim=false publication_allowed=false"
    )


if __name__ == "__main__":
    main()
