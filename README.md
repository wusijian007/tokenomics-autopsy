# tokenomics-autopsy

**Forensic post-mortems of 50+ token death spirals — and a design skill to avoid them.**

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-blue.svg)](LICENSE)
[![Python 3.x](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](simulations/)
[![Cases analyzed](https://img.shields.io/badge/cases-50%2B-red.svg)](token-collapse-analysis-2009-2026.md)
[![Failure Skills](https://img.shields.io/badge/failure%20skills-10-purple.svg)](skills/)
![GitHub stars](https://img.shields.io/github/stars/wusijian007/tokenomics-autopsy?style=social)

> 🌐 **English** | [中文](README.zh.md) · License: [CC BY 4.0](LICENSE)

> An open-source **knowledge base for tokenomics design**: a forensic analysis of 50+ landmark collapses (2009–2026), distilled into reusable failure anti-patterns, game-theoretic models, and reproducible simulations — a design reference for future token projects.
>
> **Research / design reference, not investment advice.**

---

## Three layers

| Layer | Content | File |
|---|---|---|
| **L1 Phenomenon** — Cases | 50 collapse cases + an 8-class mechanism taxonomy, with a total-count estimate | [`token-collapse-analysis-2009-2026.md`](token-collapse-analysis-2009-2026.md) |
| **L2 Mechanism** | Unified reflexivity equation (λ>1), 4 game models, quantitative supply-demand anatomy, case-by-case breakdowns + simulation charts | [`death-spiral-deep-analysis.md`](death-spiral-deep-analysis.md) |
| **L3 Knowledge** — Skills | A triggerable open-source skill pack: 10 failure anti-patterns + a risk scorecard + design axioms | [`skills/`](skills/) |

Supporting layers:
- [`simulations/`](simulations/) — 4 calibrated, reproducible Python simulations that generate every phase-transition chart.
- [`data/`](data/) — a structured dataset of 38 cases + two macro overview charts.

> Chinese versions of every document are available: [中文 README](README.zh.md) · [L1 中文](加密项目代币崩溃分析_2009-2026.md) · [L2 中文](代币经济学死亡螺旋_深度分析与失败Skills.md).

---

## The core idea

A death spiral is **not bad luck or an operational error — it is an endogenous phase transition**. When the system gain

```
λ = (∂fundamentals/∂price) · (∂price/∂fundamentals) > 1
```

the token's own price becomes the fuel for the mechanism, and any downward perturbation is amplified exponentially. Healthy designs keep `λ < 1` (fundamentals decoupled from price).

**The one-line test:** *if the token's price went to zero, would anyone still need this token?* If the answer is "no," demand is reflexive and unanchored → redesign or walk away.

---

## The 10 failure Skills (quick reference)

| # | Anti-pattern | Killer threshold |
|---|---|---|
| S1 | Reflexive collateral | corr(reserve, liability) → 1 |
| S2 | Subsidized demand | payout > revenue; reserve runway < 12 months |
| S3 | Uncapped faucet | sink/faucet < 1 and the sink needs new users |
| S4 | (3,3) coordination fragility | price/backing > 3; yield from inflation |
| S5 | Sequential-service redemption | liquidity coverage < instantly-redeemable liabilities |
| S6 | Seigniorage absorbing barrier | reserve ratio R = M/S → 1 |
| S7 | Float–FDV asymmetry | initial float <10%; first-year unlock >50% of float |
| S8 | Velocity leak | no value capture; high velocity |
| S9 | Narrative-only demand | zero revenue; concentrated, unlocked holders |
| S10 | Leverage contagion | tokens cross-collateralize; correlation → 1 in stress |

Detail + antidotes: [`skills/tokenomics-death-spiral-audit/references/anti-patterns.md`](skills/tokenomics-death-spiral-audit/references/anti-patterns.md)

---

## The 4 game models

| Model | Failure shape | Watch | Simulation |
|---|---|---|---|
| Bank run (Diamond–Dybvig) | sudden | belief shock | `sim4` |
| (3,3) coordination | collapses to backing | new-money growth | `sim2` |
| Seigniorage absorbing barrier | to zero | reserve ratio R | `sim1` |
| Unlock / inflation supply glut | slow bleed | unlock calendar | `sim3` |

See [`game-models.md`](skills/tokenomics-death-spiral-audit/references/game-models.md).

---

## Quick start

**Audit a token design** (human or AI agent):
1. Classify the mechanism with [`game-models.md`](skills/tokenomics-death-spiral-audit/references/game-models.md).
2. Check the red flags with [`anti-patterns.md`](skills/tokenomics-death-spiral-audit/references/anti-patterns.md).
3. Score it with [`scorecard.md`](skills/tokenomics-death-spiral-audit/references/scorecard.md) (includes a worked Terra example: 31/46).
4. Stress-test your parameters with the simulations.

**Run the simulations / regenerate charts:**
```bash
cd simulations && python -m pip install -r requirements.txt && python run_all.py
cd ../data && python case_dataset.py
```

**Use it as a Claude / Agent skill:** drop `skills/tokenomics-death-spiral-audit/` into your skills directory; it triggers automatically when you ask about token model design or sustainability.

---

## Repo layout
```
cryptofail/
├── README.md                              # this file (English)
├── README.zh.md                           # Chinese
├── token-collapse-analysis-2009-2026.md   # L1 case library (EN)  / 加密项目代币崩溃分析_2009-2026.md (ZH)
├── death-spiral-deep-analysis.md          # L2 deep analysis (EN, with charts) / 代币经济学死亡螺旋_深度分析与失败Skills.md (ZH)
├── skills/
│   ├── README.md
│   └── tokenomics-death-spiral-audit/
│       ├── SKILL.md                       # L3 skill entry point
│       └── references/{anti-patterns,game-models,scorecard,simulations}.md
├── simulations/
│   ├── sim1..sim4_*.py, run_all.py, viz.py, requirements.txt
│   └── charts/*.png
└── data/
    ├── case_dataset.py
    └── case_dataset.csv
```

## License
CC BY 4.0. Community contributions of new cases and models are welcome. Figures are order-of-magnitude estimates; reconcile against live data. Some named cases are in ongoing litigation — defer to final rulings.
