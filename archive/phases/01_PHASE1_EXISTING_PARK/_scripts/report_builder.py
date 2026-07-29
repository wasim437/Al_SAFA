"""
Shared PDF report builder for Al Safa 2 Park - Phase 1 Analysis Documents.
Produces a consistently designed PDF: cover header, sections, tables,
embedded chart images, and a "Program Proof" code-reference appendix
showing the exact Python script that generated the analysis.
"""

import os
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Image,
    Table, TableStyle, NextPageTemplate, PageBreak, HRFlowable, ListFlowable, ListItem
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER

NAVY = colors.HexColor("#0B1F3A")
ACCENT = colors.HexColor("#C8A24A")
GREY = colors.HexColor("#555555")
LIGHT_BG = colors.HexColor("#F4F5F7")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="ReportTitle", fontSize=22, leading=26, textColor=NAVY,
                           fontName="Helvetica-Bold", spaceAfter=6))
styles.add(ParagraphStyle(name="ReportSubtitle", fontSize=12, leading=16, textColor=GREY,
                           fontName="Helvetica", spaceAfter=14))
styles.add(ParagraphStyle(name="SectionHeading", fontSize=14, leading=18, textColor=NAVY,
                           fontName="Helvetica-Bold", spaceBefore=14, spaceAfter=8))
styles.add(ParagraphStyle(name="Body", fontSize=9.7, leading=14, textColor=colors.HexColor("#222222"),
                           fontName="Helvetica", spaceAfter=6, alignment=TA_LEFT))
styles.add(ParagraphStyle(name="BodyBold", parent=styles["Body"], fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="Caption", fontSize=8.3, leading=11, textColor=GREY,
                           fontName="Helvetica-Oblique", alignment=TA_CENTER, spaceAfter=10))
styles.add(ParagraphStyle(name="CodeBlock", fontSize=7.6, leading=10.5, fontName="Courier",
                           textColor=colors.HexColor("#1a1a1a"), backColor=LIGHT_BG,
                           borderPadding=6, spaceAfter=4))
styles.add(ParagraphStyle(name="FooterText", fontSize=7.5, textColor=GREY, alignment=TA_CENTER))

# Allowed ReportLab mini-XML tags used intentionally throughout this project's
# section text (as opening/closing pairs) - anything else gets escaped.
_ALLOWED_TAGS = ("b", "i", "u", "sub", "sup", "br", "font", "para")
_TAG_RE = re.compile(r"</?(" + "|".join(_ALLOWED_TAGS) + r")(?:\s[^>]*)?/?>", re.IGNORECASE)
_ENTITY_RE = re.compile(r"&(#\d+|#x[0-9a-fA-F]+|amp|lt|gt|quot|apos|nbsp|ndash|mdash|rsquo|lsquo|hellip|deg|ge|le);")

# Unicode characters with no glyph in core Helvetica/Times - map to safe
# equivalents so they never render as a black-box "notdef" glyph.
_UNSUPPORTED_CHARS = {
    "₂": "2",       # subscript 2 (e.g. "CO2")
    "₁": "1",
    "₃": "3",
    "³": "3",       # superscript 3 (e.g. "m3")
    "²": "2",       # superscript 2
}


def _sanitize(text):
    """Make raw section text safe for ReportLab's Paragraph mini-XML parser.

    Escapes bare '&' that aren't part of a real entity, escapes stray '<'/'>'
    that aren't one of our allowed formatting tags, and swaps unicode chars
    with no glyph in the core PDF fonts for safe ASCII equivalents. This lets
    every gen_pdf_*.py script write plain, natural text/HTML-ish markup
    without hand-escaping each one, while keeping intentional <b>/<i> tags working.
    """
    if not isinstance(text, str):
        text = str(text)
    for bad, good in _UNSUPPORTED_CHARS.items():
        text = text.replace(bad, good)
    # Protect allowed tags and real entities by temporarily replacing them,
    # escaping everything else, then restoring the protected pieces.
    placeholders = []

    def _protect(m):
        placeholders.append(m.group(0))
        return f"\x00{len(placeholders) - 1}\x00"

    protected = _TAG_RE.sub(_protect, text)
    protected = _ENTITY_RE.sub(_protect, protected)
    protected = protected.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    def _restore(m):
        return placeholders[int(m.group(1))]

    return re.sub(r"\x00(\d+)\x00", _restore, protected)


