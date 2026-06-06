#!/usr/bin/env python3
"""
lint.py — check a Magic deck HTML file against the memory rules.

Usage:
    python3 lint.py path/to/index.html [more.html ...]
    python3 lint.py --all      # lint all 3 reference decks

Exit code: 0 if clean, 1 if any errors. Warnings don't fail.

Each check maps to a memory rule. Output format:
    [ERROR] file.html:123 — rule-name: short message
    [WARN]  file.html:456 — rule-name: short message
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parent.parent  # ../../ from magic-deck-tool/

def discover_decks() -> list[Path]:
    """Find all deck index.html files under any magic-*-deck/ folder, including
    nested sub-decks (e.g. magic-artist-deck/celine-dion/index.html).

    Excludes test renders and template files.
    """
    found = []
    for deck_dir in sorted(PROJECT_ROOT.glob("magic-*-deck")):
        for path in deck_dir.rglob("index.html"):
            # Skip generated test renders + template
            if path.name == "index.test.html":
                continue
            if "magic-deck-tool" in str(path):
                continue
            found.append(path)
    return found

# Product names that must NOT be translated (data-en == data-fr).
PRODUCT_NAMES = {
    "Magic", "Magic Quest", "Magic Lens", "Magic Pulse",
    "Magic Pass", "Magic Unlimited", "Magic Pulse", "Fanverse",
}

# Canonical SVG arrow text coords (per [[svg-arrow-text-centering]] after 2026-06-06 update).
CANONICAL_ARROW_COORDS = {(369, 300), (875, 300), (1178, 300)}

# Slide-number pattern: every `s-num` div must read NN / 12. NN is the slide index.
SNUM_RE = re.compile(r'<div class="s-num">\s*(\d{1,2})\s*/\s*(\d{1,2})\s*</div>')

# data-en="..." data-fr="..." pair extractor (handles either quote style).
DATA_EN_FR_RE = re.compile(
    r'data-en=(["\'])(?P<en>(?:(?!\1).)*)\1\s+data-fr=(["\'])(?P<fr>(?:(?!\3).)*)\3'
)

# Pseudo-CSS class detector for purple pill.
TAG_PU_RE = re.compile(r'class="[^"]*\btag-pu\b[^"]*"')

# SVG <text> with explicit x/y inside the phase-band group.
SVG_TEXT_COORDS_RE = re.compile(r'<text\s+x="(?P<x>\d+)"\s+y="(?P<y>\d+)"')

# s-momentum product <text> labels (we expect them wrapped in <tspan data-en/data-fr>).
# A bare label is `<text ...>Magic Quest</text>`; wrapped is `<text ...><tspan ...>Magic Quest</tspan></text>`.
PRODUCT_TEXT_RE = re.compile(
    r'<text\b[^>]*>(?P<inner>(?:[^<]|<(?!/text>))*?)</text>'
)


@dataclass
class Finding:
    severity: str  # "ERROR" or "WARN"
    file: Path
    line: int
    rule: str
    message: str

    def format(self) -> str:
        rel = self.file
        return f"[{self.severity:<5}] {rel}:{self.line} — {self.rule}: {self.message}"


def _line_of(content: str, idx: int) -> int:
    return content.count("\n", 0, idx) + 1


# ────────────────────────────────────────────────────────────────────────────
# Checks
# ────────────────────────────────────────────────────────────────────────────

def check_slide_numbers(path: Path, content: str) -> list[Finding]:
    """Every <div class="s-num"> must read XX / N where N = actual slide count.

    Auto-detects N by counting <div class="slide"> blocks in the file, so this
    works for artist decks (12), festival (13), merch (7), SNA/GZ (6), etc.
    """
    out = []
    # Match `<div class="slide ...">` allowing additional classes (e.g. "slide active" on cover).
    slide_count = len(re.findall(r'<div\s+class="(?:[^"]*\s)?slide(?:\s[^"]*)?"', content))
    if slide_count == 0:
        # Fall back to the largest denominator seen — only useful for unusual decks.
        denoms = [int(m.group(2)) for m in SNUM_RE.finditer(content)]
        if not denoms:
            return out
        slide_count = max(denoms)
    for m in SNUM_RE.finditer(content):
        num, denom = int(m.group(1)), int(m.group(2))
        line = _line_of(content, m.start())
        if denom != slide_count:
            out.append(Finding("ERROR", path, line, "slide-numbers",
                f"denominator is /{denom}, deck has {slide_count} slides — must be /{slide_count}"))
        if not (1 <= num <= slide_count):
            out.append(Finding("ERROR", path, line, "slide-numbers",
                f"numerator {num} out of range 1..{slide_count}"))
    return out


def check_no_bercy(path: Path, content: str) -> list[Finding]:
    """Word 'Bercy' must never appear (Magic decks say 'Accor')."""
    out = []
    for m in re.finditer(r"\bBercy\b", content):
        line = _line_of(content, m.start())
        # The CSS class `.bercy` is fine (legacy class name); only flag user-facing text.
        snippet = content[max(0, m.start()-20):m.end()+20]
        if 'class="' in snippet and 'class=".*bercy' not in snippet:
            # Likely inside a class= attribute; check more carefully.
            if re.search(r'class="[^"]*\bbercy\b[^"]*"', snippet):
                continue
        out.append(Finding("ERROR", path, line, "accor-not-bercy",
            "the word 'Bercy' must be replaced with 'Accor'"))
    return out


def check_no_tag_pu(path: Path, content: str) -> list[Finding]:
    """`.tag-pu` purple pill is banned — always use the blue `.tag`."""
    out = []
    for m in TAG_PU_RE.finditer(content):
        line = _line_of(content, m.start())
        out.append(Finding("ERROR", path, line, "pill-color",
            "purple `.tag-pu` is banned; use the blue `.tag` default"))
    return out


def check_viewport_meta(path: Path, content: str) -> list[Finding]:
    """Viewport meta must disable pinch-zoom (mobile crash bug)."""
    out = []
    m = re.search(r'<meta\s+name="viewport"\s+content="([^"]+)"', content)
    if not m:
        out.append(Finding("ERROR", path, 1, "mobile-zoom",
            "<meta name='viewport'> missing"))
        return out
    content_attr = m.group(1)
    line = _line_of(content, m.start())
    if "maximum-scale=1" not in content_attr:
        out.append(Finding("ERROR", path, line, "mobile-zoom",
            "viewport meta missing maximum-scale=1"))
    if "user-scalable=no" not in content_attr:
        out.append(Finding("ERROR", path, line, "mobile-zoom",
            "viewport meta missing user-scalable=no"))
    return out


def check_product_names_no_translate(path: Path, content: str) -> list[Finding]:
    """Product names (Magic, Magic Quest, etc.) must have data-en == data-fr.

    Only flags when one side IS a product name and the other side differs.
    """
    out = []
    for m in DATA_EN_FR_RE.finditer(content):
        en = m.group("en").strip()
        fr = m.group("fr").strip()
        # Strip leading ornaments like ✦ for the comparison.
        en_clean = re.sub(r"^[✦★\s]+", "", en).strip()
        fr_clean = re.sub(r"^[✦★\s]+", "", fr).strip()
        if en_clean in PRODUCT_NAMES and en_clean != fr_clean:
            line = _line_of(content, m.start())
            out.append(Finding("ERROR", path, line, "product-names",
                f"'{en_clean}' must not translate; data-fr='{fr_clean}'"))
        elif fr_clean in PRODUCT_NAMES and en_clean != fr_clean:
            line = _line_of(content, m.start())
            out.append(Finding("ERROR", path, line, "product-names",
                f"'{fr_clean}' is a product name; data-en='{en_clean}' differs"))
    return out


def check_svg_product_labels_wrapped(path: Path, content: str) -> list[Finding]:
    """s-momentum product <text> labels must be wrapped in <tspan data-en/data-fr>
    so the i18n switcher renders them.
    """
    out = []
    for m in PRODUCT_TEXT_RE.finditer(content):
        inner = m.group("inner").strip()
        # If the inner text is a plain product name (no tspan), flag it.
        if inner in PRODUCT_NAMES:
            line = _line_of(content, m.start())
            out.append(Finding("ERROR", path, line, "product-names",
                f"SVG <text> label '{inner}' is bare; wrap in "
                f"<tspan data-en=\"{inner}\" data-fr=\"{inner}\">"))
    return out


def check_arrow_text_coords(path: Path, content: str) -> list[Finding]:
    """Phase-ribbon SVG arrow text must use canonical centroid coords.

    Only checks text elements at y≈300 (the phase ribbon row). Other SVG <text>
    on the momentum chart (axis labels at y=268, legend at y=347/362) are out
    of scope and use their own positioning.
    """
    out = []
    tolerance_groups = [(361, 380, 369), (866, 880, 875), (1170, 1185, 1178)]
    for m in SVG_TEXT_COORDS_RE.finditer(content):
        x, y = int(m.group("x")), int(m.group("y"))
        if abs(y - 300) > 5:
            continue  # not a phase-ribbon text
        line = _line_of(content, m.start())
        for lo, hi, want in tolerance_groups:
            if lo <= x <= hi:
                if x != want:
                    out.append(Finding("ERROR", path, line, "svg-arrow-centering",
                        f"phase ribbon text x={x}, should be {want}"))
                if y != 300:
                    out.append(Finding("ERROR", path, line, "svg-arrow-centering",
                        f"phase ribbon text y={y}, should be 300"))
                break
    return out


def check_fr_br_overflow(path: Path, content: str) -> list[Finding]:
    """Warn on `<br>` inside data-fr= strings — FR runs ~25% longer than EN
    and a hard break tuned for EN often overflows in FR.
    """
    out = []
    for m in DATA_EN_FR_RE.finditer(content):
        fr = m.group("fr")
        if "<br>" in fr.lower():
            line = _line_of(content, m.start())
            out.append(Finding("WARN", path, line, "fr-overflow",
                "hardcoded <br> in data-fr — verify FR render doesn't overflow"))
    return out


def check_body_font_size(path: Path, content: str) -> list[Finding]:
    """Body paragraphs use 20px / 1.65 / weight 300. Punchlines are 22px / weight 700.
    CTA sub-lines are 18px / weight 700. Anything ELSE in the 16-28px range with
    weight 300 (body weight) is suspicious.
    """
    out = []
    for m in re.finditer(r'<p\s+[^>]*style="([^"]+)"', content):
        style = m.group(1)
        fsmatch = re.search(r"font-size:\s*(\d+)px", style)
        if not fsmatch:
            continue
        size = int(fsmatch.group(1))
        if not (16 <= size <= 28):
            continue
        weight_match = re.search(r"font-weight:\s*(\d+)", style)
        weight = int(weight_match.group(1)) if weight_match else None
        # 22px @ weight 700 = punchline (canonical). 18px @ weight 700 = CTA sub. OK.
        if size == 22 and weight == 700:
            continue
        if size == 18 and weight == 700:
            continue
        # Otherwise body should be 20px.
        if size != 20:
            line = _line_of(content, m.start())
            out.append(Finding("WARN", path, line, "body-typography",
                f"<p> font-size={size}px weight={weight}; canonical body=20/300, "
                f"punchline=22/700, CTA sub=18/700"))
    return out


def check_required_chrome(path: Path, content: str) -> list[Finding]:
    """Sanity: things that should always be present in a deck."""
    out = []
    if "scroll-mode" not in content:
        out.append(Finding("ERROR", path, 1, "scroll-mode",
            "missing ?scroll= URL-param branch (scroll-mode class)"))
    if "?presentation" not in content and "presentation" not in content:
        out.append(Finding("WARN", path, 1, "presentation-mode",
            "no obvious presentation-mode handler — verify all 3 URL forms work"))
    return out


def check_crm_phase_alignment(path: Path, content: str) -> list[Finding]:
    """Phase-specific CRM mechanics must appear only in their valid phase.

    Some product features on the momentum graph are ALWAYS-ON across the
    journey (Magic Quest = XP ladder fans climb anytime; Magic Lens =
    scavenger-hunt mechanic; Invite Friends = referral; Music = catalogue).
    Those are NOT checked — they can appear in any phase legitimately.

    But some features are tied to a specific moment in the journey and don't
    make sense outside their phase:
      Mystery Box       → Peak only (surprise drops AT the moment)
      Fan Meet          → Peak only (in-venue meetups)
      Fan Faves         → Build-up only (anticipation polling)
      Talent Faves      → Build-up only (artist's pre-event picks)
      Magic Unlimited   → After only (premium subscription tier launches late)

    We only check EXPLICIT mentions of these phase-specific feature names.
    Cards using mechanics implicitly (e.g. 'Pookie hunt' implies Magic Lens)
    are not checked, only explicit name mentions.
    """
    # Phase-specific features only → phase color classes where they belong
    FEATURE_PHASE = {
        "Mystery Box": {"purp"},        # Peak only — surprise drops AT the moment
        "Fan Meet": {"purp"},           # Peak only — in-venue meetups
        "Fan Faves": {"cyan"},          # Build-up only — anticipation polling
        "Talent Faves": {"cyan"},       # Build-up only — artist's pre-event picks
        "Magic Unlimited": {"teal"},    # After only — premium subscription
    }
    PHASE_LABEL = {"cyan": "Build-up", "purp": "★ Peak", "teal": "After"}

    out = []
    # Match each j-card with its color class and inner nm + hk text
    card_re = re.compile(
        r'<div class="j-card (?P<color>cyan|purp|teal)"[^>]*>'
        r'(?P<inner>.*?)</div>\s*(?=<div class="j-card|</div>)',
        re.DOTALL
    )
    for m in card_re.finditer(content):
        color = m.group("color")
        inner = m.group("inner")
        line = _line_of(content, m.start())
        # Extract nm and hk visible text
        nm_match = re.search(r'<div class="nm"[^>]*>([^<]*)</div>', inner)
        hk_match = re.search(r'<div class="hk"[^>]*>([^<]*)</div>', inner)
        card_text = ((nm_match.group(1) if nm_match else "") + " " +
                     (hk_match.group(1) if hk_match else ""))
        # Check each distinctive feature name
        for feature, allowed_colors in FEATURE_PHASE.items():
            if feature in card_text and color not in allowed_colors:
                allowed_phase = ", ".join(PHASE_LABEL[c] for c in allowed_colors)
                actual_phase = PHASE_LABEL[color]
                out.append(Finding("ERROR", path, line, "crm-phase-alignment",
                    f"card mentions '{feature}' but is in {actual_phase} phase "
                    f"(color={color}); '{feature}' is only available in {allowed_phase} "
                    f"per the momentum graph"))
    return out


def check_mobile_scroll(path: Path, content: str) -> list[Finding]:
    """Mobile @media must override BOTH html and body for overflow-y.

    Bug found 2026-06-06: base rule sets `html, body { overflow:hidden }`. If
    the mobile @media only overrides body, html stays locked and touch scroll
    is dead on phones. Look for `body { overflow-y:auto` without the matching
    `html, body { overflow-y:auto` inside a max-width:768px media query.
    """
    out = []
    # Find the mobile @media block
    m = re.search(r"@media\s+screen\s+and\s+\(max-width:\s*768px\)\s*\{(?P<body>.*?)^\}",
                  content, re.DOTALL | re.MULTILINE)
    if not m:
        return out  # no mobile block at all — separate concern, not this check
    block = m.group("body")
    block_line = _line_of(content, m.start())
    # Look for a selector with body but not html that sets overflow-y:auto
    bad = re.search(r"^\s*body\s*\{\s*overflow-y\s*:\s*auto", block, re.MULTILINE)
    good = re.search(r"^\s*html\s*,\s*body\s*\{\s*overflow-y\s*:\s*auto", block, re.MULTILINE)
    if bad and not good:
        out.append(Finding("ERROR", path, block_line, "mobile-scroll",
            "mobile @media only overrides `body` for overflow-y; must be `html, body` "
            "(otherwise html stays overflow:hidden and touch scroll is dead on phones)"))
    return out


CHECKS: list[Callable[[Path, str], list[Finding]]] = [
    check_slide_numbers,
    check_no_bercy,
    check_no_tag_pu,
    check_viewport_meta,
    check_product_names_no_translate,
    check_svg_product_labels_wrapped,
    check_arrow_text_coords,
    check_fr_br_overflow,
    check_body_font_size,
    check_required_chrome,
    check_mobile_scroll,
    check_crm_phase_alignment,
]


# ────────────────────────────────────────────────────────────────────────────
# Runner
# ────────────────────────────────────────────────────────────────────────────

def lint_file(path: Path) -> list[Finding]:
    content = path.read_text(encoding="utf-8")
    findings = []
    for check in CHECKS:
        findings.extend(check(path, content))
    return findings


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("decks", nargs="*", type=Path,
                   help="HTML files to lint")
    p.add_argument("--all", action="store_true",
                   help="lint the 3 reference decks")
    args = p.parse_args()

    targets = list(args.decks)
    if args.all:
        targets.extend(discover_decks())
    if not targets:
        p.error("specify at least one HTML file or --all")

    errors = warns = 0
    for path in targets:
        if not path.exists():
            print(f"[lint] SKIP: {path} not found", file=sys.stderr)
            continue
        findings = lint_file(path)
        if not findings:
            print(f"[lint] {path}: clean ✓")
            continue
        print(f"[lint] {path}: {len(findings)} finding(s)")
        for f in findings:
            print(f"  {f.format()}")
            if f.severity == "ERROR":
                errors += 1
            else:
                warns += 1

    print()
    print(f"[lint] summary: {errors} error(s), {warns} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
