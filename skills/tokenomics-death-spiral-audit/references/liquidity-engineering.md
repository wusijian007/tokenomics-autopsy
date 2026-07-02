# Liquidity Engineering

The design playbook (step 7) says "get depth ≥ the largest plausible single-day
net sell." This reference is the *how*: which market structure buys the most
honest depth per dollar, how to tell rented liquidity from real, and the
quantitative bridge between the S5/S6/S12/S14 theory and an actual order book.
Frontier grounding: LVR (Milionis–Moallemi–Roughgarden–Zhang), flow toxicity
(Easley–López de Prado–O'Hara / VPIN), and the oracle-manipulation economics of
`economic-security.md`.

## 1. The first question: is your liquidity rented by losses? (LVR)

Depth on a chart is not depth you can rely on. **Loss-versus-rebalancing (LVR)**
is the systematic loss an AMM LP takes to arbitrageurs who correct the pool
price to the market price after every external move. The LP is effectively
short volatility; arbitrageurs collect the difference.

```
LP net PnL ≈ fees earned − LVR − impermanent loss vs hold
LVR per unit time ≈ (½) · σ² · (price-sensitivity of the pool position)
```

**The audit consequence**: if `fee APR < LVR APR` for the main pools, LPs lose
money net of arb flow → that liquidity is **rented by losses** and leaves the
moment incentives stop. This is S11's twin on the liquidity side: TVL that
looks like depth but is really a subsidised short-vol position.

**Metrics to compute per major pool**:
- fee APR vs an LVR estimate (from realised σ and pool curvature);
- **markout** at 5s/1min/5min after trades against the pool — persistently
  negative markouts = the pool is picking up toxic (informed) flow and LPs are
  the exit liquidity;
- toxic-flow share (VPIN-style: fraction of volume that is informed/arb vs
  uninformed/retail).

If organic LPs can't profit, only mercenary (incentivised) LPs remain →
count that liquidity as temporary (playbook step 7) and expect it to vanish in
the stress you most need it.

## 2. Venue design space — which structure fits which asset

| Venue | Best for | Depth efficiency | Key risk |
|---|---|---|---|
| **CPMM (x·y=k)** | long-tail, cold-start, any pair | poor (depth spread across all prices) | high LVR, thin near-price depth |
| **Stableswap** | correlated assets (stables, LSTs) | excellent near peg | fails hard off-peg; hides de-peg until it breaks |
| **Concentrated (v3)** | major pairs, active LPs | high near range | LPs must manage ranges; depth vanishes on a gap move |
| **Dynamic-fee / hooks (v4)** | volatile or toxic-flow assets | high, fee adapts to volatility | complexity; hook risk |
| **RFQ / intents (UniswapX class)** | large size, pro market makers | very high (off-chain inventory) | MM dependence; centralisation of flow |
| **Batch auctions (CoW)** | MEV-sensitive, fair clearing | high, uniform price | latency; needs solver competition |

**Design rule**: match structure to the asset's *flow profile*.
- A **stable/LST** wants stableswap near peg **plus** an off-peg fallback (the
  Curve stETH pool masked the 2022 discount until it was large — see S12).
- A **volatile governance token** wants concentrated or dynamic-fee liquidity;
  a CPMM bleeds LPs to LVR and offers thin near-price depth exactly where you
  need it.
- **Large-size assets** (institutional) want RFQ/intents so a whale exit doesn't
  walk a thin AMM book (the S7 unlock-vs-depth problem).

Owned vs rented: seed the base with **protocol-owned liquidity** (POL — the
sober post-Olympus use); count incentivised (rented) liquidity as temporary and
LVR-exposed.

## 3. Market-maker agreements — the contract-level red flags

Most token MM deals are a **loan + call option**: the project lends the MM
tokens; the MM provides quotes and can buy the loaned tokens at a strike.
Incentive distortions to audit:

- **Strike-adjacent pinning**: the MM is incentivised to keep price near the
  strike, not near fair value.
- **Return-the-loan dump**: when the deal ends, the MM returns tokens by buying
  them (support) or the project must, but if the option is out-of-the-money the
  MM hands back tokens and the project eats the overhang.
- **Self-dealing degenerate case**: the MM *is* an affiliate (Alameda/FTT) →
  S1/S10 in CeFi clothing; "depth" is one related party.

**Checklist**: what fraction of depth is one/affiliated MM (cap it); loan size
vs float; the strike ladder; disclosure of MM token allocations; is quoting
obligation enforceable or best-effort. A few affiliated MMs providing most
liquidity is an S10 red flag regardless of how deep the book looks in calm
markets.

## 4. Oracle & peg liquidity — bridging to the attack surface

The security panel's S14 inequality is a *liquidity* fact: **manipulation cost =
depth on the oracle's venues over its observation window.** Liquidity
engineering therefore decides leverage safety:

- **Oracle venue depth**: an oracle is only as safe as the 2%-depth on the
  venues it reads, over its TWAP window. Thin venue + short window = cheap to
  move (S14 → Mango, Inverse, Moola).
- **Listing math**: LTV and borrow caps must satisfy `cost-to-move-oracle >
  borrowable-at-inflated-mark` (economic-security.md). This is a liquidity
  computation, not an asset-class judgement.
- **Peg liquidity architecture** (stablecoins): size the PSM and peg-defense
  budget against the largest plausible redemption wave; the redemption-arb loop
  can only hold the peg if arb depth ≥ the de-peg flow (the S5/S6 bridge). Publish
  the coverage ratio continuously (P7).

## 5. Depth vs the unlock/loop calendar (the S7/S12 bridge)

Turn the abstract "sufficient depth" into a dated inequality:

```
2%-slippage depth  ≥  max( largest unlock tranche,
                           largest single-holder position,
                           largest plausible loop unwind )
```

- **Unlocks (S7)**: next-4 unlock tranches ÷ average daily volume = "days of
  volume" the market must absorb; a cliff worth 38 days of volume is a
  months-long bleed.
- **Loops (S12)**: potential unwind ÷ 2%-depth; >1 means any trigger cascades
  (ezETH). Caps must be set so this stays <1 *before* listing.

If depth can't cover the calendar, **fix the calendar** (streaming vesting P12,
loop caps P13), don't hope for demand.

## 6. Design checklist (liquidity)

- [ ] Fee APR ≥ LVR APR on main pools (else liquidity is rented by losses)
- [ ] Markout/toxic-flow monitored; LPs are not systematic exit liquidity
- [ ] Venue structure matches the asset's flow profile (§2)
- [ ] POL seeds the base; rented liquidity counted as temporary
- [ ] No single/affiliated MM > capped share of depth; MM terms disclosed
- [ ] Oracle venue depth × window ⇒ manipulation cost > borrowable value (S14)
- [ ] 2%-depth ≥ max(unlock tranche, whale, loop unwind) (S7/S12)
- [ ] Peg: PSM/defense budget ≥ largest plausible redemption wave; coverage published

Simulations: `sim5_lvr.py` (fee-vs-LVR break-even — when liquidity is rented by
losses). Related: `economic-security.md` (S14), `design-patterns.md` (P7, P10,
P13), `audit-protocol.md` steps 6–8.
