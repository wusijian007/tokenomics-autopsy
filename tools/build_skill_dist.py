"""
Build & validate the distributable skill (ROADMAP: skill packaging).

Checks, then packages, skills/tokenomics-death-spiral-audit/ for installation
into any Agent-Skills-compatible agent (Claude Code, Codex CLI, Cursor,
Gemini CLI, Grok Build, Copilot, ...):

  1. FRONTMATTER: SKILL.md has a spec-conformant name (lowercase-hyphen,
     <=64 chars) and description (<=1024 chars); reads metadata.version.
  2. SELF-CONTAINMENT: no markdown link in the skill resolves outside the
     skill folder (relative ../ escapes are packaging bugs; external content
     must use absolute https:// URLs).
  3. DRIFT: the bundled scripts/ files are byte-identical to their canonical
     tools/ sources.
  4. DIST: writes dist/tokenomics-death-spiral-audit-v<version>.zip
     (the folder, installable by unzipping into an agent's skills directory)
     and dist/PROMPT_PACK.md (a single compiled file for platforms without a
     skills mechanism - paste into a system prompt / project instructions).

Exit code != 0 on any validation failure. stdlib-only.

Run:  python build_skill_dist.py
"""
import hashlib
import re
import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "skills" / "tokenomics-death-spiral-audit"
DIST = REPO / "dist"

# canonical -> bundled byte-mirrors
MIRRORS = [
    (REPO / "tools" / "stress_runner.py", SKILL / "scripts" / "stress_runner.py"),
    (REPO / "tools" / "report_generator.py", SKILL / "scripts" / "report_generator.py"),
    (REPO / "tools" / "design.example.yaml", SKILL / "scripts" / "design.example.yaml"),
    (REPO / "tools" / "audit.example.json", SKILL / "scripts" / "audit.example.json"),
]

# PROMPT_PACK order: entry point first, then references in audit->design order.
PACK_ORDER = ["SKILL.md",
              "references/anti-patterns.md", "references/game-models.md",
              "references/scorecard.md", "references/economic-security.md",
              "references/audit-protocol.md", "references/survivors.md",
              "references/lambda-formalization.md",
              "references/design-playbook.md", "references/design-patterns.md",
              "references/archetype-playbooks.md",
              "references/liquidity-engineering.md",
              "references/circular-economy.md", "references/incentive-audit.md",
              "references/simulations.md"]

errors = []


def check_frontmatter():
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        errors.append("SKILL.md: missing YAML frontmatter")
        return "0.0.0"
    fm = m.group(1)
    name = re.search(r"^name:\s*(\S+)", fm, re.MULTILINE)
    if not name or not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", name.group(1)):
        errors.append(f"SKILL.md: name missing or not lowercase-hyphen <=64 chars")
    desc = re.search(r"^description:\s*>\n((?:  .*\n)+)", fm, re.MULTILINE)
    if not desc:
        errors.append("SKILL.md: description block not found")
    else:
        dlen = len(" ".join(l.strip() for l in desc.group(1).splitlines()))
        if dlen > 1024:
            errors.append(f"SKILL.md: description {dlen} chars > 1024 (spec limit)")
        print(f"  frontmatter: name={name.group(1) if name else '?'}, "
              f"description {dlen} chars")
    ver = re.search(r'version:\s*"?([0-9][0-9a-zA-Z.\-]*)"?', fm)
    return ver.group(1) if ver else "0.0.0"


def check_links():
    """Every relative markdown link inside the skill must resolve inside it."""
    bad = 0
    for md in sorted(SKILL.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        for target in re.findall(r"\]\(([^)\s]+)\)", text):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            target_path = (md.parent / target.split("#")[0]).resolve()
            try:
                target_path.relative_to(SKILL.resolve())
            except ValueError:
                errors.append(f"{md.relative_to(REPO)}: link escapes skill folder -> {target}")
                bad += 1
                continue
            if not target_path.exists():
                errors.append(f"{md.relative_to(REPO)}: broken link -> {target}")
                bad += 1
        # belt-and-braces: no ../../.. anywhere in prose either
        if "../../.." in text:
            errors.append(f"{md.relative_to(REPO)}: contains a '../../..' escape reference")
            bad += 1
    print(f"  self-containment: {'OK - all links resolve inside the skill' if bad == 0 else f'{bad} problems'}")


def check_drift():
    ok = True
    for src, dst in MIRRORS:
        if not dst.exists():
            errors.append(f"missing bundled mirror: {dst.relative_to(REPO)}")
            ok = False
            continue
        h = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
        if h(src) != h(dst):
            errors.append(f"drift: {dst.relative_to(REPO)} differs from canonical "
                          f"{src.relative_to(REPO)} (re-copy it)")
            ok = False
    print(f"  drift check: {'OK - scripts/ mirrors tools/ exactly' if ok else 'FAILED'}")


def build_zip(version):
    DIST.mkdir(exist_ok=True)
    out = DIST / f"tokenomics-death-spiral-audit-v{version}.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(SKILL.rglob("*")):
            generated = (f.parent.name == "scripts"
                         and f.name.endswith((".verdict.md", "-audit.md")))
            if f.is_file() and "__pycache__" not in f.parts and not generated:
                z.write(f, Path("tokenomics-death-spiral-audit") / f.relative_to(SKILL))
    kb = out.stat().st_size / 1024
    print(f"  [dist]  {out.name}  ({kb:.0f} KB)")
    return out


def build_prompt_pack(version):
    parts = [
        "# Tokenomics Death-Spiral Audit — compiled prompt pack "
        f"(skill v{version})\n\n"
        "> Single-file compilation of the `tokenomics-death-spiral-audit` Agent\n"
        "> Skill, for platforms without a skills mechanism (paste into a system\n"
        "> prompt / project instructions / knowledge file). Prefer installing\n"
        "> the actual skill where supported. Source + runnable tooling:\n"
        "> https://github.com/wusijian007/tokenomics-autopsy\n"
        "> Research / design reference, NOT investment advice.\n"
    ]
    for rel in PACK_ORDER:
        text = (SKILL / rel).read_text(encoding="utf-8")
        text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.DOTALL)  # strip frontmatter
        parts.append(f"\n\n{'=' * 78}\nFILE: {rel}\n{'=' * 78}\n\n{text.strip()}\n")
    pack = "".join(parts)
    out = DIST / "PROMPT_PACK.md"
    out.write_text(pack, encoding="utf-8")
    print(f"  [dist]  PROMPT_PACK.md  ({len(pack)/1024:.0f} KB, ~{len(pack)//4:,} tokens)")


def main():
    print("Building the distributable skill")
    version = check_frontmatter()
    check_links()
    check_drift()
    if errors:
        print("\nVALIDATION FAILED:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    build_zip(version)
    build_prompt_pack(version)
    print("  all checks passed; dist/ is ready (dist/ is gitignored - attach to a"
          " GitHub Release to distribute)")


if __name__ == "__main__":
    main()
