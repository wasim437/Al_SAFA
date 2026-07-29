"""
Phase 6.1 - Planting Plan (code-generated, to scale)
Places each real UAE-native/adapted species at specific locations across the
masterplan, DIRECTLY closing the room-shade gap that the Phase 7 annual-shade
simulation exposed (activity-room interiors got only 3.6-16.2% passive shade).
Priority canopy trees are placed inside the lowest-shade rooms first.

Also outputs a planting schedule (species, symbol, count) and the total tree
count, which feeds the Phase 7 carbon + water models.
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.lines import Line2D

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "..", "outputs")
os.makedirs(OUT, exist_ok=True)

SITE_W, SITE_H = 150.0, 100.0

# Rooms (name, x, y, w, h) from Phase 5 + their computed annual shade % (Phase 7)
rooms = [
    ("Children's Play", 14, 58, 32, 34, 3.6),
    ("Family Picnic", 48, 58, 26, 34, 6.2),
    ("Community Plaza", 76, 58, 36, 34, 7.0),
    ("Outdoor Fitness", 114, 58, 24, 34, 4.6),
    ("Native Planting", 14, 8, 32, 34, None),
    ("Quiet Garden", 48, 8, 26, 34, 16.2),
    ("Commercial Kiosks", 76, 8, 22, 34, 7.7),
    ("Sports Lawn", 100, 8, 38, 34, 4.3),
]

# Species: name -> (color, marker, canopy radius m)
SPECIES = {
    "Ghaf (Prosopis cineraria)":   ("#2d6a4f", "o", 4.0),
    "Neem (Azadirachta indica)":   ("#1b4332", "o", 4.5),
    "Date Palm (Phoenix dactylifera)": ("#957c3e", "^", 2.5),
    "Ficus nitida":                ("#40916c", "o", 3.5),
    "Olive (Olea europaea)":       ("#6b8e5a", "s", 2.5),
}

rng = np.random.default_rng(11)
planting = []  # (species, x, y)

def scatter_trees_in(room, species, target_shade_area_frac):
    """Place trees inside a room to cover ~target fraction with canopy."""
    _, x, y, w, h, _ = room
    color, marker, r = SPECIES[species]
    room_area = w * h
    canopy_area = np.pi * r * r
    n = max(1, int(target_shade_area_frac * room_area / canopy_area))
    placed = 0
    for _ in range(n):
        px = rng.uniform(x + r, x + w - r)
        py = rng.uniform(y + r, y + h - r)
        planting.append((species, px, py))
        placed += 1
    return placed

fig, ax = plt.subplots(figsize=(16, 11))
ax.add_patch(patches.Rectangle((0,0), SITE_W, SITE_H, facecolor="#f4f3ec", ec="black", lw=2))

# Draw rooms + fill priority trees based on how LOW their current shade is
for room in rooms:
    name, x, y, w, h, shade = room
    ax.add_patch(patches.Rectangle((x,y),w,h, facecolor="#e8ede6", ec="#b8c4b8", lw=1))
    ax.text(x+w/2, y+h-2, name, ha="center", va="top", fontsize=8, fontweight="bold", color="#333")
    if name == "Native Planting":
        scatter_trees_in(room, "Ghaf (Prosopis cineraria)", 0.55)  # dense native strip
    elif name == "Sports Lawn":
        scatter_trees_in(room, "Date Palm (Phoenix dactylifera)", 0.12)  # keep lawn open, edge palms
    elif name == "Children's Play":
        scatter_trees_in(room, "Neem (Azadirachta indica)", 0.35)  # highest priority: lowest shade
    elif name == "Outdoor Fitness":
        scatter_trees_in(room, "Neem (Azadirachta indica)", 0.30)
    elif name == "Community Plaza":
        scatter_trees_in(room, "Ficus nitida", 0.20)
    elif name == "Family Picnic":
        scatter_trees_in(room, "Ghaf (Prosopis cineraria)", 0.30)
    elif name == "Quiet Garden":
        scatter_trees_in(room, "Olive (Olea europaea)", 0.25)
    elif name == "Commercial Kiosks":
        scatter_trees_in(room, "Date Palm (Phoenix dactylifera)", 0.15)

# Perimeter buffers - continuous canopy
for (bx, by, bw, bh) in [(12,92,126,8),(12,0,126,8)]:
    ax.add_patch(patches.Rectangle((bx,by),bw,bh, facecolor="#d8e2d8", ec="#b8c4b8"))
    for _ in range(int(bw*bh/40)):
        planting.append(("Neem (Azadirachta indica)", rng.uniform(bx, bx+bw), rng.uniform(by, by+bh)))

# Spine edge trees (Ficus)
for sx in np.arange(16, 138, 9):
    planting.append(("Ficus nitida", sx, 43))
    planting.append(("Ficus nitida", sx, 57))

# Plot all trees as canopy circles + centre markers
for species, px, py in planting:
    color, marker, r = SPECIES[species]
    ax.add_patch(patches.Circle((px,py), r, facecolor=color, alpha=0.30, ec="none"))
    ax.plot(px, py, marker=marker, color=color, markersize=4, markeredgecolor="white", markeredgewidth=0.4)

# Shaded spine band
ax.add_patch(patches.Rectangle((12,45),126,10, facecolor="#c9d3da", ec="#8aa1b0", alpha=0.6))
ax.text(75, 50, "SHADED SPINE", ha="center", va="center", fontsize=9, fontweight="bold", color="#33475b")

# Count schedule
from collections import Counter
counts = Counter(s for s,_,_ in planting)
total = sum(counts.values())

# Legend
legend = [Line2D([0],[0], marker=SPECIES[s][1], color="w", markerfacecolor=SPECIES[s][0],
                 markersize=9, label=f"{s}  (×{counts.get(s,0)})") for s in SPECIES]
ax.legend(handles=legend, loc="upper center", bbox_to_anchor=(0.5,-0.03), ncol=3, fontsize=9, frameon=False)

# North arrow
ax.annotate("N", xy=(SITE_W+3, SITE_H-4), fontsize=13, fontweight="bold", ha="center")
ax.annotate("", xy=(SITE_W+3, SITE_H-7), xytext=(SITE_W+3, SITE_H-14), arrowprops=dict(arrowstyle="-|>", lw=2))

ax.set_xlim(-6, SITE_W+8); ax.set_ylim(-16, SITE_H+6)
ax.set_aspect("equal"); ax.axis("off")
ax.set_title(f"Al Safa 2 Park — Planting Plan (Phase 6.1)  |  {total} trees total\n"
             f"Priority canopy placed inside the lowest-shade rooms first (Play 3.6%, Fitness 4.6%, Sports 4.3%)",
             fontsize=13, fontweight="bold")
plt.tight_layout()
fig.savefig(os.path.join(OUT, "planting_plan.png"), dpi=160, bbox_inches="tight")
plt.close(fig)
print(f"Saved: planting_plan.png ({total} trees)")

# Save schedule
schedule = {"total_trees": total, "by_species": dict(counts)}
with open(os.path.join(OUT, "planting_schedule.json"), "w") as f:
    json.dump(schedule, f, indent=2)
print("Saved: planting_schedule.json")
for s, n in counts.items():
    print(f"  {s}: {n}")
