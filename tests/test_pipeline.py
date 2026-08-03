"""
Correctness checks for the analysis pipeline.

These are the assertions that stop the project quietly drifting into being
wrong. They are cheap to run and they run on every rebuild:

    python -m tests.test_pipeline

The most important one is `test_downscaling_reproduces_normals`. The hourly
climate series is modelled, not measured, so the one thing it must do is
reproduce the published monthly normals it was built from. If that check fails,
every comfort figure in the submission is wrong.
"""

from __future__ import annotations

import sys
import re

import numpy as np
import pandas as pd

from src import climate, config as C, dataset, solar

PASS, FAIL = "PASS", "FAIL"
_results: list[tuple[str, str, str]] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    _results.append((PASS if condition else FAIL, name, detail))


def test_solar_positions():
    sol = solar.hourly_solar_position()
    check("solar model returns 8,760 hourly rows",
          len(sol) == 8760, f"got {len(sol)}")

    # Dubai is at 25.19N, so the sun is never at the zenith and the highest it
    # reaches is about 88.3 degrees at the summer solstice.
    peak = sol["elevation_deg"].max()
    check("peak solar elevation is 87-89 degrees",
          87.0 <= peak <= 89.0, f"{peak:.2f} deg")

    jun = sol[(sol.index.month == 6) & sol["is_daylight"]]
    dec = sol[(sol.index.month == 12) & sol["is_daylight"]]
    check("June has more daylight hours than December",
          len(jun) / 30 > len(dec) / 31,
          f"{len(jun)/30:.2f} vs {len(dec)/31:.2f} h/day")

    daylight = int(sol["is_daylight"].sum())
    check("annual daylight hours are plausible (4,300-4,500)",
          4300 <= daylight <= 4500, f"{daylight} h")
    return sol


def test_downscaling_reproduces_normals(sol):
    normals = pd.read_csv(C.DATA_RAW / "dubai_climate_normals_ncm.csv")
    met = climate.downscale_to_hourly(normals, sol)

    check("hourly climate series has 8,760 rows",
          len(met) == 8760, f"got {len(met)}")

    cmp = climate.verify_downscaling(met, normals)
    worst_mean = cmp["err_mean_c"].abs().max()
    worst_max = cmp["err_max_c"].abs().max()
    worst_min = cmp["err_min_c"].abs().max()

    # NCM's TempMax_C is the MEAN DAILY MAXIMUM for the month, so the modelled
    # mean of daily maxima is what must match it. All three are held to 1 C.
    check("modelled monthly mean temperature within 1.0 C of the NCM normal",
          worst_mean <= 1.0, f"worst {worst_mean:.2f} C")
    check("modelled mean daily maximum within 1.0 C of the NCM normal",
          worst_max <= 1.0, f"worst {worst_max:.2f} C")
    check("modelled mean daily minimum within 1.0 C of the NCM normal",
          worst_min <= 1.0, f"worst {worst_min:.2f} C")

    check("no missing values in the hourly climate series",
          not met.isna().any().any(),
          f"{int(met.isna().sum().sum())} nulls")
    check("relative humidity stays within 0-100%",
          met["rh_pct"].between(0, 100).all(),
          f"range {met['rh_pct'].min():.1f}-{met['rh_pct'].max():.1f}")
    check("no irradiance at night",
          float(met.loc[~sol["is_daylight"], "ghi_wh_m2"].abs().max()) < 1e-6)
    return met


def test_heat_index():
    # Published NWS reference points, in Fahrenheit converted to Celsius.
    # 90 F / 70% RH -> about 105 F.  100 F / 40% RH -> about 109 F.
    hi1 = climate.heat_index_c((90 - 32) * 5 / 9, 70)
    hi2 = climate.heat_index_c((100 - 32) * 5 / 9, 40)
    f1 = float(hi1) * 9 / 5 + 32
    f2 = float(hi2) * 9 / 5 + 32
    check("heat index matches the NWS table at 90F/70%RH (105F +/-2)",
          abs(f1 - 105) <= 2.0, f"got {f1:.1f} F")
    check("heat index matches the NWS table at 100F/40%RH (109F +/-2)",
          abs(f2 - 109) <= 2.0, f"got {f2:.1f} F")

    # Shade must never make the modelled condition worse.
    t = np.array([42.0, 38.0, 30.0])
    rh = np.array([53.0, 55.0, 60.0])
    t_s, rh_s = climate.apply_shade(t, rh)
    check("shading lowers the heat index at every tested condition",
          bool((climate.heat_index_c(t_s, rh_s) < climate.heat_index_c(t, rh)).all()))
    check("shading raises relative humidity (cooler air, same moisture)",
          bool((rh_s > rh).all()), f"{rh} -> {rh_s.round(1)}")


