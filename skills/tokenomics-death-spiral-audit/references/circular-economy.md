# Circular-Economy Design (games, DePIN, social)

Reward-driven economies — play-to-earn, move-to-earn, DePIN, SocialFi — are
where S3 (uncapped faucet) and S15 (supply-subsidy mismatch) live. This
reference is the constructive side: how to build a token loop that is a real
economy rather than an emissions engine renting activity. The Web2 virtual-
economy field solved much of this a decade before crypto; we import it
(Castronova; Lehdonvirta & Castronova, *Virtual Economies*; the EVE Online
economic reports).

## 1. The net-external-payer identity (the master constraint)

A closed token loop can only **redistribute** value among participants. For the
economy to be *sustainable*, external value in must cover external value out:

```
Σ external inflows (real money spent to enter/consume, no exit intent)
        ≥  Σ external extractions (value taken out and sold)         [per period]
```

- **Axie's failure in one line**: nearly every participant was a *net extractor*
  (scholars, guilds, farmers all playing to earn and sell). No one was a net
  payer with no exit intent → the only inflow was new-entrant capital → a P2E
  economy is an S3 faucet the moment growth stalls.
- **A healthy game economy's spine**: a **spender class** (whales, status/fun
  buyers) who put money in to consume — cosmetics, status, access — with *no
  intention to sell*. They are the external inflow that funds everyone else.
- **Design deliverable** (playbook step 1, extended): name your net payers and
  what they buy that is *not exit-able*. If the only "payer" is the next entrant,
  you have a Ponzi with a game skin (S3 + S9).

This is the zero-price test raised from a token to a whole economy: *if the
reward token's price were zero, who still spends real money here, and why?*

## 2. Dual-currency segmentation (P16, done right)

Separate two currencies with opposite jobs:

| | Hard currency | Soft currency |
|---|---|---|
| Supply | scarce, capped | uncapped, minted by activity |
| Role | governance / investment / store | in-game utility / reward medium |
| Holder | investor, long-term | player, transactional |
| Inflation lands on | **not** this one | **this one, by design** |
| Sink | buy-ins, fee burns | consumption (crafting, upgrades, entry) |

- Inflation is *designed* onto the disposable soft currency, protecting the hard
  currency's book value (AXS survived while SLP bled — but only *partially*,
  because Axie lacked a spender class, so even the protected token's *economy*
  collapsed).
- **The trap**: if *both* currencies are investment assets, you have two S3
  faucets (STEPN's GST and GMT both bled). Segmentation without a net-external
  payer just distributes the inflation across two tokens.

## 3. Sink engineering — the sink taxonomy

Sinks are the demand side of the faucet/sink balance (`sim3`). Not all sinks are
equal; rank by whether they clear emissions *without needing new users*:

| Sink type | Clears via | Reflexive on growth? | Example |
|---|---|---|---|
| **Consumption sink** | existing users spend to play/upgrade | no (best) | crafting, energy, repairs, entry fees |
| **Status/cosmetic sink** | spenders buy non-functional prestige | no | skins, badges, land aesthetics |
| **Progression sink** | time/level-gated consumption | weakly | gear decay, re-rolls |
| **Speculative sink** | users lock hoping for appreciation | **yes (S3/S4)** | staking-for-yield, "breeding to flip" |
| **Growth sink** | value only if *new* users arrive | **yes (S3)** | breeding to sell to newcomers (Axie) |

**Design rule**: the dominant sink must be a consumption or status sink funded
by net-external payers. Growth/speculative sinks are S3 with extra steps —
they clear only while the user base expands.

**Sink elasticity**: sinks should scale with the faucet. Fixed sinks (a flat
entry cost) don't absorb rising emissions; elastic sinks (costs that rise with
supply/activity, seasons that reset accumulation, item decay/"mudflation"
management) keep `sink ≥ faucet` through the cycle. EVE runs deliberate ISK
sinks (transaction taxes, insurance, skill costs) tuned monthly against faucets.

## 4. DePIN — the supply-subsidy discipline (S15)

DePIN pays emissions for *capacity* (hardware, coverage, storage). The economy
is only real if paid demand shows up:

- **The ratio to publish** (Axiom 15): `service revenue / emissions value`
  (trailing, USD). ≪ 0.1 persistently = token holders subsidise infrastructure
  nobody rents (Helium's peak: ~$K/mo revenue vs tens of $M/mo emissions).
- **Burn-and-mint equilibrium (BME)**: demand burns credits at a fixed USD
  price; supply is paid in freshly minted tokens. Sound in principle (Helium's
  design), fatal when burn ≪ mint. Add a **mint floor tied to burn**
  (`mint ≤ k·burn`) so emissions can't run away from demand.
- **Demand-gated emissions**: pay capacity only where utilisation/revenue
  exists — per-region caps, utilisation multipliers — so you don't emit for
  coverage nobody uses (Filecoin's single-digit utilisation for years).

## 5. Telemetry as a launch deliverable (the EVE standard)

Faucet/sink balance is unmanageable unmeasured. The playbook (step 8) should
require, for any reward economy, an **EVE-style periodic economic report** from
day one:

- per-period **faucet** (all token sources: emissions, rewards, mint) and
  **sink** (all burns, consumption, fees) with the net;
- **money-supply and velocity** trends;
- **stock**: where the currency sits (parked vs circulating vs sunk);
- for DePIN: the revenue/emissions ratio and utilisation by region/segment;
- **cohort net-payer accounting**: which cohorts are net payers vs net
  extractors, over time.

CCP Games employs economists and publishes EVE's monthly report; RuneScape and
WoW actively manage gold/token sinks. Crypto reward economies that fly blind on
faucet/sink are choosing to rediscover S3 the hard way.

## 6. Design checklist (circular economy)

- [ ] Net-external-payer identity written: who pays real money with no exit
      intent, and what non-exit-able thing they buy
- [ ] A spender class exists and is not the same as the earner class
- [ ] Dual-currency: inflation lands on the soft/disposable currency by design
- [ ] Dominant sink is consumption/status, not growth/speculative (not S3)
- [ ] Sinks are elastic (scale with faucet; seasons/decay manage mudflation)
- [ ] `sink ≥ faucet` holds through a demand *slowdown*, not just growth (`sim3`)
- [ ] DePIN: revenue/emissions published; `mint ≤ k·burn`; emissions demand-gated
- [ ] EVE-style faucet/sink/cohort telemetry live at launch

Simulations: `sim3_p2e_faucet_sink.py` (faucet/sink phase transition; capped vs
uncapped). Related: `economic-security.md` (S15), `design-patterns.md` (P16),
`anti-patterns.md` (S3), the Axie/STEPN anatomy in the L2 analysis.
