# Data sources

*Al Safa 2 Park — Dubai Municipality AI Park Design Challenge*

Every number quoted anywhere in this submission traces back to something on this
page. For each dataset: who published it, what period it covers, **how many
years of record stand behind it**, how it was obtained, and — the section usually
left out — **what is wrong with it**.

The machine-readable version is [`data/raw/sources.json`](data/raw/sources.json).
The column-by-column provenance of the derived datasets is
[`data/processed/schema.json`](data/processed/schema.json).

---

## The classification used throughout

| Label | Meaning |
|---|---|
| **MEASURED** | Observed by an instrument and published by the source organisation |
| **COMPUTED** | Deterministic physics or astronomy — no estimation involved |
| **MODELLED** | Reconstructed by a documented model — carries model error |
| **DERIVED** | An exact function of other columns |
| **DESIGN** | This project's own geometry and decisions |

This labelling is applied at the point of use, not only here. A chart built on a
modelled series says so in its source line.

---

## 1 · Dubai climate normals — the backbone

| | |
|---|---|
| **Publisher** | National Center of Meteorology (NCM), UAE / Dubai Meteorological Office |
| **Station** | Dubai International Airport (OMDB) |
| **Period** | 1977–2015 station normals, tabulated to the WMO 1991–2020 reference period |
| **Years of record** | **39 years** |
| **Resolution** | Monthly normals — 12 rows |
| **Type** | MEASURED |
| **Retrieved** | 2026-07-24 |
| **File** | [`data/raw/dubai_climate_normals_ncm.csv`](data/raw/dubai_climate_normals_ncm.csv) |
| **Variables** | Air temperature (mean daily max / min / mean), relative humidity, wind speed, rainfall, sunshine hours, global horizontal irradiance |

**Used for:** every downstream model — thermal comfort, shade benefit, irrigation
demand, solar yield.

**Limitation — read this one.** These are *monthly normals*, not an hourly time
series. Machine learning on 12 rows is not machine learning. An 8,760-hour series
is therefore **reconstructed** from them (§7 below). Buying an AMY or TMY hourly
file from NCM would remove that step entirely and is the first recommendation for
any funded continuation of this work.

A second subtlety that silently corrupts comfort figures if missed:
`TempMax_C` is the **mean daily maximum** for the month, *not* the hottest
reading in it. The verification in
[`src/climate.py`](src/climate.py) compares the modelled mean of daily maxima
against it. Comparing the single hottest modelled hour would be comparing two
different quantities.

---

## 2 · Solar position — 8,760 hourly steps

| | |
|---|---|
| **Publisher** | National Renewable Energy Laboratory (NREL), via `pvlib-python` |
| **Citation** | Reda, I. & Andreas, A. (2004, rev. 2008). *Solar Position Algorithm for Solar Radiation Applications.* NREL/TP-560-34302 |
| **Period** | Full calendar year, hourly |
| **Resolution** | 8,760 rows |
| **Type** | **COMPUTED** — accuracy ±0.0003° |
| **Retrieved** | Computed directly for 25.190°N, 55.238°E — not downloaded |

**Used for:** sun elevation and azimuth every hour, shadow lengths, canopy
occlusion, the annual shade model, and the solar features in the ML feature set.

**Limitation:** none material. This is exact astronomy, not an estimate. It
describes where the sun *is*, not how cloudy it is — cloud comes from the NCM
sunshine-hours normals.

---

## 3 · Community population

| | |
|---|---|
| **Publisher** | Dubai Statistics Center — 2023 Population Bulletin |
| **Period** | 2023 · **1 year** (annual snapshot) |
| **Type** | OFFICIAL STATISTIC |
| **File** | [`data/raw/dubai_population_dsc_2023.csv`](data/raw/dubai_population_dsc_2023.csv) |

**Used for:** catchment population, visitor demand, capacity check.

