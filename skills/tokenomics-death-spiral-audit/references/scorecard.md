# Death-Spiral Risk Scorecard (v2 — measurable)

Score each row **0 (absent) / 1 (partial) / 2 (clearly present)** using the
measurement procedure below — not gut feel. Multiply by the weight, sum.

- **Max weighted score = 54** (12 rows; engine ×3, structure ×2, amplifier ×1).
- Any **engine row (×3) scoring 2 is a red line** — fix it before anything else.
- Report **three outputs**, not one: ① weighted total, ② engine flags (×3 rows
  at 2), ③ structure flags (×2 rows at 2). The flags predict the *shape* of
  failure; the total predicts its *intensity*. See the decision rule in
  `anti-patterns.md`.
- If a metric can't be obtained, score it **pessimistically** and label the row
  `low-confidence` — opacity is itself a risk signal (Axiom 10).

## The 12 rows and how to measure each

| # | Red flag | Skill | Wt | How to measure (formula → 0 / 1 / 2) | Primary sources |
|---|---|---|---|---|---|
| 1 | Collateral/reserve correlated with native token | S1 | ×3 | share of reserves in native/affiliated assets. **0**: fully exogenous (USDC/ETH/T-bills). **1**: <30% native or correlated. **2**: ≥30% native/affiliated, or "A backs A" | reserve attestations, on-chain treasury, DefiLlama treasury |
| 2 | Core demand from subsidized APY, not revenue | S2 | ×3 | offered APY vs revenue per $ incentivized; runway = yield reserve ÷ net monthly subsidy. **0**: payout ≤ revenue. **1**: subsidy with runway >12 mo + published taper. **2**: payout > revenue and runway <12 mo, or >60% of demand in one pool | DefiLlama fees/revenue vs emissions, protocol docs, treasury |
| 3 | Uncapped reward faucet; sink needs new users | S3 | ×2 | sink/faucet = (burn+lock+real consumption) ÷ emission, monthly; and *who* funds the sink. **0**: mint ≤ burn or hard cap with low emission. **1**: cap exists but emission > organic sink. **2**: no cap and the sink clears only via new users | token contract, emissions schedule, Dune burn/mint dashboards |
| 4 | High APY from inflation; price ≫ backing | S4 | ×2 | premium = price ÷ backing (treasury RFV per token). **0**: no premium mechanics. **1**: premium 1–3× or partially inflation-funded yield. **2**: premium >3× and yield from mint/new bonds | treasury dashboard, supply schedule |
| 5 | Instant FCFS redemption vs illiquid assets | S5 | ×3 | liquidity coverage = liquid assets ÷ instantly-redeemable liabilities. **0**: ≥1, or queue/pro-rata design. **1**: 0.5–1, or partial gates. **2**: <0.5 with FCFS promise | reserve reports, on-chain balances, terms of service |
| 6 | Self-collateralized algo-stable, no breaker | S6 | ×3 | reserve ratio R = exogenous reserves ÷ stable supply; breaker existence. **0**: n/a or fully exogenous collateral. **1**: partial-algo with a working reserve breaker. **2**: algorithmic + own token, no breaker | protocol design docs, on-chain reserves |
| 7 | Low float / heavy unlocks | S7 | ×2 | float% at TGE; next-12-mo unlocks ÷ current float; FDV ÷ annualized real revenue. **0**: float >20% and 12-mo unlocks <25% of float. **1**: float 10–20% or unlocks 25–50%. **2**: float <10%, or unlocks >50%, or FDV/revenue >100× (no revenue → auto-2) | tokenomist/unlock trackers, CoinGecko supply data, vesting contracts |
| 8 | No value capture; high velocity | S8 | ×1 | existence of burn / fee-share / collateral utility; median holding time; earn-and-dump share. **0**: real capture. **1**: weak/indirect capture. **2**: none | token contract, docs, holder-duration dashboards |
| 9 | Narrative-only demand, concentrated, unlocked | S9 | ×3 | revenue = 0? top-10 non-custodial holders %; team/celebrity tokens locked? contract backdoors (mint/tax/blacklist)? **0**: real cash-flow demand. **1**: mostly narrative, but locked team + clean contract. **2**: zero revenue + concentrated + unlocked or backdoored | Etherscan/Solscan holders, Bubblemaps, contract review |
| 10 | Cross-protocol collateral/MM entanglement | S10 | ×1 | native token accepted as collateral elsewhere? affiliated MM share of depth? large loans against the token (incl. founder)? **0**: isolated. **1**: some links. **2**: deeply interlinked or key-person leverage | lending markets, DEX depth, on-chain loan positions |
| 11 | Mercenary points / rented TVL | S11 | ×2 | organic share = pre-points TVL (or fee-paying usage) ÷ total TVL; behavior at snapshots. **0**: >70% organic. **1**: 30–70%. **2**: <30% organic with a snapshot/TGE cliff | DefiLlama TVL history vs announcement dates, points-market pricing |
| 12 | Recursive leverage loops | S12 | ×2 | loop share of the derivative's float; potential unwind ÷ real DEX depth (2% slippage). **0**: negligible, or LTV/supply caps in place. **1**: material but capped. **2**: unwind > market depth, no caps | lending-market positions (Dune), DEX depth, risk dashboards |

