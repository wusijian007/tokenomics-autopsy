"""
Sim 8 — The net-external-payer identity: why a spender class saves an economy
================================================================================

Extends the sim3 faucet/sink framework with the circular-economy.md thesis: a
closed token loop only REDISTRIBUTES value; for a reward economy to survive a
growth stall it needs EXTERNAL inflow (spenders who put in real money to consume
status/fun, with no exit intent) >= EXTERNAL extraction (earners who cash out).

    net-external-payer identity:  spender_inflow  >=  earner_extraction

Axie died because nearly everyone was a net EXTRACTOR (play-to-earn-and-sell) --
the only inflow was new-entrant capital, so the economy was an S3 faucet the
moment growth stalled. A mature F2P economy runs on a spender class (whales
buying cosmetics/status) whose money funds the loop regardless of growth.

This sim runs the SAME growth stall under three regimes -- no spenders (Axie),
a weak spender class, a strong spender class -- and sweeps the spender/earner
inflow ratio to locate the break-even.

Run:  python sim8_spender_class.py
"""
import numpy as np
from viz import plt, save, C

STEPS = 300
STALL = 140          # growth stalls (new-entrant capital dries up) at this step


def simulate(spender_ratio, steps=STEPS,
             mint_per_earner=1.0,     # reward tokens minted/earner/step (faucet)
             sell_frac=0.85,          # share earners cash out (extraction)
             buy_per_new_usd=4.0,     # USD a new entrant spends to onboard (reflexive)
             p_ref=0.20):             # reference price anchoring spender USD budgets
    """spender_ratio = spender USD inflow as a multiple of earner token extraction
    valued at p_ref. Price CLEARS the market each step (USD demand / tokens sold),
    so it settles at the spender anchor instead of compounding to a bound.
    After the growth stall, entrant demand -> 0, so price -> spender_ratio * p_ref:
    the net-external-payer identity made mechanical."""
    earners = 5.0e5
    price = p_ref
    H = {"price": [], "earners": [], "ext": [], "spend": []}

    for t in range(steps):
        # Growth: strong before the stall, ~0 after (new-entrant capital dries up).
        if t < STALL:
            growth = 0.03 * (1.0 - earners / 8.0e6)
        else:
            growth = -0.005                       # mild attrition after the stall
        new = earners * growth
        earners = max(1.0e4, earners + new)

        # FAUCET: earners mint and sell (token supply hitting the market).
        mint = mint_per_earner * earners
        sell_tokens = sell_frac * mint

        # USD DEMAND, two sources (both defined in USD, independent of live price):
        #  (1) new-entrant onboarding spend -> growth-dependent (vanishes at stall)
        entrant_usd = buy_per_new_usd * max(new, 0.0)
        #  (2) spender consumption -> external, NOT growth-dependent (the anchor),
        #      a target multiple of the token extraction valued at p_ref.
        spender_usd = spender_ratio * sell_tokens * p_ref

        clearing = (entrant_usd + spender_usd) / max(sell_tokens, 1e-9)
        price = 0.8 * price + 0.2 * clearing      # smoothed market clearing
        price = float(np.clip(price, 0.001, 5.0))

        H["price"].append(price)
        H["earners"].append(earners)
        H["ext"].append(sell_tokens * price)
        H["spend"].append(spender_usd)
    return H


def main():
    print("Sim 8: net-external-payer identity (spender class saves the economy)")
    fig = plt.figure(figsize=(12, 5))

    # Panel 1: three regimes through the same growth stall.
    ax1 = fig.add_subplot(1, 2, 1)
    regimes = [
        ("No spenders (Axie: all extractors)", 0.0,  C["red"]),
        ("Weak spender class",                 0.5,  C["amber"]),
        ("Strong spender class",               1.2,  C["green"]),
    ]
    for label, ratio, color in regimes:
        H = simulate(ratio)
        ax1.plot(H["price"], color=color, lw=2, label=label)
    ax1.axvline(STALL, color=C["gray"], lw=1, ls=":")
    ax1.text(STALL + 3, 0.05, "growth stalls", fontsize=8, color=C["gray"])
    ax1.set_yscale("log")
    ax1.set_xlabel("step")
    ax1.set_ylabel("reward-token price ($, log)")
    ax1.set_title("Same growth stall: the spender class decides survival")
    ax1.legend(fontsize=8, loc="lower left")

    # Panel 2: sweep spender/extraction ratio -> final price (survival frontier).
    ax2 = fig.add_subplot(1, 2, 2)
    ratios = np.linspace(0.0, 1.6, 90)
    finals = [simulate(r)["price"][-1] / 0.20 * 100 for r in ratios]
    ax2.plot(ratios, finals, color=C["blue"], lw=2)
    ax2.axhline(100, color=C["ink"], lw=1, ls="--")
    ax2.axvline(1.0, color=C["green"], lw=1.2, ls=":")
    ax2.text(1.02, 20, "inflow = extraction\n(net-payer break-even)", fontsize=8, color=C["green"])
    ax2.fill_between(ratios, 0, 100, where=[r < 1.0 for r in ratios],
                     color=C["red"], alpha=0.05)
    ax2.set_xlabel("spender inflow / earner extraction")
    ax2.set_ylabel("final price (% of start)")
    ax2.set_title("Survival frontier: the net-external-payer identity")
    ax2.set_ylim(0, 160)

    save(fig, "sim8_spender_class.png",
         "A closed loop only redistributes: below spender-inflow = extraction the "
         "economy bleeds after the growth stall; above it, the spender class holds it up.")

    for label, ratio, _ in regimes:
        H = simulate(ratio)
        print(f"  {label:38s}: final price {H['price'][-1]/0.20*100:6.1f}% of start")
    print("  lesson: name your net-external payers (spenders with no exit intent) and what")
    print("          non-exit-able thing they buy; if the only inflow is new entrants, it is S3.")


if __name__ == "__main__":
    main()
