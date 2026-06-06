# Round-trip & test-render workflow

## Privacy

- `magic-design-system/` is **not a git repo**. Nothing in `magic-deck-tool/` can leak to any GitHub. It stays on Laura's machine until she chooses otherwise.
- Each deck folder (`magic-toto-deck/`, etc.) IS its own git repo with remotes to vibeonmagic + lolacolafola — but the test outputs go to `index.test.html` which is in each repo's local `.git/info/exclude`, so git ignores it and nothing pushes.

## Rule: never write to a deck's `index.html`

The live `index.html` in each deck folder is what's deployed to GitHub Pages. The generator writes to `index.test.html` (sibling file) so the live deck is untouched.

```bash
cd magic-design-system/magic-deck-tool

# Generate test-render siblings (preview only, never pushed)
python3 generate.py examples/twinsmatic.yaml -o ../../magic-twinsmatic-deck/index.test.html
python3 generate.py examples/toto.yaml       -o ../../magic-toto-deck/index.test.html
python3 generate.py examples/gims.yaml       -o ../../magic-gims-deck/index.test.html
```

Open in browser:
- `magic-twinsmatic-deck/index.test.html`
- `magic-toto-deck/index.test.html`
- `magic-gims-deck/index.test.html`

Add `?scroll` to the URL for the single-page scroll view.

## Round-trip status (regenerate-from-YAML matches live `index.html`?)

| Deck       | Status                              |
| ---------- | ----------------------------------- |
| twinsmatic | **byte-identical** with live deck   |
| toto       | byte-identical EXCEPT documented drift fixes (slide numbers, SVG coords, i18n label wrapping, ?scroll, gl-br) — see TRIANGULATION.md §7 |
| gims       | byte-identical EXCEPT same drift fixes (subset) |

The Toto + Gims diffs are the canonical corrections we *want* — overwriting their live decks with the regen would fix bugs that exist there today. Decision deferred until Laura visually QA's the test-render siblings and confirms.

## DO NOT (without explicit permission)

- Overwrite any deck's `index.html` directly.
- Push, commit, or `git add` in any of the deck folders.
- Run `git init` on `magic-design-system/` or `magic-deck-tool/`.
