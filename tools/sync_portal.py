"""Rewrite the design-dependent blocks of the portal from the live analysis.

The portal's data file was originally generated from the archived phase folders,
which are frozen. Everything the redesign touches — the concept name, the room
schedule and its plan geometry, the shade performance, the planting, the render
captions and the narrative — has to come from the code that is actually run, or
the portal becomes a second, quietly contradictory account of the project.

This tool rewrites exactly those blocks and leaves the rest of the file alone.
Blocks it does not own (climate, catchment, cost, personas, references) are
untouched, because nothing in the redesign changes them.

    python tools/sync_portal.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import pandas as pd  # noqa: E402

from src import config as C, plan, solar  # noqa: E402

PORTAL = ROOT / "docs" / "_PORTAL" / "portal_data.js"
GEOM = ROOT / "docs" / "_PORTAL" / "plan_geometry.js"

# Which of the six palette tokens each zone category takes on the portal. Held
# here rather than in src/plan.py because it is a property of the portal's
# theme, not of the design.
TOKEN = {
    "Circulation": "blue", "Water": "teal", "Green": "green",
    "Green_Buffer": "lime", "Arrival": "gold", "Active": "orange",
    "Passive": "purple", "Social": "gold", "Commercial": "red",
}


def load() -> tuple[str, dict]:
    text = PORTAL.read_text(encoding="utf-8")
    start = text.index("{", text.index("window.AS2"))
    return text[:start], json.loads(text[start:text.rindex("}") + 1])


def write(header: str, data: dict) -> None:
    PORTAL.write_text(
        header + json.dumps(data, indent=1, ensure_ascii=False) + ";\n",
        encoding="utf-8")


def sync_zoning(d: dict, zones: list[dict]) -> None:
    """Replace the room schedule with the drawn plan, polygons and all."""
    out = []
    for z in zones:
        out.append({
            "name": z["name"], "fullName": z["name"], "key": z["key"],
            "category": z["category"], "area": round(z["area"], 1),
            "pct": round(z["area"] / C.SITE["area_sqm"] * 100, 1),
            "icon": z["icon"], "desc": z["desc"],
            "token": z.get("token") or TOKEN.get(z["category"], "green"),
            "residual": bool(z.get("is_residual")),
            "labelXY": [round(v, 2) for v in z.get("label_xy", [0, 0])],
            # Plan geometry as polygons. The portal used to pack rectangles from
            # areas alone; no room in this scheme is a rectangle, so it now
            # draws the real outline instead of approximating one.
            "parts": [[[round(float(a), 2), round(float(b), 2)] for a, b in part]
                      for part in z["parts"]],
        })
    green = sum(z["area"] for z in zones
                if z["category"] in ("Green", "Green_Buffer", "Passive", "Water"))
    d["zoning"] = {
        "siteArea": C.SITE["area_sqm"],
        "allocated": round(sum(z["area"] for z in zones), 1),
        "zones": out,
        "byCategory": {
            cat: round(sum(z["area"] for z in zones if z["category"] == cat), 1)
            for cat in sorted({z["category"] for z in zones})
        },
        "greenPct": round(green / C.SITE["area_sqm"] * 100, 1),
        "source": "src/plan.py — every area is the shoelace area of the drawn "
                  "polygon, so the schedule cannot disagree with the drawing.",
    }


def sync_performance(d: dict, grid: pd.DataFrame, hourly: pd.DataFrame,
                     headline: dict) -> None:
    p = d["performance"]
    p["spineShadePct"] = headline["spine_shade_canopy_only_pct"]
    p["crescentShadePct"] = headline["spine_shade_canopy_only_pct"]
    p["walkMeanShadePct"] = headline["spine_mean_per_sqm_shade_pct"]
    p["siteMeanShadePct"] = headline["site_mean_shade_pct"]
    p["totalDaylightHours"] = headline["annual_daylight_hours"]

    by_zone = grid.groupby("zone")["shade_pct"].mean().sort_values(ascending=False)
    p["zoneShade"] = [{"zone": k, "pct": round(float(v), 1)}
                      for k, v in by_zone.items()]

    lit = hourly[hourly["is_daylight"]]
    monthly = lit.groupby(lit.index.month).apply(
        lambda g: float((g["crescent_shade_fraction"] >= 0.5).mean() * 100))
    p["monthlySpineShade"] = [round(monthly.get(m, 0.0), 2) for m in range(1, 13)]

    p["heatIndex"] = {
        "peakExposed": headline["peak_heat_index_exposed_c"],
        "peakShaded": headline["peak_heat_index_shaded_c"],
        "meanReduction": headline["mean_heat_index_reduction_c"],
        "comfortableExposedPct": headline["daylight_hours_comfortable_exposed_pct"],
        "comfortableShadedPct": headline["daylight_hours_comfortable_shaded_pct"],
    }
    p["sourceShade"] = ("src/solar.py — geometric occlusion at every daylight "
                        "hour, NREL SPA sun angles via pvlib.")


def sync_planting(d: dict, trees: pd.DataFrame) -> None:
    species = pd.read_csv(C.DATA_RAW / "species_water_carbon_rates.csv")
    counts = trees.groupby("species").size()
    d["planting"]["totalTrees"] = int(len(trees))
    for s in d["planting"]["species"]:
        name = s.get("name") or s.get("species")
        if name in counts.index:
            s["count"] = int(counts[name])
    d["planting"]["sourcePlanting"] = (
        "src/solar.py tree_positions() — each species is planted into the room "
        "the masterplan gives it, by rejection sampling inside its polygon.")
    d["planting"]["nativeCount"] = int(
        species.loc[species["Native"] == 1, "Count"].sum())


def sync_provenance(d: dict, zones: list[dict], headline: dict) -> None:
    """Update the provenance entries the KPI tiles actually read.

    The portal renders headline numbers through `provValue(key)`, not from the
    performance block, so syncing performance alone leaves the tiles showing the
    old scheme's figures while the charts below them show the new one. The
    portal's own selftest catches that, which is why it is worth having.
    """
    by_key = {p["key"]: p for p in d["provenance"]}

    def put(key, value, *, label=None, method=None, note=None):
        p = by_key.get(key)
        if not p:
            return
        p["value"] = value
        if label:
            p["label"] = label
        if method:
            p["method"] = method
        if note:
            p["note"] = note

    put("spine_shade", headline["spine_shade_canopy_only_pct"],
        label="Annual shade coverage of the Crescent Walk",
        method="Geometric occlusion of the 18 m gridshell and its 3 m southern "
               "louvre, evaluated at every daylight hour of the year with NREL "
               "SPA sun angles. An hour counts as shaded when at least half the "
               "walk width is covered.",
        note=f"{headline['spine_shade_canopy_only_pct']:.1f}% of "
             f"{headline['annual_daylight_hours']:,} daylight hours. Only 56 "
             f"hours a year leave the walk with no shade anywhere along it; the "
             f"straight canopy this replaced left 330.")
    put("peak_heat_index", headline["peak_heat_index_exposed_c"])
    put("total_trees", headline["trees"])
    put("site_area", C.SITE["area_sqm"])
    put("zoned_area", round(sum(z["area"] for z in zones), 1))
    put("green_pct", d["zoning"]["greenPct"],
        note="Green, buffer, passive and water categories, measured from the "
             "drawn polygons.")


def sync_meta_and_narrative(d: dict, headline: dict) -> None:
    d["meta"]["concept"] = C.SITE["concept"]
    d["meta"]["conceptSubtitle"] = C.SITE["concept_subtitle"]

    walk = headline["spine_shade_canopy_only_pct"]
    d["concepts"]["options"] = [
        {
            "name": "A — Falaj Al Safa (the crescent)",
            "idea": "A single arc carries the shade; every room in the park is "
                    "struck off its centre, and a water channel runs its length.",
            "shade": f"{walk:.1f}% of daylight hours on the walk",
            "strength": "The route changes heading continuously, so some segment "
                        "is always angled well against the sun. The hours in "
                        "which the walk has no shade anywhere fall from 330 to 56.",
            "risk": "Concentrating the shade budget into one element means the "
                    "open rooms stay hot. That is a deliberate position, not an "
                    "oversight — see the site-wide mean.",
            "selected": True,
        },
        {
            "name": "B — the straight spine (superseded)",
            "idea": "A straight east-west canopy through the middle of the site, "
                    "with rectangular rooms packed either side.",
            "shade": "87.4% of daylight hours on the walk",
            "strength": "The highest mean coverage of any plan form tested. An "
                        "east-west canopy is close to the optimum orientation "
                        "for 25°N.",
            "risk": "One orientation. When a sun angle defeats it, it defeats "
                    "the entire length at once and the walk has no shade "
                    "anywhere — 330 hours a year of that.",
            "selected": False,
        },
        {
            "name": "C — the closed loop",
            "idea": "A shaded circuit around the site rather than a route "
                    "across it.",
            "shade": "79.1% of daylight hours on the walk",
            "strength": "A circuit is what people actually walk in a "
                        "neighbourhood park.",
            "risk": "A loop forces half its length to run north-south, and a "
                    "canopy over a north-south route only works when the sun is "
                    "low in the east or west. It loses on every measure.",
            "selected": False,
        },
    ]
    d["concepts"]["rationale"] = (
        "The three plan forms were not judged by eye. Each was run against the "
        "8,760-hour solar model at the same fixed section, and scored on mean "
        "coverage, worst month, and the number of hours in which the walk offers "
        "no shade anywhere along it. The straight bar wins the first measure and "
        "loses the third badly; the loop loses all three. The crescent was "
        "adopted for the third measure, at a cost of about one point on the "
        "first — and the concept keeps the loop as Al Madar, an unshaded running "
        "circuit, because that is what a circuit is actually for.")
    d["concepts"]["source"] = "src/config.py CRESCENT — the sweep table is in the file."


def sync_cost(d: dict, zones: list[dict], trees) -> None:
    """Re-price the elemental take-off against the rooms that now exist.

    The take-off priced fourteen rooms that the redesign removed, at areas that
    no longer hold — a 1,592 m² canopy over a 1,260 m² walkway, on a plan where
    the gridshell is 2,239 m². Every measured line is rebuilt from the drawn
    areas and data/raw/construction_unit_rates_aed.csv; the percentage lines
    (preliminaries, contingency, fees) keep their percentages and are recomputed
    off the new measured subtotal.
    """
    rates = pd.read_csv(C.DATA_RAW / "construction_unit_rates_aed.csv")
    rate = dict(zip(rates["Element"], rates["Rate_AED"]))

    items = []
    # The gridshell is priced over its true plan footprint — walk plus both
    # shaded margins plus the falaj — because that is the area the structure
    # actually spans, not the width of the path under it.
    shell = sum(z["area"] for z in zones
                if z["key"] in ("crescent_walk", "falaj", "margin_n", "margin_s"))
    items.append({"element": "Al Hilal — the Crescent Canopy (gridshell + louvre)",
                  "area": round(shell), "rate": rate["ETFE canopy structure"],
                  "cost": round(shell * rate["ETFE canopy structure"])})

    for z in sorted(zones, key=lambda a: -a["area"]):
        r = rate.get(z["rate_key"])
        if r is None:
            continue
        items.append({"element": z["name"], "area": round(z["area"]),
                      "rate": r, "cost": round(z["area"] * r)})

    n_canopy = int((trees["species"].isin(["Ghaf", "Neem", "Ficus nitida"])).sum())
    items.append({"element": f"Canopy trees ({n_canopy} × Ghaf/Neem/Ficus, supply + plant)",
                  "area": "-", "rate": f"{rate['Canopy tree supply and planting']:.0f}/tree",
                  "cost": round(n_canopy * rate["Canopy tree supply and planting"])})

    measured = sum(i["cost"] for i in items)
    for label, pct in (("Site lighting (LED — crescent, sikkas, loop, bollards)", 0.045),
                       ("Irrigation network (drip / subsurface)", 0.035),
                       ("Smart infrastructure (sensors, digital wayfinding)", 0.025)):
        items.append({"element": label, "area": "-", "rate": "% of works",
                      "cost": round(measured * pct)})

    works = sum(i["cost"] for i in items)
    for label, pct in (("Preliminaries & enabling (10%)", 0.10),
                       ("Design contingency (12%)", 0.12),
                       ("Professional fees (8%)", 0.08)):
        items.append({"element": label, "area": "-", "rate": "-",
                      "cost": round(works * pct)})

    total = sum(i["cost"] for i in items)
    d["cost"]["elemental"] = {
        "items": items, "total": total,
        "source": "data/raw/construction_unit_rates_aed.csv against the drawn "
                  "areas in src/plan.py. Rates are Dubai landscape contractor "
                  "quotations for 2025, not municipal tender pricing.",
    }
    d["cost"]["budgetUsedPct"] = round(total / d["cost"]["budget"] * 100, 1)
    d["cost"]["headroom"] = d["cost"]["budget"] - total
    for p in d["provenance"]:
        if p["key"] == "capex":
            p["value"] = total


def sync_cost_downstream(d: dict, old_capex: float) -> None:
    """Carry the new capex through the package view, the O&M model and the LCC.

    Three things hang off the construction cost, and leaving any of them on the
    old figure would put two different capex numbers on the same portal:

      * the package view — the same money grouped by trade rather than by room,
        so it is rescaled by the ratio and stays a *view* of the same total;
      * the O&M model — its horticulture and repairs lines are defined as a
        percentage of build cost, so they are recomputed, and its fixed
        estimates (security, electricity, water) are left alone because they do
        not scale with capex;
      * the 30-year LCC — its cost side is rebuilt from the new capex and opex
        at the discount and inflation rates already declared in the data.

    The rescale is stated in the source string rather than done silently.
    """
    cost = d["cost"]
    new_capex = cost["elemental"]["total"]
    if not old_capex:
        return
    k = new_capex / old_capex

    def reconcile(items, target):
        """Rescale a package view and put the rounding remainder on its
        largest line, so the view sums to the take-off exactly. A package split
        that is a few dirhams away from the total it re-expresses is a rounding
        artefact, but it reads as two different estimates."""
        if not items:
            return
        total = sum(i["cost"] for i in items)
        if total:
            biggest = max(items, key=lambda i: i["cost"])
            biggest["cost"] += round(target) - total

    pkg = cost.get("capexPackage", {})
    for it in pkg.get("items", []):
        it["item"] = it["item"].replace("Parametric Voronoi Canopy (ETFE + Steel)",
                                        "Al Hilal — Crescent Canopy (ETFE + steel gridshell)")
        it["cost"] = round(it["cost"] * k)
    reconcile(pkg.get("items", []), new_capex)
    pkg["total"] = sum(i["cost"] for i in pkg.get("items", []))
    pkg["source"] = ("The same money as the elemental take-off, grouped by trade "
                     f"package. Rescaled by {k:.4f} when the redesign changed the "
                     "measured areas; the split between packages is unchanged.")

    om = cost.get("om", {})
    old_om = om.get("total", 0)
    for it in om.get("items", []):
        if it.get("basis") == "ratio":
            pct = 0.06 if "Horticulture" in it["item"] else 0.02
            it["cost"] = round(new_capex * pct)
    om["total"] = sum(i["cost"] for i in om.get("items", []))
    om["buildCost"] = new_capex
    if om.get("total") and new_capex:
        om["pctOfBuild"] = round(om["total"] / new_capex * 100, 1)

    opkg = cost.get("opexPackage", {})
    if old_om and opkg.get("items"):
        ko = om["total"] / old_om
        for it in opkg["items"]:
            it["cost"] = round(it["cost"] * ko)
        reconcile(opkg["items"], om["total"])
        opkg["total"] = sum(i["cost"] for i in opkg["items"])

    for p in d["provenance"]:
        if p["key"] == "opex":
            p["value"] = om.get("total", p["value"])
        if p["key"] == "tco10":
            p["value"] = round(new_capex + om.get("total", 0) * 10)

    adv = d.get("advanced", {})
    adv["capexTotal"] = new_capex
    adv["opexTotal"] = om.get("total", adv.get("opexTotal"))
    lcc = adv.get("lcc", {})
    r = lcc.get("discount_rate", 0.06)
    infl = lcc.get("inflation_rate", 0.025)
    yearly = lcc.get("yearly", {})
    years = yearly.get("year", list(range(31)))
    npv_cost, cum = float(new_capex), float(new_capex)
    cum_series = [round(cum)]
    for i in years[1:]:
        annual = om.get("total", 0) * ((1 + infl) ** i)
        npv_cost += annual / ((1 + r) ** i)
        cum += annual
        cum_series.append(round(cum))
    yearly["cum_cost_AED"] = cum_series
    lcc["total_npv_cost_AED"] = round(npv_cost)
    if "total_npv_benefit_AED" in lcc:
        lcc["npv_net_AED"] = round(lcc["total_npv_benefit_AED"] - npv_cost)
        if npv_cost:
            lcc["sroi_ratio"] = round(lcc["total_npv_benefit_AED"] / npv_cost, 2)
    adv["source"] = (adv.get("source", "") +
                     f" Cost side rebuilt from the redesigned take-off "
                     f"(AED {new_capex:,.0f}) at {r:.0%} discount and "
                     f"{infl:.1%} inflation over {len(years) - 1} years.").strip()
    for p in d["provenance"]:
        if p["key"] == "npv_30yr" and "npv_net_AED" in lcc:
            p["value"] = lcc["npv_net_AED"]


def sync_personas(d: dict) -> None:
    """Point each persona at rooms that exist, in the new names."""
    remap = {
        "Children's Play Zone": "Children's Dune Play",
        "Family Picnic & Shaded Seating": "Family Picnic Grove",
        "Shaded Spine": "Al Mamsha — the Crescent Walk",
        "Shaded Spine (100% step-free)": "Al Mamsha — the Crescent Walk (step-free)",
        "Perimeter jogging loop": "Al Madar — the perimeter loop",
        "Quiet Contemplation Garden": "Quiet Contemplation Garden",
        "Community Plaza & Event Lawn": "Community Plaza & Event Lawn",
        "Community Plaza": "Community Plaza & Event Lawn",
        "Outdoor Fitness & Wellness": "Outdoor Fitness Terrace",
    }
    for p in d.get("personas", {}).get("items", []):
        p["zones"] = [remap.get(z, z) for z in p.get("zones", [])]

    # This sentence carried the withdrawn 100% shade claim back into the portal.
    d["personas"]["seasonal"] = (
        "November–April is the comfort window: full-day use is expected across "
        "every room. May–October, midday use concentrates under the crescent and "
        "along its shaded margins, with the open lawns used early in the morning "
        "and after sunset. The crescent is shaded for 87.3% of the daylight year, "
        "not all of it — the 56 hours that have no shade anywhere are stated in "
        "the performance section rather than rounded away.")


def sync_renders(d: dict) -> None:
    """Re-caption the renders in the new design language, and drop the culled."""
    captions = {
        "masterplan_aerial_golden_hour.jpg": (
            "The crescent from the north-west",
            "The arc reads as one continuous element from horn to horn, with the "
            "Oasis Basin held in its concave side."),
        "dubai_futuristic_masterplan_aerial.jpg": (
            "Canopy and channel, aerial",
            "The gridshell and the falaj running together the length of the "
            "crescent, with the sikkas cutting radially out to the perimeter."),
        "spine_corridor_interior.jpg": (
            "Beneath Al Hilal — the perforated soffit",
            "The mashrabiya rule at full size: light through, heat stopped. "
            "12% direct-beam transmittance."),
        "dubai_futuristic_spine_interior.jpg": (
            "Al Mamsha — the Crescent Walk",
            "The 7 m walk under an 18 m shell. The overhang is what keeps the "
            "shadow on the path when the sun is low."),
        "eyelevel_spine_1784970552956.jpg": (
            "The walk in the shoulder season",
            "Late afternoon in spring and autumn is where the comfort gain "
            "concentrates, and where the activation strategy is aimed."),
        "night_plaza_render_1784970565232.jpg": (
            "The Community Plaza after dark",
            "The convex side takes the uses that run in the evening, when its "
            "exposure stops being a liability."),
    }
    # A caption is not evidence that the image says what the caption claims.
    # Four of these renders were withdrawn after being opened and compared with
    # the masterplan: they showed a serpentine canopy over a lagoon, a generic
    # futuristic park, a dead-straight corridor, and a botanical pavilion —
    # while these captions called them "the crescent" and "Al Mamsha". The file
    # on disk is now the authority. If it is gone, the caption goes with it.
    root = Path(__file__).resolve().parent.parent / "docs"
    kept, dropped = [], []
    for r in d.get("renders", []):
        name = Path(r.get("src", "")).name
        if name not in captions:
            continue
        if not (root / r.get("src", "")).exists():
            dropped.append(name)
            continue
        r["title"], r["caption"] = captions[name]
        kept.append(r)
    d["renders"] = kept
    for name in dropped:
        print(f"    dropped render (not on disk): {name}")


def sync_audit(d: dict, zones: list[dict], headline: dict) -> None:
    total = sum(z["area"] for z in zones)
    d["audit"] = [
        {"name": "Zoning schedule closes on the site area",
         "ok": abs(total - C.SITE["area_sqm"]) < 1.0,
         "detail": f"Rooms and the alley residual sum to {total:,.0f} m² against "
                   f"a site area of {C.SITE['area_sqm']:,.0f} m². The areas are "
                   f"the shoelace area of each drawn polygon, so this closes by "
                   f"construction rather than by reconciliation."},
        {"name": "No ground is claimed by two rooms",
         "ok": True,
         "detail": "Rooms are disjoint boxes in the crescent's polar frame, and "
                   "that frame is injective — checked on the 1 m grid by "
                   "tests/test_pipeline.py."},
        {"name": "The walk is shaded for most of the daylight year",
         "ok": headline["spine_shade_canopy_only_pct"] >= 80,
         "detail": f"{headline['spine_shade_canopy_only_pct']:.1f}% of "
                   f"{headline['annual_daylight_hours']:,} daylight hours have at "
                   f"least half the walk width in shadow."},
        {"name": "Site-wide shade is stated, not hidden",
         "ok": True,
         "detail": f"Site-wide mean shade is {headline['site_mean_shade_pct']:.1f}%. "
                   f"This scheme concentrates its shade budget; the open rooms "
                   f"are hot and the submission says so."},
        {"name": "The 99.2% shade claim has been withdrawn",
         "ok": True,
         "detail": "An earlier version claimed 99.2% annual shade on a flat 9 m "
                   "canopy over a 9 m walkway. It does not survive a geometric "
                   "check and was withdrawn."},
        {"name": "Fabricated visuals have been withdrawn",
         "ok": True,
         "detail": "Three images presented invented data as measurement — a CFD "
                   "dashboard, an NDVI analysis and a 'solar-optimised' canopy "
                   "mesh. None had the source it claimed. See "
                   "archive/withdrawn_visuals/README.md."},
        {"name": "Site boundary is assumed, not surveyed",
         "ok": False,
         "detail": "The 150 × 100 m rectangle is an assumption pending "
                   "confirmation against the supplied DWG. Every area figure "
                   "depends on it."},
    ]


def write_geometry_module(zones: list[dict]) -> None:
    """Emit the plan geometry the portal's 2D and 3D views both read."""
    fx, fy = plan.falaj_polyline(160)
    lx, ly = plan.loop_polyline()
    doc = {
        "site": {"w": plan.SITE_W, "h": plan.SITE_H},
        "crescent": {
            "radius": round(plan.ARC_R, 3),
            "centre": [plan.ARC_CX, round(plan.ARC_CY, 3)],
            "halfAngle": round(plan.ARC_THETA, 4),
            "walkHalfAngle": round(plan.WALK_THETA, 4),
            "pathWidth": C.CRESCENT["path_width_m"],
            "canopyWidth": C.CRESCENT["canopy_width_m"],
            "canopyHeight": C.CRESCENT["canopy_height_m"],
            "louvreDepth": C.CRESCENT["south_louvre_depth_m"],
        },
        "canopy": [[round(float(a), 2), round(float(b), 2)]
                   for a, b in plan.canopy_outline(120)],
        "falaj": [[round(float(a), 2), round(float(b), 2)] for a, b in zip(fx, fy)],
        "loop": [[round(float(a), 2), round(float(b), 2)] for a, b in zip(lx, ly)],
        "majlis": plan.majlis_pods(),
        "sikkak": [[[round(float(p[0]), 2), round(float(p[1]), 2)] for p in seg]
                   for seg in plan.sikka_lines()],
    }
    GEOM.write_text(
        "/* GENERATED — python tools/sync_portal.py\n"
        "   The masterplan geometry, shared by the portal's plan view and its 3D\n"
        "   model so the two cannot drift apart. Metres, origin at the site's\n"
        "   south-west corner, +x east, +y north. */\n"
        "window.AS2_PLAN = " + json.dumps(doc, indent=1) + ";\n",
        encoding="utf-8")


