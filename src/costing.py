"""Capital cost of the scheme, against the brief's AED 35 million budget.

WHY THIS EXISTS
---------------
The Scope of Work is explicit:

    "Participants are also required to consider the project's total
     implementation budget of AED 35 million and demonstrate the feasibility,
     scalability, and practicality of their proposals within this financial
     framework."

and "Feasibility and Implementation Potential" carries **20% of the jury's
score** — the same weight as the AI criterion and four times the weight of
presentation.

Until this module existed the project costed only the ground surfaces in
`data/raw/site_zoning_schedule.csv`: about AED 6.6 M, or 19% of the budget.
That is not a cheap scheme, it is an **incomplete estimate** — it omitted the
canopy, which is the single most expensive element and the whole idea of the
design. A juror checking feasibility would have found the headline element
missing from the cost plan.

WHAT IS MEASURED VS ASSUMED
---------------------------
* **Measured** — every area comes from the drawn geometry: zone areas are the
  shoelace areas in the zoning schedule, and the canopy area is the true arc
  length (2·R·asin(chord/2R)) times its 18 m width. Nothing here is eyeballed.
* **Published rates** — `data/raw/construction_unit_rates_aed.csv`.
* **Assumed** — the on-cost percentages (preliminaries, contingency, fees) and
  the services allowances. These are industry-normal ranges, flagged ASSUMED in
  the output, and named as assumptions in the report. They are not measurements
  and this module does not pretend otherwise.

    python -m src.costing
"""

from __future__ import annotations

import csv
import json
import math

from . import config as C
from . import viz

# ── Scope the zoning schedule does not cover ─────────────────────────────────
# The schedule prices ground surfaces. These are the things standing on, over
# or under that ground. Each carries its basis so a juror can challenge it.
SERVICES_ALLOWANCES = [
    # (item, unit, qty basis, rate, basis note, assumed?)
    ("Irrigation — subsurface drip, treated sewage effluent",
     "per_sqm_soft", None, 85,
     "Gulf landscape irrigation rates 2025, TSE-fed drip", True),
    ("Site lighting — pole, bollard and canopy-integrated LED",
     "per_sqm_site", None, 60,
     "Amenity lighting allowance across the whole site", True),
    ("Site furniture — benches, litter and recycling stations, bike racks",
     "per_sqm_site", None, 35,
     "Furniture and fittings allowance", True),
    ("Wayfinding and interpretation signage",
     "per_sqm_site", None, 12,
     "Signage allowance, bilingual", True),
    ("Stormwater, drainage and below-ground services",
     "per_sqm_site", None, 90,
     "Civils allowance for a 15,000 m2 public realm", True),
    ("Earthworks — Al Kathib dune berm shaping and topsoil",
     "per_sqm_berm", None, 120,
     "Cut/fill, import and shaping of the perimeter berm", True),
]

# Buildings the brief names in its minimum programme but that the zoning
# schedule prices only as ground: restrooms, drinking fountains, service store.
AMENITY_BUILDINGS = [
    ("Public restrooms — two blocks, universally accessible", 180, 6500,
     "Dubai light commercial build rate, sanitary fit-out", True),
    ("Drinking fountains — six, chilled and bottle-fill", 6, 12000,
     "Per unit supplied and installed", True),
    ("Service and maintenance store", 60, 4500,
     "Kiosk / built structure rate", True),
    ("Bicycle parking and drop-off shelter", 90, 3000,
     "Covered structure, lighter than enclosed build", True),
]

# On-costs, applied to the works total. Ranges are conventional for a Gulf
# public realm project at concept/preliminary stage.
PRELIMINARIES_PCT = 0.12   # site set-up, management, temporary works
CONTINGENCY_PCT = 0.10     # design development at this stage of information
FEES_PCT = 0.09            # design, supervision and authority approvals


def _tree_count() -> int:
    """Trees actually laid out, read from the generated planting layout."""
    path = C.DATA_PROCESSED / "planting_layout.csv"
    with path.open(encoding="utf-8") as fh:
        return sum(1 for _ in csv.DictReader(fh))


def _rates() -> dict[str, float]:
    out = {}
    with (C.DATA_RAW / "construction_unit_rates_aed.csv").open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            out[row["Element"]] = float(row["Rate_AED"])
    return out


def _zones() -> list[dict]:
    with (C.DATA_RAW / "site_zoning_schedule.csv").open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def arc_length_m() -> float:
    """True length of the crescent, from the chord and the radius.

    Straight-line chord is 138 m; the arc it subtends is longer, and pricing the
    canopy off the chord would under-measure it by about 6 m of structure.
    """
    chord = C.CRESCENT["chord_m"]
    r = chord ** 2 / (8 * C.CRESCENT["sagitta_m"]) + C.CRESCENT["sagitta_m"] / 2
    return 2 * r * math.asin(chord / (2 * r))


