"""
Build a fully self-contained version of the project website.

tools/build_site.py produces docs/index.html for GitHub Pages, which pulls its
figures from raw.githubusercontent.com. That only works once the repository is
pushed and public. This script produces the same page with every figure inlined
as a data URI, so it stands alone anywhere — no repository, no network, no
broken images.

    python tools/build_standalone_site.py
"""

from __future__ import annotations

import base64
import io
import json
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from src import config as C  # noqa: E402

OUT = ROOT / "docs" / "standalone.html"
MAX_W = 1500          # figures are 2000-2300 px native; 1500 is ample on screen
JPEG_Q = 88

FIGS = [
    ("fig04_site_comfort_map",     "Predicted summer comfort, square metre by square metre"),
    ("fig02_comfort_bands",        "Shade converts unusable daylight hours into usable ones"),
    ("fig09_diurnal_comfort",      "When the park is comfortable, hour by hour and month by month"),
    ("fig06_feature_importance",   "What actually determines whether a square metre is shaded"),
    ("fig05_surrogate_performance","The surrogate model against ray-traced ground truth"),
    ("fig07_confusion_matrix",     "Predicting thermal stress from the clock and the sun alone"),
    ("fig01_climate_and_comfort",  "Dubai climate, and what it feels like"),
    ("fig10_masterplan",           "The masterplan, drawn from the geometry the models use"),
    ("fig03_shade_by_zone",        "Annual shade coverage by zone type"),
    ("fig08_microclimate_regimes", "The park's operating regimes, found by clustering"),
]


def inline(name: str) -> tuple[str, int]:
    """Downscale and inline a figure as a data URI. Returns (uri, kb)."""
    p = C.FIGURES / f"{name}.png"
    im = Image.open(p).convert("RGB")
    if im.width > MAX_W:
        im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=JPEG_Q, optimize=True, progressive=True)
    b = buf.getvalue()
    return "data:image/jpeg;base64," + base64.b64encode(b).decode(), len(b) // 1024


def main() -> None:
    src = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")

    total = 0
    for name, _cap in FIGS:
        uri, kb = inline(name)
        total += kb
        raw = f"https://raw.githubusercontent.com/{C.GITHUB_USER}/{C.GITHUB_REPO}/main/figures/{name}.png"
        src = src.replace(f'src="{raw}"', f'src="{uri}"')
        print(f"  {name:<30} {kb:>5} KB")

    # The figure links and submission-file links point at a repository that does
    # not exist yet. Neutralise them rather than shipping dead links.
    blob = f"{C.GITHUB_URL}/blob/main"
    src = src.replace(f'<a href="{blob}/figures/', '<a data-href="')
    src = src.replace(
        f'<a class="btn" href="{blob}/notebooks/AL_SAFA_2_PARK_COMPLETE_ANALYSIS.ipynb">'
        f'📓 The analysis notebook</a>',
        '<span class="btn" style="opacity:.55;cursor:default">📓 Notebook — in the repository</span>'
    )
    src = src.replace(
        '<p class="sub">Mapped to the Dubai Municipality upload form. Every link goes to the file on GitHub.</p>',
        '<p class="sub">Mapped to the Dubai Municipality upload form. '
        'File names and sizes are read from the actual submission folders; '
        'the files themselves live in the repository.</p>'
    )
    src = src.replace(f'<li><a href="{blob}/submission/', '<li><span data-href="')
    src = src.replace('</a><span class="sz">', '</span><span class="sz">')

    # A short banner explaining what this copy is.
    banner = (
        '<div style="background:var(--panel);border:1px solid var(--rule);'
        'border-left:3px solid var(--accent-2);border-radius:10px;padding:16px 20px;'
        'margin:22px 0 0;font-size:14.5px;line-height:1.6;color:var(--ink-2)">'
        '<strong style="color:var(--ink)">Self-contained copy.</strong> '
        'Every figure on this page is embedded in the file itself — nothing is fetched '
        'from anywhere. It is the same page that will serve from GitHub Pages once the '
        'repository is published; there, the figure and file links become live.'
        '</div>'
    )
    src = src.replace('</header>', '</header>' + f'<div class="wrap">{banner}</div>', 1)

    OUT.write_text(src, encoding="utf-8")
    size_mb = OUT.stat().st_size / 1024 / 1024
    print(f"\n  figures inlined : {total} KB")
    print(f"  wrote {OUT.name} ({size_mb:.2f} MB)")
    if size_mb > 9:
        print("  WARNING: large for a single page — consider lowering MAX_W or JPEG_Q")


if __name__ == "__main__":
    main()
