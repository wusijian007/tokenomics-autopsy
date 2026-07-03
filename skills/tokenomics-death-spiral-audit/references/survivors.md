# The Control Group — Why Survivors Survived

Studying only failures produces a biased instrument: half the checklist's
credibility comes from designs that **took the same class of stress and held**.
Each case below is a survivor of a severe, documented stress event, scored with
the same scorecard (`scorecard.md`), with the design property that carried it.

Format: stress event → why it held → which axiom it validates → score.

> Scores are order-of-magnitude, scored *at the stress point*. Survival ≠
> endorsement, and several of these carry real risks noted below.

---

## MakerDAO / DAI — Black Thursday 2020 & the USDC de-peg 2023 · score ≈ 1

- **Stress**: March 2020 — ETH −50% in a day, liquidation auctions briefly
  failed, ~$4M shortfall. March 2023 — USDC (a major PSM reserve) fell to
  ~$0.88; DAI wobbled with it.
- **Why it held**: collateral is **exogenous** to MKR (ETH, USDC, later RWA), so
  a DAI de-peg never mints DAI's own backing. The 2020 shortfall was closed by
  **minting MKR** — dilution landed on the governance token as a *backstop of
  last resort*, by design. Compare Terra: dilution landed on the reserve asset
  *as the peg mechanism itself*. Same tool (mint the second token), opposite
  wiring — backstop vs engine.
- **Validates**: Axioms 1, 2, 5. The 2023 episode also shows the residual risk:
  reserve concentration (S10) imports someone else's banking crisis.

## USDC — the SVB weekend, March 2023 · score ≈ 4

- **Stress**: $3.3B of reserves stuck in a failing bank; USDC traded to ~$0.88.
- **Why it held**: the claim was on **real, recoverable assets** — the de-peg
  was a 72-hour solvency question, answered when deposits were guaranteed.
  **The diagnostic**: a de-peg against exogenous collateral mean-reverts; a
  de-peg against reflexive collateral crosses an absorbing barrier and never
  comes back. What's on the other side of redemption decides which one you get.
- **Validates**: Axioms 1, 2. Residual: banking-rail contagion (S10 = 1),
  redemption gated on banking hours (S5 = 1 that weekend).

## Lido stETH — the June 2022 discount · score ≈ 6

- **Stress**: Celsius/3AC forced-unwound massive leveraged stETH loops; stETH
  traded 5–7% below ETH for weeks. Headlines said "de-peg".
- **Why it held**: two reasons, both structural. ① The claim was a hard 1:1
  claim on staked ETH — a real anchor that arbitrageurs eventually buy.
  ② Pre-Shanghai stETH had **no instant-redemption promise — so there was
  nothing to run**. A discount is a price; a run needs a first-mover advantage
  (S5). The *loops* were the S12 lesson: the leverage cascade around a sound
  asset nearly killed two lenders while the asset itself held.
- **Validates**: Axioms 1, 5 (corollary: the promise, not the illiquidity,
  creates the run), 12.

## BNB — FTX-contagion FUD 2022, SEC suit 2023 · score ≈ 4

- **Stress**: the FTT collapse made "exchange token as collateral" radioactive;
  regulatory action followed in 2023.
- **Why it held**: unlike FTT, BNB demand has non-reflexive legs — fee
  discounts, gas on its chain — and the burn ties supply to platform activity.
  Score honestly: partial S1 remains (used as collateral within its own
  ecosystem), which is why it scores 4, not 0.
- **Validates**: Axioms 7, 8 — and shows the difference between "exchange token
  with cash-flow anchor" and "exchange token as balance-sheet filler" (FTT).

## Ethereum ETH — every bear market · score ≈ 2

- **The base-case anchor**: gas demand exists at any price; EIP-1559 burns
  supply *proportional to usage* (a sink bound to consumption, Axiom 4); no
  yield promise, no redemption promise, no peg. `∂fundamentals/∂price ≈ 0` is
  the whole design. Residual: the LST/restaking loop ecosystem built on top of
  it (S12 = 1) — the risk lives in the loops, not the base asset.
