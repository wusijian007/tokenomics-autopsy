# Runnable Simulations

Eight calibrated, dependency-light models: six *demonstrate* the phase
transition behind a failure mode (λ>1), and two (`sim7` PID damping, `sim8`
spender-class) demonstrate the constructive side (engineered stability; a
survivable reward economy). Use them to (a) build intuition, (b) fit a critical
parameter to a specific design, or (c) generate charts for a report.

## Setup
```bash
cd simulations
python -m pip install -r requirements.txt   # numpy + matplotlib
python run_all.py                            # regenerate every chart into charts/
```
Each script is standalone and self-documenting: `python sim1_algo_stable_absorbing_barrier.py`.

## What each shows

| Script | Game model | Calibrated to | Headline result |
|---|---|---|---|
| `sim1_algo_stable_absorbing_barrier.py` | M3 Absorbing barrier | Terra (R₀≈2.2, UST $18B, LUNA $40B) | A 2.2× reserve tolerates only a ~14% run; the buffer is reflexive, not real. Phase diagram of the `R=1` absorbing barrier. |
| `sim2_olympus_33_unraveling.py` | M2 (3,3) | OHM (premium ≈13.8×, APY ~7000%) | Premium collapses to **backing, not zero** (−92%). Bifurcation: premium needs perpetual new money > dilution. |
| `sim3_p2e_faucet_sink.py` | M4 Inflation glut | Axie SLP (mint ≈4× burn) | Boom→saturation→bust; uncapped → ~0, capped (mint≤burn) survives the same demand shock. |
| `sim4_bank_run_diamond_dybvig.py` | M1 Bank run | FTX/Celsius | Sequential service: ~51% of scenarios self-fulfill a run; pro-rata: ~17% (only extreme panic). |
| `sim5_lvr_rented_liquidity.py` | S11 liquidity twin | AMM LPs | Fee APR vs LVR: below break-even the pool loses to arbitrage and only emissions keep LPs — "depth" rented by losses. Shows how emissions mask the loss until they stop. |
| `sim6_governance_capture.py` | S13 (security panel) | Beanstalk | No timelock: attack profitable across ~84% of the (treasury, quorum-cost) plane; a 7-day timelock flips it to ~7% by forcing hold-through-the-crash. The timelock is the cheapest circuit breaker. |
| `sim7_pid_damping.py` | P9 (healthy) | Reflexer RAI | A tuned PID controller turns a λ>1 unit into a damped one; over-tuning oscillates. Stability can be engineered — but it isn't demand. |
| `sim8_spender_class.py` | P16 / S3 (healthy) | Axie vs mature F2P | Same growth stall: with no spender class the reward economy cliffs (Axie); a spender class (net-external payers) whose inflow ≥ earner extraction holds price up. The net-external-payer identity made mechanical. |

## How to adapt to your design
- **Stablecoin**: set `sim1.simulate(R0=...)` to your reserve/liability ratio and
  `liq_frac` to your reserve token's real market depth; read off the critical run %.
- **Staking/(3,3)**: set `sim2` `dilution` to your rebase rate; the bifurcation's
  critical inflow = your dilution rate is the minimum sustainable new-money growth.
- **GameFi**: set `sim3` `sell_frac`, `buy_per_new`, `capacity` to your economy;
  toggle `capped=True` to test an emission-bound-to-sink policy.
- **Lending/exchange**: set `sim4` liquidity coverage `L`; compare sequential vs
  pro-rata to quantify how much a redemption-queue design shrinks your run basin.
- **Governance**: set `sim6` treasury/float ratio and quorum-cornering cost;
  read off the timelock length that flips your design from the profitable-attack
  region to safe. Pair with the security panel in `economic-security.md`.
- **DEX liquidity**: set `sim5` fee tier, daily volatility, and turnover; if fee
  APR < LVR APR your pool's depth is rented by losses (`liquidity-engineering.md`).
- **Engineered stability**: use `sim7` to tune a PID controller's gains for a
  reflexive unit; the stability map shows the damped region. Pair with
  design-pattern P9 — and remember stability ≠ demand.
- **Game/DePIN economy**: set `sim8` spender-inflow-to-extraction ratio; the
  survival frontier shows the net-external-payer break-even (`circular-economy.md`,
  P16). Below 1, the economy bleeds after a growth stall (S3).

## Modeling notes (honesty)
These are **minimal didactic models**, not forecasting tools. They reproduce the
*qualitative* phase transition and the *direction* of each critical condition;
absolute numbers depend on calibration. The point is structural: each model shows
that the failure is a property of the mechanism (`λ>1`), reachable from
realistic parameters, not an exogenous accident.

Charts are written to `simulations/charts/` and embedded in the analysis docs.
Chart text is in English to avoid CJK font issues across machines.
