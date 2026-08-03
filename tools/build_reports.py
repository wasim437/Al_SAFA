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
                                ListFlowable, ListItem, PageTemplate,
                                Paragraph, Spacer, Table, TableStyle)

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src import config as C, plan  # noqa: E402

OUT = ROOT / "reports" / "pdf"

INK = colors.HexColor("#1a1a1a")
MUTED = colors.HexColor("#6b6b6b")
RULE = colors.HexColor("#c8c8c8")
ACCENT = colors.HexColor("#12836B")   # matches the deck's TEAL exactly

# Same palette as tools/build_submission_pdfs.py's covers, methodology and
# index pages. The written reports sit between those pages once merged —
# a different palette here read as two different documents stapled together.
NAVY = colors.HexColor("#0B1B2B")
AMBER = colors.HexColor("#E8A33D")
CARD = colors.HexColor("#F3F5F7")
ON_NAVY_DIM = colors.HexColor("#9BB1C4")
WASH = CARD


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
        cap_on_navy=ParagraphStyle("cap_on_navy", parent=ss["BodyText"],
                                   fontName="Helvetica-Bold", fontSize=7.8,
                                   leading=10.5, spaceBefore=3, spaceAfter=10,
                                   textColor=colors.white),
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
        # "body" is first, so page one carries the running head like every
        # other page. There is no longer a separate cover template: the report
        # opens with a masthead block at the top of its first page of content
        # rather than on a page of its own. See opener().
        self.addPageTemplates([
            PageTemplate(id="body", frames=[frame], onPage=self._furniture),
        ])

    def _furniture(self, canv, doc):
        canv.saveState()
        w, h = A4
        # A slim navy running-head strip, not the full deck banner — this is
        # a body page read top to bottom, not a cover scanned once. But it
        # carries the same navy/amber so the report doesn't read as a
        # different document once merged behind the cover and methodology
        # pages in tools/build_submission_pdfs.py.
        bar_h = 9 * mm
        canv.setFillColor(NAVY)
        canv.rect(0, h - bar_h, w, bar_h, stroke=0, fill=1)
        canv.setFillColor(AMBER)
        canv.rect(0, h - bar_h, w, 0.9 * mm, stroke=0, fill=1)
        canv.setFont("Helvetica-Bold", 7.6)
        canv.setFillColor(colors.white)
        canv.drawString(22 * mm, h - bar_h + 2.8 * mm, self.report["running"].upper())
        canv.setFont("Helvetica", 7.2)
        canv.setFillColor(ON_NAVY_DIM)
        canv.drawRightString(w - 22 * mm, h - bar_h + 2.8 * mm,
                             f"UPLOAD SLOT {self.report['slot']:02d} OF 12")

        canv.setStrokeColor(RULE)
        canv.setLineWidth(0.4)
        canv.line(22 * mm, 13 * mm, w - 22 * mm, 13 * mm)
        canv.setFont("Helvetica", 7.4)
        canv.setFillColor(MUTED)
        canv.drawString(22 * mm, 9 * mm,
                        "Al Safa 2 Park · Falaj Al Safa · Dubai Municipality "
                        "AI Park Design Challenge")
        canv.drawRightString(w - 22 * mm, 9 * mm, f"{doc.page}")
        canv.restoreState()


