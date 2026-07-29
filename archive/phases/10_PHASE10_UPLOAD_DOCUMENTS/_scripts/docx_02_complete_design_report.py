"""
Phase 10.2 - Complete Design Report
A single cohesive master submission document that tells the whole story from
site analysis to final design, pulling the key real-data results and the design
into one narrative. This is the flagship "Complete Design Report" upload (slot 10).
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "01_PHASE1_EXISTING_PARK", "_scripts"))
from docx_report_builder import build_docx_report, convert_docx_to_pdf

BASE = os.path.join(os.path.dirname(__file__), "..", "..")
DEST = os.path.join(os.path.dirname(__file__), "..", "10.2_Required_Files", "10_Complete_Design_Report")
os.makedirs(DEST, exist_ok=True)

def img(*parts):
    return os.path.join(BASE, *parts)

sections = [
    {"type": "para", "text": (
        "<b>AI-GENERATED DRAFT — FOR REVIEW.</b> This Complete Design Report tells the full "
        "story of the Al Safa 2 Park proposal from evidence to design. It is a compiled "
        "summary; each section has its own detailed standalone report in the submission package."
    )},

    {"type": "heading", "text": "Executive Summary"},
    {"type": "para", "text": (
        "Al Safa 2 Park is a 15,000 sqm neighborhood park serving ~7,640 residents within a "
        "10-minute walk (Dubai Statistics Center 2023). Our proposal — <b>\"The Shaded "
        "Spine\"</b> — answers the park's single biggest, evidence-proven problem: Dubai's "
        "extreme heat leaves the site with almost no usable shade at summer midday. We solve "
        "this with one continuous, fully-shaded central walkway (computed at 99.2% annual "
        "shade coverage) connecting eight activity 'rooms', delivering a genuinely year-round, "
        "universally accessible, water-efficient public space within the AED 35M budget. AI "
        "was used throughout as an analysis and testing tool — not as the designer."
    )},

    {"type": "heading", "text": "Presentation Boards"},
    {"type": "image", "path": img("09_PHASE9_AI_WORKFLOW_AND_VISUALIZATION", "9.9_Presentation_Graphics", "presentation_board_1_concept.png"),
     "caption": "Board 1 — Concept & Master Plan.", "width_cm": 17.5},
    {"type": "image", "path": img("09_PHASE9_AI_WORKFLOW_AND_VISUALIZATION", "9.9_Presentation_Graphics", "presentation_board_2_evidence.png"),
     "caption": "Board 2 — Evidence & Performance (real data, computed proof).", "width_cm": 17.5},

    {"type": "heading", "text": "1. Site Understanding (Phase 1) — Real Data Foundation"},
    {"type": "bullets", "items": [
        "<b>Climate (Dubai Meteorological Office):</b> comfortable Nov-Apr; extreme heat "
        "May-Oct with near-zero natural midday shade; 8-11.5 sunshine hours/day.",
        "<b>Solar (computed, 8,760 hrs/yr):</b> summer noon sun near-overhead (~88°); "
        "only overhead structures give real midday summer shade.",
        "<b>Wind (Windfinder, 2002-2026):</b> WNW dominant, 16.7 km/h avg — usable for passive "
        "cooling.",
        "<b>Population (Dubai Statistics Center 2023):</b> ~7,640 within 10-min walk; est. peak "
        "demand ~169 fits the 225-600 capacity benchmark.",
        "<b>Transit (RTA):</b> ONPASSIVE metro (Red Line, Zone 2) — formerly 'Al Safa Metro "
        "Station' — sits in the park's catchment across Sheikh Zayed Road.",
    ]},
    {"type": "image", "path": img("01_PHASE1_EXISTING_PARK", "05_Climate_Analysis", "outputs", "fullyear_elevation_heatmap.png"),
     "caption": "Full-year (8,760-hour) exact solar elevation — the evidence base for the shade strategy.",
     "width_cm": 16},
    {"type": "image", "path": img("01_PHASE1_EXISTING_PARK", "13_Catchment_Demand_Analysis", "outputs", "catchment_rings.png"),
     "caption": "Real walk-catchment population (Dubai Statistics Center 2023).", "width_cm": 12},

    {"type": "heading", "text": "2. Problems & Objectives (Phases 2-3)"},
    {"type": "para", "text": (
        "The prioritized problems: (P1) summer thermal discomfort, (P2) undocumented "
        "accessibility, (P3) shade inequity, (P4) missing commercial/service facilities, "
        "(P5) weak legibility, (P6) severed metro connectivity across SZR. Vision: <i>Dubai's "
        "first neighborhood park shaped as much by climate science as by community voice.</i>"
    )},

    {"type": "heading", "text": "3. Concept & Master Plan (Phases 4-5)"},
    {"type": "para", "text": (
        "Three concepts were scored on a weighted matrix; <b>Concept A \"Shaded Spine\"</b> won "
        "(7.85/10, highest feasibility). The master plan realizes it as a scaled layout summing "
        "exactly to 15,000 sqm: two entrance plazas, a 10m-wide continuous shaded central "
        "walkway, and eight activity rooms (play, picnic, community plaza, fitness, quiet "
        "garden, commercial kiosks, sports lawn, biodiversity strip)."
    )},
    {"type": "image", "path": img("05_PHASE5_MASTERPLAN_DEVELOPMENT", "outputs", "masterplan_diagram.png"),
     "caption": "Preliminary Master Plan — Concept A, to scale, 15,000 sqm.", "width_cm": 17},

    {"type": "heading", "text": "4. Detailed Design (Phase 6)"},
    {"type": "para", "text": (
        "Real UAE-native planting (Ghaf, Neem, Date Palm, Ficus nitida, Olive, Paspalum turf); "
        "light-toned low-heat paving; continuous canopy lighting. The Shaded Spine section is "
        "sized against the real computed summer/winter solar angles."
    )},
    {"type": "image", "path": img("06_PHASE6_DETAILED_DESIGN", "outputs", "section_shaded_spine.png"),
     "caption": "Section A-A through the Shaded Spine, with real solar angles overlaid.", "width_cm": 16},

    {"type": "heading", "text": "5. Performance & Sustainability (Phase 7) — Proven, Not Claimed"},
    {"type": "bullets", "items": [
        "<b>Shade:</b> the Shaded Spine achieves 99.2% annual shade coverage (computed across "
        "all 4,425 real daylight hours) — and ≥97% every single month.",
        "<b>Water:</b> a real computed irrigation budget of ~5,700 m³/year, derived from real "
        "Ghaf field-study figures and real Dubai temperatures.",
        "<b>Honest finding:</b> activity-room interiors need their own canopy trees (they get "
        "only 3.6-16.2% passive shade from the spine alone) — a real fix the analysis surfaced.",
    ]},
    {"type": "image", "path": img("07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY", "outputs", "annual_shade_hours_by_zone.png"),
     "caption": "Annual shade coverage by zone (full-year computed simulation).", "width_cm": 16},
    {"type": "image", "path": img("07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY", "outputs", "water_demand_monthly.png"),
     "caption": "Computed monthly irrigation water demand (real Ghaf + real temperatures).", "width_cm": 16},

    {"type": "heading", "text": "5b. Feasibility — Computed Cost Estimate"},
    {"type": "para", "text": (
        "An element-by-element cost estimate using real sourced Dubai landscape unit rates "
        "(upper bound + standard construction add-ons) totals <b>~AED 18.6M — about 53% of the "
        "AED 35M budget</b>, leaving substantial headroom for public-park spec uplift and the "
        "per-room canopy enhancement. Affordability is computed, not assumed."
    )},
    {"type": "image", "path": img("07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY", "outputs", "budget_gauge.png"),
     "caption": "Budget utilisation vs the AED 35M competition budget.", "width_cm": 16},

    {"type": "heading", "text": "5c. Comfort & Carbon (Computed)"},
    {"type": "bullets", "items": [
        "<b>Thermal comfort:</b> using the NWS Heat Index on real Dubai temp+humidity, shade "
        "<b>doubles the comfortable season from 3 to 6 months/year</b> (+3 months).",
        "<b>Carbon:</b> the 131-tree native planting plan sequesters <b>~2.1 tonnes CO₂/year</b> "
        "at maturity (real arid-climate rates) — ~12,700 car-km equivalent.",
        "<b>Planting plan:</b> canopy trees concentrated inside the lowest-shade activity rooms "
        "(Play, Sports, Fitness) — closing the gap the annual simulation exposed.",
    ]},
    {"type": "image", "path": img("07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY", "outputs", "thermal_comfort.png"),
     "caption": "Felt temperature in sun vs shade — shade adds 3 comfortable months/year.", "width_cm": 15},
    {"type": "image", "path": img("06_PHASE6_DETAILED_DESIGN", "outputs", "planting_plan.png"),
     "caption": "Planting plan — 131 native/adapted trees, priority canopy in the low-shade rooms.", "width_cm": 16},

    {"type": "heading", "text": "6. User Experience (Phase 8)"},
    {"type": "para", "text": (
        "Five personas grounded in the real catchment population and the actual zones — from a "
        "parent doing school pickup to a wheelchair user relying on 100% step-free circulation "
        "— each with a mapped journey through the park."
    )},

    {"type": "heading", "text": "6b. Whole-Life Feasibility — Annual Running Cost"},
    {"type": "para", "text": (
        "Beyond the build cost, the annual operations & maintenance cost is computed "
        "(real DEWA water tariff on the computed water volume + standard O&M ratios): "
        "<b>~AED 2.0M/year, giving a 10-year total cost of ownership of ~AED 38M</b>. "
        "Costing operations — not just construction — is whole-life feasibility rigour."
    )},
    {"type": "image", "path": img("07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY", "outputs", "om_cost.png"),
     "caption": "Annual O&M breakdown + 10-year total cost of ownership.", "width_cm": 16},

    {"type": "heading", "text": "7. Visualization (Phase 9)"},
    {"type": "image", "path": img("09_PHASE9_AI_WORKFLOW_AND_VISUALIZATION", "9.7_Renderings", "Aerial", "aerial_day.png"),
     "caption": "Aerial day view.", "width_cm": 16},
    {"type": "image", "path": img("09_PHASE9_AI_WORKFLOW_AND_VISUALIZATION", "9.7_Renderings", "Aerial", "aerial_night.png"),
     "caption": "Aerial night view (illustrative lighting).", "width_cm": 16},
    {"type": "image", "path": img("09_PHASE9_AI_WORKFLOW_AND_VISUALIZATION", "9.7_Renderings", "Eye_Level", "eyelevel_shaded_spine.png"),
     "caption": "Eye-level view down the Shaded Spine.", "width_cm": 16},

    {"type": "heading", "text": "8. Why This Proposal Wins"},
    {"type": "bullets", "items": [
        "<b>Innovation (20%):</b> AI used for real quantitative analysis (8,760-hr solar, "
        "shade simulation, water & demand models) — not just pretty renders.",
        "<b>Human-Centered/Sustainability (20%):</b> directly solves the #1 real problem "
        "(heat) with proven 99.2% shaded circulation, +3 comfortable months (Heat Index), a "
        "real ~5,700 m³/yr water budget, and ~2.1 t CO₂/yr sequestration.",
        "<b>AI Integration (20%):</b> every phase has a reproducible Python script and a "
        "'Program Proof' code appendix — full transparency.",
        "<b>Design Quality/UX (15%):</b> one legible organizing idea, real personas, day/night "
        "activation.",
        "<b>Feasibility (20%):</b> highest-feasibility concept, costed to the AED 35M budget, "
        "with a real computed water budget.",
        "<b>Presentation (5%):</b> a consistent, professional, fully-sourced document set.",
    ]},

    {"type": "heading", "text": "Integrity Statement"},
    {"type": "para", "text": (
        "Every quantitative figure in this proposal is either (a) computed from real astronomy/"
        "geometry, (b) sourced from a named real dataset with a retrieval date, or (c) a "
        "clearly-labeled planning assumption. Genuine data gaps (exact DWG park boundary, "
        "on-site GIS/soil/noise) are flagged, never fabricated — because integrity is what "
        "separates a credible submission from a disqualified one."
    )},
]

docx_path = build_docx_report(
    output_path=os.path.join(DEST, "Al_Safa_2_Park_Complete_Design_Report.docx"),
    phase_tag="COMPLETE DESIGN REPORT",
    title="Complete Design Report",
    subtitle="Al Safa 2 Park — \"The Shaded Spine\" | Dubai Municipality AI Park Design Challenge",
    sections=sections,
    code_ref=None,
)
convert_docx_to_pdf(docx_path)
