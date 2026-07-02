"""
Sim 5 — Loss-versus-rebalancing (LVR): when AMM liquidity is rented by losses
================================================================================

Supports the liquidity-engineering reference and failure Skill #11's liquidity
twin. An AMM LP is structurally short volatility: after every external price
move, arbitrageurs rebalance the pool to the market price and pocket the
difference. That loss is LOSS-VERSUS-REBALANCING (Milionis-Moallemi-Roughgarden-
Zhang, 2022). The LP is profitable only if:

    fee income  >  LVR

For a CPMM (x*y=k) tracking a lognormal price with volatility sigma, the
instantaneous LVR rate is approximately

    LVR_rate ~= (1/8) * sigma^2        (per unit time, as a fraction of pool value)

and fee income per unit time ~= fee_bps * turnover_rate. When fees < LVR, the
only LPs who stay are those paid emissions to do so -> the "depth" is RENTED BY
LOSSES and evaporates the moment incentives stop (the S11 pathology on the
liquidity side).

This sim sweeps (volatility, fee tier) -> LP net APR, and marks the break-even
frontier. It also shows how emissions can MASK an LVR loss (apparent APR) until
they stop.

Run:  python sim5_lvr_rented_liquidity.py
"""
import numpy as np
from viz import plt, save, C

DAYS = 365


def lvr_apr(sigma_daily):
    """Annualized LVR as a fraction of pool value, CPMM approximation.
    sigma_daily is daily volatility; (1/8) sigma^2 per unit time, annualized."""
    sigma_annual = sigma_daily * np.sqrt(DAYS)
    return 0.125 * sigma_annual ** 2


def fee_apr(fee_bps, daily_turnover):
    """Annualized fee income as a fraction of pool value.
    daily_turnover = daily volume / pool value (the pool's capital efficiency)."""
    return (fee_bps / 1e4) * daily_turnover * DAYS


def sweep():
    sigmas = np.linspace(0.01, 0.10, 80)        # 1%..10% daily vol
    fees = np.array([5, 30, 100])               # 0.05%, 0.30%, 1.00% tiers (bps)
    turnover = 0.5                              # daily volume = 0.5x pool value
    return sigmas, fees, turnover


def main():
    print("Sim 5: LVR - when AMM liquidity is rented by losses")
    sigmas, fees, turnover = sweep()

    fig = plt.figure(figsize=(12, 5))

    # Panel 1: net LP APR = fee_apr - lvr_apr, per fee tier vs volatility
    ax1 = fig.add_subplot(1, 2, 1)
    lvr = np.array([lvr_apr(s) for s in sigmas])
    for fee_bps, color in zip(fees, [C["red"], C["amber"], C["green"]]):
        net = fee_apr(fee_bps, turnover) - lvr
        ax1.plot(sigmas * 100, net * 100, color=color, lw=2,
                 label=f"{fee_bps/100:.2f}% fee tier")
    ax1.axhline(0, color=C["ink"], lw=1, ls="--")
    ax1.fill_between(sigmas * 100, -60, 0, color=C["red"], alpha=0.06)
    ax1.text(6.5, -45, "LP loses to arb\n(rented-by-losses)", fontsize=8, color=C["red"])
    ax1.set_xlabel("daily volatility (%)")
    ax1.set_ylabel("LP net APR (%)  =  fees - LVR")
    ax1.set_title("Fee income vs LVR: the break-even by fee tier")
    ax1.set_ylim(-60, 60)
    ax1.legend(fontsize=8)

    # Panel 2: emissions masking. A thin-fee (0.05%) pool at 6% daily vol loses
    # to LVR; an emissions APR makes the *apparent* APR positive until it stops.
    ax2 = fig.add_subplot(1, 2, 2)
    sigma0 = 0.06
    base_net = fee_apr(5, turnover) - lvr_apr(sigma0)    # 0.05% tier -> negative
    emissions = np.linspace(0, 0.4, 80)                  # 0..40% emissions APR
    apparent = base_net + emissions
    ax2.plot(emissions * 100, apparent * 100, color=C["blue"], lw=2, label="apparent APR (fees - LVR + emissions)")
    ax2.axhline(base_net * 100, color=C["red"], lw=2, ls="--",
                label=f"true APR (fees - LVR) = {base_net*100:.0f}%")
    ax2.axhline(0, color=C["ink"], lw=1)
    # the emissions needed just to break even
    be = -base_net
    ax2.axvline(be * 100, color=C["gray"], lw=1, ls=":")
    ax2.text(be * 100 + 1, 20, f"emissions needed\njust to break even\n= {be*100:.0f}% APR",
             fontsize=8, color=C["gray"])
    ax2.set_xlabel("emissions APR paid to LPs (%)")
    ax2.set_ylabel("APR (%)")
    ax2.set_title("Emissions mask the LVR loss (0.05% pool, 6% daily vol)")
    ax2.legend(fontsize=8, loc="upper left")

    save(fig, "sim5_lvr.png",
         "Below break-even, only emissions keep LPs -> liquidity is rented by losses "
         "and leaves when incentives stop (S11's liquidity twin).")

    # Quantify the headline
    print(f"  LVR at 2%/4%/6% daily vol: "
          f"{lvr_apr(0.02)*100:.0f}% / {lvr_apr(0.04)*100:.0f}% / {lvr_apr(0.06)*100:.0f}% APR")
    for fee_bps in fees:
        # break-even daily vol where fee_apr == lvr_apr
        f = fee_apr(fee_bps, turnover)
        be_sigma = np.sqrt(f / 0.125) / np.sqrt(DAYS)
        print(f"  {fee_bps/100:.2f}% fee tier (0.5x daily turnover): "
              f"break-even at ~{be_sigma*100:.1f}% daily vol")
    print("  lesson: if fee APR < LVR APR, the pool's depth is rented by losses;")
    print("          emissions can hide it, but the liquidity leaves when they stop.")


if __name__ == "__main__":
    main()
