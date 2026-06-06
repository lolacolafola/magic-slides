# Conditionals — pulse-type branching plan

The three reference decks share **identical DOM structure** across all 12 slides. Pulse-type ("concert" vs "album") differences manifest as:

1. **String swaps** inside `data-en` / `data-fr` / `data-en-html` / `data-fr-html` attributes (handled by per-deck config, no template branching needed).
2. **A handful of numeric defaults** in s10 (revenue calculator).
3. **Tiny attribute toggles** (lowercase pill, mirrored hero image).

The good news: there is **no slide that exists in one pulse but not the other**, no `<div>` swap, no template-block conditional. Every branch is either a value override or a single attribute toggle. This makes Phase 1 dramatically simpler — `pulse_type` is mostly a default-picker, not a structural switch.

---

## Branch points by slide

### s0 — Cover

```jinja
<p ... data-en="{{ cover_trigger_en }}" data-fr="{{ cover_trigger_fr }}">
  {{ cover_trigger_en }}
</p>
```

No structural branch. The `cover_trigger_*` strings carry the pulse flavour. `generate.py` may auto-suggest defaults based on `pulse_type`:

```python
if pulse_type == "concert":
    default_cover_trigger_en = f"Built for {tour_name} · {venue} · {date}"
else:  # album
    default_cover_trigger_en = f"Built for the next album · Out {release_month}"
```

### s1 — Welcome

Two micro-branches:

**a) Lowercase artist pill** (twinsmatic case):
```jinja
<span class="tag"{% if artist_name_pill_lowercase_flag %} style="text-transform:none;"{% endif %}
      data-en="✦ {{ artist_name_pill }}" data-fr="✦ {{ artist_name_pill }}">✦ {{ artist_name_pill }}</span>
```

**b) Mirrored hero image** (Gims case):
```jinja
<img id="s1-hero-img"
     src="{{ s1_hero_img_src }}"
     alt="{{ s1_hero_img_alt }}"
     style="width:100%;height:100%;object-fit:cover;
            object-position:{{ s1_hero_object_position | default('center 30%') }};
            {% if s1_hero_mirrored %}transform:scaleX(-1);{% endif %}
            -webkit-mask-image:linear-gradient(to {{ 'left' if s1_hero_mirrored else 'right' }},transparent 0%,rgba(0,0,0,0.2) 15%,rgba(0,0,0,0.6) 30%,rgba(0,0,0,0.9) 45%,black 60%,black 100%);
            mask-image:linear-gradient(to {{ 'left' if s1_hero_mirrored else 'right' }},transparent 0%,rgba(0,0,0,0.2) 15%,rgba(0,0,0,0.6) 30%,rgba(0,0,0,0.9) 45%,black 60%,black 100%);">
```

