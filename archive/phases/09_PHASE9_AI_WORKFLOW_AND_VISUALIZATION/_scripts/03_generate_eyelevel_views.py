"""
Phase 9.7 - Eye-Level 3D Perspective Views (code-generated)
Two person's-eye-view perspective sketches (brief asks for eye-level views):
  1. Looking down the Shaded Spine (the signature experience)
  2. Standing in the Community Plaza
Simple 1-point-perspective vector renders - schematic but genuine eye-level views.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUT = os.path.join(os.path.dirname(__file__), "..", "9.7_Renderings", "Eye_Level")
os.makedirs(OUT, exist_ok=True)

SKY = "#cfe3ee"; GROUND = "#d9cfbe"; CANOPY = "#2f3e46"; TREE = "#2d6a4f"

# ============ VIEW 1: Down the Shaded Spine ============
fig, ax = plt.subplots(figsize=(14, 8))
ax.add_patch(patches.Rectangle((0,3), 16, 6, facecolor=SKY))          # sky
ax.add_patch(patches.Rectangle((0,0), 16, 3.2, facecolor=GROUND))     # ground

# 1-point perspective vanishing point at centre horizon
vp = (8, 4.2)
# Path edges converging to VP
ax.add_patch(patches.Polygon([(1,0),(6.6,4.2),(9.4,4.2),(15,0)], closed=True, facecolor="#c9b79c", ec="#a99", zorder=2))
# Path centre line dashes
for t in np.linspace(0.05, 0.9, 8):
    y = t*4.2
    w = 0.25*(1-t)
    ax.add_patch(patches.Rectangle((8-w/2, y), w, 0.12*(1-t)+0.02, facecolor="white", zorder=3))

# Canopy overhead converging (the shade structure)
ax.add_patch(patches.Polygon([(0.5,9),(6.8,4.6),(9.2,4.6),(15.5,9)], closed=True, facecolor=CANOPY, alpha=0.85, zorder=4))
# Canopy slats (perspective lines)
for t in np.linspace(0.1, 0.85, 10):
    y = 4.6 + t*(9-4.6)
    xl = 6.8 - t*6.3; xr = 9.2 + t*6.3
    ax.plot([xl, xr], [y, y], color="#1d2b30", lw=1, zorder=5)
# Columns (pairs receding)
for i, t in enumerate(np.linspace(0.08, 0.7, 5)):
    scale = 1-t
    xL = 6.6 + t*(1-6.6); xR = 9.4 + t*(15-9.4)
    h = 4.2*scale + 0.3
    for cx in (xL, xR):
        ax.add_patch(patches.Rectangle((cx-0.08*scale, t*4.2), 0.16*scale, 4.6-t*4.2, facecolor="#555", zorder=6))

# Trees flanking
for side in (-1, 1):
    for t in np.linspace(0.05, 0.6, 4):
        scale = 1-t
        x = 8 + side*(6.5*scale + 0.5)
        y = t*4.2
        ax.add_patch(patches.Circle((x, y+1.2*scale), 0.9*scale, facecolor=TREE, alpha=0.75, zorder=3))
        ax.plot([x,x],[y, y+0.6*scale], color="#6b4f3a", lw=2*scale, zorder=3)

# People walking (scale cues)
for x, y, s in [(7.2,0.3,1.0),(8.8,0.5,0.85),(8.1,1.6,0.55),(7.8,2.4,0.4)]:
    ax.add_patch(patches.Circle((x, y+0.5*s), 0.12*s, facecolor="#333", zorder=7))
    ax.plot([x,x],[y+0.38*s, y], color="#333", lw=2.5*s, zorder=7)

ax.set_xlim(0,16); ax.set_ylim(0,9); ax.axis("off")
ax.set_title("Al Safa 2 Park — Eye-Level View 1: Looking Down the Shaded Spine",
             fontsize=14, fontweight="bold")
plt.tight_layout()
fig.savefig(os.path.join(OUT, "eyelevel_shaded_spine.png"), dpi=170)
plt.close(fig)
print("Saved: eyelevel_shaded_spine.png")

# ============ VIEW 2: Community Plaza ============
fig, ax = plt.subplots(figsize=(14, 8))
ax.add_patch(patches.Rectangle((0,3.2), 16, 6, facecolor=SKY))
ax.add_patch(patches.Rectangle((0,0), 16, 3.4, facecolor="#cbb89c"))  # plaza paving

# Plaza paving grid (perspective)
for t in np.linspace(0.05, 1, 7):
    y = t*3.4
    ax.plot([0,16],[y,y], color="#b3a184", lw=0.8)
for x in np.linspace(1,15,8):
    ax.plot([x, 8+(x-8)*0.25],[0,3.4], color="#b3a184", lw=0.6)

# Central shade pavilion
ax.add_patch(patches.Rectangle((5.5,3.4),5,0.4, facecolor=CANOPY, alpha=0.85))
for cx in (5.7, 10.3):
    ax.add_patch(patches.Rectangle((cx,1.0),0.18,2.8, facecolor="#555"))
# Feature tree cluster
for x in (3, 13):
    ax.add_patch(patches.Circle((x,3.0),1.4, facecolor=TREE, alpha=0.7))
    ax.plot([x,x],[1.2,2.2], color="#6b4f3a", lw=3)
# Kiosk on the right
ax.add_patch(patches.Rectangle((12.5,1.2),2.5,1.6, facecolor="#b08968", ec="black"))
ax.text(13.75,2.0,"KIOSK", ha="center", fontsize=8, color="white", fontweight="bold")
# Seating + people
for x,y,s in [(6,1.0,1.0),(7.5,1.2,0.95),(9,0.8,1.0),(10.5,1.4,0.8),(4.5,1.8,0.6)]:
    ax.add_patch(patches.Circle((x,y+0.5*s),0.13*s, facecolor="#333"))
    ax.plot([x,x],[y+0.37*s,y], color="#333", lw=2.5*s)
# Distant skyline hint
for bx,bw,bh in [(1,0.8,1.6),(2.2,0.6,2.0),(14,0.7,1.8)]:
    ax.add_patch(patches.Rectangle((bx,3.4),bw,bh, facecolor="#b8c6d0", alpha=0.5))

ax.set_xlim(0,16); ax.set_ylim(0,9); ax.axis("off")
ax.set_title("Al Safa 2 Park — Eye-Level View 2: Community Plaza",
             fontsize=14, fontweight="bold")
plt.tight_layout()
fig.savefig(os.path.join(OUT, "eyelevel_community_plaza.png"), dpi=170)
plt.close(fig)
print("Saved: eyelevel_community_plaza.png")