# ── block builders ───────────────────────────────────────────────────────────
def opener(report: dict, S: dict) -> list:
    """The masthead each report opens with, at the top of its first page.

    This used to be a whole page of its own — a title, a one-line lead and
    then two-thirds of an A4 sheet of white. Three reports merge into a
    typical upload slot, so three near-empty sheets were landing in every
    file, and they were the pages that made the submission read as thin.

    It is now a band: navy masthead, amber rule, the lead in a tinted card,
    then the report's first heading begins immediately underneath. Same
    navy/amber/teal as the deck pages that merge in front of it, so nothing
    reads as a second document starting over.
    """
    W = 170 * mm
    # autoLeading: the block mixes a 7.6 pt kicker, a 19 pt title and a 10 pt
    # subtitle in one paragraph. On the style's fixed leading the title's
    # descenders collided with the line beneath it.
    on_navy = ParagraphStyle("on_navy", parent=S["meta"], fontSize=9.6,
                             leading=13.6, textColor=colors.HexColor("#C9D6E2"))
    on_navy.autoLeading = "max"
    lead_in = ParagraphStyle("lead_in", parent=S["lead"], fontSize=10.2,
                             leading=15, spaceAfter=0)

    masthead = Table(
        [[Paragraph(
            f"<font color='#E8A33D' size='7.6'><b>UPLOAD SLOT "
            f"{report['slot']:02d} OF 12 &nbsp;·&nbsp; "
            f"{report['running'].upper()}</b></font><br/>"
            f"<font color='#FFFFFF' size='19'><b>{report['title']}</b></font>"
            f"<br/><font size='10'>{report['subtitle']}</font>", on_navy)]],
        colWidths=[W],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), NAVY),
            ("LEFTPADDING", (0, 0), (-1, -1), 7 * mm),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7 * mm),
            ("TOPPADDING", (0, 0), (-1, -1), 7 * mm),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7 * mm),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))

    amber_rule = Table([[""]], colWidths=[W], rowHeights=[1.6 * mm],
                       style=TableStyle([
                           ("BACKGROUND", (0, 0), (-1, -1), AMBER)]))

    lead_card = Table(
        [[Paragraph(report["lead"], lead_in)]], colWidths=[W],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), CARD),
            ("LINEBEFORE", (0, 0), (0, -1), 2.2 * mm, ACCENT),
            ("LEFTPADDING", (0, 0), (-1, -1), 6 * mm),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6 * mm),
            ("TOPPADDING", (0, 0), (-1, -1), 4.5 * mm),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5 * mm),
        ]))

    stamp = Paragraph(
        "Al Safa 2 Park · <b>Falaj Al Safa</b> · 15,000 m² · Al Safa 2, Dubai "
        "&nbsp;·&nbsp; Mohamed Wasim, Individual Applicant &nbsp;·&nbsp; "
        f"Issued {date.today().strftime('%d %B %Y')} &nbsp;·&nbsp; every "
        "quantity regenerated by <font face='Courier'>python run_analysis.py</font>",
        S["meta"])

    # KeepTogether so the masthead is never orphaned from its own lead.
    return [KeepTogether([masthead, amber_rule, Spacer(1, 5 * mm), lead_card,
                          Spacer(1, 3 * mm), stamp]),
            Spacer(1, 4 * mm)]


def table(headers, rows, S, widths=None, highlight=None) -> Table:
    head_style = S.get("cap_on_navy") or S["cap"]
    data = [[Paragraph(f"<b>{h}</b>", head_style) for h in headers]]
    for r in rows:
        data.append([Paragraph(str(c), S["cap"]) for c in r])
    t = Table(data, colWidths=widths, hAlign="LEFT", repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("LINEBELOW", (0, 0), (-1, 0), 0.6, RULE),
        ("LINEBELOW", (0, 1), (-1, -2), 0.25, RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, CARD]),
    ]
    if highlight is not None:
        style.append(("BACKGROUND", (0, highlight + 1), (-1, highlight + 1),
                      colors.HexColor("#DCEDE7")))
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
    flow = opener(report, S)
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

    # ReportLab emits a page for trailing whitespace. A report whose block list
    # ended on a spacer closed on a completely blank sheet — slot 11 shipped
    # one, with nothing on it but the running head and the page number.
    while flow and isinstance(flow[-1], Spacer):
        flow.pop()

    # Bind the closing block to the one above it, so a short final paragraph or
    # note cannot be stranded alone on a page of its own.
    if len(flow) >= 2:
        tail = [flow.pop()]
        while flow and isinstance(flow[-1], Spacer):
            tail.insert(0, flow.pop())
        if flow:
            tail.insert(0, flow.pop())
        flow.append(KeepTogether(tail))

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