def test_shade_model(sol):
    frac = solar.crescent_shade_fraction(sol)
    lit = frac.dropna()
    check("shade fraction is bounded 0-1",
          bool(lit.between(0, 1).all()),
          f"range {lit.min():.3f}-{lit.max():.3f}")

    summary = solar.annual_shade_summary(frac)
    check("annual shade coverage is between 50% and 100%",
          50 <= summary["annual_shade_pct"] <= 100,
          f"{summary['annual_shade_pct']}%")

    # Physical sanity: a 6 m tree at 88 deg elevation casts a very short shadow.
    s = float(solar.shadow_length(6.0, 88.2))
    check("6 m tree at 88.2 deg casts a 0.1-0.4 m shadow", 0.1 <= s <= 0.4, f"{s:.2f} m")

    # ...and a long one at 20 degrees.
    s20 = float(solar.shadow_length(6.0, 20.0))
    check("6 m tree at 20 deg casts a 15-18 m shadow", 15 <= s20 <= 18, f"{s20:.2f} m")


def test_site_geometry():
    zones = pd.read_csv(C.DATA_RAW / "site_zoning_schedule.csv")
    total = zones["Area_sqm"].sum()
    check("zoning schedule sums to the 15,000 sqm site area",
          abs(total - C.SITE["area_sqm"]) < 1.0,
          f"{total:,.0f} vs {C.SITE['area_sqm']:,.0f} sqm")

    trees = solar.tree_positions()
    species = pd.read_csv(C.DATA_RAW / "species_water_carbon_rates.csv")
    check("planting layout is within 2 trees of the Phase 6 schedule",
          abs(len(trees) - int(species["Count"].sum())) <= 2,
          f"{len(trees)} laid out vs {int(species['Count'].sum())} scheduled")
    check("every tree sits inside the site boundary",
          bool((trees["x"].between(0, C.SITE["length_m"])).all()
               and (trees["y"].between(0, C.SITE["width_m"])).all()))


def test_plan_geometry():
    """The masterplan must be internally consistent before anything reads it.

    Rooms are laid out as boxes in the crescent's polar frame and then clipped
    to the site. That construction makes overlap impossible in principle, but
    only if the boxes really are disjoint — so this samples the plan and checks
    that no square metre of ground is claimed twice.
    """
    from matplotlib.path import Path as MplPath

    from src import plan

    zones = plan.build()
    rooms = [z for z in zones if not z.get("is_residual")]

    check("the arc closes on its own chord and sagitta",
          abs(plan.arc_point(plan.ARC_THETA)[0] - (C.SITE["length_m"] / 2
              + C.CRESCENT["chord_m"] / 2)) < 1e-6
          and abs(plan.arc_point(0.0)[1]
                  - (C.CRESCENT["y_ends_m"] - C.CRESCENT["sagitta_m"])) < 1e-6,
          f"R = {plan.ARC_R:.2f} m")

    claimed = sum(z["area"] for z in rooms)
    residual = next(z for z in zones if z.get("is_residual"))
    check("rooms plus the alley residual equal the site area",
          abs(claimed + residual["area"] - C.SITE["area_sqm"]) < 1.0,
          f"{claimed:,.0f} + {residual['area']:,.0f} m²")
    check("the alley residual is positive and plausible (5-20% of site)",
          0.05 <= residual["area"] / C.SITE["area_sqm"] <= 0.20,
          f"{residual['area'] / C.SITE['area_sqm'] * 100:.1f}%")

    # No square metre may belong to two rooms. Sampled on the same 1 m grid the
    # spatial dataset uses, so this is exactly the assignment that gets modelled
    # — but nudged off the half-metre lattice first. Adjacent rooms are supposed
    # to share an edge, and a sample point sitting exactly on one is reported as
    # inside by both polygons. Without the nudge this test fails on the berm and
    # the running loop meeting at y = 3.5, which is not a fault, it is a kerb.
    pts = solar.site_grid(1.0)[["x", "y"]].to_numpy() + np.array([0.137, 0.241])
    hits = np.zeros(len(pts), dtype=int)
    for z in rooms:
        h = np.zeros(len(pts), dtype=bool)
        for part in z["parts"]:
            if len(part) >= 3:
                h |= MplPath(part).contains_points(pts)
        hits += h.astype(int)
    check("no ground is claimed by two rooms at once",
          int(hits.max()) <= 1, f"worst cell claimed {int(hits.max())} times")

    # And the drawn area must match the ground each room actually takes.
    worst, worst_name = 0.0, ""
    for z in rooms:
        h = np.zeros(len(pts), dtype=bool)
        for part in z["parts"]:
            if len(part) >= 3:
                h |= MplPath(part).contains_points(pts)
        err = abs(int(h.sum()) - z["area"]) / z["area"] * 100
        if err > worst:
            worst, worst_name = err, z["name"]
    check("each room's drawn area matches the ground it claims within 6%",
          worst <= 6.0, f"worst {worst_name} off by {worst:.1f}%")


