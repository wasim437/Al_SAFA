import os
from docx_report_builder import build_docx_report, convert_docx_to_pdf

HERE = os.path.dirname(__file__)
OUT_DIR = os.path.join(HERE, "..", "10_Accessibility_Analysis", "outputs")
os.makedirs(OUT_DIR, exist_ok=True)

sections = [
    {"type": "heading", "text": "1. Brief Requirements (Schedule 1, Section D)"},
    {"type": "bullets", "items": [
        "Universal design principles; equitable access for all users including People of Determination.",
        "Safe, intuitive, accessible circulation throughout the park.",
        "Consideration of children, youth, families, older adults, People of Determination.",
        "AI/data-driven approaches encouraged to improve accessibility and user experience.",
    ]},
    {"type": "heading", "text": "2. Existing Conditions — What We Can Assess Now"},
    {"type": "table", "header": ["Aspect", "Status"], "rows": [
        ["Wheelchair route continuity", "Unknown — requires DWG path/level data or site visit"],
        ["Stroller/pram usability", "Unknown — same as above"],
        ["Slopes/gradients", "Unknown — requires survey/contour data (may exist in DWG once converted)"],
        ["Wayfinding signage", "Not visible in provided graphic"],
        ["Lighting for safety/visibility", "Not visible in provided graphic"],
        ["Accessible parking/drop-off", "Not confirmed — see Transportation Analysis (1.08) gap"],
        ["Tactile paving / accessible surfacing", "Unknown — requires DWG material layer or site visit"],
    ]},
    {"type": "heading", "text": "3. Honest Baseline Statement"},
    {"type": "para", "text": (
        "There is currently no verified accessibility audit data for the existing Al Safa 2 "
        "Park in the materials provided. This is not unusual for an as-built park predating "
        "explicit universal-design requirements, but it means any claim about the existing "
        "park being accessible or inaccessible would be speculation. The correct, defensible "
        "position for the submission is:"
    )},
    {"type": "para", "text": (
        "\"Existing accessibility conditions could not be fully verified from available "
        "records; the proposed design will be built to full universal-design compliance "
        "regardless of baseline, per the Brief's explicit requirement.\""
    )},
    {"type": "heading", "text": "4. Carry-Forward"},
    {"type": "para", "text": (
        "Accessibility as a design requirement (not existing-condition analysis) belongs in "
        "Phase 3.4 (Project Objectives), Phase 5.7 (Master Plan Accessibility), and Phase 8.8 "
        "(Inclusive Design). This document only establishes the baseline: largely "
        "undocumented, therefore treated as a blank slate requiring full universal-design "
        "application in the new design."
    )},
]

docx_path = build_docx_report(
    output_path=os.path.join(OUT_DIR, "Phase1.10_Accessibility_Analysis_Report.docx"),
    phase_tag="PHASE 1.10 — ACCESSIBILITY ANALYSIS",
    title="Accessibility Analysis",
    subtitle="Al Safa 2 Park — Existing Conditions Baseline (Pre-Design)",
    sections=sections,
    code_ref=None,
)
convert_docx_to_pdf(docx_path)
