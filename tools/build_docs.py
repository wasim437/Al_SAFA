"""Assemble docs/ into one website.

There used to be three of them. `docs/index.html` is the analytics portal;
`docs/summary.html` was a static one-pager whose every link pointed at a GitHub
repository that has not been pushed, so none of them resolved; and
`docs/summary_offline.html` was the same page again with 2.5 MB of base64 PNGs
inlined. Three entry points, two of them dead ends, and none of them showing the
drawings.

This makes docs/ a single site:

    docs/index.html          the portal — the only entry point
    docs/assets/renders/     the photoreal renders
    docs/assets/figures/     the ten generated charts
    docs/assets/drawings/    section, elevation, circulation, planting
    docs/assets/boards/      the two presentation boards
    docs/_PORTAL/            css, js, generated data, vendored libraries

and writes `docs/_PORTAL/gallery_data.js`, which is what puts the drawings on
the site at all. Before this the website never showed the masterplan.

    python tools/build_docs.py
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

DOCS = ROOT / "docs"
ASSETS = DOCS / "assets"

# (source, destination folder, kind, title, caption)
SHEETS = [
    ("figures/fig10_masterplan.png", "drawings", "Plan",
     "Masterplan — Falaj Al Safa",
     "One arc, and every room struck off its centre. The numbered key is the "
     "room schedule; each area is the shoelace area of the drawn polygon."),
    ("design/visuals/section_crescent.png", "drawings", "Section",
     "Section A–A — the Crescent Canopy",
     "The 7 m walk under an 18 m gridshell at 4.5 m, with the 3 m southern "
     "louvre. Both solstice sun angles are computed, not drawn."),
    ("design/visuals/elevation_crescent.png", "drawings", "Elevation",
     "Elevation — the bay rhythm",
     "6 m structural bays, the perforated soffit at 12% transmittance, and the "
     "louvre screen hanging on the southern face."),
    ("design/visuals/circulation_crescent.png", "drawings", "Circulation",
     "Circulation & accessibility",
     "One shaded primary route, radial sikkas to every room, and Al Madar — "
     "the 438 m running loop — around the whole."),
    ("design/visuals/planting_crescent.png", "drawings", "Planting",
     "Planting plan — 131 trees",
     "Drawn at mature canopy radius. Ghaf takes the southern rank because it is "
     "the most drought-tolerant species in the schedule."),
    ("design/boards/board_1_concept.png", "boards", "Board 1",
     "Presentation board — concept",
     "The concept, the plan, the section and the circulation on one sheet."),
    ("design/boards/board_2_evidence.png", "boards", "Board 2",
     "Presentation board — evidence",
     "What the models measured, and what they changed about the design."),
    ("figures/fig04_site_comfort_map.png", "figures", "Analysis",
     "Predicted summer comfort, square metre by square metre",
     "July afternoon heat index per m². The crescent reads as the coolest "
     "continuous route, and its concave side is measurably cooler."),
    ("figures/fig02_comfort_bands.png", "figures", "Analysis",
     "Shade converts unusable daylight hours into usable ones",
     "The share of the year's 4,402 daylight hours in each comfort band, "
     "exposed today and shaded as designed."),
    ("figures/fig09_diurnal_comfort.png", "figures", "Analysis",
     "When is the park comfortable?",
     "Hour by hour and month by month. The design opens up the late afternoon "
     "in spring and autumn."),
    ("figures/fig03_shade_by_zone.png", "figures", "Analysis",
     "Annual shade coverage by zone type",
     "Ray-traced ground-plane occlusion on a 1 m grid, sampled across the year."),
    ("figures/fig01_climate_and_comfort.png", "figures", "Climate",
     "Dubai climate, and what it feels like",
     "39 years of NCM monthly normals against the modelled heat index."),
    ("figures/fig06_feature_importance.png", "figures", "Model",
     "What actually determines whether a square metre is shaded",
     "Permutation importance. The caption on this figure is generated from the "
     "model output, because the redesign inverted the answer."),
    ("figures/fig05_surrogate_performance.png", "figures", "Model",
     "Does the surrogate reproduce the simulation?",
     "Neural-network predictions against ray-traced ground truth, on the "
     "held-out test set."),
    ("figures/fig07_confusion_matrix.png", "figures", "Model",
     "Predicting thermal stress from the clock and the sun alone",
     "Temperature and humidity withheld. Errors fall between adjacent bands, "
     "never between comfortable and dangerous."),
    ("figures/fig08_microclimate_regimes.png", "figures", "Model",
     "The park's operating regimes, found by clustering",
     "k selected by silhouette score rather than chosen."),
]

RETIRE = {
    "summary.html":
        "Static one-pager whose links all pointed at an unpushed GitHub repo.",
    "summary_offline.html":
        "The same page again with 2.5 MB of base64 PNGs inlined.",
}


def main() -> int:
    for sub in ("renders", "figures", "drawings", "boards"):
        (ASSETS / sub).mkdir(parents=True, exist_ok=True)

    sheets, missing = [], []
    for src, kind, tag, title, caption in SHEETS:
        s = ROOT / src
        if not s.exists():
            missing.append(src)
            continue
        dest = ASSETS / kind / s.name
        shutil.copy2(s, dest)
        sheets.append({
            "src": f"assets/{kind}/{s.name}",
            "group": kind, "tag": tag, "title": title, "caption": caption,
            "kb": round(dest.stat().st_size / 1024),
        })

    (DOCS / "_PORTAL" / "gallery_data.js").write_text(
        "/* GENERATED — python tools/build_docs.py\n"
        "   The drawings and figures the portal displays. Before this file\n"
        "   existed the website showed no drawings at all. */\n"
        "window.AS2_SHEETS = " + json.dumps(sheets, indent=1) + ";\n",
        encoding="utf-8")

    retired = []
    for name, why in RETIRE.items():
        p = DOCS / name
        if p.exists():
            p.unlink()
            retired.append((name, why))

    print(f"docs/assets/          {len(sheets)} sheets copied "
          f"({sum(s['kb'] for s in sheets) / 1024:.1f} MB)")
    for g in ("drawings", "boards", "figures", "renders"):
        n = len(list((ASSETS / g).glob("*")))
        print(f"  assets/{g:<10} {n} file(s)")
    print(f"gallery_data.js       {len(sheets)} entries")
    for name, why in retired:
        print(f"retired               docs/{name} — {why}")
    if missing:
        print("\n  ! missing sources — run the generators first:")
        for m in missing:
            print(f"      {m}")
        print("      python run_analysis.py && python -m src.drawings "
              "&& python -m src.boards")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
