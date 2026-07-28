"""Independent finite-group analogue checker for the Haar proof.

This checker does not import the proof-certificate module. It exhaustively
evaluates exact rational hockey-stick divergences for a suite of discrete laws
under the four-element rotation group in R^2. It is corroboration of the
mixture argument, not the universal proof itself.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from itertools import combinations


Point = tuple[int, int]
Law = dict[Point, Fraction]
SHIFTS: tuple[Point, ...] = ((1, 0), (-1, 0), (0, 1), (0, -1))


def rotate(point: Point, quarter_turns: int) -> Point:
    x, y = point
    for _ in range(quarter_turns % 4):
        x, y = -y, x
    return x, y


def shifted(law: Law, shift: Point) -> Law:
    dx, dy = shift
    return {(x + dx, y + dy): probability for (x, y), probability in law.items()}


def hockey_stick(law_p: Law, law_q: Law, alpha: Fraction = Fraction(2)) -> Fraction:
    support = set(law_p) | set(law_q)
    return sum(
        max(law_p.get(point, Fraction(0)) - alpha * law_q.get(point, Fraction(0)), Fraction(0))
        for point in support
    )


def symmetrize(law: Law) -> Law:
    result: defaultdict[Point, Fraction] = defaultdict(Fraction)
    for turns in range(4):
        for point, probability in law.items():
            result[rotate(point, turns)] += probability / 4
    return dict(result)


def mse(law: Law) -> Fraction:
    return sum(Fraction(x * x + y * y) * probability for (x, y), probability in law.items())


def worst_delta(law: Law) -> Fraction:
    return max(hockey_stick(law, shifted(law, shift)) for shift in SHIFTS)


def _law_suite() -> list[Law]:
    points = [(-2, 0), (-1, 1), (0, 0), (1, 0), (0, 2), (2, -1)]
    laws: list[Law] = [{point: Fraction(1)} for point in points]
    for first, second in combinations(points, 2):
        laws.append({first: Fraction(1, 3), second: Fraction(2, 3)})
        laws.append({first: Fraction(1, 2), second: Fraction(1, 2)})
    for triple in combinations(points, 3):
        laws.append(
            {
                triple[0]: Fraction(1, 6),
                triple[1]: Fraction(1, 3),
                triple[2]: Fraction(1, 2),
            }
        )
    return laws


def run_independent_checker() -> dict:
    rows = []
    for index, law in enumerate(_law_suite()):
        symm = symmetrize(law)
        mse_equal = mse(law) == mse(symm)
        privacy_before = worst_delta(law)
        privacy_after = worst_delta(symm)
        rows.append(
            {
                "case": index,
                "mse_equal_exact": mse_equal,
                "privacy_before_exact": str(privacy_before),
                "privacy_after_exact": str(privacy_after),
                "privacy_not_worse_exact": privacy_after <= privacy_before,
            }
        )
    passed = all(row["mse_equal_exact"] and row["privacy_not_worse_exact"] for row in rows)
    return {
        "scope": (
            "Exact finite C4-group analogue at alpha=e^epsilon=2 over all "
            "one-, two-, and three-point laws in the declared suite"
        ),
        "case_count": len(rows),
        "rows": rows,
        "passed": passed,
        "limitation": "Independent corroboration only; universal O(T) result comes from the symbolic certificate.",
    }

