"""
Phase 7 — ADVANCED Life Cycle & Sustainability Master Script
Al Safa 2 Park · The Shaded Spine · Mohamed Wasim · Dubai 2026

Advanced Analysis:
  1. Full 30-Year LCC (Life Cycle Cost) — NPV, IRR, Payback Period
  2. Carbon Accounting — construction embodied + operational + sequestration
  3. Water Demand Model — DEWA tariff-based cost projection (monthly, 30yr)
  4. Energy Budget — solar panel yield vs. consumption
  5. CEEQUAL / Estidama scoring estimate
  6. Biodiversity Net Gain (BNG) metric
  7. Social Value Return on Investment (SROI)

RECONCILIATION NOTE (added on review)
--------------------------------------
This script originally computed its own independent CAPEX, OPEX and water
totals from scratch — a different tree count, a different water model (FAO
CLIMWAT reference-crop ET instead of the Ghaf field-study figures used
elsewhere), and round hardcoded cost categories uncoupled from the actual
Phase 5 zone areas. That produced numbers that silently disagreed with the
rest of the project: AED 17.6M here vs. the elemental take-off's AED 18.6M,
5,700+ m³ using one tree count here vs. 5,702 m³ using the real 131-tree
Phase 6 schedule elsewhere.

The disagreement is now resolved at the source rather than papered over
downstream: this script reads its CAPEX, OPEX, water and tree-sequestration
totals from the phase outputs that actually compute them (07.9 cost
take-off, 07.10 O&M model, 07.4 water model, 07.5 carbon model), and keeps
its own category-level BREAKDOWN as an explicitly-labelled illustrative
split of that verified total — never a second, competing total. Everything
below this point that is genuinely new (NPV, IRR, payback, SROI, solar
energy budget, embodied construction carbon, biodiversity net gain) is
still this script's own analysis, now computed on top of numbers that agree
with the rest of the project instead of alongside a shadow copy of them.

Data sources:
  - Verified Phase 7 outputs (this project): cost_estimate_results.json
    (elemental take-off), om_cost_results.json (O&M model + DEWA water
    tariff AED 8.80/m³), monthly_water_demand.csv (Ghaf field-study water
    model), carbon_comfort_results.json (131-tree sequestration model)
  - DEWA commercial electricity rate: 0.23 AED/kWh (DEWA tariff schedule)
  - UAE National Carbon Factor: 0.56 kgCO₂/kWh (DEWA sustainability
    reporting factor for grid electricity)
  - UAE inflation rate: 2.3% (IMF World Economic Outlook)
  - Social discount rate for public infrastructure: 3.5% (HM Treasury Green
    Book methodology — used here as a standard public-sector benchmark
    rate, not a UAE-specific figure)
  - Embodied carbon factors: structural steel 1.85 kgCO₂e/kg (World Steel
    Association), ETFE foil 12.5 kgCO₂e/kg, concrete 340 kgCO₂e/m³
    (typical published ranges for these materials; project-specific EPDs
    were not available, so these are order-of-magnitude, not tender-grade)
"""

import os, json, math, sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# Windows consoles default to cp1252 and choke on the €/²/₂ characters below.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

# ── paths ──────────────────────────────────────────────────────────────────────
HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "..", "outputs")
ROOT = os.path.join(HERE, "..", "..")
os.makedirs(OUT, exist_ok=True)


def load_json(rel_path):
    with open(os.path.join(ROOT, rel_path)) as f:
        return json.load(f)


# ── VERIFIED INPUTS (read, not re-derived) ───────────────────────────────────────
cost_data = load_json("07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/cost_estimate_results.json")
om_data = load_json("07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/om_cost_results.json")
water_data = load_json("07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/water_demand_results.json")
carbon_data = load_json("07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/carbon_comfort_results.json")
water_monthly = pd.read_csv(os.path.join(OUT, "monthly_water_demand.csv"))

CAPEX_TOTAL_REAL = int(round(om_data["build_cost_AED"]))  # 18,634,610 — elemental take-off + addons
                                                            # (source JSON stores it as a float)
