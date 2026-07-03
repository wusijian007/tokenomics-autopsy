# Roadmap & Frontier Gap Analysis — from Autopsy to Architecture

> Target end-state: **the crypto industry's reference instrument for evaluating
> token economies, and its reference toolkit for designing them.** This
> document is the research agenda that closes the distance: a frontier scan
> across six adjacent disciplines, a numbered gap register (G-1…G-22), new
> anti-pattern candidates under explicit discipline, and a sequenced v4→v6
> plan. Status: research agenda (nothing here ships without the calibration
> and versioning rules in §3).

---

## 0. What "industry-top" means, measurably

An instrument is not top-tier because its documents are long. Commit to
outcome definitions now, so progress is checkable:

**Evaluation instrument**
- E1. Discrimination holds on an *expanding* scored universe: grow from 33
  scored cases (18 calibration + 15 holdout) to **≥100**, publish AUC and a
  calibration curve, and let data — not the author — set the row weights.
- E2. The prospective registry survives **≥2 full review cycles** (2027, 2028)
  with public confusion tables and forced revisions on misses.
- E3. **Inter-rater reliability**: two independent scorers reach κ ≥ 0.7 on a
  blind case set — the instrument works in strangers' hands or it isn't an
  instrument.
- E4. A public **blind-spot register** and at least one survived **red-team
  challenge** ("design a token that passes the scorecard and still dies").
- E5. Third parties cite audits produced with it.

**Design toolkit**
- D1. Per-archetype playbooks (DEX / lending / perp / L1 / game / DePIN /
  stablecoin / restaking) each anchored to survivor benchmarks.
- D2. A **positive mechanism pattern library** — the constructive dual of the
  15 anti-patterns — with parameters and known failure modes per pattern.
- D3. A stress-runner: a machine-readable design spec in → Monte Carlo bear
  scenarios out → the playbook's step-9 verdict generated, not hand-assembled.
- D4. At least one real launch designed with the toolkit that later **passes
  its own 24-month registry review**.

## 1. Where the project stands (v3)

| Layer | Have | Grade vs end-state |
|---|---|---|
| Failure theory | λ>1 reflexivity + 4 game models | strong core, informal math |
| Anti-patterns | 12, tiered engine/structure/amplifier | best-in-class for *structural* failure |
| Measurement | 12-row scorecard, formulas + sources + thresholds | good; hand-set weights |
| Validation | in-sample 18, holdout 15 (rule 15/15), frozen registry | ahead of the field; small n |
| Audit workflow | quick screen + full protocol + report template | solid |
| Design guidance | 10-step playbook, benchmarks, one worked example | generic; no archetypes, no pattern library |
| Simulations | 4 didactic failure sims | all failure-side; none design-grade |
| Scope | tokenomics-structural only | **economic-security attacks unscored; value unassessed** |

## 2. Frontier scan by domain

### 2.1 Incentive economics

*Have:* S2 (subsidized demand), S11 (mercenary TVL), incentives-as-CAC math.

*Frontier and gaps:*

- **G-1 · Incentives are contracts, not budgets.** Principal–agent framing:
  the protocol (principal) buys services from LPs, validators, users, MMs
  (agents). Each reward rule should pass incentive-compatibility (is honest
  behavior the best response?) and individual-rationality checks under
  *adversarial* — not average — behavior. Today the playbook budgets
  incentives but never audits them as contracts.
- **G-2 · Goodhart taxonomy + sybil cost.** Every incentivized metric is a
  target and will be gamed: volume → wash trading, TVL → parking, users →
  sybils, uptime → phantom nodes. Needed: a red-team table per reward rule —
  *cheapest exploit path, cost to sybil, value delivered vs value paid* — as
  a standard audit artifact.
- **G-3 · Multitask crowding (Holmström–Milgrom).** Paying for the measurable
  (TVL) crowds out the unmeasurable (retention, security, honest governance).
  Predicts exactly the Blast/points pathology from first principles; deserves
  a design rule: never attach the strongest incentive to the most gameable
  metric.
- **G-4 · Behavioral layer.** Unit bias (low-priced tokens), endowment effect
  (airdrops feel like house money → instant dump), hyperbolic discounting
  (why cliffs get front-run and streaming vesting behaves better), and
  Abreu–Brunnermeier bubble-riding — rational actors knowingly ride doomed
  designs and plan to exit first; explains why "everyone knew OHM was a
  ponzi" changed nothing. Currently absent from the docs' actor model.
