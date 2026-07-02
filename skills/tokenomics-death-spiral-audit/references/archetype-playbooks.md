# Archetype Playbooks

The `design-playbook.md` is the general 10-step process. This is the
per-vertical specialization: for each of 8 common token archetypes — the demand
thesis that actually works, the anti-patterns that kill it, the go-to positive
patterns (`design-patterns.md`), parameter benchmarks, the survivor to anchor
on, and the **one number that decides it**. Use alongside the general process,
not instead of it.

> Benchmarks are empirical starting points distilled from the survivor set and
> the case library — justify deviations in writing (playbook step 4). None are
> hard laws; the *mechanism* logic behind each is.

---

## 1. DEX / AMM
- **Demand thesis (works)**: fee-share on real swap volume (P2); ve-lock to
  direct emissions and earn fees (P3). Passes zero-price: traders swap whether
  or not they hold the token.
- **Killer anti-patterns**: S8 (no capture — the early UNI state), S11
  (emissions-rented liquidity), S2 (LM yield > fees).
- **Go-to patterns**: P2 fee-share, P3 ve+gauge, P1 burn, P4 buyback; on the
  liquidity side, LVR-aware venue design (`liquidity-engineering.md`).
- **Benchmarks**: fee APR ≥ LVR APR on main pools; emissions ≤ fees within
  ~18–24 mo; ve-lock max 1–4y.
- **Anchor**: Uniswap (survived zero-capture — no engine), Curve (ve model,
  survived Aug-2023 with a real fee anchor).
- **The one number**: **fees ÷ emissions** (>1 at maturity = a business;
  <1 forever = an S2 subsidy).

## 2. Lending / money market
- **Demand thesis**: spread between borrow and supply rates; the token captures
  a fee share and/or backstops bad debt (P6).
- **Killer anti-patterns**: S5 (redemption/withdrawal runs), S14 (manipulable-
  oracle leverage — Mango/Venus), S12 (looped collateral), S10 (contagion,
  key-person loans — CRV).
- **Go-to patterns**: P6 safety module (exogenous), P8 over-collateral +
  breakers, P10 Dutch liquidations, P13 collateral utility *with caps*.
- **Benchmarks**: LTV & borrow caps from the S14 math (manip cost > borrowable);
  liquidity coverage >1 for callable liabilities; loop unwind < 2%-depth.
- **Anchor**: Aave (survived 2022 cascades + absorbed CRV bad debt; caps +
  multi-oracle).
