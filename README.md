![Tokenomics Soundcheck](assets/social-preview.png)

# Tokenomics Soundcheck

> **Sound money needs sound mechanisms.**

**Design token economies that don't fuel their own collapse — and stress-test them before they launch.**

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-blue.svg)](LICENSE)
[![Python 3.x](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](simulations/)
[![Cases analyzed](https://img.shields.io/badge/cases-50%2B-red.svg)](token-collapse-analysis-2009-2026.md)
[![Failure Skills](https://img.shields.io/badge/failure%20skills-15-purple.svg)](skills/)
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
| **L3 Knowledge** — Skills | A triggerable open-source skill pack: 15 failure anti-patterns (12 spiral + 3 economic-attack) + a measurable scorecard + security panel + audit protocol (evaluation), and a 16-mechanism positive pattern library + 8 archetype playbooks + liquidity/circular-economy/incentive deep dives (design) | [`skills/`](skills/) |

Supporting layers:
- [`simulations/`](simulations/) — 8 calibrated, reproducible Python simulations (6 failure archetypes + `sim7` PID-damped stability + `sim8` spender-class economy).
- [`data/`](data/) — a 38-case dataset, an 18-case scorecard calibration, a cost-of-corruption security back-scoring (S13/S14/S15), and a 53-case scored universe with an empirical weight fit.
- [`validation/`](validation/README.md) — **out-of-sample validation**: a 15-case leakage-audited holdout backtest + a frozen prospective registry (reviews 2027/2028) + a red-team program.
- [`tools/`](tools/README.md) — the product layer: a stress-runner (design spec → verdict), a report generator, and κ / registry-monitor tooling.

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

## The 15 failure Skills (quick reference)

Two axes. **Spiral risk** (S1–S12, scored 0–54) — reflexive dynamics that amplify a decline; tiers **engine** (×3) · **structure** (×2) · **amplifier** (×1). **Attack risk** (S13–S15, separate security panel) — discrete exploits where the code works and the mechanism is mispriced.

| # | Anti-pattern | Tier | Killer threshold |
|---|---|---|---|
| S1 | Reflexive collateral | engine | corr(reserve, liability) → 1 |
| S2 | Subsidized demand | engine | payout > revenue; reserve runway < 12 months |
| S3 | Uncapped faucet | structure | sink/faucet < 1 and the sink needs new users |
| S4 | (3,3) coordination fragility | structure | price/backing > 3; yield from inflation |
| S5 | Sequential-service redemption | engine | liquidity coverage < instantly-redeemable liabilities |
| S6 | Seigniorage absorbing barrier | engine | reserve ratio R = M/S → 1 |
| S7 | Float–FDV asymmetry | structure | initial float <10%; first-year unlock >50% of float |
| S8 | Velocity leak | amplifier | no value capture; high velocity |
| S9 | Narrative-only demand | engine | zero revenue; concentrated, unlocked holders |
| S10 | Leverage contagion | amplifier | tokens cross-collateralize; correlation → 1 in stress |
| S11 | Mercenary points / rented TVL | structure | organic TVL share <30%; snapshot/TGE cliff |
| S12 | Recursive leverage loop | structure | loop unwind size > real market depth |
| S13 | Captureable governance | attack surface | cost to corrupt a quorum < value it controls; no timelock |
| S14 | Manipulable-oracle leverage | attack surface | cost to move the oracle < borrowable value |
| S15 | Supply-subsidy mismatch (DePIN) | structure | service revenue / emissions value ≪ 1 |

Detail + antidotes: [`anti-patterns.md`](skills/tokenomics-death-spiral-audit/references/anti-patterns.md) · the cost-of-corruption ledger (S13–S15): [`economic-security.md`](skills/tokenomics-death-spiral-audit/references/economic-security.md) · why survivors survived: [`survivors.md`](skills/tokenomics-death-spiral-audit/references/survivors.md)

**Economic-attack axis** — the code executing as written is no defense: Beanstalk (governance) and Mango (oracle) were *purchases*, not hacks. Back-scoring every known economic attack shows the profit inequality (`value extractable − cost to corrupt > 0`) was computable **before** each attack ([`data/security_panel.py`](data/security_panel.py)):

![cost of corruption](simulations/charts/data_security_cost_vs_prize.png)

**Calibration (in-sample)** — the scorecard was back-scored on 18 historical cases (10 collapses, 8 stress survivors). Collapses score 12–37, survivors 1–11, and **no survivor triggers an engine red line** ([`data/scorecard_calibration.py`](data/scorecard_calibration.py)):

![scorecard separation](simulations/charts/data_scorecard_separation.png)

**Validation (out-of-sample)** — 15 further cases that appear nowhere in this repo and were never used to build the instrument (leakage-audited: USDN, DEI, Tomb, StrongBlock, Titano, Solidly, Blur, Celestia vs USDT, Frax, LINK, rETH, Aave, AMPL, Pendle). The raw totals overlap in the middle band — but the **engine → structure → anchor decision rule classifies 15/15 outcomes correctly**, including the two structure-only bleeds and the stressed survivor ([`validation/`](validation/README.md)). A frozen [prospective registry](validation/prospective-registry.md) (Ethena, Hyperliquid, pump.fun, USDD, Jupiter + 2 in-flight) pre-registers falsifiable predictions for 2027/2028 review — the bias-free tier:

![holdout separation](simulations/charts/data_holdout_separation.png)

**Empirical weights** — a data-driven logistic fit on the 53-case [scored universe](data/scored_universe.py) reproduces the hand weights' engine > structure > amplifier ranking ([`fit_weights.py`](data/fit_weights.py)). The near-perfect AUC is a *consistency* result (the set is largely in-sample), not a forward-accuracy claim — but the fit surfaces genuine recalibration signal (raise S9, treat S12 as combinatorial). The frozen v2 weights are retained pending an out-of-sample win:

![weight fit](simulations/charts/data_weight_fit.png)

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

## Install as an agent skill

The skill pack follows the open [Agent Skills](https://agentskills.io) standard — the same folder works in **Claude Code, Codex CLI, Cursor, Gemini CLI, Copilot, Grok Build**, and 16+ other agents:

```
/plugin marketplace add wusijian007/tokenomics-autopsy        # Claude Code (Grok reads it too)
/plugin install tokenomics-death-spiral-audit@tokenomics-autopsy
```

or copy `skills/tokenomics-death-spiral-audit/` into your agent's skills directory (`~/.claude/skills/`, `~/.grok/skills/`, …). Self-contained: 14 reference docs + stdlib-only runnable `scripts/`. All options incl. a zip build and a single-file prompt pack for no-skill platforms: **[INSTALL.md](INSTALL.md)**.

## Quick start

**Screen a token in 15 minutes:** run the 8-question quick screen at the top of
[`audit-protocol.md`](skills/tokenomics-death-spiral-audit/references/audit-protocol.md) → `PASS` / `CONCERNS` / `RED LINE`.

**Full audit** (human or AI agent) — follow [`audit-protocol.md`](skills/tokenomics-death-spiral-audit/references/audit-protocol.md):
1. Collect inputs and draw the mechanism map (every price-dependent flow = a candidate λ>1 loop).
2. Classify the game structure with [`game-models.md`](skills/tokenomics-death-spiral-audit/references/game-models.md).
3. Measure and score the 12 rows of [`scorecard.md`](skills/tokenomics-death-spiral-audit/references/scorecard.md) (worked examples: Terra 37/54, DAI 1/54).
4. Compute distance-to-threshold, stress-test with the simulations, write the report from the template.

**Design a token** — run the 10-step [`design-playbook.md`](skills/tokenomics-death-spiral-audit/references/design-playbook.md) (necessity → demand anchor → value capture → supply → breakers → incentives-as-CAC → liquidity → monitoring → stress test → launch), pick your vertical in [`archetype-playbooks.md`](skills/tokenomics-death-spiral-audit/references/archetype-playbooks.md), and build from the 16 positive mechanisms in [`design-patterns.md`](skills/tokenomics-death-spiral-audit/references/design-patterns.md) — with deep dives on [liquidity](skills/tokenomics-death-spiral-audit/references/liquidity-engineering.md), [circular economies](skills/tokenomics-death-spiral-audit/references/circular-economy.md), and [incentives](skills/tokenomics-death-spiral-audit/references/incentive-audit.md).

**Run it as a tool** — [`tools/`](tools/README.md) turns the checklist into code:
```bash
cd tools
python stress_runner.py design.example.yaml     # design spec -> scored step-9 verdict
python report_generator.py audit.example.json   # completed audit -> full markdown report
```
The stress-runner scores a design spec on all 12 spiral rows + the security panel, runs the matching sims, and prints the verdict (the bundled Terra-like `design.badexample.yaml` scores 42/54, 5 engine red lines, REDESIGN).

**Run the simulations / regenerate charts:**
```bash
cd simulations && python -m pip install -r requirements.txt && python run_all.py
cd ../data && python case_dataset.py && python scorecard_calibration.py && python security_panel.py && python scored_universe.py && python fit_weights.py
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
│   └── tokenomics-death-spiral-audit/     # installable Agent Skill (see INSTALL.md)
│       ├── SKILL.md                       # L3 skill entry point (4 modes)
│       ├── scripts/                       # bundled stdlib-only stress-runner + report generator
│       └── references/{anti-patterns,game-models,scorecard,economic-security,
│                       audit-protocol,survivors,design-playbook,design-patterns,
│                       archetype-playbooks,liquidity-engineering,circular-economy,
│                       incentive-audit,lambda-formalization,simulations}.md
├── simulations/
│   ├── sim1..sim8_*.py (6 failure + sim7 PID + sim8 spender-class), run_all.py, viz.py
│   └── charts/*.png
├── tools/                                              # v6 product layer
│   ├── stress_runner.py + design.example.yaml          # design spec -> scored verdict
│   ├── report_generator.py + audit.example.json        # audit -> markdown report
│   ├── kappa_reliability.py                             # inter-rater κ (E3)
│   └── registry_monitor.py + registry_metrics.example.json
├── data/
│   ├── case_dataset.py / .csv                          # 38 collapse cases
│   ├── scorecard_calibration.py / .csv                 # 18-case in-sample calibration
│   ├── security_panel.py / .csv                        # cost-of-corruption back-scoring (S13/S14/S15)
│   ├── scored_universe.py / .csv                       # 53-case unified scored set
│   └── fit_weights.py / weight_fit.csv                 # empirical weight fit (hand vs data-driven)
├── ROADMAP.md                                          # frontier gap analysis + v4→v6 plan
└── validation/
    ├── README.md                                       # OOS protocol + empirical weights + freeze record
    ├── holdout_backtest.py / .csv                      # 15 leakage-audited held-out cases
    ├── prospective-registry.md / registry_scores.csv   # frozen predictions (reviews 2027/2028)
    └── red-team.md                                     # standing break-the-instrument challenge
```

## Research agenda
Where this project is headed — a frontier gap analysis across incentive
economics, mechanism design, liquidity engineering, circular economies,
valuation, and cryptoeconomic security, with a sequenced v4→v6 plan:
[ROADMAP.md](ROADMAP.md).

## Contributing
New cases, corrections, simulations, and translations are all welcome — see
[CONTRIBUTING.md](CONTRIBUTING.md). The bar is correctness and clear mechanism mapping.

## License
CC BY 4.0. Community contributions of new cases and models are welcome. Figures are order-of-magnitude estimates; reconcile against live data. Some named cases are in ongoing litigation — defer to final rulings.
