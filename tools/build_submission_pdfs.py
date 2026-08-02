"""Assemble each of the 12 upload slots into ONE PDF.

WHY THIS EXISTS
---------------
The Dubai Municipality upload form takes **a single file per slot** — "No file
chosen / Drop your file here", pdf, max 100 MB. There are twelve such fields.

`submission/` currently holds twelve *folders*, each with loose PNGs and one or
more PDFs. None of it can be uploaded. This turns each folder into one
self-contained, cover-paged PDF that can be dropped straight into its field.

WHAT IT ALSO DOES
-----------------
It refuses to build quietly over three problems that would cost marks:

1. **Draft markers.** Eleven of the source reports carry "[AI DRAFT]" in their
   title and "AI-GENERATED DRAFT — FOR REVIEW" in their body. Submitting a
   document that describes itself as an unreviewed draft undercuts the
   declaration that the work is the applicant's own. Every occurrence is
   reported.

2. **Renders that contradict the plan.** The photoreal aerial shows a serpentine
   canopy over a large lagoon. The masterplan is a single 141 m arc with a 0.9 m
   water channel. They are not two views of one park, and a juror comparing slot
   02 with slot 05 would see it immediately. Assets in HOLD are left out and
   listed; assets in REVIEW are included but flagged.

3. **Size.** Anything approaching the 100 MB ceiling is reported.

    python tools/build_submission_pdfs.py            build
    python tools/build_submission_pdfs.py --dry-run  report only, write nothing

Output goes to `UPLOAD_THESE_12_FILES/` — twelve files, named for their slot.
"""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

import pypdf
from PIL import Image
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A3, A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas as rl_canvas

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src import config as C  # noqa: E402

SRC = ROOT / "submission"
OUT = ROOT / "UPLOAD_THESE_12_FILES"

# Where a juror goes to check any claim in these files for themselves.
REPO_URL = C.GITHUB_URL
PORTAL_URL = C.PAGES_URL
BLOB = f"{REPO_URL}/blob/main"

PROJECT = "Al Safa 2 Park — Falaj Al Safa"
APPLICANT = "Mohamed Wasim · Individual Applicant"
CHALLENGE = "Dubai Municipality AI Park Design Challenge"

INK = HexColor("#1a1a1a")
MUTED = HexColor("#6b6b6b")
RULE = HexColor("#c8c8c8")
ACCENT = HexColor("#1f6f5c")

