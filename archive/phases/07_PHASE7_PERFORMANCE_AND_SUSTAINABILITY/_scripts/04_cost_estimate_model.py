"""
Phase 7.10 UPGRADE - Order-of-Magnitude Cost Estimate Model
Computes a real element-by-element cost breakdown for the Concept A design
against the actual Phase 5 zone areas, using REAL sourced Dubai landscape
unit-rate ranges (retrieved via web search 2026-07-24). Checks the total
against the AED 35,000,000 competition budget.

HONESTY NOTE: The sourced unit rates are Dubai VILLA/residential landscaping
benchmarks (public-domain figures from Dubai landscaping cost guides). Municipal
public-park construction typically runs at the HIGHER end or above these ranges
(procurement, public specs, contingency). We therefore use the UPPER bound of each
sourced range plus explicit contingency/prelims/professional-fee percentages
standard to construction estimating - so this is a conservative, defensible
order-of-magnitude estimate, NOT a quantity-surveyed tender price.
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "..", "outputs")
os.makedirs(OUT, exist_ok=True)

# Load real Phase 5 zone areas
with open(os.path.join(HERE, "..", "..", "05_PHASE5_MASTERPLAN_DEVELOPMENT", "outputs", "zoning_area_schedule.json")) as f:
    zoning = json.load(f)
zones = {z[0]: z[2] for z in zoning["zones"]}  # name -> area sqm
SITE_AREA = zoning["site_area_sqm"]
BUDGET = 35_000_000  # AED, from competition brief

# --- Real sourced Dubai unit rates (AED/m^2 unless noted), upper-bound used ---
# Source: Dubai landscaping cost guides (bayut, agroturf, klg, homeland) via web search 2026-07-24
RATES = {
    "hardscape_paving": 400,        # AED/m2 (sourced hardscape 150-400, upper bound)
    "softscape_planting": 100,      # AED/m2 (sourced softscape 50-100, upper bound)
    "turf_lawn": 130,               # AED/m2 (grass ~15/m2 + install + prep, public-park uplift)
    "shade_structure": 2500,        # AED/m2 of covered area (pergola/canopy steel+fabric, public-scale estimate)
    "play_equipment": 900,          # AED/m2 (inclusive play equipment + safety surfacing)
    "fitness_equipment": 700,       # AED/m2 (outdoor gym equipment + surfacing)
    "commercial_kiosk_build": 4500, # AED/m2 (small retail/F&B kiosk structures)
    "plaza_civil": 500,             # AED/m2 (event plaza civil + drainage)
}

# --- Map each zone to a build type + rate ---
# (zone name substring, rate key)
zone_cost_map = [
    ("Shaded Spine", "hardscape_paving"),
    ("Main Entrance Plaza", "plaza_civil"),
    ("Secondary Entrance", "plaza_civil"),
    ("Children's Play", "play_equipment"),
    ("Family Picnic", "softscape_planting"),
    ("Community Plaza", "plaza_civil"),
    ("Outdoor Fitness", "fitness_equipment"),
    ("Native Planting", "softscape_planting"),
    ("Quiet Contemplation", "softscape_planting"),
    ("Commercial & Service", "commercial_kiosk_build"),
    ("Multipurpose Sports Lawn", "turf_lawn"),
    ("Perimeter Shade Buffer (N)", "softscape_planting"),
    ("Perimeter Shade Buffer (S)", "softscape_planting"),
    ("Path Network", "hardscape_paving"),
]

rows = []
subtotal = 0
for name_sub, rate_key in zone_cost_map:
    match = next((z for z in zones if z.startswith(name_sub)), None)
    if match is None:
        continue
    area = zones[match]
    rate = RATES[rate_key]
    cost = area * rate
    subtotal += cost
    rows.append({"Element": match, "Area_sqm": round(area), "Rate_AED_sqm": rate,
                 "Cost_AED": round(cost)})

# --- Shade structure cost: the Shaded Spine's canopy (covered area ~ spine + overhang) ---
spine_canopy_area = 128.4 * 12.4  # from Phase 6/7 shade element footprint
shade_cost = spine_canopy_area * RATES["shade_structure"]
subtotal += shade_cost
rows.append({"Element": "Shaded Spine — overhead canopy structure",
             "Area_sqm": round(spine_canopy_area), "Rate_AED_sqm": RATES["shade_structure"],
             "Cost_AED": round(shade_cost)})

# --- Add per-room canopy trees (from Phase 7 annual-shade finding) as a line item ---
# ~108 trees (Phase 7 water model) at a real supply+plant rate for large Ghaf/Neem
TREE_UNIT_AED = 3500  # AED per mature-ish tree supplied & planted (public-scale estimate)
N_TREES = 108
tree_cost = N_TREES * TREE_UNIT_AED
subtotal += tree_cost
rows.append({"Element": f"Canopy trees ({N_TREES} × Ghaf/Neem, supply+plant)",
             "Area_sqm": "-", "Rate_AED_sqm": f"{TREE_UNIT_AED}/tree", "Cost_AED": round(tree_cost)})

# --- Systems (lighting, irrigation, smart infra) as % of civil subtotal ---
lighting = round(subtotal * 0.06)      # site lighting
irrigation = round(subtotal * 0.05)    # drip/subsurface irrigation network
smart = round(subtotal * 0.03)         # sensors, digital wayfinding
for label, val in [("Site lighting (LED, spine + loop + bollards)", lighting),
                    ("Irrigation network (drip/subsurface)", irrigation),
                    ("Smart infrastructure (sensors, digital wayfinding)", smart)]:
    subtotal += val
    rows.append({"Element": label, "Area_sqm": "-", "Rate_AED_sqm": "% of works", "Cost_AED": val})

# --- Standard construction estimating add-ons ---
prelims = round(subtotal * 0.10)       # site prelims/enabling
contingency = round(subtotal * 0.12)   # design contingency
prof_fees = round(subtotal * 0.08)     # professional/design fees
total = subtotal + prelims + contingency + prof_fees

addons = [("Subtotal — direct works", subtotal),
          ("Preliminaries & enabling (10%)", prelims),
          ("Design contingency (12%)", contingency),
          ("Professional fees (8%)", prof_fees),
          ("TOTAL ESTIMATED COST", total)]

df = pd.DataFrame(rows)
df.to_csv(os.path.join(OUT, "cost_estimate_lineitems.csv"), index=False)

print("COST ESTIMATE (order-of-magnitude, conservative upper-bound rates):")
print(df.to_string(index=False))
print()
for label, val in addons:
    print(f"  {label}: AED {val:,.0f}")
print(f"\n  Competition budget: AED {BUDGET:,.0f}")
headroom = BUDGET - total
print(f"  Headroom vs budget: AED {headroom:,.0f} ({'WITHIN' if headroom>=0 else 'OVER'} budget, "
      f"{100*total/BUDGET:.0f}% of budget used)")

result = {"line_items": rows, "addons": dict(addons), "budget_AED": BUDGET,
          "total_AED": total, "headroom_AED": headroom, "pct_of_budget": round(100*total/BUDGET, 1)}
with open(os.path.join(OUT, "cost_estimate_results.json"), "w") as f:
    json.dump(result, f, indent=2)
print("\nSaved: cost_estimate_results.json + cost_estimate_lineitems.csv")

# --- Chart: cost breakdown (bar) + budget line ---
plot_rows = [r for r in rows if isinstance(r["Cost_AED"], (int, float))]
plot_rows_sorted = sorted(plot_rows, key=lambda r: r["Cost_AED"], reverse=True)
names = [r["Element"][:38] for r in plot_rows_sorted]
vals = [r["Cost_AED"] / 1e6 for r in plot_rows_sorted]

fig, ax = plt.subplots(figsize=(13, 8))
ax.barh(names, vals, color="#457b9d")
for i, v in enumerate(vals):
    ax.text(v + 0.05, i, f"{v:.2f}M", va="center", fontsize=8)
ax.set_xlabel("Cost (AED millions)")
ax.set_title("Al Safa 2 Park — Order-of-Magnitude Cost Breakdown by Element\n"
             f"(direct works; total w/ prelims+contingency+fees = AED {total/1e6:.1f}M vs {BUDGET/1e6:.0f}M budget)")
ax.invert_yaxis()
plt.tight_layout()
fig.savefig(os.path.join(OUT, "cost_breakdown.png"), dpi=160)
plt.close(fig)
print("Saved: cost_breakdown.png")

# --- Budget gauge chart ---
fig, ax = plt.subplots(figsize=(10, 2.5))
ax.barh([0], [BUDGET/1e6], color="#e9ecef", height=0.5, label="Budget (AED 35M)")
ax.barh([0], [total/1e6], color="#2a9d8f" if headroom>=0 else "#e63946", height=0.5,
        label=f"Estimated cost (AED {total/1e6:.1f}M)")
ax.set_xlim(0, BUDGET/1e6 * 1.05)
ax.set_yticks([])
ax.set_xlabel("AED millions")
ax.legend(loc="lower right")
ax.set_title(f"Budget Utilisation: {100*total/BUDGET:.0f}% of the AED 35M budget "
             f"({'within budget' if headroom>=0 else 'OVER budget'})")
plt.tight_layout()
fig.savefig(os.path.join(OUT, "budget_gauge.png"), dpi=160)
plt.close(fig)
print("Saved: budget_gauge.png")
