# Imagery — Assets folder convention

The deck template references several images. Each new artist deck needs these dropped into the deck folder's `Assets/` directory before the deck can render properly. (Generator will still produce HTML if files are missing — you'll just see broken-image icons with alt text in the preview.)

## What each deck needs

Drop these into `magic-{artist-slug}-deck/Assets/` (paths are relative to the deck's `index.html`):

### Required (1 per deck)

| Placeholder in YAML | Path the template will reference | What it is | Sizing guide |
|---|---|---|---|
| `s1_hero_img_src` | `Assets/{artist-slug}-hero.{ext}` | s1 (Welcome) right-side hero photo of the artist | ~1000×1250 portrait, full-bleed; right half of slide; left side fades via gradient mask |
| `s_superfans_hero_img_src` | `Assets/{artist-slug}-superfans.{ext}` | s-superfans (slide 11) right-side photo, ideally a live/crowd moment | ~1000×1250 portrait, same masking treatment as s1 |

### Required (5 shared frame images)

These are the 4 s5 "always-on" feature mockups + the s8 Magic Pulse phone shot. By convention they live in:

```
Assets/Frames/Deck Edits/Fanverse.png
Assets/Frames/Deck Edits/Gamification.png
Assets/Frames/Deck Edits/Fan Chat.png
Assets/Frames/Deck Edits/Shop.png
Assets/Frames/Deck Edits/Magic Pulse.png
```

…and the YAML field `frames_path_prefix` defaults to `Assets/Frames/Deck Edits/`.

These 5 images are typically **the same across decks** (they're product UI mockups, not artist photos). The cleanest approach: keep a master set somewhere central, copy into each new deck folder.

#### Exception: Toto's path

Toto's `Assets/Frames/{X}.png` is at the parent level (NOT in `Deck Edits/`). The Toto YAML overrides `frames_path_prefix: "Assets/Frames/"` to match. This is a one-off; for new decks, follow the canonical `Deck Edits/` convention.

## What this looks like in practice for a new deck

```
magic-{artist-slug}-deck/
├── index.html              # Generated from YAML
├── Assets/
│   ├── {artist-slug}-hero.jpg            # ← you provide
│   ├── {artist-slug}-superfans.jpg       # ← you provide
│   └── Frames/
│       └── Deck Edits/
│           ├── Fanverse.png              # ← copy from a recent deck
│           ├── Gamification.png          # ← copy from a recent deck
│           ├── Fan Chat.png              # ← copy from a recent deck
│           ├── Shop.png                  # ← copy from a recent deck
│           └── Magic Pulse.png           # ← copy from a recent deck
└── preview-server.js       # Copy from a recent deck
```

## Photo selection rules (per deck, learned the hard way)

### Hero photo (s1)

- **Portrait orientation, head-and-shoulders or full-body** — not landscape
- **Single subject** (not a group shot) — the artist alone
- **High contrast** on the right side — that side will be fully visible; the left fades to navy
- **No busy background** on the left edge — the gradient mask blends from the navy slide background and a busy left edge fights it
- **Resolution**: at least 1000px wide. Higher is fine, the browser scales down.
- **Format**: JPEG or PNG. PNG only if there's a real transparency need (rare).

### Hero photo mirroring (Gims case)

If your hero photo has the artist facing **left** (looking out of the slide), set:

```yaml
s1_hero_mirrored: true
```

This flips the image horizontally (`scaleX(-1)`) AND flips the gradient mask direction (`to left` instead of `to right`) so the photo looks correct and the fade still goes the right way. Per [[hero-blur-rule]].

### Superfans photo (s-superfans)

- **Same constraints as s1** but ideally a different photo
- **Live/crowd moment** preferred over a studio portrait — this slide is about the fan relationship
- **Lighter/airier** mood than s1 if possible — gives the deck visual variation

### Frame images (s5 + s8 shared)

- **Don't change these per deck** unless Magic launches new product UI
- They're product mockups; they should look like screenshots of the Magic app
- Standard set: `Fanverse.png`, `Gamification.png`, `Fan Chat.png`, `Shop.png`, `Magic Pulse.png`
- ~720×1560 portrait (iPhone mockup proportions)

## Object-position fine-tuning

If the hero photo crops a face awkwardly (e.g. eyes get cut off), tweak `s1_hero_object_position` in the YAML. Default is `center 30%` (top-weighted). Examples:

- `center 30%` — default, good for most portraits
- `center top` — face is near top of image, anchor to top
- `40% 30%` — face is slightly left of center
- `60% 25%` — face is slightly right of center, prefer top

Try a value, regenerate, eyeball. Iterate.

## Future automation idea

If the imagery setup becomes a recurring friction point, two options:

1. **Image upload as a /magic-slides step** — extend the skill to ask "drop hero photo here?" before generating; auto-suggest the right object-position
2. **Image library** — maintain a master `Assets/Frames/` set in a central location; the generator symlinks rather than copies

Neither is built yet. Manual copy works fine at current volume.