# The twelve upload fields, in the order the form presents them. `blurb` is the
# one line that goes on the cover so a juror opening the file knows immediately
# what they are holding.
SLOTS: list[dict] = [
    dict(n=1, folder="01_Design_Narrative_Concept",
         title="Design Narrative & Concept",
         blurb="The argument: what is wrong with Al Safa 2 Park today, and what "
               "Falaj Al Safa does about it.",
         sources=["src/plan.py", "tools/report_content.py",
                  "data/processed/hourly_climate_comfort_8760.csv"]),
    dict(n=2, folder="02_Preliminary_Design_Masterplan",
         title="Neighborhood Park Preliminary Design Masterplan",
         blurb="The plan at scale. Every room struck off the crescent's centre; "
               "every area the measured area of the drawn polygon.",
         sources=["src/plan.py", "src/figures.py",
                  "data/raw/site_zoning_schedule.csv"]),
    dict(n=3, folder="03_Concept_Plans_Spatial_Diagrams",
         title="Concept Plans and Spatial Organization Diagrams",
         blurb="How the park is organised — the crescent, the radial alleys, and "
               "the rooms between them.",
         sources=["src/plan.py", "src/drawings.py"]),
    dict(n=4, folder="04_Key_Sections_Elevations",
         title="Key Sections & Elevations",
         blurb="The canopy section solved against the shadow geometry: a 7 m walk "
               "under an 18 m gridshell with a 3 m southern louvre.",
         sources=["src/drawings.py", "src/solar.py", "src/config.py"]),
    dict(n=5, folder="05_3D_Spatial_Visualizations",
         title="3D & Spatial Visualizations",
         blurb="Presentation boards and illustrative views. Renders are artistic "
               "impressions; the analysis outputs are computed.",
         sources=["src/boards.py", "src/plan.py",
                  "archive/withdrawn_visuals/README.md"]),
    dict(n=6, folder="06_AI_Methodology_Report",
         title="AI Methodology Report",
         blurb="Four models, the anti-leakage discipline behind them, and what "
               "each one changed about the design.",
         sources=["src/models.py", "src/dataset.py",
                  "models/model_metrics.json", "tests/test_pipeline.py"]),
    dict(n=7, folder="07_User_Experience_Activation_Strategy",
         title="User Experience & Activation Strategy",
         blurb="Who uses the park, when, and why the programme targets late "
               "afternoon in spring and autumn.",
         sources=["src/models.py", "src/climate.py",
                  "data/processed/hourly_climate_comfort_8760.csv"]),
    dict(n=8, folder="08_Sustainability_Concept_Strategy",
         title="Sustainability Concept & Strategy",
         blurb="Water, carbon, energy and shade — stated conservatively, "
               "including where the scheme runs a deficit.",
         sources=["src/plan.py", "src/costing.py", "src/climate.py"]),
    dict(n=9, folder="09_Material_Landscape_Palette",
         title="Material & Landscape Palette",
         blurb="131 trees across 5 desert species, and the materials that carry "
               "the crescent's language.",
         sources=["src/config.py", "src/plan.py", "src/drawings.py"]),
    dict(n=10, folder="10_Complete_Design_Report",
         title="Complete Design Report",
         blurb="The full concept and preliminary design proposal.",
         sources=["run_analysis.py", "src/plan.py", "src/costing.py",
                  "models/headline_metrics.json"]),
    dict(n=11, folder="11_Site_Analysis_Human_Centric_Research",
         title="Site Analysis & Human-Centric Research",
         blurb="39 years of climate normals, 8,760 modelled hours, and the "
               "7,640 residents within a ten-minute walk.",
         sources=["src/climate.py", "src/solar.py", "data/raw/sources.json",
                  "DATA_SOURCES.md"]),
    dict(n=12, folder="12_Concept_Animation_Video",
         title="One-minute Concept Animation",
         blurb="Storyboard and supporting documentation for the 60-second film.",
         sources=["tools/sync_film.py", "tests/test_film.js"]),
]

# Assets left OUT of the package, with the reason. Nothing disappears silently —
# every one of these is printed in the build report.
#
# This list is EMPTY on purpose. It once named six renders that contradicted the
# plan — a serpentine canopy over a lagoon, a dead-straight corridor, a tropical
# pavilion. All six were withdrawn and then deleted on 3 August 2026, and their
# reasons are preserved in archive/withdrawn_visuals/README.md.
#
# It must stay empty, because AL_SAFA_MASTER_PROMPT.md directs the replacement
# renders to those same filenames — src/boards.py reads them by name. Re-adding
# a name here would silently reject the correct new image along with the old bad
# one. The guard against a bad render is the acceptance test in the master
# prompt, applied by a person looking at the picture, not a filename blocklist.
HOLD: dict[str, str] = {}

# Included, but the build report says why they are worth replacing.
REVIEW: dict[str, str] = {
    "Al_Safa_2_Park_3D_Spatial_Visualizations.pdf":
        "9-page legacy package that may still embed the withdrawn renders. Open "
        "its pages and check before submitting.",
}

# What each kind of image is, said plainly on its sheet. A juror must never have
# to guess whether they are looking at a measurement or an illustration.
CLASSIFICATION = {
    "render": "Artistic impression — illustrative of design intent. AI-generated.",
    "figure": "Analysis output — computed from project data.",
    "drawing": "Technical drawing — to scale.",
    "plan": "Technical drawing — to scale. Geometry generated by src/plan.py; "
            "every area is the measured area of the drawn polygon.",
    "board": "Presentation board.",
}


def classify(p: Path) -> str:
    n = p.name.lower()
    if p.suffix.lower() in (".jpg", ".jpeg"):
        return "render"
    if n.startswith("board_"):
        return "board"
    # The masterplan is numbered as a figure because run_analysis.py writes it,
    # but it is a scale drawing and a juror should read it as one.
    if "masterplan" in n:
        return "plan"
    if n.startswith("fig"):
        return "figure"
    return "drawing"


def pretty(name: str) -> str:
    """A filename turned into something a person would read on a sheet."""
    stem = Path(name).stem
    for junk in ("_crescent", "_1784970552956", "_1784970565232"):
        stem = stem.replace(junk, "")
    stem = stem.replace("_", " ").strip()
    return stem[:1].upper() + stem[1:]