- **Validates**: Axioms 1, 4, 8 — the zero-price test archetype.

## GMX — the 2022–23 bear · score ≈ 5

- **Stress**: launched into the worst DeFi bear; every subsidized competitor's
  token bled out.
- **Why it held**: staker yield was **paid in ETH from real trading fees** —
  demand that survives when the native token falls, because the payer is a
  trader who wants leverage, not an emissions schedule. Later fee decline hit
  the price — that's a *business* problem, not a spiral: decline and death
  spiral differ exactly by λ.
- **Validates**: Axioms 3, 7.

## Uniswap UNI — years of zero value capture · score ≈ 4

- **The S8 control**: UNI long had no fee share — a textbook velocity leak —
  yet never spiraled, because no mechanism forces selling when price falls
  (no engine; λ<1 even with weak capture). This is why S8 weighs ×1: value
  capture is a *performance* problem; engines are *survival* problems.
- **Validates**: the weighting itself.

## Curve CRV — the August 2023 near-cascade · score ≈ 11 (stressed survivor)

- **Stress**: an exploit crashed CRV while the founder had ~$100M borrowed
  against CRV across several lending markets — clustered liquidation points, a
  live S10+S12 test. Liquidation would have dumped a large share of float into
  thin depth.
- **Why it held (barely)**: OTC de-risking, lenders' risk parameters, and a
  real-usage anchor under the token (Curve's fees exist at any CRV price —
  passes the zero-price test). The 11-point score sits in the "elevated" band:
  partials and amplifiers, no engine at 2 — the instrument's prediction is
  "survivable but stress-prone", which is what happened.
- **Validates**: Axioms 8, 9 — and adds *key-person leverage* to the S10 red
  flags.

---

## Watch list (unresolved by history yet)

- **Levered funding-carry "stables"** (delta-neutral basis yield, e.g. the
  USDe class): yield depends on perp funding staying positive; marketed
  adjacency to "stable" invites S12 loops. Held through 2024–25 conditions;
  the real test is a *prolonged* negative-funding regime plus a redemption
  wave. Score the mechanism, not the track record.
- **Restaking / LRT loops**: points-driven TVL (S11) stacked on leverage
  (S12) stacked on a sound base asset — the stETH-2022 geometry with more
  layers. The April 2024 ezETH cascade was a small-scale preview.

These watch items are now **pre-registered with scores and falsifiable
predictions** in the research repo's prospective registry
([validation/prospective-registry.md](https://github.com/wusijian007/tokenomics-autopsy/blob/main/validation/prospective-registry.md),
frozen 2026-07-02, reviews 2027/2028) — along with further out-of-sample
survivor evidence (USDT's post-FTX $20B+ redemption wave, Frax's de-risking
pivot, rETH, Aave, AMPL, Pendle) in
[validation/holdout_backtest.py](https://github.com/wusijian007/tokenomics-autopsy/blob/main/validation/holdout_backtest.py).

---

## What separates survivors — four regularities

1. **A zero-price anchor.** Every survivor has demand that exists if the token
   price is zero (gas, fees, redemption claims). Every collapse in the case
   library fails this test somewhere.
2. **Dilution lands on the right token.** MKR mints to recapitalize DAI
   (backstop); AXS stayed up while SLP absorbed the inflation (cost shoved
   onto players); LUNA minted to defend UST (engine). The two-token pattern is
   neither good nor bad — *what matters is whether the minted token is the peg
   mechanism or the shock absorber.*
3. **No promise they can't fund.** Survivors either hold liquid coverage ≥
   liabilities (USDC, DAI/PSM) or never promise instant redemption at all
   (stETH pre-Shanghai, ETH). Collapses promise first and fund later.
4. **Supply tied to usage, not growth.** EIP-1559, BNB burns, GMX fee flow —
   sinks proportional to consumption. Collapses tie sinks to *new users* (S3)
   or nothing.

These four are the empirical face of Axiom 1: every one of them is a way of
keeping `∂fundamentals/∂price ≈ 0`.
