"""
Phase 1.13 - Catchment & Demand Analysis (NEW, real-data)
Uses REAL Dubai Statistics Center 2023 population figures + the Neighborhood
Parks Manual capacity benchmarks + a computed walk-catchment model to answer:
  "How many people realistically depend on this park, and can the design's
   capacity actually serve them?"

REAL SOURCED INPUTS:
  Population (Dubai Statistics Center, 2023 Population Bulletin for Emirate of Dubai):
    - Umm Suqeim First  (Community 356): 7,443 residents
    - Umm Suqeim Second (Community 362): 9,220 residents
    - Umm Suqeim Third  (Community 366): 4,867 residents
    - Al Safa community: 16,986 residents; density 3,800 persons/km2; area 4.5 km2
  Park capacity benchmark (Dubai Municipality Neighborhood Parks Manual):
    - 150-400 visitors per 10,000 sqm  ->  for 15,000 sqm = 225-600 peak visitors
    - visit duration 1-3 hours; operating 05:00-23:00

Retrieved via live WebSearch on 2026-07-24 (Dubai Statistics Center + Wikipedia
community pages citing DSC). Walk-catchment geometry is computed, not assumed.
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUT = os.path.join(os.path.dirname(__file__), "..", "13_Catchment_Demand_Analysis", "outputs")
os.makedirs(OUT, exist_ok=True)

# --- REAL sourced population figures ---
communities = {
    "Umm Suqeim First (356)": 7443,
    "Umm Suqeim Second (362)": 9220,
    "Umm Suqeim Third (366)": 4867,
    "Al Safa": 16986,
}
AL_SAFA_DENSITY = 3800  # persons/km2 (sourced: DSC via Wikipedia)

# --- Walk catchment model ---
# Standard neighborhood-park catchment = 400m (5-min walk) and 800m (10-min walk).
# We estimate residents within each radius using the real Al Safa density figure
# (3,800 persons/km2) as the representative local density for the immediate ring,
# since the park sits within/adjacent to Al Safa 2.
radii_m = {"400m (5-min walk)": 400, "800m (10-min walk)": 800, "1200m (15-min walk)": 1200}
demand_rows = []
for label, r in radii_m.items():
    area_km2 = np.pi * (r / 1000) ** 2
    est_residents = int(area_km2 * AL_SAFA_DENSITY)
    demand_rows.append((label, r, round(area_km2, 3), est_residents))

# --- Park capacity (Manual benchmark, real) ---
SITE_SQM = 15000
cap_low = int(150 * SITE_SQM / 10000)   # 225
cap_high = int(400 * SITE_SQM / 10000)  # 600

# --- Demand vs capacity check ---
# Assume a plausible daily park-visitor participation rate of residents within
# the primary 800m catchment (documented as an assumption, clearly labeled).
primary_residents = [d[3] for d in demand_rows if d[0].startswith("800m")][0]
PARTICIPATION_RATE = 0.10  # 10% of primary catchment visits on a given peak day (assumption)
est_daily_visitors = int(primary_residents * PARTICIPATION_RATE)
# Peak-hour concurrency: with 1-3hr visits over an 18hr operating day, roughly
# (avg_visit_hours / operating_hours) of daily visitors are present at once, times a
# peaking factor. Use avg 2hr visit, 18hr day, peaking factor 2.0.
AVG_VISIT_HRS, OP_HOURS, PEAK_FACTOR = 2.0, 18.0, 2.0
est_peak_concurrent = int(est_daily_visitors * (AVG_VISIT_HRS / OP_HOURS) * PEAK_FACTOR)

results = {
    "population_sources": communities,
    "al_safa_density_per_km2": AL_SAFA_DENSITY,
    "walk_catchment": [{"ring": d[0], "radius_m": d[1], "area_km2": d[2], "est_residents": d[3]} for d in demand_rows],
    "park_capacity_benchmark": {"low_peak": cap_low, "high_peak": cap_high, "basis": "Neighborhood Parks Manual 150-400/10,000sqm"},
    "demand_model": {
        "primary_catchment_800m_residents": primary_residents,
        "assumed_participation_rate": PARTICIPATION_RATE,
        "est_daily_visitors": est_daily_visitors,
        "est_peak_concurrent_visitors": est_peak_concurrent,
        "capacity_low": cap_low, "capacity_high": cap_high,
        "verdict": ("Peak concurrent demand fits within benchmark capacity"
                    if est_peak_concurrent <= cap_high else
                    "Peak concurrent demand may EXCEED benchmark capacity - design should plan for overflow")
    }
}
with open(os.path.join(OUT, "catchment_demand_results.json"), "w") as f:
    json.dump(results, f, indent=2)
print(json.dumps(results["demand_model"], indent=2))

# --- Chart 1: population bar ---
fig, ax = plt.subplots(figsize=(11, 6))
names = list(communities.keys())
vals = list(communities.values())
bars = ax.bar(names, vals, color=["#2a9d8f", "#264653", "#287271", "#e76f51"])
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width()/2, v + 200, f"{v:,}", ha="center", fontsize=9, fontweight="bold")
ax.set_ylabel("Residents (2023)")
ax.set_title("Al Safa 2 Park — Surrounding Community Population\n(Source: Dubai Statistics Center, 2023 Population Bulletin)")
plt.xticks(rotation=15)
plt.tight_layout()
fig.savefig(os.path.join(OUT, "catchment_population.png"), dpi=150)
plt.close(fig)
print("Saved: catchment_population.png")

# --- Chart 2: walk-catchment rings (real geometry) ---
fig, ax = plt.subplots(figsize=(9, 9))
colors_ring = {"400m (5-min walk)": "#2a9d8f", "800m (10-min walk)": "#e9c46a", "1200m (15-min walk)": "#e76f51"}
for label, r in sorted(radii_m.items(), key=lambda x: -x[1]):
    circle = patches.Circle((0, 0), r, alpha=0.25, color=colors_ring[label], label=f"{label}")
    ax.add_patch(circle)
ax.plot(0, 0, "ks", markersize=14, label="Al Safa 2 Park")
for label, r in radii_m.items():
    est = [d[3] for d in demand_rows if d[0] == label][0]
    ax.text(0, r - 60, f"~{est:,} residents", ha="center", fontsize=9, fontweight="bold")
ax.set_xlim(-1300, 1300)
ax.set_ylim(-1300, 1300)
ax.set_aspect("equal")
ax.legend(loc="upper right", fontsize=9)
ax.set_title("Al Safa 2 Park — Walk Catchment Rings & Estimated Residents\n(rings computed; density from Dubai Statistics Center)")
ax.set_xlabel("Distance (m)")
plt.tight_layout()
fig.savefig(os.path.join(OUT, "catchment_rings.png"), dpi=150)
plt.close(fig)
print("Saved: catchment_rings.png")

# --- Chart 3: demand vs capacity ---
fig, ax = plt.subplots(figsize=(10, 5))
ax.barh(["Benchmark capacity\n(peak, high)"], [cap_high], color="#2a9d8f", alpha=0.7)
ax.barh(["Benchmark capacity\n(peak, low)"], [cap_low], color="#8ab17d", alpha=0.7)
ax.barh(["Est. peak concurrent\ndemand (model)"], [est_peak_concurrent], color="#e76f51")
for i, v in enumerate([est_peak_concurrent, cap_low, cap_high]):
    ax.text(v + 5, 2 - i, f"{v}", va="center", fontweight="bold")
ax.set_xlabel("Peak Concurrent Visitors")
ax.set_title("Al Safa 2 Park — Estimated Peak Demand vs. Benchmark Capacity")
plt.tight_layout()
fig.savefig(os.path.join(OUT, "demand_vs_capacity.png"), dpi=150)
plt.close(fig)
print("Saved: demand_vs_capacity.png")

# --- Summary ---
with open(os.path.join(OUT, "catchment_demand_summary.txt"), "w", encoding="utf-8") as f:
    f.write("PHASE 1.13 - CATCHMENT & DEMAND ANALYSIS (REAL DATA)\n")
    f.write("=" * 60 + "\n\n")
    f.write("REAL SOURCED POPULATION (Dubai Statistics Center, 2023):\n")
    for k, v in communities.items():
        f.write(f"  {k}: {v:,} residents\n")
    total_named = sum(communities.values())
    f.write(f"  Total named surrounding communities: {total_named:,} residents\n\n")
    f.write("WALK CATCHMENT (computed rings x real Al Safa density 3,800/km2):\n")
    for d in demand_rows:
        f.write(f"  {d[0]}: ~{d[3]:,} residents within {d[1]}m\n")
    f.write(f"\nPARK CAPACITY (Neighborhood Parks Manual benchmark, 15,000 sqm):\n")
    f.write(f"  Peak capacity range: {cap_low}-{cap_high} concurrent visitors\n\n")
    f.write("DEMAND MODEL:\n")
    f.write(f"  Primary (800m) catchment: ~{primary_residents:,} residents\n")
    f.write(f"  Assumed peak-day participation: {PARTICIPATION_RATE*100:.0f}% -> ~{est_daily_visitors:,} daily visitors\n")
    f.write(f"  Est. peak concurrent visitors: ~{est_peak_concurrent}\n")
    f.write(f"  VERDICT: {results['demand_model']['verdict']}\n\n")
    f.write("NOTE: Population figures are REAL (Dubai Statistics Center 2023). The\n")
    f.write("participation rate and peaking factors are clearly-labeled planning\n")
    f.write("assumptions, not measured data - stated so they can be challenged/tuned.\n")
print("Saved: catchment_demand_summary.txt")
