# magic-slides

Agent-based generator for Magic artist pitch decks. Turns a one-page YAML profile into a full, brand-compliant HTML deck, with a linter that enforces every recurring brand rule. Driven by a Claude Code skill (`/magic-slides`) that handles the end-to-end flow — fact-checking, drafting, generating, linting, previewing, and shipping.

Built and maintained by [Laura](https://github.com/lolacolafola) for [Magic](https://vibeonmagic.com). Public for portfolio / sharing; the actual deck content (artist copy, CRM cards) is Magic-specific.

## What this tool does

Takes hand-built bespoke decks (which used to take ~3 hours each, with recurring drift bugs) and turns them into something you can spin up in ~30 minutes — clean, byte-reproducible, lint-clean.

The pattern:
- One canonical HTML template with ~56 `{{placeholder}}` slots
- Per-artist YAML profiles supply the values
- A linter enforces ~10+ brand rules automatically
- An interactive AI skill walks you through new-artist setup, including web-verifying the artist's real facts before drafting anything

## Quick start

```bash
# Render a deck to a test-render sibling file (NEVER overwrites a live index.html)
python3 generate.py examples/twinsmatic.yaml -o ../magic-twinsmatic-deck/index.test.html

# Run the linter against any deck
python3 lint.py path/to/index.html
python3 lint.py --all                          # lint the 3 reference decks

# Round-trip test (verify the template still matches a live deck byte-for-byte)
python3 generate.py examples/twinsmatic.yaml --check ../magic-twinsmatic-deck/index.html
```

## What's in here

```
magic-slides/
├── README.md
├── template/
│   └── index.html          # Jinja2 deck template (~3,660 lines, ~56 placeholders)
├── examples/
│   ├── twinsmatic.yaml     # album-pulse reference (lowercase brand)
│   ├── toto.yaml           # concert-pulse single-night reference
│   ├── gims.yaml           # concert-pulse multi-night reference
│   └── sabrina-carpenter.yaml  # speculative pitch example
├── generate.py             # Jinja renderer + --check round-trip mode
├── lint.py                 # ~10 brand-rule checks (slide numbers, pill color, product names, SVG centering, mobile zoom, ...)
├── skill/
│   └── SKILL.md            # The /magic-slides Claude Code skill — interactive new-deck flow
├── notes/
│   ├── TRIANGULATION.md    # Slide inventory + per-slide variant table from the 3 reference decks
│   ├── PLACEHOLDERS.md     # Every {{placeholder}} the template uses
│   ├── CONDITIONALS.md     # Pulse-type branching plan
│   └── ROUND_TRIP_STATUS.md # Workflow rules, round-trip status
└── schemas/                # (reserved for future JSON Schema for YAML profiles)
```

## Installing the Claude Code skill

The interactive `/magic-slides` skill lives at `skill/SKILL.md`. To install it in your Claude Code setup:

```bash
# Project-local install (skill only available in this project)
mkdir -p .claude/skills/magic-slides
cp skill/SKILL.md .claude/skills/magic-slides/SKILL.md

# OR user-global install (skill available in every Claude Code session)
mkdir -p ~/.claude/skills/magic-slides
cp skill/SKILL.md ~/.claude/skills/magic-slides/SKILL.md
```

Then in Claude Code: type `/magic-slides` followed by an artist's name. It will:

1. Ask pulse type (album drop vs concert/tour/event) and anchor mode (real / speculative / hypothetical)
2. Web-search the artist's real facts (never fabricates)
3. Draft a YAML profile from the closest reference deck
4. Run the generator + linter
5. Open a browser preview
6. Wait for your eyeball before pushing to GitHub

## Hard rules

- **Never write to a live `index.html` until preview is approved.** Generator should target `index.test.html` first.
- **Never push to GitHub without explicit user approval** after a visual check.
- **Never fabricate artist facts.** Web-search to verify; ask user when uncertain.
- **Test files are local-only** — `.git/info/exclude` in each deck folder has `index.test.html` listed.

## Why this exists

Magic produces many artist pitch decks. Each one used to be a manual ~3-hour rebuild of the previous one, with predictable drift bugs (wrong slide numbers, off-canonical SVG centering, banned CSS classes sneaking back in, fabricated artist facts from earlier sessions). This tool ends that pattern: drift is caught by `lint.py`, copy is enforced by the template + memory rules, and the interactive skill ensures no fabricated facts go into a deck.

## Status

Phase 1 shipped 2026-06-06. Three reference decks (twinsmatic, toto, gims) round-trip byte-identical from their YAML profiles. Linter catches all documented brand rules. Skill flow tested end-to-end with a speculative Sabrina Carpenter / Coachella pitch.

Future ideas (not yet built, see Magic-internal notes):
- **Brand-layer extraction** — separate the Magic brand from the template so other brands could plug in
- **Figma sync** — mirror the YAML → HTML generator with YAML → Figma using the Figma MCP