def test_spatial_zone_assignment():
    """Every designed room must actually claim ground on the modelled grid.

    Regression guard. The alley network is the residual zone and covers the
    whole inner field; treating it like any other room would overwrite every
    specific room and leave the entire grid labelled "Al Sikkak" with a constant
    albedo — which silently reduces the zone analysis to a single bar and turns
    albedo into a dead feature.
    """
    from src import dataset

    # 1 m cells. A coarser grid cannot resolve the 7 m walk, and the area check
    # would report a discretisation artefact as a geometry fault. Few sampled
    # hours keeps it cheap; this test is about geometry, not shade.
    grid, _ = dataset.build_spatial(step_m=1.0, sample_hours=4, verbose=False)
    zones = pd.read_csv(C.DATA_RAW / "site_zoning_schedule.csv")

    n_zones = grid["zone"].nunique()
    check("more than one zone is represented on the grid",
          n_zones > 1, f"{n_zones} distinct zones")

    n_cat = grid["category"].nunique()
    check("more than one zone category is represented",
          n_cat > 1, f"{n_cat} categories")

    check("surface albedo varies across the site",
          grid["albedo"].nunique() > 1,
          f"{grid['albedo'].nunique()} distinct values")

    missing = [z for z in zones["Zone"] if z not in set(grid["zone"])]
    check("every scheduled zone appears on the grid",
          not missing, f"missing: {missing[:3]}")

    # The proof the rooms do not overlap: the ground each claims on the grid
    # must match the area the schedule gives it. An overlap shows up here as one
    # room eating another's area. The falaj is excluded — it is 0.9 m wide, so a
    # 1 m grid cannot resolve it and the error is discretisation, not geometry.
    got = grid["zone"].value_counts() * 1.0  # 1 m cells -> 1 m2 each
    want = zones.set_index("Zone")["Area_sqm"]
    err = ((got - want) / want * 100).abs().dropna()
    err = err[~err.index.str.contains("Falaj")]
    worst = err.max()
    check("each zone's ground area matches the schedule within 6%",
          worst <= 6.0,
          f"worst {err.idxmax()} off by {worst:.1f}%")


def test_no_leaky_features():
    """The classifier must not be able to see the answer."""
    from src.models import CLASSIFIER_FEATURES

    banned = {"temp_c", "rh_pct", "heat_index_c", "heat_index_shaded_c",
              "comfort_band", "comfort_gain_c", "temp_shaded_c"}
    leaked = banned.intersection(CLASSIFIER_FEATURES)
    check("comfort classifier features contain no leakage",
          not leaked, f"leaked: {sorted(leaked)}")


def test_cost_plan():
    """The cost plan must close inside the brief's budget, and measure the arc.

    The failure this guards against already happened once: the estimate priced
    only the ground surfaces and came to 19% of budget, because the canopy — the
    most expensive element and the entire idea of the scheme — was missing from
    it. A feasibility case with a hole that size is worse than none.
    """
    from src import costing

    model = costing.build()
    s = model["summary"]

    check("capital cost falls inside the AED 35 M budget",
          s["total_aed"] <= s["budget_aed"],
          f"AED {s['total_aed']:,.0f} of {s['budget_aed']:,.0f} "
          f"({s['utilisation_pct']:.1f}%)")

    # A scheme costing a fraction of its budget is not thrift, it is an
    # incomplete estimate — which is exactly the defect this module fixed.
    check("capital cost uses a credible share of the budget (>50%)",
          s["utilisation_pct"] > 50, f"{s['utilisation_pct']:.1f}%")

    chord = C.CRESCENT["chord_m"]
    check("canopy is priced on the arc, not the chord",
          s["arc_length_m"] > chord,
          f"arc {s['arc_length_m']:.1f} m vs chord {chord:.0f} m")

    canopy = sum(ln["total"] for ln in model["lines"]
                 if ln["group"].startswith("Al Hilal"))
    check("the canopy appears in the cost plan at all",
          canopy > 0, f"AED {canopy:,.0f}")

    every_line_has_basis = all(ln["basis"].strip() for ln in model["lines"])
    check("every cost line states its basis",
          every_line_has_basis, f"{len(model['lines'])} lines")