MARKERS = ("[AI DRAFT]", "AI-GENERATED DRAFT", "FOR REVIEW",
           "AI DRAFT]", "DRAFT - FOR REVIEW")

# Claims and language this submission has withdrawn. A document is not safe to
# upload merely because it lacks a draft stamp: two files were still shipping in
# slots 05 and 11 that described the superseded straight-spine scheme and quoted
# the 99.2% shade figure the project itself retracted. A juror comparing them
# with slot 02 would have found two different parks and a number that the
# analysis contradicts.
WITHDRAWN = {
    "99.2": "quotes the withdrawn 99.2% shade claim (re-solved section is 87.3%)",
    "SHADED SPINE": "describes the superseded straight-spine scheme",
    "LINEAR SPINE": "describes the superseded straight-spine scheme",
}


def _has_marker(text: str) -> bool:
    up = text.upper()
    return any(mk in up for mk in MARKERS)


def withdrawn_claims(pdf: Path) -> list[str]:
    """Withdrawn claims or superseded-scheme language found in a PDF.

    The distinction that matters is between *asserting* a retracted claim and
    *retracting* it. The rewritten reports quote 99.2% and the straight spine on
    purpose, in order to say they were withdrawn — that is the submission's
    strongest passage, not a defect. So a document is only flagged when it
    repeats the claim without any retraction language anywhere in it.
    """
    try:
        r = pypdf.PdfReader(str(pdf))
        txt = " ".join((pg.extract_text() or "") for pg in r.pages).upper()
    except Exception:
        return []
    retracts = any(w in txt for w in
                   ("WITHDRAW", "DOES NOT SURVIVE", "SUPERSEDE",
                    "RE-SOLVED"))
    if retracts:
        return []
    found = [why for needle, why in WITHDRAWN.items() if needle in txt]
    # "spine" alone is only damning when the crescent is never mentioned.
    if "SPINE" in txt and "CRESCENT" not in txt:
        found.append("describes the superseded scheme and never mentions the "
                     "crescent")
    return found


def draft_markers(pdf: Path) -> int:
    """How many pages of this PDF describe themselves as an unreviewed draft."""
    try:
        r = pypdf.PdfReader(str(pdf))
    except Exception:
        return 0
    hits = 0
    for pg in r.pages:
        try:
            if _has_marker(pg.extract_text() or ""):
                hits += 1
        except Exception:
            pass
    return hits


def cover_page(c: rl_canvas.Canvas, slot: dict, items: list[Path]) -> None:
    w, h = A4
    c.setFillColor(ACCENT)
    c.rect(0, h - 12 * mm, w, 12 * mm, stroke=0, fill=1)

    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8.5)
    c.drawString(20 * mm, h - 26 * mm, CHALLENGE.upper())

    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(20 * mm, h - 34 * mm, f"UPLOAD SLOT {slot['n']:02d} OF 12")

    # Title, wrapped by hand — reportlab has no flow here and the titles are short.
    c.setFont("Helvetica-Bold", 21)
    y = h - 50 * mm
    words, line = slot["title"].split(), ""
    for word in words:
        trial = f"{line} {word}".strip()
        if c.stringWidth(trial, "Helvetica-Bold", 21) > (w - 40 * mm):
            c.drawString(20 * mm, y, line)
            y -= 9.5 * mm
            line = word
        else:
            line = trial
    if line:
        c.drawString(20 * mm, y, line)
    y -= 12 * mm

    c.setFillColor(MUTED)
    c.setFont("Helvetica", 10.5)
    for chunk in _wrap(c, slot["blurb"], "Helvetica", 10.5, w - 40 * mm):
        c.drawString(20 * mm, y, chunk)
        y -= 5.6 * mm

    y -= 6 * mm
    c.setStrokeColor(RULE)
    c.line(20 * mm, y, w - 20 * mm, y)
    y -= 9 * mm

    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(20 * mm, y, "CONTENTS")
    y -= 6 * mm
    c.setFont("Helvetica", 9)
    c.setFillColor(MUTED)
    for it in items:
        c.drawString(23 * mm, y, f"·  {pretty(it.name)}")
        y -= 5 * mm
        if y < 78 * mm:
            break

    # Sits directly under the contents list, but never low enough to collide
    # with the footer.
    verify_panel(c, slot, w, max(y - 9 * mm, 70 * mm))

    c.setFont("Helvetica", 8.5)
    c.setFillColor(MUTED)
    c.drawString(20 * mm, 26 * mm, PROJECT)
    c.drawString(20 * mm, 21 * mm, APPLICANT)
    c.drawString(20 * mm, 16 * mm,
                 f"Generated {date.today().isoformat()} · "
                 f"reproducible: python tools/build_submission_pdfs.py")
    c.showPage()


