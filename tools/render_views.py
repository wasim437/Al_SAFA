"""Render still views of the park from the project's own 3D model.

WHY THIS EXISTS
---------------
The concept film is the only place this park exists in three dimensions. Its
geometry is written by tools/sync_film.py straight out of src/plan.py, so a
still rendered from it is guaranteed to agree with the masterplan, the section,
the planting plan and every number in the submission.

That guarantee is the point. Six earlier AI renders were withdrawn for showing a
different park, and the first aerial generated in August 2026 came back as a
closed ring — a plan form this project tested and rejected. An image generator
cannot promise to draw your actual scheme. This can, because it is drawing the
actual arc.

These are not photoreal and are not a substitute for renders. They are accurate
plates: correct arc, correct 131 trees at mature canopy, correct 18 m gridshell
at 4.5 m, and shadows computed by the same NOAA solar algorithm the analysis
runs, at 25.190°N.

    python tools/render_views.py

Writes 3840x2160 JPEGs to design/renders/model/. JPEG because these
go into the upload PDFs and a 4K PNG of flat shaded geometry runs to
7 MB for no visible gain over quality 90.
"""

from __future__ import annotations

import base64
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILM = ROOT / "submission" / "12_Concept_Animation_Video" / "concept_film.html"
OUT = ROOT / "design" / "renders" / "model"

# pos and tgt are world metres: x east, y north, z up. The site is 150 x 100 m
# with the arc centre off-site to the north, so a camera south of y=0 looks
# back across the whole park.
VIEWS = [
    dict(name="model_aerial_crescent.jpg",
         pos=[75, -210, 190], tgt=[75, 52, 0], fov=36, hour=15.5,
         caption="The crescent from the south — one open arc, 141 m radius",
         sub="18 m gridshell at 4.5 m over a 7 m walk · 131 trees at mature "
             "canopy · shadows computed at 25.190°N, 15 August 15:30"),
    dict(name="model_aerial_oblique.jpg",
         pos=[-40, -150, 150], tgt=[80, 50, 0], fov=40, hour=16.5,
         caption="Oblique from the south-west — the arc against the rooms",
         sub="Every room struck off the same arc centre, so none is a rectangle"),
    dict(name="model_eye_level_walk.jpg",
         pos=[26, 60.5, 1.72], tgt=[62, 50.5, 3.2], fov=54, hour=14.6,
         labels=False,
         caption="On the Crescent Walk, looking east — 15 August, 14:36",
         sub="The far end is hidden by the curve; that is the spatial argument "
             "for bowing the route"),
    dict(name="model_night_crescent.jpg",
         pos=[75, -150, 92], tgt=[75, 52, 0], fov=38, hour=19.4, night=True,
         caption="After dark — the canopy lit from within",
         sub="Nineteen lamps along the walk · the park reads as one line of "
             "light"),
]


def main() -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("  [X] playwright not installed — pip install playwright")
        print("      then: python -m playwright install chromium")
        return 1

    if not FILM.exists():
        print(f"  [X] no film at {FILM}")
        return 1

    OUT.mkdir(parents=True, exist_ok=True)
    print("=" * 78)
    print("  RENDERING STILLS from the project's own 3D model")
    print("=" * 78)

    errs: list[str] = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1400, "height": 820})
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(FILM.as_uri())
        pg.wait_for_function("() => !!window.__view", timeout=30000)
        # The play overlay sits above the canvas and would be composited into
        # any element screenshot.
        pg.evaluate("() => { const o = document.getElementById('opener');"
                    " if (o) o.hidden = true; }")

        # 2x the film's 1920x1080 working space. Every coordinate in the film is
        # written in that space, so this resolves at 4K rather than upscaling.
        pg.evaluate("() => window.__view.setStage(2)")

        for v in VIEWS:
            pg.evaluate("(o) => window.__view.still(o)", v)
            path = OUT / v["name"]
            # Read the canvas itself, not a screenshot of the element. An
            # element screenshot captures the CSS box — about 1180 px wide —
            # and would quietly throw away the 4K backing store this whole
            # tool exists to produce.
            b64 = pg.evaluate(
                "() => document.getElementById('stage')"
                ".toDataURL('image/jpeg', 0.92).split(',')[1]")
            path.write_bytes(base64.b64decode(b64))
            kb = path.stat().st_size / 1024
            print(f"  {v['name']:32} {kb:7.0f} KB   {v['caption']}")
        b.close()

    if errs:
        print()
        print("  [X] page errors while rendering:")
        for e in errs[:5]:
            print(f"      {e}")
        return 1

    print()
    print(f"  {len(VIEWS)} view(s) -> design/renders/model/")
    print("  These agree with the masterplan by construction — they are drawn")
    print("  from the same geometry, not from a description of it.")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
