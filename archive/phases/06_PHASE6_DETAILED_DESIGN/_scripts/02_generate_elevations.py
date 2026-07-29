"""
Phase 6.9 - Elevation Drawings (code-generated, to scale)
Draws two key elevations: (1) the Main Entrance Gateway, and (2) a long
elevation of the Shaded Spine canopy run. Dimensions are consistent with the
Phase 5 masterplan and Phase 6 section.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUT = os.path.join(os.path.dirname(__file__), "..", "outputs")
os.makedirs(OUT, exist_ok=True)

# ---------------- Elevation 1: Main Entrance Gateway ----------------
fig, ax = plt.subplots(figsize=(13, 7))
ax.plot([-2, 14], [0, 0], color="#6b4f3a", lw=3)  # ground

# Two gateway portal columns + a signage beam (welcoming threshold)
for cx in [1, 11]:
    ax.add_patch(patches.Rectangle((cx-0.25, 0), 0.5, 4.5, facecolor="#8d99ae", ec="black"))
# Beam
ax.add_patch(patches.Rectangle((0.75, 4.3), 10.5, 0.7, facecolor="#2f3e46", ec="black"))
ax.text(6, 4.65, "AL SAFA 2 PARK", ha="center", va="center", color="white", fontsize=13, fontweight="bold")
# Shade wings sloping down from beam
ax.add_patch(patches.Polygon([(0.75,4.3),(0.75,3.6),(3,4.0)], closed=True, facecolor="#40916c", ec="black", alpha=0.8))
ax.add_patch(patches.Polygon([(11.25,4.3),(11.25,3.6),(9,4.0)], closed=True, facecolor="#40916c", ec="black", alpha=0.8))
# Low planters flanking entry
ax.add_patch(patches.Rectangle((-1.5,0),1.2,0.6, facecolor="#2d6a4f", ec="black"))
ax.add_patch(patches.Rectangle((12.3,0),1.2,0.6, facecolor="#2d6a4f", ec="black"))
# Trees behind
for tx in [-1, 12.9]:
    ax.add_patch(patches.Circle((tx,2.2),1.0, facecolor="#1b4332", alpha=0.5))
    ax.plot([tx,tx],[0.6,1.4], color="#6b4f3a", lw=3)
# People for scale
for px in [4.5, 7.2]:
    ax.add_patch(patches.Circle((px,1.7),0.15, facecolor="#333"))
    ax.plot([px,px],[1.55,0.6], color="#333", lw=2.5)
# Dimension line
ax.annotate("", xy=(1,-0.7), xytext=(11,-0.7), arrowprops=dict(arrowstyle="<->"))
ax.text(6,-1.0,"~10 m gateway span", ha="center", fontsize=9)
ax.annotate("", xy=(13.7,0), xytext=(13.7,4.5), arrowprops=dict(arrowstyle="<->"))
ax.text(13.9,2.25,"4.5 m", rotation=90, va="center", fontsize=8)

ax.set_xlim(-2.5, 15)
ax.set_ylim(-1.6, 6)
ax.set_aspect("equal"); ax.axis("off")
ax.set_title("Al Safa 2 Park — Elevation 1: Main Entrance Gateway (to scale)", fontsize=13, fontweight="bold")
plt.tight_layout()
fig.savefig(os.path.join(OUT, "elevation_entrance_gateway.png"), dpi=170)
plt.close(fig)
print("Saved: elevation_entrance_gateway.png")

# ---------------- Elevation 2: Shaded Spine long elevation ----------------
fig, ax = plt.subplots(figsize=(16, 5))
SPAN = 60  # show a 60m run of the 126m spine
ax.plot([-2, SPAN+2], [0,0], color="#6b4f3a", lw=3)

# Repeating columns every ~6m carrying a continuous canopy at 5.5m
col_x = np.arange(0, SPAN+1, 6)
for cx in col_x:
    ax.add_patch(patches.Rectangle((cx-0.15,0),0.3,5.5, facecolor="#555", ec="black"))
# Continuous canopy band
ax.add_patch(patches.Rectangle((-1,5.5),SPAN+2,0.4, facecolor="#2f3e46", ec="black"))
# Slats texture
for sx in np.arange(-1, SPAN+1, 1.2):
    ax.plot([sx,sx],[5.45,5.9], color="#2f3e46", lw=1)
# Trees interspersed
rng = np.random.default_rng(7)
for tx in rng.uniform(2, SPAN-2, 7):
    ax.add_patch(patches.Circle((tx,3.2),1.4, facecolor="#1b4332", alpha=0.45))
    ax.plot([tx,tx],[0,1.8], color="#6b4f3a", lw=3)
# People
for px in rng.uniform(1, SPAN-1, 9):
    ax.add_patch(patches.Circle((px,1.7),0.13, facecolor="#333"))
    ax.plot([px,px],[1.57,0.6], color="#333", lw=2)
# Dimensions
ax.annotate("", xy=(0,-0.8), xytext=(6,-0.8), arrowprops=dict(arrowstyle="<->"))
ax.text(3,-1.15,"6 m bay", ha="center", fontsize=8)
ax.annotate("", xy=(SPAN+1.3,0), xytext=(SPAN+1.3,5.5), arrowprops=dict(arrowstyle="<->"))
ax.text(SPAN+1.6,2.75,"5.5 m", rotation=90, va="center", fontsize=8)

ax.set_xlim(-3, SPAN+4)
ax.set_ylim(-1.8, 7)
ax.set_aspect("equal"); ax.axis("off")
ax.set_title("Al Safa 2 Park — Elevation 2: Shaded Spine Canopy (60 m of the 126 m run, to scale)",
             fontsize=13, fontweight="bold")
plt.tight_layout()
fig.savefig(os.path.join(OUT, "elevation_shaded_spine_long.png"), dpi=170)
plt.close(fig)
print("Saved: elevation_shaded_spine_long.png")
