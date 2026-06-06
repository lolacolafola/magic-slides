# Triangulation — Toto / Gims / Twinsmatic

Reference decks:
- T = `magic-toto-deck/index.html` (concert pulse, Accor Arena, ElGrandeToto, 3675 lines)
- G = `magic-gims-deck/index.html` (concert pulse, multi-night La Défense, GIMS, 3669 lines)
- W = `magic-twinsmatic-deck/index.html` (album pulse, producer DNA, twinsmatic, 3671 lines)

All three decks each contain exactly **12 `<div class="slide">` blocks**, in the same source order, with the same DOM skeleton on every slide. Diffs:
- T vs G = 235 lines (cleanest pair — pure concert vs concert)
- T vs W = 323 lines (concert vs album — biggest divergences)
- G vs W = 266 lines

Outside the diff'd hunks, every line is byte-identical. This is the single most important finding for the template: the canonical scaffold is just one file with about 30 well-bounded swap sites.

---

## 1. Slide inventory

Twelve slide blocks, in source order. IDs are non-sequential by design (s0, s1, s2, s-momentum, s4, s5, s-applied, s8, s11, s10, s-superfans, s13) — these are historical and must be preserved (the `dots`/`nav` JS keys off them).

| # | DOM id | Section comment (T:L1527+) | Purpose | Pulse-type dependent? |
|---|---|---|---|---|
| 1 | `s0` | S0 — COVER | Cover: Magic logo + "Magic for {artist}" + trigger line | trigger line only |
| 2 | `s1` | S1 — WELCOME TO MAGIC | Welcome / problem-statement split with right-side hero photo + mask | hero img + trigger paragraph |
| 3 | `s2` | S2 — THE PROBLEM | "You have the audience. You just don't own it." — 4-row table + Magic-changes-that box | NO (fully canonical) |
| 4 | `s-momentum` | S-MILESTONES — WHERE THE PEAKS LAND | Momentum chart + phase ribbon (Build-up / Concert / After) | YES (ribbon labels + sub copy) |
| 5 | `s4` | S4 — ENTER YOUR FANVERSE | Solar-system: artist name at centre, planet ring of features | centre name only (planets canonical — see [fanverse_locked]) |
| 6 | `s5` | S5 — A REASON TO RETURN EVERY DAY | 4-image grid (Fanverse / Gamification / Fan Chat / Shop) + body copy | body copy artist name; Gims uses `Frames/Deck Edits/` path |
| 7 | `s-applied` | S5/funnel block then S-FUNNEL header (line 2045) — actually the **CRM plan** slide | 5-month journey grid with j-cards across Build-up / Concert / After phases | YES — **biggest divergence**; all card titles/copy + month labels + phase ribbon swap |
| 8 | `s8` | S8 — MAGIC PULSE (was FRM) | Magic Pulse phone mock + insights | NO (Gims uses `Deck Edits/Magic Pulse.png`) |
| 9 | `s11` | S-SUPERFANS / S11 — INCREASE EVERY REVENUE STREAM | Revenue impact slide | NO |
| 10 | `s10` | S10 — GET PAID | Interactive revenue calculator (reach → fans → tiers → net) | YES (default reach/fans/€ values per artist scale; concert vs album conversion rate 15% vs 10%) |
| 11 | `s-superfans` | (header at L2253 "S-SUPERFANS — YOUR FANVERSE, YOUR FANS") | Fan love quotes slide | NO (Toto has an extra ElGrandeToto secondary hero image here) |
| 12 | `s13` | S13 — RECAP / CTA | Flywheel recap: 3 bullets (place / moment / bond) + Magic wordmark | YES (capacity bullet per [artist_adaptation_scope]) |

Note on section-comment vs DOM-id mismatch: the `<!-- S-FUNNEL — ACQUISITION FUNNEL (TOTO) -->` comment at T:L2045 sits between two slides and labels the next slide (`s5`) as the funnel — but `s5` is in fact the "always-on" grid. The CRM plan slide is `s-applied` (T:L2128). Comments are decorative; trust the `id`.

---

## 2. Per-slide variant table

Format: `T="…" | G="…" | W="…"` → `{{placeholder_name}}`.
All line numbers reference Toto (`magic-toto-deck/index.html`) unless noted.

### s0 — Cover (T:L1530-1559)

