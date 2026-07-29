import os
import json
from report_builder import build_report

HERE = os.path.dirname(__file__)
OUT_DIR = os.path.join(HERE, "..", "13_Catchment_Demand_Analysis", "outputs")
SCRIPT_PATH = os.path.join(HERE, "06_catchment_demand_model.py")

with open(os.path.join(OUT_DIR, "catchment_demand_results.json")) as f:
    r = json.load(f)
with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
    code = f.read()

pop_rows = [[k, f"{v:,}"] for k, v in r["population_sources"].items()]
ring_rows = [[w["ring"], f"{w['radius_m']}m", f"{w['area_km2']} km²", f"{w['est_residents']:,}"] for w in r["walk_catchment"]]
dm = r["demand_model"]

sections = [
    {"type": "para", "text": (
        "<b>NEW real-data analysis (added in the v3 upgrade pass).</b> This answers a question "
        "the earlier Phase 1 left as a data gap: how many people actually depend on this park, "
        "and can the design serve them? It uses <b>real Dubai Statistics Center 2023 population "
        "figures</b> combined with a computed walk-catchment model."
    )},
    {"type": "heading", "text": "1. Real Population (Dubai Statistics Center, 2023)"},
    {"type": "table", "header": ["Community", "Residents (2023)"], "rows": pop_rows},
    {"type": "image", "path": os.path.join(OUT_DIR, "catchment_population.png"),
     "caption": "Figure 1 — Surrounding community population (Dubai Statistics Center, 2023 Bulletin).",
     "width_cm": 15},
    {"type": "heading", "text": "2. Walk Catchment (computed rings × real density)"},
    {"type": "para", "text": (
        "Using the real Al Safa density figure of <b>3,800 persons/km²</b> (Dubai Statistics "
        "Center), residents within standard neighborhood-park walk radii were computed:"
    )},
    {"type": "table", "header": ["Ring", "Radius", "Area", "Est. Residents"], "rows": ring_rows},
    {"type": "image", "path": os.path.join(OUT_DIR, "catchment_rings.png"),
     "caption": "Figure 2 — Walk-catchment rings and estimated residents (rings computed; density real).",
     "width_cm": 14},
    {"type": "heading", "text": "3. Demand vs. Capacity"},
    {"type": "table", "header": ["Metric", "Value"], "rows": [
        ["Primary (800m / 10-min walk) catchment", f"~{dm['primary_catchment_800m_residents']:,} residents"],
        ["Assumed peak-day participation rate", f"{int(dm['assumed_participation_rate']*100)}% (planning assumption)"],
        ["Estimated daily visitors (peak day)", f"~{dm['est_daily_visitors']:,}"],
        ["Estimated peak concurrent visitors", f"~{dm['est_peak_concurrent_visitors']}"],
        ["Benchmark capacity (Manual, low-high)", f"{dm['capacity_low']}-{dm['capacity_high']} concurrent"],
    ]},
    {"type": "image", "path": os.path.join(OUT_DIR, "demand_vs_capacity.png"),
     "caption": "Figure 3 — Estimated peak concurrent demand vs. benchmark capacity range.", "width_cm": 15},
    {"type": "para", "text": (
        f"<b>Verdict: {dm['verdict']}.</b> The estimated ~{dm['est_peak_concurrent_visitors']} "
        f"peak concurrent visitors sits comfortably within the Neighborhood Parks Manual's "
        f"{dm['capacity_low']}-{dm['capacity_high']} benchmark capacity for a 15,000 sqm park — "
        f"meaning the design does not need to plan for chronic overcrowding, but should retain "
        f"flexible event space for occasional surges (festivals, school events)."
    )},
    {"type": "heading", "text": "4. Data Integrity Statement"},
    {"type": "para", "text": (
        "Population figures are REAL, from the Dubai Statistics Center 2023 Population Bulletin "
        "(retrieved via web search 2026-07-24). Walk-radius geometry is computed. The "
        "participation rate (10%) and peaking factors are clearly-labeled planning assumptions "
        "— stated openly so a reviewer can challenge or re-tune them, rather than hidden."
    )},
]

build_report(
    output_path=os.path.join(OUT_DIR, "Phase1.13_Catchment_Demand_Analysis_Report.pdf"),
    phase_tag="PHASE 1.13 — CATCHMENT & DEMAND [REAL DATA]",
    title="Catchment & Demand Analysis",
    subtitle="Al Safa 2 Park — Real Population Catchment vs. Benchmark Capacity",
    sections=sections,
    code_ref=code,
    script_name="01_PHASE1_EXISTING_PARK/_scripts/06_catchment_demand_model.py",
)
