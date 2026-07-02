"""
Inter-rater reliability: weighted Cohen's kappa between two score sheets
(ROADMAP v6, E3 - "two independent scorers reach kappa >= 0.7 on a blind set").

This ships the MACHINERY (weighted kappa per row + overall, agreement matrix)
and a DEMONSTRATION on two synthetic rater sheets. It does NOT manufacture a
reliability result: a real kappa study needs two *independent* humans scoring a
*blind* case set. Use `--sheets a.json b.json` to score real rater sheets.

Score sheet JSON: {"rater": "A", "scores": {"CaseName": [s1..s12], ...}}
(each s in {0,1,2}).

Run:  python kappa_reliability.py                    # demo on synthetic sheets
      python kappa_reliability.py a.json b.json      # real two-rater sheets
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def weighted_kappa(a, b, k=3):
    """Linear-weighted Cohen's kappa for ordinal ratings in {0..k-1}.
    a, b: equal-length lists of integer ratings."""
    n = len(a)
    if n == 0:
        return float("nan")
    # observed and expected agreement with linear weights
    obs = [[0.0] * k for _ in range(k)]
    for x, y in zip(a, b):
        obs[x][y] += 1.0 / n
    ra = [sum(obs[i]) for i in range(k)]           # row marginals (rater A)
    cb = [sum(obs[i][j] for i in range(k)) for j in range(k)]  # col marginals (B)

    def w(i, j):
        return 1.0 - abs(i - j) / (k - 1)          # linear weight

    po = sum(w(i, j) * obs[i][j] for i in range(k) for j in range(k))
    pe = sum(w(i, j) * ra[i] * cb[j] for i in range(k) for j in range(k))
    if pe == 1.0:
        return 1.0
    return (po - pe) / (1.0 - pe)


def flatten(sheet_a, sheet_b):
    """Align two sheets on shared cases; return per-row and pooled rating lists."""
    cases = [c for c in sheet_a["scores"] if c in sheet_b["scores"]]
    rows = 12
    per_row = [([], []) for _ in range(rows)]
    pooled_a, pooled_b = [], []
    for c in cases:
        va, vb = sheet_a["scores"][c], sheet_b["scores"][c]
        for i in range(rows):
            per_row[i][0].append(va[i])
            per_row[i][1].append(vb[i])
            pooled_a.append(va[i])
            pooled_b.append(vb[i])
    return cases, per_row, pooled_a, pooled_b


def interpret(k):
    if k != k:      # nan
        return "n/a"
    return ("excellent (>=0.8)" if k >= 0.8 else "good (>=0.7)" if k >= 0.7 else
            "moderate (>=0.6)" if k >= 0.6 else "fair (>=0.4)" if k >= 0.4 else "poor (<0.4)")


def report(sheet_a, sheet_b):
    cases, per_row, pa, pb = flatten(sheet_a, sheet_b)
    ROWS = [f"S{i}" for i in range(1, 13)]
    print(f"Inter-rater reliability: {sheet_a['rater']} vs {sheet_b['rater']} "
          f"on {len(cases)} shared cases")
    overall = weighted_kappa(pa, pb)
    print(f"  overall weighted kappa: {overall:.3f}  ({interpret(overall)})")
    exact = sum(1 for x, y in zip(pa, pb) if x == y) / len(pa)
    print(f"  exact-agreement rate  : {exact:.0%}  ({len(pa)} row-ratings)")
    print("  per-row kappa (rows where raters diverge need tighter procedures):")
    worst = []
    for i, row in enumerate(ROWS):
        ka = weighted_kappa(per_row[i][0], per_row[i][1])
        flag = "  <- tighten" if (ka == ka and ka < 0.6) else ""
        print(f"    {row}: {ka:.3f}{flag}")
        if ka == ka and ka < 0.6:
            worst.append(row)
    print(f"  target: overall kappa >= 0.7 for an instrument that works in "
          f"strangers' hands.")
    if overall < 0.7:
        print("  -> below target: sharpen the measurement procedures in scorecard.md")
        print(f"     for the divergent rows ({', '.join(worst) or 'see per-row'}).")
    return overall


DEMO_A = {"rater": "A (demo)", "scores": {
    "Terra": [2, 2, 0, 1, 2, 2, 0, 0, 1, 2, 1, 2],
    "OHM":   [1, 2, 1, 2, 1, 0, 0, 1, 1, 0, 0, 1],
    "DAI":   [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    "Axie":  [0, 2, 2, 0, 0, 0, 1, 2, 1, 0, 1, 0],
    "stETH": [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 2],
    "FTX":   [2, 0, 0, 0, 2, 0, 1, 0, 1, 2, 0, 1]}}
# Rater B: a second scorer who differs by <=1 on a few subjective rows.
DEMO_B = {"rater": "B (demo)", "scores": {
    "Terra": [2, 2, 0, 2, 2, 2, 0, 0, 2, 2, 1, 1],
    "OHM":   [1, 2, 2, 2, 1, 0, 0, 1, 1, 1, 0, 1],
    "DAI":   [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    "Axie":  [0, 2, 2, 0, 0, 0, 2, 2, 1, 0, 1, 0],
    "stETH": [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2],
    "FTX":   [1, 0, 0, 0, 2, 0, 1, 1, 1, 2, 0, 1]}}


def main():
    if len(sys.argv) >= 3:
        a = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        b = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    else:
        print("(no sheets given - running the built-in DEMONSTRATION on synthetic")
        print(" rater sheets; a real study needs two independent humans + a blind set)\n")
        a, b = DEMO_A, DEMO_B
    report(a, b)


if __name__ == "__main__":
    main()