**Limitations:** community-level totals only. Walk-ring populations apply the Al
Safa area density to each ring, so they assume even distribution within the ring
— reasonable for this uniformly built neighbourhood, not exact. The bulletin
gives Al Safa a population but no community code; nothing computes from that
column.

---

## 4 · Walk-time catchment rings

| | |
|---|---|
| **Publisher** | Derived — this project, on the 2023 population base |
| **Type** | DERIVED |
| **File** | [`data/raw/walk_catchment_rings.csv`](data/raw/walk_catchment_rings.csv) |

**Limitation:** these are **circular** rings, not street-network isochrones. Real
walking distance exceeds the radius, so the 800 m ring slightly **over-estimates**
who can genuinely reach the park in 10 minutes. Stated rather than smoothed over.

---

## 5 · Species water and carbon rates

| | |
|---|---|
| **Publisher** | Published arid-region urban forestry literature; Ghaf figures from UAE field studies |
| **Period** | Rates published 2015–2023 |
| **Type** | LITERATURE VALUES |
| **File** | [`data/raw/species_water_carbon_rates.csv`](data/raw/species_water_carbon_rates.csv) |

**Limitation:** per-tree rates vary with age, soil and microclimate. These are
mid-range published figures for semi-mature specimens. The carbon model applies a
linear establishment curve over the first 10 years rather than crediting mature
rates from year one.

---

## 6 · Construction unit rates and utility tariffs

| | |
|---|---|
| **Publisher** | Dubai landscape contractor quotations; DEWA published tariff schedule |
| **Period** | 2025 |
| **Type** | MARKET RATES / PUBLISHED TARIFF |
| **File** | [`data/raw/construction_unit_rates_aed.csv`](data/raw/construction_unit_rates_aed.csv) |

**Limitation:** rates are the **upper bound** of quoted ranges — deliberately
conservative. A real tender would price differently depending on market
conditions.

---

## 7 · The reconstructed hourly series — what it is and is not

This is the dataset the machine learning models train on, and the one that needs
the clearest health warning.

**What it is:** 8,760 hourly rows reconstructed from the 12 monthly normals in §1
using the diurnal model of Parton & Logan (1981) — a sine rise from sunrise to a
peak lagged ~2 h after solar noon, then exponential decay overnight — anchored to
the *real* sunrise and sunset times from the NREL solar model in §2.

**How it is verified:** the modelled series is compared back against the published
normals it was built from. Worst monthly-mean error **0.39 °C**; worst mean daily
maximum error **0.54 °C**. The check is an assertion in
[`tests/test_pipeline.py`](tests/test_pipeline.py) and runs on every rebuild — if
it drifts, the build fails.

**What it cannot do:** reproduce real day-to-day weather variance. A heat wave, a
shamal, a cloudy fortnight — none of these exist in it. **Every conclusion in
this project is therefore about a *typical* year, and none is about extremes.**

---

## Integrity rules this project holds itself to

1. Every figure in every report traces to a file in `data/raw/` or to a documented
   computation over one.
2. Any series that is **modelled** rather than measured is labelled as such at the
   point of use — not only on this page.
3. Where a source has a known weakness it is stated here **and** repeated wherever
   it materially affects a conclusion.
4. No dataset is generated to make a result look better. Where the data is weak,
   the conclusion is stated as weak.
5. Nothing is quoted that the code cannot reproduce. `python run_analysis.py`
   regenerates every number in the submission from these files.

---

## Known open items

| Item | Status |
|---|---|
| **Site boundary** | The 150 × 100 m rectangle is an **assumption** pending confirmation against `00_BRIEF/Al Safa Park 2 Plan (5).dwg`. Every area figure depends on it. |
| Hourly climate | Modelled, not measured — see §7. Resolved by purchasing an NCM AMY/TMY file. |
| Shade relief (6 °C) | A literature value for hot-arid canopy shade, not a site measurement. |
| Diffuse radiation | Excluded from the shade model, so shaded comfort is stated **conservatively**. |
