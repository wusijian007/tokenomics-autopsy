"""
Sim 7 — PID supply control: engineering lambda < 1 (the first HEALTHY sim)
================================================================================

Every other simulation in this repo demonstrates a FAILURE (lambda > 1). This
one demonstrates the constructive opposite: a negative-feedback controller that
DAMPS deviations instead of amplifying them, the way Reflexer's RAI adjusts its
redemption rate to push the market back toward a moving target.

Setup: a reflexive unit whose price would, left alone, follow a positive-
feedback (lambda > 1) map -- a small deviation grows. We add a controller that
observes the deviation and adjusts an incentive (a redemption rate r) that
pushes demand the other way:

    deviation d(t)   = price - target
    controller       r(t) = Kp*d + Ki*integral(d) + Kd*d_dot        (PID)
    price update     reflexive push (+lambda*d)  MINUS  controller push (r)

With no controller the reflexive push wins and d(t) diverges. With a tuned PID
the loop gain becomes < 1 and d(t) decays back to zero -- engineered stability.
The sim also shows the failure of a MIS-TUNED controller (too much gain -> it
oscillates), because "add a controller" is not automatically "add stability".

Honest caveat (see lambda-formalization.md and design-patterns.md P9):
stability != adoption. RAI proved you can engineer lambda < 1 and still not
attract demand -- a controller is a stabilizer, not a reason to hold. It needs a
demand anchor from Group A of the pattern library.

Run:  python sim7_pid_damping.py
"""
import numpy as np
from viz import plt, save, C

STEPS = 120
LAMBDA = 1.08          # open-loop reflexive gain (>1 => would diverge)
SHOCK = 0.10           # initial 10% deviation from target


def simulate(Kp, Ki, Kd):
    d = np.zeros(STEPS)
    d[0] = SHOCK
    integral = 0.0
    prev = d[0]
    for t in range(1, STEPS):
        integral += d[t - 1]
        deriv = d[t - 1] - prev
        prev = d[t - 1]
        control = Kp * d[t - 1] + Ki * integral + Kd * deriv
        # reflexive push amplifies the deviation; controller pushes back
        d[t] = LAMBDA * d[t - 1] - control
        d[t] = np.clip(d[t], -1.0, 1.0)      # bounded market
    return d


def main():
    print("Sim 7: PID supply control - engineering lambda < 1 (the healthy sim)")
    fig = plt.figure(figsize=(12, 5))

    scenarios = [
        ("No controller (lambda=1.08)",      0.0,  0.0,   0.0,  C["red"]),
        ("Tuned PID (damped)",               0.30, 0.02,  0.10, C["green"]),
        ("Under-damped (low gain)",          0.12, 0.0,   0.0,  C["amber"]),
        ("Over-tuned (oscillates)",          1.90, 0.05,  0.0,  C["purple"]),
    ]

    ax1 = fig.add_subplot(1, 2, 1)
    for label, kp, ki, kd, color in scenarios:
        d = simulate(kp, ki, kd)
        ax1.plot(d * 100, color=color, lw=2, label=label)
    ax1.axhline(0, color=C["ink"], lw=1, ls="--")
    ax1.set_xlabel("time step")
    ax1.set_ylabel("deviation from target (%)")
    ax1.set_title("Same shock, different controllers")
    ax1.set_ylim(-12, 14)
    ax1.legend(fontsize=8)

    # Panel 2: stability map over (Kp, Ki) for fixed Kd -> final |deviation|
    ax2 = fig.add_subplot(1, 2, 2)
    kps = np.linspace(0.0, 1.2, 80)
    kis = np.linspace(0.0, 0.15, 80)
    grid = np.zeros((len(kis), len(kps)))
    for i, ki in enumerate(kis):
        for j, kp in enumerate(kps):
            d = simulate(kp, ki, 0.10)
            grid[i, j] = np.log10(abs(d[-10:]).mean() + 1e-6)
    im = ax2.imshow(grid, origin="lower", aspect="auto", cmap="RdYlGn_r",
                    extent=[kps[0], kps[-1], kis[0], kis[-1]], vmin=-4, vmax=0)
    ax2.set_xlabel("proportional gain Kp")
    ax2.set_ylabel("integral gain Ki")
    ax2.set_title("Stability map (green = damped, red = still deviating)")
    ax2.grid(False)
    fig.colorbar(im, ax=ax2, fraction=0.046, pad=0.04, label="log10 residual deviation")

    save(fig, "sim7_pid_damping.png",
         "A tuned PID turns a lambda>1 unit into a damped one; too much gain "
         "oscillates. Stability can be engineered - but it is not demand (RAI).")

    tuned = simulate(0.30, 0.02, 0.10)
    none = simulate(0.0, 0.0, 0.0)
    print(f"  no controller: deviation {SHOCK*100:.0f}% -> {none[-1]*100:.0f}% (diverged, clipped)")
    print(f"  tuned PID    : deviation {SHOCK*100:.0f}% -> {tuned[-1]*100:.2f}% (damped to target)")
    print("  lesson: negative feedback engineers lambda<1 (RAI's redemption-rate control);")
    print("          but stability != adoption -- a controller still needs a demand anchor.")


if __name__ == "__main__":
    main()
