# Economic Security — the Cost-of-Corruption Ledger

The spiral anti-patterns (S1–S12) cover *reflexive dynamics*: systems that
amplify their own decline. This module covers the orthogonal failure axis:
**discrete economic attacks** — cases where the code executed exactly as
written and the *mechanism itself was mispriced*. Beanstalk, Mango, and the
Steem takeover were not hacks; they were purchases.

**The one inequality that explains every economic attack:**

```
profit = value extractable via a control surface − cost to corrupt that surface
attack happens (eventually) wherever profit > 0
```

Treat it like an engineering bound, not a probability: if corrupting a control
surface is profitable, price it as *already exploited* — the only unknowns are
who and when. This is Budish's consensus-security bound generalized to every
layer of a token system.

## The four control surfaces

For each surface, the audit computes `cost to corrupt` vs `value extractable`
under **adversarial financing assumptions** (flash loans, borrowed stake,
rented votes, custodial shares):

| Surface | Corruption route | Cost drivers | Value at stake |
|---|---|---|---|
| **Governance** | buy / borrow / flash-loan / bribe-rent a quorum | vote-lock design, timelock, float depth, bribe-market price | treasury, mint rights, emissions control, parameter keys |
| **Oracle** | move the price the system believes | depth on oracle venues over the observation window | borrowable value at manipulated marks, liquidation flow |
| **Consensus / sequencer** | acquire stake/hashpower or rent it | staking ratio × token price, hardware, liquid-staking depth | double-spend, censorship, MEV, bridge custody |
| **Liquidity** | dominate the venue where price forms | inventory + MM agreements | pin/paint prices, force liquidations, exit exploitation |

Financing adjustments that collapse the "cost" side:

- **Flash loans**: if voting power or pool weight is usable within one
  transaction with no lock, acquisition cost ≈ fees ≈ zero (Beanstalk).
- **Borrowed stake**: lending markets let attackers rent the token; cost =
  interest, not principal (and shorting hedges the exit).
- **Bribe markets**: renting existing locked votes (Votium-class) is usually
  far cheaper than buying tokens — vote-*renting* cost is the real quorum
  price for ve systems (the Mochi incident on Curve, Nov 2021).
- **Custodial shares**: exchanges can vote customer deposits (the Steem
  takeover, 2020).

---

## S13 — Captureable Governance (attack surface)

- **Core**: the cost of assembling a deciding quorum is less than the value
  the quorum controls.
- **The inequality**: `cost(quorum) < treasury + NPV(emissions/mint control)`.
  With flash-governance (no vote lock, no timelock) the left side ≈ 0, so
  *any* treasury makes the system a standing bounty.
- **Red flags**: voting power usable in the same block/tx it was acquired; no
  (or bypassable) timelock between pass and execute; quorum small vs float on
  lending markets (borrowable quorum); emergency paths with lower thresholds;
  treasury value ≫ governance-token market depth; bribe-market rental cost per
  vote ≪ token price; custodial concentration that can vote.
- **Instances**:
  - **Beanstalk (Apr 2022)** — flash-loaned supermajority passed a malicious
    proposal in one transaction; ≈$180M drained, attacker cleared ≈$76M.
    Corruption cost: one block of flash-loan fees.
  - **Build Finance DAO (Feb 2022)** — hostile takeover via accumulated
    votes; minted and drained the treasury (small $, canonical mechanics).
  - **Tornado Cash governance (May 2023)** — proposal with hidden
    self-modify logic granted the attacker fake locked votes → full control;
    partially reverted by the attacker afterward.
  - **Steem (2020)** — corporate takeover using exchange-custodied user
    stake to vote out incumbent validators; community exited by forking (Hive).
  - **Near-miss / defended: Mochi vs Curve (Nov 2021)** — gauge + bribe
    rental steered emissions to a self-dealing pool; Curve's emergency DAO
    killed the gauge. Defense = a narrow, fast veto surface.