## Verdict bands (max 54)

| Score | Verdict |
|---|---|
| 0–7 | Low *structural* death-spiral risk (market risk still applies). |
| 8–18 | Reflexive elements present; require explicit critical thresholds + circuit breakers; if a structure row = 2, expect bleed/deleveraging risk — run the zero-price anchor test. |
| 19–33 | High risk; one or more `λ>1` engines — hidden in a bull market, exposed in a bear. |
| ≥34 | Textbook death-spiral model; historical peers almost all went to ~0. |

Usage: for every row scored 2, jump to that anti-pattern's **antidote** in
`anti-patterns.md` and redesign. Prioritize engine (×3) rows. Then compute
**distance-to-threshold** for each triggered row (how many months of runway, how
far R is from 1, the exact unlock-wall dates) — the audit protocol
(`audit-protocol.md`, step 5) shows how.

## Security panel (separate axis — S13/S14/S15)

Spiral risk (reflexive dynamics) and **attack risk** (discrete exploits where
the code works but the mechanism is mispriced) are orthogonal. Score the three
economic-attack rows on a **separate panel** and report it beside the spiral
score — never summed into the 54 (the total is frozen at v2 for registry
comparability; see the repo [ROADMAP](https://github.com/wusijian007/tokenomics-autopsy/blob/main/ROADMAP.md) §3).

| Row | Skill | Metric (0 / 1 / 2) | Sources |
|---|---|---|---|
| Governance capture | S13 | cost-to-corrupt-quorum ÷ value at stake, under flash-loan/borrowed/rented-vote assumptions; timelock present? **0** cost ≫ value (locked votes + timelock). **1** partial/unverifiable. **2** quorum flash-loanable/borrowable/rentable below value at stake, or no effective timelock | governance contracts, lending-market borrowable float, bribe-market prices, timelock config |
| Oracle/leverage | S14 | cost-to-move-oracle over its window ÷ borrowable at the inflated mark. **0** no leverage vs token, or caps sized to manip cost. **1** thin-asset leverage, partial caps. **2** manip cost < borrowable value on any live venue | oracle config, DEX/CEX depth over the TWAP window, listing LTV + caps |
| Supply subsidy | S15 | service revenue ÷ emissions value (trailing, USD). **0** ≥0.5 or demand-gated. **1** 0.1–0.5, rising. **2** ≪0.1 persistently, emissions insensitive to utilization | protocol revenue dashboards, emissions schedule, DePIN usage metrics |

**Any 2 on S13/S14 = red line** — treat as already-exploited when sizing risk;
these are usually the *cheapest* fixes in the whole audit (a timelock, a cap, a
delisting). Full framework, instances, and antidotes: `economic-security.md`.
Back-scored calibration: [data/security_panel.py](https://github.com/wusijian007/tokenomics-autopsy/blob/main/data/security_panel.py) (research repo).

---

## Worked example — Terra (LUNA/UST), early 2022

| # | Red flag | Score | Weighted | Note |
|---|---|---|---|---|
| 1 | Reflexive collateral | 2 | 6 | UST "backed" by LUNA — perfectly reflexive |
| 2 | Subsidized APY demand | 2 | 6 | Anchor 19.5%, reserve depleting, ≈75% of UST |
| 3 | Uncapped reward faucet | 0 | 0 | n/a |
| 4 | Inflation premium | 1 | 2 | Anchor-driven, indirect |
| 5 | Instant FCFS redemption | 2 | 6 | Anchor instant withdrawals were the run vector |
| 6 | Algo-stable, no breaker | 2 | 6 | the core mechanism; no reserve-ratio breaker |
| 7 | Float/FDV asymmetry | 0 | 0 | n/a |
| 8 | Velocity leak | 0 | 0 | n/a |
| 9 | Narrative-only demand | 1 | 3 | "future of money" narrative amplified it |
| 10 | Contagion links | 2 | 2 | 3AC/Celsius/Voyager/FTX exposure |
| 11 | Mercenary TVL | 1 | 2 | Anchor TVL was rate-chasing capital |
| 12 | Recursive loops | 2 | 4 | Degenbox levered-UST loops (Abracadabra) |
| | **Total** | | **37 / 54** | **≥34 → textbook; 4 engine flags + 1 structure flag** |

Four engine red lines (rows 1, 2, 5, 6) fired simultaneously — the worst
recorded combination: reflexive collateral + subsidized demand + a bank-run
vector + a seigniorage absorbing barrier with no circuit breaker.

## Worked example — MakerDAO / DAI at the March 2023 USDC de-peg (control)

| # | Red flag | Score | Weighted | Note |
|---|---|---|---|---|
| 1 | Reflexive collateral | 0 | 0 | collateral is ETH/USDC/RWA — exogenous to MKR |
| 2 | Subsidized demand | 0 | 0 | DSR paid from real stability fees |
| 5 | FCFS redemption | 0 | 0 | overcollateralized; PSM backed 1:1 by liquid USDC |
| 6 | Algo-stable | 0 | 0 | not algorithmic; MKR dilution is a *backstop*, not a peg mechanism |
| 10 | Contagion | 1 | 1 | USDC concentration via PSM — DAI wobbled with USDC |
| — | all other rows | 0 | 0 | |
| | **Total** | | **1 / 54** | **0–7 → low structural risk; 0 engine flags** |

DAI de-pegged *with* USDC for ~72 hours and mean-reverted. The instrument
correctly separates this from Terra: the de-peg had exogenous, recoverable
collateral behind it, so `λ < 1` and the shock damped instead of amplifying.
Full control-group analysis: `survivors.md`.

---

## Calibration — does the instrument actually separate?

The scorecard was back-scored against **18 historical cases**: 10 collapses
(Terra, Iron, Basis, OHM, Wonderland, Axie/SLP, STEPN/GST, FTX, Celsius, ICP)
and 8 survivors of severe stress (DAI, USDC, stETH, BNB, ETH, GMX, UNI, CRV).
Scoring matrix + chart generator: [`data/scorecard_calibration.py`](https://github.com/wusijian007/tokenomics-autopsy/blob/main/data/scorecard_calibration.py);
chart: `simulations/charts/data_scorecard_separation.png`.

Results (in-sample, order-of-magnitude scoring):

- **Collapses score 12–37** (median ≈ 22); **survivors score 1–11** (median ≈ 4).
- **Engine flags separate perfectly in-sample**: 9 of 10 collapses have ≥1
  engine row at 2; **zero survivors do**. The remaining collapse (ICP) and the
  one survivor with a structure flag (stETH, S12 = 2) are both resolved by the
  second stage of the decision rule — the zero-price anchor test: ICP's anchor
  was weak → bleed; stETH's anchor was a hard 1:1 redemption claim → discount
  that mean-reverted. The *total score* alone does not separate (see next
  point); the rule engine→structure→anchor does.
- The two borderline cases are instructive, not embarrassing:
  - **ICP (12, collapsed)** — no engine, one structure flag (S7 = 2). Shape
    prediction: slow bleed, not run-to-zero. That is exactly what happened
    (−99% over years). Structure flags + a weak zero-price anchor → bleed.
  - **CRV (11, survived)** — no engine, no structure flag at 2; its 11 points
    come from partials and amplifiers (founder leverage, emissions). Shape
    prediction: survivable but stress-prone. August 2023 was the live-fire
    test: near-liquidation cascade, survived on a real-usage anchor.
- Honesty: this is **in-sample calibration** (the same record the patterns were
  distilled from). Its value is consistency — the instrument, applied
  mechanically, reproduces the historical outcomes without special pleading.

## Out-of-sample validation

The research repo's [`validation/`](https://github.com/wusijian007/tokenomics-autopsy/blob/main/validation/README.md) layer tests the
instrument on evidence it has never seen:

- **Holdout backtest** ([validation/holdout_backtest.py](https://github.com/wusijian007/tokenomics-autopsy/blob/main/validation/holdout_backtest.py)) — 15 historical
  cases (8 collapses, 7 stress survivors) that appear nowhere in this repo and
  were never used in derivation or calibration (leakage-audited). Result: the
  totals overlap in the 8–18 band, but the **engine → structure → anchor
  decision rule classifies 15/15 correctly** — including the two
  structure-only bleeds (Blur, Celestia) and the stressed survivor (Frax, 10).
  The known weak spot (total-only in the elevated band) fails out-of-sample in
  the same, predicted way as in-sample.
- **Prospective registry** ([validation/prospective-registry.md](https://github.com/wusijian007/tokenomics-autopsy/blob/main/validation/prospective-registry.md)) — living
  projects scored and frozen on 2026-07-02 with falsifiable predictions and
  fixed review dates (2027/2028). This is the bias-free tier: the registry
  grades the instrument in both directions, and two or more misclassifications
  at the 24-month review force a documented revision.

Treat fresh audits as hypotheses and re-score as data improves; the registry
is where those hypotheses get graded.
