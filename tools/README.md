# Tools — the product layer (v6)

Runnable tools that turn the skill pack from a document set into an executable
instrument. Dependency-light (Python stdlib + numpy/matplotlib where charts are
involved); each reads a small declarative input so results are reproducible.

| Tool | Input | Does |
|---|---|---|
| [`stress_runner.py`](stress_runner.py) | `design.example.yaml` | Scores a **design spec** on the 12 spiral rows + the S13/S14/S15 security panel, runs the matching sims, and emits the design-playbook step-9 verdict (score, flags, band, prescriptions). The "audit a design before you build it" tool. |
| [`report_generator.py`](report_generator.py) | `audit.example.json` | Formats a **completed audit** into the full `audit-protocol.md` report (evidence table, security panel, thresholds, valuation quadrant, blind-spot register). The "write up a human audit" tool. |
| [`kappa_reliability.py`](kappa_reliability.py) | two score sheets | Weighted Cohen's κ between two independent scorers, per-row + overall (E3 reliability). Ships a demo; a real study needs two humans + a blind set. |
| [`registry_monitor.py`](registry_monitor.py) | `registry_metrics.example.json` | Checks the frozen prospective-registry projects against their pre-registered triggers → OK / WATCH / ALERT. Data layer is a stub; wire to live feeds for production. |
| [`build_skill_dist.py`](build_skill_dist.py) | — | Validates the installable skill (frontmatter spec, self-containment, `scripts/` drift vs `tools/`) and builds `dist/`: the skill zip + a single-file `PROMPT_PACK.md` for no-skill platforms. |

> `stress_runner.py`, `report_generator.py` and their two example inputs are
> **byte-mirrored** into `skills/tokenomics-death-spiral-audit/scripts/` so the
> installed skill is self-contained. Edit the `tools/` copy (canonical), then
> re-copy; `build_skill_dist.py` fails the build on any drift.

## Quick start

```bash
cd tools

# 1. Screen a design before building it (edit design.example.yaml for your token)
python stress_runner.py design.example.yaml
python stress_runner.py design.badexample.yaml     # a Terra-like design -> REDESIGN

# 2. Turn a completed audit into a shareable report
python report_generator.py audit.example.json

# 3. Inter-rater reliability (demo, or pass two real score sheets)
python kappa_reliability.py
python kappa_reliability.py raterA.json raterB.json

# 4. Monitor the frozen registry against a metrics snapshot
python registry_monitor.py registry_metrics.example.json
```

## Design spec schema (stress_runner)

`design.example.yaml` is a flat, commented spec: `section:` headers with
`key: value` pairs, covering demand, collateral, redemption, emissions, supply,
value capture, holders, incentives, leverage, contagion, governance, oracle, and
DePIN. Each field maps to a scorecard measurement rule (`scorecard.md`) or a
security-panel row (`economic-security.md`). Copy it, fill in your design, and
run. JSON specs also work; PyYAML is used if installed, otherwise a built-in
parser handles the flat subset.

## Honesty

- The stress-runner scores the **declared** spec — garbage in, garbage out.
  It is a design-time screen, not a substitute for the evidence-based full audit
  (`audit-protocol.md`) against live on-chain data.
- The security panel (S13/S14/S15) is a **separate axis**, never summed into the
  54-point spiral score (the scorecard stays frozen at v2 for registry
  comparability).
- `kappa_reliability` and `registry_monitor` ship the machinery; a real κ study
  needs independent human raters, and live monitoring needs the data feeds wired.
- Not investment advice.