(Per [hero_blur_rule]: the sibling navy gradient overlay div stays as `linear-gradient(to right, ...)` regardless of mirror state — don't flip it.)

### s2 — The Problem

**No branch.** Fully canonical.

### s-momentum — Phase chart

No DOM branch. Strings only:
- `{{ phase_build_label_* }}`, `{{ phase_peak_label_* }}`, `{{ phase_after_label_* }}` — pulse-type-aware defaults:

```python
PHASE_LABELS = {
    "concert_single": {  # Toto-style, one night
        "build": ("Build-up · Sep - Feb", "Mise en route · sep - fév"),
        "peak":  ("Concert · Mar", "Le concert · mars"),
        "after": ("After the show · Apr - onwards", "Après le concert · avril - et après"),
    },
    "concert_multi": {   # Gims-style, multi-night → plural
        "build": ("Build-up · Jun - Nov", "Mise en route · juin - nov"),
        "peak":  ("Concerts · Dec", "Les concerts · déc"),
        "after": ("After the shows · Jan - onwards", "Après les concerts · janvier - et après"),
    },
    "album": {
        "build": ("Recruit & warm up · Jun - Sep", "Recrutement & mise en route · juin - sep"),
        "peak":  ("Album drop · Oct", "Sortie de l'album · oct"),
        "after": ("Beyond the drop · Nov - onwards", "Au-delà de la sortie · nov - et après"),
    },
}
```

The SVG `<text>` coordinates are canonical (`367 / 872 / 1176`) — never branched.

### s4 — Fanverse solar system

No structural branch. Sun centre text varies via `{{ s4_centre_line1 }}` / `{{ s4_centre_line2 }}` (line 2 may be empty for short artist names; Gims uses 15px and omits line 2 — toggle via `{{ s4_centre_line1_size }}`).

Planet labels are **canonical** (Magic Quest / Magic Lens / Mystery Box / Magic Unlimited) per [fanverse_locked] — template hardcodes them inside `<tspan data-en/data-fr>` wrappers (per [product_names] — even though they don't translate, the wrapping is required for the i18n switcher to render them).

### s5 — Always on grid

No branch. Body copy and image paths swap via placeholders.

### s-applied — CRM plan — THE MAIN BRANCH

This is where structured per-deck config (a YAML list) matters. The template loops:

```jinja
<div class="pseg c" data-en="{{ phase_build_label_en }}" data-fr="{{ phase_build_label_fr }}">{{ phase_build_label_en }}</div>
<div class="pseg p" data-en="{{ phase_peak_label_en }}" data-fr="{{ phase_peak_label_fr }}">{{ phase_peak_label_en }}</div>
<div class="pseg t" data-en="{{ phase_after_label_en }}" data-fr="{{ phase_after_label_fr }}">{{ phase_after_label_en }}</div>

{% for month in crm_months %}
  <div class="mcol">
    <div class="mlabel{% if month.is_peak %} bercy{% endif %}">{% if month.is_peak %}&#9733; {% endif %}{{ month.label }}</div>
    {% for card in month.cards %}
      <div class="j-card {{ card.color }}">
        <div class="nm" data-en="{{ card.nm_en }}" data-fr="{{ card.nm_fr }}">{{ card.nm_en }}</div>
        <div class="hk" data-en="{{ card.hk_en }}" data-fr="{{ card.hk_fr }}">{{ card.hk_en }}</div>
        {% if card.rwd %}<div class="rwd">{{ icon_svg("coin") }}<span class="xp">XP</span></div>{% endif %}
        <div class="cds">
          {% for icon in card.icons %}{{ icon_svg(icon) }}{% endfor %}
        </div>
      </div>
    {% endfor %}
  </div>
{% endfor %}
```

Default `crm_months` come from per-pulse seed YAML (see `examples/concert.yaml` and `examples/album.yaml`); per-artist YAML overrides individual card `nm`/`hk` strings via [crm_artist_dna] translation table.

**Color rule** (observed in all 3 decks):
- Build-up cards → `cyan`
- Peak (★) cards → `purp`
- After cards → `teal`

The template can default each card's `color` from its month's phase position.

### s8 — Magic Pulse

No branch. `frames_path_prefix` placeholder handles the path drift.

### s11 — Increase every revenue stream

No branch. Fully canonical.

### s10 — Get paid (revenue calculator)

The biggest **value** branch. DOM is identical, but ~13 default values plus 1 JS literal change:

```jinja
<input id="sim-reach" type="text" value="{{ sim_default_reach }}" ... />
...
<div ...>{{ sim_conversion_pct_label }}</div>
...
<div id="sim-fans" ...>{{ sim_default_fans }}</div>
...
<span ... id="sim-bar-fan">{{ sim_tier_fan_count }}</span>
<div id="sim-amt-fan" ...>{{ sim_tier_fan_amt }}</div>
... (same pattern for merch, iap, prem)
<div id="sim-gross">{{ sim_gross }}</div>
<div id="sim-commission">{{ sim_commission }}</div>
<div id="sim-net">{{ sim_net }}</div>
```

And in the JS block at L3147:
```jinja
var fans = reach * {{ sim_conversion_rate }};
```

Pulse-type defaults:
```python
SIM_DEFAULTS = {
    "concert": {
        "reach": "4M",         "fans": "600K",
        "rate": 0.15,          "pct_label": "15% TO MAGIC",
        "tier_fan": ("600K · €0.10/activation", "€60k"),
        "tier_merch": ("200K · €5/item · 20% boost on volumes", "€230k"),
        "tier_iap": ("200K · €10/IAP", "€36k"),
        "tier_prem": ("20K · €1.15/user", "€165k"),
        "gross": "€491,000", "commission": "−€122,750", "net": "€368,250",
    },
    "album": {
        "reach": "1M",         "fans": "100K",
        "rate": 0.10,          "pct_label": "10% TO MAGIC",
        "tier_fan": ("100K · €0.10/activation", "€10k"),
        "tier_merch": ("33K · €5/item · 20% boost on volumes", "€38k"),
        "tier_iap": ("33K · €10/IAP", "€6k"),
        "tier_prem": ("3K · €1.15/user", "€28k"),
        "gross": "€81,833", "commission": "−€20,458", "net": "€61,375",
    },
}
```

(Phase 2 idea: compute these from reach + rate rather than hard-code. Phase 1: literal defaults are fine.)

### s-superfans

No DOM branch. Image src varies via `{{ s_superfans_hero_img_src }}`. (DRIFT-5 notwithstanding — pick `gl-tl + gl-br` canonical.)

### s13 — Recap

The first bullet (capacity / permanent-space) is the **only** outro string with pulse-dependent shape — for concert it counts venue seats × dates; for album it pivots to permanence. Two clean templates handle both:

```jinja
{# Bullet 1 — capacity / place #}
<div ... data-i18n="html"
     data-en-html="<span style='font-weight:700;'>A place for every fan</span><span style='font-weight:300;color:rgba(255,255,255,0.55);'>: {{ s13_capacity_bullet_en_html }}</span>"
     data-fr-html="<span style='font-weight:700;'>Une place pour chaque fan</span><span style='font-weight:300;color:rgba(255,255,255,0.55);'> : {{ s13_capacity_bullet_fr_html }}</span>">
  ...
</div>
```

The `{{ s13_capacity_bullet_*_html }}` placeholder is filled per-deck (see [artist_adaptation_scope]).

The second bullet ("Every moment shared") has a structural variant — concert version ends `…alongside {artist}, ticket or not.` while album version ends `…alongside {artist}.` (no "ticket or not"). Cleanest is to make the whole second-bullet payload its own placeholder pair (`{{ s13_moment_bullet_*_html }}`) and let per-deck config write it out fully.

### Nav / footer / mobile leaderboard / JS storage

All swap-driven by `{{ artist_name_display }}` and `{{ deck_slug }}`. No branch.

### Twinsmatic-only `?scroll=` URL branch (W:L2600-2602)

Promote to canonical template (additive, harmless on other decks):
```js
} else if (urlParams.has('scroll')) {
  document.documentElement.classList.add('scroll-mode');
  document.body.classList.add('scroll-mode');
}
```

---

## Summary: the conditional matrix

| Branch | Type | Slides affected | Template construct |
|---|---|---|---|
| Lowercase artist pill | bool attr toggle | s1 | inline `{% if %}` |
| Mirrored hero | bool style toggle | s1 | inline `{% if %}` × 3 (transform + 2 mask gradients) |
| Phase ribbon labels | string defaults | s-momentum, s-applied | per-pulse default dict, override in deck YAML |
| CRM cards | structured loop | s-applied | `{% for %}` over `crm_months` list |
| Calculator defaults | string + decimal defaults | s10 | per-pulse default dict, override in deck YAML |
| Capacity bullet HTML | html string override | s13 | per-deck YAML, no branch in template |

**Total DOM `{% if %}` branches needed in the template: 4 small inline toggles. Everything else is variable substitution or list iteration.**
