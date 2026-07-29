import os
from docx_report_builder import build_docx_report, convert_docx_to_pdf

HERE = os.path.dirname(__file__)
OUT_DIR = os.path.join(HERE, "..", "07_Environmental_Analysis", "outputs")
os.makedirs(OUT_DIR, exist_ok=True)

sections = [
    {"type": "heading", "text": "1. Ecology & Biodiversity"},
    {"type": "bullets", "items": [
        "Existing tree canopy (visible west portion of site) is the primary existing "
        "ecological asset — mature trees in Dubai's residential parks are typically Ghaf "
        "(Prosopis cineraria - UAE national tree), Neem, Ficus, and date palm plantings; "
        "species cannot be confirmed without the DWG planting layer or a site visit.",
        "No water bodies visible on site — no aquatic habitat present currently.",
        "As an isolated urban green patch, the park likely functions as a stepping-stone "
        "habitat for birds and urban-tolerant species rather than a primary habitat corridor.",
    ]},
    {"type": "heading", "text": "2. Water"},
    {"type": "para", "text": (
        "No existing water features identified. Dubai's water context (Climate Analysis, "
        "Phase 1.05): near-zero rainfall Jun-Sep, light rainfall Dec-Feb (~15-23mm/month) — "
        "any landscape strategy must assume irrigation-dependent planting, reinforcing the "
        "brief's call for water-sensitive design and sustainable irrigation."
    )},
    {"type": "heading", "text": "3. Vegetation"},
    {"type": "para", "text": (
        "Visible canopy concentration = west side of site; east side reads more open/hardscape "
        "in the aerial graphic. This asymmetry is a genuine existing condition worth carrying "
        "into Phase 2 as a potential shade-equity issue."
    )},
    {"type": "heading", "text": "4-8. Soil, Stormwater, Carbon, Habitat, Air, Noise, Visual Corridors"},
    {"type": "table", "header": ["Aspect", "Status"], "rows": [
        ["Soil", "No geotechnical data provided; regional assumption only (calcareous sandy soils typical of Dubai) — logged as gap"],
        ["Stormwater", "No infrastructure data available (sits in DWG utilities layer, pending conversion)"],
        ["Carbon", "No baseline data; would need modeling once species/quantities known"],
        ["Habitat", "Likely supports common urban bird species; no formal survey data"],
        ["Noise", "Sheikh Zayed Road (E11) borders east edge — confirmed major noise source requiring acoustic buffering"],
        ["Air", "No air quality monitoring data for this specific site; SZR proximity is a qualitative concern"],
        ["Visual Corridors", "No confirmed skyline sightline data for this specific site; internal circular plaza appears to be a potential focal point (unconfirmed function)"],
    ]},
    {"type": "heading", "text": "9. Summary of Data Status"},
    {"type": "para", "text": (
        "Most items above are qualitative/contextual reads from the one available graphic plus "
        "regional climate knowledge. Quantitative/scientific data (soil tests, stormwater "
        "capacity, noise dB readings, carbon baselines, biodiversity surveys) require sources "
        "not included in the competition package and are logged as gaps in 00_MASTER_TRACKER."
    )},
]

docx_path = build_docx_report(
    output_path=os.path.join(OUT_DIR, "Phase1.07_Environmental_Analysis_Report.docx"),
    phase_tag="PHASE 1.07 — ENVIRONMENTAL ANALYSIS",
    title="Environmental Analysis",
    subtitle="Al Safa 2 Park — Ecology, Water, Vegetation, Soil, Stormwater & Noise",
    sections=sections,
    code_ref=None,
)
convert_docx_to_pdf(docx_path)