- **The one number**: **manipulation cost ÷ borrowable value** per listed
  collateral (>1 or don't list it).

## 3. Perp / derivatives DEX
- **Demand thesis**: fees from leverage traders → real yield in a hard asset
  (P2, GMX pays stakers in ETH). Token = fee claim + insurance backstop bond.
- **Killer anti-patterns**: S5 (LP/insurance run), S14 (mark-price oracle
  manipulation), S2 (trade-mining wash volume — dYdX v1 era, an S11 cousin).
- **Go-to patterns**: P2 fee-share in the fee asset, P6 insurance fund + auto-
  deleverage, P14 bond, OI caps tied to spot depth.
- **Benchmarks**: insurance fund vs max open risk; OI cap ÷ spot 2%-depth < a
  set fraction; reward *maker/paid* volume, never self-tradeable volume.
- **Anchor**: GMX (real ETH yield through the 2022–23 bear — decline later was a
  *business* problem, not a spiral).
- **The one number**: **insurance-fund coverage ÷ worst-case shortfall**.

## 4. Stablecoin
- **Demand thesis**: a unit-of-account/medium redeemable against exogenous,
  liquid reserves (P7 PSM). The token, if any, is a *backstop* (P5), never the
  peg mechanism.
- **Killer anti-patterns**: S6 (algo + own token — Terra/Iron), S1 (reflexive
  collateral), S5 (redemption run), S10 (reserve concentration — DAI/USDC 2023).
- **Go-to patterns**: P8 exogenous over-collateral + breakers, P7 PSM with
  coverage disclosure, P5 mint-to-recapitalize (direction: absorb loss, not
  defend peg), P9 PID for non-pegged units.
- **Benchmarks**: reserve ratio R with a breaker ladder (e.g. pause expansion
  <1.5, pro-rata <1.2, freeze/recap <1.0); zero native-token in the reserve path.
- **Anchor**: MakerDAO/DAI (exogenous collateral, MKR as backstop; survived
  Black Thursday + USDC de-peg). Anti-anchor: Terra.
- **The one number**: **exogenous reserve ÷ liabilities** (and it must not be
  reflexive).

## 5. L1 / L2
- **Demand thesis**: gas demand at any price (P1 usage burn) + a work-token
  security bond (P14). Zero-price: you pay gas to use the chain regardless.
- **Killer anti-patterns**: consensus security budget < value secured (Budish),
  S7 (VC/foundation unlocks — most 2024–25 L1s), S2 (inflation-funded staking
  yield masquerading as security), restaking rehypothecation (S10/S12).
- **Go-to patterns**: P1 EIP-1559 burn, P14 bond-and-slash, P12 streaming
  insider vesting, real fee-funded (not purely inflationary) security over time.
- **Benchmarks**: staking ratio + real fee revenue vs value secured; float >20%
  and year-1 unlocks <25% of float (S7); LST/validator concentration <⅓.
- **Anchor**: Ethereum (gas anchor + EIP-1559 sink; zero-price archetype).
- **The one number**: **cost to attack consensus ÷ value secured** (Budish, must
  hold persistently, including the bear).

## 6. GameFi / game economy
- **Demand thesis**: a spender class (net-external payers) buying fun/status;
  dual-currency segmentation (P16). See `circular-economy.md`.
- **Killer anti-patterns**: S3 (uncapped reward faucet), S15-shape (reward for
  activity nobody pays for), both currencies-as-investments (STEPN).
- **Go-to patterns**: P16 hard/soft split, consumption/status sinks, elastic
  sinks + seasons, EVE-style telemetry.
- **Benchmarks**: net-external-payer inflow ≥ extraction; dominant sink is
  consumption/status not growth; `sink ≥ faucet` through a *slowdown* (`sim3`).
- **Anchor**: mature F2P economies (hard/soft + whale spenders); the partial
  on-chain attempt is AXS/SLP (governance token protected, but no spender class →
  economy still collapsed).
- **The one number**: **net-external inflow ÷ extraction** (≥1 or it's S3).

## 7. DePIN / work network
- **Demand thesis**: real buyers rent the network's service; emissions bootstrap
  supply but are demand-gated. BME with `mint ≤ k·burn` (P14 + circular-economy).
- **Killer anti-patterns**: S15 (emissions pay hardware, no paid demand —
  Helium/Filecoin), S7 (token unlocks on top).
- **Go-to patterns**: demand-gated emissions, BME mint floor, work-bond +
  slashing (P14), utilisation-multiplier rewards.
- **Benchmarks**: service revenue ÷ emissions value ≥ ~0.5 (or clearly trending
  up); emissions responsive to utilisation, not flat.
- **Anchor**: none has fully cleared history yet — score the ratio, not the
  narrative (Helium's BME was sound; the ratio was fatal).
- **The one number**: **service revenue ÷ emissions value**.

## 8. Points / pre-token program
- **Demand thesis**: temporary bootstrap of *usage* (not parked capital), with a
  credible path to a token whose demand is organic by TGE. This is S11's
  minefield — the disciplined version is P15.
- **Killer anti-patterns**: S11 (rented TVL, snapshot cliff), S12 (leveraged
  points farming), the synchronized TGE = unlock + mercenary exit on one day.
- **Go-to patterns**: P15 (reward flow not stock, vest past TGE, publish organic
  baseline), airdrop size capped vs TGE float, season taper.
- **Benchmarks**: organic share (fee-paying usage ÷ total) >50% before TGE;
  airdrop ≤ a fraction of TGE float that demand can absorb; rewards vest months
  past TGE.
- **Anchor**: contrast — the Blast/points-cliff anti-example vs designs that
  vest airdrops and reward real usage (Pendle survived the 2024 LRT unwind on a
  real-fee anchor).
- **The one number**: **organic (fee-paying) share of TVL/usage** at snapshot.

---

## How to use
1. Find your archetype above → note its *one number* and killer anti-patterns.
2. Run the general `design-playbook.md` process; pull the listed
   `design-patterns.md` patterns.
3. Score with `scorecard.md` + the security panel; anchor your parameter choices
   against the named survivor in `survivors.md`.
4. If your design can't hit its *one number*, the archetype is telling you the
   token model is wrong — go back to playbook step 1 (necessity).