def build() -> dict:
    rates, zones = _rates(), _zones()
    site_area = C.SITE["area_sqm"]
    lines: list[dict] = []

    def add(group, item, qty, unit, rate, basis, assumed=False):
        lines.append(dict(group=group, item=item, qty=round(qty, 1), unit=unit,
                          rate=rate, total=qty * rate, basis=basis,
                          assumed=assumed))

    # 1 ── Ground surfaces, straight off the drawn polygons.
    for z in zones:
        area, rate = float(z["Area_sqm"]), float(z["Rate_AED_sqm"])
        add("Ground surfaces", z["Zone"], area, "m2", rate,
            "Zone area is the shoelace area of the drawn polygon; rate from "
            "construction_unit_rates_aed.csv")

    soft_area = sum(float(z["Area_sqm"]) for z in zones
                    if z["Category"] in ("Green", "Green_Buffer", "Passive"))
    berm_area = sum(float(z["Area_sqm"]) for z in zones
                    if z["Category"] == "Green_Buffer")

    # 2 ── The canopy. The element the old estimate left out entirely.
    arc = arc_length_m()
    canopy_area = arc * C.CRESCENT["canopy_width_m"]
    add("Al Hilal — the canopy",
        f"Gridshell canopy, {C.CRESCENT['canopy_width_m']:.0f} m wide over "
        f"{arc:.0f} m of arc",
        canopy_area, "m2", rates["ETFE canopy structure"],
        "Arc length computed from chord and sagitta, not the chord")

    louvre_area = arc * C.CRESCENT["south_louvre_depth_m"]
    add("Al Hilal — the canopy",
        f"Southern louvre screen, {C.CRESCENT['south_louvre_depth_m']:.0f} m deep",
        louvre_area, "m2", 1800,
        "Vertical fin screen; lighter than the primary gridshell", True)

    # 3 ── Planting and water.
    add("Planting and water", "Canopy trees supplied and planted",
        _tree_count(), "no.",
        rates["Canopy tree supply and planting"],
        "Tree count from the generated planting layout")

    falaj_area = next((float(z["Area_sqm"]) for z in zones
                       if z["Category"] == "Water"), 0.0)
    add("Planting and water",
        "Al Falaj — lined channel, recirculation and filtration",
        falaj_area, "m2", 3000,
        "Recirculating water feature, supply and install", True)

    # 4 ── Services and allowances.
    basis_area = {"per_sqm_soft": soft_area, "per_sqm_site": site_area,
                  "per_sqm_berm": berm_area}
    for item, unit, _, rate, basis, assumed in SERVICES_ALLOWANCES:
        add("Services and allowances", item, basis_area[unit], "m2", rate,
            basis, assumed)

    # 5 ── Amenity buildings the brief requires by name.
    for item, qty, rate, basis, assumed in AMENITY_BUILDINGS:
        unit = "no." if "fountain" in item.lower() else "m2"
        add("Amenity buildings", item, qty, unit, rate, basis, assumed)

    works = sum(line["total"] for line in lines)
    prelims = works * PRELIMINARIES_PCT
    conting = (works + prelims) * CONTINGENCY_PCT
    fees = (works + prelims + conting) * FEES_PCT
    total = works + prelims + conting + fees

    budget = C.SITE["budget_aed"]
    summary = dict(
        works_aed=works, preliminaries_aed=prelims, contingency_aed=conting,
        fees_aed=fees, total_aed=total, budget_aed=budget,
        headroom_aed=budget - total, utilisation_pct=100 * total / budget,
        cost_per_sqm=total / site_area, arc_length_m=arc,
        canopy_area_sqm=canopy_area,
        preliminaries_pct=PRELIMINARIES_PCT, contingency_pct=CONTINGENCY_PCT,
        fees_pct=FEES_PCT,
    )
    return dict(lines=lines, summary=summary)


def write_outputs(model: dict) -> None:
    lines, s = model["lines"], model["summary"]

    out_csv = C.DATA_PROCESSED / "cost_plan.csv"
    with out_csv.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["Group", "Item", "Quantity", "Unit", "Rate_AED",
                    "Total_AED", "Assumed", "Basis"])
        for ln in lines:
            w.writerow([ln["group"], ln["item"], ln["qty"], ln["unit"],
                        ln["rate"], round(ln["total"], 2),
                        "ASSUMED" if ln["assumed"] else "RATED", ln["basis"]])
        for label, key in [("Preliminaries", "preliminaries_aed"),
                           ("Contingency", "contingency_aed"),
                           ("Design and supervision fees", "fees_aed"),
                           ("TOTAL", "total_aed")]:
            w.writerow(["On-costs and total", label, "", "", "",
                        round(s[key], 2), "ASSUMED", "Percentage on-cost"])

    (C.MODELS / "cost_summary.json").write_text(
        json.dumps(s, indent=2), encoding="utf-8")


