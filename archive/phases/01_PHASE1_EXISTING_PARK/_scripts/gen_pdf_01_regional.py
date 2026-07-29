import os
from report_builder import build_report

HERE = os.path.dirname(__file__)
OUT_DIR = os.path.join(HERE, "..", "01_Regional_Analysis", "outputs")
os.makedirs(OUT_DIR, exist_ok=True)

sections = [
    {"type": "heading", "text": "1. Scale Progression Studied"},
    {"type": "para", "text": "Dubai &rarr; District &rarr; Neighborhood &rarr; Park"},

    {"type": "heading", "text": "2. Dubai-Wide Context"},
    {"type": "bullets", "items": [
        "The site sits within Dubai's established low-rise residential belt west of Sheikh "
        "Zayed Road (Al Safa, Al Wasl, Umm Suqeim, Jumeirah) &mdash; one of the city's oldest "
        "planned neighborhood clusters.",
        "Dubai Municipality's own Neighborhood Parks Manual classifies this typology as a "
        "District/Community/Neighbourhood park: primarily for nearby residents, operating "
        "05:00&ndash;23:00, all seasons.",
    ]},
    {"type": "table", "header": ["Density Band", "Park Area Range (sqm)"], "rows": [
        ["High (>220 person/ha)", "3,000 &ndash; 150,000"],
        ["Medium (70&ndash;220 person/ha)", "3,500 &ndash; 300,000"],
        ["Low (<70 person/ha)", "4,000 &ndash; 500,000"],
    ]},
    {"type": "para", "text": (
        "<b>Al Safa 2 Park = 15,000 sqm</b>, placing it in the neighborhood-scale band "
        "regardless of density tier — consistent with the low-rise villa/townhouse context."
    )},

    {"type": "heading", "text": "3. District Level"},
    {"type": "para", "text": (
        "From the official master-plan location graphic, the park sits at the convergence of "
        "four named districts: <b>Umm Suqeim First</b> (west), <b>Al Safa Second</b> "
        "(north-east), <b>Al Manara</b> (south), and <b>Al Qouz Industrial First</b> (east, "
        "across Sheikh Zayed Road / E11)."
    )},

    {"type": "heading", "text": "4. Neighborhood Level"},
    {"type": "bullets", "items": [
        "Umm Suqeim Model School for Basic Education (NE, walking distance)",
        "Dubai Physiotherapy & Rehabilitation Center (N, adjacent)",
        "Aisha Butti Al Mulla Masjid (SE, adjacent)",
        "Local street grid: 4C, 6C, 6D, 10C/D, 31A, 37A, Streets 27/35, B29, C14",
        "ONPASSIVE Metro Station across Sheikh Zayed Road to the east",
    ]},

    {"type": "heading", "text": "5. Real Population & Catchment (Dubai Statistics Center, 2023)"},
    {"type": "para", "text": (
        "The surrounding communities' populations are now sourced from real data (Dubai "
        "Statistics Center 2023 Population Bulletin), replacing the earlier data gap:"
    )},
    {"type": "table", "header": ["Community", "Residents (2023)"], "rows": [
        ["Umm Suqeim First (356)", "7,443"],
        ["Umm Suqeim Second (362)", "9,220"],
        ["Umm Suqeim Third (366)", "4,867"],
        ["Al Safa", "16,986 (density 3,800/km²)"],
    ]},
    {"type": "para", "text": (
        "A full walk-catchment demand model built on this real data is provided as its own "
        "report: <b>Phase1.13_Catchment_Demand_Analysis</b>. Headline: ~7,640 residents live "
        "within a 10-minute (800m) walk, and estimated peak concurrent demand (~169 visitors) "
        "fits within the Neighborhood Parks Manual's 225-600 capacity benchmark for a 15,000 "
        "sqm park."
    )},

    {"type": "heading", "text": "6. Park Level"},
    {"type": "para", "text": (
        "15,000 sqm neighborhood park, existing and slated for full redevelopment. Per the "
        "Neighborhood Parks Manual's benchmark for this archetype: target users are families, "
        "sport enthusiasts, picnickers, teenagers, and pet owners; typical visit duration "
        "1&ndash;3 hours; peak visitor capacity 150&ndash;400 visitors per 10,000 sqm."
    )},

    {"type": "heading", "text": "7. Regional Network Items — Data Status"},
    {"type": "table", "header": ["Item", "Status"], "rows": [
        ["Service radius / catchment population", "✅ NOW SOURCED — Dubai Statistics Center 2023 (see Phase 1.13)"],
        ["Major roads", "✅ Available — SZR (E11), Al Wasl St, Al Manara St"],
        ["Metro", "✅ SOURCED — ONPASSIVE Station, Red Line, Fare Zone 2 (see Phase 1.08)"],
        ["Green network (linkage to other Dubai parks)", "Not available — requires Dubai Municipality GIS layer"],
        ["Urban growth trend", "Not available — requires Dubai 2040 Urban Master Plan data"],
    ]},
    {"type": "para", "text": (
        "Remaining \"Not available\" items require GIS layers not in the competition files, "
        "logged in <b>00_MASTER_TRACKER</b> — not fabricated here."
    )},
]

build_report(
    output_path=os.path.join(OUT_DIR, "Phase1.01_Regional_Analysis_Report.pdf"),
    phase_tag="PHASE 1.01 — REGIONAL ANALYSIS",
    title="Regional Analysis",
    subtitle="Al Safa 2 Park — Dubai → District → Neighborhood → Park",
    sections=sections,
    code_ref=None,
)