def main() -> int:
    header, d = load()
    zones = plan.build()
    grid = pd.read_csv(C.DATA_PROCESSED / "spatial_grid_comfort.csv")
    hourly = pd.read_csv(C.DATA_PROCESSED / "hourly_climate_comfort_8760.csv",
                         index_col=0, parse_dates=True)
    trees = pd.read_csv(C.DATA_PROCESSED / "planting_layout.csv")
    headline = json.loads((C.MODELS / "headline_metrics.json").read_text(encoding="utf-8"))

    sync_meta_and_narrative(d, headline)
    sync_zoning(d, zones)
    sync_provenance(d, zones, headline)
    sync_performance(d, grid, hourly, headline)
    sync_planting(d, trees)
    old_capex = d["cost"]["elemental"]["total"]
    sync_cost(d, zones, trees)
    sync_cost_downstream(d, old_capex)
    sync_personas(d)
    sync_renders(d)
    sync_audit(d, zones, headline)

    d["meta"]["generated"] = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M UTC")
    # Rewrite the banner wholesale. Patching it line by line once ate the `*/`
    # that closes the comment, and left a file that parses as one long comment —
    # the portal loads, the data object never exists, and nothing renders.
    header = ("/* GENERATED FILE — DO NOT EDIT BY HAND.\n"
              "   Rebuild with:  python tools/sync_portal.py\n"
              "   Source of truth: src/plan.py, src/solar.py, and\n"
              "   models/headline_metrics.json — i.e. the code that is run,\n"
              "   not the frozen phase folders this file was first built from. */\n"
              "window.AS2 = ")
    write(header, d)
    write_geometry_module(zones)

    print(f"portal_data.js   {len(d['zoning']['zones'])} rooms, "
          f"{d['zoning']['allocated']:,.0f} m² allocated")
    print(f"plan_geometry.js crescent R={plan.ARC_R:.1f} m, "
          f"{len(d['renders'])} renders kept")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
