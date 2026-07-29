import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "01_PHASE1_EXISTING_PARK", "_scripts"))
from docx_report_builder import build_docx_report, convert_docx_to_pdf

HERE = os.path.dirname(__file__)
OUT_DIR = os.path.join(HERE, "..")
RENDER_DIR = os.path.join(OUT_DIR, "9.7_Renderings", "Aerial")
SCRIPT_PATH = os.path.join(HERE, "01_generate_aerial_render.py")

with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
    code = f.read()

sections = [
    {"type": "para", "text": (
        "<b>AI-GENERATED DRAFT — FOR REVIEW.</b> This report documents the AI methodology "
        "used across the entire project (Phases 1-9) and presents the visualization outputs, "
        "satisfying the Brief's requirement (Schedule 1, Section C) to explain how AI tools "
        "were integrated and the role of human judgment throughout."
    )},
    {"type": "heading", "text": "9.1 AI Workflow (End-to-End)"},
    {"type": "table", "header": ["Phase", "AI Role", "Human Role"], "rows": [
        ["1. Existing Site Understanding", "Extracted site data from documents/images; computed "
         "exact solar/shadow geometry (pvlib); flagged data gaps rather than inventing data",
         "Directed scope; validated what counted as 'real' vs. 'gap'"],
        ["2. Problem Definition", "Synthesized Phase 1 evidence into root-cause analysis and "
         "prioritized problems", "Will review priority ranking and adjust before final submission"],
        ["3. Opportunity & Objectives", "Translated problems into vision/mission/objectives/metrics",
         "Will validate the vision statement reflects the human team's actual intent"],
        ["4. Concept Development", "Generated 3 distinct concept alternatives and scored them "
         "against a weighted evaluation matrix", "Will confirm or override the concept selection"],
        ["5. Master Plan Development", "Generated an actual scaled zoning geometry (Python) "
         "summing exactly to the 15,000 sqm site area", "Will validate zone sizes/adjacencies "
         "against real programmatic needs and, once available, the true DWG site boundary"],
        ["6. Detailed Design", "Specified real UAE-native plant species, materials, and a "
         "solar-angle-validated section drawing", "Will confirm material/species choices with "
         "a licensed landscape architect before construction documentation"],
        ["7. Performance & Sustainability", "Ran a genuine shadow-casting simulation over the "
         "masterplan geometry using exact solar data — not a qualitative claim",
         "Will validate simulation assumptions (canopy heights, structure placement) against "
         "final structural design"],
        ["8. User Experience & Activation", "Built personas/journeys from Phase 1's real user "
         "group evidence and the actual zoning layout", "Will validate personas against real "
         "community engagement once available"],
        ["9. AI Workflow & Visualization", "Documents itself; generates aerial day/night diagrams "
         "programmatically from the same zoning data used throughout", "Final review and sign-off"],
    ]},
    {"type": "heading", "text": "9.2 Prompt / Direction Strategy"},
    {"type": "para", "text": (
        "Each phase was scoped by an explicit human-provided framework (the 10-phase, "
        "sub-numbered structure used throughout this project) rather than open-ended AI "
        "generation — the AI filled in content within a structure the human defined, and was "
        "explicitly instructed to flag data gaps rather than fabricate figures."
    )},
    {"type": "heading", "text": "9.3 Design Iterations"},
    {"type": "para", "text": (
        "Three concept alternatives were generated and comparatively scored in Phase 4 before "
        "one was selected — this is documented iteration, not a single first-guess output. "
        "The Phase 6 shade-structure geometry was also corrected once during this process: an "
        "initial claim about shadow reach vs. path coverage was checked against the underlying "
        "geometry and revised to be accurate (documented in Phase 6 script comments)."
    )},
    {"type": "heading", "text": "9.4 AI-Assisted Optimization"},
    {"type": "para", "text": (
        "The Phase 5 zoning layout was adjusted once after an initial area-accounting check "
        "showed 46.6% of the site was unaccounted for as unlabeled leftover space — the layout "
        "was revised to properly assign and name that area as circulation/buffer zones, "
        "reducing it to a realistic 21.5% before finalizing the master plan geometry used in "
        "every subsequent phase."
    )},
    {"type": "heading", "text": "9.5 Human Review"},
    {"type": "para", "text": (
        "<b>This entire Phase 2-9 output is explicitly marked as an AI-generated draft "
        "requiring human review</b> before submission, per direct instruction. No claim in "
        "this document set should be treated as final without that review."
    )},
    {"type": "heading", "text": "9.6 Ethical Use of AI"},
    {"type": "para", "text": (
        "Per the Brief (Schedule 1, Section A), AI was used as a design-support tool — for "
        "analysis, drafting, and computation — not as a substitute for professional judgment "
        "or community participation. All data-integrity statements in Phase 1 and the honest "
        "gap-flagging throughout reflect a deliberate choice to avoid presenting AI output as "
        "more authoritative than it is."
    )},
    {"type": "heading", "text": "9.7 Renderings — Aerial (Day / Night)"},
    {"type": "image", "path": os.path.join(RENDER_DIR, "aerial_day.png"),
     "caption": "Figure 1 — Aerial day view, Concept A \"Shaded Spine\".", "width_cm": 17},
    {"type": "image", "path": os.path.join(RENDER_DIR, "aerial_night.png"),
     "caption": "Figure 2 — Aerial night view, illustrative lighting per Phase 6.5.", "width_cm": 17},
    {"type": "heading", "text": "9.7 Renderings — Eye-Level Perspective Views"},
    {"type": "para", "text": (
        "Person's-eye-view perspectives (the brief asks for eye-level views), generated as "
        "one-point-perspective vector renders from the design geometry."
    )},
    {"type": "image", "path": os.path.join(OUT_DIR, "9.7_Renderings", "Eye_Level", "eyelevel_shaded_spine.png"),
     "caption": "Figure 3 — Eye-level view looking down the Shaded Spine (the signature experience).",
     "width_cm": 17},
    {"type": "image", "path": os.path.join(OUT_DIR, "9.7_Renderings", "Eye_Level", "eyelevel_community_plaza.png"),
     "caption": "Figure 4 — Eye-level view standing in the Community Plaza.", "width_cm": 17},
    {"type": "heading", "text": "9.8 Diagrams & 9.9 Presentation Graphics"},
    {"type": "para", "text": (
        "All diagrams across Phases 1, 5, 6, and 7 (SWOT matrix, sun path, shadow direction, "
        "masterplan zoning, circulation, planting plan, section, elevations, shade/water/"
        "carbon/cost/comfort charts) were generated programmatically from real underlying "
        "data. They are assembled into two A1 competition presentation boards:"
    )},
    {"type": "image", "path": os.path.join(OUT_DIR, "9.9_Presentation_Graphics", "presentation_board_1_concept.png"),
     "caption": "Figure 5 — Presentation Board 1: Concept & Master Plan.", "width_cm": 17.5},
    {"type": "image", "path": os.path.join(OUT_DIR, "9.9_Presentation_Graphics", "presentation_board_2_evidence.png"),
     "caption": "Figure 6 — Presentation Board 2: Evidence & Performance.", "width_cm": 17.5},
]

docx_path = build_docx_report(
    output_path=os.path.join(OUT_DIR, "Phase9_AI_Workflow_and_Visualization_Report.docx"),
    phase_tag="PHASE 9 — AI WORKFLOW & VISUALIZATION [AI DRAFT]",
    title="AI Workflow & Visualization",
    subtitle="Al Safa 2 Park — Full-Project AI Methodology & Renderings",
    sections=sections,
    code_ref=code,
    script_name="09_PHASE9_AI_WORKFLOW_AND_VISUALIZATION/_scripts/01_generate_aerial_render.py",
)
convert_docx_to_pdf(docx_path)