- **Antidote**: vote-locking (no flash votes) **plus** a timelock long enough
  for exit/veto (a timelock converts the attacker's cost from "fees" to
  "full position risk through the crash they cause"); quorum floors sized to
  borrowable float; separate, higher bars for treasury/mint actions;
  a narrow emergency veto (guardian) with public accountability; monitor
  bribe-rental cost per vote vs value at stake; treasury diversification away
  from the native token (a native-token treasury inflates the prize and
  crashes with the attack — S1's governance cousin).

## S14 — Manipulable-Oracle Leverage (attack surface)

- **Core**: a leverage venue (lending market, perp, CDP) accepts as collateral
  — or settles against — a price that is cheaper to move than the credit it
  unlocks.
- **The inequality**: `cost(move price X% for the oracle window) <
  borrowable/extractable at the inflated mark`. Cost scales with real depth on
  the oracle's venues over its observation window; value scales with listing
  LTV × caps (or absence of caps).
- **Red flags**: spot- or single-venue-derived oracle for a thin asset; no
  supply/borrow caps on the collateral; LTV set by asset class, not by
  manipulation cost; oracle window short vs achievable pump duration; the
  platform's own token as collateral at marks its own thin market sets
  (FTT's CeFi version scored under S1); key-person-scale positions vs
  market depth (CRV, Aug 2023 — survived, barely).
- **Instances**:
  - **Mango Markets (Oct 2022)** — MNGO perp pumped on thin liquidity,
    inflated collateral marks, ≈$114M borrowed out. Manipulation cost was a
    single-digit fraction of the extraction. (Litigation outcomes remain
    contested; the mechanism is undisputed.)
  - **Venus/XVS (May 2021)** — XVS pump → massive borrowing against inflated
    marks → crash left the protocol with roughly $100M-scale bad debt.
  - **Inverse Finance (Apr & Jun 2022)** — INV TWAP manipulated via a thin
    pool; ≈$15.6M then ≈$5.8M extracted.
  - **Moola Market (Oct 2022)** — MOO pumped on thin Celo DEX liquidity,
    ≈$8.4M borrowed (mostly returned as "bounty").
- **Antidote**: LTV and caps as a **function of manipulation cost** (depth
  over the oracle window), not of narrative asset class; borrow caps ≤ a
  fraction of what the manipulation inequality permits; multi-venue,
  manipulation-aware oracles with deviation circuit breakers; refuse
  leverage listings for assets whose depth an attacker can afford; for
  perps: open-interest caps tied to spot depth.

## S15 — Supply-Subsidy Mismatch (DePIN / work networks) (structure)

- **Core**: emissions pay for *capacity* (hardware, storage, coverage) while
  demand-side revenue never materializes — the sink is real but tiny, so the
  economy is an emissions engine renting infrastructure theater.
- **The ratio**: `service revenue / emissions value` (both in USD, trailing).
  Persistently ≪ 1 means token holders subsidize supply that nobody rents —
  S3's professionalized cousin: the faucet pays machines instead of players.
- **Red flags**: capacity metrics (nodes, hotspots, TB, coverage) growing
  while paid demand is flat; revenue/emissions below ~5–10% for years;
  emissions schedule insensitive to utilization; hardware ROI marketed in
  token terms at current prices; burn-and-mint equilibrium (BME) where the
  burn is negligible vs the mint.
- **Instances**:
  - **Helium (2021–22 peak)** — reported data-transfer revenue of a few
    thousand dollars a month against tens of millions in monthly emissions
    value; HNT bled >90% from ATH. The BME design itself is sound
    (demand burns credits at fixed USD price) — the *ratio* was the disease.
    Later pivoted toward Mobile.
  - **Filecoin (2020–23)** — storage capacity vastly exceeded paid demand
    (single-digit utilization for years); miner collateral + emissions ran
    supply-side while revenue lagged (also an S7 case in the library).
  - **Hivemapper-class mapping/sensor networks (2023–25)** — coverage grew
    with emissions; map-data sales remained a small fraction of emissions
    value (evaluate per project against live numbers).
- **Antidote**: **demand-gated emissions** — pay capacity only where
  utilization/revenue exists (per-region caps, utilization multipliers);
  BME with a mint floor tied to burn (mint ≤ k·burn); denominate hardware
  ROI in service revenue, not token appreciation; publish the
  revenue/emissions ratio as a first-class dashboard metric (Axiom 15).

---

## Scoring: the security panel (separate axis, does NOT add to the 54-point spiral score)

Spiral risk (reflexive dynamics) and attack risk (discrete exploits) are
orthogonal; adding them into one number would dilute both. The audit reports
the spiral scorecard **plus** this panel:

| Row | 0 | 1 | 2 (red line) |
|---|---|---|---|
| S13 governance | corruption cost ≫ value (locked votes + timelock + sane quorum) | partial mitigations or unverifiable | quorum flash-loanable/rentable/borrowable below value at stake, or no effective timelock |
| S14 oracle/leverage | no leverage against the token, or caps sized to manipulation cost | thin-asset leverage with partial caps | manipulation cost < borrowable value on any live venue |
| S15 supply subsidy | revenue/emissions ≥ ~0.5 or demand-gated emissions | 0.1–0.5 and trending up | ≪ 0.1 persistently, emissions insensitive to utilization |

**Why a separate panel, not three more scorecard rows:** the 54-point spiral
scorecard is frozen at v2 for prospective-registry comparability
(the repo [ROADMAP](https://github.com/wusijian007/tokenomics-autopsy/blob/main/ROADMAP.md) §3 — no new rows in the total until they clear full
re-calibration and a re-freeze). So S13/S14/S15 are reported *alongside* the
spiral score, never summed into it. S13/S14 (attack surfaces) are genuinely
orthogonal and stay a separate axis permanently; S15 is structure-class by
nature and is a candidate to fold into a future scorecard v3.

**Any 2 on S13/S14 = red line**: treat as *already exploited* when sizing
risk; fix before launch (these are cheaper to fix than any spiral engine —
usually a timelock, a cap, or a delisting). S15 = structure-class: expect
bleed while the ratio stays ≪ 1.

Historical check (back-scored; see [data/security_panel.py](https://github.com/wusijian007/tokenomics-autopsy/blob/main/data/security_panel.py) in the research repo): every exploited
case above scores 2 on its surface **pre-hoc** — the inequality was computable
from public data before each attack. Defended cases (Curve/Mochi; CRV Aug-23;
timelocked majors) score 0–1, and each defense maps to a listed antidote.
No case in the 33-case spiral calibration/holdout set scores a false red line
on this panel (max: partials on FTX/Celsius-style self-marked collateral and
the Waves/Vires entanglement, consistent with their S1/S10 scores).

## Consensus-layer note (L1/L2/restaking audits)

Same ledger, biggest surface: **security budget** = what it costs to attack
consensus vs what consensus protects (bridged value, DEX float, oracle roots).
Checks: staking ratio and its *real* yield source (fee-funded vs inflation-
funded — inflation-funded security is S2 wearing a validator suit); stake
rentability (liquid-staking depth, restaking rehypothecation — the same stake
"securing" N systems secures each less); validator/LST concentration
(a >⅓ staker is a liveness veto); sequencer centralization as a censorship
mono-surface. Budish's bound is the through-line: security spend must scale
with value secured, *persistently, in the bear too*.

## The three mirrored axioms

13. **Make corruption cost exceed the prize, at all times** — locked votes +
    real timelocks + quorum floors sized to borrowable float; meter the
    bribe-rental price of your own governance.
14. **Size leverage to manipulation cost** — LTV, caps, and listings derive
    from depth-over-oracle-window math, never from asset-class vibes.
15. **Gate supply subsidies on demand** — pay for utilization, not capacity;
    publish revenue/emissions; mint ≤ k·burn once BME exists.

Related simulation: `sim6_governance_capture.py` (the timelock/vote-locking
phase diagram, in the research repo's [`simulations/`](https://github.com/wusijian007/tokenomics-autopsy/tree/main/simulations)).
Audit integration: `audit-protocol.md` step 6 (security panel) and step 8
(control-surface map). Case data: [data/security_panel.py](https://github.com/wusijian007/tokenomics-autopsy/blob/main/data/security_panel.py).
