"""
Phase 7.9 UPGRADE - Annual Operations & Maintenance (O&M) Cost Model
Computes the park's yearly running cost (not just the one-off build cost),
anchored on REAL figures: the computed water budget (Phase 7.4), the real DEWA
water tariff (~AED 7.7/m3 + surcharge, sourced 2026-07-24), and the computed
build cost (Phase 7.10). Non-water items use standard landscape-O&M ratios,
explicitly labelled.
"""

import os
import json
import matplotlib.pyplot as plt

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "..", "outputs")

with open(os.path.join(OUT, "water_demand_results.json")) as f:
    water = json.load(f)
with open(os.path.join(OUT, "cost_estimate_results.json")) as f:
    build = json.load(f)

# ---- Real anchors ----
WATER_TARIFF_AED_M3 = 7.70 + 1.10   # DEWA water 0-27m3 slab + fuel surcharge (sourced 2026-07-24)
annual_water_m3 = water["annual_total_water_m3"]
build_total = build["total_AED"]

# ---- O&M line items ----
# 1. Water (REAL: computed volume x real tariff)
water_cost = annual_water_m3 * WATER_TARIFF_AED_M3

# 2. Horticulture/landscape maintenance labour+materials
#    Industry standard: ~5-7% of landscape build cost per year. Use 6% (mid).
hort_cost = build_total * 0.06

# 3. Electricity (lighting + smart infra + irrigation pumps)
#    Estimated from lighting/smart line items (Phase 7.10) running cost ~ standard load.
elec_cost = 180_000   # order-of-magnitude annual electricity for a 1.5ha lit public park

# 4. Cleaning, waste, minor repairs
cleaning_cost = build_total * 0.02

# 5. Facilities/kiosk servicing + security (public park)
facilities_cost = 250_000

items = [
    ("Irrigation water (computed vol × real DEWA tariff)", water_cost, "REAL"),
    ("Horticulture maintenance (6% of build cost)", hort_cost, "ratio"),
    ("Electricity (lighting, pumps, smart infra)", elec_cost, "estimate"),
    ("Cleaning, waste & minor repairs (2% of build)", cleaning_cost, "ratio"),
    ("Facilities servicing & security", facilities_cost, "estimate"),
]
total_om = sum(v for _, v, _ in items)

print("ANNUAL O&M COST ESTIMATE:")
for label, val, tag in items:
    print(f"  [{tag:8}] {label}: AED {val:,.0f}")
print(f"  TOTAL ANNUAL O&M: AED {total_om:,.0f}")
print(f"  (Water tariff used: AED {WATER_TARIFF_AED_M3}/m3 on {annual_water_m3:,} m3)")
print(f"  O&M as % of build cost: {100*total_om/build_total:.1f}%/year")

result = {
    "water_tariff_AED_m3": WATER_TARIFF_AED_M3,
    "annual_water_m3": annual_water_m3,
    "line_items": [{"item": l, "annual_AED": round(v), "basis": t} for l, v, t in items],
    "total_annual_om_AED": round(total_om),
    "build_cost_AED": build_total,
    "om_pct_of_build": round(100*total_om/build_total, 1),
    "cost_over_10yr_AED": round(build_total + total_om*10),
}
with open(os.path.join(OUT, "om_cost_results.json"), "w") as f:
    json.dump(result, f, indent=2)
print("Saved: om_cost_results.json")

# ---- Chart: O&M pie ----
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
labels = [l.split(" (")[0] for l, _, _ in items]
vals = [v for _, v, _ in items]
colors = ["#457b9d", "#2a9d8f", "#e9c46a", "#f4a261", "#e76f51"]
ax1.pie(vals, labels=[f"{l}\nAED {v/1000:.0f}k" for l, v in zip(labels, vals)],
        colors=colors, autopct="%1.0f%%", startangle=90, textprops={"fontsize": 8})
ax1.set_title(f"Annual O&M Breakdown — Total AED {total_om/1e6:.2f}M/year")

# ---- Chart: 10-year total cost of ownership ----
years = list(range(0, 11))
cumulative = [build_total + total_om*y for y in years]
ax2.plot(years, [c/1e6 for c in cumulative], "o-", color="#264653", lw=2)
ax2.fill_between(years, [build_total/1e6]*len(years), [c/1e6 for c in cumulative], alpha=0.15, color="#2a9d8f")
ax2.axhline(build_total/1e6, color="gray", ls="--", label=f"Build cost (AED {build_total/1e6:.1f}M)")
ax2.set_xlabel("Year"); ax2.set_ylabel("Cumulative cost (AED millions)")
ax2.set_title("10-Year Total Cost of Ownership\n(build + annual O&M)")
ax2.legend()
plt.tight_layout()
fig.savefig(os.path.join(OUT, "om_cost.png"), dpi=160)
plt.close(fig)
print("Saved: om_cost.png")
print(f"10-year total cost of ownership: AED {(build_total + total_om*10)/1e6:.1f}M")
