# Incentive Audit — Rewards as Contracts, Not Budgets

The design playbook (step 6) budgets incentives as customer-acquisition cost.
This reference is the deeper layer: an incentive is a **contract with an
adversarial counterparty**, and every incentivised metric will be gamed to the
cheapest satisfying behaviour. Grounding: principal–agent theory, Holmström–
Milgrom multitask, Goodhart's law, and the behavioural finance of token markets.
This is the audit standard behind S2 (subsidised demand) and S11 (mercenary
TVL) — it explains *why* those pathologies are the default, not the exception.

## 1. Incentives are contracts — the IC/IR checklist

The protocol (principal) buys services from agents: LPs, validators, users,
market makers, referrers. Each reward rule must pass two classic tests, checked
against **adversarial**, not average, behaviour:

- **Incentive compatibility (IC)**: is *honest* behaviour the agent's best
  response, or is there a cheaper action that collects the reward without
  delivering the value? (Wash-trade to earn volume rewards; park idle TVL to
  earn TVL rewards; run a phantom node to earn uptime rewards.)
- **Individual rationality (IR)**: does the agent earn more participating
  honestly than not participating — *and does the protocol get more value than
  it pays*?

For every reward rule, write: the intended behaviour, the cheapest behaviour
that still collects, and the gap. If the cheapest collecting behaviour isn't the
intended one, the incentive is mis-specified — it will fund the exploit.

## 2. The Goodhart red-team table (a standard audit artifact)

> "When a measure becomes a target, it ceases to be a good measure."

Every incentivised metric is a target and will be gamed. Produce this table for
each reward rule:

| Metric rewarded | Cheapest exploit | Cost to sybil/game | Value actually delivered | Verdict |
|---|---|---|---|---|
| Volume | wash trading (self-trade) | ~gas + fees to self | ≈ 0 (no real flow) | fake unless spread-paying |
| TVL | park stable, no usage | ~opportunity cost | ≈ 0 (S11) | rent, not adoption |
| Users / wallets | sybil farms | ~gas per wallet | ≈ 0 | fake unless PoP-gated |
| Uptime / nodes | phantom/idle hardware | ~cheap VPS | ≈ 0 (S15) | capacity ≠ demand |
| Referrals | self-referral rings | ~0 | ≈ 0 (Ponzi shape) | fraud vector |
| Fees paid | fee round-tripping to farm | fee − reward | ≈ 0 if reward > fee | net-negative! |

**The reward-must-be-earned rule**: never let the reward for producing a metric
exceed the cost of faking it. If reward-per-unit > sybil-cost-per-unit, you are
paying people to manufacture the metric (the last row is the S2 death spiral in
miniature: paying more to farm than the activity is worth).

**Sybil-cost worksheet**: for each reward, estimate the marginal cost to create
one more rewarded unit (wallet, node, dollar of TVL, unit of volume). Compare to
reward-per-unit. Defenses that raise sybil cost: proof-of-personhood gating,
minimum-stake/bond (P14), reward *flow* not *stock* (P15), quadratic/diminishing
curves, vesting so the exploit must survive a lockup.

## 3. Multitask crowding (Holmström–Milgrom)

When agents do several things and you can only measure some, paying hard for the
**measurable** crowds out the **unmeasurable**:

- Pay for TVL (measurable) → crowds out *sticky* usage and retention
  (unmeasurable) → the Blast/points pathology, derived from first principles.
- Pay for volume → crowds out organic price discovery (wash volume is easier).
- Pay for governance participation by quantity → crowds out *thoughtful*
  governance (vote-farming, S13 adjacency).

**Design rule**: never attach the strongest incentive to the most gameable
metric. Prefer rewarding outcomes that are (a) hard to fake and (b) aligned with
the unmeasurable goal — reward *fees paid by third parties* (hard to fake, means
real usage) over *TVL* (trivial to park).

## 4. The behavioural layer (the actor model the docs otherwise omit)

Rational-actor models miss why "everyone knew it was a ponzi" changes nothing.
Add these to the actor model:

- **Bubble-riding (Abreu–Brunnermeier)**: sophisticated actors *knowingly* ride
  a doomed design, planning to exit before the crash — so awareness doesn't
  prevent the bubble; it just makes the exit more crowded. This is why OHM/points
  farms attract smart money that fully understands the endgame.
- **Endowment effect / house money**: airdropped tokens feel free → instant
  dump (the S11 TGE cliff). Vesting reframes the endowment and dampens this.
- **Hyperbolic discounting**: users over-value immediate rewards → cliffs get
  front-run, streaming vesting (P12) behaves better because there's no single
  date to race to.
- **Unit bias**: retail over-buys low-unit-price tokens ("cheap") → high supply
  / low nominal price exploits a cognitive bias, not a valuation.
- **Positive-feedback trading (DeLong–Shleifer–Summers–Waldmann)**: momentum
  traders amplify moves both ways — the market-microstructure face of
  reflexivity (L2 §1).

Design consequence: assume a meaningful fraction of participants are
short-horizon and exit-planning. Mechanisms must be robust to *rational
defection*, not just to naïve behaviour.

## 5. Cohort accounting standard (the measurement behind S11)

"Organic share" (S11's scorecard metric) must be measured, not eyeballed. The
standard:

- **Incentive LTV/CAC per cohort**: for each acquisition cohort, lifetime value
  delivered (fees paid, retained deposits) ÷ incentive cost to acquire. <1 means
  you paid more than they're worth.
- **Retention curves after each emissions cut**: does the cohort stay when the
  subsidy tapers? A cliff at every cut = mercenary (S11); a gentle decay = some
  organic stickiness.
- **Organic-baseline netting**: TVL/usage that would remain if incentives
  stopped today. Publish it (playbook step 8 dashboard). This is the honest
  denominator for "is our growth real?"
- **Net-payer cohort split** (ties to `circular-economy.md`): which cohorts are
  net payers vs net extractors, tracked over time.

## 6. Design checklist (incentives)

- [ ] Every reward rule passes IC (honest = best response) and IR (protocol
      nets value), checked adversarially
- [ ] Goodhart red-team table filled; no reward-per-unit > sybil-cost-per-unit
- [ ] Strongest incentive is *not* on the most gameable metric (multitask)
- [ ] Rewards target *flow* (third-party fees) over *stock* (parked TVL)
- [ ] Sybil cost raised by gating/bonding/vesting where the metric is fakeable
- [ ] Actor model assumes rational defectors and bubble-riders, not naïfs
- [ ] Cohort LTV/CAC, post-cut retention, and organic baseline measured + published

Related: `anti-patterns.md` (S2, S11), `design-patterns.md` (P15 disciplined
points, P14 bonded work), `circular-economy.md` (net-payer accounting),
`economic-security.md` (S13 when governance participation is the gamed metric).