def test_published_site() -> None:
    """The portal must survive GitHub Pages.

    Pages runs the published folder through Jekyll, and Jekyll silently skips
    every path beginning with an underscore. The portal's stylesheet, scripts
    and data all live in docs/_PORTAL/, so without a .nojekyll marker the site
    serves index.html with no CSS and no JavaScript — a 200, not a 404, which
    is why it looked fine from here and broken in a browser. It happened once.
    """
    docs = C.ROOT / "docs"
    check("docs/.nojekyll exists so GitHub Pages skips Jekyll",
          (docs / ".nojekyll").exists(),
          "underscore folders are dropped without it")

    underscored = [p.name for p in docs.iterdir()
                   if p.is_dir() and p.name.startswith("_")]
    check("underscore asset folders are accounted for",
          not underscored or (docs / ".nojekyll").exists(),
          f"{underscored or 'none'}")

    index = docs / "index.html"
    if index.exists():
        html = index.read_text(encoding="utf-8", errors="replace")
        # Local file references only: skip absolute URLs, protocol-relative
        # ones, in-page anchors and data/mailto URIs.
        refs = re.findall(
            r'(?:href|src)="((?!https?:|//|#|data:|mailto:)[^"]+)"', html)
        missing = [r for r in refs
                   if not (docs / r.split("?")[0].split("#")[0]).exists()]
        check("every local asset index.html references exists",
              not missing, f"missing: {missing[:3] or 'none'}")


def test_film_narration() -> None:
    """The film's voice-over must be inlined, not merely sitting beside it.

    Opened as a local file — which is how it gets used — a browser will not
    load a sibling audio file at all, and Web Audio cannot tap a media element
    it treats as cross-origin, so a `narration/` folder next to the HTML gives
    a silent film AND a silent recording. The audio is embedded as data: URIs
    by tools/embed_narration.py; this asserts it is still there, because the
    failure is silent in the most literal sense.
    """
    film = (C.ROOT / "submission" / "12_Concept_Animation_Video" /
            "concept_film.html")
    html = film.read_text(encoding="utf-8", errors="replace")

    clips = html.count("data:audio/wav;base64,")
    check("the film carries its narration inline", clips == 4,
          f"{clips} embedded clip(s), expected 4")

    # A data: URI that got truncated would still match the count above.
    shortest = min((len(m) for m in
                    re.findall(r'"data:audio/wav;base64,([^"]*)"', html)),
                   default=0)
    check("each embedded clip holds real audio", shortest > 200_000,
          f"smallest clip {shortest/1024:.0f} KB of base64")

    check("narration is never fetched from a sibling file",
          'new Audio("narration/' not in html,
          "a file:// browser refuses those, silently")


def main() -> int:
    sol = test_solar_positions()
    test_downscaling_reproduces_normals(sol)
    test_heat_index()
    test_shade_model(sol)
    test_site_geometry()
    test_plan_geometry()
    test_spatial_zone_assignment()
    test_no_leaky_features()
    test_cost_plan()
    test_published_site()
    test_film_narration()

    width = max(len(n) for _, n, _ in _results) + 2
    print("\n" + "=" * (width + 34))
    print("  AL SAFA 2 PARK — PIPELINE CHECKS")
    print("=" * (width + 34))
    for status, name, detail in _results:
        mark = "[ok]  " if status == PASS else "[FAIL]"
        print(f"  {mark} {name:<{width}} {detail}")

    failed = sum(1 for s, _, _ in _results if s == FAIL)
    print("-" * (width + 34))
    print(f"  {len(_results) - failed} passed, {failed} failed")
    print("=" * (width + 34))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
