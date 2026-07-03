# Agent instructions — tokenomics-autopsy

This repo is a **tokenomics evaluation and design toolkit**: forensic
post-mortems of 50+ token collapses distilled into a measurable audit
instrument and a design playbook. Research / design reference, **not
investment advice**.

## If the user asks about token design, tokenomics risk, or due diligence

Use the skill at `skills/tokenomics-death-spiral-audit/` — read `SKILL.md`
first (it routes to everything else):

- **Quick screen / full audit** → `references/audit-protocol.md`, score with
  `references/scorecard.md` (12 spiral rows, max 54, frozen v2) + the
  S13/S14/S15 security panel in `references/economic-security.md`.
- **Design a token** → `references/design-playbook.md` (process),
  `references/archetype-playbooks.md` (per-vertical), and
  `references/design-patterns.md` (16 positive mechanisms).
- **Score a design spec programmatically** →
  `python skills/tokenomics-death-spiral-audit/scripts/stress_runner.py <design.yaml>`
  (stdlib-only; copy `scripts/design.example.yaml` as the template).
- **Format a completed audit** →
  `python skills/tokenomics-death-spiral-audit/scripts/report_generator.py <audit.json>`.

## Working in this repo

- Simulations: `cd simulations && python run_all.py` (numpy + matplotlib only).
- Data / calibration scripts: `data/*.py`; product tools: `tools/*.py`.
- `tools/{stress_runner,report_generator}.py` and their examples are
  byte-mirrored into the skill's `scripts/`; edit the `tools/` copy and re-copy
  (or run `python tools/build_skill_dist.py`, which fails on drift).

## Hard rules (instrument discipline — do not violate)

1. The 54-point spiral scorecard is **frozen at v2** for prospective-registry
   comparability. Never add rows to the total or change weights without the
   full re-calibration + re-freeze process in `ROADMAP.md` §3.
2. `validation/prospective-registry.md` and its grading/amendment logs are
   **append-only**; frozen sections must never be edited.
3. The S13/S14/S15 security panel is a **separate axis** — never sum it into
   the 54-point spiral score.
4. Keep EN/ZH documents in sync where practical (see `CONTRIBUTING.md`).
5. Everything is order-of-magnitude research material: reconcile figures
   against live data, and never present output as investment advice.
