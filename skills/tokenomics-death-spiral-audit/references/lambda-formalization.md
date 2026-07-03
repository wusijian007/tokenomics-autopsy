# Formalizing and Measuring λ

The skill's through-line is `λ`, the system gain of the price↔fundamentals
feedback loop: `λ<1` self-corrects, `λ>1` amplifies. This note makes λ precise
enough to (a) compute for multi-loop designs and (b) *estimate from data* — the
step that would turn "we assert this design is reflexive" into "we measured its
reflexivity." It is a methodology note, not a shipped scorecard row; the honest
caveats are as important as the math.

## 1. Scalar case (the intuition, made exact)

Take the discrete reflexivity map from the L2 analysis:

```
P(t+1) = P(t) · [1 + g(P, F)]          price responds to fundamentals
F(t+1) = F(t) · [1 + h(P)]             fundamentals respond back to price
```

Linearize around an equilibrium `(P*, F*)` and write the loop gain as the
product of the two sensitivities (in log terms, i.e. elasticities):

```
λ = (∂ ln F / ∂ ln P) · (∂ ln P / ∂ ln F)
      └── h′: reflexivity ──┘   └── g′: price's fundamentals-sensitivity ──┘
```

- `∂ ln F/∂ ln P` — the **reflexivity term**: how much "fundamentals" move when
  price moves. Healthy designs engineer this ≈ 0 (fees, gas, redemption claims
  don't care about token price). Death-spiral designs make it large and
  positive (collateral *is* the token; demand *is* an APY that quotes price;
  rewards depend on new buyers).
- `∂ ln P/∂ ln F` — how much price responds to fundamentals; always positive.

`|λ|<1` ⇒ perturbations decay (stable); `|λ|>1` ⇒ perturbations grow
(the spiral). The whole anti-pattern catalog is a catalog of design choices
that push the first term above zero.

## 2. Multi-loop case (why one number isn't enough)

Real designs have several coupled state variables — price, reserve ratio, TVL,
debt, staking ratio. Stack them in a state vector `x` and linearize the
one-period map `x(t+1) = M · x(t)` around equilibrium. `M` is the Jacobian; its
entries are the pairwise elasticities. Then:

```
stability ⇔ spectral radius ρ(M) = max|eigenvalue(M)| < 1
```

- `ρ(M) < 1`: all loops jointly damp → stable.
- `ρ(M) ≥ 1`: at least one eigen-combination amplifies → spiral. The dominant
  eigenvector tells you *which* coupled loop drives it (e.g., the
  price→reserve→redemption loop in Terra, not any single edge).

This is why the mechanism map (audit step 2) matters: each price-dependent edge
is a nonzero off-diagonal term, and it's their *joint* spectral radius —
not any single scary edge — that decides the regime. Two mild loops can
compound into `ρ>1`; one moderate loop with strong damping elsewhere may not.

**Worked sketch — Terra.** States: UST peg deviation, LUNA price, reserve ratio
R. Edges: de-peg → mint+sell LUNA (peg→−LUNA), LUNA price → R (LUNA→R),
R → redemption pressure → de-peg (R→peg). The product around that 3-cycle is
the loop gain; with a reflexive reserve it exceeds 1 near R≈1, which is exactly
the absorbing barrier `sim1` locates. The scorecard's engine rows are the edges
that make this cycle's gain exceed 1.

## 3. Estimating λ from data — the reflexivity beta

The ambitious step: stop asserting the reflexivity term and *estimate* it.

**Definition.** The **reflexivity beta** β_R is the elasticity of a
fundamental proxy to price, measured empirically:

```
Δ ln(Fundamental)_t = α + β_R · Δ ln(Price)_t + controls + ε_t
```

Fundamental proxies, by design type: TVL (lending/DEX), reserve ratio R
(stables), staking ratio (PoS/(3,3)), active users/volume (apps), collateral
value in loops (S12 designs). A large positive β_R is measured reflexivity;
β_R ≈ 0 is a decoupled (healthy) design.

**The hard part — endogeneity (why this is research, not a feature).**
Price and fundamentals are jointly driven by common shocks (a bull market lifts
both; a hack tanks both), so a naive regression *overstates* β_R. Mitigations,
in rough order of credibility:

1. **Event studies around exogenous shocks** — measure the fundamental's
   response to a price move the protocol didn't cause (a broad-market crash, an
   unrelated-exploit contagion day, a large exogenous liquidation). This is the
   cleanest read on "does *this* mechanism amplify an outside shock?"
2. **High-frequency identification** — within tight windows around a discrete
   price jump, common slow-moving fundamentals are held roughly fixed.
3. **Instrumental variables** — instrument token price with a basket of
   comparable tokens' returns (common crypto-beta) to isolate the exogenous
   component; imperfect, exclusion restriction is arguable.
4. **Regime/sign asymmetry** — reflexive designs amplify *down* moves more than
   *up* moves (the mechanism is forced to mint/liquidate on the way down);
   estimate β_R separately for negative vs positive returns. A large *downside*
   β_R is the death-spiral signature.

**What "good" looks like.** A survivor (ETH, DAI) should show β_R ≈ 0 or even
negative on the downside (arbitrage/redemption *stabilizes*). A live
death-spiral design should show a large positive downside β_R *before* it
collapses — the falsifiable, prospective claim. If measured β_R fails to lead
outcomes in the registry projects, the whole reflexivity framing needs revising
— and that is exactly the kind of test the validation layer is built for.

**Status & honesty.** This is a **research programme**, not a current scorecard
input (repo [ROADMAP](https://github.com/wusijian007/tokenomics-autopsy/blob/main/ROADMAP.md) §2.2, G-10). It requires clean panel data and defensible
identification; done badly it manufactures false precision. Done well it is the
instrument's most defensible differentiator: *measured* reflexivity, with error
bars, instead of asserted reflexivity. Until then, the scorecard's row-based
proxy for λ (engine flags) stands — it is coarser but robust, and it is what
the calibration and holdout actually validated.

## 4. How this maps to the rest of the skill

- **Engine rows (S1/S2/S5/S6/S9)** are the design choices that put a large
  positive term into the Jacobian → they push `ρ(M)` toward and past 1. That is
  why they carry the ×3 weight and act as the decision rule's first gate.
- **Structure rows** don't create the loop; they load the spring (supply
  overhang, rented capital) so that when something else trips `ρ>1`, the move
  is large. They bleed rather than run.
- **The zero-price anchor test** is the qualitative version of "is the
  reflexivity term zero?": if the token can go to zero and demand persists,
  `∂ ln F/∂ ln P ≈ 0` and no engine can form.
- **Simulations** are the nonlinear truth behind this linearization: `sim1`–`4`
  show the actual phase transition once `ρ` crosses 1; `sim7` (planned) shows a
  PID controller *engineering* `ρ<1` (RAI-style negative feedback).