- **G-5 · Cohort accounting standard.** Incentive LTV/CAC per cohort,
  retention curves after each emissions cut, organic-baseline netting — the
  measurement standard behind S11's "organic share" number, so scorers stop
  eyeballing it.

*Deliverables:* `incentive-audit.md` reference (IC/IR checklist, Goodhart
red-team table, sybil-cost worksheet, cohort standard); playbook step-6
upgrade.

### 2.2 Market game theory & mechanism design

*Have:* Diamond–Dybvig, (3,3) PD, absorbing barrier, unlock lemon market.

*Frontier and gaps:*

- **G-6 · Launch mechanism selection.** The S7 float/FDV lemon problem is
  partly a *mechanism choice*: fixed-price lists vs LBPs vs batch auctions vs
  bonding curves differ in sniping resistance, sybil exposure, price
  discovery, and winner's curse. The design playbook currently prescribes
  float numbers but not the *mechanism* that produces honest initial prices.
- **G-7 · Fee, liquidation, and blockspace mechanisms.** EIP-1559 (analyzed
  by Roughgarden) is the canonical shipped mechanism: posted-price + burn,
  with known stability properties — it belongs in the pattern library.
  Liquidation design (Maker's Liquidations 2.0 Dutch auctions vs FCFS keeper
  races) determines whether liquidations are orderly or an S12 cascade
  amplifier. MEV structure (PBS, order-flow auctions) decides who captures
  the value the token system leaks.
- **G-8 · Governance games — a scoring blind spot.** Beanstalk (Apr 2022):
  a flash-loaned quorum passed a malicious proposal and drained ≈$180M in one
  block — *the code worked; the mechanism was the exploit*. Tornado Cash
  governance (2023), Build Finance's hostile takeover (2022), perennial
  vote-buying markets (Curve/Votium — which double as legitimate price
  discovery for emissions). The current scorecard cannot see any of this →
  S13 candidate (§3).
