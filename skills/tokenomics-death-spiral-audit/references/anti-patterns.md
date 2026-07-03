# The 15 Failure Skills (Anti-Pattern Catalog)

Each anti-pattern is something you can detect at the **whitepaper / smart-contract
stage**, before launch. Format: core → game/math structure → quantitative red
flags → historical instances → design antidote.

S1–S10 are distilled from the 2009–2022 collapse record; S11–S12 cover the
2023–2026 wave (points-farmed TVL, restaking/looped leverage); S13–S15 cover
**economic attacks** — the orthogonal axis where the code works and the
mechanism itself is mispriced (full framework: `economic-security.md`).
Measurement procedures for every red flag live in `scorecard.md`.

> Companion analysis with full derivations (research repo):
> [death-spiral-deep-analysis.md](https://github.com/wusijian007/tokenomics-autopsy/blob/main/death-spiral-deep-analysis.md)
> (Chinese: 代币经济学死亡螺旋_深度分析与失败Skills.md). Game models: `game-models.md`.
> Control group (why survivors survived): `survivors.md`.

## Four tiers — engines, structures, amplifiers, attack surfaces

| Tier | Skills | Role | Typical failure shape |
|---|---|---|---|
| **Engine** (×3 weight) | S1 S2 S5 S6 S9 | creates the `λ>1` loop itself | run / collapse to zero |
| **Structure** (×2 weight) | S3 S4 S7 S11 S12 S15 | builds structural sell pressure | slow bleed / violent deleveraging |
| **Amplifier** (×1 weight) | S8 S10 | worsens whatever else fires | stress passthrough |
| **Attack surface** (separate axis) | S13 S14 | discrete exploit where corruption cost < prize | one-shot drain, then collapse |

S13/S14/S15 report on a **separate security panel**, not the 54-point spiral
total (see `scorecard.md` and `economic-security.md`). Reason: the 54-point
scorecard is **frozen at v2** for prospective-registry comparability, and
instrument discipline (the repo [ROADMAP](https://github.com/wusijian007/tokenomics-autopsy/blob/main/ROADMAP.md) §3) bars folding new rows into the total
until they clear full re-calibration and a re-freeze. S15 is *structure-class
by nature* (it produces a slow bleed), which is why it sits in the structure
tier above — but for scoring integrity it lives on the panel for now. Attack
risk (S13/S14) is genuinely orthogonal to spiral risk and stays a separate
axis permanently.

**Decision rule (calibrated on 18 historical cases and validated out-of-sample
on 15 leakage-audited holdout cases, 15/15 correct — see `scorecard.md`):**
any *engine* clearly present → structural death-spiral risk, redesign before
anything else. No engine but a *structure* clearly present → bleed/deleveraging
risk; survival then depends entirely on the zero-price anchor test. Amplifiers
alone → survivable, but they set how hard external shocks hit.

---

## S1 — Reflexive Collateral (engine)
- **Core**: the token uses itself (or an asset tightly correlated to itself) as
  reserve / collateral.
- **Structure**: collateral value and the liability it backs are positively
  correlated, so `λ > 1` — when price falls, both sides deteriorate together.
- **Red flags**: corr(reserve asset, liability) → 1; "A-coin backs the A-coin
  system"; self-printed collateral held by affiliated parties.
- **Instances**: Terra (LUNA backs UST), FTX (FTT as collateral), Iron (TITAN
  backs IRON).
- **Antidote**: exogenous, *de-correlated* collateral (USDC/ETH); >150%
  overcollateralization; reserve-adequacy circuit breaker.

## S2 — Subsidized Demand Engine (engine)
- **Core**: core demand comes from a subsidized high APY, not real willingness to pay.
- **Structure**: a subsidy is a forward-borrow against future demand (reflexive
  demand curve). When the subsidy ends or confidence flips, demand vanishes.
- **Red flags**: protocol **payout > protocol revenue**; yield-reserve runway < 12
  months; > 60% of token demand concentrated in one incentive pool.
- **Instances**: Anchor 19.5% (≈75% of UST demand sat there), OHM, most
  "liquidity-mining life-support" tokens.
- **Antidote**: real yield (= real fees); APY auto-throttles to reserve; design a
  soft-landing for when the subsidy is withdrawn.

## S3 — Uncapped Faucet (structure)
- **Core**: the reward token has no hard supply cap and its sink depends on new users.
- **Structure**: faucet (emission) is not reflexive but sink (burn/use) is — it
  only clears while the user base grows. `sink/faucet < 1` once growth stalls.
- **Red flags**: no supply ceiling; annual emission > demand growth; the sink's
  demand source is *new users*, not real consumption by the existing base.
- **Instances**: Axie SLP, STEPN GST, DeFi Kingdoms JEWEL.
- **Antidote**: bind emission to the realized sink (mint ≤ burn); hard cap; make
  the sink real utility consumed by existing users, not onboarding by new ones.

## S4 — Coordination-Fragile Staking ((3,3)) (structure)
- **Core**: the model paints "everyone stakes" as optimal, but the Nash
  equilibrium is "everyone exits".
- **Structure**: a prisoner's dilemma disguised as cooperation; backward induction
  unravels it from the last buyer. Stable only while new money > dilution.
- **Red flags**: APY from inflation / new bonds; `market price / backing (RFV) > 3`;
  strong first-mover advantage to "stay" over "exit".
- **Instances**: OHM and every (3,3) fork (TIME, KLIMA, …).
- **Antidote**: pay yield from real revenue; symmetrize exit; publish backing and
  discourage premium speculation.

## S5 — Sequential-Service Redemption (Bank Run) (engine)
- **Core**: instant, full, first-come-first-served redemption + maturity/liquidity
  mismatch.
- **Structure**: Diamond–Dybvig multiple equilibria; the first-mover advantage
  makes the bad (run) equilibrium self-fulfilling on any belief shock (sunspot).
- **Red flags**: instant redemption promised against illiquid assets; liquidity
  coverage < instantly-redeemable liabilities; no queue / FCFS.
- **Instances**: FTX, Celsius, Voyager, the Anchor withdrawal wave.
- **Antidote**: redemption queues / lockups; **pro-rata haircuts instead of FCFS**
  (kills the run incentive); liquidity coverage > 100%; circuit breakers.
- **Corollary (from the stETH control case)**: it is the *promise* of instant
  redemption, not illiquidity itself, that creates the run. An asset with no
  instant-redemption promise can trade at a discount but cannot be run.

## S6 — Seigniorage Absorbing Barrier (engine)
- **Core**: a dual-token mint/burn stablecoin turns de-peg selling pressure into
  unlimited minting of the reserve token.
- **Structure**: reserve ratio `R = M_reserve / S_stable`. `R < 1` is an
  irreversible absorbing barrier — past it, full redemption mathematically forces
  the reserve token to 0.
- **Red flags**: no reserve-adequacy circuit breaker; unlimited mint on de-peg;
  reserve token is reflexive/same-system as the stablecoin.
- **Instances**: Terra, Iron, Basis Cash, ESD.
- **Antidote**: reserve-ratio circuit breaker + switch to partial collateral; mint
  rate-limiting is only a band-aid — the real fix is to drop "algorithmic + own
  token" entirely.

## S7 — Float–FDV Asymmetry (structure)
- **Core**: the marginal seller (insiders) has a cost basis ≈ 0, and continuous
  unlocks drag price toward the floor.
- **Structure**: lemon market (info asymmetry on the unlock calendar) + a supply
  curve that shifts right every unlock. A *continuous* spiral, not a run.
- **Red flags**: initial float < 10%; first-year unlock > 50% of float;
  `FDV / annual real revenue > 100×` (no revenue → auto-max risk).
- **Instances**: ICP, Filecoin, Worldcoin, ApeCoin.
- **Antidote**: long, linear unlocks (no cliffs); float matched to real demand
  depth; insider unlocks tied to verifiable milestones; on-chain public calendar.

## S8 — Velocity Leak (amplifier)
- **Core**: a pure medium-of-exchange token with no value capture; high velocity
  keeps pushing price down.
- **Structure**: `P = utility_value / (M · V)` — high V → low P; no non-reflexive
  reason to hold.
- **Red flags**: no burn / no ve-lock / no fee-share; high share of "earn-and-dump"
  users; very short median holding time.
- **Instances**: most utility/GameFi reward tokens.
- **Antidote**: fee burn, ve-locking for governance + fee share — upgrade the token
  from "medium of exchange" to "productive asset".
- **Calibration note**: S8 alone is a *price-performance* problem, not a spiral
  (UNI survived years of zero value capture). That is why its weight is ×1.

## S9 — Narrative-Only Demand (engine)
- **Core**: demand is 100% narrative / celebrity / meme with no cash-flow anchor.
- **Structure**: extreme reflexive demand = attention; attention can be financed
  instantly and can evaporate instantly. (Usually *fraud*, not failed engineering.)
- **Red flags**: zero revenue; extreme holder concentration; team/celebrity
  holdings **unlocked**; contract has high tax / cannot-sell / mint backdoors.
- **Instances**: LIBRA, MELANIA, TRUMP, HAWK, SQUID, SafeMoon.
- **Antidote**: none by design — the value here is *detection and avoidance*, and a
  regulatory/due-diligence red line.

## S10 — Leverage Contagion (amplifier)
- **Core**: protocols are interlinked at the collateral / market-making / lending
  layer, so one local spiral becomes systemic.
- **Structure**: tokens cross-collateralize; concentrated market makers; in a
  crisis correlations → 1.
- **Red flags**: tokens used as collateral for each other; few affiliated MMs
  provide most liquidity; shared upstream risk exposure; **key-person leverage**
  (founder/whale loans collateralized by the governance token — CRV, Aug 2023).
- **Instances**: Terra → 3AC → Celsius/Voyager → FTX chain reaction.
- **Antidote**: diversify collateral + stress-test correlations; cap affiliated
  MM concentration; isolate risk exposures; monitor large on-chain loans against
  the native token.

## S11 — Mercenary Points / Rented TVL (structure, 2023–26)
- **Core**: growth metrics (TVL, users, volume) are *rented* with expected future
  token payments (points → airdrop). The demand is a forward claim on the token,
  so it evaporates exactly when the token arrives.
- **Structure**: a points program forward-sells emissions. Expected-airdrop value
  scales with FDV expectations → reflexive. Because every farmer shares the same
  snapshot/TGE calendar, exit is *coordinated*: the airdrop unlock (supply shock)
  and the mercenary-capital exit (demand cliff) land on the same day. Combines
  Model 4 (supply glut) with Model 2 (new-money game).
- **Red flags**: majority of TVL arrived only after the points announcement;
  capital exits at each season snapshot; fee revenue per $ TVL far below peers
  (parked, not used); escalating multi-season promises; points farmed with
  leverage (loops → S12); points markets pricing implied FDV far above
  comparables.
- **Instances**: Blast (TVL cliff after the mid-2024 airdrop), friend.tech
  (activity and fees collapsed once the reward cycle ended), the 2024 LRT
  points wave, trade-mining wash volume (dYdX v1 era).
- **Antidote**: vest/lock rewards past TGE; reward *flow* (fees actually paid)
  rather than *stock* (TVL parked); publish an organic-baseline dashboard
  (what remains if points stop); taper seasons; cap airdrop size relative to
  TGE float so the cliff can't overwhelm demand.

## S12 — Recursive Leverage Loop (structure, 2022–26)
- **Core**: a yield-bearing derivative is looped as collateral to borrow its own
  underlying (deposit stETH → borrow ETH → buy stETH → repeat), or a "stable"
  carry yield is levered (UST Degenbox; funding-rate carry). The base asset can
  be sound — the loop adds a liquidation channel that makes the *system*
  reflexive.
- **Structure**: with loop LTV `ℓ` and `n` iterations, system leverage
  → `1/(1−ℓ)` as n grows. A small discount/de-peg breaches clustered liquidation
  thresholds → forced unwinding sells the derivative into thin liquidity →
  deeper discount → more liquidations. `λ > 1` through the liquidation channel.
  Critical condition: **potential unwind size > real secondary-market depth**.
- **Red flags**: a large share of the derivative's float sits in leveraged loops;
  loop APY ≫ base APY; liquidation thresholds clustered in a narrow band; thin
  DEX depth vs loop size; funding-rate-dependent yield marketed as "stable";
  no supply/LTV caps on correlated collateral.
- **Instances**: stETH loop unwind of June 2022 (amplified Celsius/3AC; stETH
  itself held — see `survivors.md`), UST Degenbox leverage (Abracadabra),
  ezETH's April 2024 depeg-liquidation cascade. Watch item: levered
  funding-carry stables in a prolonged negative-funding regime.
- **Antidote**: LTV and supply caps for self-referential/correlated collateral;
  stress-test the full unwind against *actual* DEX depth, not TVL; oracle-
  deviation circuit breakers; never market carry yield as principal-stable.

## S13 — Captureable Governance (attack surface, 2020–26)
- **Core**: assembling a deciding quorum costs less than the value the quorum
  controls (treasury, mint rights, emissions).
- **The inequality**: `cost(quorum) < value at stake`. Flash-loanable votes +
  no timelock ⇒ cost ≈ fees ⇒ any treasury is a standing bounty.
- **Red flags**: voting power usable in the block it was acquired; no
  effective timelock; quorum borrowable on lending markets or rentable via
  bribe markets below value at stake; custodial stake can vote; treasury held
  in the native token (inflates the prize, crashes with the attack).
- **Instances**: Beanstalk (Apr 2022, ≈$180M drained via flash-loaned
  supermajority), Build Finance DAO (2022 hostile takeover), Tornado Cash
  governance (2023), Steem custodial-stake takeover (2020). Defended
  near-miss: Mochi vs Curve's emergency DAO (2021).
- **Antidote**: vote-locking + real timelock (turns attacker cost from "fees"
  into "position risk through the crash they cause"); quorum floors sized to
  borrowable float; higher bars for treasury/mint actions; narrow emergency
  veto; monitor bribe-rental cost per vote. Full math: `economic-security.md`.

## S14 — Manipulable-Oracle Leverage (attack surface, 2020–26)
- **Core**: a lending market / perp / CDP accepts a price that is cheaper to
  move than the credit it unlocks.
- **The inequality**: `cost(move price over the oracle window) <
  borrowable at the inflated mark`.
- **Red flags**: spot/single-venue oracle for a thin asset; no supply/borrow
  caps; LTV set by asset class rather than manipulation cost; short oracle
  window; platform's own token as collateral at self-set marks;
  key-person-scale positions vs depth (CRV, Aug 2023 — survived, barely).
- **Instances**: Mango (Oct 2022, ≈$114M), Venus/XVS (2021, ~$100M-scale bad
  debt), Inverse Finance (2022, two attacks), Moola (2022).
- **Antidote**: LTV/caps as a function of manipulation cost (depth over the
  oracle window); OI caps tied to spot depth; multi-venue manipulation-aware
  oracles + deviation breakers; refuse thin-asset leverage listings.
  Full math: `economic-security.md`.

## S15 — Supply-Subsidy Mismatch (structure, DePIN/work networks, 2020–26)
- **Core**: emissions pay for *capacity* (hardware, storage, coverage) while
  paid demand never arrives — the faucet pays machines instead of players.
  S3's professionalized cousin.
- **Structure**: `service revenue / emissions value ≪ 1` persistently. The sink
  is real but tiny; token holders subsidize supply nobody rents.
- **Red flags**: capacity metrics (nodes/hotspots/TB/coverage) growing while
  paid demand is flat; revenue/emissions <5–10% for years; emissions
  insensitive to utilization; hardware ROI marketed in token terms at current
  prices; burn-and-mint equilibrium (BME) where burn ≪ mint.
- **Instances**: Helium (2021–22 peak — sound BME design, fatal ratio: a few
  $K/mo revenue vs tens of $M/mo emissions), Filecoin (single-digit
  utilization for years; also an S7 case), Hivemapper-class networks
  (evaluate live).
- **Antidote**: demand-gated emissions (utilization multipliers, per-region
  caps); BME mint floor tied to burn (mint ≤ k·burn); denominate hardware ROI
  in service revenue, not token appreciation; publish revenue/emissions as a
  first-class metric (Axiom 15). Full framework: `economic-security.md`.

---

# The 15 Design Axioms (mirror of the anti-patterns)

1. **Decouple fundamentals from price** — ensure `λ < 1`. This is the master axiom.
2. **Exogenous, de-correlated collateral** — never the native token; stress-test
   tail correlation → 1.
3. **Yield from real cash flow** — real yield first; any subsidy needs a runway and
   a soft-landing path.
4. **Self-balancing supply/demand** — `sink ≥ faucet`; emission bound to real
   consumption, not user growth.
5. **Kill the first-mover advantage** — pro-rata payouts, redemption queues, circuit
   breakers; make "running first" non-profitable.
6. **Predictable supply + symmetric info** — linear unlocks, float matched to
   demand, public on-chain calendar.
7. **Capture value to suppress velocity** — long-term holding driven by real
   fee-share/governance, not APY bribery.
8. **Demand must pass the zero-price test** — "if price went to zero, would anyone
   still need this?" If no, redesign or don't ship.
9. **Isolate contagion** — limit cross-protocol collateral links, MM concentration,
   and key-person leverage on the governance token.
10. **Transparency is verifiable** — treasury, collateral, unlocks, team holdings
    all on-chain readable. Opacity is the #1 sunspot fuel.
11. **Rent growth only with vesting** — reward flow (fees paid), not stock (TVL
    parked); know and publish your organic baseline; size the airdrop so the
    TGE cliff cannot overwhelm real demand.
12. **Cap recursion** — leverage loops on your own token/derivative are a systemic
    short fuse; cap LTV and supply for correlated collateral and stress-test the
    unwind against real market depth.
13. **Make corruption cost exceed the prize, always** — locked votes + real
    timelocks + quorum floors sized to borrowable float; meter the bribe-rental
    price of your own governance; keep the treasury off the native token.
14. **Size leverage to manipulation cost** — LTV, caps, and listings derive from
    depth-over-oracle-window math, never from asset-class vibes.
15. **Gate supply subsidies on demand** — pay for utilization, not capacity;
    publish revenue/emissions; mint ≤ k·burn once a BME exists.

The positive-direction expansion of these axioms — a full design process with
parameter benchmarks and a worked example — is in `design-playbook.md`.
Axioms 13–15 (economic-security) are detailed in `economic-security.md`.
