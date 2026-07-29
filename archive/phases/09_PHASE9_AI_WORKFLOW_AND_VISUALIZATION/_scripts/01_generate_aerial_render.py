"""
Phase 9.7 - Aerial Visualization
Produces a more rendered aerial-style diagram of the Concept A masterplan,
building on the exact zoning geometry from Phase 5 with tree-canopy texture,
shadow overlay (from the Phase 7 shade model), and day/night variants.
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "..", "9.7_Renderings")
for sub in ["Aerial", "Day", "Night"]:
    os.makedirs(os.path.join(OUT, sub), exist_ok=True)

SITE_W, SITE_H = 150.0, 100.0

zones = [
    ("Main Entrance Plaza", 0, 40, 12, 20, "#C9A24A"),
    ("Shaded Spine", 12, 45, 126, 10, "#3D5A80"),
    ("Secondary Entrance", 138, 40, 12, 20, "#C9A24A"),
    ("Children's Play Zone", 14, 58, 32, 34, "#EE6C4D"),
    ("Family Picnic & Shaded Seating", 48, 58, 26, 34, "#7FB069"),
    ("Community Plaza & Event Lawn", 76, 58, 36, 34, "#F4A261"),
    ("Outdoor Fitness & Wellness", 114, 58, 24, 34, "#4A7C59"),
    ("Native Planting / Biodiversity", 14, 8, 32, 34, "#2D6A4F"),
    ("Quiet Contemplation Garden", 48, 8, 26, 34, "#8AA29E"),
    ("Commercial & Service Kiosks", 76, 8, 22, 34, "#B08968"),
    ("Multipurpose Sports Lawn", 100, 8, 38, 34, "#588157"),
    ("Perimeter Shade Buffer (N)", 12, 92, 126, 8, "#40916C"),
    ("Perimeter Shade Buffer (S)", 12, 0, 126, 8, "#40916C"),
]

tree_zones = ["Native Planting / Biodiversity", "Perimeter Shade Buffer (N)", "Perimeter Shade Buffer (S)",
              "Family Picnic & Shaded Seating", "Quiet Contemplation Garden"]

rng = np.random.default_rng(42)

def render(mode="day", filename="aerial_day.png"):
    fig, ax = plt.subplots(figsize=(16, 11))
    bg = "#EDE6D6" if mode == "day" else "#0D1B2A"
    fig.patch.set_facecolor(bg)
    ax.set_facecolor(bg)

    for name, x, y, w, h, color in zones:
        rect = patches.Rectangle((x, y), w, h, facecolor=color, edgecolor="black",
                                  linewidth=0.8, alpha=0.9 if mode == "day" else 0.65)
        ax.add_patch(rect)
        # tree canopy dot texture for green zones
        if name in tree_zones:
            n_trees = int(w * h / 12)
            tx = rng.uniform(x + 1, x + w - 1, n_trees)
            ty = rng.uniform(y + 1, y + h - 1, n_trees)
            ax.scatter(tx, ty, s=rng.uniform(20, 55, n_trees), color="#1b4332",
                       alpha=0.55, edgecolors="none")
        if mode == "night":
            # simulate lighting glow at path/plaza edges
            if name in ("Shaded Spine", "Main Entrance Plaza", "Secondary Entrance",
                         "Community Plaza & Event Lawn"):
                for lx in np.linspace(x + 3, x + w - 3, max(int(w / 15), 2)):
                    ax.scatter([lx], [y + h / 2], s=180, color="#FFD166", alpha=0.35, zorder=5)
                    ax.scatter([lx], [y + h / 2], s=40, color="#FFF3B0", alpha=0.9, zorder=6)

    text_color = "black" if mode == "day" else "white"
    for name, x, y, w, h, color in zones:
        ax.text(x + w / 2, y + h / 2, name, ha="center", va="center", fontsize=6.8,
                 color=text_color, fontweight="bold", zorder=10)

    ax.add_patch(patches.Rectangle((0, 0), SITE_W, SITE_H, fill=False,
                                    edgecolor=text_color, linewidth=2))
    ax.set_xlim(-5, SITE_W + 5)
    ax.set_ylim(-5, SITE_H + 5)
    ax.set_aspect("equal")
    ax.axis("off")
    title_suffix = "Day Aerial View" if mode == "day" else "Night Aerial View (illustrative lighting)"
    ax.set_title(f"Al Safa 2 Park — Concept A \"Shaded Spine\" — {title_suffix}",
                 fontsize=14, fontweight="bold", color=text_color)

    plt.tight_layout()
    out_path = os.path.join(OUT, "Aerial", filename)
    fig.savefig(out_path, dpi=170, facecolor=bg)
    plt.close(fig)
    print(f"Saved: {out_path}")

render("day", "aerial_day.png")
render("night", "aerial_night.png")
