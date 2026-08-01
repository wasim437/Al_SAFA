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

Output goes to `submission_upload/` — twelve files, named for their slot.
"""

from __future__ import annotations

import argparse
import shutil
from datetime import date
from pathlib import Path

import pypdf
from PIL import Image
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A3, A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas as rl_canvas

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "submission"
OUT = ROOT / "submission_upload"

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
               "Falaj Al Safa does about it."),
    dict(n=2, folder="02_Preliminary_Design_Masterplan",
         title="Neighborhood Park Preliminary Design Masterplan",
         blurb="The plan at scale. Every room struck off the crescent's centre; "
               "every area the measured area of the drawn polygon."),
    dict(n=3, folder="03_Concept_Plans_Spatial_Diagrams",
         title="Concept Plans and Spatial Organization Diagrams",
         blurb="How the park is organised — the crescent, the radial alleys, and "
               "the rooms between them."),
    dict(n=4, folder="04_Key_Sections_Elevations",
         title="Key Sections & Elevations",
         blurb="The canopy section solved against the shadow geometry: a 7 m walk "
               "under an 18 m gridshell with a 3 m southern louvre."),
    dict(n=5, folder="05_3D_Spatial_Visualizations",
         title="3D & Spatial Visualizations",
         blurb="Presentation boards and illustrative views. Renders are artistic "
               "impressions; the analysis outputs are computed."),
    dict(n=6, folder="06_AI_Methodology_Report",
         title="AI Methodology Report",
         blurb="Four models, the anti-leakage discipline behind them, and what "
               "each one changed about the design."),
    dict(n=7, folder="07_User_Experience_Activation_Strategy",
         title="User Experience & Activation Strategy",
         blurb="Who uses the park, when, and why the programme targets late "
               "afternoon in spring and autumn."),
    dict(n=8, folder="08_Sustainability_Concept_Strategy",
         title="Sustainability Concept & Strategy",
         blurb="Water, carbon, energy and shade — stated conservatively, "
               "including where the scheme runs a deficit."),
    dict(n=9, folder="09_Material_Landscape_Palette",
         title="Material & Landscape Palette",
         blurb="131 trees across 5 desert species, and the materials that carry "
               "the crescent's language."),
    dict(n=10, folder="10_Complete_Design_Report",
         title="Complete Design Report",
         blurb="The full concept and preliminary design proposal."),
    dict(n=11, folder="11_Site_Analysis_Human_Centric_Research",
         title="Site Analysis & Human-Centric Research",
         blurb="39 years of climate normals, 8,760 modelled hours, and the "
               "7,640 residents within a ten-minute walk."),
    dict(n=12, folder="12_Concept_Animation_Video",
         title="One-minute Concept Animation",
         blurb="Storyboard and supporting documentation for the 60-second film."),
]

# Assets left OUT of the package, with the reason. Nothing disappears silently —
# every one of these is printed in the build report.
HOLD: dict[str, str] = {
    "masterplan_aerial_golden_hour.jpg":
        "VERIFIED — serpentine S-curve canopy over a large free-form lagoon. The "
        "plan is ONE 141 m arc with a 0.9 m channel. Prompt 01 replaces it.",
    "dubai_futuristic_masterplan_aerial.jpg":
        "VERIFIED — multiple free-form organic shells over winding canals and "
        "rainforest planting, with the Museum of the Future on the skyline. This "
        "is a generic 'futuristic Dubai park', not this project. Prompt 01.",
    "spine_corridor_interior.jpg":
        "VERIFIED — a DEAD STRAIGHT hexagonal gridshell corridor. This is the "
        "superseded straight-spine scheme, the exact design the crescent "
        "replaced. It is also nearly empty of people. Prompt 03.",
    "dubai_futuristic_spine_interior.jpg":
        "VERIFIED — a vaulted timber-and-glass botanical pavilion with tropical "
        "planting (cycads, agave, flowering shrubs) and misting. Beautiful, but "
        "it is not a 7 m walk under an 18 m arc, and the planting contradicts the "
        "five-species desert palette in slot 09. Prompt 03 or 04.",
}

# Included, but the build report says why they are worth replacing.
REVIEW: dict[str, str] = {
    "eyelevel_spine_1784970552956.jpg":
        "VERIFIED — the strongest of the existing set. Curved timber louvre walk, "
        "families, good light. But it curves as an S rather than one arc, and no "
        "water channel is visible at its edge. Prompt 03 replaces it.",
    "night_plaza_render_1784970565232.jpg":
        "VERIFIED — does not contradict the plan (it shows no canopy), and it is "
        "the only night image, which the brief requires. But the jet fountains "
        "work against the water-scarcity argument in slot 08, where the falaj is "
        "105 m² total. Prompt 02 or 05.",
    "Al_Safa_2_Park_3D_Spatial_Visualizations.pdf":
        "9-page package that likely embeds the held renders. Check its pages "
        "before submitting.",
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


def draft_markers(pdf: Path) -> int:
    """How many pages of this PDF describe themselves as an unreviewed draft."""
    try:
        r = pypdf.PdfReader(str(pdf))
    except Exception:
        return 0
    hits = 0
    for pg in r.pages:
        try:
            if "DRAFT" in (pg.extract_text() or "").upper():
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
        if y < 45 * mm:
            break

    c.setFont("Helvetica", 8.5)
    c.setFillColor(MUTED)
    c.drawString(20 * mm, 26 * mm, PROJECT)
    c.drawString(20 * mm, 21 * mm, APPLICANT)
    c.drawString(20 * mm, 16 * mm,
                 f"Generated {date.today().isoformat()} · "
                 f"reproducible: python tools/build_submission_pdfs.py")
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


def image_sheet(c: rl_canvas.Canvas, img: Path) -> None:
    """One image, one A3 landscape sheet, titled and classified."""
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
    c.drawRightString(pw - 16 * mm, 8 * mm, img.name)
    c.showPage()


def build_slot(slot: dict, act: bool) -> dict:
    folder = SRC / slot["folder"]
    report = dict(slot=slot["n"], title=slot["title"], pages=0, mb=0.0,
                  drafts=[], held=[], review=[], missing=not folder.exists(),
                  out=None)
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
    cover_page(c, slot, ordered)
    for img in imgs:
        image_sheet(c, img)
    c.save()

    writer = pypdf.PdfWriter()
    front = pypdf.PdfReader(str(tmp))
    writer.add_page(front.pages[0])              # cover
    for p in pdfs:                                # the written reports
        try:
            for pg in pypdf.PdfReader(str(p)).pages:
                writer.add_page(pg)
        except Exception as e:
            print(f"    ! could not merge {p.name}: {e}")
    for pg in front.pages[1:]:                    # then the image sheets
        writer.add_page(pg)

    with dest.open("wb") as fh:
        writer.write(fh)
    tmp.unlink(missing_ok=True)

    report["pages"] = len(writer.pages)
    report["mb"] = dest.stat().st_size / 1e6
    return report


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    act = not args.dry_run

    if act and OUT.exists():
        shutil.rmtree(OUT)

    print("=" * 78)
    print("  BUILDING 12 UPLOAD PDFs - one file per Dubai Municipality slot")
    print("=" * 78)

    reports = [build_slot(s, act) for s in SLOTS]

    print()
    for r in reports:
        if r["missing"]:
            print(f"  {r['slot']:02d}  MISSING FOLDER — {r['title']}")
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
        print(f"  {built}/12 slots built | {total:.1f} MB total -> submission_upload/")
        print("=" * 78)
    else:
        print("\n  DRY RUN — nothing written.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
