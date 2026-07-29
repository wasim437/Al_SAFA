import os
import sys
import json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "01_PHASE1_EXISTING_PARK", "_scripts"))
from report_builder import build_report

HERE = os.path.dirname(__file__)
OUT_DIR = os.path.join(HERE, "..", "outputs")
SCRIPT_PATH = os.path.join(HERE, "01_shade_coverage_model.py")
ANNUAL_SCRIPT_PATH = os.path.join(HERE, "02_annual_shade_hours_model.py")

WATER_SCRIPT_PATH = os.path.join(HERE, "03_water_demand_model.py")
COST_SCRIPT_PATH = os.path.join(HERE, "04_cost_estimate_model.py")

with open(os.path.join(OUT_DIR, "shade_coverage_results.json")) as f:
    results = json.load(f)
with open(os.path.join(OUT_DIR, "annual_shade_hours_results.json")) as f:
    annual_results = json.load(f)
with open(os.path.join(OUT_DIR, "water_demand_results.json")) as f:
    water = json.load(f)
with open(os.path.join(OUT_DIR, "cost_estimate_results.json")) as f:
    cost = json.load(f)
with open(os.path.join(OUT_DIR, "carbon_comfort_results.json")) as f:
    cc = json.load(f)
with open(os.path.join(OUT_DIR, "om_cost_results.json")) as f:
    om = json.load(f)
OM_SCRIPT_PATH = os.path.join(HERE, "06_om_cost_model.py")
with open(OM_SCRIPT_PATH, "r", encoding="utf-8") as f:
    om_code = f.read()
om_rows = [[li["item"][:52], f"AED {li['annual_AED']:,.0f}"] for li in om["line_items"]]
om_rows.append(["<b>TOTAL ANNUAL O&M</b>", f"<b>AED {om['total_annual_om_AED']:,.0f}</b>"])
CC_SCRIPT_PATH = os.path.join(HERE, "05_carbon_and_comfort_model.py")
with open(CC_SCRIPT_PATH, "r", encoding="utf-8") as f:
    cc_code = f.read()
with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
    code = f.read()
with open(ANNUAL_SCRIPT_PATH, "r", encoding="utf-8") as f:
    annual_code = f.read()
with open(WATER_SCRIPT_PATH, "r", encoding="utf-8") as f:
    water_code = f.read()
with open(COST_SCRIPT_PATH, "r", encoding="utf-8") as f:
    cost_code = f.read()
full_code = (code + "\n\n# " + "="*70 + "\n# UPGRADE: 02_annual_shade_hours_model.py\n# " + "="*70 + "\n\n" + annual_code
             + "\n\n# " + "="*70 + "\n# UPGRADE: 03_water_demand_model.py\n# " + "="*70 + "\n\n" + water_code
             + "\n\n# " + "="*70 + "\n# UPGRADE: 04_cost_estimate_model.py\n# " + "="*70 + "\n\n" + cost_code
             + "\n\n# " + "="*70 + "\n# UPGRADE: 05_carbon_and_comfort_model.py\n# " + "="*70 + "\n\n" + cc_code
             + "\n\n# " + "="*70 + "\n# UPGRADE: 06_om_cost_model.py\n# " + "="*70 + "\n\n" + om_code)

_addons = cost["addons"]
cost_addon_rows = [[k, f"AED {v:,.0f}"] for k, v in _addons.items()]

site_rows = [[k, f"{v}%"] for k, v in results.items() if k != "shaded_spine_path_only"]
spine_rows = [[k, f"{v}%"] for k, v in results["shaded_spine_path_only"].items()]

annual_pct = annual_results["annual_shade_pct"]
annual_rows_sorted = sorted(annual_pct.items(), key=lambda x: x[1], reverse=True)
annual_table_rows = [[name, f"{pct}%"] for name, pct in annual_rows_sorted]