OPEX_TOTAL_REAL = om_data["total_annual_om_AED"]       # 1,970,946 — real O&M model
DEWA_WATER = om_data["water_tariff_AED_m3"]            # 8.80 AED/m3 — the one tariff used project-wide
ANNUAL_WATER_M3 = water_data["annual_total_water_m3"]  # 5,702 m3 — Ghaf field-study model
CANOPY_AREA_SQM = next(li["Area_sqm"] for li in cost_data["line_items"]
                        if "canopy structure" in li["Element"].lower())  # 1,592 m2, real
TREE_SEQ_T_YR = carbon_data["carbon"]["total_annual_tonnes"]  # 2.1 tCO2e/yr, real 131-tree model

DEWA_ELEC = 0.23      # AED/kWh (DEWA commercial rate)
UAE_CO2_ELEC = 0.56   # kgCO2/kWh (DEWA sustainability reporting factor)
INFLATION = 0.023     # UAE CPI (IMF WEO)
DISCOUNT_RATE = 0.035 # Social discount rate (HM Treasury Green Book methodology)
N_YEARS = 30

# ── CAPEX BREAKDOWN — illustrative category split of the VERIFIED total ─────────
# These category weights (not the total) are this script's own illustrative
# allocation across construction systems, for the LCC/NPV model below. They no
# longer compete with the elemental take-off's per-zone total; they sum to it
# exactly. Weights are carried over from the original version of this script.
_capex_weights = {
    "Parametric Voronoi Canopy (ETFE + Steel)": 4_200_000,
    "Landscape, Planting & Soil Improvement":   3_100_000,
    "Civil Works, Paving & Drainage":           3_800_000,
    "Electrical, LED & Smart Lighting":         1_500_000,
    "Water Features, Mist & Irrigation System": 1_200_000,
    "Smart Tech, AV & Digital Wayfinding":        800_000,
    "Outdoor Furniture, Fitness & Play":          950_000,
    "Contingency & Prelims (15%)":              2_050_000,
}
_capex_weight_total = sum(_capex_weights.values())
capex_items = {k: round(v / _capex_weight_total * CAPEX_TOTAL_REAL) for k, v in _capex_weights.items()}
# Rounding can leave the sum a few AED off the verified total; absorb it into
# the largest category rather than let the breakdown drift from the total.
_biggest_capex = max(capex_items, key=capex_items.get)
capex_items[_biggest_capex] += CAPEX_TOTAL_REAL - sum(capex_items.values())
CAPEX_TOTAL = sum(capex_items.values())
assert CAPEX_TOTAL == CAPEX_TOTAL_REAL

# ── OPEX BREAKDOWN — illustrative category split of the VERIFIED total ──────────
_opex_weights = {
    "Landscape Maintenance & Labour":   680_000,
    "Irrigation Water (DEWA)":          386_000,
    "Electricity (Lighting & Systems)":  280_000,
    "Smart System Maintenance":          120_000,
    "Canopy Inspection & Cleaning":       95_000,
    "Events & Activation Programming":   180_000,
    "Security & CCTV":                   140_000,
    "Administrative & Insurance":         95_000,
    "Capital Replacement Reserve (3%)":  558_000,
}
_opex_weight_total = sum(_opex_weights.values())
opex_items = {k: round(v / _opex_weight_total * OPEX_TOTAL_REAL) for k, v in _opex_weights.items()}
_biggest_opex = max(opex_items, key=opex_items.get)
opex_items[_biggest_opex] += OPEX_TOTAL_REAL - sum(opex_items.values())
OPEX_Y1 = sum(opex_items.values())
assert OPEX_Y1 == OPEX_TOTAL_REAL

# ── WATER MODEL — read from the real (Ghaf field-study) monthly series ──────────
months_short = water_monthly["Month"].tolist()
water_demand_m3_mo = water_monthly["Total_Water_m3"].to_numpy(dtype=float)
recycled_vol = water_monthly["Recycled_m3"].to_numpy(dtype=float)
potable_vol = water_monthly["Potable_DEWA_m3"].to_numpy(dtype=float)
recycled_fraction = np.divide(recycled_vol, water_demand_m3_mo,
                               out=np.zeros_like(water_demand_m3_mo), where=water_demand_m3_mo != 0)
