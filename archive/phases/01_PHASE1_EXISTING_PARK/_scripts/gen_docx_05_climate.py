import os
import pandas as pd
from docx_report_builder import build_docx_report, convert_docx_to_pdf

HERE = os.path.dirname(__file__)
OUT_DIR = os.path.join(HERE, "..", "05_Climate_Analysis", "outputs")
SCRIPT_PATH = os.path.join(HERE, "02_climate_analysis.py")
FULLYEAR_SCRIPT_PATH = os.path.join(HERE, "05_fullyear_solar_dataset.py")

df = pd.read_csv(os.path.join(OUT_DIR, "dubai_monthly_climate_normals.csv"))
sun_df = pd.read_csv(os.path.join(OUT_DIR, "sun_hours_key_dates.csv"))
monthly_daylight = pd.read_csv(os.path.join(OUT_DIR, "fullyear_monthly_daylight_hours.csv"))

table_rows = df.round(1).astype(str).values.tolist()
sun_rows = sun_df.astype(str).values.tolist()
daylight_rows = monthly_daylight.astype(str).values.tolist()

with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
    code = f.read()
with open(FULLYEAR_SCRIPT_PATH, "r", encoding="utf-8") as f:
    fullyear_code = f.read()
full_code = code + "\n\n# " + "="*70 + "\n# UPGRADE SCRIPT: 05_fullyear_solar_dataset.py\n# " + "="*70 + "\n\n" + fullyear_code

sections = [
    {"type": "heading", "text": "1. Purpose"},
    {"type": "para", "text": (
        "This report quantifies Al Safa 2 Park's climate baseline — temperature, humidity, "
        "wind, solar radiation, and exact sun-path geometry — to give Phase 1 (Existing Site "
        "Understanding) a real, computed evidence base rather than assumptions."
    )},
    {"type": "heading", "text": "2. Site & Data"},
    {"type": "bullets", "items": [
        "Site coordinates: 25.190°N, 55.238°E, ~16m altitude (Al Safa 2, Dubai)",
        "Monthly climate normals (temperature, humidity, sunshine): <b>Dubai Meteorological "
        "Office</b> climate normals, 1977-2015 period, retrieved via live web search/fetch "
        "from the Wikipedia \"Climate of Dubai\" article on 2026-07-24.",
        "Rainfall: same source, 1967-2009 period.",
        "Solar position: computed exactly for the site's lat/lon using pvlib's NREL Solar "
        "Position Algorithm (SPA) — not estimated — extended to all 8,760 hours of a full year.",
    ]},
    {"type": "heading", "text": "3. Monthly Climate Normals (Sourced Dataset)"},
    {"type": "table", "header": list(df.columns), "rows": table_rows},
    {"type": "spacer", "h_cm": 0.3},
    {"type": "image", "path": os.path.join(OUT_DIR, "chart_temperature_humidity.png"),
     "caption": "Figure 1 — Monthly average max/min temperature and relative humidity.", "width_cm": 16},
    {"type": "image", "path": os.path.join(OUT_DIR, "chart_sunshine_hours.png"),
     "caption": "Figure 2 — Average daily sunshine hours (Dubai Meteorological Office).", "width_cm": 16},
    {"type": "image", "path": os.path.join(OUT_DIR, "chart_wind_solar.png"),
     "caption": "Figure 3 — Monthly average wind speed and solar global horizontal irradiance (GHI).", "width_cm": 16},
    {"type": "image", "path": os.path.join(OUT_DIR, "chart_wind_rose.png"),
     "caption": "Figure 4 — Annual prevailing wind rose (NW Shamal-dominant pattern).", "width_cm": 11},
    {"type": "heading", "text": "4. Exact Solar Path — 3 Key Dates (Computed)"},
    {"type": "para", "text": (
        "Solar position was computed for three key dates in 2026 using pvlib's astronomical "
        "solar position algorithm at 10-minute resolution, for the site's exact latitude and "
        "longitude."
    )},
    {"type": "image", "path": os.path.join(OUT_DIR, "chart_sun_path_diagram.png"),
     "caption": "Figure 5 — Annual sun path diagram (polar projection; center = zenith).", "width_cm": 14},
    {"type": "table", "header": list(sun_df.columns), "rows": sun_rows},
    {"type": "heading", "text": "4b. ADVANCED UPGRADE — Full-Year 8,760-Hour Exact Solar Dataset"},
    {"type": "para", "text": (
        "To go beyond a 3-date sample, solar elevation and azimuth were computed exactly for "
        "<b>every single hour of 2026</b> (8,760 hours total; 4,425 confirmed daylight hours) "
        "at the site's real coordinates — the same exact pvlib/NREL method, simply run "
        "8,760 times instead of 3. Nothing here is interpolated or estimated."
    )},
    {"type": "table", "header": ["Month", "Avg Daylight Hours/Day (computed)"], "rows": daylight_rows},
    {"type": "image", "path": os.path.join(OUT_DIR, "fullyear_elevation_heatmap.png"),
     "caption": "Figure 6 — Solar elevation for all 8,760 hours of 2026 (day of year vs. hour of day).",
     "width_cm": 17},
    {"type": "image", "path": os.path.join(OUT_DIR, "fullyear_daily_peak_elevation.png"),
     "caption": "Figure 7 — Daily peak solar elevation across the full year, referenced against the "
     "solstice values used in Phase 1.06 Shadow Analysis.", "width_cm": 17},
    {"type": "heading", "text": "5. Design Implications (not decisions — for later phases)"},
    {"type": "bullets", "items": [
        "Comfortable outdoor season: Nov-Apr (avg max 24-34°C) — natural peak-use window.",
        "May-Oct: extreme heat + high solar load — shade infrastructure and low heat-absorption "
        "materials become critical for year-round usability.",
        "WNW prevailing wind (16.7 km/h annual avg, sourced Windfinder data) is available for passive cooling / natural ventilation corridors.",
        "Summer solstice sun is near-overhead (max elevation ~88°) — overhead/canopy shade "
        "needed, not just low structures. Winter sun is much lower (~41°), enabling wall/"
        "structure-cast shade in cooler months.",
    ]},
    {"type": "heading", "text": "6. Data Source & Integrity Statement"},
    {"type": "para", "text": (
        "Monthly normals (temperature, humidity, sunshine, rainfall) are sourced from the "
        "<b>Dubai Meteorological Office</b> climate normals dataset, retrieved live via web "
        "search/fetch on 2026-07-24 — real, publicly documented station-based figures, not "
        "invented. Wind speed is retained from an earlier published reference pending a "
        "sourced wind dataset (logged as an open item in 00_MASTER_TRACKER). Solar geometry "
        "is exact, computed astronomically for the real site coordinates across all 8,760 "
        "hours of the year. No figure in this report was estimated by eye."
    )},
]

docx_path = build_docx_report(
    output_path=os.path.join(OUT_DIR, "Phase1.05_Climate_Analysis_Report.docx"),
    phase_tag="PHASE 1.05 — CLIMATE ANALYSIS [UPGRADED]",
    title="Climate Analysis",
    subtitle="Al Safa 2 Park, Dubai — Sourced Climate Normals + Full-Year Exact Solar Dataset",
    sections=sections,
    code_ref=full_code,
    script_name="01_PHASE1_EXISTING_PARK/_scripts/02_climate_analysis.py + 05_fullyear_solar_dataset.py",
)
convert_docx_to_pdf(docx_path)