def figure(model: dict):
    """One chart: where the money goes, and how much budget is left."""
    viz.apply_style()
    lines, s = model["lines"], model["summary"]
    groups: dict[str, float] = {}
    for ln in lines:
        groups[ln["group"]] = groups.get(ln["group"], 0.0) + ln["total"]
    groups["Preliminaries"] = s["preliminaries_aed"]
    groups["Contingency"] = s["contingency_aed"]
    groups["Design and supervision fees"] = s["fees_aed"]

    order = sorted(groups.items(), key=lambda kv: -kv[1])
    labels = [k for k, _ in order]
    vals = [v / 1e6 for _, v in order]

    fig, axes = viz.open_figure(
        "The scheme costs AED "
        f"{s['total_aed'] / 1e6:.1f} M of the AED "
        f"{s['budget_aed'] / 1e6:.0f} M budget",
        f"Capital cost plan — {s['utilisation_pct']:.0f}% of the budget, "
        f"AED {s['headroom_aed'] / 1e6:.1f} M of headroom",
        width=11.5, height=8.6, nrows=2,
        gridspec_kw=dict(height_ratios=[3, 1], hspace=0.42))
    ax, ax2 = axes

    colors = (C.SERIES * 4)[:len(labels)]
    ax.barh(labels[::-1], vals[::-1], color=colors[::-1], height=0.62)
    for i, v in enumerate(vals[::-1]):
        ax.text(v + max(vals) * 0.015, i, f"{v:.2f} M",
                va="center", fontsize=9, color=C.PALETTE["ink_secondary"])
    ax.set_xlabel("AED, millions")
    ax.set_xlim(0, max(vals) * 1.18)

    total_m, budget_m = s["total_aed"] / 1e6, s["budget_aed"] / 1e6
    ax2.barh([""], [budget_m], color=C.PALETTE["rule"], height=0.5)
    ax2.barh([""], [total_m], color=C.STATUS["good"], height=0.5)
    ax2.axvline(budget_m, color=C.STATUS["critical"], lw=1.4, ls="--")
    ax2.text(budget_m, 0.30, f"  budget {budget_m:.0f} M",
             color=C.STATUS["critical"], fontsize=9, va="bottom")
    ax2.text(total_m / 2, 0, f"estimate {total_m:.1f} M "
             f"({s['utilisation_pct']:.0f}%)",
             ha="center", va="center", fontsize=9.5, color="white",
             fontweight="semibold")
    ax2.set_xlim(0, budget_m * 1.12)
    ax2.set_yticks([])
    ax2.set_xlabel("AED, millions")

    n_assumed = sum(1 for ln in lines if ln["assumed"])
    return viz.finish(
        fig, "fig11_cost_plan",
        source="src/costing.py — quantities from the drawn geometry, rates from "
               "data/raw/construction_unit_rates_aed.csv",
        note=f"Quantities are measured, not estimated: zone areas are the shoelace "
             f"areas of the drawn polygons, and the canopy is "
             f"{s['arc_length_m']:.0f} m of true arc x "
             f"{C.CRESCENT['canopy_width_m']:.0f} m — not the "
             f"{C.CRESCENT['chord_m']:.0f} m chord, which would under-measure it.\n"
             f"{n_assumed} allowance lines and the three on-cost percentages "
             f"(preliminaries {s['preliminaries_pct']:.0%}, contingency "
             f"{s['contingency_pct']:.0%}, fees {s['fees_pct']:.0%}) are ASSUMED, "
             f"and flagged as such in data/processed/cost_plan.csv.\n"
             f"AED {s['cost_per_sqm']:,.0f}/m2 across the 15,000 m2 site.")


def main() -> int:
    model = build()
    write_outputs(model)
    path = figure(model)
    s = model["summary"]
    print(f"  arc length            {s['arc_length_m']:.1f} m "
          f"(chord is {C.CRESCENT['chord_m']:.0f} m)")
    print(f"  canopy area           {s['canopy_area_sqm']:,.0f} m2")
    print(f"  works                 AED {s['works_aed']:,.0f}")
    print(f"  + prelims/cont/fees   AED "
          f"{s['preliminaries_aed'] + s['contingency_aed'] + s['fees_aed']:,.0f}")
    print(f"  TOTAL                 AED {s['total_aed']:,.0f}")
    print(f"  budget                AED {s['budget_aed']:,.0f}")
    print(f"  utilisation           {s['utilisation_pct']:.1f}%  "
          f"(headroom AED {s['headroom_aed']:,.0f})")
    print(f"  {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
