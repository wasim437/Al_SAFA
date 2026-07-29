import os
import sys
import json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "01_PHASE1_EXISTING_PARK", "_scripts"))
from report_builder import build_report

HERE = os.path.dirname(__file__)
OUT_DIR = os.path.join(HERE, "..", "outputs")
SCRIPT_PATH = os.path.join(HERE, "01_generate_masterplan_geometry.py")

with open(os.path.join(OUT_DIR, "zoning_area_schedule.json")) as f:
    schedule = json.load(f)

zone_rows = [[z[0], z[1], f"{z[2]:,.0f} sqm", f"{z[3]}%"] for z in schedule["zones"]]

with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
    code = f.read()

sections = [
    {"type": "para", "text": (
        "<b>AI-GENERATED DRAFT — FOR REVIEW.</b> This master plan implements Concept A "
        "(\"Shaded Spine\", Phase 4.7) as an actual scaled geometric layout — every zone is "
        "sized in real square meters, and the total sums exactly to the Brief's confirmed "
        "15,000 sqm site area. Site proportions (150m x 100m) are an assumed elongated "
        "rectangle consistent with the aerial massing seen in the Phase 1 master-plan "
        "graphic; the exact boundary polygon awaits DWG conversion (logged gap)."
    )},
    {"type": "heading", "text": "5.1 Spatial Framework & 5.2 Functional Zoning"},
    {"type": "image", "path": os.path.join(OUT_DIR, "masterplan_diagram.png"),
     "caption": "Figure 1 — Preliminary Master Plan, Concept A \"Shaded Spine\" (to scale, 15,000 sqm).",
     "width_cm": 17.5},
    {"type": "heading", "text": "Zoning Area Schedule (computed, sums to 15,000 sqm)"},
    {"type": "table", "header": ["Zone", "Category", "Area", "% of Site"], "rows": zone_rows},
    {"type": "heading", "text": "5.3 Circulation"},
    {"type": "table", "header": ["Mode", "Strategy"], "rows": [
        ["Pedestrians", "Primary: 10m-wide Shaded Spine (continuous overhead shade structure) "
         "connecting both entrances. Secondary: perimeter jogging/walking loop (dashed, "
         "~4m inset from boundary) plus cross-links into each activity room."],
        ["Cyclists", "Shared use of the perimeter loop outside peak pedestrian hours; dedicated "
         "cycle parking at both entrance plazas (brief requirement, Section F)."],
        ["Service access", "Via the two entrance plazas, routed behind Commercial & Service "
         "Kiosk Cluster to avoid crossing main pedestrian flows."],
        ["Emergency access", "Both entrance plazas sized (12m x 20m) to permit emergency "
         "vehicle access; Shaded Spine width (10m) accommodates emergency vehicle passage "
         "if required."],
    ]},
    {"type": "heading", "text": "5.4 Activity Areas"},
    {"type": "para", "text": (
        "Active (Children's Play, Outdoor Fitness, Multipurpose Sports Lawn), Passive (Family "
        "Picnic, Quiet Contemplation Garden), Social (Community Plaza & Event Lawn), and Green "
        "(Native Planting/Biodiversity Strip) zones are distributed on both sides of the "
        "Shaded Spine so every activity type has direct shaded access — addressing Phase "
        "2.2's shade-equity problem directly."
    )},
    {"type": "heading", "text": "5.5 Green Network"},
    {"type": "para", "text": (
        "Native Planting/Biodiversity Strip (1,088 sqm) plus two Perimeter Shade Buffers "
        "(1,008 sqm each, north and south edges) total 3,104 sqm of dedicated green "
        "infrastructure (~20.7% of site), rebalancing the existing west-only canopy "
        "concentration identified in Phase 1.02/1.11 into a site-wide green network."
    )},
    {"type": "heading", "text": "5.6 Water Strategy"},
    {"type": "para", "text": (
        "Drip/subsurface irrigation for all planting zones (per Phase 1.05's near-zero summer "
        "rainfall finding); drinking fountains at both entrance plazas and the Community "
        "Plaza; no ornamental water features proposed, consistent with Dubai's water-scarcity "
        "context and the brief's water-sensitive design requirement."
    )},
    {"type": "heading", "text": "5.7 Accessibility"},
    {"type": "para", "text": (
        "100% step-free circulation along the Shaded Spine and all room entries; the "
        "perimeter loop and cross-links are graded for wheelchair/stroller use; both "
        "entrance plazas provide accessible drop-off adjacency — directly resolving Phase "
        "1.10's undocumented-baseline finding with an explicit universal-design commitment."
    )},
    {"type": "heading", "text": "5.8 Safety Strategy"},
    {"type": "para", "text": (
        "Continuous lighting along the Shaded Spine and perimeter loop for night use "
        "(brief requires day/night activation); clear sightlines maintained across each "
        "room (no fully enclosed blind corners); Community Plaza positioned centrally for "
        "natural surveillance from surrounding rooms."
    )},
    {"type": "heading", "text": "5.9 Wayfinding"},
    {"type": "para", "text": (
        "Two legible entrances (west Main Plaza, east Secondary Plaza) with the Shaded Spine "
        "acting as the primary orientation device — from any point on the spine, every room "
        "is a single, short, shaded detour away."
    )},
    {"type": "heading", "text": "5.10 Smart Infrastructure"},
    {"type": "bullets", "items": [
        "Environmental sensors (temperature/shade monitoring) along the Shaded Spine to "
        "validate the Phase 7 shade-performance model against real conditions post-construction.",
        "Smart irrigation controllers tied to soil-moisture sensors in all green zones.",
        "Digital wayfinding kiosks at both entrance plazas.",
    ]},
    {"type": "heading", "text": "Data Integrity Note"},
    {"type": "para", "text": (
        "All areas in the schedule above are computed directly from the geometry defined in "
        "the script below — not estimated by eye. The exact site boundary (vs. this "
        "assumed 150m x 100m rectangle) should be validated once the DWG conversion "
        "(logged in 00_MASTER_TRACKER) is complete."
    )},
]

build_report(
    output_path=os.path.join(OUT_DIR, "..", "Phase5_Masterplan_Development_Report.pdf"),
    phase_tag="PHASE 5 — MASTERPLAN DEVELOPMENT [AI DRAFT]",
    title="Master Plan Development",
    subtitle="Al Safa 2 Park — Concept A \"Shaded Spine\" Implemented as Scaled Geometry",
    sections=sections,
    code_ref=code,
    script_name="05_PHASE5_MASTERPLAN_DEVELOPMENT/_scripts/01_generate_masterplan_geometry.py",
)