def _header_footer(canvas, doc, phase_tag, title):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(NAVY)
    canvas.rect(0, h - 1.6 * cm, w, 1.6 * cm, fill=1, stroke=0)

    # Left: fixed brand. Right: the phase tag. A guaranteed gap between them
    # prevents the overlap seen previously.
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 9)
    canvas.drawString(1.5 * cm, h - 1.02 * cm, "AL SAFA 2 PARK — AI DESIGN CHALLENGE")
    canvas.setFillColor(ACCENT)
    canvas.setFont("Helvetica-Bold", 8)
    # Shrink the tag's font size (rather than truncate mid-word) until it fits
    # the space right of the brand text, so long tags stay fully readable.
    max_tag_w = w - 3.0 * cm - canvas.stringWidth("AL SAFA 2 PARK — AI DESIGN CHALLENGE", "Helvetica-Bold", 9)
    tag_font_size = 8
    while tag_font_size > 5.5 and canvas.stringWidth(phase_tag, "Helvetica-Bold", tag_font_size) > max_tag_w:
        tag_font_size -= 0.5
    canvas.setFont("Helvetica-Bold", tag_font_size)
    canvas.drawRightString(w - 1.5 * cm, h - 1.02 * cm, phase_tag)

    canvas.setFillColor(ACCENT)
    canvas.rect(0, h - 1.65 * cm, w, 0.05 * cm, fill=1, stroke=0)

    canvas.setFillColor(GREY)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(1.5 * cm, 1.0 * cm, "Dubai Municipality AI Park Design Challenge — Al Safa 2 Park")
    canvas.drawRightString(w - 1.5 * cm, 1.0 * cm, f"Page {doc.page}")
    canvas.restoreState()