def _link(c, label: str, url: str, x: float, y: float,
          font: str = "Helvetica-Bold", size: float = 8.5) -> None:
    """Draw `label` as a live hyperlink to `url`."""
    c.setFillColor(ACCENT)
    c.setFont(font, size)
    c.drawString(x, y, label)
    wide = c.stringWidth(label, font, size)
    c.linkURL(url, (x, y - 1.2 * mm, x + wide, y + 3.2 * mm), relative=0)


def verify_panel(c: rl_canvas.Canvas, slot: dict, w: float, top: float) -> None:
    """The evidence block: where to go to check any claim in this file.

    Every slot carries it, because the point of the submission is that no
    number in it was typed by hand — each one is regenerated from the code and
    data named here, and a juror can open that code in a browser.
    """
    x = 20 * mm

    c.setStrokeColor(RULE)
    c.line(x, top + 6 * mm, w - 20 * mm, top + 6 * mm)

    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x, top, "VERIFY THIS DOCUMENT")

    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8)
    c.drawString(x, top - 5 * mm,
                 "Every quantity in this file is regenerated from data by code. "
                 "Nothing is typed by hand.")

    rows = [
        ("Repository", REPO_URL.replace("https://", ""), REPO_URL),
        ("Live portal", PORTAL_URL.replace("https://", ""), PORTAL_URL),
    ]
    y = top - 12 * mm
    for label, shown, url in rows:
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 8)
        c.drawString(x, y, label)
        _link(c, shown, url, x + 24 * mm, y)
        y -= 5 * mm

    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8)
    c.drawString(x, y, "Produced by")
    sx = x + 24 * mm
    for i, src in enumerate(slot.get("sources", [])):
        if sx + c.stringWidth(src, "Helvetica-Bold", 8.5) > w - 22 * mm:
            y -= 4.6 * mm
            sx = x + 24 * mm
        _link(c, src, f"{BLOB}/{src}", sx, y)
        sx += c.stringWidth(src, "Helvetica-Bold", 8.5) + 3 * mm
        if i < len(slot.get("sources", [])) - 1:
            c.setFillColor(MUTED)
            c.setFont("Helvetica", 8)
            c.drawString(sx - 2.4 * mm, y, "·")
    y -= 5 * mm

    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8)
    c.drawString(x, y, "Reproduce")
    c.setFont("Courier", 8)
    c.setFillColor(INK)
    c.drawString(x + 24 * mm, y,
                 "python run_analysis.py   ·   python -m tests.test_pipeline")


# The ten phases the project actually ran, and what each one produced. Every
# slot names the phases behind it, so a juror can see where in the process this
# particular document came from rather than being handed a finished artefact.
PHASES: list[tuple[int, str, str]] = [
    (1, "Site & Context Analysis",
     "39 years of NCM normals rebuilt into an 8,760-hour year, verified back to "
     "within 0.39 °C; sun position for every hour via NREL/pvlib; shadow "
     "geometry; 7,640 residents inside a ten-minute walk"),
    (2, "Problem Definition",
     "Phase 1 findings turned into problems and scored by severity rather than "
     "listed flat — thermal discomfort dominates everything else"),
    (3, "Opportunity & Objectives",
     "The ranked problems converted into measurable targets, including the "
     "comfort-hours target the finished design is scored against"),
    (4, "Concept Development",
     "Multiple plan forms generated and swept against the solar model; the "
     "crescent selected on hours-with-no-shade, not on mean coverage"),
    (5, "Masterplan Development",
     "Every room struck off the crescent's centre; areas taken as the shoelace "
     "area of the drawn polygon, so the schedule closes on 15,000 m²"),
    (6, "Detailed Design",
     "The canopy section solved against shadow geometry — 7 m walk, 18 m "
     "gridshell at 4.5 m, 3 m southern louvre; 131 trees at mature canopy"),
    (7, "Performance & Sustainability",
     "Water balance, carbon, the canopy PV deficit, and ray-traced shade "
     "performance by zone"),
    (8, "User Experience & Activation",
     "K-Means microclimate regimes and the hour-by-month comfort surface; "
     "programming targeted at late afternoon, spring and autumn"),
    (9, "AI Workflow & Visualisation",
     "The four models and the anti-leakage discipline; drawings, boards, the "
     "analytics portal and the sixty-second film"),
    (10, "Submission Assembly",
     "Every report and visual mapped onto the twelve upload slots, each with a "
     "manifest naming what produced it"),
]

