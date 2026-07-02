# Simulations — death-spiral phase transitions

Four minimal, calibrated models that *demonstrate* the mechanism behind each
collapse archetype. No heavy dependencies (numpy + matplotlib only).

```bash
python -m pip install -r requirements.txt
python run_all.py          # regenerate all charts into ./charts/
# or run one:
python sim1_algo_stable_absorbing_barrier.py
```

| Script | Archetype | Chart |
|---|---|---|
| `sim1_algo_stable_absorbing_barrier.py` | Algo-stable (Terra) | `charts/sim1_absorbing_barrier.png` |
| `sim2_olympus_33_unraveling.py` | (3,3) (OlympusDAO) | `charts/sim2_olympus_33.png` |
| `sim3_p2e_faucet_sink.py` | Play-to-Earn (Axie/STEPN) | `charts/sim3_p2e_faucet_sink.png` |
| `sim4_bank_run_diamond_dybvig.py` | Bank run (FTX/Celsius) | `charts/sim4_bank_run.png` |
| `sim5_lvr_rented_liquidity.py` | LVR — when AMM liquidity is rented by losses (S11's liquidity twin) | `charts/sim5_lvr.png` |
| `sim6_governance_capture.py` | Governance capture (Beanstalk) — S13, the timelock as circuit breaker | `charts/sim6_governance_capture.png` |
| `sim7_pid_damping.py` | PID supply control — the first *healthy* sim: engineering λ<1 (RAI) | `charts/sim7_pid_damping.png` |
| `sim8_spender_class.py` | Net-external-payer identity — a spender class saves a reward economy (circular-economy) | `charts/sim8_spender_class.png` |

> Six show a **failure** (λ>1); `sim7` and `sim8` are constructive — a
> negative-feedback controller that damps a would-be spiral (RAI-style), and a
> spender class (net-external payers) that lets a reward economy survive a
> growth stall.

`viz.py` holds the shared chart style. See
`../skills/tokenomics-death-spiral-audit/references/simulations.md` for how to
adapt each model to your own token design.

> These are didactic models: they reproduce the *qualitative* phase transition and
> the direction of each critical condition, not precise forecasts.
