"""
Phase 1.11 - SWOT Synthesis
Synthesizes findings from Phase 1.01-1.10 into a visual SWOT matrix.
This is a synthesis of already-documented findings, not new invented data.
"""

import os
import matplotlib.pyplot as plt

OUT = os.path.join(os.path.dirname(__file__), "..", "11_SWOT", "outputs")
os.makedirs(OUT, exist_ok=True)

swot = {
    "STRENGTHS": [
        "Established 15,000 sqm neighborhood park - existing tree canopy asset (west side)",
        "Strong residential embedding - walkable from surrounding local streets on 3 sides",
        "Adjacent community anchors: school, mosque, physiotherapy/rehab center",
        "Metro proximity (ONPASSIVE Station) - potential for wider catchment if crossing improved",
        "High-profile competition status - AED 35M implementation budget secured",
        "Comfortable outdoor climate window Nov-Apr (avg max 24-34C) for high park usage",
    ],
    "WEAKNESSES": [
        "Sheikh Zayed Rd (E11) borders east edge - noise, air quality, visual/physical barrier",
        "Tree canopy concentrated only on west side - shade equity gap (from image analysis)",
        "No confirmed accessibility features documented in existing conditions",
        "No confirmed existing parking, drop-off, or cycling infrastructure",
        "Extreme summer heat (up to ~41C avg max, near-zero shade at solar noon in Jun) limits usability May-Oct",
        "As-built DWG not yet converted - full existing geometry (paths, utilities, levels) unverified",
    ],
    "OPPORTUNITIES": [
        "Redevelopment budget allows full reprogramming vs. incremental fixes",
        "WNW prevailing wind (16.7 km/h avg, sourced Windfinder data) available for passive cooling design",
        "AI Design Challenge status brings visibility - opportunity for a flagship, replicable model",
        "Community voting (jury + public selection process) supports genuine co-design outcome",
        "Winter solar angle (elev ~41deg) still allows usable structure-cast shade for cooler months",
        "Adjacent school population = untapped recurring user base (students, families at pickup/dropoff)",
    ],
    "THREATS": [
        "Summer thermal extremes could undermine usability if shade/microclimate design is inadequate",
        "SZR-side noise/pollution may deter passive/quiet activity zones nearest that edge",
        "Rapid urban growth pressure in Dubai could increase future demand beyond current 15,000 sqm capacity",
        "Metro-park pedestrian link across SZR, if unresolved, limits realized catchment gains",
        "Data gaps (GIS, DWG, accessibility) risk under-informed decisions if not resolved before Phase 5 Masterplan",
    ],
}

# --- 2x2 SWOT matrix visualization ---
fig, axes = plt.subplots(2, 2, figsize=(18, 12))
configs = [
    ("STRENGTHS", "#2ca02c", axes[0, 0]),
    ("WEAKNESSES", "#d62728", axes[0, 1]),
    ("OPPORTUNITIES", "#1f77b4", axes[1, 0]),
    ("THREATS", "#ff7f0e", axes[1, 1]),
]
for label, color, ax in configs:
    ax.set_facecolor("#f7f7f7")
    ax.set_title(label, fontsize=18, fontweight="bold", color=color, loc="left")
    text = "\n\n".join(f"- {item}" for item in swot[label])
    ax.text(0.02, 0.95, text, transform=ax.transAxes, fontsize=9.5,
            verticalalignment="top", wrap=True)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_edgecolor(color)
        spine.set_linewidth(2)

plt.suptitle("Al Safa 2 Park - SWOT Analysis (Phase 1 Synthesis)", fontsize=20, fontweight="bold")
plt.tight_layout(rect=[0, 0, 1, 0.96])
fig.savefig(os.path.join(OUT, "swot_matrix.png"), dpi=150)
plt.close(fig)
print("Saved: swot_matrix.png")

# --- Text version ---
with open(os.path.join(OUT, "swot_matrix.md"), "w", encoding="utf-8") as f:
    f.write("# Phase 1.11 - SWOT Analysis\nAl Safa 2 Park (synthesized from Phase 1.01-1.10 findings)\n\n")
    for label in ["STRENGTHS", "WEAKNESSES", "OPPORTUNITIES", "THREATS"]:
        f.write(f"## {label}\n")
        for item in swot[label]:
            f.write(f"- {item}\n")
        f.write("\n")

print("Saved: swot_matrix.md")
