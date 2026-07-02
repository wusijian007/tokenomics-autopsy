# The Positive Pattern Library — Mechanisms That Work

The anti-pattern catalog (`anti-patterns.md`) tells a designer what *not* to
build. This is its constructive dual: a library of mechanisms that have
survived stress, each with the parameters that make it work, the failure modes
it introduces, and the anti-pattern it neutralizes. Composed with the
`design-playbook.md` process, this is the "architecture" half of the toolkit.

**How to read each entry** — mechanism → what it does → where it fits →
key parameters → *failure modes it introduces* (no mechanism is free) →
exemplars → which anti-pattern (Sx) it neutralizes.

**The meta-rule**: patterns are not modular Lego. Every one you add creates a
new edge in the mechanism map (`audit-protocol.md` step 2) and therefore a new
term in the reflexivity Jacobian (`lambda-formalization.md`). Compose, then
re-audit the *whole* — a fee-burn (P1) stacked on a ve-lock (P5) stacked on
collateral utility (P13) can quietly rebuild an S12 loop. Design is add-then-
re-score, never add-and-assume.

---

## Group A — Value capture (turn a token into a productive asset)

### P1 — Usage-tied fee burn (EIP-1559 class)
- **Does**: burns a fee denominated in the token, proportional to real usage →
  a supply sink that scales with demand, not with emissions.
- **Fits**: high-throughput protocols/chains with genuine transactional demand.
- **Parameters**: burn share of fees; base-fee vs priority split; whether the
  burn floats with congestion. Target: net issuance turns negative under load.
- **Failure modes introduced**: if usage is itself reflexive (fees paid only to
  farm the token), the "sink" is S3 in disguise; burn ≠ value if demand is fake.
- **Exemplars**: ETH (EIP-1559), BNB auto-burn.
- **Neutralizes**: S8 (velocity leak), partially S3 (binds a sink to usage).

### P2 — Fee-share to stakers (real yield)
- **Does**: routes a share of realized protocol fees to stakers → a cash-flow
  anchor that survives the token price falling (the payer is a paying user).
- **Fits**: revenue-positive protocols (DEXs, perps, lending).
- **Parameters**: % of fees shared; paid in the fee asset (ETH/USDC) vs the
  native token (native = weaker anchor, reintroduces reflexivity); lock to earn?
- **Failure modes**: paying yield from *emissions dressed as fees* is S2;
  securities-law surface; yield volatility with fee volatility.
- **Exemplars**: GMX (ETH to stakers), later Aave/MakerDAO revenue routing.
- **Neutralizes**: S2 (real vs subsidized), S8; passes the zero-price test.

### P3 — ve-lock + gauge + bribe market
- **Does**: vote-escrow locks tokens for boosted rewards + governance over
  emissions; gauges let lockers direct emissions; bribe markets let protocols
  pay for that direction → **emissions become a priced, market-cleared resource**
  instead of a flat subsidy.
- **Fits**: protocols that must allocate liquidity incentives (DEXs, stable
  AMMs).
- **Parameters**: max lock length; boost curve; emission budget under gauge
  control; whether bribes are native or exogenous.
- **Failure modes**: locked supply is future overhang; bribe markets are also
  the S13 governance-capture surface (Mochi); can devolve into mercenary
  gauge-farming (S11) if the underlying pool has no organic use.
- **Exemplars**: Curve veCRV/gauges, Balancer, the Votium bribe layer.
- **Neutralizes**: S2/S8 (aligns horizon, prices emissions) — *at the cost of*
  needing S13 discipline.

### P4 — Buyback-and-make / buyback-and-burn
- **Does**: uses treasury cash flow to buy the token and either burn it or add
  protocol-owned liquidity. Flexible, treasury-controlled value return.
- **Fits**: mature, profitable protocols with real free cash flow.
- **Parameters**: % of revenue; rules-based vs discretionary; burn vs POL.
- **Failure modes**: discretionary buybacks are a trust/timing load (buying the
  top); if funded by debt or reserves rather than profit, it's a disguised
  subsidy; can mask insider exit liquidity.
- **Exemplars**: various DEX/CEX token buybacks; treasury-funded POL programs.
- **Neutralizes**: S8; supports (never replaces) a real demand anchor.

## Group B — Stability & backstops (for pegs, deposits, claims)

### P5 — Backstop tranche (mint-to-recapitalize)
- **Does**: a junior token absorbs first losses; on a shortfall the system mints
  it to recapitalize — dilution lands on a *designated absorber*, by design.
- **Fits**: overcollateralized stablecoins, lending markets, insurance.
- **Parameters**: trigger, mint cap/rate, who gets diluted, governance path.
- **Failure modes**: **direction is everything** — mint-to-absorb-loss is a
  backstop (MKR); mint-to-defend-peg is the S6 engine (LUNA). Same tool, opposite
  wiring. An uncapped backstop on a reflexive asset is still S1/S6.
- **Exemplars**: MakerDAO MKR (Black Thursday recap), Aave's deficit mechanisms.
- **Neutralizes**: S5/S6 when collateral is exogenous (P8); validated in
  `survivors.md` (MKR).

