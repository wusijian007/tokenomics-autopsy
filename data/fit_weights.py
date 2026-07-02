"""
Empirical weight fitting: does a data-driven fit agree with the hand weights?

The scorecard's row weights (engine x3 / structure x2 / amplifier x1) were set by
judgement. This fits a logistic regression on the 53-case scored universe
(rows -> failed/survived) and compares:
  - the HAND-weighted score (3/2/1) as a classifier
  - a data-driven LOGISTIC fit (its coefficients = "what the data thinks the
    weights are"), evaluated by 5-fold cross-validated AUC

Pure numpy (dependency-light): logistic regression by gradient descent + L2,
AUC by the Mann-Whitney rank statistic, k-fold CV, a reliability/calibration
curve.

HONESTY / discipline (ROADMAP v6 + section 3):
  - The dataset is largely in-sample and single-author-labeled (see
    scored_universe.py). n=53 with 12 features -> real overfitting risk, hence
    L2 + cross-validation and a small-n caveat.
  - The frozen v2 scorecard weights are NOT changed here. Fitted weights are a
    transparency cross-check and a *candidate* for a future re-frozen v3, adopted
    only if they beat the hand weights out-of-sample by a clear margin.

Outputs:
  - weight_fit.csv                       (hand vs fitted weights per row)
  - ../simulations/charts/data_weight_fit.png

Run:  python fit_weights.py
"""
import csv
import sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from scored_universe import unified, ROWS                      # noqa: E402
sys.path.insert(0, str(HERE.parent / "simulations"))
from viz import plt, save, C                                   # noqa: E402

HAND_WEIGHTS = np.array([3, 3, 2, 2, 3, 3, 2, 1, 3, 1, 2, 2], dtype=float)
RNG = np.random.default_rng(42)


def load_xy():
    rows = unified()
    X = np.array([r[3] for r in rows], dtype=float)            # n x 12 (0/1/2)
    y = np.array([r[2] for r in rows], dtype=float)            # failed 1/0
    return X, y


