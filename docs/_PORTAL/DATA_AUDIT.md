# Data Audit — Al Safa 2 Park

Generated 2026-07-30 14:23 UTC by `_PORTAL/build_portal.py`.

This report cross-checks the computed outputs of every phase against each other. It is regenerated on every build, so it always describes the current state of the data — not a past one.

**10 passed · 1 warnings · 0 failures**

## Checks

| Check | Result | Detail |
|---|---|---|
| Zoning schedule fully allocates the site area | ✅ pass | Zones sum to 15,000.0 m² against a site area of 15,000.0 m² (+0.0 m²). |
| Carbon: species rows reconcile with the annual total | ✅ pass | Species rows sum to 2,124 kgCO₂/yr against a reported total of 2,124 kgCO₂/yr. |
| Tree counts agree between the planting schedule and the carbon model | ✅ pass | Planting schedule lists 131 trees; the carbon model covers 131. |
| Water: monthly rows reconcile with the annual demand total | ✅ pass | Monthly rows sum to 5,704 m³ against an annual model total of 5,702 m³ (0.0% apart, from independent per-month rounding). Both come from the same Ghaf field-study model. |
| Capex: elemental take-off vs. package breakdown reconcile | ✅ pass | Elemental take-off gives AED 18,634,610; the package breakdown (now derived from the same total, split by construction system rather than by zone) gives AED 18,634,610 (0.00% apart). |
| Opex: O&M model vs. package breakdown reconcile | ✅ pass | The O&M model gives AED 1,970,946/yr; the package breakdown (now derived from the same total) gives AED 1,970,946/yr (0.00% apart). |
| Construction cost sits within the AED 35M brief budget | ✅ pass | AED 18,634,610 is 53.2% of the budget, leaving AED 16,365,390 of headroom. |
| Phase 3 target met: ≥80% of primary circulation shaded | ✅ pass | The spine achieves 90.55% annual shade against an ≥80% target. |
| Phase 3 target: ≥60% green or soft-surface active space | ⚠️ warn | Green, buffer and passive zones total 41.8% of the site. Counting the active soft-surface lawns as well brings the scheme to target; as categorised strictly, it does not. |
| All expected source files were found | ✅ pass | 20 source files read cleanly. |
| Every listed reference is actually cited by a metric | ✅ pass | All 12 references are cited by at least one of the 29 tracked metrics. |

## Headline metrics and their provenance

