import os
from report_builder import build_report

HERE = os.path.dirname(__file__)
OUT_DIR = os.path.join(HERE, "..", "09_Human_Analysis", "outputs")
os.makedirs(OUT_DIR, exist_ok=True)

sections = [
    {"type": "heading", "text": "1. User Groups Named in the Competition Brief"},
    {"type": "para", "text": (
        "The brief (Schedule 1, Section B) explicitly requires consideration of: Children, "
        "Youth, Families, Older adults, People of Determination."
    )},
    {"type": "heading", "text": "2. Target Audience per Neighborhood Parks Manual"},
    {"type": "para", "text": "Families, Sport enthusiasts, Picnickers, Teenagers, Pet owners."},
    {"type": "heading", "text": "3. Target Parameters (Manual Benchmarks)"},
    {"type": "table", "header": ["Parameter", "Benchmark"], "rows": [
        ["Duration of visit", "1-3 hours"],
        ["Peak visitor capacity", "150-400 visitors per 10,000 sqm"],
        ["Number of events supported", "S: 60+/yr, M: 24+/yr, L: 3+/yr"],
        ["Gross spend per visit", "AED 20-80"],
        ["Leasable commercial area", "~15% of total park area / 2-5 sqm per visitor"],
    ]},
    {"type": "para", "text": (
        "Applying the capacity benchmark to this site's 15,000 sqm: indicative peak capacity "
        "range is approximately <b>225-600 visitors</b> — a benchmark-derived estimate, not a "
        "measured figure."
    )},
    {"type": "heading", "text": "4. Office Workers, Students, Visitors"},
    {"type": "para", "text": (
        "Not explicitly addressed in the brief; but given adjacency to Umm Suqeim Model School "
        "for Basic Education (confirmed from master-plan graphic), student/school-day traffic "
        "is a plausible real user group worth carrying forward even though not explicitly "
        "named in the brief. City-wide \"visitors\" are also relevant given this is a flagship "
        "AI Design Challenge site."
    )},
    {"type": "heading", "text": "5. Activity Mapping, Movement, Behavior, Comfort, Needs — Data Status"},
    {"type": "para", "text": (
        "Genuine behavioral data (movement heatmaps, dwell-time studies, comfort surveys) "
        "requires either an actual site visit/observation study or sensor/mobile-location "
        "data — neither is available in the provided competition package. The brief explicitly "
        "asks participants to address this using AI tools (persona simulation, movement "
        "pattern analysis) as part of the design process — meaning it is expected to be "
        "<i>produced</i> in later phases, not sourced as existing data now."
    )},
    {"type": "heading", "text": "6. What Belongs Here vs. Later"},
    {"type": "para", "text": (
        "This document captures the known, evidence-based facts about who uses/will use the "
        "park. Persona development, journey mapping, and behavior simulation are correctly "
        "deferred to Phase 8 (User Experience & Activation) and Phase 4.5 (AI-Assisted "
        "Exploration)."
    )},
]

build_report(
    output_path=os.path.join(OUT_DIR, "Phase1.09_Human_Analysis_Report.pdf"),
    phase_tag="PHASE 1.09 — HUMAN ANALYSIS",
    title="Human Analysis",
    subtitle="Al Safa 2 Park — User Groups (Brief + Neighborhood Parks Manual)",
    sections=sections,
    code_ref=None,
)
