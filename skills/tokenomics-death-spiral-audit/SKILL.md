---
name: tokenomics-death-spiral-audit
description: >
  Audit a crypto/Web3 token economic design for death-spiral (reflexive collapse)
  and economic-attack risk, and guide the design of resilient tokenomics. Use
  whenever someone is designing, reviewing, or doing due diligence on a token
  model, stablecoin, staking/yield mechanism, GameFi/Play-to-Earn economy,
  points/airdrop program, restaking/looped-leverage product, bonding/treasury
  (3,3) system, or token unlock/emission schedule — or asks "will this tokenomics
  work", "is this sustainable", "what's the risk in this token model", or "how do
  I design tokenomics that won't collapse". Built from forensic analysis of 50+
  landmark collapses (Terra, OlympusDAO, Axie, FTX, ICP…), a survivor control
  group (DAI, USDC, stETH, GMX…), and out-of-sample validation. Research / design
  reference, NOT investment advice.
license: CC-BY-4.0
metadata:
  version: "2.0.0"
  instrument: "spiral scorecard v2 (frozen 2026-07-02) + security panel"
  homepage: "https://github.com/wusijian007/tokenomics-autopsy"
---

# Tokenomics Death-Spiral Audit

A death spiral is **not bad luck or bad ops — it is a built-in phase transition.**
A token model with reflexive feedback is a stable attractor above a critical
parameter and jumps to a different attractor (→ 0, or → backing) once that
threshold is crossed. This skill finds the threshold *before* it is crossed.

> **Self-contained.** Everything needed to audit or design ships in this folder:
> the `references/` knowledge base and runnable, stdlib-only `scripts/`
> (stress-runner + report generator). The full research repo — 8 calibrated
> simulations, case datasets, and the validation layer (holdout backtest +
> frozen prospective registry) — is optional and lives at
> https://github.com/wusijian007/tokenomics-autopsy.

## The one idea that explains every collapse

Every death spiral is a **positive feedback loop** where the token's own price is
the fuel for the mechanism:

```
price ↓ → mechanism is forced to mint / sell / liquidate / redeem → supply ↑ / demand ↓ → price ↓↓
```

Formally, the system gain is `λ = (∂g/∂F)·(∂h/∂P)`, where `P` is price and `F` is
"fundamentals". Healthy projects keep `∂(fundamentals)/∂(price) ≈ 0` so `λ < 1`
(self-correcting). Death-spiral projects wire fundamentals *to* price (collateral
is the token itself, demand is an APY, rewards depend on new users) so `λ > 1`
and any downward nudge is amplified.

**The master test:** *If the token's price went to zero, would anyone still need
this token?* If the answer is "no", demand is reflexive and unanchored — redesign
or walk away. Every survivor in the control group passes this test; every
collapse in the case library fails it somewhere (`references/survivors.md`).

## How to use this skill — pick a mode

### Mode Q — Quick screen (~15 min triage)
Run the 8-question screen at the top of `references/audit-protocol.md`
(zero-price test, backing, yield source, redemption coverage, emission cap,
float/unlocks, holders, rented-vs-looped growth). Output: `PASS` / `CONCERNS` /
`RED LINE`. Use it before any deeper commitment, or when the user just wants a
sanity check.

### Mode A — Full audit (due-diligence grade)
Follow `references/audit-protocol.md` end-to-end:
1. **Collect inputs** (docs, unlock schedule, contracts, treasury, revenue,
   TVL history, holders, depth) — the protocol lists sources.
2. **Draw the mechanism map** and mark every price-dependent flow (candidate
   `λ>1` loops).
3. **Classify the game structure** with `references/game-models.md`.
4. **Score the 12 rows** of `references/scorecard.md` using its measurement
   procedures; fill the evidence table with confidence labels.
5. **Compute distance-to-threshold** for every triggered row (runway months,
   R vs 1, unlock walls vs depth…).
6. **Score the security panel** (S13/S14/S15) — the cost-of-corruption ledger
   in `references/economic-security.md`. This is a *separate axis* from the
   spiral score: it catches attacks where the code works and the mechanism is
   mispriced (Beanstalk, Mango). Mandatory for anything with governance, a
   price oracle used for leverage, or a DePIN/work-token supply side.
7. **Stress-test** with the calibrated simulations (`references/simulations.md`).
8. **Map the control surfaces** (governance / oracle / consensus / liquidity)
   and contagion, then **write the report** using the protocol's template:
   verdict → scorecard → security panel → thresholds → stress test → valuation
   context → prescriptions → limitations (incl. the blind-spot register).

### Mode B — Designing resilient tokenomics from scratch
Follow `references/design-playbook.md` step by step: necessity test → demand
anchor → value capture → supply schedule (with parameter benchmarks) →
stability infrastructure → incentives-as-CAC → liquidity plan → monitoring
dashboard → pre-launch stress test → launch checklist. The constraints are the
15 design axioms at the end of `references/anti-patterns.md` (12 spiral + 3
economic-security); the non-negotiable one is axiom #1: **decouple fundamentals
from price (`λ < 1`)**. Then reach for the constructive toolkit:
- **`references/design-patterns.md`** — 16 positive mechanisms (the dual of the
  anti-patterns): what to build, its parameters, the failure modes it *adds*,
  and which Sx it neutralizes. Compose, then re-audit the whole.
- **`references/archetype-playbooks.md`** — per-vertical templates (DEX,
  lending, perp, stablecoin, L1/L2, GameFi, DePIN, points) with benchmarks, a
  survivor anchor, and the *one number* that decides each.
