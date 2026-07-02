# Red-Team Program — Break the Instrument on Purpose

An evaluation tool earns trust by surviving deliberate attempts to fool it. This
is the standing challenge (ROADMAP v6, E4): **design a token that passes the
scorecard and still dies**, or **design a token that the scorecard condemns but
that is actually sound**. Every successful attack becomes either a new
anti-pattern row or a documented, permanent limitation.

## The two challenges

1. **False negative** — a design that scores **≤ 7 with zero engine flags and a
   clean security panel**, yet has a credible, mechanism-level path to collapse
   that a competent auditor would miss using this instrument. (The dangerous
   one: it means the checklist has a blind spot.)
2. **False positive** — a design the instrument flags as high-risk (engine at 2,
   or ≥ 19/54) that is nonetheless structurally sound, with a survivor-grade
   argument for why. (Means a row is mis-specified or over-weighted.)

Out of scope (already-acknowledged blind spots, `audit-protocol.md`): pure
contract exploits, regulatory kills, key-person fraud, chain-level failure,
market beta, off-chain fraud an audit can't see, and timing. An attack that
relies only on these doesn't count — the instrument already says it can't see
them.

## Rules

- **Mechanism, not magic.** The attack must be a *token-economic* mechanism
  describable at the whitepaper stage — the same altitude the instrument works
  at. "A hidden mint function" is a contract bug (out of scope); "a reward loop
  whose sink is invisible to the sink/faucet metric" is a valid attack.
- **Score it honestly first.** Fill the scorecard and security panel with the
  measurement procedures. Show the score, then show the death.
- **Pre-register the outcome claim.** State what would prove the design dies (or
  survives), so the challenge is falsifiable like the prospective registry.
- **Reproducible.** A `design.yaml` for `stress_runner.py` plus a written
  mechanism walk-through is ideal.

## How to submit

Open a PR adding an entry to the log below (and a `design.yaml` under
`tools/redteam/` if applicable). Include: the design, its honest score, the
failure/soundness argument, and the outcome claim. See `CONTRIBUTING.md`.

## Triage → outcome

Each accepted attack resolves to exactly one of:

- **New row** — a genuinely novel mechanism not covered by S1–S15. Must clear
  the ROADMAP §3 discipline (≥3 instances, a measurement procedure, re-run
  calibration + holdout, a version bump) before it enters a re-frozen scorecard.
- **Row fix** — an existing row's measurement procedure or weight was wrong;
  patch `scorecard.md` and re-run the calibration.
- **Documented limitation** — a real failure the instrument structurally cannot
  see; added to the blind-spot register, stated loudly, not papered over.
- **Rejected** — the attack relies on an out-of-scope blind spot, or the honest
  score actually does flag it.

## Known-limitations seed (self-red-team)

Starting the log honestly with attacks the authors already know land:

- **Combination-only reflexivity.** A design can keep every *individual* row at
  0–1 while the *product* of several mild loops gives ρ(M) > 1 (the
  `lambda-formalization.md` spectral view). The linear scorecard sums rows; it
  underweights interactions. Mitigation: audit step 2 (draw the whole mechanism
  map) and the composition meta-rule in `design-patterns.md` — but this is a
  real structural limitation of a checklist, acknowledged.
- **The measurable-sink illusion (S3).** If a reward token's sink is technically
  present but economically hollow (e.g., a buy-to-burn funded by the same
  emissions), sink/faucet can read ≥ 1 while the economy is still an S3 faucet.
  Mitigation: the net-external-payer identity (`circular-economy.md`) — trace who
  actually pays, don't trust the ratio.
- **Off-chain-collateral opacity.** A design backed by "real-world assets" an
  audit can't verify can score S1=0 while being S1=2 in reality. Mitigation:
  score unverifiable claims pessimistically (scorecard.md), but a determined
  fabricator defeats this — a documented limitation.

## Log

*(append-only; one dated entry per accepted attack)*

- 2026-07-02 — seed limitations above logged by the authors (self-red-team).
