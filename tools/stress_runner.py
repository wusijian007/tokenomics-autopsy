"""
Stress-runner: a design spec in -> a scored verdict out (ROADMAP v6, D3).

Reads a declarative design spec (design.example.yaml), scores the 12 spiral
scorecard rows + the S13/S14/S15 security panel from its fields using the
measurement rules in scorecard.md / economic-security.md, runs the matching
parameterized simulations, and emits the design-playbook step-9 verdict:
score, engine/structure flags, band, security panel, the archetype's one number,
and prioritized prescriptions.

Dependency-light: uses PyYAML if present, else a built-in parser for the flat
key: value spec subset; JSON specs also work. Calls sim4/sim6 functions for the
bank-run and governance numbers.

Run:  python stress_runner.py [design.example.yaml]
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "simulations"))

WEIGHTS = {"S1": 3, "S2": 3, "S3": 2, "S4": 2, "S5": 3, "S6": 3,
           "S7": 2, "S8": 1, "S9": 3, "S10": 1, "S11": 2, "S12": 2}
ENGINE = {"S1", "S2", "S5", "S6", "S9"}
STRUCTURE = {"S3", "S4", "S7", "S11", "S12"}
ARCHETYPE_ONE_NUMBER = {
    "dex": ("fees / emissions", "value_capture + incentives.runway_months"),
    "lending": ("manipulation cost / borrowable value", "oracle.manip_cost_over_borrowable"),
    "perp": ("insurance coverage / worst-case shortfall", "redemption.liquidity_coverage"),
    "stablecoin": ("exogenous reserve / liabilities (non-reflexive)", "collateral.native_share"),
    "l1": ("cost to attack consensus / value secured", "governance + supply"),
    "gamefi": ("net-external inflow / extraction", "emissions.sink_needs_new_users"),
    "depin": ("service revenue / emissions value", "depin.revenue_over_emissions"),
    "points": ("organic (fee-paying) share of TVL", "incentives.organic_tvl_share"),
}


# --------------------------- spec loading ---------------------------

def load_spec(path):
    text = Path(path).read_text(encoding="utf-8")
    if path.suffix == ".json":
        return json.loads(text)
    try:
        import yaml  # optional
        return yaml.safe_load(text)
    except ImportError:
        return _parse_flat_yaml(text)


def _coerce(v):
    v = v.strip()
    if v.lower() in ("true", "false"):
        return v.lower() == "true"
    try:
        return int(v)
    except ValueError:
        pass
    try:
        return float(v)
    except ValueError:
        return v


def _parse_flat_yaml(text):
    """Restricted parser: top-level 'section:' headers + 2-space 'key: value'
    pairs, plus top-level scalars. Comments (#) and blank lines ignored."""
    root, section = {}, None
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if not line.startswith(" "):
            key, _, val = line.partition(":")
            key = key.strip()
            if val.strip() == "":
                section = key
                root[key] = {}
            else:
                root[key] = _coerce(val)
                section = None
        else:
            key, _, val = line.strip().partition(":")
            if section is not None:
                root[section][key.strip()] = _coerce(val)
    return root


def g(spec, path, default=None):
    """Nested get: g(spec, 'redemption.liquidity_coverage')."""
    cur = spec
    for part in path.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return default
    return cur


# --------------------------- scoring ---------------------------

def score_rows(s):
    """Return {row: (score, reason)} for the 12 spiral rows."""
    r = {}

    native = g(s, "collateral.native_share", 0.0)
    r["S1"] = ((2, f"reserves {native:.0%} native/affiliated") if native >= 0.30 else
               (1, f"{native:.0%} native") if native > 0 else
               (0, "exogenous collateral"))

    yld = g(s, "demand.yield_source", "none")
    runway = g(s, "incentives.runway_months", 999)
    if yld == "real_fees":
        r["S2"] = (0, "yield from real fees")
    elif runway >= 12:
        r["S2"] = (1, f"subsidy but runway {runway}mo")
    else:
        r["S2"] = (2, f"subsidy, runway {runway}mo < 12")

    capped = g(s, "emissions.capped", True)
    sf = g(s, "emissions.sink_faucet_ratio", 1.0)
    needs_new = g(s, "emissions.sink_needs_new_users", False)
    if capped and sf >= 1.0:
        r["S3"] = (0, f"capped, sink/faucet {sf}")
    elif not capped and needs_new:
        r["S3"] = (2, "uncapped and sink needs new users")
    else:
        r["S3"] = (1, f"cap={capped}, sink/faucet {sf}")

    prem = g(s, "premium.price_over_backing", 1.0)
    infl = g(s, "premium.yield_from_inflation", False)
    r["S4"] = ((2, f"premium {prem}x, inflation-funded") if prem > 3 and infl else
               (1, f"premium {prem}x") if prem > 1.5 else (0, "no premium mechanics"))

    cov = g(s, "redemption.liquidity_coverage", 1.0)
    fcfs = g(s, "redemption.fcfs", False)
    if cov >= 1.0 or not fcfs:
        r["S5"] = (0, f"coverage {cov}, fcfs={fcfs}")
    elif cov >= 0.5:
        r["S5"] = (1, f"coverage {cov} with fcfs")
    else:
        r["S5"] = (2, f"coverage {cov} < 0.5 with fcfs")

    algo = g(s, "collateral.algorithmic", False)
    r["S6"] = (2, "algorithmic + own token") if algo and native > 0 else \
              (1, "partial-algo") if algo else (0, "not algorithmic")

    float_pct = g(s, "supply.float_pct", 1.0)
    unlock = g(s, "supply.year1_unlock_pct_of_float", 0.0)
    fdvr = g(s, "supply.fdv_to_revenue", 0)
    if float_pct < 0.10 or unlock > 0.50 or fdvr > 100:
        r["S7"] = (2, f"float {float_pct:.0%}, y1 unlock {unlock:.0%}, FDV/rev {fdvr}")
    elif float_pct < 0.20 or unlock > 0.25:
        r["S7"] = (1, f"float {float_pct:.0%}, y1 unlock {unlock:.0%}")
    else:
        r["S7"] = (0, f"float {float_pct:.0%}, y1 unlock {unlock:.0%}")

    vc = g(s, "value_capture", "none")
    r["S8"] = (0, f"{vc} capture") if vc in ("fee_share", "burn", "velock") else \
              (2, "no value capture")

    rev = g(s, "holders.revenue_positive", False)
    top10 = g(s, "holders.top10_holder_share", 0.0)
    locked = g(s, "holders.team_locked", True)
    backdoor = g(s, "holders.contract_backdoors", False)
    if not rev and (top10 > 0.5 or not locked or backdoor):
        r["S9"] = (2, "zero revenue + concentrated/unlocked/backdoored")
    elif not rev:
        r["S9"] = (1, "narrative-led but locked + clean contract")
    else:
        r["S9"] = (0, "real cash-flow demand")

    cross = g(s, "contagion.cross_collateralized", False)
    r["S10"] = (2, "cross-collateralized / key-person leverage") if cross else \
               (0, "isolated")

    organic = g(s, "incentives.organic_tvl_share", 1.0)
    r["S11"] = ((0, f"organic {organic:.0%}") if organic > 0.70 else
                (1, f"organic {organic:.0%}") if organic >= 0.30 else
                (2, f"organic {organic:.0%} < 30%"))

    unwind = g(s, "leverage.loop_unwind_over_depth", 0.0)
    r["S12"] = ((2, f"unwind {unwind}x depth") if unwind > 1.0 else
                (1, f"unwind {unwind}x depth") if unwind > 0.3 else
                (0, f"unwind {unwind}x depth"))
    return r


def score_security(s):
    """Return {row: (score, reason)} for S13/S14/S15 (separate panel)."""
    r = {}
    lockable = g(s, "governance.votes_lockable", True)
    timelock = g(s, "governance.timelock_days", 0)
    borrowable = g(s, "governance.quorum_borrowable_below_value", False)
    if (not lockable and timelock < 1) or borrowable:
        r["S13"] = (2, f"quorum capturable (lockable={lockable}, timelock={timelock}d)")
    elif timelock < 2 or not lockable:
        r["S13"] = (1, f"partial (timelock {timelock}d, lockable={lockable})")
    else:
        r["S13"] = (0, f"locked votes + {timelock}d timelock")

    lev = g(s, "oracle.token_used_as_leverage_collateral", False)
    manip = g(s, "oracle.manip_cost_over_borrowable", 99)
    if not lev:
        r["S14"] = (0, "not used as leverage collateral")
    elif manip >= 1.5:
        r["S14"] = (0, f"manip cost {manip}x borrowable")
    elif manip >= 1.0:
        r["S14"] = (1, f"manip cost {manip}x borrowable (thin margin)")
    else:
        r["S14"] = (2, f"manip cost {manip}x < borrowable value")

    if not g(s, "depin.is_depin", False):
        r["S15"] = (0, "not a DePIN/work network")
    else:
        ratio = g(s, "depin.revenue_over_emissions", 0.0)
        r["S15"] = ((0, f"revenue/emissions {ratio}") if ratio >= 0.5 else
                    (1, f"revenue/emissions {ratio}") if ratio >= 0.1 else
                    (2, f"revenue/emissions {ratio} << 0.1"))
    return r


# --------------------------- sims ---------------------------

def run_sims(s):
    out = []
    cov = g(s, "redemption.liquidity_coverage", 1.0)
    fcfs = g(s, "redemption.fcfs", False)
    if fcfs:
        try:
            from sim4_bank_run_diamond_dybvig import run_fraction
            seq = run_fraction(min(cov, 1.0), 0.05, prorata=False)
            pro = run_fraction(min(cov, 1.0), 0.05, prorata=True)
            out.append(f"sim4 bank run @ coverage {cov}: sequential run={seq:.0%}, "
                       f"pro-rata run={pro:.0%}")
        except Exception as e:
            out.append(f"sim4 unavailable: {e}")
    tl = g(s, "governance.timelock_days", 0)
    tr = g(s, "governance.treasury_over_float_mcap", 0.0)
    if tr > 0:
        try:
            from sim6_governance_capture import attacker_profit
            qcost = 0.30 if g(s, "governance.votes_lockable", True) else 0.02
            p_now = attacker_profit(tr, qcost, tl)
            p_notl = attacker_profit(tr, qcost, 0.0)
            out.append(f"sim6 governance @ treasury {tr}x float, timelock {tl}d: "
                       f"attacker profit {p_now:+.2f} (vs {p_notl:+.2f} with no timelock)")
        except Exception as e:
            out.append(f"sim6 unavailable: {e}")
    return out


# --------------------------- verdict ---------------------------

def verdict(spec):
    rows = score_rows(spec)
    sec = score_security(spec)
    total = sum(sc * WEIGHTS[k] for k, (sc, _) in rows.items())
    eng = [k for k in ENGINE if rows[k][0] == 2]
    stru = [k for k in STRUCTURE if rows[k][0] == 2]
    sec_flags = [k for k in ("S13", "S14") if sec[k][0] == 2]

    band = ("0-7 low structural risk" if total <= 7 else
            "8-18 reflexive elements present" if total <= 18 else
            "19-33 high risk (>=1 engine)" if total <= 33 else
            ">=34 textbook death-spiral")

    lines = []
    lines.append(f"# Stress-runner verdict - {spec.get('name','(unnamed)')} "
                 f"[{spec.get('archetype','?')}]")
    lines.append("")
    lines.append(f"**Spiral score {total}/54** - {band}")
    lines.append(f"- engine flags (2): {', '.join(eng) or 'none'}")
    lines.append(f"- structure flags (2): {', '.join(stru) or 'none'}")
    lines.append(f"- security panel red lines: {', '.join(sec_flags) or 'none'}")
    one = ARCHETYPE_ONE_NUMBER.get(spec.get("archetype", ""), None)
    if one:
        lines.append(f"- archetype one-number to watch: **{one[0]}**")
    lines.append("")

    if eng or sec_flags:
        decision = "REDESIGN - engine/attack red line present; fix before launch."
    elif stru:
        decision = ("STRUCTURE RISK - no engine, but bleed/deleveraging risk; "
                    "verdict hinges on the zero-price anchor test.")
    else:
        decision = "PASS (structural) - no engine, no structure red line; market risk still applies."
    zpt = g(spec, "demand.zero_price_test", "unknown")
    lines.append(f"**Decision:** {decision}  (zero-price test: {zpt})")
    lines.append("")

    lines.append("## Spiral rows")
    for k in [f"S{i}" for i in range(1, 13)]:
        sc, reason = rows[k]
        mark = "  <- ENGINE RED LINE" if (sc == 2 and k in ENGINE) else "  <- flag" if sc == 2 else ""
        lines.append(f"- {k} (w{WEIGHTS[k]}): {sc} - {reason}{mark}")
    lines.append("")
    lines.append("## Security panel (separate axis)")
    for k in ("S13", "S14", "S15"):
        sc, reason = sec[k]
        mark = "  <- RED LINE" if sc == 2 else ""
        lines.append(f"- {k}: {sc} - {reason}{mark}")
    lines.append("")

    sims = run_sims(spec)
    if sims:
        lines.append("## Simulations")
        for x in sims:
            lines.append(f"- {x}")
        lines.append("")

    lines.append("## Prescriptions (prioritized)")
    pri = []
    for k in eng:
        pri.append(f"[engine] fix {k} - see anti-patterns.md antidote")
    for k in sec_flags:
        pri.append(f"[attack] fix {k} - see economic-security.md (timelock/cap/delist)")
    for k in stru:
        pri.append(f"[structure] fix {k} - supply schedule / caps / vesting")
    if not pri:
        pri.append("no red lines; monitor the archetype one-number and the step-8 dashboard")
    for i, p in enumerate(pri, 1):
        lines.append(f"{i}. {p}")
    lines.append("")
    lines.append("_Not investment advice. Scores are derived from the declared spec; "
                 "verify against live data (audit-protocol.md). Security panel is a "
                 "separate axis, not summed into /54._")
    return "\n".join(lines)


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "design.example.yaml"
    spec = load_spec(path)
    report = verdict(spec)
    print(report)
    out = HERE / (path.stem + ".verdict.md")
    out.write_text(report, encoding="utf-8")
    print(f"\n[written] {out.name}")


if __name__ == "__main__":
    main()
