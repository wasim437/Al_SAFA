import os
from report_builder import build_report

HERE = os.path.dirname(__file__)
OUT_DIR = os.path.join(HERE, "..", "02_Urban_Context", "outputs")
SCRIPT_PATH = os.path.join(HERE, "01_site_context_extraction.py")

with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
    code = f.read()

sections = [
    {"type": "heading", "text": "1. Purpose"},
    {"type": "para", "text": (
        "This report documents everything around the park &mdash; residential, commercial, "
        "schools, mosques, clinics, metro, roads &mdash; extracted from the official "
        "master-plan location graphic, cross-checked with a Python image-analysis pass."
    )},
    {"type": "heading", "text": "2. Python Image Analysis — Green Footprint Detection"},
    {"type": "para", "text": (
        "A color-threshold script was run on the master-plan graphic to detect the park's "
        "visible green footprint and compute its pixel-based bounding box, as an objective "
        "cross-check on the graphic rather than a manual visual guess."
    )},
    {"type": "image", "path": os.path.join(OUT_DIR, "site_context_footprint_detection.png"),
     "caption": "Figure 1 — Source master-plan graphic (left) and detected green footprint with bounding box (right).",
     "width_cm": 17},
    {"type": "heading", "text": "3. Context Landmarks Identified (from map)"},
    {"type": "bullets", "items": [
        "Al Wasl Street (north-west edge)",
        "Sheikh Zayed Road / E11 (east side, major arterial)",
        "Al Manara Street (south)",
        "ONPASSIVE Metro Station (east, walkable distance across SZR)",
        "Umm Suqeim Model School for Basic Education (adjacent, north-east)",
        "Dubai Physiotherapy & Rehabilitation Center (adjacent, north)",
        "Aisha Butti Al Mulla Masjid (adjacent, south-east)",
    ]},
    {"type": "heading", "text": "4. Neighborhood Context"},
    {"type": "para", "text": (
        "Bounded by: Umm Suqeim First (west), Al Safa Second (north-east), Al Manara (south), "
        "Al Qouz Industrial First (east, across SZR)."
    )},
    {"type": "heading", "text": "5. Site Facts (from Competition Brief, Schedule 1)"},
    {"type": "table", "header": ["Fact", "Value"], "rows": [
        ["Site area", "15,000 sqm (neighborhood park)"],
        ["Location", "Al Safa 2, Dubai"],
        ["Implementation budget", "AED 35,000,000"],
        ["Classification", "District/Community/Neighborhood park archetype"],
    ]},
    {"type": "heading", "text": "6. Note on the CAD File"},
    {"type": "para", "text": (
        "'Al Safa Park 2 Plan (5).dwg' is a binary AutoCAD 2018 (AC1032) file. Full geometric "
        "extraction (exact boundary polygon, layers, existing features) requires conversion to "
        "DXF via ODA File Converter or opening in AutoCAD/BricsCAD. Logged as a pending action "
        "in 00_MASTER_TRACKER."
    )},
]

build_report(
    output_path=os.path.join(OUT_DIR, "Phase1.02_Urban_Context_Report.pdf"),
    phase_tag="PHASE 1.02 — URBAN CONTEXT",
    title="Urban Context Analysis",
    subtitle="Al Safa 2 Park — Surroundings, Landmarks & Site Extraction",
    sections=sections,
    code_ref=code,
    script_name="01_PHASE1_EXISTING_PARK/_scripts/01_site_context_extraction.py",
)