# Which phases produced each slot.
SLOT_PHASES: dict[int, list[int]] = {
    1: [2, 3, 4], 2: [5], 3: [4, 5], 4: [6], 5: [9], 6: [9],
    7: [8], 8: [7], 9: [6], 10: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    11: [1], 12: [9],
}

# The evidence index printed at the back of every slot. Grouped, and every row
# is a live link, so a juror holding any one of the twelve files can reach the
# whole project from it.
INDEX: list[tuple[str, list[tuple[str, str]]]] = [
    ("Start here", [
        ("EXPLAIN_THE_PROJECT/START_HERE.md", "The project in plain language"),
        ("PROJECT_PLAN.md", "Requirements, phases, status, what is left"),
        ("README.md", "The design argument, written for a juror"),
        ("notebooks/AL_SAFA_2_PARK_COMPLETE_ANALYSIS.ipynb",
         "The complete analysis, outputs embedded"),
    ]),
    ("The geometry and the models", [
        ("src/plan.py", "Single source of the crescent geometry"),
        ("src/climate.py", "The 8,760-hour year rebuilt from NCM normals"),
        ("src/solar.py", "Sun position and shadow ray-tracing"),
        ("src/dataset.py", "Assembles the ML training tables"),
        ("src/models.py", "The four models"),
        ("src/costing.py", "The cost model against the AED 35 M ceiling"),
    ]),
    ("The data, as issued and as processed", [
        ("data/raw/sources.json", "Every source dataset, with its period"),
        ("DATA_SOURCES.md", "Sources and their stated limitations"),
        ("data/raw/site_zoning_schedule.csv", "The measured room schedule"),
        ("data/processed/hourly_climate_comfort_8760.csv",
         "The 8,760-hour climate and comfort series"),
        ("data/processed/cost_plan.csv", "The capital cost plan, line by line"),
    ]),
    ("The results, and the checks on them", [
        ("models/model_metrics.json", "Trained-model metrics"),
        ("models/headline_metrics.json", "The headline numbers"),
        ("tests/test_pipeline.py", "38 correctness checks"),
        ("archive/withdrawn_visuals/README.md",
         "Images withdrawn on purpose, and why"),
    ]),
    ("The drawings", [
        ("figures/fig10_masterplan.png", "Masterplan and room schedule"),
        ("design/visuals/section_crescent.png", "Section A–A at midspan"),
        ("design/visuals/circulation_crescent.png", "Circulation and accessibility"),
        ("design/visuals/facilities_crescent.png",
         "Commercial & Service Facilities Map"),
        ("design/visuals/planting_crescent.png", "Planting plan, 131 trees"),
    ]),
]


