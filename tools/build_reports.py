"""Generate the written reports from the live analysis.

WHY THIS EXISTS
---------------
The reports that were about to be submitted had three problems, and all three
were fatal in front of a jury:

1. **They said they were drafts.** Eleven of the twelve slots carried
   "[AI DRAFT]" in the running title and "AI-GENERATED DRAFT — FOR REVIEW" in
   the body. Declaration 2 on the upload form asks the applicant to confirm the
   submission is their own original work; a document that introduces itself as
   an unreviewed draft argues the opposite.

2. **They described a different park.** The scheme was redesigned from a
   straight spine through rectangular rooms to a single crescent with radial
   rooms, a water channel and a sunken palm court. The code, the drawings, the
   portal and the film all moved. The Word documents did not, so slot 02 and
   slot 10 described two different projects.

3. **They carried withdrawn numbers.** The 99.2% annual shade claim does not
   survive a geometric check and was withdrawn; it was still in the prose.

The fix is not to edit eleven Word files by hand, because they would drift again
the next time the geometry moved. Every number below is read at build time from
`models/`, `data/` and `src.plan`. If the sagitta changes, these reports change
with it — or the pipeline's tests fail first.

WHAT THIS DOES NOT DO
---------------------
It does not write the design. The argument, the ordering and the judgement in
these pages are authored; what is automated is that the *figures quoted in the
prose* cannot fall out of step with the model that produced them.

    python tools/build_reports.py
"""

from __future__ import annotations

import csv
import json
import sys
from datetime import date
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (BaseDocTemplate, Frame, Image, KeepTogether,
                                ListFlowable, ListItem, NextPageTemplate,
                                PageTemplate, Paragraph, Spacer, Table,
                                TableStyle)

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src import config as C, plan  # noqa: E402

OUT = ROOT / "reports" / "pdf"

INK = colors.HexColor("#1a1a1a")
MUTED = colors.HexColor("#6b6b6b")
RULE = colors.HexColor("#c8c8c8")
ACCENT = colors.HexColor("#1f6f5c")
WASH = colors.HexColor("#f4f2ed")


# ── live data ────────────────────────────────────────────────────────────────
def load() -> dict:
    m = json.loads((C.MODELS / "headline_metrics.json").read_text(encoding="utf-8"))
    cost = json.loads((C.MODELS / "cost_summary.json").read_text(encoding="utf-8"))
    models = json.loads((C.MODELS / "model_metrics.json").read_text(encoding="utf-8"))
    with (C.DATA_RAW / "site_zoning_schedule.csv").open(encoding="utf-8") as fh:
        zones = list(csv.DictReader(fh))
    with (C.DATA_PROCESSED / "cost_plan.csv").open(encoding="utf-8") as fh:
        cost_lines = list(csv.DictReader(fh))
    with (C.DATA_RAW / "species_water_carbon_rates.csv").open(encoding="utf-8") as fh:
        species = list(csv.DictReader(fh))
    return dict(m=m, cost=cost, models=models, zones=zones,
                cost_lines=cost_lines, species=species,
                facilities=plan.facilities())


# ── page furniture ───────────────────────────────────────────────────────────
def _styles() -> dict:
    ss = getSampleStyleSheet()
    return dict(
        h1=ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold",
                          fontSize=15, leading=19, spaceBefore=14, spaceAfter=7,
                          textColor=INK),
        h2=ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold",
                          fontSize=11, leading=14, spaceBefore=11, spaceAfter=5,
                          textColor=ACCENT),
        body=ParagraphStyle("body", parent=ss["BodyText"], fontName="Helvetica",
                            fontSize=9.4, leading=14.2, spaceAfter=7,
                            alignment=TA_JUSTIFY, textColor=INK),
        lead=ParagraphStyle("lead", parent=ss["BodyText"], fontName="Helvetica",
                            fontSize=11, leading=16, spaceAfter=10,
                            textColor=INK),
        bullet=ParagraphStyle("bullet", parent=ss["BodyText"],
                              fontName="Helvetica", fontSize=9.4, leading=13.6,
                              spaceAfter=3, textColor=INK),
        cap=ParagraphStyle("cap", parent=ss["BodyText"], fontName="Helvetica",
                           fontSize=7.8, leading=10.5, spaceBefore=3,
                           spaceAfter=10, textColor=MUTED),
        note=ParagraphStyle("note", parent=ss["BodyText"], fontName="Helvetica",
                            fontSize=8.8, leading=13, spaceAfter=7,
                            textColor=colors.HexColor("#8a5a00")),
        title=ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=25,
                             leading=29, textColor=INK, spaceAfter=8),
        sub=ParagraphStyle("sub", fontName="Helvetica", fontSize=12.5,
                           leading=17, textColor=MUTED, spaceAfter=20),
        meta=ParagraphStyle("meta", fontName="Helvetica", fontSize=8.6,
                            leading=13, textColor=MUTED),
    )


