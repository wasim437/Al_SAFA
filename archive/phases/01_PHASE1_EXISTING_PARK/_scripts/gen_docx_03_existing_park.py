import os
from docx_report_builder import build_docx_report, convert_docx_to_pdf

HERE = os.path.dirname(__file__)
OUT_DIR = os.path.join(HERE, "..", "03_Existing_Park_Analysis", "outputs")
os.makedirs(OUT_DIR, exist_ok=True)

sections = [
    {"type": "heading", "text": "1. Data Sources Available"},
    {"type": "bullets", "items": [
        "Ai Park - Master Plan (4).jpg — aerial/graphic location map (schematic level only)",
        "Al Safa Park 2 Plan (5).dwg — as-built AutoCAD drawing (AC1032 binary format)",
        "Competition Brief, Schedule 1 & Appendix (Schedule 8) references",
    ]},
    {"type": "heading", "text": "2. What We Can Confirm Visually"},
    {"type": "bullets", "items": [
        "Park footprint is an elongated rectangular plot oriented roughly NW-SE, fronting a "
        "service road off Al Wasl Street.",
        "Visible tree canopy clusters concentrated toward the site's western portion; more "
        "open/hardscape appearance toward the east.",
        "A circular plaza/hub feature is visible near the park's approximate center (exact use "
        "unconfirmed).",
        "Single primary pedestrian access point visible on the west edge; extent of secondary "
        "access is not legible at this graphic's resolution.",
    ]},
    {"type": "heading", "text": "3. What Requires the DWG (Not Yet Extracted)"},
    {"type": "para", "text": (
        "The as-built DWG is a binary AutoCAD 2018 (AC1032) file. Python's open-source DXF "
        "tooling (ezdxf) cannot parse binary DWG directly — it requires either the free ODA "
        "File Converter (opendesign.com) to convert DWG→DXF, or opening directly in "
        "AutoCAD / BricsCAD / DraftSight."
    )},
    {"type": "para", "text": "Pending extraction, this file should yield:"},
    {"type": "bullets", "items": [
        "Exact site boundary polygon & precise area (validate the stated 15,000 sqm)",
        "Existing entrances (count, location, width)",
        "Path/track network (alignment, width, surfacing)",
        "Existing tree/planting locations and species (if labeled)",
        "Existing hardscape: plazas, seating, play equipment footprints",
        "Existing lighting poles, furniture, signage (if drawn)",
        "Existing utilities/services (drainage, irrigation, electrical) if included as a layer",
        "Existing buildings/structures (kiosks, restrooms, maintenance)",
        "Levels/contours (if a survey layer exists)",
    ]},
    {"type": "heading", "text": "4. Existing Park Inventory Checklist (status)"},
    {"type": "table", "header": ["Element", "Status", "Notes"], "rows": [
        ["Entrances", "Pending DWG", "1 visible in master-plan graphic (west side)"],
        ["Paths", "Pending DWG", "Schematic path visible; no width/surface data"],
        ["Trees", "Pending DWG", "Canopy massing visible west side; no species/count"],
        ["Grass/lawn", "Pending DWG", "General green area visible; no exact sqm"],
        ["Lighting", "Not available", "No lighting layer visible"],
        ["Furniture", "Not available", "Not legible at graphic resolution"],
        ["Playground", "Not available", "Not clearly identifiable"],
        ["Sports facilities", "Not available", "Not clearly identifiable"],
        ["Utilities", "Not available", "Requires DWG utility layer"],
        ["Water features", "Not available", "None visible"],
        ["Buildings/structures", "Partially visible", "Central plaza feature, function unconfirmed"],
        ["Landscape character", "Partial", "Tree-dense west / open east (aerial impression)"],
        ["Maintenance condition", "Not available", "Requires site visit/photos"],
        ["Accessibility features", "Not available", "Requires DWG or site visit"],
    ]},
    {"type": "heading", "text": "5. Action Logged"},
    {"type": "para", "text": (
        "Conversion of Al Safa Park 2 Plan (5).dwg to DXF is logged as an open task in "
        "00_MASTER_TRACKER. Once available, this document should be re-run/updated with "
        "confirmed geometry rather than visual estimation."
    )},
]

docx_path = build_docx_report(
    output_path=os.path.join(OUT_DIR, "Phase1.03_Existing_Park_Analysis_Report.docx"),
    phase_tag="PHASE 1.03 — EXISTING PARK ANALYSIS",
    title="Existing Park Analysis",
    subtitle="Al Safa 2 Park — Existing Conditions Inventory",
    sections=sections,
    code_ref=None,
)
convert_docx_to_pdf(docx_path)
