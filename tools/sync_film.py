"""Rewrite the concept film's geometry block from the live masterplan.

The film is a standalone HTML deliverable — it has to run from a single file
with no network — so its geometry is inlined rather than fetched. That makes it
the easiest thing in the project to leave behind: it kept drawing a straight
sine-meandered spine and eight rectangular rooms for as long as nobody looked.

This tool regenerates the block between the two markers in concept_film.html
from src/plan.py, so the film is the same park as the drawings and the portal.

    python tools/sync_film.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src import config as C, plan, solar  # noqa: E402

FILM = ROOT / "submission" / "12_Concept_Animation_Video" / "concept_film.html"
BEGIN = "  // ===== GENERATED GEOMETRY — python tools/sync_film.py ====="
END = "  // ===== END GENERATED GEOMETRY ====="

# Which rooms the film names on screen. Eighteen labels on a moving camera is
# noise; these nine carry the programme and the rest read as ground.
NAMED = {
    "basin": "AL NAKHIL — OASIS BASIN",
    "quiet": "QUIET GARDEN",
    "play": "CHILDREN'S DUNE PLAY",
    "picnic": "FAMILY PICNIC GROVE",
    "fitness": "FITNESS TERRACE",
    "wadi": "BIODIVERSITY WADI",
    "plaza": "COMMUNITY PLAZA",
    "souk": "SOUK",
    "sports": "SPORTS LAWN",
}

# Species -> the film's four tree archetypes (crown radius, height, draw style).
SPECIES_KIND = {"Ghaf": 0, "Neem": 0, "Ficus nitida": 1, "Olive": 2, "Date Palm": 3}


def block() -> str:
    cr = C.CRESCENT
    zones = {z["key"]: z for z in plan.build()}
    trees = solar.tree_positions()

    rooms = []
    for key, label in NAMED.items():
        z = zones.get(key)
        if not z:
            continue
        big = max(z["parts"], key=plan.polygon_area)
        # Decimate: the film redraws these every frame at 30 fps, and 64-point
        # outlines cost more than they show at this scale.
        pts = [[round(float(p[0]), 1), round(float(p[1]), 1)] for p in big[::4]]
        rooms.append({"n": label, "p": pts,
                      "c": [round(float(v), 1) for v in z["label_xy"]]})

    tl = [{"x": round(float(t.x), 1), "y": round(float(t.y), 1),
           "r": float(t.canopy_r_m), "h": float(t.height_m),
           "t": SPECIES_KIND.get(t.species, 0)}
          for t in trees.itertuples()]

    def poly(pts, step=1):
        return [[round(float(a), 1), round(float(b), 1)] for a, b in pts[::step]]

    fx, fy = plan.falaj_polyline(80)
    lx, ly = plan.loop_polyline(120)

    lines = [
        BEGIN,
        "  // The park, straight out of src/plan.py. Do not hand-edit: run the",
        "  // tool. The film is a standalone file, so this is inlined rather",
        "  // than fetched — which is exactly why it has to be regenerated.",
        f"  const SITE = {{ w:{plan.SITE_W:.0f}, d:{plan.SITE_H:.0f} }};",
        "",
        "  // AL HILAL — one circular arc. Sagitta was swept against the",
        "  // 8,760-hour solar model; see src/config.py for the table.",
        "  const CRESCENT = {",
        f"    cx:{plan.ARC_CX:.2f}, cy:{plan.ARC_CY:.4f}, R:{plan.ARC_R:.4f},",
        f"    tMax:{plan.WALK_THETA:.4f},",
        f"    pathW:{cr['path_width_m']}, canopyW:{cr['canopy_width_m']},",
        f"    h:{cr['canopy_height_m']}, louvre:{cr['south_louvre_depth_m']},",
        f"    hSpring:{cr['canopy_height_m']}, hCrown:{cr['canopy_height_m'] + 1.2},",
        "  };",
        f"  const ARC_X0 = {plan.arc_point(-plan.WALK_THETA)[0]:.3f},",
        f"        ARC_X1 = {plan.arc_point(plan.WALK_THETA)[0]:.3f};",
        "",
        "  // The centreline as a function of x. The arc is single-valued over",
        "  // its own span, so the film can keep parameterising by x.",
        "  const arcY = x => CRESCENT.cy - Math.sqrt(Math.max(0,",
        "    CRESCENT.R*CRESCENT.R - (x - CRESCENT.cx)*(x - CRESCENT.cx)));",
        "  // Unit normal in plan, radial and pointing SOUTH — the direction the",
        "  // canopy spans across. On an arc it rotates along the route, which is",
        "  // the entire reason the plan is an arc.",
        "  function arcNormal(x) {",
        "    const s = clamp((x - CRESCENT.cx)/CRESCENT.R, -1, 1);",
        "    return [s, -Math.sqrt(Math.max(0, 1 - s*s))];",
        "  }",
        "",
        f"  const FALAJ = {json.dumps(poly(list(zip(fx, fy))))};",
        f"  const LOOP = {json.dumps(poly(list(zip(lx, ly))))};",
        f"  const MAJLIS = {json.dumps([{k: round(float(v), 1) for k, v in m.items()} for m in plan.majlis_pods()])};",
        f"  const SIKKAK = {json.dumps([poly(s) for s in plan.sikka_lines()])};",
        "",
        f"  const TREES = {json.dumps(tl)};",
        "",
        "  const ROOMS = [",
    ]
    for r in rooms:
        lines.append(f"    {json.dumps(r, ensure_ascii=False)},")
    lines += ["  ];", END]
    return "\n".join(lines)


def _cover_at(frac, sol, month, day, hour):
    m = (sol.index.month == month) & (sol.index.day == day) & (sol.index.hour == hour)
    return float(frac[m].iloc[0]) * 100, float(sol["elevation_deg"][m].iloc[0])


def figures_html() -> str:
    """The claim grid on the film's page, from the pipeline's own numbers."""
    import json

    h = json.loads((C.MODELS / "headline_metrics.json").read_text(encoding="utf-8"))
    cells = [
        ("hot", "42.1&nbsp;°C", "August mean daily maximum — NCM normals, 39-year record"),
        ("hot", f"{h['peak_heat_index_exposed_c']}&nbsp;°C", "Peak heat index, exposed"),
        ("up", f"{h['peak_heat_index_shaded_c']}&nbsp;°C", "Peak heat index, under the canopy"),
        ("", f"{h['daylight_hours_comfortable_exposed_pct']}&nbsp;%",
         "Daylight hours comfortable today"),
        ("up", f"{h['daylight_hours_comfortable_shaded_pct']}&nbsp;%",
         "Daylight hours comfortable as designed"),
        ("", f"{h['spine_shade_canopy_only_pct']}&nbsp;%",
         "Annual shade on the Crescent Walk — canopy and louvre alone"),
        ("", f"{h['spine_mean_per_sqm_shade_pct']}&nbsp;%",
         "The same walk per square metre, with the tree avenue counted"),
        ("", f"{h['annual_daylight_hours']:,}", "Annual daylight hours modelled"),
        ("", f"{h['trees']}", "Trees, five species, from the planting schedule"),
        ("", f"{h['site_mean_shade_pct']}&nbsp;%",
         "Site-wide mean shade — stated, not hidden"),
    ]
    return "\n".join(
        f'      <div class="cell"><div class="v{" " + k if k else ""}">{v}</div>'
        f'<div class="l">{l}</div></div>' for k, v, l in cells)


def section_html() -> str:
    """The honesty note. Recomputed, because the section it describes changed."""
    import numpy as np

    sol = solar.hourly_solar_position()
    frac = solar.crescent_shade_fraction(sol)
    jun, jun_e = _cover_at(frac, sol, 6, 21, 12)
    dec9, dec9_e = _cover_at(frac, sol, 12, 21, 9)
    dec15, dec15_e = _cover_at(frac, sol, 12, 21, 15)
    lit = frac.dropna()
    monthly = lit.groupby(lit.index.month).mean() * 100
    worst_m = int(monthly.idxmin())
    none_h = int((lit < 0.05).sum())
    cr = C.CRESCENT
    month_name = ["", "January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November", "December"][worst_m]

    return f"""      <h3>Where the canopy still loses</h3>
      <p>The same model, evaluated on the {cr['path_width_m']:.0f} m walk beneath its
        {cr['canopy_width_m']:.0f} m gridshell at {cr['canopy_height_m']} m, with the
        {cr['south_louvre_depth_m']:.0f} m southern louvre:</p>
      <div class="grid" style="grid-template-columns:1fr">
        <div class="cell"><div class="v up">{jun:.0f}%</div><div class="l">21 June, noon —
          sun at {jun_e:.1f}°, walk fully covered</div></div>
        <div class="cell"><div class="v up">{dec9:.0f}%</div><div class="l">21 December, 09:00 —
          sun at {dec9_e:.1f}°. The louvre is what holds this; the plane alone
          loses the path entirely</div></div>
        <div class="cell"><div class="v hot">{dec15:.0f}%</div><div class="l">21 December, 15:00 —
          sun at {dec15_e:.1f}° in the south-west. This is the worst case, and it
          is not fixed by more structure</div></div>
      </div>
      <p style="margin-top:14px">
        {month_name} is the weakest month at {monthly.min():.0f}% mean coverage, and
        {none_h} hours a year leave the walk with no shade anywhere along it. The
        straight canopy this scheme replaced left {330}. That reduction is what the
        arc buys, and it costs about a point of mean coverage — which is the trade,
        stated in the direction that is not flattering.
      </p>"""


def main() -> int:
    src = FILM.read_text(encoding="utf-8")
    if BEGIN not in src:
        raise SystemExit(
            "concept_film.html has no generated-geometry markers. Add\n"
            f"{BEGIN}\n...\n{END}\naround the geometry block first.")
    new = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END), lambda _: block(),
                 src, flags=re.S)

    # The two prose blocks quote figures that the redesign moved. They are
    # regenerated too — a film page that states 69.6% while the model says 87.3%
    # is exactly the drift this project keeps having to correct.
    new = re.sub(r'(<div class="grid" id="filmFigures">).*?(</div>\s*\n\s*<!-- END GENERATED FIGURES -->)',
                 lambda m: m.group(1) + "\n" + figures_html() + "\n    " + m.group(2),
                 new, flags=re.S)
    new = re.sub(r'(<div id="filmSection">).*?(</div>\s*\n\s*<!-- END GENERATED SECTION NOTE -->)',
                 lambda m: m.group(1) + "\n" + section_html() + "\n      " + m.group(2),
                 new, flags=re.S)

    FILM.write_text(new, encoding="utf-8")
    print(f"concept_film.html  crescent R={plan.ARC_R:.1f} m · "
          f"{len(solar.tree_positions())} trees · {len(NAMED)} named rooms · "
          f"figures and section note regenerated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