### P6 — Safety module / insurance fund
- **Does**: a staked capital buffer, slashed to cover shortfalls, earning fees
  for the risk → aligns a capital cushion with the protocol's solvency.
- **Fits**: lending, perps, anything with tail credit risk.
- **Parameters**: fund size vs open risk; funded in what asset (native =
  reflexive cover that evaporates in the stress it's meant to cover); replenish
  path; auto-deleverage rules.
- **Failure modes**: native-token insurance is procyclical (S1) — the cover
  craters exactly when needed; undersized funds are theater.
- **Exemplars**: Aave Safety Module, dYdX/GMX insurance funds, perp
  auto-deleveraging.
- **Neutralizes**: S5/S10 (absorbs shortfall before it contages) — only if the
  fund is exogenous and sized to real tail risk.

### P7 — PSM with coverage disclosure
- **Does**: a peg-stability module lets the stable be minted/redeemed 1:1
  against a liquid exogenous reserve → hard arbitrage anchor for the peg.
- **Fits**: collateralized stablecoins.
- **Parameters**: reserve composition (liquidity, credit quality), coverage
  ratio published continuously, per-block mint/redeem caps, fee.
- **Failure modes**: imports the reserve asset's risk (DAI wobbled with USDC,
  Mar 2023 — an S10 concentration cost); a PSM backed by a *correlated* asset
  is S1.
- **Exemplars**: MakerDAO PSM, Frax's collateral ratio machinery.
- **Neutralizes**: S5/S6 (real redemption anchor); the honest face of "backing".

### P8 — Exogenous over-collateralization + circuit breakers
- **Does**: back liabilities with de-correlated assets at >100–150%, with
  *pre-specified* breakers (pause/partial-collateral/pro-rata at named
  thresholds).
- **Fits**: any peg or credit system.
- **Parameters**: collateral set + haircuts, coverage target, the breaker
  ladder (trigger → action → authority), oracle robustness.
- **Failure modes**: breakers invented mid-crisis are tweets, not mechanisms;
  over-collateral in a *correlated* asset is fake (S1).
- **Exemplars**: MakerDAO, Liquity (ETH-backed, algorithmic redemptions).
- **Neutralizes**: S1/S6 (the master antidote); pairs with the playbook step-5
  breaker spec.

### P9 — PID supply controller (engineered λ<1)
- **Does**: a controller adjusts a redemption rate / target to damp deviations —
  negative feedback that pushes back on moves instead of amplifying them. The
  literal opposite of a death spiral.
- **Fits**: non-pegged stable-ish units, reflexive-index designs.
- **Parameters**: the P/I/D gains, the controlled variable, update cadence,
  bounds.
- **Failure modes**: **stability ≠ adoption** — RAI proved you can engineer
  `λ<1` and still not get demand (a controller is not a reason to hold);
  mis-tuned gains oscillate; still needs a demand anchor from Group A.
- **Exemplars**: Reflexer RAI (the canonical case); see `sim7`.
- **Neutralizes**: the whole reflexivity family *dynamically* — the constructive
  mirror of λ (`lambda-formalization.md`).

### P10 — Dutch-auction liquidations
- **Does**: liquidates collateral via descending-price auctions rather than
  FCFS keeper races → orderly, competitive, front-running-resistant unwinds.
- **Fits**: any collateralized lending/CDP system, especially with S12 loops.
- **Parameters**: price decay curve, auction duration, keeper incentives,
  circuit breakers on cascading auctions.
- **Failure modes**: in a true liquidity vacuum even Dutch auctions clear low;
  parameters tuned for calm markets fail in a 2022-grade event.
- **Exemplars**: MakerDAO Liquidations 2.0, Aave v3.
- **Neutralizes**: S5 (kills the keeper-race first-mover advantage), dampens S12.

## Group C — Launch, supply & distribution

### P11 — LBP / batch-auction launches
- **Does**: price discovery via a declining-weight pool or uniform-clearing
  batch auction → sniping- and whale-resistant, honest opening price.
- **Fits**: token generation events wanting fair initial distribution.
- **Parameters**: starting/ending weights or auction window; per-address caps;
  anti-sybil.
- **Failure modes**: doesn't fix a bad *supply schedule* behind the launch
  (S7 lives in vesting, not the first hour); LBPs can still be gamed by informed
  bots.
- **Exemplars**: Balancer LBPs, Gnosis batch auctions.
- **Neutralizes**: partially S7 (honest initial price), S9 (reduces launch
  manipulation).

### P12 — Streaming + milestone vesting
- **Does**: continuous (per-block) vesting with no cliffs; insider unlocks gated
  on verifiable on-chain milestones where possible.
- **Fits**: every project with team/investor allocations.
- **Parameters**: stream rate, milestone definitions, the public machine-readable
  calendar (Axiom 6/10).
- **Failure modes**: streaming reduces cliff shock but not total overhang; if
  float is tiny, even a stream is a persistent bid-drain (still S7 by magnitude).