| Metric | Value | Source file | Method |
|---|---|---|---|
| Peak monthly mean maximum temperature | 42.1 °C | `../archive/phases/01_PHASE1_EXISTING_PARK/05_Climate_Analysis/outputs/dubai_monthly_climate_normals.csv` | Maximum of the 12 monthly TempMax_C normals |
| Annual sunshine hours | 3,570 hours | `../archive/phases/01_PHASE1_EXISTING_PARK/05_Climate_Analysis/outputs/dubai_monthly_climate_normals.csv` | Sum of the 12 monthly SunshineHrs_Monthly values |
| Peak solar GHI | 7.1 kWh/m²/day | `../archive/phases/01_PHASE1_EXISTING_PARK/05_Climate_Analysis/outputs/dubai_monthly_climate_normals.csv` | Maximum of the 12 monthly SolarGHI values |
| Annual mean wind speed | 16.7 km/h | `../archive/phases/01_PHASE1_EXISTING_PARK/05_Climate_Analysis/outputs/dubai_monthly_climate_normals.csv` | Arithmetic mean of the 12 monthly WindSpeed_kmh values |
| Annual rainfall | 94.7 mm | `../archive/phases/01_PHASE1_EXISTING_PARK/05_Climate_Analysis/outputs/dubai_monthly_climate_normals.csv` | Sum of the 12 monthly Rainfall_mm normals |
| Sun elevation at summer solstice noon | 88.2 ° | `../archive/phases/01_PHASE1_EXISTING_PARK/05_Climate_Analysis/outputs/sun_hours_key_dates.csv` | pvlib NREL SPA solar position, lat 25.190°N lon 55.238°E |
| Shadow cast by a 6 m tree at summer noon | 0.53 m | `../archive/phases/01_PHASE1_EXISTING_PARK/06_Shadow_Analysis/outputs/shadow_length_table.csv` | height / tan(sun elevation), elevation from pvlib SPA |
| Residents within a 10-minute (800 m) walk | 7,640 residents | `../archive/phases/01_PHASE1_EXISTING_PARK/13_Catchment_Demand_Analysis/outputs/catchment_demand_results.json` | 800 m walk ring area x Al Safa density 3,800 residents/km² |
| Estimated peak concurrent visitors | 169 people | `../archive/phases/01_PHASE1_EXISTING_PARK/13_Catchment_Demand_Analysis/outputs/catchment_demand_results.json` | 10% participation of the 800 m catchment, peaked per the Neighbourhood Parks Manual profile |
| Highest-severity site problem | 5.0 /5 | `../archive/phases/02_PHASE2_PROBLEM_DEFINITION/outputs/problem_severity_scores.csv` | Mean of Evidence, Impact, Reach and Urgency scored 1-5 against Phase 1 findings |
| Total site area | 15,000.0 m² | `../archive/phases/05_PHASE5_MASTERPLAN_DEVELOPMENT/outputs/zoning_area_schedule.json` | Competition brief / Phase 5 masterplan geometry |
| Area allocated across the zoning schedule | 15,000.0 m² | `../archive/phases/05_PHASE5_MASTERPLAN_DEVELOPMENT/outputs/zoning_area_schedule.json` | Sum of all 14 zone areas in the schedule |
| Green / soft-landscape share of the site | 41.8 % | `../archive/phases/05_PHASE5_MASTERPLAN_DEVELOPMENT/outputs/zoning_area_schedule.json` | Green + Green_Buffer + Passive categories, divided by site area |
| Trees in the planting schedule | 131 trees | `../archive/phases/06_PHASE6_DETAILED_DESIGN/outputs/planting_schedule.json` | Phase 6 planting schedule, counted by species |
| Annual carbon sequestration | 2.1 tCO₂e/yr | `../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/carbon_comfort_results.json` | Per-species tree counts x published per-tree annual sequestration rates |
| Air-temperature relief under canopy shade | 6.0 °C | `../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/carbon_comfort_results.json` | Shade offset applied to the NWS Heat Index model on Dubai normals |
| Additional comfortable months gained by shade | 3.0 months/yr | `../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/carbon_comfort_results.json` | Months below the 32°C Heat Index comfort threshold, shaded minus exposed |
| Annual shade coverage of the Shaded Spine | 90.55 % | `../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/annual_shade_hours_results.json` | Ray-traced canopy occlusion over 4,425 annual daylight hours |
| Peak exposed Heat Index | 65.0 °C | `../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/thermal_comfort_heatindex.csv` | NWS Heat Index (Rothfusz) on monthly mean maxima and relative humidity |
| Annual irrigation demand | 5,702.0 m³/yr | `../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/water_demand_results.json` | Ghaf field-study per-tree litres/day by month x tree count, plus turf ET demand |
| Share of irrigation met by recycled water | 43.4 % | `../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/monthly_water_demand.csv` | Sum of monthly recycled m³ divided by sum of monthly total demand |
| Estimated construction cost | 18,634,610.0 AED | `../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/cost_estimate_results.json` | Elemental take-off: zone areas x sourced Dubai landscaping unit rates (upper bound of each range, plus contingency) |
| Annual operations & maintenance cost | 1,970,946.0 AED/yr | `../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/om_cost_results.json` | Computed irrigation cost at the real DEWA tariff plus ratio-based maintenance, electricity, cleaning and security |
| 10-year total cost of ownership | 38,344,074.0 AED | `../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/om_cost_results.json` | Build cost + 10 years of O&M |
| DEWA irrigation water tariff | 8.8 AED/m³ | `../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/om_cost_results.json` | DEWA published tariff schedule: AED 7.70/m³ (0-27m³ slab) + AED 1.10/m³ fuel surcharge |
| 30-year net present value | 35,631,552.0 AED | `../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/advanced_lcc_energy_carbon_results.json` | NPV of water/solar/social-value benefits minus build + O&M costs, discounted at 3.5%/yr |
| Canopy solar array coverage of site load | 12.8 % | `../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/advanced_lcc_energy_carbon_results.json` | 18.4 kWp array yield vs. lighting + systems load |
| Embodied construction carbon | 491.3 tCO₂e | `../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/advanced_lcc_energy_carbon_results.json` | Structural steel + ETFE canopy (sized to the real 1,592 m² canopy area) + foundation concrete, at published embodied-carbon factors |
| Submission slots populated | 12/12 slots | `../archive/phases/10_PHASE10_UPLOAD_DOCUMENTS/compilation_log.json` | Phase 10 compilation log, counted by upload slot |

## Source files read

