from pathlib import Path

p = Path("tools/build_submission_pdfs.py")
t = p.read_text(encoding="utf-8")

old_cta = """    # ── portal call-to-action — big, obvious, clickable, not buried in a
    # panel further down the page. This is the single most important link in
    # the document: everything else in it can be checked by clicking here.
    # Two lines deep, and the address set large on its own. The whole
    # submission's claim is that any figure in it can be checked, and this is
    # the door to that — at 10.5 pt tucked beside a label it read as a footnote.
    cta_h = 19 * mm
    c.setFillColor(TEAL)
    c.roundRect(x, y - cta_h, inner, cta_h, 2 * mm, stroke=0, fill=1)
    c.setFillColor(mix(TEAL, PAPER, 0.30))
    c.roundRect(x, y - cta_h, 2.4 * mm, cta_h, 1.2 * mm, stroke=0, fill=1)

    # A drawn triangle, not a Unicode glyph — "▶" isn't in the base-14 PDF
    # font encoding and rendered as an empty box.
    ty = y - 6.4 * mm
    c.setFillColor(PAPER)
    p = c.beginPath()
    p.moveTo(x + 8 * mm, ty + 1.7 * mm)
    p.lineTo(x + 8 * mm, ty - 1.7 * mm)
    p.lineTo(x + 11.2 * mm, ty)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x + 14.5 * mm, y - 5.4 * mm,
                 "VISIT THE LIVE PROJECT PORTAL")
    c.setFont("Helvetica-Bold", 17)
    c.drawString(x + 8 * mm, y - 14 * mm, PORTAL_URL.replace("https://", ""))
    c.linkURL(PORTAL_URL, (x, y - cta_h, w - 18 * mm, y), relative=0)
    y -= cta_h + 7 * mm"""

new_cta = """    # ── portal call-to-action — big, obvious, clickable ─────────────────────
    if slot["n"] == 12:
        film_url = f"{PORTAL_URL}submission/12_Concept_Animation_Video/concept_film_hero.html"
        v_h = 24 * mm
        c.setFillColor(HexColor("#8B1E2B"))
        c.roundRect(x, y - v_h, inner, v_h, 2 * mm, stroke=0, fill=1)
        c.setFillColor(AMBER)
        c.roundRect(x, y - v_h, 2.8 * mm, v_h, 1.4 * mm, stroke=0, fill=1)

        ty = y - 7.5 * mm
        c.setFillColor(AMBER)
        p = c.beginPath()
        p.moveTo(x + 8 * mm, ty + 2.5 * mm)
        p.lineTo(x + 8 * mm, ty - 2.5 * mm)
        p.lineTo(x + 13 * mm, ty)
        p.close()
        c.drawPath(p, fill=1, stroke=0)

        c.setFillColor(PAPER)
        c.setFont("Helvetica-Bold", 9.5)
        c.drawString(x + 16 * mm, y - 6.5 * mm, "WATCH THE 60-SECOND CONCEPT ANIMATION FILM ONLINE (4K)")
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(AMBER)
        c.drawString(x + 8 * mm, y - 14.5 * mm, film_url.replace("https://", ""))
        c.setFont("Helvetica", 7.5)
        c.setFillColor(PAPER)
        c.drawString(x + 8 * mm, y - 20.5 * mm, "VISIT THE LIVE PROJECT PORTAL: " + PORTAL_URL.replace("https://", ""))
        c.linkURL(film_url, (x, y - v_h, w - 18 * mm, y), relative=0)
        y -= v_h + 6 * mm

    cta_h = 19 * mm
    c.setFillColor(TEAL)
    c.roundRect(x, y - cta_h, inner, cta_h, 2 * mm, stroke=0, fill=1)
    c.setFillColor(mix(TEAL, PAPER, 0.30))
    c.roundRect(x, y - cta_h, 2.4 * mm, cta_h, 1.2 * mm, stroke=0, fill=1)

    ty = y - 6.4 * mm
    c.setFillColor(PAPER)
    p = c.beginPath()
    p.moveTo(x + 8 * mm, ty + 1.7 * mm)
    p.lineTo(x + 8 * mm, ty - 1.7 * mm)
    p.lineTo(x + 11.2 * mm, ty)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x + 14.5 * mm, y - 5.4 * mm,
                 "VISIT THE LIVE PROJECT PORTAL")
    c.setFont("Helvetica-Bold", 17)
    c.drawString(x + 8 * mm, y - 14 * mm, PORTAL_URL.replace("https://", ""))
    c.linkURL(PORTAL_URL, (x, y - cta_h, w - 18 * mm, y), relative=0)
    y -= cta_h + 7 * mm"""

assert old_cta in t, "old_cta block not found"
t = t.replace(old_cta, new_cta, 1)
p.write_text(t, encoding="utf-8")
print("Updated build_submission_pdfs.py with Slot 12 Video banner!")
