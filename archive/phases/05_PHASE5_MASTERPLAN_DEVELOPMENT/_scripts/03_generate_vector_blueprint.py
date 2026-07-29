"""
Architectural Vector Masterplan Blueprint Generator for Al Safa 2 Park.
Generates an ultra-high resolution SVG and PNG masterplan blueprint with precise zoning,
coordinate grid, scale bar, north arrow, circulation vectors, and tree placement.
"""
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

HERE = os.path.dirname(__file__)
OUT_DIR = os.path.join(HERE, "..", "outputs")
os.makedirs(OUT_DIR, exist_ok=True)

def generate_blueprint():
    fig, ax = plt.subplots(figsize=(16, 11), dpi=300)
    fig.patch.set_facecolor('#0B1F3A')
    ax.set_facecolor('#071326')

    # Site Boundary: 150m x 100m
    site_w, site_h = 150, 100
    margin = 15
    ax.set_xlim(-margin, site_w + margin)
    ax.set_ylim(-margin, site_h + margin)
    ax.set_aspect('equal')

    # Coordinate Grid (10m grid)
    for x in range(0, site_w + 1, 10):
        ax.axvline(x, color='#1E3A60', linewidth=0.5, linestyle='--')
        ax.text(x, -3, f"{x}m", color='#64748B', fontsize=7, ha='center', va='top')
    for y in range(0, site_h + 1, 10):
        ax.axhline(y, color='#1E3A60', linewidth=0.5, linestyle='--')
        ax.text(-3, y, f"{y}m", color='#64748B', fontsize=7, ha='right', va='center')

    # Outer Boundary
    boundary = patches.Rectangle((0, 0), site_w, site_h, linewidth=2, edgecolor='#C8A24A', facecolor='none', linestyle='-')
    ax.add_patch(boundary)

    # 13 Zones Definition
    zones = [
        {"name": "Entrance Plaza & Gateway", "rect": (0, 35, 20, 30), "color": "#EAB308", "alpha": 0.3},
        {"name": "The Shaded Spine (Main Walkway)", "rect": (20, 42, 110, 16), "color": "#06B6D4", "alpha": 0.45},
        {"name": "Community Event Plaza", "rect": (40, 20, 30, 22), "color": "#3B82F6", "alpha": 0.35},
        {"name": "Children's Inclusive Play", "rect": (20, 65, 30, 25), "color": "#EC4899", "alpha": 0.35},
        {"name": "Youth Sports & Fitness Zone", "rect": (75, 60, 35, 30), "color": "#F97316", "alpha": 0.35},
        {"name": "Botanical Sensory Garden", "rect": (20, 10, 20, 25), "color": "#10B981", "alpha": 0.4},
        {"name": "Shaded Reading Lawn", "rect": (45, 65, 25, 25), "color": "#84CC16", "alpha": 0.35},
        {"name": "Family Picnic Meadow", "rect": (75, 10, 35, 25), "color": "#22C55E", "alpha": 0.35},
        {"name": "Micro-Forest & Bioswale", "rect": (115, 65, 30, 25), "color": "#059669", "alpha": 0.4},
        {"name": "Sub-Entrance & Service Node", "rect": (130, 35, 20, 30), "color": "#A855F7", "alpha": 0.3},
        {"name": "Eco-Pond & Recycled Water", "rect": (115, 10, 30, 25), "color": "#0EA5E9", "alpha": 0.4},
        {"name": "Senior Wellness Grove", "rect": (55, 3, 18, 14), "color": "#14B8A6", "alpha": 0.35},
        {"name": "Interactive Water Pavilion", "rect": (72, 3, 18, 14), "color": "#38BDF8", "alpha": 0.35},
    ]

    for z in zones:
        x, y, w, h = z["rect"]
        rect = patches.Rectangle((x, y), w, h, linewidth=1.2, edgecolor=z["color"], facecolor=z["color"], alpha=z["alpha"])
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, z["name"], color='#FFFFFF', fontsize=7.5, fontweight='bold', ha='center', va='center', wrap=True)

    # Spine Canopy Trees (131 trees along spine & key activity zones)
    np.random.seed(42)
    tree_x = np.concatenate([np.linspace(22, 128, 45), np.random.uniform(5, 145, 86)])
    tree_y = np.concatenate([np.linspace(44, 56, 45), np.random.uniform(5, 95, 86)])
    for tx, ty in zip(tree_x, tree_y):
        circle = patches.Circle((tx, ty), radius=2.2, color='#22C55E', alpha=0.5, edgecolor='#15803D', linewidth=0.8)
        ax.add_patch(circle)

    # Circulation Vectors (Main Walkway + Loops)
    ax.annotate("", xy=(145, 50), xytext=(5, 50), arrowprops=dict(arrowstyle="->", color="#38BDF8", lw=2, ls="--"))
    ax.annotate("", xy=(75, 90), xytext=(75, 10), arrowprops=dict(arrowstyle="<->", color="#F59E0B", lw=1.5, ls=":"))

    # Title & Metadata Block
    ax.text(0, site_h + 10, "AL SAFA 2 PARK — ARCHITECTURAL BLUEPRINT MASTERPLAN", color='#FFFFFF', fontsize=14, fontweight='bold')
    ax.text(0, site_h + 6, "Dubai Municipality AI Design Challenge | Applicant: MOHAMED WASIM | Scale 1:500 @ A3", color='#C8A24A', fontsize=9)

    # North Arrow
    na_x, na_y = site_w + 8, site_h + 5
    ax.annotate("N", xy=(na_x, na_y+6), xytext=(na_x, na_y-2),
                arrowprops=dict(facecolor='#C8A24A', edgecolor='#C8A24A', width=3, headwidth=9),
                color='#C8A24A', fontsize=10, fontweight='bold', ha='center')

    # Scale Bar (50m scale)
    sb_x, sb_y = 0, -10
    ax.plot([sb_x, sb_x + 50], [sb_y, sb_y], color='#C8A24A', linewidth=3)
    ax.text(sb_x, sb_y - 2, "0m", color='#94A3B8', fontsize=7, ha='center')
    ax.text(sb_x + 25, sb_y - 2, "25m", color='#94A3B8', fontsize=7, ha='center')
    ax.text(sb_x + 50, sb_y - 2, "50m Scale", color='#94A3B8', fontsize=7, ha='center')

    ax.axis('off')
    plt.tight_layout()

    svg_path = os.path.join(OUT_DIR, "masterplan_vector_blueprint.svg")
    png_path = os.path.join(OUT_DIR, "masterplan_vector_blueprint.png")
    plt.savefig(svg_path, format='svg', bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.savefig(png_path, format='png', dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"Generated Vector Blueprint: {svg_path} & {png_path}")

if __name__ == "__main__":
    generate_blueprint()