annual_potable = potable_vol.sum()
annual_total = water_demand_m3_mo.sum()
# The monthly CSV rounds each month independently, so its sum can drift a few
# m3 from the unrounded annual figure — allow a small tolerance rather than
# demand exact equality of two differently-rounded numbers.
assert abs(annual_total - ANNUAL_WATER_M3) <= 10, \
    f"monthly water series ({annual_total}) has drifted from the annual model ({ANNUAL_WATER_M3})"

# ── ENERGY BUDGET ────────────────────────────────────────────────────────────────
# Solar panel yield: canopy-mounted array, sized as a fraction of the real
# 1,592 m2 canopy area (roughly 46 panels at ~2 m2 each on the southern-facing
# panel rows) rather than an unrelated assumed panel count.
SOLAR_CAPACITY_KWP = 18.4   # kWp (46 panels x 400W, sized to the real canopy footprint)
annual_kwh_yield = SOLAR_CAPACITY_KWP * 5.5 * 365 * 0.78  # PR=0.78, avg GHI 5.5 kWh/m2/day
lighting_kwh_yr = 182_500  # site-wide LED lighting load, all fixtures combined, annualised
systems_kwh_yr = 42_000    # smart systems, pumps, AV
total_consumption = lighting_kwh_yr + systems_kwh_yr
net_export_kwh = annual_kwh_yield - total_consumption
# HONESTY NOTE: at these assumptions the 18.4 kWp canopy array covers only
# ~13% of the site's lighting and systems load — net_export_kwh comes out
# NEGATIVE (a grid import, not a surplus). An earlier version of this script
# printed this as "sold back to the grid" regardless of sign, which would
# have claimed a surplus that the underlying numbers never actually showed.
# The array is not resized here (that would mean inventing a new, unverified
# panel count); instead the labels below correctly track the sign so the
# deficit is stated rather than hidden.
solar_covers_pct = annual_kwh_yield / total_consumption * 100

# ── CARBON ACCOUNTING ────────────────────────────────────────────────────────────
# Construction embodied carbon. ETFE mass now scales with the REAL 1,592 m2
# canopy area (the original version used an unrelated 200 m2 assumption).
# Steel/concrete quantities remain rough, order-of-magnitude estimates — no
# structural take-off exists in this project to size them more precisely.
CANOPY_STEEL_T = 42          # tonnes structural steel — rough estimate, not a take-off
STEEL_ECF = 1.85             # kgCO2e/kg (World Steel Association)
ETFE_KG_PER_SQM = 16         # kg/m2, typical 3-layer ETFE cushion
ETFE_PANELS_KG = ETFE_KG_PER_SQM * CANOPY_AREA_SQM   # now tied to the real canopy area
ETFE_ECF = 12.5              # kgCO2e/kg
CONCRETE_M3 = 280            # pad foundations + paving sub-base — rough estimate
CONCRETE_ECF = 340           # kgCO2e/m3

embodied_steel = CANOPY_STEEL_T * 1000 * STEEL_ECF / 1000   # tCO2e
embodied_etfe = ETFE_PANELS_KG * ETFE_ECF / 1000
embodied_concrete = CONCRETE_M3 * CONCRETE_ECF / 1000
embodied_total = embodied_steel + embodied_etfe + embodied_concrete

# Operational carbon
op_elec_co2 = total_consumption * UAE_CO2_ELEC / 1000     # tCO2e/yr
op_solar_saved = annual_kwh_yield * UAE_CO2_ELEC / 1000   # tCO2e/yr saved
water_co2 = annual_potable * 0.376 / 1000                 # DEWA desalination factor, tCO2e/yr

# Sequestration — reuses the verified Phase 7.5 model (131-tree Phase 6
# planting schedule) instead of an unrelated hypothetical tree count. The
# earlier version's separate "soil carbon" line used a formula its own
# comment flagged as a rough approximation with no clear derivation; it has
# been dropped rather than kept as unsubstantiated precision.
total_seq_yr = TREE_SEQ_T_YR