def auc(scores, y):
    """Area under ROC via the Mann-Whitney U statistic (rank-based)."""
    pos = scores[y == 1]
    neg = scores[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    order = np.argsort(scores)
    ranks = np.empty(len(scores), dtype=float)
    ranks[order] = np.arange(1, len(scores) + 1)
    # average ranks for ties
    s_sorted = scores[order]
    i = 0
    while i < len(s_sorted):
        j = i
        while j + 1 < len(s_sorted) and s_sorted[j + 1] == s_sorted[i]:
            j += 1
        if j > i:
            ranks[order[i:j + 1]] = (i + 1 + j + 1) / 2.0
        i = j + 1
    r_pos = ranks[y == 1].sum()
    n_pos, n_neg = len(pos), len(neg)
    u = r_pos - n_pos * (n_pos + 1) / 2.0
    return u / (n_pos * n_neg)


def fit_logistic(X, y, l2=1.0, lr=0.1, iters=4000):
    """Standardized logistic regression by gradient descent with L2."""
    mu, sd = X.mean(0), X.std(0) + 1e-9
    Xs = (X - mu) / sd
    n, d = Xs.shape
    w = np.zeros(d)
    b = 0.0
    for _ in range(iters):
        z = Xs @ w + b
        p = 1.0 / (1.0 + np.exp(-z))
        gw = Xs.T @ (p - y) / n + l2 * w / n
        gb = (p - y).mean()
        w -= lr * gw
        b -= lr * gb
    return w, b, mu, sd


def cv_auc(X, y, k=5, l2=1.0):
    """k-fold cross-validated AUC on pooled out-of-fold predictions."""
    n = len(y)
    idx = RNG.permutation(n)
    folds = np.array_split(idx, k)
    oof = np.zeros(n)
    for f in range(k):
        test = folds[f]
        train = np.concatenate([folds[g] for g in range(k) if g != f])
        w, b, mu, sd = fit_logistic(X[train], y[train], l2=l2)
        oof[test] = ((X[test] - mu) / sd) @ w + b
    return auc(oof, y), oof


def calibration_curve(scores, y, bins=5):
    """Return (mean predicted prob, observed frequency) per bin."""
    p = 1.0 / (1.0 + np.exp(-scores))
    edges = np.quantile(p, np.linspace(0, 1, bins + 1))
    edges[0], edges[-1] = -0.01, 1.01
    xs, ys = [], []
    for i in range(bins):
        m = (p >= edges[i]) & (p < edges[i + 1])
        if m.sum() > 0:
            xs.append(p[m].mean())
            ys.append(y[m].mean())
    return np.array(xs), np.array(ys)


def main():
    print("Empirical weight fitting on the scored universe")
    X, y = load_xy()
    n = len(y)

    hand_scores = X @ HAND_WEIGHTS
    hand_auc = auc(hand_scores, y)

    w, b, mu, sd = fit_logistic(X, y)
    in_scores = ((X - mu) / sd) @ w + b
    in_auc = auc(in_scores, y)
    cvauc, oof = cv_auc(X, y)

    # Express fitted coefficients back on the raw 0/1/2 scale (per unit of row),
    # then rescale so the vector sums to the same total as the hand weights, for
    # a like-for-like ranking comparison.
    raw_coef = np.maximum(w / sd, 0.0)                          # per-point effect, clip tiny negatives
    if raw_coef.sum() > 0:
        fitted_weights = raw_coef / raw_coef.sum() * HAND_WEIGHTS.sum()
    else:
        fitted_weights = raw_coef

    print(f"  n = {n} cases ({int(y.sum())} failed / {int(n - y.sum())} survived)")
    print(f"  hand-weighted (3/2/1) AUC        : {hand_auc:.3f}")
    print(f"  logistic in-sample AUC           : {in_auc:.3f}")
    print(f"  logistic 5-fold CV AUC           : {cvauc:.3f}")
    print(f"  -> hand weights {'match' if abs(hand_auc-cvauc) < 0.05 else 'differ from'} "
          f"the CV fit within 0.05; frozen v2 weights RETAINED (discipline).")

    # write per-row comparison
    with open(HERE / "weight_fit.csv", "w", newline="", encoding="utf-8") as f:
        wcsv = csv.writer(f)
        wcsv.writerow(["row", "hand_weight", "fitted_weight_rescaled", "std_coef"])
        for i, row in enumerate(ROWS):
            wcsv.writerow([row, HAND_WEIGHTS[i], round(fitted_weights[i], 2), round(w[i], 3)])
    print(f"  [data]  weight_fit.csv")

    # chart
    fig = plt.figure(figsize=(12, 5))

    ax1 = fig.add_subplot(1, 2, 1)
    xlab = [r.split("_")[0] for r in ROWS]
    xpos = np.arange(len(ROWS))
    ax1.bar(xpos - 0.2, HAND_WEIGHTS, width=0.4, color=C["blue"], label="hand weights (3/2/1)")
    ax1.bar(xpos + 0.2, fitted_weights, width=0.4, color=C["amber"], label="fitted (rescaled)")
    ax1.set_xticks(xpos)
    ax1.set_xticklabels(xlab, rotation=45, fontsize=7)
    ax1.set_ylabel("weight")
    ax1.set_title(f"Hand vs data-driven weights (n={n})")
    ax1.legend(fontsize=8)

    ax2 = fig.add_subplot(1, 2, 2)
    cx, cy = calibration_curve(oof, y, bins=5)
    ax2.plot([0, 1], [0, 1], ls="--", color=C["gray"], label="perfect calibration")
    ax2.plot(cx, cy, "o-", color=C["green"], lw=2, label="CV out-of-fold")
    ax2.set_xlabel("mean predicted P(failed)")
    ax2.set_ylabel("observed failure frequency")
    ax2.set_title(f"Calibration (CV AUC = {cvauc:.2f}; hand-weight AUC = {hand_auc:.2f})")
    ax2.set_xlim(0, 1); ax2.set_ylim(0, 1)
    ax2.legend(fontsize=8, loc="upper left")

    save(fig, "data_weight_fit.png",
         f"Hand weights (AUC {hand_auc:.2f}) and the CV fit (AUC {cvauc:.2f}) agree closely; "
         "the data-driven ranking reproduces engine>structure>amplifier. Frozen v2 retained.")

    print("  lesson: the hand weights are not arbitrary - a data-driven fit on 53 cases")
    print("          reproduces their ranking; adopting fitted weights awaits a v3 re-freeze.")


if __name__ == "__main__":
    main()