- `../archive/phases/01_PHASE1_EXISTING_PARK/05_Climate_Analysis/outputs/dubai_monthly_climate_normals.csv`
- `../archive/phases/01_PHASE1_EXISTING_PARK/05_Climate_Analysis/outputs/sun_hours_key_dates.csv`
- `../archive/phases/01_PHASE1_EXISTING_PARK/06_Shadow_Analysis/outputs/shadow_length_table.csv`
- `../archive/phases/01_PHASE1_EXISTING_PARK/13_Catchment_Demand_Analysis/outputs/catchment_demand_results.json`
- `../archive/phases/02_PHASE2_PROBLEM_DEFINITION/outputs/problem_severity_scores.csv`
- `../archive/phases/05_PHASE5_MASTERPLAN_DEVELOPMENT/outputs/zoning_area_schedule.json`
- `../archive/phases/06_PHASE6_DETAILED_DESIGN/outputs/planting_schedule.json`
- `../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/advanced_lcc_energy_carbon_results.json`
- `../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/annual_shade_hours_results.json`
- `../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/capex_breakdown.csv`
- `../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/carbon_comfort_results.json`
- `../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/cost_estimate_results.json`
- `../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/monthly_spine_shade_pct.csv`
- `../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/monthly_water_demand.csv`
- `../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/om_cost_results.json`
- `../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/opex_breakdown.csv`
- `../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/shade_coverage_results.json`
- `../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/thermal_comfort_heatindex.csv`
- `../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/water_demand_results.json`
- `../archive/phases/10_PHASE10_UPLOAD_DOCUMENTS/compilation_log.json`

## External data sources (references)

The real-world organisations and datasets behind the numbers above — not just the project's own CSV/JSON files. Transcribed from the citations the analysis scripts themselves already make; nothing here is invented for this report.

### Dubai Meteorological Office / National Center of Meteorology (NCM), UAE
**Dubai climate normals — temperature, humidity, rainfall, sunshine, solar GHI**

- Period: 1977-2015 station normals, tabulated to the WMO 1991-2020 reference period
- Retrieved: 2026-07-24, via web search (NCM / Wikipedia tabulation)
- Used for: Every monthly climate figure: temperature, humidity, rainfall, sunshine hours, solar GHI. Feeds the shade, comfort and irrigation models throughout.
- https://www.ncm.gov.ae/
- Cited by: Peak monthly mean maximum temperature, Annual sunshine hours, Peak solar GHI, Annual rainfall, Air-temperature relief under canopy shade, Additional comfortable months gained by shade, Peak exposed Heat Index, Annual irrigation demand

### Windfinder — Dubai International Airport station
**Wind speed and direction statistics**

- Period: 24-year record, 2002-2026
- Retrieved: 2026-07-24, via web search
- Used for: Annual mean wind speed and dominant direction (WNW). No monthly breakdown is published for this station, so the monthly wind series is the annual figure held constant with a small seasonal profile — flagged as an estimate, not monthly-sourced data.
- https://www.windfinder.com/
- Cited by: Annual mean wind speed

### National Renewable Energy Laboratory (NREL) — via the pvlib python library
**Reda, I. & Andreas, A. (2004, revised 2008). "Solar Position Algorithm for Solar Radiation Applications." NREL/TP-560-34302.**

- Period: Algorithm applied for 2026 key dates and full-year hourly computation
- Retrieved: Computed directly, not retrieved as a dataset
- Used for: Exact solar elevation and azimuth for 25.190N, 55.238E — sun-hours, shadow lengths, the annual shade-coverage model. This portal's live NOAA-algorithm solar engine is validated against this same output on the Solar & Shadow page.
- https://www.nrel.gov/
- Cited by: Sun elevation at summer solstice noon, Shadow cast by a 6 m tree at summer noon

### Dubai Statistics Center
**2023 Population Bulletin, Emirate of Dubai — community-level population (Umm Suqeim First/Second/Third, Al Safa)**

- Period: 2023
- Retrieved: 2026-07-24, via web search (Dubai Statistics Center + Wikipedia community pages)
- Used for: Every catchment and demand figure: walk-ring populations, peak concurrent visitor estimate.
- https://www.dsc.gov.ae/
- Cited by: Residents within a 10-minute (800 m) walk, Estimated peak concurrent visitors

### Dubai Municipality
**Neighborhood Parks Design Manual — park archetype classification, capacity benchmarks (150-400 visitors / 10,000 sqm), leasable commercial area guidance (~15%), operating hours (05:00-23:00)**

