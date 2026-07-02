# Validation Layer — Out-of-Sample Testing of the Scorecard

The calibration in `data/scorecard_calibration.py` is **in-sample**: it re-scores
the same cases the anti-patterns were distilled from. This layer tests the
instrument on evidence it has never seen, in two tiers of increasing rigor:

| Tier | What | File | Bias remaining |
|---|---|---|---|
| 1 | **Holdout backtest** — 15 historical cases never used in derivation, calibration, or any repo document | [`holdout_backtest.py`](holdout_backtest.py) | hindsight-scoring bias (mitigated, not eliminated) |
| 2 | **Prospective registry** — living projects scored and frozen *before* outcomes exist, with falsifiable predictions and fixed review dates | [`prospective-registry.md`](prospective-registry.md) | none (the gold standard; requires time) |

Supporting the tiers (v6 scaling work):

- **Scored universe** ([`data/scored_universe.py`](../data/scored_universe.py)) —
  the union of every scored case (18 calibration + 15 holdout + 20 new,
  documented, = **53**), with per-row justifications, for weight-fitting and
  reliability work. Community-contributable (see `CONTRIBUTING.md`).
- **Empirical weights** ([`data/fit_weights.py`](../data/fit_weights.py)) — a
  pure-numpy logistic fit on the 53 cases that asks whether a data-driven
  ranking agrees with the hand weights (3/2/1). It does, closely
  (§ "Empirical weights" below). The frozen v2 weights are **retained** — the
  fit is a transparency cross-check, not a silent re-weighting.
- **Red-team program** ([`red-team.md`](red-team.md)) — a standing challenge to
  break the instrument on purpose; every successful attack becomes a new row, a
  row fix, or a documented limitation.
- **Tools** ([`tools/`](../tools/README.md)) — the `registry_monitor.py` checks
  these frozen projects against their pre-registered triggers; `kappa_reliability.py`
  computes inter-rater κ (E3) once real independent score sheets exist.

---

## Outcome definitions (pre-registered, used by both tiers)

- **`spiral_collapse`** — an engine realized: permanent peg loss, reward-token
  hyperinflation, or a forced mint/dump/liquidation unwind; the token or claim
  ends ≤ −95% vs its mechanism baseline with no recovery ≥ 12 months.
- **`structural_bleed`** — ≥ −90% from cycle peak, sustained ≥ 6 months, driven
  by supply mechanics (unlocks, emissions, airdrop cliffs); the protocol may
  keep operating.
- **`survived_stress`** — a documented stress episode (run, de-peg, cascade,
  or ≥50% market-wide drawdown) with the mechanism intact afterward: peg
  restored within 30 days, redemptions honored, or the economy still
  functioning.
- Baselines: pegged assets are measured against the peg; others against both
  cycle ATH and TGE price (report both).

**What the instrument predicts** (from `scorecard.md` / `anti-patterns.md`):

1. Any **engine row at 2** → `spiral_collapse` risk class.
2. **Structure row(s) at 2, no engine** → shape is `structural_bleed` or
   violent deleveraging; final outcome decided by the **zero-price anchor
   test** (weak anchor → bleed; hard anchor → recoverable stress).
3. **No rows at 2** → no structural failure; market risk only.

The *weighted total* is an intensity gauge, not the classifier. A validation
run grades the **rule (1)–(3)**, and reports the totals for context.

## Tier 1 — Holdout backtest

### Leakage audit

Requirement: a holdout case must appear **nowhere** in this repository — not in
the case library (L1), the mechanism analysis (L2), the skill pack (L3), the
calibration set, or the survivors control group. Verified by full-repo text
search on 2026-07-02 (all 15 names below: zero matches before this layer was
added).

Selection also aims at **temporal holdout** where possible: Blur and Celestia's
declines realized in 2024–25, after the S1–S10 patterns were fixed from the
2009–2022 canon.

### Cases (8 collapses, 7 stress survivors)

Collapses: Neutrino USDN, Deus DEI, Tomb Finance, StrongBlock, Titano,
Solidly, Blur, Celestia.
Survivors: Tether USDT (post-FTX run), Frax (Terra contagion), Chainlink,
Rocket Pool rETH (June 2022 LST stress), Aave (2022 cascade), Ampleforth
(2020–21 rebase cycles), Pendle (2024 LRT points unwind).

Scoring rules: each row scored with the `scorecard.md` measurement procedure
using only information publicly available at the `score_asof` date (before the
outcome); per-case justifications live in the script/CSV so any scoring call
can be audited and challenged.

### Honesty — what Tier 1 can and cannot claim

