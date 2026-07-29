"""
Project Methodology Roadmap - a single PDF explaining, step by step, HOW each
phase produces its answer and feeds the next, all the way to the final 12 files.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "01_PHASE1_EXISTING_PARK", "_scripts"))
from report_builder import build_report

OUT_DIR = os.path.join(os.path.dirname(__file__), "..")

sections = [
    {"type": "para", "text": (
        "<b>This document shows the method — how the whole project was built, step by step.</b> "
        "Each phase takes the previous phase's output as its input, so the design is traceable "
        "end-to-end: every decision leads back to real data. Read it to understand the logic "
        "of how we got from 'an empty site' to 'the final 12 submission files.'"
    )},
    {"type": "heading", "text": "The Chain — How Each Phase Feeds the Next"},
    {"type": "table", "col_widths": [1.5, 2.2, 4.5, 2.6],
     "header": ["Phase", "Input (from prev.)", "What We Do (method)", "Output (the answer)"], "rows": [
        ["1. Understand Site", "Competition files (brief, DWG, map, manual)",
         "Pull & compute REAL data: 8,760-hr solar (pvlib), sourced climate (Dubai Met Office), catchment (Dubai Stats Center), wind, transit. Python + pandas.",
         "Existing Conditions Knowledge Base + SWOT"],
        ["2. Define Problems", "Phase 1 Knowledge Base (weaknesses, gaps)",
         "Score every problem 1-5 on Evidence/Impact/Reach/Urgency with a weighted Python model; rank them.",
         "Ranked problem list (P1 heat = 5.0/CRITICAL)"],
        ["3. Set Objectives", "Phase 2 ranked problems",
         "Turn each top problem into a measurable objective + success metric.",
         "Vision, mission, 5 objectives, 5 metrics"],
        ["4. Choose Concept", "Phase 3 objectives",
         "Generate 3 concepts; score each on a weighted matrix (function, UX, sustainability, feasibility, innovation).",
         "Winner: 'Shaded Spine' (7.85/10)"],
        ["5. Master Plan", "Phase 4 chosen concept",
         "Draw the concept as REAL scaled geometry in Python — 13 zones summing to exactly 15,000 m² + circulation.",
         "Master plan + circulation diagram + area schedule"],
        ["6. Detailed Design", "Phase 5 zone geometry",
         "Assign REAL native species per zone, place 131 trees, draw section + elevations to scale.",
         "Planting plan, materials, section, elevations"],
        ["7. Prove Performance", "Phase 5 geometry + Phase 6 planting",
         "COMPUTE everything: shade over 8,760 hrs, water budget (real Ghaf data), build cost (real Dubai rates), carbon, Heat-Index comfort, annual O&M.",
         "99.2% shade, ~AED18.6M build, +3 comfort months, 2.1t CO2/yr, ~AED2M/yr O&M"],
        ["8. User Experience", "Phase 1 catchment + Phase 5 zones",
         "Build personas from the real population; map their journeys through the actual zones.",
         "5 personas, daily/seasonal use, journey maps"],
        ["9. AI + Visualize", "All prior phases",
         "Document the AI method for every phase; generate renders (aerial day/night, eye-level) + 2 presentation boards.",
         "AI methodology report + all visuals + boards"],
        ["10. Package", "Everything above",
         "Auto-compile each output into its correct upload folder; QA against the brief; build the master report + checklist.",
         "The final 12 submission files, verified"],
    ]},
    {"type": "heading", "text": "Worked Example — How Phase 1 Produces One Answer"},
    {"type": "para", "text": (
        "Take the single most important finding, so you can see the method concretely:"
    )},
    {"type": "bullets", "items": [
        "<b>Question:</b> \"Does the existing park have usable shade in summer?\"",
        "<b>Data pulled (real):</b> the site's exact latitude/longitude → fed to pvlib (NASA/NREL "
        "solar algorithm) to compute the sun's exact position for all 8,760 hours of the year.",
        "<b>Analysis (Python):</b> for the summer solstice at noon, the sun sits ~88° above the "
        "horizon → shadow length = object height ÷ tan(88°) ≈ almost zero.",
        "<b>Answer:</b> \"No — a normal tree casts a <0.5m shadow at summer noon, so the site is "
        "unshaded when it's hottest.\" This becomes Problem P1 in Phase 2.",
        "<b>How it feeds forward:</b> P1 scored 5.0/CRITICAL (Phase 2) → became the #1 objective "
        "(Phase 3) → drove the 'Shaded Spine' concept (Phase 4) → which Phase 7 then PROVED "
        "delivers 99.2% shade. Full circle, all from one real data pull.",
    ]},
    {"type": "heading", "text": "Worked Example — How Phase 2 Produces Its Answer"},
    {"type": "bullets", "items": [
        "<b>Question:</b> \"Which problem should the design solve first?\"",
        "<b>Data used:</b> the findings from all 13 Phase 1 sub-analyses.",
        "<b>Analysis (Python):</b> each candidate problem is scored 1-5 on four criteria — "
        "Evidence (25%), Impact (30%), Reach (25%), Urgency (20%) — and a weighted total is computed.",
        "<b>Answer:</b> a ranked list. P1 (summer heat) = 5.00 CRITICAL; P2 (accessibility) = "
        "4.30 CRITICAL; then the rest. The design then addresses problems in THIS computed order.",
        "<b>Why it matters:</b> priorities are calculated from evidence, not guessed — which is "
        "exactly what a jury wants to see.",
    ]},
    {"type": "heading", "text": "The Golden Rule Across All Phases"},
    {"type": "para", "text": (
        "Every number is one of three things, always labelled: (a) computed from real astronomy/"
        "geometry, (b) pulled from a named real dataset with a date, or (c) a clearly-flagged "
        "assumption. Real data gaps (the exact DWG boundary, on-site soil/noise) are stated "
        "honestly, never invented. That integrity is what makes the whole chain credible."
    )},
    {"type": "heading", "text": "Where to Find Each Phase's Work"},
    {"type": "para", "text": (
        "Each phase lives in its numbered folder (01–10). Inside each: the analysis outputs, the "
        "PDF report, and a `_scripts/` folder with the exact Python code that generated it. The "
        "`_FINAL_DELIVERABLES/` folder gathers all the finished reports and visuals in one place. "
        "Start from `START_HERE.md` at the top level."
    )},
]

build_report(
    output_path=os.path.join(OUT_DIR, "PROJECT_METHODOLOGY_ROADMAP.pdf"),
    phase_tag="METHODOLOGY ROADMAP",
    title="Project Methodology Roadmap",
    subtitle="Al Safa 2 Park — How Each Phase Produces Its Answer & Feeds the Next",
    sections=sections,
    code_ref=None,
)
