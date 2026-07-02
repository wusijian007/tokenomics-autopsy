"""
Scored universe: the union of every case scored on the 12-row spiral scorecard,
for empirical-weight fitting and reliability work (ROADMAP v6, E1).

Sources, single-sourced by import so scores never drift:
  - 18 in-sample calibration cases   (data/scorecard_calibration.py)
  - 15 leakage-audited holdout cases  (validation/holdout_backtest.py)
  - 20 NEW documented cases added here (below), with per-row justifications

Total ~= 53. Outcome is normalized to a binary survival label for fitting:
  failed = 1  if the design collapsed OR structurally bled (did not survive intact)
  failed = 0  if it survived a documented stress event with the mechanism intact

HONESTY: most of these are scored by one author from public post-mortems; this
is an expert-labeled, largely in-sample dataset, not an adjudicated benchmark.
Scores are order-of-magnitude and community-contributable (see CONTRIBUTING).
Its purpose is transparency -- to let a data-driven fit cross-check the hand
weights (3/2/1), not to replace the frozen v2 instrument.

Outputs:
  - scored_universe.csv

Run:  python scored_universe.py
"""
import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))                                  # data/
sys.path.insert(0, str(HERE.parent / "validation"))            # validation/

from scorecard_calibration import CASES as CAL_CASES           # noqa: E402
from holdout_backtest import CASES as HOLD_CASES               # noqa: E402

ROWS = ["S1_reflexive_collateral", "S2_subsidized_demand", "S3_uncapped_faucet",
        "S4_inflation_premium", "S5_fcfs_redemption", "S6_algo_stable",
        "S7_float_fdv", "S8_velocity_leak", "S9_narrative_only",
        "S10_contagion", "S11_mercenary_tvl", "S12_leverage_loops"]

# NEW cases: name, year, failed(1/0), [S1..S12], justification
# Scored consistently with analogous cases already in the calibration/holdout.
NEW_CASES = [
    # --- collapses / bleeds (failed = 1) ---
    ("Voyager VGX", 2022, 1, [1, 1, 0, 0, 2, 0, 0, 1, 1, 2, 0, 0],
     "CeFi bank run; dragged down by the 3AC default (contagion)"),
    ("Anchor ANC", 2022, 1, [0, 2, 0, 0, 1, 0, 1, 1, 1, 2, 1, 1],
     "the 19.5% subsidy engine of UST demand; died with Terra"),
    ("Klima DAO KLIMA", 2021, 1, [1, 2, 1, 2, 1, 0, 0, 1, 1, 0, 0, 1],
     "(3,3) carbon fork; scored like OHM, unravelled to backing then near-zero"),
    ("DeFi Kingdoms JEWEL", 2021, 1, [0, 2, 2, 1, 0, 0, 1, 2, 1, 0, 1, 0],
     "GameFi inflation; scored like Axie SLP, emission-rented liquidity"),
    ("SafeMoon SFM", 2021, 1, [0, 0, 0, 0, 0, 0, 1, 2, 2, 0, 0, 0],
     "reflection+high-tax narrative token; team charged with misappropriation"),
    ("HEX", 2019, 1, [0, 2, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0],
     "stake-for-high-APY, widely called Ponzi-like; no external revenue"),
    ("Gala Games GALA", 2021, 1, [0, 1, 2, 0, 0, 0, 1, 2, 1, 0, 0, 0],
     "GameFi platform inflation + a co-founder dispute"),
    ("Mirror Protocol MIR", 2022, 1, [1, 1, 0, 0, 1, 0, 1, 1, 1, 2, 0, 0],
     "Terra-ecosystem synthetics; went to zero via contagion"),
    ("Waves", 2022, 1, [2, 1, 0, 0, 1, 2, 0, 1, 1, 2, 0, 1],
     "the L1 reflexively entangled with USDN (Vires leverage); repeated de-pegs"),
    ("Bancor BNT", 2022, 1, [1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0],
     "IL-protection suspension broke trust; long bleed"),
    ("The Sandbox SAND", 2021, 1, [0, 0, 0, 0, 0, 0, 2, 1, 1, 0, 1, 0],
     "metaverse high-FDV unlock bleed; -97% as the narrative faded"),
    ("Decentraland MANA", 2021, 1, [0, 0, 0, 0, 0, 0, 2, 1, 1, 0, 0, 0],
     "metaverse unlock bleed; chronically thin active-user demand"),
    ("ApeCoin APE", 2022, 1, [0, 0, 0, 0, 0, 0, 2, 1, 1, 0, 1, 0],
     "airdrop + unlock overhang; continuous bleed after the narrative faded"),
    # --- stress survivors (failed = 0) ---
    ("Synthetix SNX", 2022, 0, [1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
     "SNX-collateralized synths (mild reflexivity) but survived multiple bears; real fees"),
    ("Compound COMP", 2022, 0, [0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
     "real lending fees, timelocked governance; survived 2022 intact"),
    ("Convex CVX", 2022, 0, [0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0],
     "ve-aggregator on Curve; bribe-driven but real-fee anchored, survived"),
    ("Solana SOL", 2022, 0, [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
     "near-death via FTX/Alameda holdings; recovered on a real-usage anchor"),
    ("Bitcoin BTC", 2022, 0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     "no mechanism forces selling; the base-case no-engine asset (all zeros)"),
    ("Lido LDO", 2022, 0, [0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1],
     "governance token over the largest LST; survived the June-2022 stETH stress"),
    ("Rocket Pool RPL", 2023, 0, [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
     "RPL bonds node operators (mild self-reference) but capped; survived"),
]


def failed_label(outcome):
    """Normalize the three source schemas to failed=1 / survived=0."""
    return 0 if outcome in ("survived", "survived_stress") else 1


def unified():
    """Return list of (name, source, failed01, [S1..S12], note)."""
    rows = []
    for name, yr, outcome, sc, note in CAL_CASES:
        rows.append((name, "calibration", failed_label(outcome), list(sc), note))
    for name, asof, outcome, anchor, sc, note in HOLD_CASES:
        rows.append((name, "holdout", failed_label(outcome), list(sc), note))
    for name, yr, failed, sc, note in NEW_CASES:
        rows.append((name, "new", failed, list(sc), note))
    return rows


def write_csv(path):
    rows = unified()
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["name", "source", "failed"] + ROWS + ["note"])
        for name, src, failed, sc, note in rows:
            w.writerow([name, src, failed] + sc + [note])
    print(f"  [data]  {path.name}  ({len(rows)} cases)")
    return rows


def main():
    print("Scored universe: unifying calibration + holdout + new cases")
    rows = write_csv(HERE / "scored_universe.csv")
    n = len(rows)
    failed = sum(r[2] for r in rows)
    by_src = {}
    for _, src, *_ in rows:
        by_src[src] = by_src.get(src, 0) + 1
    print(f"  total {n} cases: {failed} failed / {n - failed} survived")
    print(f"  by source: " + ", ".join(f"{k}={v}" for k, v in by_src.items()))


if __name__ == "__main__":
    main()
