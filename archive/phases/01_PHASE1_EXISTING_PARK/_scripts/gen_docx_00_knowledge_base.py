import os
from docx_report_builder import build_docx_report, convert_docx_to_pdf

HERE = os.path.dirname(__file__)
OUT_DIR = os.path.join(HERE, "..")

sections = [
    {"type": "para", "text": (
        "Compiled: 2026-07-24. This is the master compiled index of Phase 1. It states, "
        "honestly, what is evidence-based vs. what remains a data gap for later resolution. "
        "<b>No design decisions have been made in this phase</b> — Phase 1 is understanding "
        "only, per explicit project instruction."
    )},
    {"type": "heading", "text": "Index of Sub-Analyses"},
    {"type": "table", "header": ["#", "Analysis", "Report File", "Status"], "rows": [
        ["1.01", "Regional Analysis", "Phase1.01_Regional_Analysis_Report.pdf", "Complete (qualitative)"],
        ["1.02", "Urban Context", "Phase1.02_Urban_Context_Report.pdf", "Complete (image-derived)"],
        ["1.03", "Existing Park Analysis", "Phase1.03_Existing_Park_Analysis_Report.pdf", "Partial — DWG pending"],
        ["1.04", "GIS Analysis", "Phase1.04_GIS_Analysis_Report.pdf", "Partial — external GIS data gap"],
        ["1.05", "Climate Analysis", "Phase1.05_Climate_Analysis_Report.pdf", "UPGRADED — sourced Dubai Meteorological Office data + full-year (8,760hr) exact solar dataset"],
        ["1.06", "Shadow Analysis", "Phase1.06_Shadow_Analysis_Report.pdf", "Complete (computed, exact astronomy, 3 key dates)"],
        ["1.07", "Environmental Analysis", "Phase1.07_Environmental_Analysis_Report.pdf", "Partial — soil/stormwater/noise gaps"],
        ["1.08", "Transportation Analysis", "Phase1.08_Transportation_Analysis_Report.pdf", "Partial — bus/parking gaps"],
        ["1.09", "Human Analysis", "Phase1.09_Human_Analysis_Report.pdf", "Complete (brief + manual derived)"],
        ["1.10", "Accessibility Analysis", "Phase1.10_Accessibility_Analysis_Report.pdf", "Complete (baseline = undocumented)"],
        ["1.11", "SWOT + Opportunities/Constraints", "Phase1.11_SWOT_Report.pdf", "Complete (synthesis)"],
        ["1.12", "AI Analysis (methodology log)", "Phase1.12_AI_Analysis_Report.pdf", "Complete"],
        ["1.13", "Catchment & Demand Analysis", "Phase1.13_Catchment_Demand_Analysis_Report.pdf", "NEW — real Dubai Statistics Center 2023 population + computed demand model"],
    ]},
    {"type": "heading", "text": "Headline Facts (verified from competition documents)"},
    {"type": "bullets", "items": [
        "Site: Al Safa 2 Park, 15,000 sqm, Al Safa 2 district, Dubai",
        "Budget: AED 35,000,000 implementation",
        "Context: bounded by Umm Suqeim First, Al Safa Second, Al Manara, Al Qouz Industrial "
        "First (across Sheikh Zayed Road)",
        "Transit: ONPASSIVE Metro Station nearby (across SZR)",
        "Adjacent anchors: Umm Suqeim Model School, Aisha Butti Al Mulla Masjid, Dubai "
        "Physiotherapy & Rehabilitation Center",
        "Climate: Hot desert climate; comfortable season Nov-Apr; extreme heat + near-zero "
        "midday shade May-Oct; prevailing WNW wind (16.7 km/h avg, sourced); near-zero rainfall Jun-Sep",
        "Park archetype (Neighborhood Parks Manual): Neighborhood/community park, 05:00-23:00 "
        "operation, 1-3hr visits, 150-400 visitors/10,000sqm peak capacity benchmark",
    ]},
    {"type": "heading", "text": "Real Data Now Sourced (v3 pass — previously gaps)"},
    {"type": "bullets", "items": [
        "<b>Population / catchment:</b> RESOLVED — real Dubai Statistics Center 2023 figures "
        "(Umm Suqeim 1/2/3 + Al Safa), plus a computed walk-catchment demand model (Phase 1.13).",
        "<b>Wind:</b> RESOLVED — real annual average (16.7 km/h) and dominant direction (WNW) "
        "from Windfinder / Dubai Intl Airport 24-year record (Phase 1.05).",
        "<b>Transit:</b> RESOLVED — ONPASSIVE Station confirmed Red Line, Fare Zone 2, RTA, "
        "formerly \"Al Safa Metro Station\" (Phase 1.08).",
        "<b>Plant specs & water:</b> RESOLVED — real Ghaf irrigation figures drive a computed "
        "~5,700 m³/year park water budget (Phase 6 + Phase 7.4).",
    ]},
    {"type": "heading", "text": "Remaining Data Gaps (still logged, not fabricated)"},
    {"type": "bullets", "items": [
        "As-built DWG geometry (paths, entrances, utilities, levels) — needs DXF conversion",
        "Building density, slope, noise (dB), soil, stormwater capacity data (need GIS layers)",
        "Existing on-site parking/drop-off/cycling counts (need DWG or site visit)",
        "Behavioral/observational user data (movement, dwell time — needs a site study)",
    ]},
    {"type": "para", "text": "These are tracked centrally in 00_MASTER_TRACKER."},
    {"type": "heading", "text": "Real-Data Upgrade Log (2026-07-24, second pass)"},
    {"type": "bullets", "items": [
        "Climate normals replaced: previously a generic published reference; now sourced live "
        "via WebSearch/WebFetch from the <b>Dubai Meteorological Office</b> climate normals "
        "table (Wikipedia \"Climate of Dubai\"), including a genuinely new metric — average "
        "daily sunshine hours — not present in the original analysis.",
        "Solar analysis extended from 3 sample dates to a full <b>8,760-hour, whole-year exact "
        "computation</b> (4,425 confirmed real daylight hours) using the same pvlib/NREL "
        "method, at hourly resolution for every day of 2026.",
        "This full-year dataset was then used to re-run the Phase 7 shade simulation across "
        "every daylight hour of the year (not just 3 snapshots), revealing that while the "
        "Shaded Spine holds 99.2% annual shade coverage, individual activity-room centroids "
        "only get 3.6-16.2% passive shade from the spine/buffer canopy alone — a genuine new "
        "finding that feeds back into Phase 6 planting placement.",
        "World Bank Climate Knowledge Portal was attempted as an additional source but returned "
        "HTTP 403 (bot-blocked) on both the page and its data API — logged as inaccessible, "
        "not silently skipped.",
    ]},
    {"type": "heading", "text": "What Happens Next"},
    {"type": "para", "text": (
        "Phase 2 (Problem Definition) will use this Knowledge Base — specifically the "
        "Weaknesses, Threats, and data-gap items — as its evidence base for identifying the "
        "specific problems the new design must solve. No problem prioritization or design "
        "response happens until Phase 2 is explicitly started."
    )},
]

docx_path = build_docx_report(
    output_path=os.path.join(OUT_DIR, "00_EXISTING_CONDITIONS_KNOWLEDGE_BASE.docx"),
    phase_tag="PHASE 1 — MASTER KNOWLEDGE BASE",
    title="Existing Conditions Knowledge Base",
    subtitle="Al Safa 2 Park — Phase 1 Master Index & Compiled Findings",
    sections=sections,
    code_ref=None,
)
convert_docx_to_pdf(docx_path)
