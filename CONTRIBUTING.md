# Contributing to tokenomics-autopsy

Thanks for helping make this a better design reference for the whole ecosystem.
Contributions of all sizes are welcome — a one-line correction is as valuable as a
new game-theoretic model.

> 中文贡献者:欢迎用中文提 issue / PR;英文是开源主语言,新增内容请尽量同时更新
> 中英两个版本(若只会一种语言也没关系,维护者会帮忙补另一版)。

## What you can contribute

- **New cases** — a notable collapse that fits the scope (see below), with sources.
- **Corrections** — wrong figures, dates, mislabeled mechanisms, dead links.
- **New / improved simulations** — better calibration, a new archetype, cleaner code.
- **New antidotes or design axioms** — battle-tested fixes for an anti-pattern.
- **Survivor / control cases** — stress events a design *survived*, mapped to the
  axioms that carried it (`skills/.../references/survivors.md`), and back-scored
  in `data/scorecard_calibration.py`.
- **Validation** — new *leakage-audited* holdout cases for
  `validation/holdout_backtest.py` (the case must appear nowhere else in the
  repo), and **grading the prospective registry** at its review dates
  (2027-07-02 / 2028-07-02) per the append-only rules in `validation/README.md`.
  Challenges to any individual row score are welcome — that is what the
  published per-row justifications are for.
- **Scored universe** — add well-documented cases (with per-row justifications)
  to `data/scored_universe.py` to grow the set toward 100 and improve the
  empirical weight fit. Independent (non-author) labels are especially valuable.
- **Red-team** — try to break the instrument: a design that passes the scorecard
  and still dies, or one it wrongly condemns. See `validation/red-team.md`;
  every successful attack becomes a new row, a row fix, or a documented limit.
- **Tools** — improvements to `tools/` (stress-runner spec coverage, report
  templates, wiring the registry monitor's data layer to live feeds).
- **Translations** — keeping the EN ⇄ ZH documents in sync.
- **Data** — improving `data/case_dataset.py` / `data/scorecard_calibration.py`
  with better-sourced estimates.

## Scope & principles

This repo is about **structural / mechanistic failure** on two axes:
**spiral risk** (death spirals: reflexive collateral, subsidized demand, uncapped
emission, bank runs, absorbing barriers, unlock gluts…) and **economic-attack
risk** (governance capture, oracle-manipulation leverage, supply-subsidy
mismatch — where the code works and the *mechanism* is mispriced). Pure fraud
(rugs, Ponzis) is **included but always labeled as fraud**, not presented as
failed engineering. Contract *bugs* are out of scope (see the blind-spot
register in `audit-protocol.md`).

New economic-attack cases go in `data/security_panel.py` with the
cost-of-corruption numbers (`cost to corrupt` vs `value extractable`) and map to
S13/S14/S15 in `references/economic-security.md`.

Please uphold:

1. **Honesty over hype.** Figures are order-of-magnitude estimates — label them as
   such and cite sources (CoinGecko / on-chain / reputable reporting).
2. **No investment advice, no shilling, no token promotion.** This is research.
3. **Mechanism first.** A new case should map to a failure Skill / game model, not
   just be "a coin that went down."
4. **Respect ongoing litigation.** For unresolved cases, describe allegations as
   allegations and defer to final rulings.

## How to add a case

1. Add the row to **both** case libraries:
   - EN: `token-collapse-analysis-2009-2026.md`
   - ZH: `加密项目代币崩溃分析_2009-2026.md`
   Place it under the correct mechanism group (A–H) with year, peak→trough,
   drawdown, and a one-paragraph assessment.
2. If it is significant, add it to the structured dataset `data/case_dataset.py`
   (name, ticker, year, mechanism code, est. peak value-at-risk, drawdown,
   primary failure Skill), then regenerate the overview charts:
   ```bash
   cd data && python case_dataset.py
   ```
3. If it illustrates a Skill especially well, reference it in the relevant section
   of `death-spiral-deep-analysis.md` (and the ZH version).

## How to add / change a simulation

- Keep it **dependency-light** (numpy + matplotlib only) and self-documenting.
- **Calibrate to real data** and cite the calibration in the docstring.
- Chart **text in English** (avoids CJK font issues across machines).
- Regenerate everything and confirm it runs clean:
  ```bash
  cd simulations && python -m pip install -r requirements.txt && python run_all.py
  ```
- Update the simulation table in
  `skills/tokenomics-death-spiral-audit/references/simulations.md`.

## Dev setup

```bash
git clone https://github.com/wusijian007/tokenomics-autopsy
cd tokenomics-autopsy/simulations
python -m pip install -r requirements.txt
python run_all.py        # regenerate phase-transition charts
```

## Pull request process

1. Fork, then branch from `main` (e.g. `add-case-xyz`, `fix-terra-figures`).
2. Make focused changes; keep EN/ZH in sync where practical.
3. If you changed code, run `run_all.py` / `case_dataset.py` so committed charts
   match the code.
4. Open a PR describing **what** changed and **why**, with sources for any figures.
5. Be open to review feedback — the bar is correctness and clear mechanism mapping.

## License of contributions

By contributing, you agree that your contributions are licensed under
[CC BY 4.0](LICENSE), the same license as the project.

## Code of conduct

Be respectful and constructive. Critique mechanisms and claims, not people.
Harassment, spam, and token promotion are not welcome.