- `<title>` (T:L6): `Magic — ElGrandeToto` | `Magic — GIMS` | `Magic — twinsmatic` → `{{deck_title}}`
- Cover headline span (T:L1548-1549): `Magic for<br><span class='gt cover-title'>ElGrandeToto</span>` (lowercase for W: `twinsmatic`) → `{{artist_name_display}}` (also drives `data-en-html` / `data-fr-html`)
- Trigger line (T:L1555-1556): EN/FR pair —
  - T: `Built for Salgoat world tour · Accor Arena · 27 March 2027` / `Pensé pour le Salgoat world tour · Accor Arena · 27 mars 2027`
  - G: `Built for Carpe Diem tour · La Défense Arena · 16-17 December 2026` / `Pensé pour la tournée Carpe Diem · La Défense Arena · 16-17 décembre 2026`
  - W: `Built for the next album · Out October` / `Pensé pour le prochain album · Sortie en octobre`
  → `{{cover_trigger_en}}` / `{{cover_trigger_fr}}`

### s1 — Welcome (T:L1565-1598)

- s-num text (T:L1569): `02 / 10` (T) vs `02 / 12` (G,W) — **DRIFT: Toto numerator total is wrong; canonical is `/12`** since all decks have 12 slide blocks.
- Eyebrow pill (T:L1573): `✦ ElGrandeToto` | `✦ GIMS` | `✦ twinsmatic` (W adds `style="text-transform:none;"` to preserve lowercase) → `{{artist_name_pill}}` (+ optional `style="text-transform:none;"` for lowercase artists). Always default `.tag` blue, never `.tag-pu` ([pill-text-color]).
- Trigger paragraph (T:L1584-1585):
  - T: `Accor on 27 March is the trigger. Magic is what turns one night into a fandom that keeps going.`
  - G: `La Défense Arena on 16-17 December is the trigger. Magic is what turns those two nights into a fandom that keeps going.`
  - W: `The album is the trigger. Magic is what turns a release week into a fandom that keeps going.`
  → `{{s1_trigger_en}}` / `{{s1_trigger_fr}}`
- Hero img (T:L1592):
  - T: `Assets/76e84c62-elgrandetoto2-1010x1263.jpg`, `alt="ElGrandeToto"`, mask `to right`
  - G: `Assets/welcome-gims.jpeg`, `alt="GIMS"`, mask `to left` + `transform:scaleX(-1)` (mirrored)
  - W: `Assets/Deck Edits/Group 1171275387.png`, `alt="twinsmatic"`, mask `to right`
  → `{{s1_hero_img_src}}` / `{{s1_hero_img_alt}}` / `{{s1_hero_mask_direction}}` (enum: `right`|`left`) / `{{s1_hero_extra_transform}}` (optional `transform:scaleX(-1)`) — see [hero_blur_rule].
  Note the sibling gradient overlay div at T:L1593 has the **same** color/gradient direction in all 3 decks regardless of which way the image is mirrored (it always fades `to right`); only the `<img>` mask flips.

### s2 — The Problem (T:L1602-1676)

**Fully canonical across all 3 decks** — zero diff hunks. Lift verbatim.

### s-momentum (T:L1689-1804)

- s-num (T:L1693): `04 / 14` (T) vs `04 / 12` (G,W) — **DRIFT: Toto says `/14`**, also wrong.
- Sub body (T:L1699):
  - T: `Magic turns Accor and everything around it into fan experiences…`
  - G: `Magic turns the Carpe Diem tour and everything around it into fan experiences…`
  - W: `Magic turns the album drop and everything around it into fan experiences…`
  → `{{momentum_sub_en}}` / `{{momentum_sub_fr}}`
- Phase ribbon SVG `<text>` x positions (T:L1787/1791/1795) — **DRIFT: Toto has `x="369"`, `x="875"`, `x="1178"`; Gims+Twins use the canonical `367 / 872 / 1176`** per [svg_arrow_text_centering]. Always emit canonical.
- Phase ribbon labels (T:L1787-1795 tspans) — see "Per-pulse divergences" below.

### s4 — Fanverse solar system (T:L1809-2042)

- s-num (T:L1813): `05 / 10` (T) vs `05 / 12` (G,W) — DRIFT.
- Sub body (T:L1822): T/G identical; W rewrites with `data-i18n="html"` + non-breaking spaces.
- **Centre sun text only** (T:L1890-1891) — split across two `<span>`s:
  - T: `ELGRANDE` (size 11px wt 700) + `TOTO` (size 10px wt 400) — short tag with subtitle
  - G: `GIMS` (size **15px**) + (no second line)
  - W: `twins` + `matic` (split lowercase)
  → `{{s4_centre_line1}}` / `{{s4_centre_line2}}` / `{{s4_centre_line1_size}}` (default 11, Gims 15)
