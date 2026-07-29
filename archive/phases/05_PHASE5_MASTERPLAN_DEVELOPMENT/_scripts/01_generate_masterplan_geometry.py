"""
Phase 5 - Master Plan Development
Generates an actual geometric zoning + circulation layout for Al Safa 2 Park
implementing the selected "Shaded Spine" concept (Phase 4), sized to the real
15,000 sqm site area confirmed in the Competition Brief.

Site assumed as an elongated rectangle (consistent with the aerial massing seen
in the master-plan graphic, Phase 1.02) since the DWG's exact boundary polygon
is not yet available (logged gap). Proportions: 150m x 100m = 15,000 sqm,
oriented long-axis NW-SE per the site graphic.
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUT = os.path.join(os.path.dirname(__file__), "..", "outputs")
os.makedirs(OUT, exist_ok=True)

SITE_W, SITE_H = 150.0, 100.0  # meters; 150 x 100 = 15,000 sqm exactly
SITE_AREA = SITE_W * SITE_H
assert SITE_AREA == 15000, "Site area must match brief's confirmed 15,000 sqm"

# --- Zoning layout (Shaded Spine concept) ---
# The "Spine" runs along the long (east-west, 150m) axis at mid-depth (y=45-55m, 10m wide shaded walkway).
# Rooms are arranged along both sides of the spine.
zones = [
    # name, x, y, w, h, color, category
    ("Main Entrance Plaza", 0, 40, 12, 20, "#C9A24A", "Arrival"),
    ("Shaded Spine (Central Walkway)", 12, 45, 126, 10, "#3D5A80", "Circulation"),
    ("Secondary Entrance (E)", 138, 40, 12, 20, "#C9A24A", "Arrival"),

    ("Children's Play Zone", 14, 58, 32, 34, "#EE6C4D", "Active"),
    ("Family Picnic & Shaded Seating", 48, 58, 26, 34, "#7FB069", "Passive"),
    ("Community Plaza & Event Lawn", 76, 58, 36, 34, "#F4A261", "Social"),
    ("Outdoor Fitness & Wellness", 114, 58, 24, 34, "#4A7C59", "Active"),

    ("Native Planting / Biodiversity Strip", 14, 8, 32, 34, "#2D6A4F", "Green"),
    ("Quiet Contemplation Garden", 48, 8, 26, 34, "#8AA29E", "Passive"),
    ("Commercial & Service Kiosk Cluster", 76, 8, 22, 34, "#B08968", "Commercial"),
    ("Multipurpose Sports Lawn", 100, 8, 38, 34, "#588157", "Active"),

    # Secondary green buffers filling perimeter margins between rooms and site edge
    ("Perimeter Shade Buffer (N)", 12, 92, 126, 8, "#40916C", "Green_Buffer"),
    ("Perimeter Shade Buffer (S)", 12, 0, 126, 8, "#40916C", "Green_Buffer"),
    ("Path Network & Landscape Setbacks", 0, 0, 0, 0, "none", "Path_Remainder"),

    ("Jogging Track (perimeter loop)", 0, 0, 150, 100, "none", "Circulation_Loop"),
]

# --- Area accounting (validate against 15,000 sqm total site) ---
area_rows = []
total_room_area = 0
for name, x, y, w, h, color, cat in zones:
    if cat in ("Circulation_Loop", "Path_Remainder"):
        continue  # computed below / overlay only
    area = w * h
    total_room_area += area
    area_rows.append((name, cat, round(area, 1), round(100 * area / SITE_AREA, 1)))

remaining = SITE_AREA - total_room_area  # named paths + landscape setbacks between rooms
area_rows.append(("Path Network & Landscape Setbacks (between rooms, to entrances, perimeter jogging loop)",
                   "Circulation", round(remaining, 1), round(100 * remaining / SITE_AREA, 1)))

print(f"Site area: {SITE_AREA} sqm")
print(f"Total zoned room area: {total_room_area} sqm")
print(f"Remaining (paths/buffers): {remaining} sqm")
for r in area_rows:
    print(r)

with open(os.path.join(OUT, "zoning_area_schedule.json"), "w") as f:
    json.dump({"site_area_sqm": SITE_AREA, "zones": area_rows}, f, indent=2)
print("Saved: zoning_area_schedule.json")

# --- Draw the master plan diagram ---
fig, ax = plt.subplots(figsize=(15, 10))
ax.set_xlim(-5, SITE_W + 5)
ax.set_ylim(-5, SITE_H + 5)
ax.set_aspect("equal")

# Site boundary
ax.add_patch(patches.Rectangle((0, 0), SITE_W, SITE_H, fill=False, edgecolor="black", linewidth=2.5))

for name, x, y, w, h, color, cat in zones:
    if cat == "Path_Remainder":
        continue  # not drawn as a block; represented by the visible gaps + loop path
    if cat == "Circulation_Loop":
        # draw perimeter jogging loop (inset from boundary)
        inset = 4
        loop = patches.Rectangle((inset, inset), SITE_W - 2*inset, SITE_H - 2*inset,
                                  fill=False, edgecolor="#264653", linewidth=2, linestyle="--")
        ax.add_patch(loop)
        continue
    rect = patches.Rectangle((x, y), w, h, facecolor=color, edgecolor="black",
                              linewidth=1, alpha=0.75)
    ax.add_patch(rect)
    text_color = "white" if cat not in ("Arrival",) else "black"
    ax.text(x + w/2, y + h/2, name, ha="center", va="center", fontsize=7.2,
             wrap=True, color=text_color, fontweight="bold")

# North arrow + scale
ax.annotate("N", xy=(SITE_W + 2, SITE_H - 5), fontsize=14, fontweight="bold", ha="center")
ax.annotate("", xy=(SITE_W + 2, SITE_H - 8), xytext=(SITE_W + 2, SITE_H - 15),
            arrowprops=dict(arrowstyle="-|>", lw=2))
ax.plot([0, 20], [-3, -3], color="black", linewidth=2)
ax.text(10, -4.5, "20 m", ha="center", fontsize=9)

ax.set_title("Al Safa 2 Park — Preliminary Master Plan (Concept A: \"Shaded Spine\")\n"
              "15,000 sqm | AI-generated draft layout for review", fontsize=13, fontweight="bold")
ax.axis("off")

plt.tight_layout()
fig.savefig(os.path.join(OUT, "masterplan_diagram.png"), dpi=170)
plt.close(fig)
print("Saved: masterplan_diagram.png")
