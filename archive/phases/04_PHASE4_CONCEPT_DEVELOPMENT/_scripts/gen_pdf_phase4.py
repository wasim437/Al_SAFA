import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "01_PHASE1_EXISTING_PARK", "_scripts"))
from report_builder import build_report

HERE = os.path.dirname(__file__)
OUT_DIR = os.path.join(HERE, "..")

sections = [
    {"type": "para", "text": (
        "<b>AI-GENERATED DRAFT — FOR REVIEW.</b> Three distinct concept alternatives are "
        "developed and scored, each responding differently to Phase 3's objectives."
    )},
    {"type": "heading", "text": "4.1 Research Inspiration"},
    {"type": "bullets", "items": [
        "<b>Local context:</b> Dubai's Shamal wind pattern, palm/Ghaf shade traditions, "
        "sikka (shaded alleyway) urban form.",
        "<b>International precedents (typology reference, not copied):</b> shaded desert "
        "park strategies using canopy structures and misting (Middle East precedent), "
        "linear park zoning with clear activity bands (High Line-style legibility), "
        "biophilic play design for inclusive playgrounds.",
        "<b>Landscape trends:</b> climate-responsive/native xeriscaping, multi-generational "
        "activity zoning, park-as-microclimate-infrastructure thinking.",
    ]},
    {"type": "heading", "text": "4.2 Mood & Design Language Direction"},
    {"type": "para", "text": (
        "Material and form language: warm sand/stone tones, filtered dappled shade (not solid "
        "roofed structures everywhere), local Ghaf/palm planting as the dominant canopy "
        "species, and a restrained geometric language (straight + arced paths) echoing the "
        "site's elongated rectangular geometry rather than fighting it."
    )},
    {"type": "heading", "text": "4.4 Concept Alternatives"},
    {"type": "table", "header": ["", "Concept A — \"Shaded Spine\"", "Concept B — \"Canopy Village\"", "Concept C — \"Cool Loop\""], "rows": [
        ["Organizing idea", "One continuous shaded central spine connects all zones",
         "Cluster of discrete shaded \"rooms\" (play, fitness, social, quiet) around a plaza",
         "A single perimeter shaded loop (jogging/walking) with activities nested inside"],
        ["Circulation", "Linear, highly legible, single primary path",
         "Radial from central plaza to each room",
         "Circular loop + inner cross-paths"],
        ["Shade strategy", "Continuous overhead shade structure along the spine",
         "Shade concentrated per-room (tree clusters + pergolas)",
         "Shade concentrated on the loop itself"],
        ["Best fits", "Wayfinding clarity, day/night activation along one axis",
         "Distinct age-group zoning, event flexibility",
         "Fitness/wellness emphasis, continuous exercise use"],
        ["Risk", "Areas off the spine may still be under-shaded",
         "Central plaza could become a pinch-point / less flexible for events",
         "Interior zones could feel disconnected from the loop's comfort"],
    ]},
    {"type": "heading", "text": "4.5 AI-Assisted Exploration"},
    {"type": "para", "text": (
        "All three concepts were tested against Phase 1.06's shadow-length data "
        "(6m canopy shadow ranges from ~0.2m at summer noon to ~19m at winter evening) to "
        "sanity-check shade-structure spacing assumptions before scoring. This is documented "
        "further in Phase 9 (AI Workflow)."
    )},
    {"type": "heading", "text": "4.6 Evaluation Matrix"},
    {"type": "table", "header": ["Criterion (weight)", "A: Shaded Spine", "B: Canopy Village", "C: Cool Loop"], "rows": [
        ["Function (25%)", "8", "7", "8"],
        ["User Experience (25%)", "8", "9", "7"],
        ["Sustainability (20%)", "7", "8", "7"],
        ["Feasibility within AED 35M (20%)", "9", "6", "8"],
        ["Innovation (10%)", "7", "8", "6"],
        ["<b>Weighted Total /10</b>", "<b>7.85</b>", "<b>7.55</b>", "<b>7.35</b>"],
    ]},
    {"type": "heading", "text": "4.7 Final Concept Selection"},
    {"type": "para", "text": (
        "<b>Selected: Concept A — \"Shaded Spine\"</b>, with Concept B's room-based zoning "
        "logic merged in as secondary structure along the spine (best of both: legibility + "
        "distinct age-group zones). Justification: highest feasibility score within the fixed "
        "AED 35M budget, directly addresses Phase 2's #1 evidence-backed problem (summer "
        "thermal comfort) via one continuous engineered shade structure rather than dozens of "
        "smaller ones, and gives the AI Design Challenge submission the clearest single "
        "diagram to communicate (important per Evaluation Matrix criterion 6: Quality of "
        "Presentation, 5% weight, and criterion 4: Quality of Design and User Experience, 15%)."
    )},
]

build_report(
    output_path=os.path.join(OUT_DIR, "Phase4_Concept_Development_Report.pdf"),
    phase_tag="PHASE 4 — CONCEPT DEVELOPMENT [AI DRAFT]",
    title="Concept Development",
    subtitle="Al Safa 2 Park — Alternatives, Evaluation & Final Concept Selection",
    sections=sections,
    code_ref=None,
)
