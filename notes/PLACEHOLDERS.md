# Placeholders — magic-deck-tool template

Flat, deduplicated list of every `{{placeholder}}` the template engine will need to fill, grouped by surface. EN/FR column indicates whether the placeholder has a paired `_fr` variant (most copy does; identity slugs don't).

Conventions:
- `string` = plain text
- `html` = HTML fragment (allowed inline `<span>`, `<br>`)
- `url` / `path` = asset reference
- `enum` = fixed set of allowed values
- `int` / `decimal` = number

---

## A. Artist identity (cross-slide)

| Placeholder | Type | EN+FR? | Used on | Example values |
|---|---|---|---|---|
| `{{deck_slug}}` | string | no | JS storage keys (`magic-{slug}-deck-{edits,layout,images}-v1`), download filenames, internal paths | `toto` / `gims` / `twinsmatic` |
| `{{artist_name_display}}` | string | no (same both langs) | `<title>`, s0 cover headline (`Magic for {name}`), s13 second bullet, nav footer, mobile leaderboard, PDF filename (`Magic - {name}.pdf`) | `ElGrandeToto` / `GIMS` / `twinsmatic` (lowercase preserved for twins) |
| `{{artist_name_pill}}` | string | no | s1 eyebrow `✦ {name}` | `ElGrandeToto` / `GIMS` / `twinsmatic` (usually same as display) |
| `{{artist_name_pill_lowercase_flag}}` | bool | no | controls `style="text-transform:none;"` on s1 pill so a lowercase brand (twinsmatic) doesn't get upcased by CSS | `true` / `false` |
| `{{s4_centre_line1}}` | string | no | s4 sun centre, line 1 (size-weight 700) — short tag | `ELGRANDE` / `GIMS` / `twins` |
| `{{s4_centre_line2}}` | string \| empty | no | s4 sun centre, line 2 (size-weight 400) — subtitle/suffix; can be empty for single-word artists | `TOTO` / `` / `matic` |
| `{{s4_centre_line1_size}}` | int (px) | no | Override the 11px default when the brand is short (Gims single line uses 15px) | `11` (default) / `15` (Gims) |

## B. Cover / trigger anchor (s0 + s1)

| Placeholder | Type | EN+FR? | Used on | Example values |
|---|---|---|---|---|
| `{{deck_title}}` | string | no | `<title>` tag at HTML head | `Magic — ElGrandeToto` |
| `{{cover_trigger_en}}` | string | EN | s0 uppercase eyebrow under cover headline | `Built for Salgoat world tour · Accor Arena · 27 March 2027` / `Built for the next album · Out October` |
| `{{cover_trigger_fr}}` | string | FR | s0 same line, FR | `Pensé pour le Salgoat world tour · Accor Arena · 27 mars 2027` |
| `{{s1_trigger_en}}` | string | EN | s1 third paragraph (the trigger line that names the anchor moment) | `Accor on 27 March is the trigger…` / `The album is the trigger…` |
| `{{s1_trigger_fr}}` | string | FR | s1 third paragraph, FR | `Accor le 27 mars, c'est le déclencheur…` |

## C. Hero imagery (s1 + s-superfans)

| Placeholder | Type | EN+FR? | Used on | Example values |
|---|---|---|---|---|
| `{{s1_hero_img_src}}` | path | no | s1 right-side hero `<img src="...">` | `Assets/76e84c62-elgrandetoto2-1010x1263.jpg` / `Assets/welcome-gims.jpeg` / `Assets/Deck Edits/Group 1171275387.png` |
| `{{s1_hero_img_alt}}` | string | no | s1 `alt=""` (use display name) | `ElGrandeToto` / `GIMS` / `twinsmatic` |
| `{{s1_hero_object_position}}` | string | no | `object-position` value | `center 30%` (default) / `40% 30%` |
| `{{s1_hero_mirrored}}` | bool | no | When true, add `transform:scaleX(-1)` to img and flip mask gradient direction to `to left` (per [hero_blur_rule]) | `false` (T, W) / `true` (G) |
| `{{s_superfans_hero_img_src}}` | path | no | s-superfans right-side image | `Assets/2a6d5dfcf5624daba1a7bb0b6f468cddf2f10b1a.jpeg` / `Assets/MMCJUWLHLRCNXL4UAFHPH36IM4.jpg` / `Assets/Deck Edits/Twinsmatic 1st photo.png` |
| `{{s_superfans_hero_object_position}}` | string | no | `object-position` for s-superfans img | `center 30%` (default) / `40% 30%` (Toto) |
| `{{frames_path_prefix}}` | path | no | Path prefix for the 4 s5 grid frames + s8 Magic Pulse frame — `Assets/Frames/` (Toto) or `Assets/Frames/Deck Edits/` (Gims, Twins) | `Assets/Frames/Deck Edits/` (recommended canonical) |

## D. Momentum slide (s-momentum)

| Placeholder | Type | EN+FR? | Used on | Example values |
|---|---|---|---|---|
| `{{momentum_sub_en}}` | string | EN | s-momentum sub paragraph below headline | `Magic turns Accor and everything around it into fan experiences…` |
| `{{momentum_sub_fr}}` | string | FR | same, FR | `Magic transforme Accor et tout ce qui l'entoure…` |
| `{{phase_build_label_en}}` | string | EN | s-momentum SVG ribbon segment 1 + s-applied `.pseg c` (same label must appear in both places) | `Build-up · Sep - Feb` / `Recruit & warm up · Jun - Sep` |
| `{{phase_build_label_fr}}` | string | FR | same, FR | `Mise en route · sep - fév` / `Recrutement & mise en route · juin - sep` |
| `{{phase_peak_label_en}}` | string | EN | ribbon segment 2 + `.pseg p` | `Concert · Mar` / `Concerts · Dec` / `Album drop · Oct` |
| `{{phase_peak_label_fr}}` | string | FR | same | `Le concert · mars` / `Sortie de l'album · oct` |
| `{{phase_after_label_en}}` | string | EN | ribbon segment 3 + `.pseg t` | `After the show · Apr - onwards` / `Beyond the drop · Nov - onwards` |
| `{{phase_after_label_fr}}` | string | FR | same | `Après le concert · avril - et après` |

## E. CRM plan (s-applied)

| Placeholder | Type | EN+FR? | Used on | Example values |
|---|---|---|---|---|
| `{{crm_headline_en_html}}` | html | EN | s-applied `<div class="h">` headline | `The road to <span class='gt'>Accor and beyond.</span>` / `The build-up to <span class='gt'>the album, and beyond.</span>` |
| `{{crm_headline_fr_html}}` | html | FR | same, FR | `La route vers <span class='gt'>Accor, et au-delà.</span>` |
| `{{crm_sub_en}}` | string | EN | s-applied `<p class="sub">` | `Here's an example of ElGrandeToto's Fanverse in action…` |
| `{{crm_sub_fr}}` | string | FR | same, FR | `Voici un exemple du Fanverse d'ElGrandeToto en action…` |
| `{{crm_month_1}}` … `{{crm_month_7}}` | string | no | The 7 `.mlabel` columns (months/ranges, all uppercase, e.g. `SEPT`, `OCT/NOV`, `MAR`) | `SEPT`, `OCT/NOV`, `DEC`, `JAN/FEB`, `MAR`, `APR`, `MAY` (T) — but template only renders 7; concert pulse often groups (e.g. `OCT/NOV`) |
| `{{crm_pulse_month_index}}` | int (1-7) | no | Which `mlabel` column gets `class="mlabel bercy"` and the `★` prefix (= the peak/anchor month) | `5` for T (`★ MAR`), `5` for G (`★ DEC`), `5` for W (`★ OCT`) — always 5 in the 3 reference decks |
| `{{crm_card_{m}_{n}_nm_en}}` | string | EN | j-card title (m = month 1-7, n = card 1-2) | `Connect & climb`, `Drop day stream`, `Final countdown`, … |
| `{{crm_card_{m}_{n}_nm_fr}}` | string | FR | same, FR | `Stream du jour J`, … |
| `{{crm_card_{m}_{n}_hk_en}}` | string | EN | j-card hook copy | `Link Spotify, earn coins per stream` |
| `{{crm_card_{m}_{n}_hk_fr}}` | string | FR | same, FR | `Connecte Spotify, gagne des coins par écoute` |
| `{{crm_card_{m}_{n}_color}}` | enum | no | j-card colour class | `cyan` / `purp` / `teal` |
| `{{crm_card_{m}_{n}_icons}}` | enum-set | no | Which `cds` icon SVGs to render (sparkle, ticket, music, bag, video, spotify) | `["sparkle"]`, `["ticket","bag"]`, `["video"]`, `["sparkle","spotify"]`, … |
| `{{crm_card_{m}_{n}_rwd}}` | enum | no | XP/coin reward chip presence | `none` / `coin+sparkle` (default for free actions) |

(Recommend modelling the CRM grid as a structured `crm_cards: [{month, month_label, is_peak, cards: [...]}]` list in YAML rather than 14 flat slots — the template loops over it.)

## F. Revenue calculator (s10)

| Placeholder | Type | EN+FR? | Used on | Example values |
|---|---|---|---|---|
| `{{sim_default_reach}}` | string | no | `#sim-reach` initial `value=""` | `4M` (concert) / `1M` (album) |
| `{{sim_default_fans}}` | string | no | `#sim-fans` initial inner text | `600K` / `100K` |
| `{{sim_conversion_rate}}` | decimal | no | JS `var fans = reach * X;` at L3147 | `0.15` (concert) / `0.10` (album) |
| `{{sim_conversion_pct_label}}` | string | no | Chip between reach and fans (`15% TO MAGIC`) | `15% TO MAGIC` / `10% TO MAGIC` |
| `{{sim_tier_fan_count}}` | string | no | "fan tier" row label (`600K · €0.10/activation`) | `600K · €0.10/activation` / `100K · €0.10/activation` |
| `{{sim_tier_fan_amt}}` | string | no | fan tier amount column | `€60k` / `€10k` |
| `{{sim_tier_merch_count}}` | string | no | merch tier left label | `200K · €5/item · 20% boost on volumes` / `33K · ...` |
| `{{sim_tier_merch_amt}}` | string | no | merch tier amount | `€230k` / `€38k` |
| `{{sim_tier_iap_count}}` | string | no | IAP tier left label | `200K · €10/IAP` / `33K · €10/IAP` |
| `{{sim_tier_iap_amt}}` | string | no | IAP tier amount | `€36k` / `€6k` |
| `{{sim_tier_prem_count}}` | string | no | Premium tier left label | `20K · €1.15/user` / `3K · €1.15/user` |
| `{{sim_tier_prem_amt}}` | string | no | Premium tier amount | `€165k` / `€28k` |
| `{{sim_gross}}` | string | no | gross total | `€491,000` / `€81,833` |
| `{{sim_commission}}` | string | no | commission line | `−€122,750` / `−€20,458` |
| `{{sim_net}}` | string | no | net total | `€368,250` / `€61,375` |

(All revenue tier amounts can in principle be derived from `pulse_type` + `reach`. Recommend computing them in `generate.py` from a single `{{sim_default_reach_numeric}}` + `{{sim_conversion_rate}}` rather than asking deck author to fill 12 fields by hand. Keep slot-level overrides for edge cases.)

## G. Recap / outro (s13)

| Placeholder | Type | EN+FR? | Used on | Example values |
|---|---|---|---|---|
| `{{s13_capacity_bullet_en_html}}` | html | EN | First bullet "A place for every fan" body (after the bold label) | `Accor holds 20,000 on 27 March. Magic opens a space for them…` / `a release reaches a moment, then fades. Magic opens a permanent space…` |
| `{{s13_capacity_bullet_fr_html}}` | html | FR | same, FR | `Accor accueillera 20 000 fans le 27 mars…` |
| `{{s13_moment_artist}}` | string | no | Second bullet `alongside {artist}, ticket or not` (concert) — for album, the whole bullet text changes shape; treat as full sentence override below | `ElGrandeToto` / `GIMS` (concert) / N/A (album) |
| `{{s13_moment_bullet_en_html}}` | html | EN | Optional full override for the second bullet (album pulse drops the "ticket or not" tail) | `from the first teaser to release week and the months after, every fan lives every beat alongside twinsmatic.` |
| `{{s13_moment_bullet_fr_html}}` | html | FR | same, FR | … |

(Third bullet "Every bond owned" is canonical — no placeholders.)

## H. Pulse-type conditional flag

| Placeholder | Type | EN+FR? | Used on | Example values |
|---|---|---|---|---|
| `{{pulse_type}}` | enum | no | Drives `{% if pulse_type == "album" %}` branches throughout the template; defaults for s10 calculator; venue-vs-release phrasing in canned bullets if you prefer to compute them server-side | `concert` / `album` |

---

## Quick dedup summary

Total distinct placeholders: **~58**.

- Identity: 7
- Cover/trigger: 5
- Hero imagery: 7
- Momentum: 8
- CRM (modelled as a loop, see note): 4 scalar + 1 list-of-objects (≈ 28 fields if flattened)
- Revenue: 13
- Outro: 5
- Conditional flag: 1

Modelling the CRM grid + revenue tiers as structured objects (rather than flat placeholders) keeps the deck-config YAML readable. The flat-name list above is the maximalist count.
