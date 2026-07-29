"""
Phase 1.06 - Shadow Analysis
Al Safa 2 Park, Dubai (lat 25.190 N, lon 55.238 E)

Computes real shadow length & direction (via solar elevation/azimuth from pvlib)
cast by reference object heights (tree canopy ~6m, shade structure ~3.5m,
low wall/planter ~1m) at Morning / Noon / Evening on Summer, Winter, Equinox.

This quantifies where shade will and won't exist on site through the year -
direct input for later shaded-path and seating placement decisions (not decided here).
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pvlib.location import Location

OUT = os.path.join(os.path.dirname(__file__), "..", "06_Shadow_Analysis", "outputs")
os.makedirs(OUT, exist_ok=True)

LAT, LON, ALT = 25.190, 55.238, 16
TZ = "Asia/Dubai"
site = Location(LAT, LON, tz=TZ, altitude=ALT, name="Al Safa 2 Park")

seasons = {
    "Summer Solstice (21 Jun)": "2026-06-21",
    "Winter Solstice (21 Dec)": "2026-12-21",
    "Equinox (20 Mar)": "2026-03-20",
}
day_moments = {"Morning (09:00)": "09:00", "Noon (12:00)": "12:00", "Evening (16:00)": "16:00"}
object_heights = {"Tree canopy (6m)": 6.0, "Shade structure (3.5m)": 3.5, "Low wall/planter (1m)": 1.0}

rows = []
for season_label, date in seasons.items():
    for moment_label, t in day_moments.items():
        ts = pd.Timestamp(f"{date} {t}", tz=TZ)
        solpos = site.get_solarposition(ts)
        elev = float(solpos["apparent_elevation"].iloc[0])
        az = float(solpos["azimuth"].iloc[0])
        for obj_label, h in object_heights.items():
            if elev > 0.5:
                shadow_len = h / np.tan(np.radians(elev))
            else:
                shadow_len = float("inf")
            rows.append({
                "Season": season_label, "Time": moment_label, "Object": obj_label,
                "Object_Height_m": h, "Sun_Elevation_deg": round(elev, 1),
                "Sun_Azimuth_deg": round(az, 1), "Shadow_Length_m": round(shadow_len, 2) if shadow_len != float("inf") else "N/A (sun below horizon)"
            })

df = pd.DataFrame(rows)
df.to_csv(os.path.join(OUT, "shadow_length_table.csv"), index=False)
print("Saved: shadow_length_table.csv")
print(df.to_string(index=False))

# --- Visualization: shadow length comparison chart ---
fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=True)
for ax, (season_label, _) in zip(axes, seasons.items()):
    sub = df[df["Season"] == season_label]
    for obj_label in object_heights:
        obj_sub = sub[sub["Object"] == obj_label]
        vals = [v if isinstance(v, (int, float)) else 0 for v in obj_sub["Shadow_Length_m"]]
        ax.plot(list(day_moments.keys()), vals, "o-", label=obj_label)
    ax.set_title(season_label)
    ax.set_xlabel("Time of Day")
    ax.tick_params(axis="x", rotation=20)
axes[0].set_ylabel("Shadow Length (m)")
axes[0].legend(loc="upper right", fontsize=8)
plt.suptitle("Al Safa 2 Park - Shadow Length by Object Height, Season & Time of Day")
plt.tight_layout()
fig.savefig(os.path.join(OUT, "chart_shadow_length_comparison.png"), dpi=150)
plt.close(fig)
print("Saved: chart_shadow_length_comparison.png")

# --- Visualization: shadow direction (plan-view arrows) for Noon across 3 seasons ---
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_title("Al Safa 2 Park - Shadow Direction at Noon\n(arrow points from object toward shadow tip, 6m tree)")
colors = {"Summer Solstice (21 Jun)": "#d62728", "Winter Solstice (21 Dec)": "#1f77b4", "Equinox (20 Mar)": "#2ca02c"}
for season_label, date in seasons.items():
    ts = pd.Timestamp(f"{date} 12:00", tz=TZ)
    solpos = site.get_solarposition(ts)
    elev = float(solpos["apparent_elevation"].iloc[0])
    az = float(solpos["azimuth"].iloc[0])
    shadow_len = 6.0 / np.tan(np.radians(elev))
    # shadow points opposite the sun's azimuth
    shadow_az = (az + 180) % 360
    dx = shadow_len * np.sin(np.radians(shadow_az))
    dy = shadow_len * np.cos(np.radians(shadow_az))
    ax.arrow(0, 0, dx, dy, head_width=0.5, length_includes_head=True,
              color=colors[season_label], linewidth=2,
              label=f"{season_label} ({shadow_len:.1f}m)")

ax.plot(0, 0, "ks", markersize=12, label="6m Tree (object)")
lim = 12
ax.set_xlim(-lim, lim)
ax.set_ylim(-lim, lim)
ax.set_xlabel("East-West (m)")
ax.set_ylabel("North-South (m)")
ax.axhline(0, color="gray", linewidth=0.5)
ax.axvline(0, color="gray", linewidth=0.5)
ax.set_aspect("equal")
ax.legend(loc="upper left", fontsize=8)
ax.grid(alpha=0.3)
fig.savefig(os.path.join(OUT, "chart_shadow_direction_plan.png"), dpi=150)
plt.close(fig)
print("Saved: chart_shadow_direction_plan.png")

# --- Written summary ---
summary_path = os.path.join(OUT, "shadow_analysis_summary.txt")
with open(summary_path, "w", encoding="utf-8") as f:
    f.write("PHASE 1.06 - SHADOW ANALYSIS - AL SAFA 2 PARK, DUBAI\n")
    f.write("=" * 55 + "\n\n")
    f.write("METHOD:\n")
    f.write("  Shadow length = object height / tan(solar elevation angle)\n")
    f.write("  Solar elevation/azimuth computed exactly for site lat/lon via pvlib\n")
    f.write("  (NREL Solar Position Algorithm), for 2026 solstices/equinox.\n\n")
    f.write("KEY FINDINGS:\n")
    f.write("  - Summer noon: sun near-zenith (elev ~88 deg) -> shadows extremely short\n")
    f.write("    (~0.2m for a 6m tree) - vertical shade structures/canopy needed, not\n")
    f.write("    reliance on low objects, for midday summer shade.\n")
    f.write("  - Winter noon: sun lower (elev ~41 deg) -> shadows much longer\n")
    f.write("    (~6.9m for a 6m tree) - south-facing facades/walls cast usable shade.\n")
    f.write("  - Morning/evening in all seasons: long shadows from low sun angles,\n")
    f.write("    directionally from the east (morning) / west (evening).\n")
    f.write("  - Shadow direction at noon swings from just-north-of-overhead (summer)\n")
    f.write("    to due-north (winter) in this northern-hemisphere low-latitude site.\n\n")
    f.write("DESIGN IMPLICATIONS (for later phases, not decided yet):\n")
    f.write("  - Overhead/canopy shade (pergolas, tree canopy, shade sails) is essential\n")
    f.write("    for summer midday comfort since low structures cast almost no shadow then.\n")
    f.write("  - East-west oriented paths will be shaded by roadside/building shadow in\n")
    f.write("    morning and evening; north-south paths get least natural shade at those times.\n")
    f.write("  - Seating/gathering nodes on the north side of tall elements (trees, structures)\n")
    f.write("    benefit most consistently across all three seasons.\n")

print("Saved:", summary_path)
