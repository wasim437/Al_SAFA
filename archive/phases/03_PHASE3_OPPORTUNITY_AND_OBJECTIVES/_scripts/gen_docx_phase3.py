import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "01_PHASE1_EXISTING_PARK", "_scripts"))
from docx_report_builder import build_docx_report, convert_docx_to_pdf

HERE = os.path.dirname(__file__)
OUT_DIR = os.path.join(HERE, "..")

sections = [
    {"type": "para", "text": (
        "<b>AI-GENERATED DRAFT — FOR REVIEW.</b> Translates Phase 2's problems into "
        "opportunities and measurable objectives. First-pass synthesis for review, not final."
    )},
    {"type": "heading", "text": "3.1 Opportunity Mapping"},
    {"type": "table", "header": ["Domain", "Opportunity", "Basis"], "rows": [
        ["Climate", "WNW prevailing wind (16.7 km/h avg, sourced) usable for passive cooling corridors; winter sun (41°) usable for seasonal solar-responsive zones", "Phase 1.05/1.06"],
        ["Landscape", "Full redevelopment allows rebalancing canopy from west-only to site-wide equitable shade", "Phase 1.02, 1.11"],
        ["Social", "Adjacent school/mosque/rehab center provide built-in recurring user base", "Phase 1.01, 1.09"],
        ["Ecological", "Opportunity to introduce native/climate-responsive planting and biodiversity features not present today", "Phase 1.07"],
        ["Mobility", "Metro proximity is a real catchment asset if pedestrian connectivity across SZR is improved", "Phase 1.08"],
        ["Technology", "AI Design Challenge status + budget allow genuine smart-park infrastructure (brief Section 10)", "Competition Brief"],
    ]},
    {"type": "heading", "text": "3.2 Vision Statement"},
    {"type": "para", "text": (
        "<i>\"Al Safa 2 Park becomes Dubai's first neighborhood park shaped as much by climate "
        "science as by community voice — a shaded, year-round, inclusive gathering ground that "
        "proves AI-assisted design can produce more human, not less human, public space.\"</i>"
    )},
    {"type": "heading", "text": "3.3 Design Mission"},
    {"type": "para", "text": (
        "To redevelop a 15,000 sqm neighborhood park that closes the park's most evidence-backed "
        "gap (summer thermal comfort) while delivering full universal accessibility, a "
        "balanced activity mix, and a self-sustaining commercial layer — within the AED 35M "
        "budget — using AI as a rigor tool for analysis, iteration and testing, not as a "
        "gimmick or design output in itself."
    )},
    {"type": "heading", "text": "3.4 Project Objectives"},
    {"type": "table", "header": ["Objective Type", "Statement"], "rows": [
        ["Human-centered", "Every zone usable and comfortable for children, families, teens, older adults, and People of Determination"],
        ["Climate-responsive", "Eliminate unshaded midday exposure across all primary circulation and gathering spaces during peak summer"],
        ["Inclusive", "100% step-free, universal-design circulation from every entrance to every major destination"],
        ["Sustainable", "Native/climate-adapted planting, water-sensitive irrigation, and biodiversity enhancement as default, not add-on"],
        ["Feasible", "Every proposed element sized and specified to fit within the AED 35M implementation budget"],
    ]},
    {"type": "heading", "text": "3.5 Success Metrics"},
    {"type": "table", "header": ["Metric", "Target (draft, to validate in Phase 7)"], "rows": [
        ["Shaded route coverage", "≥80% of primary circulation shaded at summer solar noon"],
        ["Accessible circulation", "100% of paths meet universal-design gradient/width standards"],
        ["Usable green/active space", "≥60% of site area as green/planted or soft-surface active space"],
        ["Biodiversity", "Net increase in native tree/shrub species count vs. existing baseline (once DWG confirms baseline)"],
        ["Community use", "Support the Manual's benchmark of 60+ small events/year for a park this size"],
    ]},
    {"type": "heading", "text": "3.6 Design Principles"},
    {"type": "bullets", "items": [
        "<b>People first</b> — every design choice traceable to a real user need from Phase 2.4.",
        "<b>Nature first</b> — planting and shade lead the layout, not fill leftover space.",
        "<b>AI as a design assistant</b> — used for analysis, iteration, and testing; final "
        "judgment stays human (per Brief Schedule 1, Section A).",
        "<b>Flexibility</b> — spaces support multiple uses across day/night and seasons.",
        "<b>Local identity</b> — materials and forms that read as authentically Dubai/Al Safa, "
        "not generic global parkland.",
    ]},
]

docx_path = build_docx_report(
    output_path=os.path.join(OUT_DIR, "Phase3_Opportunity_and_Objectives_Report.docx"),
    phase_tag="PHASE 3 — OPPORTUNITY & OBJECTIVES [AI DRAFT]",
    title="Opportunity & Design Objectives",
    subtitle="Al Safa 2 Park — Vision, Mission, Objectives, Success Metrics, Principles",
    sections=sections,
)
convert_docx_to_pdf(docx_path)