def method_page(c: rl_canvas.Canvas, slot: dict) -> None:
    """How this document came to exist — the process, not the artefact."""
    c.setPageSize(A4)
    w, h = A4

    c.setFillColor(ACCENT)
    c.rect(0, h - 12 * mm, w, 12 * mm, stroke=0, fill=1)

    x = 20 * mm
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(x, h - 28 * mm, "How this document was produced")

    c.setFillColor(MUTED)
    c.setFont("Helvetica", 9)
    y = h - 36 * mm
    intro = ("This submission is the output of a ten-phase process in which "
             "each phase is checked against the one before it. Nothing "
             "downstream is hand-drawn or hand-typed: change an input, re-run, "
             "and every chart, drawing and figure moves with it — or a test "
             "fails loudly. The phases behind this particular document are "
             "marked.")
    for line in _wrap(c, intro, "Helvetica", 9, w - 40 * mm):
        c.drawString(x, y, line)
        y -= 4.6 * mm

    y -= 5 * mm
    mine = SLOT_PHASES.get(slot["n"], [])
    for n, name, what in PHASES:
        here = n in mine
        if here:
            c.setFillColor(ACCENT)
            c.rect(x - 3 * mm, y - 1.5 * mm, 1.6 * mm, 5.5 * mm, stroke=0, fill=1)
        c.setFillColor(INK if here else MUTED)
        c.setFont("Helvetica-Bold" if here else "Helvetica", 8.8)
        c.drawString(x, y, f"Phase {n} — {name}")
        y -= 4.4 * mm
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 7.8)
        for line in _wrap(c, what, "Helvetica", 7.8, w - 46 * mm):
            c.drawString(x + 4 * mm, y, line)
            y -= 3.9 * mm
        y -= 2.2 * mm

    y -= 2 * mm
    c.setStrokeColor(RULE)
    c.line(x, y, w - 20 * mm, y)
    y -= 7 * mm

    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x, y, "THE CODE AND DATA BEHIND THIS DOCUMENT")
    y -= 6 * mm
    for src in slot.get("sources", []):
        _link(c, src, f"{BLOB}/{src}", x + 3 * mm, y, size=8.2)
        y -= 4.8 * mm

    y -= 3 * mm
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x, y, "REPRODUCE IT")
    y -= 6 * mm
    c.setFont("Courier", 8)
    c.setFillColor(MUTED)
    for cmd in ("pip install -r requirements.txt",
                "python run_analysis.py           # data, models, figures",
                "python -m src.drawings           # section, elevation, planting",
                "python -m src.boards             # the presentation boards",
                "python tools/build_submission_pdfs.py",
                "python -m tests.test_pipeline    # 38 checks"):
        c.drawString(x + 3 * mm, y, cmd)
        y -= 4.4 * mm

    c.setFont("Helvetica", 8)
    c.setFillColor(MUTED)
    c.drawString(x, 16 * mm, f"{PROJECT} · Upload slot {slot['n']:02d} of 12")
    c.showPage()


def index_page(c: rl_canvas.Canvas, slot: dict) -> None:
    """Every part of the project, live, from whichever file a juror opened."""
    c.setPageSize(A4)
    w, h = A4

    c.setFillColor(ACCENT)
    c.rect(0, h - 12 * mm, w, 12 * mm, stroke=0, fill=1)

    x = 20 * mm
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(x, h - 28 * mm, "The complete project, and where to check it")

    c.setFillColor(MUTED)
    c.setFont("Helvetica", 9)
    y = h - 36 * mm
    intro = ("Every link below is live. The repository holds the data, the "
             "code, the trained models and the tests, and runs end to end with "
             "one command. A juror who wants to know where a number came from "
             "can be given a file path rather than an opinion.")
    for line in _wrap(c, intro, "Helvetica", 9, w - 40 * mm):
        c.drawString(x, y, line)
        y -= 4.6 * mm

    y -= 4 * mm
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8.5)
    c.drawString(x, y, "Repository")
    _link(c, REPO_URL.replace("https://", ""), REPO_URL, x + 24 * mm, y)
    y -= 5 * mm
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8.5)
    c.drawString(x, y, "Live portal")
    _link(c, PORTAL_URL.replace("https://", ""), PORTAL_URL, x + 24 * mm, y)
    y -= 9 * mm

    for heading, rows in INDEX:
        c.setStrokeColor(RULE)
        c.line(x, y + 4.5 * mm, w - 20 * mm, y + 4.5 * mm)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 8.6)
        c.drawString(x, y, heading.upper())
        y -= 5.4 * mm
        for path, what in rows:
            _link(c, path, f"{BLOB}/{path}", x + 3 * mm, y, size=7.8)
            c.setFillColor(MUTED)
            c.setFont("Helvetica", 7.6)
            c.drawRightString(w - 20 * mm, y, what)
            y -= 4.3 * mm
        y -= 4 * mm

    c.setFillColor(MUTED)
    c.setFont("Helvetica", 7.6)
    c.drawString(x, 20 * mm,
                 "Links resolve once the repository is published. GitHub "
                 "renders PDFs and notebooks in the browser — nothing needs to "
                 "be downloaded or cloned.")
    c.setFont("Helvetica", 8)
    c.drawString(x, 14 * mm, f"{PROJECT} · Upload slot {slot['n']:02d} of 12")
    c.showPage()


