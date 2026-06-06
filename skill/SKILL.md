---
name: magic-slides
description: Spin up a new Magic artist deck end-to-end — verify facts, draft YAML profile, generate HTML, lint, preview, commit. Use when the user types /magic-slides or says "start a new artist deck", "set up a deck for [artist]", "create a Magic deck for [artist name]".
---

# /magic-slides — new Magic artist deck

You are guiding the user through creating a brand-new Magic artist deck from scratch. The end state: a generated, linted, browser-previewed deck ready for the user to approve before pushing to GitHub.

**Hard constraints — never break these:**
- NEVER fabricate songs, albums, tours, venues, dates, or stats. Web-search to verify EVERY claim before putting it in the deck. If unverifiable, ask the user. (Rule: [[rule-never-fabricate]] in memory.)
- NEVER push to GitHub without explicit user approval after they've eyeballed the preview.
- NEVER write to a deck's `index.html` until the preview is approved — always write `index.test.html` first.
- Always read [[magic-deck-tool]] and [[round-trip-status]] memory + `magic-design-system/magic-deck-tool/notes/` before starting.

## Reference

Tooling lives at `magic-design-system/magic-deck-tool/`:
- `template/index.html` — Jinja2 deck template
- `generate.py` — renders YAML → HTML
- `lint.py` — checks deck against all memory rules
- `examples/{twinsmatic,toto,gims}.yaml` — copy one as the starting profile

## Step-by-step flow

### 1. Gather basics (ask in one batch with AskUserQuestion)

There are only TWO meaningful per-artist axes in Magic decks today:

1. **Pulse type**: **concert / tour / event** OR **album drop**. That's it. This drives phase ribbon labels, CRM card flavour, revenue defaults, capacity bullet shape.
2. **The anchor moment itself** (whatever the user tells you): venue + date for concert/event/tour, OR release month + album name for album drop. **NO assumed default venue (especially NOT Accor — Accor was just the venue for Toto/Gims, not a Magic-wide default).**

Ask the user:
- **Artist name** (display form, e.g. `Aya Nakamura`; preserve lowercase brands like `twinsmatic`)
- **Pulse type**: concert/tour/event vs album drop
- **Anchor mode** (NEW — ask this BEFORE web-searching, to avoid wasted verification):
  - **Real confirmed booking** — user has insider info, give exact venue/date
  - **Speculative pitch** — user is pitching Magic to the artist's team using a proposed venue/date; treat as the deck's hypothesis, no need to "verify" it externally
  - **Hypothetical demo / template** — clearly-flagged placeholder
- **Anchor details** based on pulse + mode (venue + date for concert/event/tour; release month + album name for album drop). Whatever the user says is what goes in. Don't web-search to validate the venue/date — that's their input, not a fact-claim to challenge.

Save the answers; don't proceed without them.

### 2. Verify the artist's real facts with web search

(Skip this step entirely if anchor mode is "hypothetical demo".)

Web-search for context that will populate CRM card content, NOT to second-guess the user's anchor:
- Genre / scene
- Recent release (album, single, EP)
- Label
- Recent / signature live moments
- Fan name / fan culture
- Notable collaborators