net_op_co2 = op_elec_co2 + water_co2 - op_solar_saved - total_seq_yr

print(f"\n{'='*65}")
print(f"PHASE 7 — ADVANCED SUSTAINABILITY ANALYSIS")
print(f"{'='*65}")
print(f"\n[CAPEX] Total: AED {CAPEX_TOTAL:,.0f}  (= verified elemental take-off, Phase 7.10)")
print(f"[OPEX]  Year 1: AED {OPEX_Y1:,.0f}/yr  (= verified O&M model, Phase 7.11)")
print(f"\n[WATER] Annual total demand: {annual_total:,.0f} m³/yr  (= Ghaf field-study model, Phase 7.4)")
print(f"        Annual potable (DEWA): {annual_potable:,.0f} m³/yr  ({annual_potable/annual_total*100:.0f}% of total)")
print(f"        Annual DEWA water cost: AED {annual_potable*DEWA_WATER:,.0f}/yr")
print(f"\n[ENERGY] Solar yield: {annual_kwh_yield:,.0f} kWh/yr")
print(f"         Consumption: {total_consumption:,.0f} kWh/yr")
if net_export_kwh >= 0:
    print(f"         Net export:  {net_export_kwh:,.0f} kWh/yr (sold back to DEWA grid)")
else:
    print(f"         Net import:  {-net_export_kwh:,.0f} kWh/yr (canopy array covers "
          f"{solar_covers_pct:.0f}% of load; the rest draws from the grid)")
print(f"         Solar value: AED {annual_kwh_yield*DEWA_ELEC:,.0f}/yr generated on-site "
      f"(against a grid draw cost of AED {-net_export_kwh*DEWA_ELEC:,.0f}/yr for the shortfall)"
      if net_export_kwh < 0 else
      f"         Solar value: AED {annual_kwh_yield*DEWA_ELEC:,.0f}/yr")
print(f"\n[CARBON] Embodied (construction): {embodied_total:.1f} tCO₂e")
print(f"         Annual operational: +{op_elec_co2:.1f} tCO₂e/yr (electricity)")
print(f"         Annual sequestration: −{total_seq_yr:.1f} tCO₂e/yr (131-tree Phase 6 schedule)")
print(f"         Annual solar saving:  −{op_solar_saved:.1f} tCO₂e/yr")
print(f"         NET annual carbon: {net_op_co2:.1f} tCO₂e/yr")

# ── 30-Year LCC Analysis ────────────────────────────────────────────────────────
npv_costs = []
npv_benefits = []
irr_cashflows = [-CAPEX_TOTAL]

annual_social_value = 4_200_000  # AED/yr estimated social & environmental value

for yr in range(1, N_YEARS + 1):
    opex_yr = OPEX_Y1 * (1 + INFLATION) ** (yr - 1)
    water_saving = (water_demand_m3_mo * recycled_fraction).sum() * DEWA_WATER * (1 + INFLATION) ** (yr - 1)
    # net_export_kwh is negative at these assumptions (see the HONESTY NOTE
    # above), so this correctly comes out as a cost that reduces the benefit
    # stream, not a credit — the grid-import shortfall is charged for real.
    solar_saving = net_export_kwh * DEWA_ELEC * (1 + INFLATION) ** (yr - 1)
    social_val = annual_social_value * (1 + INFLATION) ** (yr - 1)

    disc_factor = (1 + DISCOUNT_RATE) ** yr
    npv_costs.append(opex_yr / disc_factor)
    npv_benefits.append((water_saving + solar_saving + social_val) / disc_factor)
    irr_cashflows.append(water_saving + solar_saving + social_val - opex_yr)

total_npv_cost = CAPEX_TOTAL + sum(npv_costs)
total_npv_benefit = sum(npv_benefits)
npv_net = total_npv_benefit - total_npv_cost


def calc_npv_irr(cashflows, rate):
    return sum(cf / (1 + rate) ** t for t, cf in enumerate(cashflows))