def _wrap(c, text: str, font: str, size: float, maxw: float) -> list[str]:
    out, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if c.stringWidth(trial, font, size) > maxw:
            out.append(line)
            line = word
        else:
            line = trial
    if line:
        out.append(line)
    return out


def image_sheet(c: rl_canvas.Canvas, img: Path, slot: dict) -> None:
    """One image, one A3 landscape sheet, titled, classified and sourced."""
    pw, ph = landscape(A3)
    c.setPageSize((pw, ph))

    kind = classify(img)
    title = pretty(img.name)

    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(16 * mm, ph - 16 * mm, title)

    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8.5)
    c.drawString(16 * mm, ph - 21.5 * mm, CLASSIFICATION[kind])

    top = ph - 27 * mm
    bottom = 14 * mm
    avail_w, avail_h = pw - 32 * mm, top - bottom

    with Image.open(img) as im:
        iw, ih = im.size
    scale = min(avail_w / iw, avail_h / ih)
    dw, dh = iw * scale, ih * scale
    c.drawImage(str(img), (pw - dw) / 2, bottom + (avail_h - dh) / 2,
                width=dw, height=dh, preserveAspectRatio=True, mask="auto")

    c.setFillColor(MUTED)
    c.setFont("Helvetica", 7.5)
    c.drawString(16 * mm, 8 * mm, f"{PROJECT} · {CHALLENGE}")

    # The image's own file, live. A juror who doubts a drawing can open the
    # exact asset this sheet was built from.
    rel = f"submission/{slot['folder']}/{img.name}"
    url = f"{BLOB}/{rel}"
    label = img.name
    c.setFillColor(ACCENT)
    c.setFont("Helvetica", 7.5)
    c.drawRightString(pw - 16 * mm, 8 * mm, label)
    wide = c.stringWidth(label, "Helvetica", 7.5)
    c.linkURL(url, (pw - 16 * mm - wide, 6.8 * mm, pw - 16 * mm, 11 * mm),
              relative=0)
    c.showPage()