- Deep dives: **`references/liquidity-engineering.md`** (LVR, venue choice, MM
  terms, oracle depth), **`references/circular-economy.md`** (net-payer
  identity, dual-currency, sink design, DePIN), **`references/incentive-audit.md`**
  (rewards as contracts: IC/IR, Goodhart red-team, sybil cost, cohort accounting).

### Mode C — Demonstrating / stress-testing a mechanism
To score a whole design at once, run the **bundled** `scripts/stress_runner.py`
on a copy of `scripts/design.example.yaml` — it scores all 12 spiral rows plus
the security panel and emits the step-9 verdict (stdlib-only, works anywhere
this skill is installed). For the phase-transition demonstrations themselves,
the research repo's `simulations/` folder has 8 runnable, calibrated models —
six failure archetypes plus two constructive ones (`sim7` PID-damped stability,
`sim8` spender-class economy); see `references/simulations.md`. The math behind
λ (Jacobian spectral radius + the reflexivity-beta estimation programme) is in
`references/lambda-formalization.md`.

## Quick-reference: the 15 failure Skills

Two axes. **Spiral risk** (S1–S12, scored 0–54): reflexive dynamics that
amplify a decline. **Attack risk** (S13–S15, separate panel): discrete
exploits where the code works and the mechanism is mispriced. Spiral tiers:
**engine** (creates the spiral, ×3), **structure** (builds sell pressure, ×2),
**amplifier** (worsens shocks, ×1).

| # | Anti-pattern | Tier | One-line tell | Killer threshold |
|---|---|---|---|---|
| S1 | Reflexive collateral | engine | reserve = the token itself | corr(reserve, liability) → 1 |
| S2 | Subsidized demand engine | engine | APY paid from subsidy, not revenue | payout > revenue; runway < 12mo |
| S3 | Uncapped faucet | structure | reward token has no supply cap | sink/faucet < 1, sink needs new users |
| S4 | (3,3) coordination fragility | structure | "everyone stakes = best" | price/backing > 3; yield from inflation |
| S5 | Sequential-service redemption | engine | instant FCFS + illiquid | liquidity coverage < redeemable liabilities |
| S6 | Seigniorage absorbing barrier | engine | mint/burn dual-token stable | reserve ratio R = M/S → 1 |
| S7 | Float–FDV asymmetry | structure | low float, high FDV, cheap insiders | float <10%; 1yr unlock >50% of float |
| S8 | Velocity leak | amplifier | pure medium-of-exchange, no capture | no burn/lock/fee-share; high velocity |
| S9 | Narrative-only demand | engine | celeb/meme, zero cash flow | no revenue; concentrated, unlocked |
| S10 | Leverage contagion | amplifier | tokens cross-collateralize | shared MM/collateral; corr→1 in stress |
| S11 | Mercenary points / rented TVL | structure | TVL arrives with the points program | organic share <30%; snapshot cliff |
| S12 | Recursive leverage loop | structure | derivative looped as its own collateral | unwind size > real market depth |
| S13 | Captureable governance | attack surface | quorum is buyable/borrowable | cost-to-corrupt < value at stake; no timelock |
| S14 | Manipulable-oracle leverage | attack surface | thin token as collateral/perp | manip cost < borrowable value |
| S15 | Supply-subsidy mismatch | structure (DePIN) | emissions pay hardware, no demand | service revenue / emissions ≪ 1 |

**Decision rule** (spiral axis; calibrated on 10 collapses + 8 survivors,
validated on 15 holdout cases 15/15, see `references/scorecard.md`): any engine
clearly present → structural death-spiral risk, redesign first. Structures
without engines → bleed or deleveraging risk; survival hinges on the zero-price
anchor. Amplifiers alone → survivable, but they set the blast radius. **On the
attack axis**: any S13/S14 at 2 → treat the surface as already exploited (fix
it — usually a timelock, a cap, or a delisting).

Full detail, instances, and antidotes: `references/anti-patterns.md`.
The cost-of-corruption ledger (S13–S15): `references/economic-security.md`.
Why the survivors survived (control group): `references/survivors.md`.

## Hard red lines (auto-fail)
- Algorithmic stablecoin collateralized by its own/affiliated token, no reserve circuit-breaker. (S6+S1 → Terra, Iron)
- Yield whose source is unidentifiable or is "the next depositor". (S2 → Anchor, HEX)
- Reward emission with no cap whose only sink is user growth. (S3 → Axie, STEPN)
- Instant full redemption promised against illiquid/maturity-mismatched assets. (S5 → FTX, Celsius)
- Demand that fails the zero-price test (100% narrative/APY/celebrity). (S9 → LIBRA, SQUID)
- Leverage loops whose unwind exceeds real market depth, with no LTV/supply caps. (S12 → UST Degenbox, LRT cascades)
- Governance quorum cheaper to buy/borrow/flash-loan than the treasury it controls, with no timelock. (S13 → Beanstalk)
- Leverage against a token whose oracle price costs less to move than the credit it unlocks. (S14 → Mango)

## Scope & honesty
Research and design reference, **not investment advice**. Ponzi/rug cases (S9)
are *fraud*, not failed engineering — for those, the skill's value is detection,
not repair. Validation status: in-sample calibration (18 cases) **plus an
out-of-sample layer** — a 15-case leakage-audited holdout backtest (decision
rule 15/15 correct) and a frozen prospective registry with falsifiable
predictions under 2027/2028 review (repo `validation/`; summarized in
`references/scorecard.md`). Key nuance from the holdout: **the weighted total
is an intensity gauge, not the classifier** — trust the engine → structure →
anchor rule. Treat fresh audits as hypotheses and re-score as data improves.
Estimates in the data layer are order-of-magnitude; reconcile against live
data. Several named cases involve ongoing litigation — defer to final rulings.