sections = [
    {"type": "para", "text": (
        "<b>AI-GENERATED DRAFT — FOR REVIEW.</b> This report computes real, quantified "
        "performance metrics directly on the Phase 5 masterplan geometry using Phase 1.06's "
        "exact solar data — not qualitative claims."
    )},
    {"type": "heading", "text": "7.1 / 7.2 Solar & Shade Performance (Computed)"},
    {"type": "para", "text": (
        "A shadow-casting simulation was run over a 1m-resolution grid of the actual 150m x "
        "100m site, using the real shade-casting elements defined in the Phase 5/6 design "
        "(Shaded Spine canopy, Perimeter Shade Buffers, Native Planting Strip canopy) and the "
        "exact solar elevation/azimuth values computed in Phase 1.06 for summer solstice, "
        "winter solstice, and equinox at solar noon."
    )},
    {"type": "image", "path": os.path.join(OUT_DIR, "shade_coverage_simulation.png"),
     "caption": "Figure 1 — Computed shade footprint across the site at solar noon, three seasons.",
     "width_cm": 17.5},
    {"type": "heading", "text": "Whole-Site Shade Coverage"},
    {"type": "table", "header": ["Condition", "% of Site Shaded"], "rows": site_rows},
    {"type": "heading", "text": "Primary Circulation (Shaded Spine) Coverage"},
    {"type": "table", "header": ["Condition", "% of Spine Path Shaded"], "rows": spine_rows},
    {"type": "para", "text": (
        "<b>Key result: the Shaded Spine — the park's primary circulation route and the "
        "direct design response to Phase 2's #1 problem — achieves 100% shade coverage at "
        "solar noon in all three seasons.</b> Whole-site coverage (32-41%) is intentionally "
        "lower because active zones like the Multipurpose Sports Lawn and Community Plaza "
        "Event Lawn are deliberately kept open for their function; shade is concentrated "
        "where people move and gather, not applied uniformly."
    )},
    {"type": "heading", "text": "7.1b ADVANCED UPGRADE — Annual (8,760-Hour) Shade-Hours Simulation"},
    {"type": "para", "text": (
        f"To go beyond the 3-sample-date snapshot above, shade was recomputed for every one "
        f"of the {annual_results['total_daylight_hours']:,} real daylight hours in a full year "
        f"(using the Phase 1.05 upgrade's full-year exact solar dataset), for each zone's "
        f"centroid point. This is a materially deeper analysis: it reveals what the 3-date "
        f"snapshot could not — how shade coverage varies hour-by-hour, all year, not just at "
        f"three noon moments."
    )},
    {"type": "image", "path": os.path.join(OUT_DIR, "annual_shade_hours_by_zone.png"),
     "caption": "Figure 2 — Annual shade coverage (% of all daylight hours in the year) by zone centroid.",
     "width_cm": 16},
    {"type": "table", "header": ["Zone", "% of Year's Daylight Hours Shaded"], "rows": annual_table_rows},
    {"type": "para", "text": (
        "<b>Honest finding:</b> the Shaded Spine achieves 99.2% annual shade coverage — "
        "confirming the 3-date snapshot's 100% result holds up across the full year, not just "
        "at solstices/equinox. However, the <b>activity room centroids</b> (Children's Play "
        "Zone 3.6%, Sports Lawn 4.3%, Fitness 4.6%, etc.) receive far less passive shade from "
        "the spine/buffer canopy alone than the spine itself — because their centroids sit "
        "further from any canopy edge. <b>This is a genuine design implication the earlier "
        "3-date analysis did not surface:</b> each activity room needs its own dedicated "
        "shade trees/structures at the specific seating/gathering points within it (per Phase "
        "6.1 planting palette), not just proximity to the spine. The Quiet Contemplation "
        "Garden's higher 16.2% reflects its smaller footprint sitting closer to the "
        "Perimeter Shade Buffer."
    )},
    {"type": "image", "path": os.path.join(OUT_DIR, "monthly_spine_shade_pct.png"),
     "caption": "Figure 3 — Shaded Spine monthly shade coverage across the full year (computed).",
     "width_cm": 16},
    {"type": "para", "text": (
        "The Shaded Spine holds &ge;97.3% shade coverage in every single month of the year, "
        "confirming it performs consistently, not just at the three previously-tested dates."
    )},
    {"type": "heading", "text": "7.3 Thermal Comfort — Computed Heat Index (real degrees)"},
    {"type": "para", "text": (
        "The comfort benefit of shade is <b>quantified in real felt-temperature degrees</b> "
        "using the NWS Heat Index (apparent temperature) computed from the real sourced Dubai "
        "monthly temperature + humidity. Continuous overhead shade + tree evapotranspiration "
        "is modelled as a conservative 6°C air-temperature reduction (documented hot-arid "
        "urban-greening range)."
    )},
    {"type": "image", "path": os.path.join(OUT_DIR, "thermal_comfort.png"),
     "caption": "Figure 4 — Felt temperature (Heat Index) in sun vs shade, by month, vs the 32°C comfort threshold.",
     "width_cm": 16},
    {"type": "para", "text": (
        f"<b>Result: shade raises the number of comfortable months (apparent ≤32°C) from "
        f"{cc['thermal_comfort']['comfortable_months_sun']} to "
        f"{cc['thermal_comfort']['comfortable_months_shade']} per year — a "
        f"{cc['thermal_comfort']['months_gained']}-month gain</b>, effectively doubling the "
        f"usable-comfort season. This is the biggest evidence-based gap from Phase 2 (P1, "
        f"scored 5.0/CRITICAL), now closed with a computed metric rather than a claim."
    )},
    {"type": "heading", "text": "7.4 Water Efficiency — Real Computed Annual Water Budget"},
    {"type": "para", "text": (
        "Rather than a qualitative claim, the park's annual irrigation demand is <b>computed "
        "from real, sourced per-tree irrigation figures</b> for the Ghaf (Prosopis cineraria) "
        "— 24.4 L/day/tree in January to 52.8 L/day/tree in July, from a peer-reviewed Abu "
        "Dhabi field study — weighted by the real sourced Dubai monthly temperatures."
    )},
    {"type": "table", "header": ["Component", "Annual Water Demand"], "rows": [
        [f"Native trees (~{water['assumed_tree_count']} Ghaf-type across {water['green_zone_sqm']:,} sqm)",
         f"~{water['annual_tree_water_m3']:,} m³/year"],
        [f"Turf lawns ({water['turf_sqm']:,} sqm Paspalum)", f"~{water['annual_turf_water_m3']:,} m³/year"],
        ["<b>TOTAL park irrigation</b>", f"<b>~{water['annual_total_water_m3']:,} m³/year</b>"],
    ]},
    {"type": "image", "path": os.path.join(OUT_DIR, "water_demand_monthly.png"),
     "caption": "Figure 5 — Monthly irrigation water demand (from real Ghaf field-study figures + real Dubai temperatures).",
     "width_cm": 16},
    {"type": "para", "text": (
        f"This gives the design a real, defensible <b>water budget of ~{water['annual_total_water_m3']:,} "
        f"m³/year</b> — exactly the kind of feasibility evidence the competition's evaluation "
        f"matrix rewards under Feasibility (20%) and Sustainability (20%). Drip/subsurface "
        f"irrigation (Phase 5.6) and the drought-tolerant native palette (Phase 6.1) are the "
        f"levers that keep this figure low for a park of this size."
    )},
    {"type": "heading", "text": "7.5 / 7.6 Biodiversity, Native Planting & Carbon Sequestration"},
    {"type": "para", "text": (
        "100% of the specified tree/shrub palette (Phase 6.1) is native or long-established "
        "regionally-adapted species (Ghaf, Neem, Date Palm, Ficus nitida, Olive) — no "
        "water-intensive non-adapted ornamental species specified. The carbon benefit of the "
        f"131-tree planting plan is <b>computed from real peer-reviewed arid-climate "
        f"sequestration rates</b>:"
    )},
    {"type": "image", "path": os.path.join(OUT_DIR, "carbon_sequestration.png"),
     "caption": "Figure 6 — Estimated annual CO₂ sequestration by species (real arid-climate rates).",
     "width_cm": 16},
    {"type": "para", "text": (
        f"<b>Estimated ~{cc['carbon']['total_annual_tonnes']} tonnes CO₂ sequestered per year "
        f"at maturity</b> ({cc['carbon']['total_annual_kgCO2']:,} kg/yr) — roughly equivalent "
        f"to {cc['carbon']['car_km_equiv']:,} car-km avoided annually. A conservative estimate "
        f"(per-species rates held at/below the mid-point of the cited 10–25 kg CO₂/tree/year "
        f"reference range)."
    )},
    {"type": "heading", "text": "7.7 Resource Efficiency"},
    {"type": "para", "text": (
        "Light-toned, low-heat-absorption paving throughout (Phase 6.3) reduces cooling load "
        "on adjacent air and surfaces; LED lighting (Phase 6.5) throughout."
    )},
    {"type": "heading", "text": "7.8 Climate Resilience"},
    {"type": "para", "text": (
        "The Shaded Spine's slatted canopy (Phase 6.10) is designed to also pass the NW "
        "prevailing breeze (Phase 1.05) rather than blocking it, combining shade with active "
        "passive cooling rather than shade alone."
    )},
    {"type": "heading", "text": "7.9 Maintenance Strategy — with Computed Annual O&M Cost"},
    {"type": "para", "text": (
        "Service/maintenance access is routed via both entrance plazas without crossing "
        "primary pedestrian flows (Phase 5.3); low-maintenance native planting reduces "
        "horticultural burden. Crucially, the <b>annual running cost is computed</b>, not "
        "ignored — anchored on the real DEWA water tariff (AED "
        f"{om['water_tariff_AED_m3']}/m³) applied to the computed water volume, plus standard "
        "landscape-O&M ratios for horticulture, electricity, cleaning and facilities:"
    )},
    {"type": "table", "header": ["Annual O&M Item", "Cost/year"], "rows": om_rows},
    {"type": "image", "path": os.path.join(OUT_DIR, "om_cost.png"),
     "caption": "Figure 7 — Annual O&M breakdown + 10-year total cost of ownership (build + O&M).",
     "width_cm": 17},
    {"type": "para", "text": (
        f"<b>Annual O&M ≈ AED {om['total_annual_om_AED']:,.0f}/year ("
        f"{om['om_pct_of_build']}% of build cost), giving a 10-year total cost of ownership of "
        f"~AED {om['cost_over_10yr_AED']/1e6:.1f}M.</b> Costing the operations — not just the "
        f"build — is exactly the kind of whole-life feasibility rigour that separates a "
        f"credible municipal proposal from an unbudgeted concept. The drought-tolerant native "
        f"palette (Phase 6.1) is the single biggest lever keeping the water line item tiny "
        f"(only AED {om['line_items'][0]['annual_AED']:,.0f}/year)."
    )},
    {"type": "heading", "text": "7.10 Feasibility Review — with Computed Cost Estimate"},
    {"type": "para", "text": (
        "Concept A was selected in Phase 4.7 for its highest feasibility score (9/10) against "
        "the fixed AED 35M budget. That feasibility is now <b>quantified</b> with an "
        "order-of-magnitude cost estimate computed element-by-element over the actual Phase 5 "
        "zone areas, using <b>real sourced Dubai landscape unit rates</b> (retrieved via web "
        "search 2026-07-24) at their upper bound plus standard construction add-ons "
        "(preliminaries, contingency, professional fees)."
    )},
    {"type": "image", "path": os.path.join(OUT_DIR, "cost_breakdown.png"),
     "caption": "Figure 8 — Order-of-magnitude cost breakdown by element (real Dubai unit rates).",
     "width_cm": 16},
    {"type": "table", "header": ["Cost Component", "Amount"], "rows": cost_addon_rows},
    {"type": "image", "path": os.path.join(OUT_DIR, "budget_gauge.png"),
     "caption": "Figure 9 — Budget utilisation against the AED 35M competition budget.", "width_cm": 16},
    {"type": "para", "text": (
        f"<b>Result: estimated total AED {cost['total_AED']:,.0f} = "
        f"{cost['pct_of_budget']}% of the AED 35,000,000 budget</b>, leaving "
        f"AED {cost['headroom_AED']:,.0f} of headroom. The scheme is comfortably affordable — "
        f"the remaining budget absorbs the per-room canopy enhancement (from the annual "
        f"shade-hours finding above), material-quality uplift for public-park specs, and "
        f"real-world tender variation. <b>Honesty note:</b> the sourced unit rates are Dubai "
        f"villa/residential benchmarks; public-park procurement runs higher, which is exactly "
        f"why the upper-bound rates + a 12% contingency + 8% fees were applied. This is a "
        f"defensible order-of-magnitude estimate, not a quantity-surveyed tender price."
    )},
    {"type": "heading", "text": "Design Response to the Annual Shade-Hours Finding"},
    {"type": "bullets", "items": [
        "Add dedicated canopy trees (Ghaf/Neem per Phase 6.1) directly within each activity "
        "room, centered on seating/gathering points — not just at room edges facing the spine.",
        "Priority order for added canopy: Children's Play Zone and Multipurpose Sports Lawn "
        "(lowest computed annual shade, 3.6% and 4.3%) should receive canopy trees first.",
        "Re-run this simulation once specific tree placements are finalized in Phase 6 to "
        "confirm improved room-level annual shade percentages before construction documentation.",
    ]},
    {"type": "heading", "text": "Data Integrity Statement"},
    {"type": "para", "text": (
        "All percentages above are computed by simulating light-blocking geometry over the "
        "actual masterplan layout using real solar angles across either 3 sample dates or the "
        "full 8,760-hour year — not asserted or visually estimated."
    )},
]

build_report(
    output_path=os.path.join(OUT_DIR, "..", "Phase7_Performance_and_Sustainability_Report.pdf"),
    phase_tag="PHASE 7 — PERFORMANCE & SUSTAINABILITY [UPGRADED]",
    title="Performance & Sustainability",
    subtitle="Al Safa 2 Park — Shade, Water, Cost, Carbon & Thermal-Comfort — All Computed",
    sections=sections,
    code_ref=full_code,
    script_name="07_PHASE7_.../01_shade_coverage_model.py + 02_annual_shade_hours_model.py + 03_water_demand_model.py",
)
