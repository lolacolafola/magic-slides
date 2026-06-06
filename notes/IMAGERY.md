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

**Coin-to-EUR pricing — confirmed rule (2026-06-06)**

Rough mapping (it's not exact math, treat as flexible ranges):

> **1,000 coins ≈ €1** as a baseline. For mid-to-premium items, coin price intentionally runs HIGHER than real EUR cost (showcases the "fan value" / exclusivity premium).

**Hard design constraint: coin prices must fit in 5 digits (max 99,999).** No item can be priced 100K+ coins.

Per-item bands from Laura's existing decks:

| Item class | Coin price band | Real EUR cost | Notes |
|---|---|---|---|
| **CD** (physical music) | ~15K coins | ~€15 | entry-tier; close to 1:1 |
| **T-shirt** | 25-35K coins | €25-35 | close to 1:1 |
| **Hoodie / vinyl / mid-tier** | 45-65K coins | €40-50 | coin price runs above real cost |
| **VIP bundle / premium experience** | 80-95K coins | €60-85 | premium markup; cap at 99K for the 5-digit limit |

The skill should:
1. Draft 4 merch items themed to the artist's actual style
2. Apply a coin price from the band that matches each item's category
3. For mid-tier and VIP items, choose a coin price that sits ABOVE the realistic EUR cost (rewards engagement)
4. Never exceed 99,999 coins (design constraint)
5. Show user the band + chosen value so they can fine-tune (e.g. an exclusive Coachella tee might lean toward 35K rather than 25K to reflect scarcity)

Exact-math vibe is wrong — these are pitch decks, not real shop prices, so the bands above are guidance not strict rules.

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
