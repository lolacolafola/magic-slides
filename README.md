# magic-slides

Agent-based generator for bespoke pitch decks. Turns a one-page YAML profile into a full, brand-compliant HTML deck, with a linter that enforces every recurring brand rule. Driven by a Claude Code skill (`/magic-slides`) that handles the end-to-end flow — fact-checking, drafting, generating, linting, previewing, and shipping.

Built and maintained by [Laura Cordrey](https://github.com/lolacolafola). The pattern was developed against a specific brand system; the public version of this repo shows the structure with a fictional example. Real client adaptations stay local.

## What this tool does

Takes hand-built bespoke decks (which used to take ~3 hours each, with recurring drift bugs) and turns them into something you can spin up in ~30 minutes — clean, byte-reproducible, lint-clean.

The pattern:
- One canonical HTML template with ~56 `{{placeholder}}` slots
- Per-client YAML profiles supply the values
- A linter enforces ~10+ brand rules automatically
- An interactive AI skill walks you through new-deck setup, including web-verifying real facts before drafting anything

## Quick start

```bash
# Render the example deck
python3 generate.py examples/example-artist.yaml -o /tmp/example-deck.html

# Lint any deck
python3 lint.py path/to/index.html
python3 lint.py --all                          # lint all discovered decks

# Round-trip test (verify the template still matches a live deck byte-for-byte)
python3 generate.py examples/example-artist.yaml --check path/to/index.html
```

## What's in here

```
magic-slides/
├── README.md
├── template/
│   └── index.html          # Jinja2 deck template (~3,660 lines, ~56 placeholders)
├── examples/
│   └── example-artist.yaml # Fictional reference profile showing the YAML structure
├── generate.py             # Jinja renderer + --check round-trip mode
├── lint.py                 # ~11 brand-rule checks (slide numbers, pill color, product names, SVG centering, mobile zoom, CRM phase alignment, etc.)
├── skill/
│   └── SKILL.md            # The /magic-slides Claude Code skill — interactive new-deck flow
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

Then in Claude Code: type `/magic-slides` followed by an artist or client name. It will:

1. Ask pulse type (album drop vs concert/tour/event) and anchor mode (real / speculative / hypothetical)
2. Web-search real facts (never fabricates)
3. Draft a YAML profile from a starting reference
4. Run the generator + linter
5. Open a browser preview
6. Wait for your eyeball before pushing to GitHub

## Hard rules

- **Never write to a live `index.html` until preview is approved.** Generator targets `index.test.html` first.
- **Never push to GitHub without explicit user approval** after a visual check.
- **Never fabricate facts.** Web-search to verify; ask user when uncertain.

## Why this exists

Producing many bespoke client decks used to mean a manual ~3-hour rebuild of the previous one, with predictable drift bugs (wrong slide numbers, off-canonical SVG centering, banned CSS classes sneaking back in, fabricated facts from earlier sessions). This tool ends that pattern: drift is caught by `lint.py`, copy is enforced by the template + memory rules, and the interactive skill ensures no fabricated facts go into a deck.

## Status

Phase 1 shipped 2026-06-06. Production decks round-trip byte-identical from their YAML profiles. Linter catches all documented brand rules across the deployed deck fleet. Skill flow tested end-to-end with real and speculative pitches.

Future ideas (not yet built):
- **Brand-layer extraction** — separate brand-specific bits from the template so other brands could plug in
- **Figma sync** — mirror the YAML → HTML generator with YAML → Figma using the Figma MCP
