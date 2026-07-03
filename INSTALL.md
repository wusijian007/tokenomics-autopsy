# Install the skill in your AI agent

`skills/tokenomics-death-spiral-audit/` follows the open
[Agent Skills](https://agentskills.io) standard (`SKILL.md` + `references/` +
`scripts/`), so the **same folder works across Claude Code, OpenAI Codex CLI,
Cursor, Gemini CLI, GitHub Copilot, Grok Build, Amp, Goose, OpenCode, and any
other agent that supports the spec**. It is fully self-contained — the
knowledge base plus two stdlib-only runnable scripts; the wider research repo
(simulations, datasets, validation layer) is optional.

> Research / design reference, **not investment advice**.

## Option A — Claude Code plugin marketplace (recommended)

```
/plugin marketplace add wusijian007/tokenomics-autopsy
/plugin install tokenomics-death-spiral-audit@tokenomics-autopsy
```

This installs the full repo as a plugin (so the bundled stress-runner also
finds the simulations). Grok Build reads Claude Code marketplaces and plugins
automatically, so this path covers Grok too.

## Option B — copy the folder (any Agent-Skills agent)

Copy `skills/tokenomics-death-spiral-audit/` (or unzip the release archive)
into your agent's skills directory:

| Agent | Personal | Per-project |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| Grok Build | `~/.grok/skills/` | `.grok/skills/` |
| Codex CLI / Cursor / Gemini CLI / Copilot / Amp / Goose / OpenCode … | the agent's skills directory per its docs (same folder format) | — |

One-liner from a clone:

```bash
git clone https://github.com/wusijian007/tokenomics-autopsy
cp -r tokenomics-autopsy/skills/tokenomics-death-spiral-audit ~/.claude/skills/
```

Grok Build also supports `grok skills install ./tokenomics-autopsy/skills/tokenomics-death-spiral-audit`.

## Option C — claude.ai / web agents (upload a zip)

Build the self-contained archive and upload it where the product accepts
skill/knowledge uploads (e.g., claude.ai → Settings → Capabilities → Skills):

```bash
python tools/build_skill_dist.py     # -> dist/tokenomics-death-spiral-audit-v2.0.0.zip
```

## Option D — platforms with no skills mechanism (prompt pack)

The build also compiles the whole skill into one file —
`dist/PROMPT_PACK.md` (~150 KB, ≈38k tokens). Paste it into a system prompt,
project instructions, or a knowledge file (web Grok/ChatGPT/Gemini projects).
Prefer a real skill install where supported: progressive disclosure loads only
what each task needs.

## Option E — agents working inside this repo

`AGENTS.md` at the repo root points any agent (Codex, Cursor, etc. — the
[agents.md](https://agents.md) convention) at the skill and states the
instrument's hard rules. Nothing to install; just open the repo.

## Verify the install

Ask your agent something like:

> "Audit this token design for death-spiral risk: an algorithmic stablecoin
> backed by its own volatile token, 19% APY paid from reserves."

A correct install triggers the skill: it should classify the mechanism
(seigniorage / bank-run), cite engine rows S1/S2/S6 with the 0/1/2 scorecard,
and land near a "textbook death-spiral" verdict. For the programmatic path:

```bash
cd <skills-dir>/tokenomics-death-spiral-audit/scripts
python stress_runner.py design.example.yaml     # expect: 2/54, PASS
```

## What's inside

```
tokenomics-death-spiral-audit/
  SKILL.md              # entry point: 4 modes (quick screen / audit / design / stress-test)
  references/           # 14 docs: anti-patterns, scorecard, security panel, playbooks…
  scripts/              # stdlib-only: stress_runner.py, report_generator.py + examples
```

Full research repo (8 simulations, 53-case scored universe, out-of-sample
validation, frozen prospective registry):
https://github.com/wusijian007/tokenomics-autopsy
