# tokenomics-autopsy

**代币死亡螺旋的机制级"尸检" + 一套避坑设计 skill。**

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-blue.svg)](LICENSE)
[![Python 3.x](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](simulations/)
[![Cases analyzed](https://img.shields.io/badge/cases-50%2B-red.svg)](加密项目代币崩溃分析_2009-2026.md)
[![Failure Skills](https://img.shields.io/badge/failure%20skills-10-purple.svg)](skills/)
![GitHub stars](https://img.shields.io/github/stars/wusijian007/tokenomics-autopsy?style=social)

> [English](README.md) | 🌐 **中文** · 许可:[CC BY 4.0](LICENSE)

> 一个开源的代币经济学**避坑知识库**:从 2009–2026 的 50+ 个标志性崩盘中,蒸馏出可复用的失败反模式、博弈论模型与可复现仿真,供未来代币项目作设计参考。
> An open-source knowledge base for tokenomics design: forensic analysis of 50+ landmark collapses distilled into reusable anti-patterns, game-theoretic models, and reproducible simulations.
>
> **研究 / 设计参考,非投资建议。** Research / design reference, **not investment advice.**

---

## 三层结构 / Three layers

| 层 | 内容 | 文件 |
|---|---|---|
| **L1 现象层** Cases | 50 个崩盘案例 + 8 类机制分类,总量估算 | [`加密项目代币崩溃分析_2009-2026.md`](加密项目代币崩溃分析_2009-2026.md) |
| **L2 机制层** Mechanisms | 统一反身性方程(λ>1)、4 个博弈模型、供需定量解剖、逐案拆解 + 仿真图 | [`代币经济学死亡螺旋_深度分析与失败Skills.md`](代币经济学死亡螺旋_深度分析与失败Skills.md) |
| **L3 知识层** Skills | 可触发的开源 skill pack:10 个失败反模式 + 风险评分卡 + 设计公理 | [`skills/`](skills/) |

支撑层 / Supporting:
- [`simulations/`](simulations/) — 4 个校准过的可复现 Python 仿真,生成所有相变图表。
- [`data/`](data/) — 38 个案例的结构化数据集 + 两张宏观量化总览图。

---

## 核心洞见 / The core idea

死亡螺旋**不是运气或运营失误,而是机制内生的相变**。当系统增益

```
λ = (∂fundamentals/∂price) · (∂price/∂fundamentals) > 1
```

时,代币价格本身成为机制的燃料,任何向下扰动被指数放大。健康设计保持 `λ < 1`(基本面与价格解耦)。

**一句话判据**:*如果币价归零,还有人需要这个代币吗?* 答"否" = 需求反身、无锚 → 重新设计或不做。

---

## 10 个失败 Skills(速查)/ The 10 failure Skills

| # | 反模式 | 致命阈值 |
|---|---|---|
| S1 | 反身性燃料 Reflexive collateral | corr(储备, 负债) → 1 |
| S2 | 补贴需求 Subsidized demand | 支出 > 收入;储备 runway < 12 月 |
| S3 | 无上限龙头 Uncapped faucet | sink/faucet < 1 且 sink 靠新用户 |
| S4 | (3,3) 协调脆性 | 市价/背书 > 3;收益靠增发 |
| S5 | 银行挤兑结构 Sequential redemption | 流动性覆盖 < 可即时赎回负债 |
| S6 | 算稳吸收壁垒 Absorbing barrier | 储备率 R = M/S → 1 |
| S7 | 低流通高 FDV | 初始流通 <10%;首年解锁 >50% |
| S8 | 速度漏损 Velocity leak | 无价值捕获;高 velocity |
| S9 | 纯叙事需求 Narrative-only | 零收入;持仓集中;名人未锁 |
| S10 | 杠杆传染 Leverage contagion | 互为抵押;危机中相关性→1 |

详解 + 解药:[`skills/tokenomics-death-spiral-audit/references/anti-patterns.md`](skills/tokenomics-death-spiral-audit/references/anti-patterns.md)

---

## 4 个博弈模型 / The 4 game models

| 模型 | 失败形态 | 看什么 | 仿真 |
|---|---|---|---|
| 银行挤兑 Diamond–Dybvig | 突变 | 信念冲击 | `sim4` |
| (3,3) 协调 | 塌到背书价 | 新钱增长率 | `sim2` |
| 算稳吸收壁垒 | 归零 | 储备率 R | `sim1` |
| 解锁/通胀供给 | 阴跌 | 解锁日历 | `sim3` |

详见 [`game-models.md`](skills/tokenomics-death-spiral-audit/references/game-models.md)。

---

## 快速开始 / Quick start

**审计一个代币设计**(人类或 AI agent):
1. 用 [`game-models.md`](skills/tokenomics-death-spiral-audit/references/game-models.md) 归类机制。
2. 用 [`anti-patterns.md`](skills/tokenomics-death-spiral-audit/references/anti-patterns.md) 逐项检查红旗。
3. 用 [`scorecard.md`](skills/tokenomics-death-spiral-audit/references/scorecard.md) 打分(附 Terra 实例:31/46)。
4. 用仿真压力测试你的参数。

**跑仿真 / 生成图表:**
```bash
cd simulations && python -m pip install -r requirements.txt && python run_all.py
cd ../data && python case_dataset.py
```

**作为 Claude / Agent skill 使用:** 把 `skills/tokenomics-death-spiral-audit/` 放进 skills 目录,询问代币模型设计/可持续性时会自动触发。

---

## 目录树 / Repo layout
```
cryptofail/
├── README.md                                  # 本文件
├── 加密项目代币崩溃分析_2009-2026.md            # L1 案例库
├── 代币经济学死亡螺旋_深度分析与失败Skills.md     # L2 深度分析(含仿真图)
├── skills/
│   ├── README.md
│   └── tokenomics-death-spiral-audit/
│       ├── SKILL.md                           # L3 skill 入口
│       └── references/{anti-patterns,game-models,scorecard,simulations}.md
├── simulations/
│   ├── sim1..sim4_*.py, run_all.py, viz.py, requirements.txt
│   └── charts/*.png
└── data/
    ├── case_dataset.py
    └── case_dataset.csv
```

## 许可 / License
CC BY 4.0。欢迎社区贡献新案例与新模型。数字为量级估算,请以实时数据为准;部分案例仍在诉讼中,定性以最终司法结论为准。
