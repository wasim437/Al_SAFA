"""
Phase 5.3 - Circulation & Accessibility Diagram (code-generated)
Overlays the movement network (pedestrian spine, perimeter loop, cyclist,
service/emergency access, entry points) on the masterplan zone footprint.
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.lines import Line2D

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "..", "outputs")
with open(os.path.join(OUT, "zoning_area_schedule.json")) as f:
    pass  # confirm exists

SITE_W, SITE_H = 150.0, 100.0
fig, ax = plt.subplots(figsize=(15, 10))
ax.add_patch(patches.Rectangle((0,0), SITE_W, SITE_H, fill=True, facecolor="#f0efe9", ec="black", lw=2))

# Room footprints (light, for context)
rooms = [
    (14,58,32,34),(48,58,26,34),(76,58,36,34),(114,58,24,34),
    (14,8,32,34),(48,8,26,34),(76,8,22,34),(100,8,38,34),
]
for (x,y,w,h) in rooms:
    ax.add_patch(patches.Rectangle((x,y),w,h, facecolor="#dfe7df", ec="#b8c4b8", lw=1))

# --- Pedestrian Shaded Spine (thick blue) ---
ax.plot([2,148],[50,50], color="#1f6f8b", lw=10, solid_capstyle="round", label="_", zorder=3)
# --- Perimeter jogging/walking loop (green dashed) ---
loop = patches.Rectangle((6,6), SITE_W-12, SITE_H-12, fill=False, ec="#2a9d40", lw=3, ls="--", zorder=3)
ax.add_patch(loop)
# --- Secondary cross-links (thin blue) from spine into each room ---
for (x,y,w,h) in rooms:
    cx = x+w/2
    ax.plot([cx,cx],[50, y+ (h if y>50 else 0)], color="#1f6f8b", lw=2.5, ls=":", zorder=2)
# --- Cyclist route (orange, shares loop) marker ---
ax.plot([6,144],[6,6], color="#e76f51", lw=3, zorder=4)
# --- Service/emergency access (red) from both plazas behind kiosks ---
ax.annotate("", xy=(88,42), xytext=(150,50), arrowprops=dict(arrowstyle="->", color="#c1121f", lw=2.5))
ax.annotate("", xy=(0,50), xytext=(14,50), arrowprops=dict(arrowstyle="->", color="#c1121f", lw=2.5))

# --- Entry points ---
for (ex,ey,lbl) in [(0,50,"MAIN\nENTRY (W)"),(150,50,"SECONDARY\nENTRY (E)")]:
    ax.add_patch(patches.Circle((ex,ey),3.5, facecolor="#ffd166", ec="black", zorder=6))
    ax.text(ex, ey-9, lbl, ha="center", fontsize=8, fontweight="bold")

# North arrow
ax.annotate("N", xy=(SITE_W+3, SITE_H-4), fontsize=13, fontweight="bold", ha="center")
ax.annotate("", xy=(SITE_W+3, SITE_H-7), xytext=(SITE_W+3, SITE_H-14), arrowprops=dict(arrowstyle="-|>", lw=2))

legend = [
    Line2D([0],[0], color="#1f6f8b", lw=8, label="Pedestrian Shaded Spine (primary, 100% shaded, step-free)"),
    Line2D([0],[0], color="#1f6f8b", lw=2.5, ls=":", label="Secondary pedestrian cross-links to rooms"),
    Line2D([0],[0], color="#2a9d40", lw=3, ls="--", label="Perimeter jogging / walking loop"),
    Line2D([0],[0], color="#e76f51", lw=3, label="Cyclist route (shared, off-peak)"),
    Line2D([0],[0], color="#c1121f", lw=2.5, label="Service / emergency vehicle access"),
    Line2D([0],[0], marker="o", color="w", markerfacecolor="#ffd166", markersize=12, label="Entry point"),
]
ax.legend(handles=legend, loc="upper center", bbox_to_anchor=(0.5,-0.02), ncol=2, fontsize=9, frameon=False)

ax.set_xlim(-6, SITE_W+8); ax.set_ylim(-14, SITE_H+6)
ax.set_aspect("equal"); ax.axis("off")
ax.set_title("Al Safa 2 Park — Circulation & Accessibility Diagram (Phase 5.3 / 5.7)",
             fontsize=14, fontweight="bold")
plt.tight_layout()
fig.savefig(os.path.join(OUT, "circulation_diagram.png"), dpi=160, bbox_inches="tight")
plt.close(fig)
print("Saved: circulation_diagram.png")
