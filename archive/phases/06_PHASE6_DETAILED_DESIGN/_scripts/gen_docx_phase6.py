import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "01_PHASE1_EXISTING_PARK", "_scripts"))
from docx_report_builder import build_docx_report, convert_docx_to_pdf

HERE = os.path.dirname(__file__)
OUT_DIR = os.path.join(HERE, "..", "outputs")
SCRIPT_PATH = os.path.join(HERE, "01_generate_section.py")

with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
    code = f.read()
with open(os.path.join(OUT_DIR, "section_shade_performance.txt")) as f:
    shade_txt = f.read()

sections = [
    {"type": "para", "text": (
        "<b>AI-GENERATED DRAFT — FOR REVIEW.</b> Technical development of Concept A "
        "(\"Shaded Spine\") into real planting species, materials, and a scaled section "
        "drawing with shade performance validated against Phase 1.06's computed solar data."
    )},
    {"type": "heading", "text": "6.1 Planting Strategy — Species Palette (real UAE-native/adapted species)"},
    {"type": "table", "header": ["Zone", "Species (Common / Botanical)", "Role"], "rows": [
        ["Native Planting / Biodiversity Strip", "Ghaf (Prosopis cineraria) — UAE national tree",
         "Primary native canopy tree; deep-rooted, drought-tolerant, habitat value"],
        ["Perimeter Shade Buffers", "Neem (Azadirachta indica), Date Palm (Phoenix dactylifera)",
         "Fast-establishing shade + local cultural/edible-landscape identity"],
        ["Shaded Spine edges", "Ficus nitida (Indian Laurel), underplanted with Lantana (Lantana camara)",
         "Reinforces the spine's shaded, continuous canopy feel at path edge"],
        ["Community Plaza perimeter", "Bougainvillea spectabilis, Conocarpus lancifolius (Damas)",
         "Color/seasonal interest + fast screening for plaza edges"],
        ["Quiet Contemplation Garden", "Olive (Olea europaea), ornamental grasses (Pennisetum spp.)",
         "Low-water, sensory, calm palette for passive/quiet use"],
        ["Multipurpose Sports Lawn", "Paspalum vaginatum (seashore paspalum)",
         "Salt- and heat-tolerant turf suited to Dubai's irrigation water quality"],
    ]},
    {"type": "heading", "text": "6.1b Ghaf (Prosopis cineraria) — Real Sourced Specifications"},
    {"type": "para", "text": (
        "The primary native canopy species is specified using real horticultural data "
        "(retrieved via web search 2026-07-24 from UAE nursery/botanical sources and a "
        "peer-reviewed Abu Dhabi irrigation field study):"
    )},
    {"type": "table", "header": ["Attribute", "Real Value"], "rows": [
        ["Mature height", "4-10 m (can reach 25 m in ideal conditions)"],
        ["Canopy spread", "3-5 m, rounded/spreading habit"],
        ["Irrigation (established)", "24.4 L/day/tree (Jan) to 52.8 L/day/tree (Jul) — field-study measured"],
        ["Drought tolerance", "High (thrives below 500 mm annual rainfall — Dubai gets ~95 mm)"],
        ["Salinity tolerance", "High (irrigable with saline groundwater per field study)"],
        ["Sun / wind tolerance", "High / High — nitrogen-fixing, improves soil"],
        ["Status", "UAE national tree; native to the Arabian Peninsula"],
    ]},
    {"type": "para", "text": (
        "These real figures directly feed the Phase 7 water-demand model, which computes the "
        "park's full annual irrigation budget (~5,700 m³/year) from them — not from guesses."
    )},
    {"type": "heading", "text": "6.1c Planting Plan (code-generated, to scale)"},
    {"type": "para", "text": (
        "The species above are placed at specific locations across the site. Critically, the "
        "canopy trees are concentrated INSIDE the activity rooms that the Phase 7 annual-shade "
        "simulation flagged as lowest-shade (Children's Play 3.6%, Sports Lawn 4.3%, Fitness "
        "4.6%) — directly closing that gap. 131 trees total."
    )},
    {"type": "image", "path": os.path.join(OUT_DIR, "planting_plan.png"),
     "caption": "Figure 1 — Planting Plan: species placement with canopy footprints; priority "
     "trees inside the lowest-shade rooms.", "width_cm": 17.5},
    {"type": "heading", "text": "6.2 Landscape Strategy"},
    {"type": "para", "text": (
        "Planting is concentrated to correct the shade-equity gap identified in Phase 1.11 "
        "(existing canopy was west-only) — the Native Planting Strip and both Perimeter "
        "Shade Buffers together add roughly 3,100 sqm of new green infrastructure distributed "
        "along the full length of the site (see Phase 5 zoning schedule)."
    )},
    {"type": "heading", "text": "6.3 / 6.4 Hardscape & Softscape"},
    {"type": "table", "header": ["Surface", "Material", "Rationale"], "rows": [
        ["Shaded Spine path", "Light-toned permeable concrete pavers", "Low heat absorption vs. dark asphalt; permeable for irrigation runoff"],
        ["Entrance plazas", "Local sandstone-tone porcelain pavers", "Durable, reflects rather than absorbs solar heat, celebrates local material tone"],
        ["Perimeter jogging loop", "Resin-bound rubber running surface", "Joint-friendly surface for the Manual's fitness/wellness benchmark activity"],
        ["Community Plaza", "Permeable interlocking concrete", "Supports event loading (Manual benchmark: 60+ small events/yr) while draining rainfall"],
        ["Play zone surfacing", "Poured-in-place rubber safety surfacing", "Universal-design and child-safety compliant, per Brief Section D"],
    ]},
    {"type": "heading", "text": "6.5 Lighting Concept"},
    {"type": "para", "text": (
        "Continuous LED strip lighting integrated into the Shaded Spine canopy structure "
        "(addresses Phase 1.10's undocumented lighting gap directly); pole lighting along the "
        "perimeter loop at 25m spacing for even nighttime coverage; low-level bollard lighting "
        "in the Quiet Contemplation Garden to preserve its calmer night character."
    )},
    {"type": "heading", "text": "6.6 Furniture Strategy"},
    {"type": "bullets", "items": [
        "Modular shaded seating clusters at every room's spine-facing edge",
        "Family-sized picnic tables (Family Picnic zone)",
        "Accessible seating (armrests, back support) distributed every ~30m along the spine",
        "Bicycle racks at both entrance plazas",
    ]},
    {"type": "heading", "text": "6.7 Materials Palette Summary"},
    {"type": "para", "text": (
        "Warm sand/stone tones throughout, selected for low solar heat gain and visual "
        "consistency with the surrounding Al Safa/Umm Suqeim low-rise residential material "
        "language — avoiding dark, heat-absorptive surfaces given the extreme summer solar "
        "load quantified in Phase 1.05."
    )},
    {"type": "heading", "text": "6.8 Key Section — Shaded Spine (Section A-A)"},
    {"type": "image", "path": os.path.join(OUT_DIR, "section_shaded_spine.png"),
     "caption": "Figure 2 — Section A-A through the Shaded Spine, with real computed summer/winter "
     "solar angles from Phase 1.06 overlaid.", "width_cm": 17},
    {"type": "para", "text": shade_txt.replace("\n", "<br/>")},
    {"type": "heading", "text": "6.9 Elevations"},
    {"type": "para", "text": (
        "Two key elevations are drawn to scale, consistent with the master plan and the "
        "Section A-A geometry above."
    )},
    {"type": "image", "path": os.path.join(OUT_DIR, "elevation_entrance_gateway.png"),
     "caption": "Figure 3 — Elevation 1: Main Entrance Gateway (~10m span, 4.5m portal height).",
     "width_cm": 16},
    {"type": "image", "path": os.path.join(OUT_DIR, "elevation_shaded_spine_long.png"),
     "caption": "Figure 4 — Elevation 2: Shaded Spine canopy, showing a 60m run of the 126m "
     "continuous structure (6m column bays, 5.5m clearance).", "width_cm": 17},
    {"type": "heading", "text": "6.10 Key Detail Concepts"},
    {"type": "para", "text": (
        "Canopy-to-column connection uses a slatted profile (visible in Figure 2) rather than "
        "a fully solid roof, allowing some diffuse light and the WNW prevailing breeze "
        "(Phase 1.05) to pass through while still blocking direct summer solar radiation."
    )},
]

docx_path = build_docx_report(
    output_path=os.path.join(OUT_DIR, "..", "Phase6_Detailed_Design_Report.docx"),
    phase_tag="PHASE 6 — DETAILED DESIGN [AI DRAFT]",
    title="Detailed Design",
    subtitle="Al Safa 2 Park — Planting, Materials & Section Development",
    sections=sections,
    code_ref=code,
    script_name="06_PHASE6_DETAILED_DESIGN/_scripts/01_generate_section.py",
)
convert_docx_to_pdf(docx_path)