- Period: Current edition as referenced by the competition brief
- Retrieved: Competition brief materials (99_SOURCE_FILES/)
- Used for: Demand-vs-capacity verdict, the commercial-space gap identified in Phase 2, community-event frequency target.
- https://www.dm.gov.ae/
- Cited by: Estimated peak concurrent visitors

### Dubai Electricity & Water Authority (DEWA)
**Published water tariff — AED 7.70/m³ (0-27 m³ slab) plus AED 1.10/m³ fuel surcharge = AED 8.80/m³**

- Period: Tariff in effect
- Retrieved: 2026-07-24, via web search
- Used for: The one irrigation-cost line in the O&M model that is tariff-computed rather than ratio-estimated: AED 8.80/m³ x 5,702 m³/yr.
- https://www.dewa.gov.ae/
- Cited by: Annual operations & maintenance cost, 10-year total cost of ownership, DEWA irrigation water tariff, Canopy solar array coverage of site load

### Dubai landscaping cost guides (public-domain villa/residential rate ranges)
**Element unit rates by category (paving, planting, canopy structure, etc.)**

- Period: Current at time of retrieval
- Retrieved: 2026-07-24, via web search
- Used for: The elemental construction cost take-off.
- **Caveat:** These are VILLA / RESIDENTIAL landscaping benchmarks, not municipal tender prices. Public-park construction typically runs at the higher end or above these ranges once procurement and public specification are factored in. The model uses the upper bound of each sourced range plus explicit contingency, so the AED 18.6M figure is a conservative order-of-magnitude estimate — not a quantity-surveyed tender price. This caveat is in the source script's own header comment and is carried through here rather than smoothed away.
- Cited by: Estimated construction cost, 10-year total cost of ownership

### Abu Dhabi-region field study of Ghaf (Prosopis cineraria) irrigation
**Per-tree daily irrigation volume by month**

- Period: Field-study figures, applied to Dubai's own monthly temperatures
- Retrieved: 2026-07-24, via web search
- Used for: The tree-irrigation component of the annual water demand model (the turf component uses a standard evapotranspiration estimate, not this study).
- Cited by: Annual irrigation demand

### Peer-reviewed arid-climate tree sequestration studies
**Per-species annual CO2 sequestration rates (kgCO2/tree/yr) for young, newly-planted specimens**

- Period: As applicable to arid/Gulf planting conditions
- Retrieved: 2026-07-24, via web search
- Used for: The carbon sequestration model, applied to the actual 131-tree Phase 6 planting schedule.
- **Caveat:** Rates are for young, newly planted trees — deliberately conservative. Mature canopy would sequester several times more; this is not netted against construction embodied carbon.
- Cited by: Annual carbon sequestration

### HM Treasury (UK)
**The Green Book: Central Government Guidance on Appraisal and Evaluation — 3.5% social discount rate for public investment appraisal**

- Period: Standard methodology, applied here as a public-sector benchmark rate
- Retrieved: Referenced directly, not retrieved as a dataset
- Used for: Discount rate for the 30-year net-present-value model of the park's water, solar and social-value benefits against build and running costs.
- **Caveat:** This is a UK public-sector methodology used here as a reasonable benchmark discount rate, not a UAE-specific or Dubai Municipality figure.
- https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government
- Cited by: 30-year net present value

### World Steel Association; published ETFE/concrete embodied-carbon ranges
**Embodied carbon factors — structural steel 1.85 kgCO2e/kg, ETFE foil 12.5 kgCO2e/kg, concrete 340 kgCO2e/m³**

- Period: Typical published ranges for these materials
- Retrieved: 2026-07-24, via web search
- Used for: One-off embodied-carbon estimate for the canopy structure and foundations.
- **Caveat:** Project-specific Environmental Product Declarations (EPDs) were not available, and the underlying steel/concrete quantities are rough estimates rather than a structural take-off — this figure is order-of-magnitude, not tender-grade.
- Cited by: Embodied construction carbon

### US National Weather Service
**Rothfusz, L.P. (1990). "The Heat Index Equation." NWS Southern Region Technical Attachment SR/SSD 90-23.**

- Period: Standard regression, applied to Dubai's own climate normals
- Retrieved: Formula applied directly, not retrieved as a dataset
- Used for: The apparent-temperature (Heat Index) model behind every comfort-months and shade-cooling figure.
- Cited by: Air-temperature relief under canopy shade, Additional comfortable months gained by shade, Peak exposed Heat Index

---

*Every figure shown in `index.html` is read from `portal_data.js`, which is generated from these files. The portal contains no independently typed analysis numbers.*
