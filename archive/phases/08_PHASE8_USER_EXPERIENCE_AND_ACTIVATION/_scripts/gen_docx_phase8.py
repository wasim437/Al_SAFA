import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "01_PHASE1_EXISTING_PARK", "_scripts"))
from docx_report_builder import build_docx_report, convert_docx_to_pdf

HERE = os.path.dirname(__file__)
OUT_DIR = os.path.join(HERE, "..")

sections = [
    {"type": "para", "text": (
        "<b>AI-GENERATED DRAFT — FOR REVIEW.</b> Personas and journeys are grounded in the "
        "real user groups from Phase 1.09, the real catchment population from Phase 1.13 "
        "(~7,640 residents within a 10-min walk, Dubai Statistics Center 2023), and the "
        "masterplan zones from Phase 5 — not generic."
    )},
    {"type": "heading", "text": "8.1 User Personas"},
    {"type": "table", "header": ["Persona", "Profile", "Primary Zones Used"], "rows": [
        ["Amina, 34 — parent", "Visits after school pickup from adjacent Umm Suqeim Model School with 2 kids",
         "Children's Play Zone, Family Picnic & Shaded Seating"],
        ["Rashid, 68 — older resident", "Daily evening walk, values shade and seating",
         "Shaded Spine, perimeter jogging loop, Quiet Contemplation Garden"],
        ["Sara, 16 — teenager", "After-school social visit with friends",
         "Community Plaza & Event Lawn, Outdoor Fitness & Wellness"],
        ["Mr. Al Farsi — wheelchair user", "Weekly visit for fresh air and social contact",
         "Shaded Spine (100% step-free per Phase 5.7), Community Plaza"],
        ["Fatima, 29 — fitness enthusiast", "Early morning run before work",
         "Perimeter jogging loop, Outdoor Fitness & Wellness"],
    ]},
    {"type": "heading", "text": "8.2 Daily Use Pattern"},
    {"type": "table", "header": ["Time", "Dominant Activity"], "rows": [
        ["05:00-08:00", "Fitness/jogging (cooler hours, per Phase 1.05 comfort window)"],
        ["08:00-15:00", "Lowest use — peak heat, minimal shade-independent activity expected"],
        ["15:00-18:00", "Family/school pickup traffic — Children's Play Zone peak"],
        ["18:00-23:00", "Community Plaza, evening walking loop, social/teen use (within Manual's 05:00-23:00 operating window)"],
    ]},
    {"type": "heading", "text": "8.3 Seasonal Use"},
    {"type": "para", "text": (
        "Nov-Apr (Phase 1.05 comfort window): full-day use across all zones expected. "
        "May-Oct: use concentrated in the 100%-shaded Shaded Spine and shaded room edges "
        "during midday (per Phase 7.1/7.2 computed coverage), with open lawns (Sports Lawn, "
        "Event Lawn) more viable in early morning/evening only."
    )},
    {"type": "heading", "text": "8.4 Programming"},
    {"type": "para", "text": (
        "Targeting the Neighborhood Parks Manual's benchmark of 60+ small events/year for a "
        "park this size: weekly fitness classes (Outdoor Fitness zone), monthly community "
        "markets (Community Plaza), and seasonal cultural celebrations aligned with UAE "
        "national holidays."
    )},
    {"type": "heading", "text": "8.5 Events"},
    {"type": "para", "text": (
        "Community Plaza & Event Lawn (1,224 sqm, Phase 5 schedule) sized specifically to "
        "host the Manual's benchmark small-to-medium event scale, with permeable paving "
        "(Phase 6.3) selected to support event loading."
    )},
    {"type": "heading", "text": "8.6 Community Interaction"},
    {"type": "para", "text": (
        "Central Community Plaza position (Phase 5.1) places it within natural view of every "
        "surrounding room, supporting incidental social interaction beyond programmed events."
    )},
    {"type": "heading", "text": "8.7 Safety Experience"},
    {"type": "para", "text": (
        "Continuous spine lighting (Phase 6.5) plus natural surveillance from the plaza's "
        "central position (Phase 5.8) support the brief's day/night, all-season safety requirement."
    )},
    {"type": "heading", "text": "8.8 Inclusive Design"},
    {"type": "para", "text": (
        "100% step-free primary circulation (Phase 5.7), poured-in-place rubber play "
        "surfacing (Phase 6.3), and accessible seating every ~30m (Phase 6.6) directly answer "
        "Phase 1.10's undocumented-accessibility-baseline finding with concrete commitments."
    )},
    {"type": "heading", "text": "8.9 Children's Experience"},
    {"type": "para", "text": (
        "Children's Play Zone (1,088 sqm) positioned directly off the Shaded Spine near the "
        "Main Entrance Plaza — shortest, most legible route from arrival to play, with Family "
        "Picnic seating immediately adjacent for parent sightlines."
    )},
    {"type": "heading", "text": "8.10 Visitor Journey Map"},
    {"type": "table", "header": ["Step", "Amina (parent) — Weekday Journey"], "rows": [
        ["1. Arrival", "Enters via Main Entrance Plaza (west) after school pickup"],
        ["2. Orientation", "Shaded Spine visible immediately, provides clear route"],
        ["3. Destination", "Turns into Children's Play Zone (first room off the spine)"],
        ["4. Dwell", "Sits in adjacent Family Picnic & Shaded Seating, maintains sightline to kids"],
        ["5. Departure", "Returns via Shaded Spine to Main Entrance Plaza, fully shaded route both ways"],
    ]},
]

docx_path = build_docx_report(
    output_path=os.path.join(OUT_DIR, "Phase8_User_Experience_and_Activation_Report.docx"),
    phase_tag="PHASE 8 — USER EXPERIENCE & ACTIVATION [AI DRAFT]",
    title="User Experience & Activation",
    subtitle="Al Safa 2 Park — Personas, Daily/Seasonal Use, Programming & Journey Maps",
    sections=sections,
    code_ref=None,
)
convert_docx_to_pdf(docx_path)
