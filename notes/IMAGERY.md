# Imagery + asset customisation per deck

Every new deck needs **3 photos + 5 Figma mockup PNGs**, each playing a specific role. The HTML template references them by path; if a file is missing, browsers show broken-image alt text instead.

## Quick map: what goes where

```
magic-{artist-slug}-deck/Assets/
├── {artist-slug}-hero.jpg             # s1 — "cool" photo (on stage / iconic pose)
├── {artist-slug}-fanverse.jpg         # s4 — "iconic" square photo (round centre frame)
├── {artist-slug}-superfans.jpg        # s-superfans — "warm" personality photo
└── Frames/
    └── Deck Edits/
        ├── Fanverse.png               # Artist-customised
        ├── Gamification.png           # Artist-customised
        ├── Fan Chat.png               # Artist-customised (3 chats + 1 poll)
        ├── Shop.png                   # Artist-customised (4 merch items)
        └── Magic Pulse.png            # Artist-customised
```

---

## The 3 photos — what each one needs to *do*

Each photo plays a distinct emotional role. Brief the photographer / image-sourcer in these terms:

### 1. s1 hero — "the cool photo"

**What it does:** First real image of the artist in the deck. Sets the tone: this artist is a serious creative force.

**Brief:**
- **Vibe**: COOL. On stage in performance mode, OR an iconic pose
- **Critical layout requirement**: dead/quiet space on the **LEFT** side of the image. The left half fades to navy via the gradient mask — a busy left edge fights the fade
- **Subject**: solo (the artist alone, not a group shot)
- **Orientation**: portrait, ~1000×1250+ resolution
- **Background**: high contrast on the right (will be fully visible), calm/dark on the left

**If the artist faces LEFT in the photo** → set `s1_hero_mirrored: true` in YAML. The template flips the image AND reverses the gradient mask direction (`to left` instead of `to right`).

### 2. s4 Fanverse centre — "the iconic square photo"

**What it does:** Sits inside a round frame at the centre of the solar-system slide. Must be instantly recognisable at small size.

**Brief:**
- **Aspect ratio**: square (it sits inside a round mask)
- **Composition**: close-up of the artist's face, OR something they're VERY famously associated with (signature item, recognisable silhouette, etc.)
- **Should read instantly at thumbnail size** — high contrast face shot usually wins
- **Centre-weighted**: subject in the middle, since the round mask crops corners

### 3. s-superfans / outro — "the warm personality photo"

**What it does:** This is the slide that says "join their Fanverse." Needs to make viewers want to be part of this artist's community.

**Brief:**
- **Vibe**: WARM, personality-forward, inviting
- **Tone**: outstanding, iconic, or radiating personality — something that makes you want to be in their community
- **Same portrait + dead-space-on-correct-side rules as s1**
- **Different mood from s1** — if s1 was "cool on stage", this is "warm with their people / smiling / inviting"

---

## The 5 Figma mobile frames — per-artist customisation

These are the highest-friction per-deck task today (~1-2 hours of Figma per new deck). All need artist face / brand / content swapped in.

### Fanverse.png

Overall Fanverse home mock. Swap:
- Avatar = artist's face
- Display name = artist's name
- Activities visible = themed to the deck's pulse (concert vs album mechanics)

### Gamification.png

XP / coin progression UI. Simpler edit:
- Avatar = artist's face
- (Levels / coin amounts can stay canonical)

### Fan Chat.png — 3 chats + 1 poll, themed to the activation

Three fan-side chat messages plus one poll, ALL themed around the deck's anchor pulse.

**For concert / tour pulse:**
- Chats reference tour anticipation, ticket access, the specific city the show is in
- Poll asks something like "Which support act would you want?" or "Which surprise track?"

**For album pulse:**
- Chats reference single drops, listening sessions, lyric reveals
- Poll asks something like "Favourite track?" or "Which deluxe addition?"

**Content sourcing rule (NEVER fabricate)**: chat content can only reference verified material — real recent songs, real fan rituals, real moments. The `/magic-slides` skill drafts these and asks for user approval before they go into Figma.

### Shop.png — 4 merch items with coin pricing

Four cool merch items themed to the artist's actual real-world aesthetic.

**Content guidance:**
- Use real-world signature items where possible (artist's known fashion, recurring imagery, festival-exclusive drops, vinyl variants)
- Each item displays a **coin price** that should map to a real € value

**Coin-to-EUR pricing — TODO formula**

Laura has worked out conversions from existing decks (e.g. "85K coins for a VIP bundle" maps to some EUR figure). Until formulised in this file, options:

1. Pull the formula from an existing deck's Shop frame
2. Ask Laura for the rate
3. Use this rough placeholder (REPLACE WITH REAL FORMULA WHEN AVAILABLE):
   - 1,000 coins ≈ €X (TBD)
   - VIP/premium items: 50K-100K coins
   - Mid-tier items (hoodie, vinyl): 10K-30K coins
   - Entry items (sticker, badge): 1K-5K coins

When the formula is documented here, the `/magic-slides` skill should compute coin prices from EUR targets automatically.

### Magic Pulse.png

Phone-mock insights dashboard. Swap:
- Avatar = artist's face
- Insight strings can stay canonical OR be lightly themed (the canonical "Mood dashboard / Discovery map / Targeted messaging / Fan moments" headers are brand-locked per the template)

---

## Object-position fine-tuning (for the 3 photos)

If a hero photo crops faces awkwardly, tweak `s1_hero_object_position` / `s_superfans_hero_object_position` in YAML. Default is `center 30%`. Examples:

- `center 30%` — default, top-weighted
- `center top` — face is near top of image
- `40% 30%` — face slightly left of centre
- `60% 25%` — face slightly right of centre, prefer top

Try a value, regenerate, eyeball. Iterate.

---

## Future automation idea — Figma frames

The 5 mobile frames are by far the largest per-deck time sink. See [project_figma_automation memory](../../../.claude/projects/-Users-laura-AI-Projects-Magic-Slides/memory/project_figma_automation.md). Master Figma file with named text/image layers, generator swaps them from the same YAML profile, exports PNGs straight to `Assets/Frames/Deck Edits/`. Could collapse 1-2 hours to ~30 seconds.
