#!/usr/bin/env python3
"""
generate.py — render a Magic artist deck from a YAML profile.

Usage:
    python3 generate.py examples/twinsmatic.yaml > out.html
    python3 generate.py examples/toto.yaml -o ../magic-toto-deck/index.html
    python3 generate.py examples/gims.yaml --check ../magic-gims-deck/index.html

If --check is given, render is compared against the reference file and a
unified diff is printed; exit 0 if identical, 1 if any drift.
"""
import argparse
import difflib
import sys
from pathlib import Path

import jinja2
import yaml

ROOT = Path(__file__).resolve().parent
TEMPLATE = ROOT / "template" / "index.html"


def _flatten(data: dict) -> dict:
    """Hoist values from top-level group dicts into a flat namespace.
    YAML profiles group fields under identity/cover/s1/... for readability;
    the template uses flat names like {{ deck_title }}.
    Lists (e.g. crm_months) and scalars at top level pass through unchanged.
    """
    flat: dict = {}
    for key, val in data.items():
        if isinstance(val, dict):
            flat.update(val)
        else:
            flat[key] = val
    return flat


def render(yaml_path: Path) -> str:
    data = _flatten(yaml.safe_load(yaml_path.read_text()))
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(TEMPLATE.parent)),
        keep_trailing_newline=True,
        autoescape=False,
        undefined=jinja2.StrictUndefined,
    )
    tmpl = env.get_template(TEMPLATE.name)
    return tmpl.render(**data)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("yaml", type=Path, help="artist YAML profile")
    p.add_argument("-o", "--out", type=Path, help="write rendered HTML here")
    p.add_argument("--check", type=Path, help="diff against this reference file")
    args = p.parse_args()

    try:
        html = render(args.yaml)
    except jinja2.UndefinedError as e:
        print(f"[generate] Template variable missing: {e}", file=sys.stderr)
        return 2

    if args.check:
        ref = args.check.read_text()
        if html == ref:
            print(f"[generate] OK — render matches {args.check}")
            return 0
        diff = difflib.unified_diff(
            ref.splitlines(keepends=True),
            html.splitlines(keepends=True),
            fromfile=str(args.check),
            tofile=f"render({args.yaml.name})",
            n=2,
        )
        sys.stdout.writelines(diff)
        return 1

    if args.out:
        args.out.write_text(html)
        print(f"[generate] Wrote {args.out} ({len(html):,} bytes)")
    else:
        sys.stdout.write(html)
    return 0


if __name__ == "__main__":
    sys.exit(main())
