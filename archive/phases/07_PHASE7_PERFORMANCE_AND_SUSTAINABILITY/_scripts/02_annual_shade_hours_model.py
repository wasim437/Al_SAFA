"""
Phase 7 UPGRADE - Annual Shade-Hours Model
Uses the full-year (8,760-hour) exact solar dataset from Phase 1.05 upgrade
to compute REAL annual shade-hour totals for each masterplan zone - a much
deeper metric than the original 3-sample-date snapshot.

For each daylight hour of the year, we compute whether each zone's centroid
is shaded by the design's shade-casting elements (Shaded Spine canopy,
Perimeter Buffers, Native Planting canopy), then sum hours shaded per zone
across the whole year.
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "..", "outputs")
os.makedirs(OUT, exist_ok=True)

CLIMATE_OUT = os.path.join(HERE, "..", "..", "01_PHASE1_EXISTING_PARK", "05_Climate_Analysis", "outputs")
solar = pd.read_csv(os.path.join(CLIMATE_OUT, "fullyear_solar_daylight_hours.csv"), index_col=0, parse_dates=True)
print(f"Loaded {len(solar)} real computed daylight hours from Phase 1.05 upgrade dataset")

# Shade-casting elements (same as Phase 7's original shade_coverage_model.py)
shade_elements = [
    ("Shaded Spine canopy", 10.8, 44, 128.4, 12.4, 5.5),
    ("Perimeter Shade Buffer (N)", 12, 92, 126, 8, 6.0),
    ("Perimeter Shade Buffer (S)", 12, 0, 126, 8, 6.0),
    ("Native Planting Strip", 14, 8, 32, 34, 6.0),
]

# Zone centroids to evaluate (from Phase 5 zoning schedule)
zone_centroids = {
    "Shaded Spine (path)": (12 + 126 / 2, 45 + 10 / 2),
    "Children's Play Zone": (14 + 32 / 2, 58 + 34 / 2),
    "Family Picnic & Shaded Seating": (48 + 26 / 2, 58 + 34 / 2),
    "Community Plaza & Event Lawn": (76 + 36 / 2, 58 + 34 / 2),
    "Outdoor Fitness & Wellness": (114 + 24 / 2, 58 + 34 / 2),
    "Quiet Contemplation Garden": (48 + 26 / 2, 8 + 34 / 2),
    "Commercial & Service Kiosks": (76 + 22 / 2, 8 + 34 / 2),
    "Multipurpose Sports Lawn": (100 + 38 / 2, 8 + 34 / 2),
}

def is_point_shaded(px, py, elev_deg, az_deg, elements):
    if elev_deg <= 0.5:
        return False
    shadow_len_per_height = 1.0 / np.tan(np.radians(elev_deg))
    shadow_az = (az_deg + 180) % 360
    dx_dir = np.sin(np.radians(shadow_az))
    dy_dir = np.cos(np.radians(shadow_az))
    for name, ex, ey, ew, eh, height in elements:
        reach = shadow_len_per_height * height
        steps = max(int(reach), 1)
        for s in range(steps + 1):
            t = s * (reach / steps) if steps > 0 else 0
            sx0, sy0 = ex - dx_dir * t, ey - dy_dir * t
            if (sx0 <= px <= sx0 + ew) and (sy0 <= py <= sy0 + eh):
                return True
    return False

# --- Run the full-year simulation (this is the real computational upgrade) ---
results = {name: 0 for name in zone_centroids}
elevations = solar["apparent_elevation"].values
azimuths = solar["azimuth"].values
n_hours = len(solar)

print(f"Running shade check for {len(zone_centroids)} zones across {n_hours} real daylight hours...")
for name, (px, py) in zone_centroids.items():
    shaded_count = 0
    for elev, az in zip(elevations, azimuths):
        if is_point_shaded(px, py, elev, az, shade_elements):
            shaded_count += 1
    results[name] = shaded_count

annual_shade_pct = {name: round(100 * hrs / n_hours, 1) for name, hrs in results.items()}
annual_shade_hours = results

print("Annual shaded hours per zone (out of", n_hours, "daylight hours):")
for name, hrs in results.items():
    print(f"  {name}: {hrs} hrs ({annual_shade_pct[name]}%)")

with open(os.path.join(OUT, "annual_shade_hours_results.json"), "w") as f:
    json.dump({"total_daylight_hours": n_hours,
                "annual_shade_hours": annual_shade_hours,
                "annual_shade_pct": annual_shade_pct}, f, indent=2)
print("Saved: annual_shade_hours_results.json")

# --- Chart: annual shade % by zone, sorted ---
names_sorted = sorted(annual_shade_pct, key=annual_shade_pct.get, reverse=True)
vals_sorted = [annual_shade_pct[n] for n in names_sorted]

fig, ax = plt.subplots(figsize=(12, 7))
colors = ["#2a9d8f" if v >= 50 else "#e76f51" for v in vals_sorted]
ax.barh(names_sorted, vals_sorted, color=colors)
for i, v in enumerate(vals_sorted):
    ax.text(v + 1, i, f"{v}%", va="center", fontsize=9)
ax.set_xlabel("% of Annual Daylight Hours Shaded (computed across 4,425 real hours)")
ax.set_title("Al Safa 2 Park — Annual Shade Coverage by Zone\n(Full-Year 8,760-Hour Exact Solar Simulation)")
ax.set_xlim(0, 100)
plt.tight_layout()
fig.savefig(os.path.join(OUT, "annual_shade_hours_by_zone.png"), dpi=160)
plt.close(fig)
print("Saved: annual_shade_hours_by_zone.png")

# --- Monthly breakdown for the Shaded Spine (primary circulation) ---
solar_copy = solar.copy()
spine_shaded = []
for idx, row in solar_copy.iterrows():
    px, py = zone_centroids["Shaded Spine (path)"]
    spine_shaded.append(is_point_shaded(px, py, row["apparent_elevation"], row["azimuth"], shade_elements))
solar_copy["spine_shaded"] = spine_shaded

monthly_spine_pct = solar_copy.groupby("month")["spine_shaded"].mean() * 100
monthly_spine_pct.to_csv(os.path.join(OUT, "monthly_spine_shade_pct.csv"), header=["spine_shade_pct"])

fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(monthly_spine_pct.index.astype(str), monthly_spine_pct.values, color="#3D5A80")
ax.set_xlabel("Month")
ax.set_ylabel("% of Daylight Hours Shaded")
ax.set_title("Al Safa 2 Park — Shaded Spine: Monthly Shade Coverage\n(computed from full-year real solar data)")
ax.set_ylim(0, 100)
for i, v in enumerate(monthly_spine_pct.values):
    ax.text(i, v + 1, f"{v:.0f}%", ha="center", fontsize=8)
plt.tight_layout()
fig.savefig(os.path.join(OUT, "monthly_spine_shade_pct.png"), dpi=150)
plt.close(fig)
print("Saved: monthly_spine_shade_pct.png")
print("Monthly spine shade %:")
print(monthly_spine_pct.round(1))