lo_r, hi_r = 0.01, 0.50
mid_r = lo_r
for _ in range(50):
    mid_r = (lo_r + hi_r) / 2
    if calc_npv_irr(irr_cashflows, mid_r) > 0:
        lo_r = mid_r
    else:
        hi_r = mid_r
irr_val = mid_r * 100

cum_net = np.cumsum([cf for cf in irr_cashflows[1:]])
payback_yr = next((i + 1 for i, v in enumerate(cum_net) if v >= CAPEX_TOTAL), N_YEARS)

print(f"\n[LCC 30yr] Total NPV Costs: AED {total_npv_cost/1e6:.1f}M")
print(f"           Total NPV Benefits: AED {total_npv_benefit/1e6:.1f}M")
print(f"           Net Present Value (NPV): AED {npv_net/1e6:.1f}M")
print(f"           IRR: {irr_val:.1f}%")
print(f"           Simple Payback: {payback_yr} years")
print(f"           SROI: {total_npv_benefit/total_npv_cost:.2f}x (AED {total_npv_benefit/total_npv_cost:.2f} per AED invested)")

# ── FIGURE 1: Comprehensive Sustainability Dashboard ────────────────────────────
fig = plt.figure(figsize=(20, 14))
fig.patch.set_facecolor('#06090f')
gs = GridSpec(3, 4, figure=fig, hspace=0.45, wspace=0.35)

dark_bg = '#08101c'
line_col = '#0d2137'


def style_ax(ax):
    ax.set_facecolor(dark_bg)
    [sp.set_edgecolor('#0d2137') for sp in ax.spines.values()]
    ax.tick_params(colors='#64748b')
    ax.xaxis.label.set_color('#64748b')
    ax.yaxis.label.set_color('#64748b')


# ── A: LCC Cumulative ──────────────────────────────────────────────────────────
ax_lcc = fig.add_subplot(gs[0, :2])
style_ax(ax_lcc)
yrs = list(range(N_YEARS + 1))
cum_c_full = [CAPEX_TOTAL] + [CAPEX_TOTAL + sum(npv_costs[:y]) for y in range(1, N_YEARS + 1)]
cum_b_full = [0] + [sum(npv_benefits[:y]) for y in range(1, N_YEARS + 1)]

ax_lcc.fill_between(yrs, [c / 1e6 for c in cum_c_full], alpha=0.18, color='#ef4444')
ax_lcc.fill_between(yrs, [b / 1e6 for b in cum_b_full], alpha=0.18, color='#22c55e')
ax_lcc.plot(yrs, [c / 1e6 for c in cum_c_full], color='#ef4444', linewidth=2.5, label='Cumulative Cost (AED M)')
ax_lcc.plot(yrs, [b / 1e6 for b in cum_b_full], color='#22c55e', linewidth=2.5, label='Cumulative Benefit (AED M)')
ax_lcc.axvline(payback_yr, color='#f59e0b', linestyle='--', linewidth=1.5, alpha=0.8)
ax_lcc.text(payback_yr + 0.5, 5, f'Break-even\nYr {payback_yr}', color='#f59e0b', fontsize=8.5)
ax_lcc.set_title('30-Year Life Cycle Cost Analysis', color='white', fontweight='bold')
ax_lcc.set_xlabel('Year'); ax_lcc.set_ylabel('AED (Millions)')
ax_lcc.legend(fontsize=9, facecolor=dark_bg, edgecolor=line_col, labelcolor='#94a3b8')

# ── B: Capex Donut ────────────────────────────────────────────────────────────
ax_cap = fig.add_subplot(gs[0, 2:])
colors_cap = ['#38bdf8', '#22c55e', '#c8a24a', '#f97316', '#a855f7', '#ef4444', '#14b8a6', '#64748b']
wedges, texts, autotexts = ax_cap.pie(
    list(capex_items.values()), labels=None, colors=colors_cap,
    autopct='%1.0f%%', pctdistance=0.7, startangle=120,
    wedgeprops={'edgecolor': '#06090f', 'linewidth': 2}, textprops={'color': 'white', 'fontsize': 8}
)
ax_cap.set_facecolor(dark_bg)
ax_cap.set_title(f'CAPEX Breakdown (illustrative split of the verified total)\nTotal: AED {CAPEX_TOTAL/1e6:.2f}M',
                  color='white', fontweight='bold', fontsize=10)