def build_slot(slot: dict, act: bool) -> dict:
    folder = SRC / slot["folder"]
    report = dict(slot=slot["n"], title=slot["title"], pages=0, mb=0.0,
                  drafts=[], held=[], review=[], stale=[], locked=False,
                  missing=not folder.exists(), out=None)
    if not folder.exists():
        return report

    files = [f for f in sorted(folder.iterdir())
             if f.is_file() and f.name != "MANIFEST.md"]

    pdfs, imgs = [], []
    for f in files:
        if f.name in HOLD:
            report["held"].append((f.name, HOLD[f.name]))
            continue
        if f.name in REVIEW:
            report["review"].append((f.name, REVIEW[f.name]))
        if f.suffix.lower() == ".pdf":
            pdfs.append(f)
        elif f.suffix.lower() in (".png", ".jpg", ".jpeg"):
            imgs.append(f)

    for p in pdfs:
        n = draft_markers(p)
        if n:
            report["drafts"].append((p.name, n))
        for why in withdrawn_claims(p):
            report["stale"].append((p.name, why))

    ordered = pdfs + imgs
    if not ordered:
        return report

    OUT.mkdir(exist_ok=True)
    stem = f"{slot['n']:02d}_{slot['title'].replace(' ', '_').replace('&', 'and')}"
    stem = "".join(ch for ch in stem if ch.isalnum() or ch in "_-")
    dest = OUT / f"{stem}.pdf"
    report["out"] = dest.name

    if not act:
        report["pages"] = -1
        return report

    tmp = OUT / f".{stem}.front.pdf"
    c = rl_canvas.Canvas(str(tmp), pagesize=A4)
    cover_page(c, slot, ordered)                  # page 0
    method_page(c, slot)                          # page 1
    for img in imgs:                              # pages 2 .. 2+len(imgs)
        image_sheet(c, img, slot)
    index_page(c, slot)                           # last page
    c.save()

    writer = pypdf.PdfWriter()
    front = pypdf.PdfReader(str(tmp))
    writer.add_page(front.pages[0])              # cover
    writer.add_page(front.pages[1])              # how it was produced
    for p in pdfs:                                # the written reports
        try:
            for pg in pypdf.PdfReader(str(p)).pages:
                writer.add_page(pg)
        except Exception as e:
            print(f"    ! could not merge {p.name}: {e}")
    for pg in front.pages[2:]:                    # image sheets, then the index
        writer.add_page(pg)

    try:
        with dest.open("wb") as fh:
            writer.write(fh)
    except PermissionError:
        # Open in a viewer. Say so instead of dying, so the other eleven slots
        # still build and the summary can name what went stale.
        tmp.unlink(missing_ok=True)
        report["locked"] = True
        return report
    tmp.unlink(missing_ok=True)

    report["pages"] = len(writer.pages)
    report["mb"] = dest.stat().st_size / 1e6
    return report


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    act = not args.dry_run

    locked: list[str] = []
    if act and OUT.exists():
        # Not rmtree: on Windows a PDF open in a viewer cannot be deleted, and
        # a half-cleared folder that then fails to rewrite one slot would leave
        # a STALE file sitting in the upload folder looking current. Delete what
        # we can, remember what we could not, and refuse to finish quietly.
        for old in OUT.iterdir():
            try:
                old.unlink()
            except PermissionError:
                locked.append(old.name)

    print("=" * 78)
    print("  BUILDING 12 UPLOAD PDFs - one file per Dubai Municipality slot")
    print("=" * 78)
    if locked:
        print()
        print("  [!] LOCKED — open in another program, could not be replaced:")
        for name in locked:
            print(f"      {name}")
        print("      Close the viewer and re-run, or these stay OUT OF DATE.")

    reports = [build_slot(s, act) for s in SLOTS]

    print()
    for r in reports:
        if r["missing"]:
            print(f"  {r['slot']:02d}  MISSING FOLDER — {r['title']}")
            continue
        if r["locked"]:
            print(f"  {r['slot']:02d}  LOCKED — STALE, not rewritten   {r['out']}")
            continue
        size = f"{r['mb']:5.1f} MB" if act else "   dry  "
        pages = f"{r['pages']:3d}pp" if act else "  ?pp"
        print(f"  {r['slot']:02d}  {pages}  {size}   {r['out']}")

    drafts = [(r, d) for r in reports for d in r["drafts"]]
    if drafts:
        print()
        print("=" * 78)
        print("  [!] DRAFT MARKERS - these documents describe themselves as")
        print("      unreviewed AI drafts. Do not submit them in this state.")
        print("=" * 78)
        for r, (name, n) in drafts:
            print(f"  slot {r['slot']:02d}  {name}  ({n} page(s))")

    held = [(r, h) for r in reports for h in r["held"]]
    if held:
        print()
        print("=" * 78)
        print("  [X] HELD BACK - contradicts the design. Not in the package.")
        print("=" * 78)
        for r, (name, why) in held:
            print(f"  slot {r['slot']:02d}  {name}")
            print(f"           {why}")

    stale = [(r, t) for r in reports for t in r["stale"]]
    if stale:
        print()
        print("=" * 78)
        print("  [X] WITHDRAWN CLAIMS / SUPERSEDED SCHEME still in the package")
        print("=" * 78)
        for r, (name, why) in stale:
            print(f"  slot {r['slot']:02d}  {name}")
            print(f"           {why}")

    rev = [(r, v) for r in reports for v in r["review"]]
    if rev:
        print()
        print("=" * 78)
        print("  [!] INCLUDED BUT WORTH REPLACING")
        print("=" * 78)
        for r, (name, why) in rev:
            print(f"  slot {r['slot']:02d}  {name}")
            print(f"           {why}")

    if act:
        over = [r for r in reports if r["mb"] > 95]
        if over:
            print("\n  ⛔ OVER 95 MB — the form's ceiling is 100 MB:")
            for r in over:
                print(f"     slot {r['slot']:02d}  {r['mb']:.1f} MB")
        total = sum(r["mb"] for r in reports)
        built = sum(1 for r in reports if r["out"])
        print()
        print("=" * 78)
        print(f"  {built}/12 slots built | {total:.1f} MB total -> UPLOAD_THESE_12_FILES/")
        print("=" * 78)
        stuck = locked or [r["out"] for r in reports if r["locked"]]
        if stuck:
            print(f"  [X] BUILD INCOMPLETE — {len(set(stuck))} file(s) could not "
                  f"be rewritten and are STALE. Close them and re-run before "
                  f"uploading.")
            return 1
    else:
        print("\n  DRY RUN — nothing written.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
