"""
Phase 9.9 - Competition Presentation Board (code-generated, A1 landscape)
Assembles the strongest visuals + headline numbers into a single professional
board, the way a jury first encounters the scheme. Two boards produced.
"""

import os
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.image as mpimg

BASE = os.path.join(os.path.dirname(__file__), "..", "..")
OUT = os.path.join(os.path.dirname(__file__), "..", "9.9_Presentation_Graphics")
os.makedirs(OUT, exist_ok=True)

NAVY = "#0B1F3A"; GOLD = "#C8A24A"

def imgpath(*p): return os.path.join(BASE, *p)

def load(path):
    return mpimg.imread(path) if os.path.exists(path) else None

def show(ax, path, title=None):
    im = load(path)
    ax.axis("off")
    if im is not None:
        ax.imshow(im)
    if title:
        ax.set_title(title, fontsize=10, fontweight="bold", color=NAVY, pad=4)

# ============ BOARD 1: Concept & Master Plan ============
fig = plt.figure(figsize=(23.4, 16.5), facecolor="white")  # A1 landscape ratio
gs = GridSpec(3, 3, figure=fig, height_ratios=[0.5, 2.2, 1.4], hspace=0.18, wspace=0.08)

# Header band
hdr = fig.add_axes([0, 0.93, 1, 0.07]); hdr.axis("off")
hdr.add_patch(plt.Rectangle((0,0),1,1, facecolor=NAVY, transform=hdr.transAxes))
hdr.text(0.012, 0.5, "AL SAFA 2 PARK  —  \"THE SHADED SPINE\"", color="white",
         fontsize=26, fontweight="bold", va="center", transform=hdr.transAxes)
hdr.text(0.988, 0.5, "Dubai Municipality AI Park Design Challenge  |  Board 1 of 2",
         color=GOLD, fontsize=13, va="center", ha="right", transform=hdr.transAxes)

ax_mp = fig.add_subplot(gs[1, :2]); show(ax_mp, imgpath("05_PHASE5_MASTERPLAN_DEVELOPMENT","outputs","masterplan_diagram.png"), "Master Plan (to scale, 15,000 m²)")
ax_day = fig.add_subplot(gs[1, 2]); show(ax_day, imgpath("09_PHASE9_AI_WORKFLOW_AND_VISUALIZATION","9.7_Renderings","Aerial","aerial_day.png"), "Aerial — Day")
ax_circ = fig.add_subplot(gs[2, 0]); show(ax_circ, imgpath("05_PHASE5_MASTERPLAN_DEVELOPMENT","outputs","circulation_diagram.png"), "Circulation & Accessibility")
ax_plant = fig.add_subplot(gs[2, 1]); show(ax_plant, imgpath("06_PHASE6_DETAILED_DESIGN","outputs","planting_plan.png"), "Planting Plan (131 trees)")
ax_sec = fig.add_subplot(gs[2, 2]); show(ax_sec, imgpath("06_PHASE6_DETAILED_DESIGN","outputs","section_shaded_spine.png"), "Section — Shaded Spine")

fig.savefig(os.path.join(OUT, "presentation_board_1_concept.png"), dpi=130, facecolor="white", bbox_inches="tight")
plt.close(fig)
print("Saved: presentation_board_1_concept.png")

# ============ BOARD 2: Evidence & Performance ============
fig = plt.figure(figsize=(23.4, 16.5), facecolor="white")
gs = GridSpec(3, 3, figure=fig, height_ratios=[0.5, 1.7, 1.7], hspace=0.22, wspace=0.1)

hdr = fig.add_axes([0, 0.93, 1, 0.07]); hdr.axis("off")
hdr.add_patch(plt.Rectangle((0,0),1,1, facecolor=NAVY, transform=hdr.transAxes))
hdr.text(0.012, 0.5, "EVIDENCE & PERFORMANCE  —  REAL DATA, COMPUTED PROOF", color="white",
         fontsize=24, fontweight="bold", va="center", transform=hdr.transAxes)
hdr.text(0.988, 0.5, "AI Park Design Challenge  |  Board 2 of 2", color=GOLD,
         fontsize=13, va="center", ha="right", transform=hdr.transAxes)

# Headline metric strip
strip = fig.add_axes([0.02, 0.845, 0.96, 0.06]); strip.axis("off")
metrics = [("99.2%", "annual shade on\nprimary spine"),
           ("AED 18.6M", "est. cost = 53%\nof 35M budget"),
           ("+3 months", "extra comfortable\nseason (shade)"),
           ("2.1 t/yr", "CO₂ sequestered\n(131 trees)"),
           ("7,640", "residents in\n10-min walk")]
for i,(big,small) in enumerate(metrics):
    x = i/len(metrics) + 0.008
    strip.text(x, 0.72, big, fontsize=22, fontweight="bold", color=NAVY, transform=strip.transAxes)
    strip.text(x, 0.05, small, fontsize=9.5, color="#444", transform=strip.transAxes)

ax1 = fig.add_subplot(gs[1,0]); show(ax1, imgpath("01_PHASE1_EXISTING_PARK","05_Climate_Analysis","outputs","fullyear_elevation_heatmap.png"), "Full-Year Solar (8,760 hrs, exact)")
ax2 = fig.add_subplot(gs[1,1]); show(ax2, imgpath("07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY","outputs","shade_coverage_simulation.png"), "Shade Simulation (3 seasons)")
ax3 = fig.add_subplot(gs[1,2]); show(ax3, imgpath("07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY","outputs","annual_shade_hours_by_zone.png"), "Annual Shade by Zone")
ax4 = fig.add_subplot(gs[2,0]); show(ax4, imgpath("07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY","outputs","thermal_comfort.png"), "Thermal Comfort (+3 comfortable months)")
ax5 = fig.add_subplot(gs[2,1]); show(ax5, imgpath("07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY","outputs","cost_breakdown.png"), "Cost Breakdown (real Dubai rates)")
ax6 = fig.add_subplot(gs[2,2]); show(ax6, imgpath("07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY","outputs","carbon_sequestration.png"), "Carbon (~2.1 t CO₂/yr)")

fig.savefig(os.path.join(OUT, "presentation_board_2_evidence.png"), dpi=130, facecolor="white", bbox_inches="tight")
plt.close(fig)
print("Saved: presentation_board_2_evidence.png")