- **Planet labels are CANONICAL** ([fanverse_locked]); each `<text>` for Magic Quest / Magic Lens / Mystery Box / Magic Unlimited (T:L1743-1754).
  - DRIFT: T leaves these labels as bare text; W wraps them in `<tspan data-en="..." data-fr="...">` (correct per [product_names], because product names don't translate but i18n switcher needs the wrapping to keep them visible). G also has them un-wrapped. **Canonical = W's wrapped version.**

### s5 — Always on grid (T:L2051-2125)

- s-num (T:L2054): `06 / 10` vs `06 / 12` — DRIFT.
- Body copy (T:L2062-2063): swaps artist name (`ElGrandeToto` / `GIMS` / `twinsmatic`).
- 4 image srcs (T:L2072/2079/2086/2093):
  - T+W: `Assets/Frames/Fanverse.png`, `…/Gamification.png`, `…/Fan Chat.png`, `…/Shop.png`
  - G: `Assets/Frames/Deck Edits/{same names}.png` — **DRIFT or Gims uses a different asset folder**; need to confirm whether Gims-specific edits exist or whether the path should be unified.
  → Use canonical `Assets/Frames/{Fanverse|Gamification|Fan Chat|Shop}.png` and document a deck-level `{{frames_path_prefix}}` override.

### s-applied — The CRM plan (T:L2128-2199) — **HEAVIEST DIVERGENCE**

- s-num: same drift `07/10` issue.
- Headline `class="h"` (T:L2137-2138):
  - T: `The road to <span class='gt'>Accor and beyond.</span>`
  - G: `The road to <span class='gt'>La Défense and beyond.</span>`
  - W: `The build-up to <span class='gt'>the album, and beyond.</span>`
  → `{{crm_headline_en_html}}` / `{{crm_headline_fr_html}}`
- Sub line (T:L2138):
  - T: `Here's an example of ElGrandeToto's Fanverse in action, from his first stream to the next tour.`
  - G: same pattern (GIMS)
  - W: `We take our library of features and experiences and tailor them to twinsmatic, making every pulse point bigger and keeping the engagement going from one to the next.`
  → `{{crm_sub_en}}` / `{{crm_sub_fr}}`
- Phase ribbon `<div class="pseg">` (T:L2143-2145) — same labels as s-momentum SVG ribbon; must stay in sync.
- **Five month columns, each with a `mlabel` + 2 `j-card`s**:
  - T: SEPT / OCT-NOV / DEC / JAN-FEB / **★ MAR** (Build-up months → Accor month uses `class="mlabel bercy"`) / APR / MAY
  - G: JUN / JUL-AUG / SEPT / OCT-NOV / **★ DEC** / JAN / FEB
  - W: JUN / JUL / AUG / SEP / **★ OCT** / NOV / DEC
  → `{{crm_month_1}}` … `{{crm_month_7}}` + a flag for which one gets `.bercy` (always the concert/release month) → `{{crm_pulse_month_index}}`
- **Each j-card carries `nm` (name), `hk` (hook copy), `rwd`/`cds` (icon SVGs).** All `nm` and `hk` strings vary per deck; icons are canonical SVG. See per-pulse table in CONDITIONALS.md.

### s8 — Magic Pulse (T:L2204-2251)

- s-num (T:L2207): `08 / 10` vs `08 / 12` — DRIFT.
- Phone mock img (T:L2244): T+W = `Assets/Frames/Magic Pulse.png`; G = `Assets/Frames/Deck Edits/Magic Pulse.png`. Same drift as s5 — unify path.
- Everything else canonical.

### s11 — Increase every revenue stream (T:L2261-2308)

- s-num (T:L2264): `12 / 13` (T — wildly off) vs `09 / 12` (G,W). **DRIFT** — Toto is mis-numbered.
- Body copy fully canonical otherwise.

### s10 — Get paid (revenue calculator) (T:L2313-2441)

- s-num (T:L2316): `12 / 16` (T) vs `10 / 12` (G,W). **DRIFT** — Toto says `/16`. Canonical `10 / 12`.
- Default input values vary per deck scale:
  - `#sim-reach` value (T:L2341): T=`4M`, G=`4M`, W=`1M` → `{{sim_default_reach}}`
  - `.revshare` chip label (T:L2345): T=`15% TO MAGIC`, G=`15% TO MAGIC`, W=`10% TO MAGIC` → `{{sim_conversion_pct_label}}`
  - `#sim-fans` initial (T:L2349): T=`600K`, G=`600K`, W=`100K` → `{{sim_default_fans}}`
  - `#sim-bar-fan` and tier bars (T:L2384, 2387, 2393, 2396, 2402, 2405, 2411, 2414, 2427, 2429, 2431): all scale down proportionally for W. → `{{sim_*_amount}}` per tier
  - JS hard-coded conversion rate (T:L3147): `var fans = reach * 0.15;` (T) vs `* 0.10;` (W). → `{{sim_conversion_rate}}` (concert default 0.15, album 0.10)
- Tier names + structure canonical.

### s-superfans (T:L2443-2468)

- s-num (T:L2446): `09 / 10` vs `11 / 12` — DRIFT.
- Toto-only: second hero `<img>` (T:L2461-2463) with the comment `<!-- Right: ElGrandeToto image — same style as s1 (swap filename when concert photo is added) -->`. Gims removes that comment + the `gl gl-br` div (T:L2445 has both `gl-tl` and `gl-br`, Gims keeps only `gl-tl` — see diff line 270). Image src varies per artist.
  → `{{s_superfans_hero_img_src}}` (optional, but in practice all 3 have one)

### s13 — Recap / CTA (T:L2473-2520)

- s-num (T:L2476): `10 / 10` (T) vs `12 / 12` (G,W). **DRIFT** — final slide must read `12 / 12`.
- First bullet "A place for every fan" (T:L2492) — **CAPACITY BULLET** per [artist_adaptation_scope]:
  - T: `Accor holds 20,000 on 27 March. Magic opens a space for them, and for the millions who couldn't be there too.`
  - G: `La Défense Arena holds 40,000. Across two nights on 16–17 December, that's 80,000 fans. Magic opens a space…`
  - W: `a release reaches a moment, then fades. Magic opens a permanent space for every fan, on every release, forever.`
  → `{{s13_capacity_bullet_en_html}}` / `{{s13_capacity_bullet_fr_html}}` (HTML because the bold span is inline)
- Second bullet "Every moment shared" (T:L2498): artist name swap (`alongside ElGrandeToto` etc.) → `{{s13_moment_artist}}` (or just reuse `{{artist_name_display}}`)
- Third bullet "Every bond owned" — fully canonical.

### Footer / nav (T:L2527, T:L2562)

- `✦ Magic — For ElGrandeToto` (twice — nav at L2527, mobile leaderboard at L2562) → `{{nav_footer_label}}`.

### JS storage keys (T:L2607-2609)

- `magic-{slug}-deck-{edits|layout|images}-v1` → `{{deck_slug}}` (toto / gims / twinsmatic).

### PDF/download filenames (T:L2988, T:L3638)

- `magic_{slug}_deck_edited.html`, `Magic - {DisplayName}.pdf` → `{{deck_slug}}` + `{{artist_name_display}}`.

### Twinsmatic-only addition: `?scroll=` URL param (W:L2600-2602)

Twins adds:
```
} else if (urlParams.has('scroll')) {
  document.documentElement.classList.add('scroll-mode');
  document.body.classList.add('scroll-mode');
```
Toto and Gims don't have this branch. → Include in canonical template (it's strictly additive and won't break the other decks).

---

## 3. Shared / canonical blocks

Every line **outside** the diff hunks is byte-identical across all three decks. Concretely, this means the following can be lifted as-is into the template:

- Lines 1-1526 (head, all `<style>`, all SVG `<symbol>` defs, opening `#shell` / `#stage` / `#scaler`) — except `<title>` on L6.
- The entire s2 block (L1602-1676).
- s-momentum chart SVG path data + axis ticks (L1689-1804) except the phase-ribbon `<text>` tspans.
- The whole s4 starfield (L1827-1888) and planet ring DOM (L1894-onwards through L2042) except the centre-sun two `<span>`s (L1890-1891) and the planet `<text>` labels which should be wrapped per W's pattern.
- The 4 `<style>`/`<script>` blocks for the CRM grid (cards/layout CSS).
- The whole s8 phone-mock structure (L2204-2251) except the img src.
- The whole revenue model UI scaffold (L2313-2441) except the input default values and the JS conversion rate.
- Nav bar HTML, mobile leaderboard structure, all JS event handlers (L2526 onwards) except storage keys and download/PDF filenames.

Verbatim canonical anchors worth quoting in the template:
- `<div class="s-bar s-bar-pu"></div><div class="s-logo">✦ Magic</div><div class="s-num">{{n}} / 12</div>` — the slide-number bar pattern used on every slide ≥ s1.
- `<svg width="357" height="136" viewBox="0 0 357 136" ...>` — the Magic wordmark SVG (appears twice: s0 cover at L1539 and s13 outro at L2509). 100% identical across decks. Single inline asset.
- `<div class="gl gl-tl"></div><div class="grid"></div>` — standard slide chrome.

---

## 4. Per-pulse divergences (concert vs album)

The structural DOM is identical — only string contents and a handful of numeric defaults swap. The per-pulse branching falls into 4 well-defined surfaces:

### 4.1 Trigger/anchor copy (s0 cover, s1 trigger, s2 *unchanged*, s-momentum sub, s-applied sub, s13 capacity bullet)

Concert pulse phrases venue + date (`Accor on 27 March`, `La Défense Arena on 16–17 December`). Album pulse phrases the release (`the album`, `the album drop`, `the next album · Out October`). See per-slide table above.

### 4.2 Phase ribbon labels (s-momentum SVG L1787-1795 + s-applied `.pseg` L2143-2145)

| | Build-up label | Peak label | After label |
|---|---|---|---|
| Concert (T) | `Build-up · Sep - Feb` | `Concert · Mar` | `After the show · Apr - onwards` |
| Concert (G, multi-night) | `Build-up · Jun - Nov` | `Concerts · Dec` (plural) | `After the shows · Jan - onwards` (plural) |
| Album (W) | `Recruit & warm up · Jun - Sep` | `Album drop · Oct` | `Beyond the drop · Nov - onwards` |

The ribbon **structure** (3 segments, same SVG geometry, same x-coords 367/872/1176) is canonical; only label text + month range changes.

### 4.3 CRM j-cards (s-applied L2147-2197) — biggest divergence

Five month columns × 2 cards each = 10 cards. Each card has `{nm, hk, rwd?, cds}`. Card titles are themed to the pulse:

| Phase | Concert flavour (T) | Album flavour (W) |
|---|---|---|
| Build-up month 1 | `Connect & climb` / `City crew` | `Spotify connect` / `Plug a friend` |
| Build-up month 2 | `Casa hunt` / `Match the beat` | `Scan the wild` / `Magic Quest` |
| Build-up month 3 | `Toto tastes` / *(no 2nd)* | `twinsmatic tastes` / `Beat library` |
| Build-up month 4 | `Show vote` / `Golden ticket` | `Album pre-order` / `Final countdown` |
| Peak (★) | `Final countdown` / `City challenge` then `Collect at Accor` / `Encore unlock` | `Drop day stream` / `Listening session` then `Exclusive merch drop` / `Hidden track` |
| After 1 | `Backstage pass` / `Goat limited` | `Behind the boards` / `Loop drops` |
| After 2 | `Stream club` | `Magic Quest` premium |

Concert flavour for Gims is essentially a Toto rewrite (different artist signatures: `Sapés crew`, `Sunglasses hunt`, `Bella tempo`, `Ceinture noire drop`). This confirms [crm_artist_dna]: identify pulse FIRST, then translate per the table; concert sub-variations are just artist-DNA flavouring of the same skeleton.

### 4.4 Revenue calculator defaults (s10)

| | reach | fans | conversion % | gross | commission | net |
|---|---|---|---|---|---|---|
| Concert (T, G) | 4M | 600K | 15% | €491,000 | −€122,750 | €368,250 |
| Album (W) | 1M | 100K | 10% | €81,833 | −€20,458 | €61,375 |

JS literal `reach * 0.15` (concert) vs `reach * 0.10` (album) at L3147 must branch on `pulse_type`.

---

## 5. i18n surface

- Every visible string is wrapped either as `data-en="…" data-fr="…"` (plain text) or `data-i18n="html" data-en-html="…" data-fr-html="…"` (HTML with inline `<span>` formatting).
- Product names (`Magic`, `Magic Quest`, `Magic Lens`, `Magic Pulse`, `Magic Pass`, `Magic Unlimited`, `Fanverse`) intentionally use `data-en="Magic Quest" data-fr="Magic Quest"` — same string both languages — per [product_names].
- SVG `<text>` labels need `<tspan data-en="…" data-fr="…">…</tspan>` wrapping or they're invisible to the i18n switcher (per [product_names] feedback). **Gap found**: in Toto and Gims, the 4 product `<text>` labels on s-momentum (T:L1743/1745/1750/1754: `Magic Quest`, `Magic Lens`, `Mystery Box`, `Magic Unlimited`) are bare text. In Twinsmatic, they are correctly wrapped in `<tspan data-en/data-fr>`. **Canonical = Twins's wrapping**; promote into template so the issue can't recur.
- s-momentum phase-ribbon `<text>` tspans are correctly wrapped in all 3 decks.

---

## 6. Asset references

### Toto (`Assets/...`)
- `Assets/76e84c62-elgrandetoto2-1010x1263.jpg` — s1 hero
- `Assets/2a6d5dfcf5624daba1a7bb0b6f468cddf2f10b1a.jpeg` — s-superfans hero
- `Assets/Frames/Fanverse.png`, `Gamification.png`, `Fan Chat.png`, `Shop.png` — s5 grid
- `Assets/Frames/Magic Pulse.png` — s8 phone mock

### Gims
- `Assets/welcome-gims.jpeg` — s1 hero (note: mirrored via `scaleX(-1)` + `to left` mask)
- `Assets/MMCJUWLHLRCNXL4UAFHPH36IM4.jpg` — s-superfans hero
- `Assets/Frames/Deck Edits/Fanverse.png`, `Gamification.png`, `Fan Chat.png`, `Shop.png` — s5 grid (note `Deck Edits/` subfolder)
- `Assets/Frames/Deck Edits/Magic Pulse.png` — s8 phone mock

### Twinsmatic
- `Assets/Deck Edits/Group 1171275387.png` — s1 hero
- `Assets/Deck Edits/Twinsmatic 1st photo.png` — s-superfans hero
- `Assets/Frames/Deck Edits/Fanverse.png` etc. — s5 grid (same `Deck Edits/` path as Gims)
- `Assets/Frames/Deck Edits/Magic Pulse.png` — s8 phone mock

No external image URLs — everything is local `Assets/…`.

---

## 7. DRIFT findings — call-outs for canonicalisation

**DRIFT-1 (high severity):** Toto's slide-number denominators are all wrong. Should be `XX / 12` (12 slide blocks in every deck), but Toto reads `02/10`, `03/10`, `04/14`, `05/10`, `06/10`, `08/10`, `12/13`, `12/16`, `09/10`, `10/10`. Gims and Twins are correctly `XX / 12` throughout. **Template must always emit `/12`** and renumerate from `01/12` (cover) through `12/12` (s13).

**DRIFT-2:** Toto's phase-ribbon `<text>` x-coords (s-momentum L1787/1791/1795) are `369 / 875 / 1178` — Gims and Twins use the canonical `367 / 872 / 1176` per [svg_arrow_text_centering]. Template must emit `367 / 872 / 1176`.

**DRIFT-3:** Toto and Gims leave s-momentum product-name `<text>` labels (`Magic Quest`, `Magic Lens`, `Mystery Box`, `Magic Unlimited` at T:L1743/1745/1750/1754) un-wrapped. Twins wraps them in `<tspan data-en/data-fr>`. Template must wrap (per [product_names]).

**DRIFT-4:** Gims s5 + s8 use `Assets/Frames/Deck Edits/{Fanverse|Gamification|Fan Chat|Shop|Magic Pulse}.png`, while Toto uses `Assets/Frames/{same}.png`. Twins uses Gims's path. Likely an unintended path drift in Gims's commit (or canonical edits live in `Deck Edits/`). **Pick one — recommend `Assets/Frames/Deck Edits/...` since 2 of 3 decks use it and the folder name implies it's the canonical edited set.**

**DRIFT-5 (cosmetic):** Toto s-superfans has both `<div class="gl gl-tl"></div><div class="gl gl-br"></div>`; Gims drops the `gl-br`. Twins keeps both. Pick one — recommend keeping both (more glow corners).

**DRIFT-6:** Toto's s1 hero `<!--` comment reads `Hero media — full bleed right, fade only on left` (no trailing period); Twins's version has `…on left.` (trailing period). Comment-only, harmless, but for byte-stable template output normalise.

**DRIFT-7:** Twins-only `?scroll=` URL-param branch at L2600-2602 (adds `scroll-mode` class to html+body). Not present in Toto/Gims. **Recommend keeping in the canonical template** — strictly additive and a useful feature for the scroll-export workflow.
