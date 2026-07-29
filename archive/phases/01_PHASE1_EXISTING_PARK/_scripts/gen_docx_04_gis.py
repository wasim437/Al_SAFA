import os
from docx_report_builder import build_docx_report, convert_docx_to_pdf

HERE = os.path.dirname(__file__)
OUT_DIR = os.path.join(HERE, "..", "04_GIS_Analysis", "outputs")
os.makedirs(OUT_DIR, exist_ok=True)

sections = [
    {"type": "heading", "text": "1. Status Overview"},
    {"type": "para", "text": (
        "Professional GIS analysis (land use, building density, connectivity, slope, "
        "visibility, heat, noise, green coverage, service radius, walkability) normally "
        "requires authoritative datasets: Dubai Municipality GIS portal layers, satellite/"
        "aerial imagery, a DEM, and population/land-use shapefiles. <b>None of these raw "
        "datasets were included in the competition files provided</b> (only a JPG location "
        "graphic, a PDF brief, a DWG as-built, and a park design manual PDF). This document "
        "records what can legitimately be assessed now vs. what is a logged data gap."
    )},
    {"type": "heading", "text": "2. Assessable Now (from provided materials)"},
    {"type": "table", "header": ["Layer", "Finding", "Source"], "rows": [
        ["Land Use (qualitative)", "Low-rise residential surrounds park on 3 sides; SZR + "
         "Al Qouz Industrial on 4th (east) side", "Master-plan location image"],
        ["Connectivity (qualitative)", "Local street grid feeds the park; SZR is a hard edge/"
         "barrier on the east", "Master-plan location image"],
        ["Green Coverage (approx.)", "~0.94% of the reviewed graphic's frame flagged as "
         "green-toned pixels via color-threshold script — a rough visual proxy only, not "
         "survey-grade canopy measurement", "Python image analysis (Phase 1.02)"],
        ["Walkability (qualitative)", "Park is walkable from surrounding residential streets; "
         "crossing SZR to reach metro/Al Qouz side is not pedestrian-friendly", "Contextual reading"],
    ]},
    {"type": "heading", "text": "3. Logged Data Gaps (require external GIS sourcing)"},
    {"type": "table", "header": ["Layer", "Requirement"], "rows": [
        ["Building Density", "Dubai Municipality building footprint GIS layer"],
        ["Slope", "Site DEM / survey contours (may exist inside the DWG once converted)"],
        ["Visibility analysis", "Requires 3D massing model of surrounding buildings"],
        ["Heat (urban heat island)", "Requires satellite thermal imagery (e.g., Landsat/Sentinel thermal bands)"],
        ["Noise", "Requires traffic count data for SZR + acoustic modeling"],
        ["Service radius / catchment", "Requires population density GIS layer for accurate isochrone modeling"],
    ]},
    {"type": "heading", "text": "4. Recommendation"},
    {"type": "para", "text": (
        "If genuine GIS rigor is required for the submission, the highest-value next step is: "
        "(1) convert the as-built DWG to DXF to recover any survey/contour layer; (2) "
        "optionally pull free satellite imagery for a heat/greenery cross-check — technically "
        "feasible with Python but requires external API access/credentials not yet confirmed."
    )},
    {"type": "para", "text": (
        "This keeps the analysis honest: qualitative/contextual GIS reading is complete; "
        "quantitative GIS layers remain flagged as pending real data, not fabricated."
    )},
]

docx_path = build_docx_report(
    output_path=os.path.join(OUT_DIR, "Phase1.04_GIS_Analysis_Report.docx"),
    phase_tag="PHASE 1.04 — GIS ANALYSIS",
    title="GIS Analysis",
    subtitle="Al Safa 2 Park — Professional GIS Layer Review & Data Gap Log",
    sections=sections,
    code_ref=None,
)
convert_docx_to_pdf(docx_path)
