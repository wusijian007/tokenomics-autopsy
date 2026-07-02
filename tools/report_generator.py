"""
Report generator: a structured audit JSON -> the full markdown report
(ROADMAP v6). Emits the audit-protocol.md report template, pre-filled from a
scored audit, including the evidence table, security panel, thresholds, the
risk x valuation quadrant, prescriptions, and the blind-spot register.

This is the human-audit companion to stress_runner.py (which scores a *design
spec*); report_generator formats a *completed audit* into a shareable report.

Input: a JSON file (see audit.example.json). Output: <name>-audit.md.

Run:  python report_generator.py [audit.example.json]
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

WEIGHTS = {"S1": 3, "S2": 3, "S3": 2, "S4": 2, "S5": 3, "S6": 3,
           "S7": 2, "S8": 1, "S9": 3, "S10": 1, "S11": 2, "S12": 2}
ENGINE = {"S1", "S2", "S5", "S6", "S9"}
STRUCTURE = {"S3", "S4", "S7", "S11", "S12"}
ROW_NAME = {
    "S1": "Reflexive collateral", "S2": "Subsidized demand", "S3": "Uncapped faucet",
    "S4": "(3,3) inflation premium", "S5": "FCFS redemption", "S6": "Algo-stable",
    "S7": "Float/FDV", "S8": "Velocity leak", "S9": "Narrative-only",
    "S10": "Contagion", "S11": "Mercenary TVL", "S12": "Recursive loops",
    "S13": "Governance capture", "S14": "Oracle/leverage", "S15": "Supply subsidy"}
BLIND_SPOTS = [
    "Smart-contract exploits (code bugs) - see contract audits / formal verification",
    "Regulatory / legal kill - counsel, jurisdiction analysis",
    "Key-person / operational (founder fraud, lost keys)",
    "Chain-level failure of the underlying L1/L2",
    "Pure market beta (whole-market drawdown, no mechanism fault)",
    "Off-chain fraud beyond S9's tells (fake reserves, cooked books)",
    "Narrative / timing - the instrument gives structure, never timing",
]


def band(total):
    return ("0-7 low structural risk" if total <= 7 else
            "8-18 reflexive elements present" if total <= 18 else
            "19-33 high risk (>=1 engine)" if total <= 33 else
            ">=34 textbook death-spiral")


def render(a):
    rows = a.get("scorecard", {})            # {S1: {score, reason, confidence, source}}
    sec = a.get("security_panel", {})        # {S13: {score, reason, ...}}
    total = sum(rows.get(k, {}).get("score", 0) * WEIGHTS[k] for k in WEIGHTS)
    eng = [k for k in ENGINE if rows.get(k, {}).get("score") == 2]
    stru = [k for k in STRUCTURE if rows.get(k, {}).get("score") == 2]
    sec_flags = [k for k in ("S13", "S14") if sec.get(k, {}).get("score") == 2]

    L = []
    L.append(f"# Tokenomics Audit - {a.get('project','(project)')} ({a.get('date','')})")
    L.append("")
    L.append("## Verdict")
    verdict = a.get("verdict", "")
    L.append(f"Spiral score **{total}/54** ({band(total)}); "
             f"engine flags: {', '.join(eng) or 'none'}; "
             f"structure flags: {', '.join(stru) or 'none'}; "
             f"security panel red lines: {', '.join(sec_flags) or 'none'}.")
    if verdict:
        L.append("")
        L.append(verdict)
    L.append("")

    L.append("## Mechanism map & game classification")
    L.append(a.get("mechanism", "_(describe the mechanism map; which of the 4 game models; expected failure shape)_"))
    L.append("")

    L.append("## Scorecard (spiral axis)")
    L.append("| Row | Skill | Score | Weighted | Confidence | Evidence |")
    L.append("|---|---|---|---|---|---|")
    for k in [f"S{i}" for i in range(1, 13)]:
        row = rows.get(k, {})
        sc = row.get("score", 0)
        L.append(f"| {k} | {ROW_NAME[k]} | {sc} | {sc*WEIGHTS[k]} | "
                 f"{row.get('confidence','-')} | {row.get('reason','-')} |")
    L.append(f"| | **Total** | | **{total}/54** | | |")
    L.append("")

    L.append("## Security panel (attack axis - not summed into /54)")
    L.append("| Row | Skill | Score | Evidence |")
    L.append("|---|---|---|---|")
    for k in ("S13", "S14", "S15"):
        row = sec.get(k, {})
        L.append(f"| {k} | {ROW_NAME[k]} | {row.get('score',0)} | {row.get('reason','-')} |")
    L.append("")

    thr = a.get("thresholds", [])
    if thr:
        L.append("## Critical thresholds & distance")
        L.append("| Trigger | Current | Threshold | Trend | ETA |")
        L.append("|---|---|---|---|---|")
        for t in thr:
            L.append(f"| {t.get('trigger','')} | {t.get('current','')} | "
                     f"{t.get('threshold','')} | {t.get('trend','')} | {t.get('eta','')} |")
        L.append("")

    if a.get("stress_test"):
        L.append("## Stress test")
        L.append(a["stress_test"])
        L.append("")

    if a.get("contagion"):
        L.append("## Control surfaces & contagion")
        L.append(a["contagion"])
        L.append("")

    val = a.get("valuation", {})
    if val:
        L.append("## Valuation context (not a price target)")
        L.append(f"Regime: **{val.get('regime','?')}**. Quadrant: "
                 f"**{val.get('quadrant','?')}**.")
        if val.get("notes"):
            L.append("")
            L.append(val["notes"])
        L.append("")

    L.append("## Prescriptions (prioritized)")
    presc = a.get("prescriptions")
    if presc:
        for i, p in enumerate(presc, 1):
            L.append(f"{i}. {p}")
    else:
        order = ([f"[engine] {k}" for k in eng] + [f"[attack] {k}" for k in sec_flags] +
                 [f"[structure] {k}" for k in stru]) or ["monitor; no red lines"]
        for i, p in enumerate(order, 1):
            L.append(f"{i}. fix {p} (cite the antidote)")
    L.append("")

    L.append("## Limitations & blind spots")
    L.append(a.get("limitations", "_(data gaps, estimated rows, what would change the verdict)_"))
    L.append("")
    L.append("The instrument is blind to these failure families - a clean score does not rule them out:")
    for b in BLIND_SPOTS:
        L.append(f"- {b}")
    L.append("")
    L.append("_Research / design reference, not investment advice._")
    return "\n".join(L)


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "audit.example.json"
    audit = json.loads(path.read_text(encoding="utf-8"))
    report = render(audit)
    out = HERE / (path.stem.replace(".", "_") + "-audit.md")
    out.write_text(report, encoding="utf-8")
    print(report)
    print(f"\n[written] {out.name}")


if __name__ == "__main__":
    main()