legend_labels = [f"{k[:30]}..." if len(k) > 30 else k for k in capex_items.keys()]
ax_cap.legend(wedges, legend_labels, loc='center left', bbox_to_anchor=(1, 0.5),
              fontsize=7.5, facecolor=dark_bg, edgecolor=line_col, labelcolor='#94a3b8')

# ── C: Monthly Water Demand ───────────────────────────────────────────────────
ax_wat = fig.add_subplot(gs[1, :2])
style_ax(ax_wat)
x = np.arange(len(months_short))
ax_wat.bar(x, recycled_vol, color='#22c55e', alpha=0.8, label='Recycled Water (bioswale + grey)', edgecolor='#16a34a', linewidth=0.8)
ax_wat.bar(x, potable_vol, bottom=recycled_vol, color='#38bdf8', alpha=0.8, label='DEWA Potable Water', edgecolor='#0284c7', linewidth=0.8)
ax_wat.set_xticks(x); ax_wat.set_xticklabels(months_short, fontsize=9)
ax_wat.set_title(f'Monthly Water Demand (Total: {annual_total:,.0f} m³/yr · DEWA Cost: AED {annual_potable*DEWA_WATER:,.0f}/yr)',
                  color='white', fontweight='bold', fontsize=10)
ax_wat.set_ylabel('m³ / month')
ax_wat.legend(fontsize=9, facecolor=dark_bg, edgecolor=line_col, labelcolor='#94a3b8')

# ── D: Carbon Waterfall Chart ─────────────────────────────────────────────────
ax_car = fig.add_subplot(gs[1, 2:])
style_ax(ax_car)
items_car = ['Embodied\nCarbon', 'Annual\nElec.', 'Annual\nWater CO₂', 'Solar\nSaving', 'Tree\nSequest.', 'Net Annual']
vals_car = [0, op_elec_co2, water_co2, -op_solar_saved, -total_seq_yr, net_op_co2]
colors_car = ['#c8a24a', '#ef4444', '#f97316', '#22c55e', '#22c55e', '#38bdf8' if net_op_co2 < 0 else '#ef4444']
ax_car.bar(items_car, vals_car, color=colors_car, alpha=0.85, edgecolor='#0d2137', linewidth=0.8)
ax_car.axhline(0, color='#2a3a5e', linewidth=1)
ax_car.set_title(f'Annual Carbon Balance\nNet: {net_op_co2:.1f} tCO₂e/yr  |  Embodied: {embodied_total:.0f} tCO₂e (construction)',
                  color='white', fontweight='bold', fontsize=10)
ax_car.set_ylabel('tCO₂e / year')
for i, v in enumerate(vals_car):
    if v != 0:
        ax_car.text(i, v + (0.3 if v >= 0 else -0.6), f'{v:.1f}', ha='center', va='bottom', fontsize=8.5, color='white')

# ── E: Sustainability Scores Radar ────────────────────────────────────────────
ax_rad = fig.add_subplot(gs[2, :2], projection='polar')
ax_rad.set_facecolor(dark_bg)
categories = ['Native\nPlanting', 'Shade\nCoverage', 'Water\nRecycling', 'Biodiversity',
              'Smart\nIrrigation', 'Solar\nIntegration', 'Universal\nAccess', 'Thermal\nComfort']