- **G-9 · Economic security budgets.** Budish's bound (cost of attack must
  exceed value secured, persistently) applied to PoS: staking ratio and real
  security spend vs value at stake; restaking as security *rehypothecation*
  (EigenLayer's attributable-security question); LST concentration
  (Lido-share debate) as a governance-liveness hazard; Chitra's
  staking-vs-lending competitive equilibria (DeFi yield competes capital away
  from consensus security). An L1/L2/restaking audit needs this module; the
  tool currently has nothing above the application layer.
- **G-10 · Formalize and *measure* λ.** Upgrade λ from heuristic to the
  spectral radius of the price↔fundamentals Jacobian (multi-loop designs get
  a loop-gain matrix). Then the ambitious empirical step: a **reflexivity
  beta** estimated from data (e.g., ΔTVL response to Δprice, event-study
  around exogenous shocks) — honest caveat: endogeneity is hard (common
  shocks drive both), so this is a research project with a methodology note,
  not a weekend feature. If it works, it is the instrument's most defensible
  differentiator: *measured* reflexivity instead of asserted reflexivity.

*Deliverables:* mechanism-selection matrix in the playbook;
`economic-security.md` module (cost-of-corruption ledger across
governance/oracle/consensus); λ formalization + estimation methodology note;
S13 candidate.

### 2.3 Liquidity market construction

*Have:* depth targets, POL-vs-rented, MM red flags, loop caps (playbook §7).

*Frontier and gaps:*

- **G-11 · LP profitability and LVR.** Loss-versus-rebalancing
  (Milionis–Moallemi–Roughgarden–Zhang) reframes AMM liquidity: LPs
  structurally lose to arbitrageurs unless fees > LVR. Audit consequence: if
  a token's pools are LP-unprofitable after arb flow, that liquidity is
  *rented by losses* and will leave — S11's cousin on the liquidity side.
  Needed metric: fee APR vs LVR + markout/toxic-flow estimate per major pool.
- **G-12 · Venue design space.** CPMM vs stableswap vs concentrated (v3) vs
  hooks/dynamic fees (v4) vs RFQ/intents (UniswapX-class) vs batch auctions —
  which venue architecture fits which asset profile (volatility, flow
  toxicity, depth budget). The playbook says "get depth"; it should say
  *which market structure buys the most honest depth per dollar*.
- **G-13 · MM agreements.** The standard loan+call-option deal, its
  incentive distortions (strike-adjacent price pinning, return-the-loan
  dumps), disclosure norms, and the self-dealing degenerate case (Alameda —
  S1/S10's CeFi face). Deserves a contract-level red-flag checklist with
  the loan-size-vs-float and strike-ladder numbers spelled out.
- **G-14 · Oracle-manipulation economics — a scoring blind spot.** Mango
  (Oct 2022, ≈$114M): pump a thin-liquidity token, borrow against the marked
  value — profit because *manipulation cost < extractable value*. This is a
  computable inequality (depth on oracle venues over the TWAP window vs
  borrowable value at inflated marks) and generalizes to every lending/perp
  listing of a thin asset, including key-person leverage (CRV wallets, S10).
  → S14 candidate (§3).
- **G-15 · Peg liquidity architecture.** PSM sizing, peg-defense budgets,
  redemption-arb loop capacity — the quantitative bridge between S5/S6
  theory and an actual stablecoin's order book.

*Deliverables:* `liquidity-engineering.md` reference; two new audit
sub-metrics (LP-profitability, manipulation-cost ratio); sim5 (LVR); S14
candidate.

### 2.4 Circular economies (games, DePIN, social)

*Have:* S3 faucet/sink, sim3, GameFi case anatomy.

*Frontier and gaps:*

- **G-16 · The net-external-payer constraint.** A closed token loop can only
  *redistribute* value; sustainable circular economies require external
  inflow ≥ external extraction. Axie died because every participant was a
  net extractor; healthy F2P economies run on a spender class (whales) who
  buy status/fun with no exit intent. This generalizes the zero-price test
  to whole economies and belongs in the playbook as an accounting identity:
  *name your net payers and what they buy that isn't exit-able*.
- **G-17 · Import the Web2 game-economy canon.** Virtual-economy design is a
  solved-er field than crypto admits: EVE Online (in-house economists,
  public monthly economic reports, deliberate sink engineering), WoW Token,
  RuneScape Bonds, dual-currency architectures (hard/soft currency
  segmentation), mudflation management via seasons and item decay
  (Castronova; Lehdonvirta & Castronova, *Virtual Economies*). The L2 doc
  cites none of it.
- **G-18 · Telemetry as a design deliverable.** An EVE-style monthly
  faucet/sink/stock report should be a *launch requirement* in the playbook's
  step 8 for any reward economy — sinks-vs-faucets is unmanageable unmeasured.
- **G-19 · DePIN burn-and-mint equilibrium.** Helium's HNT→Data-Credit BME is
  the most interesting post-2021 supply mechanism: demand burns the token at
  a fixed USD price, emissions pay supply-side hardware. Its historical
  weakness is measurable — service revenue tiny vs emissions value = a
  supply-side subsidy with no demand traction (S15 candidate, §3). The whole
  DePIN category (2024–26 wave) needs this one ratio audited: **service
  revenue / emissions value**.

*Deliverables:* `circular-economy.md` reference (net-payer identity,
dual-currency architecture, sink taxonomy with elasticities, telemetry
spec); EVE + Helium case studies; sim3 extension (spender-class parameter);
S15 candidate.

### 2.5 Monetary economics & valuation

*Have:* MV=PQ velocity critique; risk-only lens.

*Frontier and gaps:*

- **G-20 · Money-view vs equity-view regimes.** A token being priced as
  money (velocity, store-of-value premia, Gresham dynamics in dual-token
  systems) obeys different laws than one priced as equity (discounted fee
  claims). Misclassifying the regime produces wrong audits: reward tokens
  are *currencies* and die by Cagan-style hyperinflation; fee-share tokens
  are *equities* and die by dilution and multiple compression. The scorecard
  should ask "which regime?" before scoring S8.
- **G-21 · Negative-feedback supply policy.** RAI's PID-controlled
  redemption rate is the canonical *engineered λ<1* design — a stabilizer
  that pushes back instead of amplifying. It never scaled, which is itself
  instructive (stability without a demand engine ≠ adoption). Deserves a
  case study + a sim7 showing damping — every current sim shows failure;
  the library needs one that shows *health*.
- **G-22 · Valuation triangulation.** The instrument scores *survival* but
  says nothing about *price* — yet "top evaluation tool" users ask both.
  Add a valuation module: revenue multiples vs comparables, staking-yield
  DDM, dilution-adjusted forward supply (S7 numbers reused), fully-diluted
  vs float value bridges — output a **risk × valuation quadrant** (e.g.,
  "structurally sound but priced for perfection" vs "cheap but engine-flagged").
  Explicitly *not* investment advice; it disciplines the audit's context.

*Deliverables:* valuation module in `audit-protocol.md`; regime question in
scorecard preamble; RAI case study; sim7 (PID damping).

### 2.6 Cryptoeconomic security — the missing pillar

The scope statement excludes *contract exploits* (code bugs). But Beanstalk,
Mango, and Tornado governance were **economic** attacks: the code executed
exactly as written; the *mechanism* was mispriced. That is squarely inside a
"crypto-economic system design tool" and currently invisible to the scorecard.

Unifying framework — a **cost-of-corruption ledger**: for each control
surface (governance quorum, oracle, sequencer/consensus, liquidity), compute
`cost to corrupt` vs `value extractable`, under flash-loan and
borrowed-stake assumptions. Budish's bound, applied at every layer, not just
consensus. This one table would have flagged Beanstalk (corruption cost ≈
one block of flash-loan fees; prize ≈ $180M treasury) and Mango
(manipulation cost on thin books ≪ borrowable value) *pre-hoc*.

*Deliverables:* `economic-security.md` module + two scorecard candidates
(S13/S14 below) + audit-protocol step 7 upgrade (contagion map → control-
surface map).

## 3. New anti-pattern candidates — under explicit discipline

Instrument integrity rule (learned from v2→v3): **no new row ships** until it
has (a) ≥3 historical instances, (b) a 0/1/2 measurement procedure,
(c) re-run in-sample calibration *and* holdout with the expanded rows,
(d) a version bump + changelog. The frozen registry keeps being graded under
its frozen v2 rows; new rows apply to new freezes only.

| Cand. | Name | One-line tell | Candidate metric | Instances |
|---|---|---|---|---|
| S13 | Captureable governance | quorum is buyable/borrowable relative to treasury | cost-to-corrupt ÷ extractable value < 1; no timelock | Beanstalk '22, Build Finance '22, Tornado '23 |
| S14 | Manipulable-oracle leverage | thin token listed as collateral/perp with spot-derived oracle | manip cost over TWAP window ÷ borrowable value < 1 | Mango '22, several small-cap lending drains '21–23 |
| S15 | Supply-side subsidy mismatch (DePIN) | emissions pay hardware; demand never arrives | service revenue ÷ emissions value ≪ 1 persistently | Helium (early years), most 2024–26 DePIN |

S13/S14 sit at the boundary of "tokenomics" — include them because the
end-state is a *systems* tool, and because both are pure incentive failures,
not bugs.

## 4. The positive pattern library (the constructive dual)

The anti-pattern catalog tells designers what not to build; top-tier design
tooling needs the same rigor on the constructive side. Planned
`references/design-patterns.md` — each entry: mechanism → where it works →
parameters → failure modes → exemplars → which anti-pattern it neutralizes.

Initial 16: fee burn tied to usage (EIP-1559 class) · backstop tranche
(MKR-style mint-to-recapitalize) · safety module / insurance fund ·
PSM with coverage disclosure · ve-lock + gauge + bribe market (emissions
price discovery) · buyback-and-make (Smart-Burn class) · burn-and-mint
equilibrium (DePIN) · PID supply controller (RAI) · Dutch-auction
liquidations · LBP / batch-auction launches · streaming + milestone vesting ·
protocol-owned liquidity (post-Olympus, done soberly) · work-token
bond-and-slash · points with organic-baseline netting + vesting ·
retroactive funding · dual-currency segmentation (game economies).

## 5. Simulation & tooling roadmap

| Item | What it shows / does | Tier |
|---|---|---|
| sim5 LVR | fee APR vs LVR: when liquidity is rented-by-losses | v5 |
| sim6 governance capture | flash-loan quorum economics; timelock as circuit breaker | v4 |
| sim7 PID damping | the first *healthy* sim: engineered λ<1 absorbing shocks | v5 |
| sim3 ext. | spender-class parameter: net-external-payer identity live | v5 |
| stress-runner | `design.yaml` → parameterized sim suite → step-9 verdict auto-generated | v5 |
| ABM bridge | cadCAD/radCAD-style heterogeneous agents for design-grade Monte Carlo | v6 |
| data pipeline | DefiLlama/CoinGecko/Dune pulls auto-fill scorecard metrics (runway, sink/faucet, unlock/depth) | v6 |
| registry monitor | threshold alerts on frozen-registry projects | v6 |
| report generator | evidence table + report skeleton from pipeline output | v6 |

## 6. Validation roadmap — from expert instrument to statistical instrument

1. **Scored universe expansion**: 33 → 50 → 100+ cases with per-row
   justifications (community-contributable under CONTRIBUTING rules).
2. **Empirical weights**: at n≈80–100, fit logistic regression / simple
   ensemble on rows vs outcomes; publish AUC + calibration curve; compare
   hand weights (3/2/1) vs fitted — keep whichever wins out-of-sample,
   document the change.
3. **Inter-rater reliability**: blind double-scoring on a 15-case set;
   publish κ; tighten row procedures wherever raters diverge.
4. **Blind-spot register** (ship with v4): regulatory kill, key-person/legal,
   contract exploits, chain-level failure, pure market beta, fraud beyond
   S9's observables — what the instrument *cannot* see, stated as loudly as
   what it can.
5. **Red-team challenge**: standing invitation + template to design a token
   that passes the scorecard and still dies in simulation; every successful
   attack becomes a candidate row or a documented limitation.
6. **Registry cadence** (already frozen): grade 2027-07-02 / 2028-07-02;
   C4 forces revision on ≥2 misses.

## 7. Adoption — content alone doesn't make "industry-top"

- Publish periodic public audits of prominent live designs using the full
  protocol (the registry is the seed; make the reports the marketing).
- Offer the pre-launch design review (playbook step 9 + sign-off) to real
  teams; D4 requires at least one shipped design.
- Agent-native distribution: keep the skill pack the best-in-class agent
  skill for token audits (it already triggers on design/DD questions).
- Versioning discipline: semver the instrument (scorecard v2.0 = current
  frozen), changelog every row/weight change — credibility compounds through
  visible discipline, exactly like the freeze records.

## 8. Sequencing

| Version | Theme | Contents | Rationale |
|---|---|---|---|
| **v4** ✅ *(shipped)* | Evaluation depth | economic-security module + S13/S14/S15 with a back-scored cost-of-corruption ledger (`data/security_panel.py`, 8/8 attacks flagged pre-hoc); valuation module + regime question (audit step 9); blind-spot register; λ formalization note (`lambda-formalization.md`); sim6 governance capture | evaluation credibility compounds first; the security pillar is the largest hole |
| **v5** ✅ *(shipped)* | Design depth | `design-patterns.md` (16 positive mechanisms, the constructive dual); `archetype-playbooks.md` (8 verticals, each with a survivor anchor + the *one number*); `liquidity-engineering.md` (LVR/venues/MM/oracle-depth), `circular-economy.md` (net-payer identity/dual-currency/sinks/DePIN), `incentive-audit.md` (IC-IR/Goodhart/sybil/cohorts); sim5 (LVR) + sim7 (PID — the first *healthy* sim) | the constructive dual — turns the autopsy into architecture |
| **v6** ✅ *(shipped, partial)* | Product & scale | `tools/`: stress-runner (design.yaml → sims → step-9 verdict), report generator, κ machinery, registry monitor; scored universe → **53** + empirical weight fit (data agrees with hand weights); red-team program; sim8 spender-class. Deferred (need external inputs): live data pipeline, real κ study (needs 2 human raters), ABM bridge, scored universe → 100 | automation last: automate a validated instrument, not a draft |

### v6 shipped — what landed vs deferred

**Landed:** the product layer (`tools/README.md`) — `stress_runner.py`
(design.yaml → scored step-9 verdict, calls sim4/sim6; Terra-like spec →
42/54 REDESIGN), `report_generator.py` (audit JSON → full report),
`kappa_reliability.py` (weighted-κ machinery), `registry_monitor.py`
(pre-registered trigger checks). Validation scaling: `data/scored_universe.py`
(53 cases) + `data/fit_weights.py` (pure-numpy logistic + CV AUC; the fit
reproduces engine>structure>amplifier and flags S9/S12 recalibration signal,
frozen v2 retained). `validation/red-team.md` (standing challenge + seed
limitations). `sim8_spender_class.py` (net-external-payer identity — the D3/G-16
capstone). Closes/advances D3 (stress-runner), D2 report tooling, E1 (scored
universe grown), E2 (empirical weights machinery + first fit), E4 (red-team
program).

**Honestly deferred** (require inputs this environment can't fabricate): a live
DefiLlama/CoinGecko/Dune **data pipeline** (the monitor's data layer is a tested
stub); a real **inter-rater κ study** (needs two independent human scorers on a
blind set — the machinery is ready); the **ABM/cadCAD bridge** (needs a real ABM
framework to be worth shipping); **scored universe → 100** with independent
labels. These stay open items, tracked in `validation/README.md`.

### v5 shipped — what landed vs the gap register

Closed with the constructive work: **G-1…G-5** (incentive-audit: rewards as
contracts, Goodhart/sybil, multitask crowding, behavioural layer, cohort
accounting), **G-6/G-7** partial (mechanism-selection in archetype playbooks +
P10/P11 patterns), **G-11…G-13/G-15** (liquidity-engineering: LVR, venue design,
MM agreements, peg liquidity), **G-16…G-18** (circular-economy: net-payer
identity, dual-currency, sink taxonomy, EVE-style telemetry), **G-21**
(PID/sim7). Plus the positive pattern library (D2) and archetype playbooks (D1).
Deferred to v6: stress-runner (D3), ABM bridge, data pipeline, empirical weights
+ κ study + red-team + scored-universe expansion (the remaining validation and
automation items). Discipline held: scorecard still frozen at v2; the new design
docs add no scored rows.

### v4 shipped — what landed vs the gap register

Closed or opened: **G-9** (economic-security consensus note), **G-14**
(S14 oracle-manipulation math), **G-19** (S15 DePIN ratio), **G-8** (S13
governance), **G-10** (λ formalization + reflexivity-beta programme), **G-22**
(valuation module + regime split). Deferred to v5/v6 with the constructive
work: G-1…G-5 (incentive-audit), G-6/G-7 (mechanism selection, fee/liquidation
patterns), G-11…G-15 (liquidity-engineering), G-16…G-18 (circular-economy),
G-20/G-21 (money-regime patterns, PID/sim7). Discipline honored: the 54-point
scorecard stayed **frozen at v2**; S13–S15 report on a *separate* security
panel, so the prospective registry remains comparable. Scored-universe
expansion (→50→100) and empirical weights remain the biggest open validation
items, now scheduled in v6.

## 9. Reading anchors (why each matters here)

- Diamond & Dybvig 1983 — bank runs (in use, M1).
- Akerlof 1970 — lemon markets (in use, M4).
- Holmström & Milgrom 1991 — multitask incentives → G-3.
- Myerson 1981 / auction theory — launch mechanisms → G-6.
- Roughgarden 2020/21, *Transaction Fee Mechanism Design (EIP-1559)* → G-7.
- Budish 2018/2025, *The Economic Limits of Bitcoin/Blockchain* → G-9, §2.6.
- Milionis, Moallemi, Roughgarden, Zhang 2022, *LVR* → G-11.
- Chitra 2019, *Competitive Equilibria Between Staking and On-chain Lending* → G-9.
- Easley, López de Prado, O'Hara 2012, *VPIN / flow toxicity* → G-11.
- Abreu & Brunnermeier 2003, *Bubbles and Crashes* → G-4.
- De Long, Shleifer, Summers, Waldmann 1990, *Positive-feedback traders* → L2 §1 grounding.
- Minsky, *Financial Instability Hypothesis* — displacement→euphoria→Ponzi
  finance maps cleanly onto bull-masking and S2.
- Cagan 1956, *Hyperinflation dynamics* → G-20 (reward-token economies).
- Castronova 2005, *Synthetic Worlds*; Lehdonvirta & Castronova 2014,
  *Virtual Economies* → G-16…G-18.
- EVE Online monthly economic reports (CCP) — the telemetry gold standard → G-18.
- Reflexer/RAI documentation — PID supply control → G-21.
- Helium docs — burn-and-mint equilibrium → G-19.
- Soros, *Alchemy of Finance* — reflexivity (in use, L2 §1).

---

*This document is a research agenda, not shipped instrument behavior. The
scorecard remains at v2 (frozen 2026-07-02 with the registry) until the §3
discipline is satisfied for any change.*
