import os
import sys
import json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "01_PHASE1_EXISTING_PARK", "_scripts"))
from docx_report_builder import build_docx_report, convert_docx_to_pdf

HERE = os.path.dirname(__file__)
OUT_DIR = os.path.join(HERE, "..")
MODEL_OUT = os.path.join(OUT_DIR, "outputs")
SCORE_SCRIPT = os.path.join(HERE, "01_problem_severity_model.py")

with open(os.path.join(MODEL_OUT, "problem_severity_scores.json")) as f:
    scores = json.load(f)
with open(SCORE_SCRIPT, "r", encoding="utf-8") as f:
    score_code = f.read()

score_rows = [[str(s["Rank"]), s["id"], s["name"][:46], str(s["WeightedScore"]), str(s["Priority"])]
              for s in scores]

sections = [
    {"type": "para", "text": (
        "<b>AI-GENERATED DRAFT — FOR REVIEW.</b> This Problem Definition is derived directly "
        "from the Phase 1 Existing Conditions Knowledge Base (now including real-data findings "
        "on population, transit, wind, and water). It is a first-pass synthesis, not a "
        "validated conclusion — review and adjust before treating it as final."
    )},
    {"type": "heading", "text": "2.0 Real-Data Context (v3)"},
    {"type": "bullets", "items": [
        "~7,640 residents live within a 10-min walk (real Dubai Statistics Center 2023 data, "
        "Phase 1.13) — a solid, quantified demand base for the park, confirming redevelopment "
        "is worthwhile.",
        "The adjacent metro station was literally named \"Al Safa Metro Station\" (now "
        "ONPASSIVE, Red Line, Zone 2) — real evidence the park sits in a genuine transit "
        "catchment, making the SZR pedestrian-crossing problem (below) more important, not less.",
        "Estimated peak demand (~169 concurrent) fits the benchmark capacity (225-600) — so "
        "the core problem is quality/comfort/shade, not raw capacity.",
    ]},
    {"type": "heading", "text": "2.1 Existing Performance Review"},
    {"type": "table", "header": ["Dimension", "Performance", "Evidence (Phase 1)"], "rows": [
        ["Functional", "Weak — single confirmed entrance, unclear internal path hierarchy",
         "1.03 Existing Park Analysis"],
        ["Spatial", "Imbalanced — canopy/shade concentrated west, open/hardscape east",
         "1.02 Urban Context image analysis, 1.11 SWOT"],
        ["Environmental", "Poor in summer — near-zero midday shade May-Oct, SZR noise/air edge",
         "1.05 Climate, 1.06 Shadow, 1.07 Environmental"],
        ["Social", "Undocumented — no observed activity/behavior data available",
         "1.09 Human Analysis"],
        ["Accessibility", "Undocumented baseline — no verified universal-design features",
         "1.10 Accessibility Analysis"],
        ["Safety", "Undocumented — no lighting/wayfinding data available",
         "1.03, 1.10"],
        ["Maintenance", "Undocumented — no condition survey available", "1.03 Existing Park Analysis"],
    ]},
    {"type": "heading", "text": "2.2 Problem Mapping"},
    {"type": "bullets", "items": [
        "<b>Underused areas (hypothesis):</b> the open/hardscape east zone, lacking canopy "
        "shade, is plausibly underused in hot months — consistent with the shade-equity gap "
        "identified in Phase 1.11 SWOT.",
        "<b>Heat-stress zones (confirmed by computation):</b> per Phase 1.06 Shadow Analysis, "
        "any unshaded surface experiences near-zero natural shade at summer solar noon "
        "(elevation ~88°) — the entire site is a heat-stress zone at that time without "
        "engineered shade.",
        "<b>Missing connections:</b> pedestrian link across Sheikh Zayed Road to ONPASSIVE "
        "Metro Station is unconfirmed/likely inadequate (Phase 1.08 Transportation).",
        "<b>Poor visibility / safety:</b> no lighting data confirmed — cannot verify nighttime "
        "visibility or safety sightlines (Phase 1.10).",
        "<b>Conflicting activities (hypothesis):</b> without confirmed zoning, active "
        "(sports/play) and passive (rest/quiet) uses may currently be unseparated — to be "
        "verified once DWG is available.",
        "<b>Barriers to movement:</b> Sheikh Zayed Road is a hard, confirmed barrier on the "
        "east edge (Phase 1.01, 1.08).",
        "<b>Gaps in amenities:</b> no confirmed parking, drop-off, cycling infrastructure, or "
        "accessible restroom/fountain provision (Phase 1.08, 1.10).",
    ]},
    {"type": "heading", "text": "2.3 Root Cause Analysis"},
    {"type": "table", "header": ["Problem", "Evidence", "Likely Cause", "Impact", "Priority"], "rows": [
        ["Summer heat-stress across most of site", "Shadow Analysis: <0.5m shadow at summer noon for any object under 6m",
         "Existing canopy insufficient / concentrated on one side; no engineered overhead shade",
         "Park unusable ~5 months/yr at midday", "HIGH"],
        ["Shade inequity (west vs east)", "Green-footprint image analysis (Phase 1.02)",
         "Historic planting concentrated on one side only", "Uneven usability across site", "MEDIUM"],
        ["Weak metro connectivity", "SZR confirmed barrier; no confirmed crossing (Phase 1.08)",
         "Park pre-dates or was not integrated with metro-era connectivity planning",
         "Reduced catchment / underuse of nearby transit asset", "MEDIUM"],
        ["Undocumented accessibility", "No survey data found (Phase 1.10)",
         "Park likely pre-dates current universal-design standards",
         "Risk of excluding older adults / People of Determination", "HIGH"],
        ["Unclear zoning/circulation", "No DWG-derived path network yet (Phase 1.03)",
         "As-built documentation not yet digitized/converted for this analysis",
         "Cannot verify activity conflicts until resolved", "MEDIUM (data-dependent)"],
    ]},
    {"type": "heading", "text": "2.4 User Needs Assessment"},
    {"type": "table", "header": ["User Group", "Likely Needs (from Phase 1.09)"], "rows": [
        ["Families", "Shaded picnic/gathering areas, sightlines to children, all-day comfort"],
        ["Children", "Inclusive, shaded play areas for multiple age bands"],
        ["Teenagers", "Active/social zones distinct from quiet family areas"],
        ["Students (school-adjacent)", "Safe pickup/drop-off adjacency, short-visit friendly spaces"],
        ["Older adults", "Level, shaded, seating-rich circulation; rest points"],
        ["Visitors (city-wide, challenge visibility)", "Clear wayfinding, an identifiable arrival/landmark moment"],
        ["People of Determination", "Step-free, wide, shaded, clearly wayfound circulation throughout"],
    ]},
    {"type": "heading", "text": "2.5 Experience Assessment"},
    {"type": "table", "header": ["Experience Stage", "Current State (from Phase 1)", "Gap"], "rows": [
        ["Arrival", "One confirmed entrance (west); no gateway feature confirmed", "Weak sense of arrival"],
        ["Wayfinding", "No signage data available", "Unknown / likely absent"],
        ["Comfort", "Near-zero shade at summer midday (computed)", "Critical gap May-Oct"],
        ["Rest", "Seating locations unconfirmed", "Unknown"],
        ["Play", "Playground not clearly identifiable in available imagery", "Unconfirmed provision"],
        ["Exercise", "No confirmed fitness/jogging infrastructure data", "Unconfirmed provision"],
        ["Social interaction", "Central plaza feature visible but function unconfirmed", "Ambiguous"],
        ["Safety", "No lighting data available", "Unknown, flagged as priority"],
    ]},
    {"type": "heading", "text": "2.6 Benchmark Gap Analysis"},
    {"type": "para", "text": (
        "Compared against the Dubai Municipality Neighborhood Parks Manual's own benchmark "
        "targets for this park archetype (05:00-23:00 operation, 1-3hr visits, 150-400 "
        "visitors/10,000sqm peak capacity, ~15% leasable commercial area, destination "
        "playscapes, wellness/fitness activities, seasonal event programming):"
    )},
    {"type": "table", "header": ["Manual Benchmark", "Existing Al Safa 2 (known)", "Gap"], "rows": [
        ["Destination playscapes + edutainment", "Playground not clearly confirmed", "Likely gap — verify/design in Phase 5-6"],
        ["Wellness / fitness activities", "Not confirmed", "Likely gap"],
        ["Commercial activities (~15% area / 2-5 sqm/visitor)", "No kiosks/F&B visible", "Gap — brief requires this (Section E)"],
        ["Digital routes / wayfinding challenges", "No wayfinding data", "Gap"],
        ["Seasonal celebrations / regular community events", "Not confirmed", "Opportunity for Phase 8 programming"],
    ]},
    {"type": "heading", "text": "2.7 Quantified Problem Severity Model (computed)"},
    {"type": "para", "text": (
        "Rather than assert priorities, each problem is scored 1–5 on four weighted criteria "
        "— Evidence strength (25%), Impact severity (30%), User reach (25%), Urgency (20%) — "
        "and ranked by weighted score. Every score traces to a Phase 1 finding. This is a "
        "reproducible computation (see the Program Proof appendix)."
    )},
    {"type": "image", "path": os.path.join(MODEL_OUT, "problem_severity_ranking.png"),
     "caption": "Figure 1 — Computed problem severity ranking, colored by priority band.", "width_cm": 16.5},
    {"type": "image", "path": os.path.join(MODEL_OUT, "problem_criteria_heatmap.png"),
     "caption": "Figure 2 — Per-criterion scoring matrix for each problem.", "width_cm": 13},
    {"type": "heading", "text": "Output — Prioritized Design Challenges (computed ranking)"},
    {"type": "table", "header": ["Rank", "ID", "Problem", "Score", "Priority"], "rows": score_rows},
    {"type": "para", "text": (
        "<b>The computation confirms the design strategy:</b> P1 (summer thermal discomfort) "
        "scores a maximum 5.00 / CRITICAL — mathematically the top priority — which is exactly "
        "why the whole design (Phases 4–7) is organized around the Shaded Spine. P2 "
        "(accessibility) follows at 4.30 / CRITICAL, driving the 100% step-free commitment. "
        "The design responds to problems in the order the evidence ranks them, not by intuition."
    )},
]

docx_path = build_docx_report(
    output_path=os.path.join(OUT_DIR, "Phase2_Problem_Definition_Report.docx"),
    phase_tag="PHASE 2 — PROBLEM DEFINITION [AI DRAFT]",
    title="Problem Definition",
    subtitle="Al Safa 2 Park — Prioritized Design Challenges + Computed Severity Model",
    sections=sections,
    code_ref=score_code,
    script_name="02_PHASE2_PROBLEM_DEFINITION/_scripts/01_problem_severity_model.py",
)
convert_docx_to_pdf(docx_path)
