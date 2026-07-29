import os
from report_builder import build_report

HERE = os.path.dirname(__file__)
OUT_DIR = os.path.join(HERE, "..", "11_SWOT", "outputs")
SCRIPT_PATH = os.path.join(HERE, "04_swot_synthesis.py")

with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
    code = f.read()

sections = [
    {"type": "heading", "text": "1. Purpose"},
    {"type": "para", "text": (
        "This report synthesizes findings from Phase 1.01-1.10 into a single SWOT matrix. "
        "Nothing here is new invented data — every point traces back to an earlier Phase 1 "
        "sub-analysis document."
    )},
    {"type": "image", "path": os.path.join(OUT_DIR, "swot_matrix.png"),
     "caption": "Figure 1 — SWOT Matrix (Python-generated synthesis).", "width_cm": 17.5},
    {"type": "heading", "text": "2. Opportunities & Constraints Summary"},
    {"type": "para", "text": "<b>Constraints (hard facts that limit design freedom):</b>"},
    {"type": "bullets", "items": [
        "Fixed site area: 15,000 sqm — no expansion possible.",
        "Fixed budget ceiling: AED 35,000,000 implementation cost.",
        "Sheikh Zayed Road borders the east edge — a permanent noise/physical barrier.",
        "Submission requires Concept + Preliminary Design only — detailed construction "
        "documentation is explicitly out of scope at this stage.",
        "All winning-entry IP transfers to Dubai Municipality.",
        "Climate: ~5 months (May-Oct) of extreme heat with near-zero natural shade at solar "
        "noon — a hard environmental constraint.",
    ]},
    {"type": "para", "text": "<b>Opportunities (real, evidence-based, not yet decided how to use):</b>"},
    {"type": "bullets", "items": [
        "Full redevelopment scope (not retrofit) — every zone can be reprogrammed from scratch.",
        "WNW prevailing wind pattern (16.7 km/h avg, sourced) — usable for passive ventilation corridors.",
        "Winter sun angle (~41&#176; at noon) — usable for solar-responsive seasonal design.",
        "Adjacent school, mosque, and rehab center — built-in recurring user bases.",
        "Metro proximity — a genuine regional catchment opportunity IF pedestrian connectivity "
        "across SZR is addressed.",
        "High public visibility of the AI Design Challenge — potential citywide precedent.",
    ]},
    {"type": "para", "text": (
        "This document intentionally stops at listing opportunities/constraints — it does not "
        "select or prioritize a design response. That belongs to Phase 3 (Opportunity & Design "
        "Objectives)."
    )},
]

build_report(
    output_path=os.path.join(OUT_DIR, "Phase1.11_SWOT_Report.pdf"),
    phase_tag="PHASE 1.11 — SWOT ANALYSIS",
    title="SWOT Analysis",
    subtitle="Al Safa 2 Park — Synthesis of Phase 1.01–1.10 Findings",
    sections=sections,
    code_ref=code,
    script_name="01_PHASE1_EXISTING_PARK/_scripts/04_swot_synthesis.py",
)