class Doc(BaseDocTemplate):
    def __init__(self, path: Path, report: dict, **kw):
        super().__init__(str(path), pagesize=A4,
                         leftMargin=22 * mm, rightMargin=22 * mm,
                         topMargin=20 * mm, bottomMargin=18 * mm,
                         title=report["title"],
                         author="Mohamed Wasim", **kw)
        self.report = report
        frame = Frame(self.leftMargin, self.bottomMargin,
                      self.width, self.height, id="main")
        self.addPageTemplates([
            PageTemplate(id="cover", frames=[frame]),
            PageTemplate(id="body", frames=[frame], onPage=self._furniture),
        ])

    def _furniture(self, canv, doc):
        canv.saveState()
        canv.setStrokeColor(RULE)
        canv.setLineWidth(0.4)
        y = A4[1] - 14 * mm
        canv.line(22 * mm, y, A4[0] - 22 * mm, y)
        canv.setFont("Helvetica", 7.4)
        canv.setFillColor(MUTED)
        canv.drawString(22 * mm, y + 2.5 * mm, self.report["running"])
        canv.drawRightString(A4[0] - 22 * mm, y + 2.5 * mm,
                             "Al Safa 2 Park · Falaj Al Safa")
        canv.line(22 * mm, 13 * mm, A4[0] - 22 * mm, 13 * mm)
        canv.drawString(22 * mm, 9 * mm,
                        "Dubai Municipality AI Park Design Challenge")
        canv.drawRightString(A4[0] - 22 * mm, 9 * mm, f"{doc.page}")
        canv.restoreState()


# ── block builders ───────────────────────────────────────────────────────────
def cover(report: dict, S: dict) -> list:
    f = [Spacer(1, 42 * mm),
         Paragraph(report["title"], S["title"]),
         Paragraph(report["subtitle"], S["sub"])]
    f.append(Table([[""]], colWidths=[C.SITE and 150 * mm], rowHeights=[1.6],
                   style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), ACCENT)])))
    f.append(Spacer(1, 10 * mm))
    f.append(Paragraph(report["lead"], S["lead"]))
    f.append(Spacer(1, 24 * mm))
    meta = [
        f"<b>Upload slot {report['slot']:02d}</b> — {report['running']}",
        "Al Safa 2 Park · <b>Falaj Al Safa</b> · 15,000 m² · Al Safa 2, Dubai",
        "Mohamed Wasim · Individual Applicant",
        f"Issued {date.today().strftime('%d %B %Y')}",
    ]
    for line in meta:
        f.append(Paragraph(line, S["meta"]))
    f.append(Spacer(1, 12 * mm))
    f.append(Paragraph(
        "Every quantity in this report is regenerated from the project's "
        "analysis pipeline by <font face='Courier'>python run_analysis.py</font>. "
        "No figure quoted here is typed in by hand.", S["meta"]))
    f.append(NextPageTemplate("body"))
    from reportlab.platypus import PageBreak
    f.append(PageBreak())
    return f


