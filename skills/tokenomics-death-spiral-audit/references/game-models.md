# The 4 Game-Theoretic Models

Behind 50+ collapses there are only **four** recurring game structures. Classify
any new design into one (or more) of these, then read off the failure mode and
the critical condition. Runnable, calibrated versions live in the research
repo's [`simulations/`](https://github.com/wusijian007/tokenomics-autopsy/tree/main/simulations)
folder — see `simulations.md` in these references.

---

## Model 1 — Bank Run (Diamond–Dybvig) → *sudden* collapse
**Where**: any platform promising instant, full, **first-come-first-served**
redemption against illiquid / maturity-mismatched assets (CeFi lenders,
exchanges, withdrawable yield protocols).

**Game**: the redemption game has **two pure-strategy Nash equilibria**:

| Equilibrium | Everyone | Outcome | Stability |
|---|---|---|---|
| Good | waits | protocol fine, all repaid | fragile (belief-held) |
| Bad | runs | assets fire-sold, latecomers ~0 | self-locking |

**Best response**: if you *believe* others will run, your dominant strategy is to
run **first** (positive first-mover advantage). So the bad equilibrium is
self-fulfilling — it needs no real deterioration, only a belief jump (a *sunspot*:
a leaked balance sheet, a tweet, a small de-peg).

**Critical condition**: liquidity coverage `L` < instantly-redeemable liabilities.
Below that, even zero initial panic tips into a run (see `sim4`).
**Antidote**: pro-rata haircuts (no FCFS) → removes first-mover advantage → run
basin collapses. Instances: FTX, Celsius, Voyager.

---

## Model 2 — (3,3) Coordination → *unravels to backing*
**Where**: bonding/treasury/rebase staking ("(3,3)") with very high APY.

**Game**: the marketed "(3,3): stake-stake is best" hides where payouts come from
(inflation + new bond capital). The real game is a prisoner's dilemma:

```
                 other STAKE         other SELL
 I STAKE     (nominal+, real depends   (I'm diluted,
              on new money)             they cash out)   ← I lose
 I SELL      (I cash out)              (stampede, premium→backing)
```

Your nominal balance grows with APY, but your **real share = your tokens / total
supply** is diluted. Staking only pays while **new-money inflow ≥ dilution**.
Backward induction: a "last buyer" exists → unravels from the end.

**Critical condition**: sustained new-money growth < dilution rate ⇒ premium
(`price / backing`) collapses to 1×. Note: it falls to **backing, not zero** (the
treasury floors it) — the key difference from algo-stables (see `sim2`).
**Antidote**: pay from real revenue; symmetrize exit; publish backing. Instances:
OHM and all forks.

---

## Model 3 — Seigniorage Absorbing Barrier → *to zero*
**Where**: dual-token mint/burn algorithmic stablecoins.

**Game/arbitrage**:
```
stable < $1:  burn 1 stable → mint $1 of reserve token (sell)   → contracts stable supply
stable > $1:  burn $1 reserve token → mint 1 stable             → expands stable supply
```
The peg holds in a bull market but the **downward** arc converts stable-coin
selling into reserve-token *minting + dumping*.

**Critical condition** — solvency ratio `R = M_reserve / S_stable`:
- Looks safe at `R ≫ 1` (Terra peaked ≈ 2.2).
- But `M_reserve` is **reflexive**: redemptions mint+dump it → price ↓ → `M ↓` →
  `R ↓` → more panic. This is `λ > 1`.
- `R < 1` is an **absorbing barrier**: past it, full redemption *cannot* happen
  without driving the reserve token to 0. Terra crossed it in ~72h (see `sim1`).

**Antidote**: reserve-ratio circuit breaker + partial collateral. Rate-limiting
mint only delays the run. The real fix: drop "algorithmic + own token". Instances:
Terra, Iron, Basis, ESD.

---

## Model 4 — Unlock / Inflation Supply Glut → *slow bleed*
**Where**: low-float / high-FDV launches; uncapped reward emissions.

**Game**: a multi-period game with **cost-basis asymmetry**:
```
marginal seller = insiders (VC/team), cost basis ≈ 0  → reservation price ≈ 0
marginal buyer  = retail, cost basis = market price   → needs narrative to bid
```
Every unlock injects ~zero-cost-basis supply. Add **information asymmetry**
(insiders know the real unlock calendar / treasury / retention; retail sees only
the chart) → an Akerlof lemon market. No sunspot, no coordination failure — just a
supply curve marching right on schedule.

**Critical condition**: `unlocks (next 12mo) / circulating` and `FDV / real
revenue` too high; `sink/faucet < 1` for reward emissions (see `sim3`).
**Antidote**: linear long unlocks (no cliffs), float matched to demand, milestone-
gated insider unlocks, public on-chain calendar. Instances: ICP, FIL, WLD, APE;
Axie/STEPN for the emission variant.

---

## Picking the model fast

| If the design… | Model | Failure shape | Watch |
|---|---|---|---|
| promises instant redemption of illiquid assets | 1 Bank run | sudden | belief shock |
| pays high APY from inflation/new bonds | 2 (3,3) | to backing | new-money growth |
| is a self-collateralized algo-stablecoin | 3 Absorbing barrier | to zero | reserve ratio R |
| has low float / uncapped emission | 4 Supply glut | slow bleed | unlock calendar |
| rents TVL with points → airdrop (S11) | 4 + 2 hybrid | cliff at TGE/snapshot | organic share, snapshot dates |
| stacks leverage loops on a derivative (S12) | 1 + 3 hybrid | liquidation cascade | unwind size ÷ market depth |

**Note on the 2023–26 variants.** The two newer anti-patterns are combinations,
not new games: a points program (S11) is Model 4's supply glut with Model 2's
new-money dependence, synchronized on a snapshot calendar; a recursive leverage
loop (S12) is Model 1's run played by liquidation bots, with Model 3's
absorbing-barrier geometry (unwind size vs real depth) deciding whether it
cascades. Classify them by their components and read off both watch metrics.