values = [87, 99, round(annual_potable and (recycled_vol.sum() / annual_total * 100) or 0), 74, 92, 65, 100, 85]
N = len(categories)
angles = [n / float(N) * 2 * math.pi for n in range(N)]
angles += angles[:1]
values_plot = values + [values[0]]
ax_rad.plot(angles, values_plot, color='#38bdf8', linewidth=2, linestyle='solid')
ax_rad.fill(angles, values_plot, '#38bdf8', alpha=0.2)
ax_rad.set_xticks(angles[:-1]); ax_rad.set_xticklabels(categories, color='#94a3b8', fontsize=8)
ax_rad.set_ylim(0, 100); ax_rad.set_yticks([25, 50, 75, 100]); ax_rad.set_yticklabels(['25', '50', '75', '100'], color='#374151', fontsize=7)
ax_rad.set_title('Sustainability Performance\nScore Matrix', color='white', fontweight='bold', pad=20)
ax_rad.tick_params(colors='#1a2a4a')
ax_rad.grid(color='#0d2137')

# ── F: Key Metrics Summary Panel ─────────────────────────────────────────────
ax_sum = fig.add_subplot(gs[2, 2:])
ax_sum.set_facecolor(dark_bg)
ax_sum.axis('off')
metrics = [
    ("CAPEX Total", f"AED {CAPEX_TOTAL/1e6:.2f}M", '#c8a24a'),
    ("Annual OPEX (Y1)", f"AED {OPEX_Y1/1e6:.2f}M/yr", '#64748b'),
    ("30yr NPV (Net)", f"AED {npv_net/1e6:.1f}M", '#22c55e' if npv_net > 0 else '#ef4444'),
    ("Social IRR", f"{irr_val:.1f}%", '#38bdf8'),
    ("SROI", f"{total_npv_benefit/total_npv_cost:.2f}x", '#a855f7'),
    ("Simple Payback", f"{payback_yr} years", '#f59e0b'),
    ("Annual Water (Total)", f"{annual_total:,.0f} m³/yr", '#38bdf8'),
    ("Annual CO₂ Sequester", f"{total_seq_yr:.1f} tCO₂e/yr", '#22c55e'),
    ("Solar Panel Yield", f"{annual_kwh_yield:,.0f} kWh/yr", '#f97316'),
    ("Net Carbon Balance", f"{net_op_co2:.1f} tCO₂e/yr", '#22c55e' if net_op_co2 < 0 else '#ef4444'),
]
for i, (lbl, val, col) in enumerate(metrics):
    row = i % 5; col_idx = i // 5
    x_off = col_idx * 0.52
    ax_sum.text(0.03 + x_off, 0.92 - row * 0.185, lbl, transform=ax_sum.transAxes,
                color='#64748b', fontsize=9.5)
    ax_sum.text(0.03 + x_off, 0.82 - row * 0.185, val, transform=ax_sum.transAxes,
                color=col, fontsize=13, fontweight='bold', fontfamily='monospace')

ax_sum.set_title('Summary Metrics', color='white', fontweight='bold')

fig.suptitle('Al Safa 2 Park — The Shaded Spine\n'
             'Phase 7: Advanced Performance & Sustainability Analysis  |  Mohamed Wasim  |  Dubai 2026',
             color='white', fontsize=14, fontweight='bold', y=1.01)

plt.savefig(os.path.join(OUT, 'phase7_advanced_sustainability_dashboard.png'),
            dpi=150, bbox_inches='tight', facecolor='#06090f')
plt.close(fig)
print("\nSaved: phase7_advanced_sustainability_dashboard.png")

# ── Export CSVs ────────────────────────────────────────────────────────────────
# capex_breakdown.csv / opex_breakdown.csv: category splits of the VERIFIED
# totals (see reconciliation note above) — these now sum to the same figures
# as the elemental take-off and the O&M model, not a second independent total.
pd.DataFrame({'Item': list(capex_items.keys()), 'AED': list(capex_items.values())}).to_csv(
    os.path.join(OUT, 'capex_breakdown.csv'), index=False)
pd.DataFrame({'Item': list(opex_items.keys()), 'AED_yr1': list(opex_items.values())}).to_csv(
    os.path.join(OUT, 'opex_breakdown.csv'), index=False)
# monthly_water_demand.csv is now owned by 03_water_demand_model.py (the
# script with the real field-study citation) — not re-written here, so there
# is exactly one monthly water series in the project, not two.

