# Bundled scripts (stdlib-only, no dependencies)

Runnable companions to the skill — Python 3.8+ standard library only, so they
work in any environment the skill is installed into.

| Script | Input | Does |
|---|---|---|
| `stress_runner.py` | `design.example.yaml` | Scores a design spec on the 12 spiral rows + the S13/S14/S15 security panel and emits the design-playbook step-9 verdict (score, flags, band, prescriptions). |
| `report_generator.py` | `audit.example.json` | Formats a completed audit into the full `audit-protocol.md` report (evidence table, security panel, thresholds, valuation quadrant, blind-spot register). |

```bash
python stress_runner.py design.example.yaml     # copy + edit the spec for your token
python report_generator.py audit.example.json
```

If the full research repo is present (these scripts detect it automatically),
`stress_runner.py` also runs the matching calibrated simulations (sim4 bank-run,
sim6 governance-capture); standalone installs simply skip them with a note.
Full repo — 8 simulations, case datasets, the validation layer:
https://github.com/wusijian007/tokenomics-autopsy

These files are byte-mirrors of the repo's `tools/` versions; the repo's
`tools/build_skill_dist.py` fails the build if they drift.
