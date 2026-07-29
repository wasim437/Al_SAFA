#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
05_build_visualizations_pdf.py — Compiles Slot 05 (3D & Spatial Visualizations) PDF
Builds a high-res PDF presentation sheet for Slot 05 meeting Dubai Municipality's
exact upload form requirement (PDF format).
"""

import os
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, "..", "10.2_Required_Files", "05_3D_Spatial_Visualizations")
os.makedirs(OUT_DIR, exist_ok=True)

PDF_PATH = os.path.join(OUT_DIR, "Al_Safa_2_Park_3D_Spatial_Visualizations.pdf")
IMG_DIR = os.path.join(BASE_DIR, "..", "..", "09_PHASE9_AI_WORKFLOW_AND_VISUALIZATION", "outputs")
BOARD_DIR = os.path.join(BASE_DIR, "..", "..", "09_PHASE9_AI_WORKFLOW_AND_VISUALIZATION", "9.9_Presentation_Graphics")

def build_pdf():
    # Landscape A4 for presentation sheets (297mm x 210mm = 841.89 x 595.27 points)
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=landscape(A4),
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#1a2b3c'),
        alignment=1, # Center
        spaceAfter=12
    )

    subtitle_style = ParagraphStyle(
        'CoverSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#4a5568'),
        alignment=1,
        spaceAfter=24
    )

    heading_style = ParagraphStyle(
        'PageHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#1a365d'),
        spaceAfter=6
    )

    caption_style = ParagraphStyle(
        'Caption',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#4a5568'),
        spaceAfter=8
    )

    story = []

    # --- Cover Page ---
    story.append(Spacer(1, 100))
    story.append(Paragraph("AL SAFA 2 PARK REDESIGN", title_style))
    story.append(Paragraph("<b>3D &amp; Spatial Visualizations Package</b><br/>Dubai Municipality AI Park Design Challenge", subtitle_style))
    story.append(Spacer(1, 40))

    meta_text = """
    <b>Applicant:</b> MOHAMED WASIM (Individual Applicant)<br/>
    <b>Design Concept:</b> The Shaded Spine<br/>
    <b>Site Area:</b> 15,000 m² (Al Safa 2, Dubai)<br/>
    <b>Phase Focus:</b> Phase 9 — AI Workflow &amp; High-Resolution Architectural Renders<br/>
    <b>Submission Deadline:</b> 15 August 2026
    """
    story.append(Paragraph(meta_text, ParagraphStyle('Meta', parent=styles['Normal'], fontName='Helvetica', fontSize=11, leading=16, alignment=1)))
    story.append(PageBreak())

    # Renders list: (filename, title, description, dir_path)
    slides = [
        ("masterplan_aerial_golden_hour.jpg", "Aerial Masterplan — Golden Hour View",
         "Overview of the full 15,000 m² site showing the central Shaded Spine, zoned activity rooms, native tree groves, and perimeter buffers.", IMG_DIR),
        ("aerial_day_view_1784970538631.jpg", "Midday Solar & Shade Simulation Aerial",
         "Near-vertical summer sun analysis illustrating the high shade efficiency of the engineered parametric ETFE canopy.", IMG_DIR),
        ("spine_corridor_interior.jpg", "The Shaded Spine Promenade — Interior View",
         "Pedestrian eye-level view along the 100% shaded central spine walkway connecting all 13 functional park zones.", IMG_DIR),
        ("eyelevel_spine_1784970552956.jpg", "Pedestrian Eye-Level View & Native Canopy",
         "Human-scale perspective highlighting native Ghaf tree canopy integration, timber structures, and permeable paving.", IMG_DIR),
        ("night_plaza_render_1784970565232.jpg", "Night Activation — Community Plaza",
         "Illuminated plaza view showcasing the 18:00–23:00 evening activation strategy for community events and social gatherings.", IMG_DIR),
        ("thermal_comfort_heatmap.jpg", "Thermal Comfort & Microclimate Heatmap",
         "Quantitative thermal comfort visualization demonstrating a -5.2°C Universal Thermal Climate Index (UTCI) reduction along the spine.", IMG_DIR),
        ("presentation_board_1_concept.png", "Jury Presentation Board 1 — Concept & Master Plan",
         "A1 competition presentation board covering site analysis, concept evolution, zoning geometry, and circulation strategy.", BOARD_DIR),
        ("presentation_board_2_evidence.png", "Jury Presentation Board 2 — Evidence & Performance",
         "A1 competition presentation board highlighting climate evidence, pvlib solar geometry, water budget, carbon sink, and cost feasibility.", BOARD_DIR)
    ]

    # Target dimensions for landscape A4 (width ~770pt, height ~470pt available)
    max_w = 750
    max_h = 440

    for fname, ptitle, pdesc, dpath in slides:
        ipath = os.path.join(dpath, fname)
        if os.path.exists(ipath):
            story.append(Paragraph(ptitle, heading_style))
            story.append(Paragraph(pdesc, caption_style))
            story.append(Image(ipath, width=max_w, height=max_h, kind='proportional'))
            story.append(PageBreak())

    doc.build(story)
    print(f"Successfully generated: {PDF_PATH}")

if __name__ == "__main__":
    build_pdf()
