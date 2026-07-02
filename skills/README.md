# Skill Pack — Tokenomics Death-Spiral Audit

An open-source skill distilled from forensic analysis of 50+ landmark token
collapses and **calibrated against a control group of survivors**. It helps you
**audit a token economic design for death-spiral risk** and **design resilient
tokenomics**.

## Contents
```
tokenomics-death-spiral-audit/
  SKILL.md                      # entry point: core idea, 4 modes, quick-reference, red lines
  references/
    anti-patterns.md            # the 15 failure Skills (engine/structure/amplifier/attack) + 15 design axioms
    game-models.md              # the 4 game-theoretic models + critical conditions
    scorecard.md                # measurable 12-row spiral scorecard + security panel + Terra/DAI examples + calibration
    economic-security.md        # cost-of-corruption ledger: S13 governance, S14 oracle, S15 supply-subsidy
    audit-protocol.md           # 15-min quick screen + 10-step full audit + valuation module + blind-spot register
    survivors.md                # control group: why DAI/USDC/stETH/BNB/ETH/GMX/UNI/CRV held
    design-playbook.md          # 10-step design process, parameter benchmarks, launch checklist
    design-patterns.md          # the positive pattern library — 16 mechanisms that work (dual of the anti-patterns)
    archetype-playbooks.md      # per-vertical templates (DEX/lending/perp/stablecoin/L1/GameFi/DePIN/points)
    liquidity-engineering.md    # LVR, venue design, MM agreements, oracle/peg liquidity
    circular-economy.md         # net-payer identity, dual-currency, sink design, DePIN telemetry
    incentive-audit.md          # rewards as contracts: IC/IR, Goodhart red-team, sybil cost, cohort accounting
    lambda-formalization.md     # λ as a Jacobian spectral radius + the reflexivity-beta estimation programme
    simulations.md              # how to run/adapt the 7 calibrated simulations
```

## Using it as a Claude Code / Agent skill
Drop `tokenomics-death-spiral-audit/` into your skills directory (e.g.
`~/.claude/skills/` or a plugin's `skills/`). It triggers when you ask about token
model design, sustainability, stablecoin/staking/GameFi/points/restaking
mechanics, unlock schedules, or due diligence on a token.

## Using it as a human reference
- **Evaluating a project**: `SKILL.md` → quick screen in `audit-protocol.md` →
  full audit: `game-models.md` (classify) → `scorecard.md` (spiral score) →
  `economic-security.md` (security panel) → `../simulations/` (stress-test) →
  valuation module → report template with blind-spot register.
- **Designing a token**: `design-playbook.md` process + `archetype-playbooks.md`
  for your vertical → build from `design-patterns.md` (16 positive mechanisms),
  with the `liquidity-engineering.md` / `circular-economy.md` / `incentive-audit.md`
  deep dives; constrained by `anti-patterns.md` (15 axioms), evidenced by
  `survivors.md`.

The deep analysis with full derivations is in the repo root:
`death-spiral-deep-analysis.md` (Chinese: `代币经济学死亡螺旋_深度分析与失败Skills.md`).

## License
CC BY 4.0. Research / design reference, **not investment advice**. Fraud cases
(S9) are detection targets, not engineering lessons. Reconcile all figures against
live data; some named cases are in ongoing litigation.