It eliminates **derivation leakage** (the tool never saw these cases). It
cannot fully eliminate **hindsight bias**: the scorer knows the outcomes.
Mitigations: mechanical row procedures, pre-outcome information vintage,
published per-row justifications. The residual bias is exactly why Tier 2
exists.

### Result (run `python holdout_backtest.py`)

- Collapses total **12–25** (median 16); survivors **3–10** (median 5).
- **The total alone is a weak classifier out-of-sample**: 6 of 8 collapses and
  1 survivor (Frax, 10) land together in the 8–18 "elevated" band.
- **The engine → structure → anchor rule classifies 15/15 correctly**:
  - 6 collapses with an engine at 2 → `spiral_collapse` ✓ (USDN, DEI, TOMB,
    STRONG, TITANO, SOLID)
  - 2 collapses with structure-only flags + weak anchor → `structural_bleed` ✓
    (BLUR, TIA — mirroring ICP in-sample)
  - 7 survivors with no row at 2 → `survived_stress` ✓ (Frax at 10 points but
    all partials — the same "stressed survivor" geometry as CRV in-sample)
- Chart: `simulations/charts/data_holdout_separation.png`.

This is the instrument's strongest evidence to date: the *decision rule*
(not the raw score) generalizes to cases it never saw, and its known weak spot
(the elevated band) fails in the same, predicted way as in-sample.

## Tier 2 — Prospective registry

[`prospective-registry.md`](prospective-registry.md) freezes, as of
**2026-07-02**: scores, flags, band, and **falsifiable predictions** for living
projects, plus instrument-level success criteria. Review dates: 2027-07-02 and
2028-07-02.

Integrity rules:

1. **Append-only.** After the freeze, the registry is never edited — only
   dated entries in its Amendment Log (e.g., a materially wrong input, or a
   flag change from new unlock data).
2. **Timestamping.** Commit the frozen files to git and push; the commit hash
   + hosting timestamp are the proof of priority. Optionally anchor the file
   hash with OpenTimestamps (`ots stamp prospective-registry.md`).
3. **Grading.** At each review date, grade every prediction
   TRUE / FALSE / UNRESOLVED with evidence links, appended to the log.
   The confusion table grades the *instrument*; per criterion C4, two or more
   misclassifications at the 24-month review force a documented revision of
   the scorecard.
4. **No cherry-picking.** Projects cannot be silently dropped; a delisted or
   migrated token is graded against the outcome definitions as-is.

## Empirical weights — does the data agree with the hand weights?

`data/fit_weights.py` fits a logistic regression on the 53-case scored universe
(rows → failed/survived) and compares it to the hand-weighted (3/2/1) score.

Result: hand-weighted AUC ≈ **0.99**, 5-fold CV logistic AUC ≈ **1.00**; the
data-driven weight *ranking* reproduces engine > structure > amplifier. Two
honest, important caveats:

- **The near-perfect AUC is a consistency result, not a forward-accuracy claim.**
  The dataset is largely in-sample and single-author-labeled — the rows were
  used to assign the very outcomes being predicted, so high separation is
  expected almost by construction. The genuine forward test is the prospective
  registry (Tier 2), where nothing is known yet. Do **not** read "0.99 AUC" as
  "99% accurate at predicting the future."
- **The fit surfaces real recalibration signal**, not a rubber stamp: it wants
  to *raise* S9 (narrative-only almost always failed in the set) and *lower* S12
  standalone (loops appear in both survivors like stETH and collapses like
  Celsius — S12's value is in *combination*, which a linear model can't see).
  This is exactly the kind of finding a future v3 recalibration would weigh.

**Discipline:** the frozen v2 weights are **retained**. Fitted weights are a
published transparency cross-check and a *candidate* for a future re-frozen v3 —
adopted only if they beat the hand weights **out-of-sample** (registry review,
or a larger independent set), per ROADMAP §3. Chart:
`simulations/charts/data_weight_fit.png`.

Open validation items (v6+): grow the scored universe toward 100 with
independent labels; run a real inter-rater κ study (two humans, blind set,
`tools/kappa_reliability.py`); grade the registry at 2027-07-02 / 2028-07-02.

## Freeze record

SHA-256 of the artifacts frozen on **2026-07-02** (the git commit introducing
them is the authoritative timestamp; regenerating `holdout_backtest.csv` from
the unmodified script reproduces its hash):

```
FC427E58BA33BF3444482D8FE062BCAFE50EF13835CAA8E32868D57CD04CC28D  prospective-registry.md
8972022515BFA4CD87F687163CD40442A4621E1E3333D77EDB9DE12534C93B84  registry_scores.csv
447658F5CC62FEA62AF31AED7344A0D740A03CEF4556A1870FFA07DCF9DD7BE8  holdout_backtest.csv
```
