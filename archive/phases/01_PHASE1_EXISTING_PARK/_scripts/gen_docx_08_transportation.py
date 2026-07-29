import os
from docx_report_builder import build_docx_report, convert_docx_to_pdf

HERE = os.path.dirname(__file__)
OUT_DIR = os.path.join(HERE, "..", "08_Transportation_Analysis", "outputs")
os.makedirs(OUT_DIR, exist_ok=True)

sections = [
    {"type": "heading", "text": "1. Road Hierarchy (from master-plan location image)"},
    {"type": "table", "header": ["Road", "Classification", "Relevance to Site"], "rows": [
        ["Sheikh Zayed Road (E11)", "Primary arterial / national highway",
         "Forms the park's east-side context edge; major barrier and noise source"],
        ["Al Wasl Street", "Secondary arterial", "Runs along the site's north-west side"],
        ["Al Manara Street", "Secondary arterial", "Runs along the south side of the district"],
        ["Local streets (4C, 6C, 6D, 10C/D, 31A, 37A, St 27/35, B29, C14)", "Local/residential access",
         "Provide direct neighborhood access to the park"],
    ]},
    {"type": "heading", "text": "2. Metro (REAL SOURCED — RTA / Dubai Metro)"},
    {"type": "table", "header": ["Attribute", "Value (sourced)"], "rows": [
        ["Station", "ONPASSIVE Metro Station"],
        ["Line", "Dubai Metro Red Line"],
        ["Fare zone", "Zone 2"],
        ["Operator", "Roads & Transport Authority (RTA)"],
        ["Former name", "Al Safa Metro Station (rebranded to ONPASSIVE in Jan 2023)"],
        ["Location", "Along Sheikh Zayed Road, in the Al Safa area"],
        ["Nearby interchange", "Al Quoz Bus Station within walking distance of the metro station"],
    ]},
    {"type": "para", "text": (
        "<b>This is a genuinely significant, now-sourced finding:</b> the station was literally "
        "named after this area (\"Al Safa Metro Station\") — confirming the park sits within "
        "the station's natural catchment. The station is east of the site across Sheikh Zayed "
        "Road; SZR remains a significant pedestrian barrier, so a quality crossing "
        "(bridge/underpass) is the key move to convert this real transit proximity into real "
        "walkable access. (Source: RTA / Dubai Metro data, retrieved via web search 2026-07-24.)"
    )},
    {"type": "heading", "text": "3. Bus, Cycling, Parking, Drop-off, Emergency Access"},
    {"type": "table", "header": ["Mode", "Status"], "rows": [
        ["Bus", "No bus stop locations visible/labeled in provided graphic — data gap, requires RTA route data"],
        ["Cycling", "No dedicated cycle infrastructure visible in surrounding streets"],
        ["Walking", "Typical low-rise-residential walkable block pattern; east-west walkability constrained by SZR"],
        ["Parking", "No existing dedicated park parking visible/confirmed — brief requires this be addressed in the new design"],
        ["Drop-off", "Not confirmed from available materials — pending DWG or site visit"],
        ["Emergency Access", "Not confirmed — DWG (once converted) may show service/emergency routes"],
    ]},
    {"type": "heading", "text": "4. Summary"},
    {"type": "para", "text": (
        "Confirmed context: strong arterial (SZR) and secondary road (Al Wasl, Al Manara) "
        "framing, metro proximity across a highway barrier, walkable residential local-street "
        "access. Genuine gaps: bus routes, existing parking capacity, drop-off zones, cycling "
        "infrastructure, emergency access — all logged for follow-up rather than assumed."
    )},
]

docx_path = build_docx_report(
    output_path=os.path.join(OUT_DIR, "Phase1.08_Transportation_Analysis_Report.docx"),
    phase_tag="PHASE 1.08 — TRANSPORTATION ANALYSIS",
    title="Transportation Analysis",
    subtitle="Al Safa 2 Park — Roads, Metro, Bus, Cycling & Parking Context",
    sections=sections,
    code_ref=None,
)
convert_docx_to_pdf(docx_path)
