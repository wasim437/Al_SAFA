import os
import pandas as pd
from report_builder import build_report

HERE = os.path.dirname(__file__)
OUT_DIR = os.path.join(HERE, "..", "06_Shadow_Analysis", "outputs")
SCRIPT_PATH = os.path.join(HERE, "03_shadow_analysis.py")

df = pd.read_csv(os.path.join(OUT_DIR, "shadow_length_table.csv"))
rows = df.astype(str).values.tolist()

with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
    code = f.read()

sections = [
    {"type": "heading", "text": "1. Purpose"},
    {"type": "para", "text": (
        "This report quantifies exactly where and how far shadows fall on Al Safa 2 Park "
        "across the year, using real solar geometry rather than visual estimation — direct "
        "evidence for later shaded-path and seating placement decisions (not decided here)."
    )},
    {"type": "heading", "text": "2. Method"},
    {"type": "para", "text": (
        "Shadow length = object height &divide; tan(solar elevation angle). Solar elevation and "
        "azimuth were computed exactly for the site's coordinates via pvlib's NREL Solar "
        "Position Algorithm, for three reference object heights (6m tree canopy, 3.5m shade "
        "structure, 1m low wall/planter) at Morning (09:00), Noon (12:00), and Evening (16:00) "
        "on the Summer Solstice, Winter Solstice, and Equinox of 2026."
    )},
    {"type": "heading", "text": "3. Shadow Length Table (full computed dataset)"},
    {"type": "table", "header": list(df.columns), "rows": rows},
    {"type": "spacer", "h_cm": 0.3},
    {"type": "image", "path": os.path.join(OUT_DIR, "chart_shadow_length_comparison.png"),
     "caption": "Figure 1 — Shadow length by object height, season, and time of day.", "width_cm": 17},
    {"type": "image", "path": os.path.join(OUT_DIR, "chart_shadow_direction_plan.png"),
     "caption": "Figure 2 — Shadow direction (plan view) at noon for a 6m tree, across three seasons.",
     "width_cm": 11},
    {"type": "heading", "text": "4. Key Findings"},
    {"type": "bullets", "items": [
        "Summer noon: sun near-zenith (elevation ~88&#176;) &rarr; shadows extremely short "
        "(~0.2m for a 6m tree) &mdash; overhead canopy/shade structures required for midday "
        "summer comfort; low objects provide almost no shade.",
        "Winter noon: sun much lower (elevation ~41&#176;) &rarr; shadows far longer (~6.9m for "
        "a 6m tree) &mdash; walls and vertical elements become effective shade sources.",
        "Morning/evening in all seasons: long shadows from low sun angles (east in morning, "
        "west in evening).",
        "Shadow direction at noon points north in this northern-hemisphere low-latitude site, "
        "swinging from near-overhead (summer) to a clear northward cast (winter).",
    ]},
    {"type": "heading", "text": "5. Design Implications (not decisions — for later phases)"},
    {"type": "bullets", "items": [
        "Overhead/canopy shade (pergolas, tree canopy, shade sails) is essential for summer "
        "midday comfort since low structures cast almost no shadow then.",
        "East-west oriented paths receive natural shade in morning/evening from roadside or "
        "building shadow; north-south paths receive the least shade at those times.",
        "Seating/gathering nodes placed on the north side of tall elements benefit most "
        "consistently across all three seasons.",
    ]},
    {"type": "heading", "text": "6. Data Integrity Statement"},
    {"type": "para", "text": (
        "All shadow lengths and directions in this report are computed directly from exact "
        "solar position astronomy (pvlib / NREL SPA) for the site's real coordinates — none "
        "were estimated visually or by rule of thumb."
    )},
]

build_report(
    output_path=os.path.join(OUT_DIR, "Phase1.06_Shadow_Analysis_Report.pdf"),
    phase_tag="PHASE 1.06 — SHADOW ANALYSIS",
    title="Shadow Analysis",
    subtitle="Al Safa 2 Park, Dubai — Seasonal Shadow Length & Direction (Computed)",
    sections=sections,
    code_ref=code,
    script_name="01_PHASE1_EXISTING_PARK/_scripts/03_shadow_analysis.py",
)