- **Exemplars**: Sablier/streaming-vesting-based cap tables.
- **Neutralizes**: S7 (removes synchronized cliff sell-dates; the lemon-market
  discount shrinks with transparency).

### P13 — Collateral utility with caps
- **Does**: real hold-demand from the token being usable as collateral — but
  with LTV and supply caps sized to manipulation cost and unwind depth.
- **Fits**: deep-liquidity assets only.
- **Parameters**: LTV, supply/borrow caps, oracle robustness, all derived from
  the S12/S14 math (unwind ≤ real depth; manip cost > borrowable value).
- **Failure modes**: this is the *doorway* to S12 and S14 — uncapped, it is the
  loop/oracle-attack surface itself. Only safe with caps.
- **Exemplars**: ETH as DeFi collateral (deep); the anti-example is any thin
  token listed uncapped.
- **Neutralizes**: S8 (adds structural demand) — *only if* S12/S14 caps hold.

### P14 — Work-token bond-and-slash
- **Does**: service providers post the token as a bond, slashed for misbehavior
  → demand scales with the work secured, and honesty is the best response.
- **Fits**: PoS validation, oracles, DePIN, keeper/relayer networks.
- **Parameters**: bond size vs value secured (Budish!), slashing conditions,
  unbonding period, insurance for honest faults.
- **Failure modes**: if the bond's value is reflexive to the token, security is
  procyclical (S1 at the consensus layer); rented/restaked bonds secure each
  system less (S10/S12); inflation-funded staking yield is S2 in a validator hat.
- **Exemplars**: PoS staking with slashing, Chainlink (soft), EigenLayer
  (restaking — with the rehypothecation caveat).
- **Neutralizes**: S8/S9 (real utility demand); implements economic-security
  Axiom 13 when the bond exceeds the value secured.

## Group D — Incentives & circular economies

### P15 — Points with organic-baseline netting + vesting
- **Does**: bootstrap incentives that (a) reward *flow* (fees paid, volume with
  spread) not *stock* (TVL parked), (b) vest past TGE, (c) publish an
  organic-baseline dashboard (what remains if points stop today).
- **Fits**: early-stage protocols needing a cold-start push.
- **Parameters**: reward-per-fee (not per-TVL); vest length; airdrop size vs TGE
  float; season taper.
- **Failure modes**: this is S11 done carefully — get any of the three wrong and
  it's just mercenary TVL with extra steps; escalating seasons re-inflate the
  cliff.
- **Exemplars**: designs that vest/lock airdrops and reward usage (contrast the
  Blast/points-cliff anti-example).
- **Neutralizes**: S11 (rented growth) — the disciplined version of a points
  program.

### P16 — Dual-currency segmentation (game/DePIN economies)
- **Does**: separate a *hard* currency (scarce, capped, tradable, investor-grade)
  from a *soft* currency (uncapped utility/reward, sinks locally, not the
  investment) → inflation lands on the soft currency by design, protecting the
  hard one; net-external payers (spenders) fund the loop.
- **Fits**: game economies, DePIN, any reward-driven circular economy.
- **Parameters**: sink design for the soft currency (elastic, consumption-based),
  the net-external-payer identity, telemetry (EIP-style faucet/sink reports).
- **Failure modes**: if *both* currencies are investment assets, you have two
  S3 faucets (STEPN GST+GMT both bled); soft-currency sinks tied to *new users*
  are S3 regardless of segmentation.
- **Exemplars**: mature F2P game economies (hard/soft split), AXS/SLP as the
  *partial* on-chain attempt (governance token protected, reward token bled —
  segmentation without a spender class).
- **Neutralizes**: S3 (shoves inflation onto the disposable currency) — *only*
  paired with the net-external-payer identity from `circular-economy.md`.

---

## Composition guide — which patterns answer which risk

| If your audit flags… | Reach for | But watch |
|---|---|---|
| S1/S6 reflexive backing | P7, P8 (exogenous collateral + breakers) | P5 direction (backstop, not peg engine) |
| S2 subsidized demand | P2 (real fee-share), P15 (disciplined points) | native-token yield is still S2 |
| S3 uncapped faucet | P1 (usage burn), P16 (dual-currency) | soft-currency sink must not need new users |
| S4 (3,3) fragility | P2 (revenue-funded yield), symmetrize exit | premium speculation |
| S5 bank run | P8/P10 (pro-rata/Dutch, breakers), P6 (insurance) | coverage must exceed instant liabilities |
| S7 float/FDV | P11 (fair launch), P12 (streaming vesting) | tiny float bleeds even when streamed |
| S8 velocity leak | P1, P2, P3, P13 | P3/P13 can rebuild loops/overhang |
| S11 mercenary TVL | P15 (flow rewards + vesting + baseline) | escalating seasons re-inflate the cliff |
| S12 recursive loops | P10 (Dutch liq), P13 caps | caps sized to *real* depth, not TVL |
| S13 governance capture | P14 (bonded stake), timelock+locks | bribe markets (P3) are the same surface |

The full design *process* that sequences these — necessity test through launch
checklist — is `design-playbook.md`; the survivor evidence base for each is
`survivors.md`.
