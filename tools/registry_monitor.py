"""
Registry monitor: checks the frozen prospective-registry projects against their
pre-registered falsifiable triggers (ROADMAP v6).

Reads a metrics SNAPSHOT (registry_metrics.example.json) and evaluates each
project's registered trigger conditions from validation/prospective-registry.md,
printing OK / WATCH / ALERT. An ALERT means a pre-registered condition fired and
the registry's Grading log should be updated at the review date.

HONEST SCOPE: the data layer is a stub. A live deployment wires the marked
fetch_* functions to DefiLlama (TVL/fees/revenue), CoinGecko (supply/price),
Dune (loop positions, funding), and unlock trackers. This tool does not fetch
live data itself - it evaluates whatever snapshot it is given, so the logic can
be tested and the alerts are reproducible.

Run:  python registry_monitor.py [registry_metrics.example.json]
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


# --- data layer (STUB): a live deployment replaces this with real API calls ---
def load_snapshot(path):
    """In production, build this dict from DefiLlama/CoinGecko/Dune/unlock feeds.
    Here we read a local snapshot so the trigger logic is testable + reproducible."""
    return json.loads(Path(path).read_text(encoding="utf-8"))


# --- pre-registered triggers (from validation/prospective-registry.md) ---
def check_usde(m):
    alerts = []
    # P-USDe trigger T: >=60 consecutive days negative funding while supply > $5B
    if m.get("consecutive_neg_funding_days", 0) >= 60 and m.get("supply_usd_bn", 0) > 5:
        alerts.append(("ALERT", "trigger T active (>=60d neg funding, supply>$5B) - "
                                "P-USDe-2 conditional predictions now in force"))
    elif m.get("consecutive_neg_funding_days", 0) >= 30:
        alerts.append(("WATCH", f"neg-funding streak {m['consecutive_neg_funding_days']}d "
                                "approaching the 60d trigger"))
    # P-USDe-1: no sustained secondary discount >2% with redemptions working
    if m.get("secondary_discount_pct", 0) > 2 and m.get("primary_redemptions_ok", True):
        alerts.append(("ALERT", "secondary discount >2% - tests P-USDe-1"))
    return alerts


def check_hype(m):
    alerts = []
    # P-HYPE-1 falsifier: a mint/dump recapitalization of a shortfall
    if m.get("hlp_shortfall_recap_via_mint", False):
        alerts.append(("ALERT", "HLP shortfall recapitalized via HYPE mint/dump - "
                                "falsifies P-HYPE-1 (would be an engine spiral)"))
    # P-HYPE-2 re-score trigger: realized 12mo unlocks > 50% of float
    u = m.get("realized_12mo_unlocks_pct_of_float", 0)
    if u > 50:
        alerts.append(("ALERT", f"12mo unlocks {u}% of float >50% - amend S7->2 (P-HYPE-2)"))
    elif u > 35:
        alerts.append(("WATCH", f"12mo unlocks {u}% of float approaching the 50% re-score line"))
    return alerts


def check_pump(m):
    if m.get("reflexive_mint_dump_loop", False):
        return [("ALERT", "reflexive mint/dump loop observed - falsifies P-PUMP-1")]
    if m.get("memecoin_volume_index", 1.0) < 0.3:
        return [("WATCH", "memecoin volumes collapsing - watch for business-risk decline "
                          "(should be proportional, not a spiral)")]
    return []


def check_usdd(m):
    # P-USDD-2 conditional: TRX drawdown >60% + redemption wave >30% -> discount >3%?
    if m.get("trx_drawdown_pct", 0) > 60 and m.get("redemption_wave_pct_supply", 0) > 30:
        if m.get("discount_pct", 0) > 3:
            return [("ALERT", "TRX crash + redemption wave + discount>3% - confirms S1/S5 scoring")]
        return [("ALERT", "TRX crash + redemption wave WITHOUT a >3% discount - "
                          "P-USDD-2 says revise our pessimistic S1/S5 down")]
    return []


def check_jup(m):
    if m.get("run_shaped_event", False):
        return [("ALERT", "run-shaped collapse - falsifies P-JUP-1 (expected bleed, not run)")]
    u = m.get("next_90d_unlocks_pct_of_float", 0)
    if u > 25:
        return [("WATCH", f"next-90d unlocks {u}% of float - bleed-shape pressure (consistent w/ S7)")]
    return []


CHECKS = {
    "Ethena USDe": check_usde,
    "Hyperliquid HYPE": check_hype,
    "pump.fun PUMP": check_pump,
    "USDD": check_usdd,
    "Jupiter JUP": check_jup,
}


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "registry_metrics.example.json"
    snap = load_snapshot(path)
    print(f"Registry monitor - snapshot as of {snap.get('as_of','?')}")
    print("(data layer is a stub; wire fetch_* to live feeds for production)\n")
    any_alert = False
    for project, check in CHECKS.items():
        m = snap.get(project, {})
        if not m:
            print(f"  {project}: (no metrics in snapshot)")
            continue
        results = check(m)
        if not results:
            print(f"  {project}: OK - no registered trigger fired")
        for level, msg in results:
            if level == "ALERT":
                any_alert = True
            print(f"  {project}: [{level}] {msg}")
    print()
    if any_alert:
        print("  >> ALERT(s) fired: update the registry Grading log at the next review date")
        print("     (2027-07-02 / 2028-07-02) with evidence; grade the affected predictions.")
    else:
        print("  no ALERTs; all monitored triggers within pre-registered bounds.")


if __name__ == "__main__":
    main()