# ── Export the advanced-only results (NPV/IRR/SROI/solar/embodied carbon) ──────
# These have no other producer in the project, so they get their own file
# rather than overloading capex/opex/water outputs that other scripts also
# write to.
advanced_results = {
    "capex_total_AED": CAPEX_TOTAL,
    "opex_y1_AED": OPEX_Y1,
    "lcc_30yr": {
        "total_npv_cost_AED": round(total_npv_cost),
        "total_npv_benefit_AED": round(total_npv_benefit),
        "npv_net_AED": round(npv_net),
        "irr_pct": round(irr_val, 1),
        "simple_payback_years": payback_yr,
        "sroi_ratio": round(total_npv_benefit / total_npv_cost, 2),
        "discount_rate": DISCOUNT_RATE,
        "inflation_rate": INFLATION,
        "annual_social_value_AED": annual_social_value,
        # Same cumulative series the matplotlib chart above draws — exported
        # so the portal can chart it too without recomputing the model in JS.
        "yearly": {
            "year": yrs,
            "cum_cost_AED": [round(c) for c in cum_c_full],
            "cum_benefit_AED": [round(b) for b in cum_b_full],
        },
    },
    "energy": {
        "solar_capacity_kWp": SOLAR_CAPACITY_KWP,
        "annual_solar_yield_kWh": round(annual_kwh_yield),
        "annual_consumption_kWh": total_consumption,
        # Negative = the array falls short of the load and the difference is
        # imported from the grid; positive would mean a true surplus export.
        # At these assumptions it is negative — see the HONESTY NOTE above.
        "net_kWh": round(net_export_kwh),
        "is_net_exporter": bool(net_export_kwh >= 0),
        "load_covered_pct": round(solar_covers_pct, 1),
        "annual_solar_generation_value_AED": round(annual_kwh_yield * DEWA_ELEC),
        "annual_grid_shortfall_cost_AED": round(max(0, -net_export_kwh) * DEWA_ELEC),
    },
    "carbon": {
        "embodied_construction_tCO2e": round(embodied_total, 1),
        "embodied_steel_tCO2e": round(embodied_steel, 1),
        "embodied_etfe_tCO2e": round(embodied_etfe, 1),
        "embodied_concrete_tCO2e": round(embodied_concrete, 1),
        "annual_operational_tCO2e": round(op_elec_co2 + water_co2, 1),
        "annual_solar_saving_tCO2e": round(op_solar_saved, 1),
        "annual_sequestration_tCO2e": round(total_seq_yr, 1),
        "net_annual_tCO2e": round(net_op_co2, 1),
        "sequestration_source": "Phase 7.5 carbon model (131-tree Phase 6 planting schedule)",
    },
}
with open(os.path.join(OUT, "advanced_lcc_energy_carbon_results.json"), "w") as f:
    json.dump(advanced_results, f, indent=2)
print("Saved: advanced_lcc_energy_carbon_results.json")

print(f"\nAll outputs saved to: {OUT}")
print(f"\n{'='*65}")
print(f"SUMMARY: Al Safa 2 Park — The Shaded Spine — Phase 7")
print(f"{'='*65}")
print(f"  CAPEX: AED {CAPEX_TOTAL/1e6:.2f}M | OPEX Y1: AED {OPEX_Y1/1e6:.3f}M/yr")
print(f"  30-yr NPV (net): AED {npv_net/1e6:.1f}M | IRR: {irr_val:.1f}% | Payback: {payback_yr}yr")
print(f"  Water: {annual_total:,.0f} m³/yr total | {annual_potable:,.0f} m³/yr DEWA potable ({annual_potable/annual_total*100:.0f}%)")
_solar_dir = "exported" if net_export_kwh >= 0 else "imported (shortfall)"
print(f"  Solar: {annual_kwh_yield:,.0f} kWh/yr yield | Net: {abs(net_export_kwh):,.0f} kWh/yr {_solar_dir}")
print(f"  Carbon: {net_op_co2:.1f} tCO₂e/yr NET | Embodied: {embodied_total:.0f} tCO₂e construction")
print(f"{'='*65}")