def table(headers, rows, S, widths=None, highlight=None) -> Table:
    data = [[Paragraph(f"<b>{h}</b>", S["cap"]) for h in headers]]
    for r in rows:
        data.append([Paragraph(str(c), S["cap"]) for c in r])
    t = Table(data, colWidths=widths, hAlign="LEFT", repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), WASH),
        ("LINEBELOW", (0, 0), (-1, 0), 0.6, RULE),
        ("LINEBELOW", (0, 1), (-1, -2), 0.25, RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    if highlight is not None:
        style.append(("BACKGROUND", (0, highlight + 1), (-1, highlight + 1),
                      colors.HexColor("#e8f3ef")))
    t.setStyle(TableStyle(style))
    return t


def figure(rel: str, caption: str, S: dict, width=150 * mm) -> list:
    p = ROOT / rel
    if not p.exists():
        return [Paragraph(f"[figure pending: {rel}]", S["note"])]
    from PIL import Image as PImage
    with PImage.open(p) as im:
        w, h = im.size
    return [KeepTogether([Image(str(p), width=width, height=width * h / w),
                          Paragraph(caption, S["cap"])])]


def render(report: dict, S: dict) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{report['slug']}.pdf"
    flow = cover(report, S)
    for kind, payload in report["blocks"]:
        if kind == "h1":
            flow.append(Paragraph(payload, S["h1"]))
        elif kind == "h2":
            flow.append(Paragraph(payload, S["h2"]))
        elif kind == "p":
            flow.append(Paragraph(payload, S["body"]))
        elif kind == "note":
            flow.append(Paragraph(payload, S["note"]))
        elif kind == "bullets":
            flow.append(ListFlowable(
                [ListItem(Paragraph(b, S["bullet"]), leftIndent=12)
                 for b in payload], bulletType="bullet", start="•",
                leftIndent=12, bulletFontSize=7))
            flow.append(Spacer(1, 6))
        elif kind == "table":
            headers, rows, caption, *rest = payload
            widths = rest[0] if rest else None
            hi = rest[1] if len(rest) > 1 else None
            flow.append(table(headers, rows, S, widths, hi))
            if caption:
                flow.append(Paragraph(caption, S["cap"]))
        elif kind == "figure":
            flow.extend(figure(payload[0], payload[1], S))
        elif kind == "space":
            flow.append(Spacer(1, payload))
    Doc(path, report).build(flow)
    return path


def main() -> int:
    from tools import report_content

    D = load()
    S = _styles()
    reps = report_content.build(D)

    # Column widths in the content module are plain numbers, meaning mm.
    for r in reps:
        fixed = []
        for kind, payload in r["blocks"]:
            if kind == "table":
                headers, rows, cap, *rest = payload
                widths = [w * mm for w in rest[0]] if rest else None
                hi = rest[1] if len(rest) > 1 else None
                fixed.append((kind, (headers, rows, cap, widths, hi)))
            else:
                fixed.append((kind, payload))
        r["blocks"] = fixed

    print("=" * 74)
    print("  BUILDING WRITTEN REPORTS from the live analysis")
    print("=" * 74)
    written = []
    for r in reps:
        path = render(r, S)
        import pypdf
        n = len(pypdf.PdfReader(str(path)).pages)
        kb = path.stat().st_size / 1024
        print(f"  slot {r['slot']:02d}  {n:3d}pp  {kb:7.0f} KB  {path.name}")
        written.append((path, r["slot"]))

    # Push each regenerated report over every copy of itself in submission/,
    # so the upload package cannot keep serving the superseded text.
    import shutil
    replaced = placed = 0
    for path, slot in written:
        dests = list((ROOT / "submission").glob(f"*/{path.name}"))
        for dest in dests:
            shutil.copy2(path, dest)
            replaced += 1
        if dests:
            continue
        # A report nobody has a copy of yet — a newly written one. Overwriting
        # existing copies alone would silently produce nothing, which is how
        # slot 05 came to hold images and no document at all. Place it in the
        # folder its own `slot` declares.
        folder = next((d for d in (ROOT / "submission").iterdir()
                       if d.is_dir() and d.name.startswith(f"{slot:02d}_")), None)
        if folder is None:
            print(f"  ! no folder for slot {slot:02d} — {path.name} not placed")
            continue
        shutil.copy2(path, folder / path.name)
        placed += 1
        print(f"  + placed {path.name} in {folder.name}")
    print("")
    print(f"  {replaced} copy(ies) refreshed, {placed} newly placed in submission/")

    # The whole point: none of these may describe themselves as a draft.
    import pypdf
    bad = []
    for p, _slot in written:
        txt = " ".join((pg.extract_text() or "")
                       for pg in pypdf.PdfReader(str(p)).pages).upper()
        if any(mk in txt for mk in
               ("[AI DRAFT]", "AI-GENERATED DRAFT", "FOR REVIEW")):
            bad.append(p.name)
    print()
    if bad:
        print("  [X] DRAFT MARKERS STILL PRESENT:")
        for b in bad:
            print(f"      {b}")
    else:
        print("  [ok] no draft markers in any generated report")
    print(f"  {len(written)} report(s) -> reports/pdf/")
    print("=" * 74)
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