Pull from official sources where possible (artist's own socials, official announcement, Spotify/Apple artist pages).

Compile a **facts brief**: 5-10 bullet points the user must confirm. Format:

```
Here's what I verified about {artist}:
- Genre / scene: ...
- Recent release: ...
- Next anchor moment: ...
- Notable collaborators: ...
- Anything specific to their fanbase (signature ad-libs, fan nicknames, recurring imagery): ...

Anything wrong or missing? I'll only use confirmed facts in the deck.
```

Wait for explicit user approval. If something's wrong, ask follow-ups and re-verify before proceeding. If the artist is obscure or you can't find solid sources, say so plainly and ask the user to provide the facts manually.

### 2b. Verify the artist's AUDIENCE SIZE — drives revenue calculator defaults

Before drafting the YAML, web-search the artist's measurable audience to set realistic `sim_*` values:

- **Spotify monthly listeners** (primary signal for music artists)
- **Instagram followers** (cross-check)
- **YouTube subscribers** (cross-check)
- **TikTok followers** (for younger artists)
- **Recent tour gross / venue capacities** (sanity for paying-fan scale)

Compile and present:

```
Audience snapshot for {artist}:
- Spotify monthly listeners: {N}M
- Instagram: {N}M followers
- (other relevant signals)

Proposed revenue calculator defaults (concert pulse, 15% conversion):
- sim_default_reach: {X}M     (≈ {pct}% of Spotify monthly listeners — Magic-addressable audience)
- sim_default_fans: {Y}M      (reach × 15%)
- Tier breakdown scales from there

Does {X}M reach feel right, or should we adjust before drafting?
```

Reach is NOT the artist's total audience — it's the slice Magic can realistically convert into a Fanverse. Defaults from existing decks for calibration:
- Toto (regional francophone star): 4M reach, 600K fans, €491k gross
- Twinsmatic (producer, smaller scale): 1M reach, 100K fans, €81.8k gross
- Global pop stars (Sabrina-scale): ballpark 10-20M reach, 1.5-3M fans, €1-2M+ gross

Wait for user approval before locking in the calculator numbers.

### 3. Pick a starting YAML profile

There are TWO canonical starting profiles, one per pulse type:

- **Album drop** → copy `examples/twinsmatic.yaml` (album pulse, lowercase brand example)
- **Concert / tour / event** → copy `examples/toto.yaml` (single-date) OR `examples/gims.yaml` (multi-night). Either works for any concert-style pitch — pick whichever skeleton is closer to the artist's situation.

Save as `examples/{artist-slug}.yaml`. The `{artist-slug}` is lowercase + hyphens (e.g. `aya-nakamura`).

### 4. Adapt the YAML to the artist

Per the [[artist-adaptation-scope]] memory rule, only certain fields change per artist:
- `deck_slug`, `deck_title`, `artist_name_display`, `artist_name_pill` (preserve lowercase if applicable; set `artist_name_pill_lowercase_flag: true`)
- `s4_centre_line1` / `_line2` / `_line1_size` (artist name split for the Fanverse sun)
- `cover_trigger_*` (EN + FR pair)
- `s1_trigger_*` (EN + FR pair)
- `s1_hero_img_src` + `s1_hero_img_alt` + `s1_hero_object_position` + `s1_hero_mirrored`
- `s_superfans_hero_img_src` + `s_superfans_hero_object_position`
- `frames_path_prefix` (default `Assets/Frames/Deck Edits/`; some decks use parent — check what asset folder you have)
- `s5_body_*` (mentions the artist name)
- `momentum_sub_*`
- `phase_*_label_*` (depend on pulse type — pull from [[crm-artist-dna]] phase ribbon naming table)
- `crm_headline_*_html`, `crm_sub_*`, `crm_months[...]` (the CRM card grid — per [[crm-artist-dna]] translate the canonical concert/album skeleton to the artist's DNA)
- `sim_*` revenue calculator defaults (use pulse-type defaults from [[magic-deck-tool]] notes)
- `s13_capacity_bullet_*_html`, `s13_moment_bullet_*_html`

Everything else stays canonical — DO NOT improvise.

For CRM cards: keep the structure (build-up cards → peak ★ cards → after cards), translate each card's `nm` (name) + `hk` (hook copy) to the artist's flavour using [[crm-artist-dna]] as the translation table. Identify pulse type FIRST. Don't put anticipation cards in the D-day peak phase.

### 5. Set up the deck folder + give the user the asset brief

Create `magic-{artist-slug}-deck/` as a sibling of the other deck folders.

Structure to copy from a reference deck (e.g. magic-twinsmatic-deck):
- `Assets/` subfolder for images
- `preview-server.js` (copy verbatim)
- `.git/info/exclude` with `index.test.html` added so it never gets committed

#### THE ASSET BRIEF — what the user needs to source + customise

There are **3 photos + 5 Figma mockups** per deck. Compile the brief and present to the user (so they can collect/produce in parallel while you continue drafting):

##### A. The 3 photos

1. **s1 hero (the "cool" photo)** — `Assets/{artist-slug}-hero.jpg`
   - Vibe: COOL. On stage in performance mode, OR an iconic pose
   - **Critical**: dead/quiet space on the LEFT side (the left half fades to navy via gradient mask; busy left side fights the fade)
   - Portrait orientation, ~1000×1250+, single subject
   - If artist faces LEFT in photo → flag `s1_hero_mirrored: true` in YAML

2. **s4 Fanverse centre (the "iconic" square photo)** — used in the round centre of the solar-system slide
   - Square aspect ratio (it sits inside a round frame)
   - Close-up of face OR something they're very famously associated with
   - Should read instantly at small size — high contrast face shot works best

3. **s-superfans / outro hero (the "warm" photo)** — `Assets/{artist-slug}-superfans.jpg`
   - Vibe: WARM, personality-forward, inviting
   - Should make a viewer want to *join their Fanverse* — show the artist as someone you'd want to be in community with
   - Same portrait + dead-space-on-the-correct-side rules as s1
   - Outstanding, iconic, or radiating personality

Tell the user explicitly what each photo needs to *do* (cool / iconic / warm) so they brief their team or pick from existing material appropriately.

##### B. The 5 Figma mobile frames (require per-artist customisation in Figma, then export PNG)

These ALL need the artist's face / brand swapped in. Land each PNG at `Assets/Frames/Deck Edits/{name}.png`:

1. **Fanverse.png** — overall Fanverse home mock. Avatar = artist, copy + activities themed around the deck's pulse (concert vs album)
2. **Gamification.png** — XP/coin progression UI. Avatar = artist. Simpler edit, mostly just face swap.
3. **Fan Chat.png** — chat mockup. Needs **3 chat messages + 1 poll**, all themed around the deck's anchor activation:
   - For concert/tour: messages reference tour anticipation, ticket access, city the show is in; poll asks something like "Which support act?" or "Which surprise track?"
   - For album: messages reference single drops, listening sessions, lyric reveals; poll asks something like "Favourite track?" or "Which deluxe addition?"
4. **Shop.png** — merch shop mockup. Needs **4 cool merch items** themed to the artist:
   - Use real-world signature items where possible (e.g. for Sabrina: bow accessories, lingerie-inspired tee, vinyl in heart-shape, Coachella-exclusive hoodie)
   - Each item needs a **coin price** that maps to a real € value
   - **Coin-to-EUR formula**: TODO — extract from existing decks (Laura has worked out conversions e.g. "85K coins for a VIP bundle"). Until formulised, ask Laura for the rate or look at recent decks' shop frames.
5. **Magic Pulse.png** — phone-mock insights dashboard. Avatar = artist; insight strings can stay canonical or be lightly themed.

If the user can't source/produce all 5 immediately, still proceed with HTML generation — broken-image alt text will surface what's missing in preview, then fill in incrementally.

##### C. Fan Chat content suggestions (you draft, user approves)

Per the 3 chats + 1 poll requirement, draft based on the deck's anchor + verified artist DNA. Format as:

```
Fan Chat content for {artist} (around {anchor} activation):

Chat 1: [fan name] — "[message that references something specific to the activation]"
Chat 2: [fan name] — "[message expressing the kind of fan culture that already exists IRL]"
Chat 3: [fan name] — "[message about something verified — recent song, recent moment, fan ritual]"

Poll: "[question themed to the activation, with 2-4 fan-relevant options]"
- Option A: ...
- Option B: ...
- Option C: ...
- Option D: ...
```

NEVER invent fan ritual / nickname / recent moment — use only what was verified in step 2. Reuse verified material from the CRM cards where it overlaps.

##### D. Merch items suggestions (you draft, user approves)

For the 4 merch slots, draft based on the artist's real merch aesthetic + the anchor moment. Format as:

```
Merch lineup for {artist}'s Coachella drop:
1. [Item name] — [short desc] — {coin_price}c (≈ €{eur_price})
2. ...
3. ...
4. ...
```

Pricing math: TODO formula from Laura. Until formulised, ballpark from recent deck examples or ask Laura.

### 6. Generate the test render

```bash
cd magic-design-system/magic-deck-tool
python3 generate.py examples/{artist-slug}.yaml -o ../../magic-{artist-slug}-deck/index.test.html
```

### 7. Run the linter

```bash
python3 lint.py ../../magic-{artist-slug}-deck/index.test.html
```

If there are ERRORs: fix them before showing the user. WARNs are OK to show — flag them and let the user decide.

### 8. Open browser preview

Add an entry to `.claude/launch.json` for the new deck (port = next free port, e.g. 4179 onwards). Then:

```
preview_start({name: "magic-{artist-slug}-deck"})
preview_eval({serverId, expression: "window.location.href = 'http://localhost:{port}/index.test.html?scroll'"})
preview_screenshot({serverId})  # for the user-visible report
```

Give the user the file:// URL to open in their own browser too (Safari preview may render fonts slightly differently from headless preview).

### 9. Walk through verification

Ask the user to check:
1. **Cover slide** — name, trigger line correct?
2. **s1 hero photo** — right image, right side, masked properly?
3. **s4 Fanverse centre** — name reads correctly?
4. **s7 CRM grid** — card titles + hooks make sense for this artist?
5. **s10 revenue calculator** — numbers feel right for this artist's scale?
6. **s13 outro** — capacity bullet appropriate?
7. **All FR text renders** without overflow (toggle the EN/FR switcher if possible)

Iterate on YAML, regenerate, reload, until user is happy.

### 10. Promote to live + push (ONLY after explicit user OK)

```bash
# Overwrite live index.html with the approved render
python3 generate.py examples/{artist-slug}.yaml -o ../../magic-{artist-slug}-deck/index.html

# Set up GitHub remotes IF this is the first push (ask user about repo creation)
cd ../../magic-{artist-slug}-deck
git init  # if not already initialized
# Ask user: does a vibeonmagic/magic-{slug}-deck repo exist on GitHub? lolacolafola/magic-{slug}-deck?
# If yes, add remotes:
git remote add origin https://github.com/lolacolafola/magic-{slug}-deck.git
git remote set-url --add --push origin https://github.com/lolacolafola/magic-{slug}-deck.git
git remote set-url --add --push origin https://github.com/vibeonmagic/magic-{slug}-deck.git

# Commit + push
git add index.html Assets/ preview-server.js
git commit -m "Initial Magic deck for {Artist Name}

Generated from magic-deck-tool template."
git push -u origin main
```

After push, give the user the 3 URLs (per [[deck-deploy-rule]]):
- Presentation: `https://vibeonmagic.com/magic-{slug}-deck/`
- EN scroll: `https://vibeonmagic.com/magic-{slug}-deck/?scroll&en`
- FR scroll: `https://vibeonmagic.com/magic-{slug}-deck/?scroll&fr`

(Or `lolacolafola` equivalents.)

### 11. Update memory if anything surprising came up

If new artist-specific facts were verified (similar to [[project-twinsmatic-facts]]), save them as a project memory so future sessions don't re-verify.

## When NOT to proceed

- If web search returns thin / contradictory results about the artist → STOP, ask for source documents from the user.
- If lint errors persist after one round of fixing → STOP, surface to the user.
- If the user can't yet provide the hero image → STOP at step 5, generate later.

## Quick checklist before declaring "done"

- [ ] Linter passes (0 errors) on `index.html`
- [ ] All 3 URL forms work in browser (default, ?scroll, ?presentation if applicable)
- [ ] EN and FR both render without overflow
- [ ] User explicitly approved the visual
- [ ] Pushed to both vibeonmagic + lolacolafola
- [ ] User has the 3 deploy URLs in hand