def build_report(output_path, phase_tag, title, subtitle, sections, code_ref=None, script_name=None):
    """
    sections: list of dicts, each one of:
      {"type": "heading", "text": "..."}
      {"type": "para", "text": "..."}
      {"type": "bullets", "items": [...]}
      {"type": "table", "header": [...], "rows": [[...]], "col_widths": [...]}
      {"type": "image", "path": "...", "caption": "...", "width_cm": 16}
      {"type": "spacer", "h_cm": 0.5}
    code_ref: raw python source text to embed as "Program Proof" appendix
    """
    doc = BaseDocTemplate(output_path, pagesize=A4,
                           topMargin=2.1 * cm, bottomMargin=1.6 * cm,
                           leftMargin=1.5 * cm, rightMargin=1.5 * cm)
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")

    def _on_page(canvas, d):
        _header_footer(canvas, d, phase_tag, title)

    doc.addPageTemplates([PageTemplate(id="main", frames=frame, onPage=_on_page)])

    story = []
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph(_sanitize(title), styles["ReportTitle"]))
    story.append(Paragraph(_sanitize(subtitle), styles["ReportSubtitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=10))

    for s in sections:
        t = s["type"]
        if t == "heading":
            story.append(Paragraph(_sanitize(s["text"]), styles["SectionHeading"]))
        elif t == "para":
            story.append(Paragraph(_sanitize(s["text"]), styles["Body"]))
        elif t == "bullets":
            items = [ListItem(Paragraph(_sanitize(it), styles["Body"]), leftIndent=8) for it in s["items"]]
            story.append(ListFlowable(items, bulletType="bullet", start="•", leftIndent=10))
            story.append(Spacer(1, 0.2 * cm))
        elif t == "table":
            header = s["header"]
            rows = s["rows"]
            ncol = len(header)
            avail = doc.width  # usable width between margins

            # Column widths: use given ratios if provided, else weight by AVERAGE
            # cell text length per column (not the single longest cell - that let
            # one long narrative cell in another column starve a short-label
            # column of width, forcing mid-word character-splitting). Then apply
            # a minimum width based on the column's longest WORD so no single
            # word is ever forced to wrap character-by-character, and scale the
            # rest to exactly fit the page.
            given = s.get("col_widths")
            if given and len(given) == ncol:
                weights = list(given)
                col_widths = [avail * w / float(sum(weights)) for w in weights]
            else:
                import re
                avg_len = []
                min_word_chars = []
                for c in range(ncol):
                    cell_texts = [str(header[c])] + [str(r[c]) if c < len(r) else "" for r in rows]
                    lens = [len(re.sub(r"<[^>]+>", "", x)) for x in cell_texts]
                    avg_len.append(max(4, sum(lens) / len(lens)))
                    words = []
                    for x in cell_texts:
                        plain = re.sub(r"<[^>]+>", "", x)
                        words.extend(plain.replace("/", " ").split())
                    min_word_chars.append(max((len(w) for w in words), default=4))

                total_w = float(sum(avg_len))
                col_widths = [avail * w / total_w for w in avg_len]

                # Enforce a floor: wide enough for the longest word at ~7.8pt
                # Helvetica (~4.4pt/char) plus cell padding (8pt total).
                floor_widths = [mw * 4.4 + 8 for mw in min_word_chars]
                deficit = sum(max(0, f - c) for f, c in zip(floor_widths, col_widths))
                if deficit > 0:
                    # Raise under-floor columns to their floor, shrink the
                    # remaining columns proportionally to absorb the difference.
                    boosted = [max(c, f) for c, f in zip(col_widths, floor_widths)]
                    over_budget = sum(boosted) - avail
                    if over_budget > 0:
                        flexible_idx = [i for i in range(ncol) if col_widths[i] > floor_widths[i]]
                        flexible_total = sum(col_widths[i] for i in flexible_idx) or 1
                        for i in flexible_idx:
                            shrink = over_budget * (col_widths[i] / flexible_total)
                            boosted[i] = max(floor_widths[i], col_widths[i] - shrink)
                    col_widths = boosted
                # Final safety scale so the table never exceeds the page width.
                scale = avail / sum(col_widths)
                if scale < 1:
                    col_widths = [w * scale for w in col_widths]

            # Wrap EVERY cell in a Paragraph so text flows within its column
            # instead of forcing the column wider than the page.
            hstyle = ParagraphStyle("th", parent=styles["Body"], fontName="Helvetica-Bold",
                                    textColor=colors.white, fontSize=7.8, leading=10)
            cstyle = ParagraphStyle("td", parent=styles["Body"], fontSize=7.8, leading=10, spaceAfter=0)

            def cell(x, st):
                return Paragraph(_sanitize(x), st)

            data = [[cell(h, hstyle) for h in header]]
            for r in rows:
                data.append([cell(r[c] if c < len(r) else "", cstyle) for c in range(ncol)])

            tbl = Table(data, colWidths=col_widths, repeatRows=1)
            tbl.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CCCCCC")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ]))
            story.append(tbl)
            story.append(Spacer(1, 0.3 * cm))
        elif t == "image":
            img_path = s["path"]
            if os.path.exists(img_path):
                width = s.get("width_cm", 16) * cm
                from PIL import Image as PILImage
                with PILImage.open(img_path) as im:
                    iw, ih = im.size
                height = width * ih / iw
                story.append(Image(img_path, width=width, height=height))
                if s.get("caption"):
                    story.append(Paragraph(_sanitize(s["caption"]), styles["Caption"]))
            else:
                story.append(Paragraph(f"[Missing image: {img_path}]", styles["Body"]))
        elif t == "spacer":
            story.append(Spacer(1, s.get("h_cm", 0.5) * cm))

    # --- Program Proof appendix ---
    if code_ref:
        story.append(PageBreak())
        story.append(Paragraph("Appendix — Program Proof (Source Code)", styles["SectionHeading"]))
        story.append(Paragraph(
            f"The analysis, figures, and tables in this report were generated by the Python "
            f"script <b>{script_name}</b> below. Re-running this script reproduces identical "
            f"outputs — nothing in this report was manually estimated or invented.",
            styles["Body"]))
        story.append(Spacer(1, 0.2 * cm))
        for line in code_ref.splitlines():
            safe = (line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")) or " "
            story.append(Paragraph(safe, styles["CodeBlock"]))

    doc.build(story)
    print(f"Saved PDF: {output_path}")
