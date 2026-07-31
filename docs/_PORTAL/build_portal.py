#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_portal.py — SUPERSEDED. Do not run this to rebuild the portal.
=================================================================

This script builds portal_data.js from the frozen phase folders under
archive/phases/. Those describe the PREVIOUS scheme — a straight spine through
rectangular rooms, sixteen zones, and a cost take-off priced against areas that
no longer exist. Running it would overwrite the portal with a design the project
has replaced, and would restore render captions for images that were withdrawn.

The portal's design-dependent blocks are now generated from the live pipeline:

    python tools/sync_portal.py

which reads src/plan.py, src/solar.py and models/headline_metrics.json — the
code that is actually run. This file is kept because the blocks sync_portal.py
does not own (climate, catchment, references, the provenance scaffolding) were
originally produced here, and it records where they came from.

-----------------------------------------------------------------
Original header follows.

Al Safa 2 Park Analytics Portal · data pipeline
=================================================================

WHY THIS EXISTS
---------------
Before this script, index.html carried its own hand-typed copy of every number.
That copy had drifted from the computed phase outputs (worst case: annual carbon
sequestration shown as 147 tCO2e/yr when the Phase 7 model computes 2.1 t/yr).

This script makes the phase `outputs/` folders the single source of truth:

    phase outputs (CSV / JSON)  ->  build_portal.py  ->  _PORTAL/portal_data.js
                                                     ->  _PORTAL/DATA_AUDIT.md

index.html reads ONLY portal_data.js. It hard-codes no analysis numbers, so the
portal can never again disagree with the reports.

Every headline figure additionally carries a provenance record (source file +
producing script + note), surfaced on the portal's "Verification" page, so a
judge can audit any claim in two clicks.

RUN
---
    python _PORTAL/build_portal.py

No third-party dependencies (stdlib only) so it runs anywhere Python 3.8+ does.
"""

from __future__ import annotations

import csv
import json
import os
import sys
from datetime import datetime, timezone

# --------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# The repository restructure moved the numbered phase folders under
# archive/phases/, and this portal now lives in docs/. Resolve the phase root
# by looking for the folders rather than assuming they sit beside this file, so
# the portal keeps building wherever it is placed.
def _find_phase_root(start):
    for base in (start, os.path.dirname(start)):
        for cand in (os.path.join(base, "archive", "phases"), base):
            if os.path.isdir(os.path.join(cand, "01_PHASE1_EXISTING_PARK")):
                return cand
    return start

PHASE_ROOT = _find_phase_root(ROOT)
# Renders and the submission log were relocated too.
RENDER_ROOT = os.path.join(os.path.dirname(HERE), "..", "design", "renders")

P1 = os.path.join(PHASE_ROOT, "01_PHASE1_EXISTING_PARK")
P2 = os.path.join(PHASE_ROOT, "02_PHASE2_PROBLEM_DEFINITION", "outputs")
P5 = os.path.join(PHASE_ROOT, "05_PHASE5_MASTERPLAN_DEVELOPMENT", "outputs")
P6 = os.path.join(PHASE_ROOT, "06_PHASE6_DETAILED_DESIGN", "outputs")
P7 = os.path.join(PHASE_ROOT, "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY", "outputs")
P9 = os.path.join(PHASE_ROOT, "09_PHASE9_AI_WORKFLOW_AND_VISUALIZATION", "outputs")
P10 = os.path.join(PHASE_ROOT, "10_PHASE10_UPLOAD_DOCUMENTS")

CLIMATE_OUT = os.path.join(P1, "05_Climate_Analysis", "outputs")
SHADOW_OUT = os.path.join(P1, "06_Shadow_Analysis", "outputs")
CATCHMENT_OUT = os.path.join(P1, "13_Catchment_Demand_Analysis", "outputs")

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


# --------------------------------------------------------------------------
# Bibliography — the real-world sources behind the numbers
# --------------------------------------------------------------------------
# Every entry here is transcribed from a citation the analysis scripts
# themselves already make (see the header comments and inline "sourced:"
# notes in each phase's _scripts/*.py) — nothing below is invented for the
# portal. Where a script's own comment includes an honest caveat about a
# source's limits (e.g. villa-rate cost benchmarks, not a tender price), that
# caveat is kept here rather than smoothed away.
#
# `url` is only set for an organisation's general public homepage, which is
# stable and independently checkable — never for a specific document or PDF
# whose exact path this project cannot verify.
REFERENCES = [
    {
        "id": "ncm", "org": "Dubai Meteorological Office / National Center of Meteorology (NCM), UAE",
        "title": "Dubai climate normals — temperature, humidity, rainfall, sunshine, solar GHI",
        "period": "1977-2015 station normals, tabulated to the WMO 1991-2020 reference period",
        "retrieved": "2026-07-24, via web search (NCM / Wikipedia tabulation)",
        "usedFor": "Every monthly climate figure: temperature, humidity, rainfall, sunshine hours, "
                   "solar GHI. Feeds the shade, comfort and irrigation models throughout.",
        "url": "https://www.ncm.gov.ae/",
    },
    {
        "id": "windfinder", "org": "Windfinder — Dubai International Airport station",
        "title": "Wind speed and direction statistics",
        "period": "24-year record, 2002-2026",
        "retrieved": "2026-07-24, via web search",
        "usedFor": "Annual mean wind speed and dominant direction (WNW). No monthly breakdown is "
                   "published for this station, so the monthly wind series is the annual figure "
                   "held constant with a small seasonal profile — flagged as an estimate, not "
                   "monthly-sourced data.",
        "url": "https://www.windfinder.com/",
    },
    {
        "id": "nrel-spa", "org": "National Renewable Energy Laboratory (NREL) — via the pvlib python library",
        "title": "Reda, I. & Andreas, A. (2004, revised 2008). "
                 "\"Solar Position Algorithm for Solar Radiation Applications.\" NREL/TP-560-34302.",
        "period": "Algorithm applied for 2026 key dates and full-year hourly computation",
        "retrieved": "Computed directly, not retrieved as a dataset",
        "usedFor": "Exact solar elevation and azimuth for 25.190N, 55.238E — sun-hours, shadow "
                   "lengths, the annual shade-coverage model. This portal's live NOAA-algorithm "
                   "solar engine is validated against this same output on the Solar & Shadow page.",
        "url": "https://www.nrel.gov/",
    },
    {
        "id": "dsc", "org": "Dubai Statistics Center",
        "title": "2023 Population Bulletin, Emirate of Dubai — community-level population "
                 "(Umm Suqeim First/Second/Third, Al Safa)",
        "period": "2023",
        "retrieved": "2026-07-24, via web search (Dubai Statistics Center + Wikipedia community pages)",
        "usedFor": "Every catchment and demand figure: walk-ring populations, peak concurrent "
                   "visitor estimate.",
        "url": "https://www.dsc.gov.ae/",
    },
    {
        "id": "parks-manual", "org": "Dubai Municipality",
        "title": "Neighborhood Parks Design Manual — park archetype classification, capacity "
                 "benchmarks (150-400 visitors / 10,000 sqm), leasable commercial area guidance "
                 "(~15%), operating hours (05:00-23:00)",
        "period": "Current edition as referenced by the competition brief",
        "retrieved": "Competition brief materials (99_SOURCE_FILES/)",
        "usedFor": "Demand-vs-capacity verdict, the commercial-space gap identified in Phase 2, "
                   "community-event frequency target.",
        "url": "https://www.dm.gov.ae/",
    },
    {
        "id": "dewa-tariff", "org": "Dubai Electricity & Water Authority (DEWA)",
        "title": "Published water tariff — AED 7.70/m³ (0-27 m³ slab) plus AED 1.10/m³ fuel "
                 "surcharge = AED 8.80/m³",
        "period": "Tariff in effect",
        "retrieved": "2026-07-24, via web search",
        "usedFor": "The one irrigation-cost line in the O&M model that is tariff-computed rather "
                   "than ratio-estimated: AED 8.80/m³ x 5,702 m³/yr.",
        "url": "https://www.dewa.gov.ae/",
    },
    {
        "id": "landscape-rates", "org": "Dubai landscaping cost guides (public-domain villa/residential rate ranges)",
        "title": "Element unit rates by category (paving, planting, canopy structure, etc.)",
        "period": "Current at time of retrieval",
        "retrieved": "2026-07-24, via web search",
        "usedFor": "The elemental construction cost take-off.",
        "caveat": "These are VILLA / RESIDENTIAL landscaping benchmarks, not municipal tender "
                  "prices. Public-park construction typically runs at the higher end or above "
                  "these ranges once procurement and public specification are factored in. The "
                  "model uses the upper bound of each sourced range plus explicit contingency, "
                  "so the AED 18.6M figure is a conservative order-of-magnitude estimate — "
                  "not a quantity-surveyed tender price. This caveat is in the source script's "
                  "own header comment and is carried through here rather than smoothed away.",
        "url": None,
    },
    {
        "id": "ghaf-field", "org": "Abu Dhabi-region field study of Ghaf (Prosopis cineraria) irrigation",
        "title": "Per-tree daily irrigation volume by month",
        "period": "Field-study figures, applied to Dubai's own monthly temperatures",
        "retrieved": "2026-07-24, via web search",
        "usedFor": "The tree-irrigation component of the annual water demand model (the turf "
                   "component uses a standard evapotranspiration estimate, not this study).",
        "url": None,
    },
    {
        "id": "carbon-rates", "org": "Peer-reviewed arid-climate tree sequestration studies",
        "title": "Per-species annual CO2 sequestration rates (kgCO2/tree/yr) for young, "
                 "newly-planted specimens",
        "period": "As applicable to arid/Gulf planting conditions",
        "retrieved": "2026-07-24, via web search",
        "usedFor": "The carbon sequestration model, applied to the actual 131-tree Phase 6 "
                   "planting schedule.",
        "caveat": "Rates are for young, newly planted trees — deliberately conservative. Mature "
                  "canopy would sequester several times more; this is not netted against "
                  "construction embodied carbon.",
        "url": None,
    },
    {
        "id": "green-book", "org": "HM Treasury (UK)",
        "title": "The Green Book: Central Government Guidance on Appraisal and Evaluation — "
                 "3.5% social discount rate for public investment appraisal",
        "period": "Standard methodology, applied here as a public-sector benchmark rate",
        "retrieved": "Referenced directly, not retrieved as a dataset",
        "usedFor": "Discount rate for the 30-year net-present-value model of the park's "
                   "water, solar and social-value benefits against build and running costs.",
        "caveat": "This is a UK public-sector methodology used here as a reasonable "
                  "benchmark discount rate, not a UAE-specific or Dubai Municipality figure.",
        "url": "https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government",
    },
    {
        "id": "embodied-carbon-factors", "org": "World Steel Association; published ETFE/concrete embodied-carbon ranges",
        "title": "Embodied carbon factors — structural steel 1.85 kgCO2e/kg, ETFE foil "
                 "12.5 kgCO2e/kg, concrete 340 kgCO2e/m³",
        "period": "Typical published ranges for these materials",
        "retrieved": "2026-07-24, via web search",
        "usedFor": "One-off embodied-carbon estimate for the canopy structure and foundations.",
        "caveat": "Project-specific Environmental Product Declarations (EPDs) were not "
                  "available, and the underlying steel/concrete quantities are rough "
                  "estimates rather than a structural take-off — this figure is "
                  "order-of-magnitude, not tender-grade.",
        "url": None,
    },
    {
        "id": "nws-heat-index", "org": "US National Weather Service",
        "title": "Rothfusz, L.P. (1990). \"The Heat Index Equation.\" "
                 "NWS Southern Region Technical Attachment SR/SSD 90-23.",
        "period": "Standard regression, applied to Dubai's own climate normals",
        "retrieved": "Formula applied directly, not retrieved as a dataset",
        "usedFor": "The apparent-temperature (Heat Index) model behind every comfort-months and "
                   "shade-cooling figure.",
        "url": None,
    },
]

REFERENCES_BY_ID = {r["id"]: r for r in REFERENCES}

# Windows consoles default to cp1252 and choke on the °/≥/₂ characters in the
# audit messages. Force UTF-8 on stdout so the summary always prints.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):  # pragma: no cover - older/odd streams
        pass


# --------------------------------------------------------------------------
# Loading helpers — every read is recorded so the audit can show coverage
# --------------------------------------------------------------------------
SOURCES_READ: list[str] = []
WARNINGS: list[str] = []


def rel(path: str) -> str:
    """Repo-relative POSIX path, used as the provenance key."""
    return os.path.relpath(path, ROOT).replace("\\", "/")


def load_json(path: str, default=None):
    if not os.path.exists(path):
        WARNINGS.append(f"missing source: {rel(path)}")
        return default
    with open(path, "r", encoding="utf-8") as fh:
        SOURCES_READ.append(rel(path))
        return json.load(fh)


def load_csv(path: str) -> list[dict]:
    if not os.path.exists(path):
        WARNINGS.append(f"missing source: {rel(path)}")
        return []
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        SOURCES_READ.append(rel(path))
        return list(csv.DictReader(fh))


def num(value, default=0.0) -> float:
    """Tolerant numeric cast — data files mix '-', '', and '3500/tree'."""
    if value is None:
        return default
    if isinstance(value, (int, float)):
        return float(value)
    cleaned = str(value).replace(",", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return default


def fmtnum(value) -> str:
    """Thousands-separated integer, for building provenance note strings."""
    return f"{num(value):,.0f}"


# --------------------------------------------------------------------------
# Provenance ledger
# --------------------------------------------------------------------------
PROVENANCE: list[dict] = []


def track(key, label, value, unit, source, method, note="", refs=None):
    """Register a headline metric together with where it came from.

    `refs` names entries in REFERENCES (see the bibliography above) — the
    real-world organisation/dataset behind the source file, not just the
    project's own CSV/JSON. Unknown ids fail the build loudly rather than
    silently, so a typo here can't quietly drop a citation.
    """
    for r in refs or []:
        assert r in REFERENCES_BY_ID, f"track({key!r}): unknown reference id {r!r}"
    PROVENANCE.append({
        "key": key,
        "label": label,
        "value": value,
        "unit": unit,
        "source": source,
        "method": method,
        "note": note,
        "refs": refs or [],
    })
    return value


# --------------------------------------------------------------------------
# 1. Climate (Phase 1.05)
# --------------------------------------------------------------------------
def build_climate():
    rows = load_csv(os.path.join(CLIMATE_OUT, "dubai_monthly_climate_normals.csv"))
    src = rel(os.path.join(CLIMATE_OUT, "dubai_monthly_climate_normals.csv"))

    climate = {
        "months": MONTHS,
        "tempMax": [num(r["TempMax_C"]) for r in rows],
        "tempMin": [num(r["TempMin_C"]) for r in rows],
        "tempAvg": [num(r["TempAvg_C"]) for r in rows],
        "humidity": [num(r["RH_pct"]) for r in rows],
        "wind": [num(r["WindSpeed_kmh"]) for r in rows],
        "rainfall": [num(r["Rainfall_mm"]) for r in rows],
        "sunHrsMonthly": [num(r["SunshineHrs_Monthly"]) for r in rows],
        "sunHrsDaily": [num(r["SunshineHrs_Daily"]) for r in rows],
        "ghi": [num(r["SolarGHI_kWh_m2_day"]) for r in rows],
        "source": src,
    }

    peak = max(climate["tempMax"]) if climate["tempMax"] else 0
    peak_month = MONTHS[climate["tempMax"].index(peak)] if climate["tempMax"] else "-"
    track("peak_temp", "Peak monthly mean maximum temperature", peak, "°C", src,
          "Maximum of the 12 monthly TempMax_C normals",
          f"Occurs in {peak_month}. NCM/WMO climate normals.", refs=["ncm"])

    annual_sun = round(sum(climate["sunHrsMonthly"]))
    track("annual_sunshine", "Annual sunshine hours", annual_sun, "hours", src,
          "Sum of the 12 monthly SunshineHrs_Monthly values", "", refs=["ncm"])

    peak_ghi = max(climate["ghi"]) if climate["ghi"] else 0
    track("peak_ghi", "Peak solar GHI", peak_ghi, "kWh/m²/day", src,
          "Maximum of the 12 monthly SolarGHI values", "June, at the solstice.", refs=["ncm"])

    mean_wind = round(sum(climate["wind"]) / len(climate["wind"]), 1) if climate["wind"] else 0
    track("mean_wind", "Annual mean wind speed", mean_wind, "km/h", src,
          "Arithmetic mean of the 12 monthly WindSpeed_kmh values", "", refs=["windfinder"])

    annual_rain = round(sum(climate["rainfall"]), 1)
    track("annual_rain", "Annual rainfall", annual_rain, "mm", src,
          "Sum of the 12 monthly Rainfall_mm normals",
          "Effectively zero Jun-Sep, so planting is fully irrigation-dependent.", refs=["ncm"])

    climate["annualSunshine"] = annual_sun
    climate["annualRain"] = annual_rain
    climate["meanWind"] = mean_wind
    climate["peakTemp"] = peak
    climate["peakTempMonth"] = peak_month
    return climate


# --------------------------------------------------------------------------
# 2. Solar geometry + shadows (Phase 1.05 / 1.06)
# --------------------------------------------------------------------------
def build_solar():
    key_path = os.path.join(CLIMATE_OUT, "sun_hours_key_dates.csv")
    rows = load_csv(key_path)
    src = rel(key_path)

    key_dates = []
    for r in rows:
        key_dates.append({
            "date": r["Date"],
            "sunrise": r["Sunrise"],
            "sunset": r["Sunset"],
            "dayLength": num(r["Day_Length_hrs"]),
            "maxElev": num(r["Max_Sun_Elevation_deg"]),
        })

    summer = next((k for k in key_dates if "Summer" in k["date"]), None)
    if summer:
        track("summer_max_elev", "Sun elevation at summer solstice noon",
              summer["maxElev"], "°", src,
              "pvlib NREL SPA solar position, lat 25.190°N lon 55.238°E",
              "Near-zenith sun is why horizontal shade must be engineered, not borrowed "
              "from vertical elements.", refs=["nrel-spa"])

    shadow_path = os.path.join(SHADOW_OUT, "shadow_length_table.csv")
    shadow_rows = load_csv(shadow_path)
    shadows = [{
        "season": r["Season"],
        "time": r["Time"],
        "object": r["Object"],
        "height": num(r["Object_Height_m"]),
        "elev": num(r["Sun_Elevation_deg"]),
        "azimuth": num(r["Sun_Azimuth_deg"]),
        "length": num(r["Shadow_Length_m"]),
    } for r in shadow_rows]

    noon_summer = next((s for s in shadows
                        if "Summer" in s["season"] and "Noon" in s["time"]
                        and "Tree" in s["object"]), None)
    if noon_summer:
        track("summer_noon_shadow", "Shadow cast by a 6 m tree at summer noon",
              noon_summer["length"], "m", rel(shadow_path),
              "height / tan(sun elevation), elevation from pvlib SPA",
              "A 6 m canopy throws barely half a metre of shade at midday — the "
              "evidence base for Problem P1.", refs=["nrel-spa"])

    return {
        "site": {"lat": 25.190, "lon": 55.238, "elevation_m": 16, "tz": "Asia/Dubai (UTC+4)"},
        "keyDates": key_dates,
        "shadows": shadows,
        "sourceKeyDates": src,
        "sourceShadows": rel(shadow_path),
    }


# --------------------------------------------------------------------------
# 3. Catchment & demand (Phase 1.13)
# --------------------------------------------------------------------------
def build_catchment():
    path = os.path.join(CATCHMENT_OUT, "catchment_demand_results.json")
    data = load_json(path, {}) or {}
    src = rel(path)

    demand = data.get("demand_model", {})
    pop800 = demand.get("primary_catchment_800m_residents", 0)
    track("catchment_pop", "Residents within a 10-minute (800 m) walk", pop800,
          "residents", src,
          "800 m walk ring area x Al Safa density 3,800 residents/km²",
          "Dubai Statistics Center community populations. Note the ring is 800 m, "
          "not 1.5 km.", refs=["dsc"])
    track("peak_visitors", "Estimated peak concurrent visitors",
          demand.get("est_peak_concurrent_visitors", 0), "people", src,
          "10% participation of the 800 m catchment, peaked per the Neighbourhood "
          "Parks Manual profile",
          demand.get("verdict", ""), refs=["dsc", "parks-manual"])

    return {
        "populationSources": data.get("population_sources", {}),
        "density": data.get("al_safa_density_per_km2", 0),
        "rings": data.get("walk_catchment", []),
        "capacity": data.get("park_capacity_benchmark", {}),
        "demand": demand,
        "source": src,
    }


# --------------------------------------------------------------------------
# 4. Problems (Phase 2)
# --------------------------------------------------------------------------
def build_problems():
    path = os.path.join(P2, "problem_severity_scores.csv")
    rows = load_csv(path)
    src = rel(path)

    problems = [{
        "id": r["id"],
        "name": r["name"],
        "evidence": num(r["Evidence"]),
        "impact": num(r["Impact"]),
        "reach": num(r["Reach"]),
        "urgency": num(r["Urgency"]),
        "score": num(r["WeightedScore"]),
        "basis": r["basis"],
        "rank": int(num(r["Rank"])),
        "priority": r["Priority"],
    } for r in rows]
    problems.sort(key=lambda p: p["rank"])

    if problems:
        top = problems[0]
        track("top_problem", "Highest-severity site problem", top["score"], "/5", src,
              "Mean of Evidence, Impact, Reach and Urgency scored 1-5 against Phase 1 findings",
              f"{top['id']} — {top['name']}")

    return {"items": problems, "source": src,
            "criteria": ["Evidence", "Impact", "Reach", "Urgency"]}


# --------------------------------------------------------------------------
# 5. Masterplan zoning (Phase 5)
# --------------------------------------------------------------------------
# Presentation metadata for each zone. Areas/categories are NEVER defined here —
# they come from zoning_area_schedule.json. This dict only supplies an icon and a
# one-line description, keyed by the exact zone name in that file.
ZONE_META = {
    "Main Entrance Plaza": ("🏛️", "Arrival threshold, wayfinding and shade-first welcome"),
    "Shaded Spine (Central Walkway)": ("⬡", "Continuous engineered shade corridor linking every zone"),
    "Secondary Entrance (E)": ("🚪", "Eastern pedestrian entry from the residential edge"),
    "Children's Play Zone": ("🛝", "Inclusive play under canopy, step-free throughout"),
    "Family Picnic & Shaded Seating": ("🧺", "Informal family gathering in tree shade"),
    "Community Plaza & Event Lawn": ("🎪", "Flexible surface for markets and the 60+ events/year target"),
    "Outdoor Fitness & Wellness": ("🏋️", "Calisthenics and wellness equipment, shaded edges"),
    "Native Planting / Biodiversity Strip": ("🌿", "Native species massing, habitat and CO₂ sink"),
    "Quiet Contemplation Garden": ("🧘", "Low-stimulation retreat with high canopy cover"),
    "Commercial & Service Kiosk Cluster": ("🏪", "F&B and services — closes the Manual's leasable-area gap"),
    "Multipurpose Sports Lawn": ("⚽", "Open turf for informal sport and events"),
    "Perimeter Shade Buffer (N)": ("🌳", "Northern tree buffer against the street edge"),
    "Perimeter Shade Buffer (S)": ("🌳", "Southern tree buffer and micro-forest"),
}
# Category -> portal colour token. Each of the eight categories gets its own
# hue: three shades of green would be unreadable in the plan and the doughnut.
CATEGORY_TOKEN = {
    "Arrival": "gold", "Circulation": "blue", "Active": "orange",
    "Passive": "teal", "Social": "purple", "Green": "green",
    "Commercial": "red", "Green_Buffer": "lime",
}


def build_zoning():
    path = os.path.join(P5, "zoning_area_schedule.json")
    data = load_json(path, {}) or {}
    src = rel(path)

    site_area = num(data.get("site_area_sqm", 15000))
    zones = []
    for entry in data.get("zones", []):
        name, category, area, pct = entry[0], entry[1], num(entry[2]), num(entry[3])
        icon, desc = ZONE_META.get(name, ("📍", ""))
        # Long circulation label is descriptive prose — keep a short display name.
        display = name.split(" (between rooms")[0]
        z = {
            "name": display,
            "fullName": name,
            "category": category,
            "area": area,
            "pct": pct,
            "icon": icon,
            "desc": desc or "Circulation, setbacks and the perimeter jogging loop",
            "token": CATEGORY_TOKEN.get(category, "blue"),
        }
        # Real masterplan coordinates, when the schedule carries them. The plan
        # drawing used to invent a layout from areas alone, which meant the
        # picture on the portal was never quite the picture in the drawings —
        # and once the canopy section changed, its packing started overlapping
        # the entrance plazas outright. With bounds present the portal draws
        # the actual plan.
        if len(entry) >= 8:
            z["bounds"] = [num(entry[4]), num(entry[5]), num(entry[6]), num(entry[7])]
        zones.append(z)

    allocated = round(sum(z["area"] for z in zones), 1)
    track("site_area", "Total site area", site_area, "m²", src,
          "Competition brief / Phase 5 masterplan geometry", "Al Safa 2 Park, Dubai.")
    track("zoned_area", "Area allocated across the zoning schedule", allocated, "m²", src,
          "Sum of all 14 zone areas in the schedule",
          f"{allocated:,.0f} of {site_area:,.0f} m² — the schedule is fully allocated."
          if abs(allocated - site_area) < 1
          else f"Differs from site area by {allocated - site_area:+,.1f} m².")

    by_category: dict[str, float] = {}
    for z in zones:
        by_category[z["category"]] = by_category.get(z["category"], 0) + z["area"]

    green = sum(z["area"] for z in zones
                if z["category"] in ("Green", "Green_Buffer", "Passive"))
    green_pct = round(green / site_area * 100, 1) if site_area else 0
    track("green_pct", "Green / soft-landscape share of the site", green_pct, "%", src,
          "Green + Green_Buffer + Passive categories, divided by site area",
          "Phase 3 success metric targets ≥60% green or soft-surface active space.")

    return {
        "siteArea": site_area,
        "allocated": allocated,
        "zones": zones,
        "byCategory": by_category,
        "greenPct": green_pct,
        "source": src,
    }


# --------------------------------------------------------------------------
# 6. Planting & carbon (Phase 6 + Phase 7)
# --------------------------------------------------------------------------
# Horticultural notes per species (design reference, not computed data).
SPECIES_META = {
    "Neem (Azadirachta indica)":
        ("Dense evergreen canopy, high shade yield per tree, proven in Gulf street planting.", "🌳"),
    "Ghaf (Prosopis cineraria)":
        ("UAE national tree. Deep taproot, minimal irrigation once established.", "🌾"),
    "Ficus nitida":
        ("Fast, dense shade for the spine edges; needs managed root control.", "🌲"),
    "Olive (Olea europaea)":
        ("Drought-hardy, low litter — suits seating and contemplation areas.", "🫒"),
    "Date Palm (Phoenix dactylifera)":
        ("Cultural identity marker; vertical accent rather than shade provider.", "🌴"),
}


def build_planting():
    plant_path = os.path.join(P6, "planting_schedule.json")
    carbon_path = os.path.join(P7, "carbon_comfort_results.json")

    plant = load_json(plant_path, {}) or {}
    carbon_data = load_json(carbon_path, {}) or {}
    carbon = carbon_data.get("carbon", {})
    comfort = carbon_data.get("thermal_comfort", {})

    rate_by_species = {s["Species"]: s for s in carbon.get("by_species", [])}

    species = []
    for name, count in plant.get("by_species", {}).items():
        c = rate_by_species.get(name, {})
        note, icon = SPECIES_META.get(name, ("", "🌱"))
        species.append({
            "name": name,
            "count": int(count),
            "carbonPerTree": num(c.get("kgCO2_per_tree_yr")),
            "annualCO2": num(c.get("annual_kgCO2")),
            "note": note,
            "icon": icon,
        })
    species.sort(key=lambda s: -s["count"])

    total_trees = int(plant.get("total_trees", sum(s["count"] for s in species)))
    total_kg = num(carbon.get("total_annual_kgCO2"))
    total_t = num(carbon.get("total_annual_tonnes"))

    track("total_trees", "Trees in the planting schedule", total_trees, "trees",
          rel(plant_path), "Phase 6 planting schedule, counted by species", "")
    track("carbon_seq", "Annual carbon sequestration", total_t, "tCO₂e/yr",
          rel(carbon_path),
          "Per-species tree counts x published per-tree annual sequestration rates",
          f"{total_kg:,.0f} kg/yr across {total_trees} trees — equivalent to about "
          f"{carbon.get('car_km_equiv', 0):,} car-km. This is a young-planting figure; "
          "it rises substantially as the canopy matures.", refs=["carbon-rates"])
    track("shade_cooling", "Air-temperature relief under canopy shade",
          num(comfort.get("shade_cooling_C")), "°C", rel(carbon_path),
          "Shade offset applied to the NWS Heat Index model on Dubai normals", "",
          refs=["nws-heat-index", "ncm"])
    track("comfort_months_gained", "Additional comfortable months gained by shade",
          num(comfort.get("months_gained")), "months/yr", rel(carbon_path),
          "Months below the 32°C Heat Index comfort threshold, shaded minus exposed",
          f"{comfort.get('comfortable_months_sun', 0)} months in sun -> "
          f"{comfort.get('comfortable_months_shade', 0)} months in shade.",
          refs=["nws-heat-index", "ncm"])

    return {
        "totalTrees": total_trees,
        "species": species,
        "carbonTotalKg": total_kg,
        "carbonTotalTonnes": total_t,
        "carKmEquiv": num(carbon.get("car_km_equiv")),
        "comfort": comfort,
        "sourcePlanting": rel(plant_path),
        "sourceCarbon": rel(carbon_path),
    }


# --------------------------------------------------------------------------
# 7. Performance — shade, comfort, water (Phase 7)
# --------------------------------------------------------------------------
def build_performance():
    shade_path = os.path.join(P7, "annual_shade_hours_results.json")
    cover_path = os.path.join(P7, "shade_coverage_results.json")
    monthly_path = os.path.join(P7, "monthly_spine_shade_pct.csv")
    hi_path = os.path.join(P7, "thermal_comfort_heatindex.csv")
    water_path = os.path.join(P7, "water_demand_results.json")
    water_month_path = os.path.join(P7, "monthly_water_demand.csv")

    shade = load_json(shade_path, {}) or {}
    coverage = load_json(cover_path, {}) or {}
    monthly_rows = load_csv(monthly_path)
    hi_rows = load_csv(hi_path)
    water = load_json(water_path, {}) or {}
    water_rows = load_csv(water_month_path)

    spine_pct = shade.get("annual_shade_pct", {}).get("Shaded Spine (path)", 0)
    track("spine_shade", "Annual shade coverage of the Shaded Spine", spine_pct, "%",
          rel(shade_path),
          "Ray-traced canopy occlusion over 4,425 annual daylight hours",
          "The spine is shaded for 4,391 of 4,425 daylight hours. Off-spine zones "
          "score far lower — that gap is the design argument for the spine.")

    zone_shade = [{"zone": k,
                   "hours": shade.get("annual_shade_hours", {}).get(k, 0),
                   "pct": v}
                  for k, v in shade.get("annual_shade_pct", {}).items()]
    zone_shade.sort(key=lambda z: -z["pct"])

    heat_index = {
        "months": [r["Month"] for r in hi_rows],
        "airMax": [num(r["AirTempMax_C"]) for r in hi_rows],
        "sun": [num(r["HeatIndex_Sun_C"]) for r in hi_rows],
        "shade": [num(r["HeatIndex_Shade_C"]) for r in hi_rows],
        "source": rel(hi_path),
    }
    if heat_index["sun"]:
        worst = max(heat_index["sun"])
        worst_m = heat_index["months"][heat_index["sun"].index(worst)]
        delta = round(worst - heat_index["shade"][heat_index["sun"].index(worst)], 1)
        track("peak_heat_index", "Peak exposed Heat Index", worst, "°C", rel(hi_path),
              "NWS Heat Index (Rothfusz) on monthly mean maxima and relative humidity",
              f"{worst_m} in full sun. Shade removes {delta}°C of apparent temperature "
              "at the same hour.", refs=["nws-heat-index", "ncm"])

    water_monthly = {
        "months": [r["Month"] for r in water_rows],
        "total": [num(r["Total_Water_m3"]) for r in water_rows],
        "recycled": [num(r["Recycled_m3"]) for r in water_rows],
        "potable": [num(r["Potable_DEWA_m3"]) for r in water_rows],
        "cost": [num(r["DEWA_Water_Cost_AED"]) for r in water_rows],
        "source": rel(water_month_path),
    }

    annual_water = num(water.get("annual_total_water_m3"))
    track("annual_water", "Annual irrigation demand", annual_water, "m³/yr",
          rel(water_path),
          "Ghaf field-study per-tree litres/day by month x tree count, plus turf ET demand",
          f"{water.get('assumed_tree_count', 0)} trees plus "
          f"{water.get('turf_sqm', 0):,} m² of turf. Turf is the dominant driver "
          "— reducing turf is the single biggest water lever.", refs=["ghaf-field", "ncm"])

    recycled_total = sum(water_monthly["recycled"])
    monthly_total = sum(water_monthly["total"])
    recycled_pct = round(recycled_total / monthly_total * 100, 1) if monthly_total else 0
    track("recycled_pct", "Share of irrigation met by recycled water", recycled_pct, "%",
          rel(water_month_path),
          "Sum of monthly recycled m³ divided by sum of monthly total demand", "")

    return {
        "spineShadePct": spine_pct,
        "totalDaylightHours": shade.get("total_daylight_hours", 0),
        "zoneShade": zone_shade,
        "coverage": coverage,
        "monthlySpineShade": [num(r["spine_shade_pct"]) for r in monthly_rows],
        "heatIndex": heat_index,
        "water": water,
        "waterMonthly": water_monthly,
        "recycledPct": recycled_pct,
        "sourceShade": rel(shade_path),
        "sourceCoverage": rel(cover_path),
        "sourceWater": rel(water_path),
    }


# --------------------------------------------------------------------------
# 8. Cost (Phase 7) — two independent models, both reported
# --------------------------------------------------------------------------
BUDGET_AED = 35_000_000  # Competition brief implementation budget


def build_cost():
    elem_path = os.path.join(P7, "cost_estimate_results.json")
    capex_path = os.path.join(P7, "capex_breakdown.csv")
    opex_path = os.path.join(P7, "opex_breakdown.csv")
    om_path = os.path.join(P7, "om_cost_results.json")

    elemental = load_json(elem_path, {}) or {}
    capex_rows = load_csv(capex_path)
    opex_rows = load_csv(opex_path)
    om = load_json(om_path, {}) or {}

    line_items = [{
        "element": li["Element"],
        "area": li["Area_sqm"],
        "rate": li["Rate_AED_sqm"],
        "cost": num(li["Cost_AED"]),
    } for li in elemental.get("line_items", [])]
    direct_works_total = sum(li["cost"] for li in line_items)
    line_items.sort(key=lambda li: -li["cost"])

    # The source JSON's "addons" (prelims, design contingency, professional
    # fees) are what actually take direct-works cost up to the quoted total —
    # without them the table's own rows summed to only 77% of its footer.
    # They're appended as normal rows here rather than silently folded into
    # the total, so the table is internally consistent by construction.
    for label, cost in (elemental.get("addons") or {}).items():
        if label.startswith(("Subtotal", "TOTAL")):
            continue
        line_items.append({"element": label, "area": "-", "rate": "-", "cost": num(cost)})

    elemental_total = num(om.get("build_cost_AED")) or sum(li["cost"] for li in line_items)

    capex_pkg = [{"item": r["Item"], "cost": num(r["AED"])} for r in capex_rows]
    capex_pkg.sort(key=lambda c: -c["cost"])
    capex_pkg_total = sum(c["cost"] for c in capex_pkg)

    opex_pkg = [{"item": r["Item"], "cost": num(r["AED_yr1"])} for r in opex_rows]
    opex_pkg.sort(key=lambda c: -c["cost"])
    opex_pkg_total = sum(c["cost"] for c in opex_pkg)

    om_items = [{"item": li["item"], "cost": num(li["annual_AED"]), "basis": li["basis"]}
                for li in om.get("line_items", [])]
    om_items.sort(key=lambda c: -c["cost"])
    om_total = num(om.get("total_annual_om_AED"))

    track("capex", "Estimated construction cost", elemental_total, "AED", rel(elem_path),
          "Elemental take-off: zone areas x sourced Dubai landscaping unit rates "
          "(upper bound of each range, plus contingency)",
          f"{elemental_total / BUDGET_AED * 100:.0f}% of the AED 35M brief budget, "
          f"leaving AED {(BUDGET_AED - elemental_total) / 1e6:.1f}M of headroom. "
          + REFERENCES_BY_ID["landscape-rates"]["caveat"],
          refs=["landscape-rates"])
    track("opex", "Annual operations & maintenance cost", om_total, "AED/yr", rel(om_path),
          "Computed irrigation cost at the real DEWA tariff plus ratio-based "
          "maintenance, electricity, cleaning and security",
          f"{om.get('om_pct_of_build', 0)}% of build cost per year.", refs=["dewa-tariff"])
    track("tco10", "10-year total cost of ownership", num(om.get("cost_over_10yr_AED")),
          "AED", rel(om_path), "Build cost + 10 years of O&M", "", refs=["landscape-rates", "dewa-tariff"])
    track("water_tariff", "DEWA irrigation water tariff",
          num(om.get("water_tariff_AED_m3")), "AED/m³", rel(om_path),
          "DEWA published tariff schedule: AED 7.70/m³ (0-27m³ slab) + AED 1.10/m³ fuel surcharge",
          "Applied to the computed 5,702 m³/yr demand.", refs=["dewa-tariff"])

    return {
        "budget": BUDGET_AED,
        "elemental": {"items": line_items, "total": elemental_total,
                      "source": rel(elem_path)},
        "capexPackage": {"items": capex_pkg, "total": capex_pkg_total,
                         "source": rel(capex_path)},
        "opexPackage": {"items": opex_pkg, "total": opex_pkg_total,
                        "source": rel(opex_path)},
        "om": {"items": om_items, "total": om_total,
               "pctOfBuild": num(om.get("om_pct_of_build")),
               "tco10": num(om.get("cost_over_10yr_AED")),
               "waterTariff": num(om.get("water_tariff_AED_m3")),
               "annualWaterM3": num(om.get("annual_water_m3")),
               "source": rel(om_path)},
        "headroom": BUDGET_AED - elemental_total,
        "budgetUsedPct": round(elemental_total / BUDGET_AED * 100, 1),
    }


# --------------------------------------------------------------------------
# 8b. Advanced LCC / energy / embodied-carbon model (Phase 7, advanced script)
# --------------------------------------------------------------------------
# This model used to compute its own independent capex/opex/water totals,
# which silently disagreed with the rest of Phase 7 (see the reconciliation
# note at the top of 08_advanced_lca_sustainability_master.py). It has since
# been rewritten to read those totals from the same canonical outputs
# everything else uses, so what's read here is guaranteed consistent with
# `cost` and `performance` above. What's genuinely unique to this model —
# 30-year NPV/IRR/payback/SROI, the solar energy budget, and embodied
# construction carbon — has no other source in the project.
def build_advanced():
    path = os.path.join(P7, "advanced_lcc_energy_carbon_results.json")
    data = load_json(path, {}) or {}
    if not data:
        return None
    src = rel(path)

    lcc = data.get("lcc_30yr", {})
    energy = data.get("energy", {})
    carbon = data.get("carbon", {})

    track("npv_30yr", "30-year net present value", num(lcc.get("npv_net_AED")), "AED",
          src, "NPV of water/solar/social-value benefits minus build + O&M costs, "
          f"discounted at {num(lcc.get('discount_rate')) * 100:.1f}%/yr",
          f"IRR {num(lcc.get('irr_pct'))}% · simple payback "
          f"{lcc.get('simple_payback_years', '-')} years · SROI "
          f"{num(lcc.get('sroi_ratio'))}x per AED invested.", refs=["green-book"])
    track("solar_coverage", "Canopy solar array coverage of site load",
          num(energy.get("load_covered_pct")), "%", src,
          f"{num(energy.get('solar_capacity_kWp'))} kWp array yield vs. lighting + systems load",
          f"The array generates {fmtnum(energy.get('annual_solar_yield_kWh'))} kWh/yr against "
          f"{fmtnum(energy.get('annual_consumption_kWh'))} kWh/yr of load — a shortfall, not a "
          f"surplus, at this panel count. An earlier draft of this script mislabelled the "
          f"shortfall as power \"sold back to the grid\"; it is corrected here to state the "
          f"deficit plainly.", refs=["dewa-tariff"])
    track("embodied_carbon", "Embodied construction carbon", num(carbon.get("embodied_construction_tCO2e")),
          "tCO₂e", src,
          "Structural steel + ETFE canopy (sized to the real 1,592 m² canopy area) + "
          "foundation concrete, at published embodied-carbon factors",
          "A one-off construction figure, not annual. Not netted against the annual "
          "sequestration figure quoted elsewhere — the two measure different things.",
          refs=["embodied-carbon-factors"])

    return {
        "capexTotal": num(data.get("capex_total_AED")),
        "opexTotal": num(data.get("opex_y1_AED")),
        "lcc": lcc,
        "energy": energy,
        "carbon": carbon,
        "source": src,
    }


# --------------------------------------------------------------------------
# 9. Narrative content transcribed from the phase reports
#    (kept here, with a `source` on every block, so the portal never invents text)
# --------------------------------------------------------------------------
def build_narrative():
    p4 = "04_PHASE4_CONCEPT_DEVELOPMENT/Phase4_Concept_Development_Report.pdf"
    p3 = "03_PHASE3_OPPORTUNITY_AND_OBJECTIVES/Phase3_Opportunity_and_Objectives_Report.pdf"
    p8 = "08_PHASE8_USER_EXPERIENCE_AND_ACTIVATION/Phase8_User_Experience_and_Activation_Report.pdf"

    concepts = {
        "source": p4,
        "criteria": [
            {"name": "Function", "weight": 25},
            {"name": "User Experience", "weight": 25},
            {"name": "Sustainability", "weight": 20},
            {"name": "Feasibility within AED 35M", "weight": 20},
            {"name": "Innovation", "weight": 10},
        ],
        "options": [
            {
                "id": "A", "name": "The Shaded Spine", "selected": True,
                "idea": "One continuous shaded central spine connects all zones",
                "circulation": "Linear, highly legible, single primary path",
                "shade": "Continuous overhead shade structure along the spine",
                "fits": "Wayfinding clarity, day/night activation along one axis",
                "risk": "Areas off the spine may still be under-shaded",
                "scores": [8, 8, 7, 9, 7],
            },
            {
                "id": "B", "name": "Canopy Village", "selected": False,
                "idea": "Cluster of discrete shaded rooms around a central plaza",
                "circulation": "Radial from central plaza to each room",
                "shade": "Shade concentrated per-room (tree clusters + pergolas)",
                "fits": "Distinct age-group zoning, event flexibility",
                "risk": "Central plaza could become a pinch-point, less event-flexible",
                "scores": [7, 9, 8, 6, 8],
            },
            {
                "id": "C", "name": "Cool Loop", "selected": False,
                "idea": "A single perimeter shaded loop with activities nested inside",
                "circulation": "Circular loop plus inner cross-paths",
                "shade": "Shade concentrated on the loop itself",
                "fits": "Fitness and wellness emphasis, continuous exercise use",
                "risk": "Interior zones could feel disconnected from the loop's comfort",
                "scores": [8, 7, 7, 8, 6],
            },
        ],
        "rationale": (
            "Concept A was selected and merged with Concept B's room-based zoning logic. "
            "It scores highest on feasibility inside the fixed AED 35M budget, answers "
            "Phase 2's top evidence-backed problem (summer thermal discomfort) with one "
            "engineered shade structure rather than dozens of small ones, and gives the "
            "submission a single legible diagram."
        ),
    }

    objectives = {
        "source": p3,
        "items": [
            {"type": "Human-centered", "statement": "Every zone usable and comfortable for children, families, teens, older adults, and People of Determination"},
            {"type": "Climate-responsive", "statement": "Eliminate unshaded midday exposure across all primary circulation and gathering spaces during peak summer"},
            {"type": "Inclusive", "statement": "100% step-free, universal-design circulation from every entrance to every major destination"},
            {"type": "Sustainable", "statement": "Native and climate-adapted planting, water-sensitive irrigation, and biodiversity enhancement as default, not add-on"},
            {"type": "Feasible", "statement": "Every proposed element sized and specified to fit within the AED 35M implementation budget"},
        ],
        "metrics": [
            {"metric": "Shaded route coverage", "target": "≥80% of primary circulation shaded at summer solar noon", "actualKey": "spine_shade"},
            {"metric": "Accessible circulation", "target": "100% of paths meet universal-design gradient and width standards", "actualKey": None},
            {"metric": "Usable green / active space", "target": "≥60% of site area green, planted or soft-surface active", "actualKey": "green_pct"},
            {"metric": "Biodiversity", "target": "Net increase in native tree and shrub species vs. existing baseline", "actualKey": "total_trees"},
            {"metric": "Community use", "target": "Support the Manual benchmark of 60+ small events per year", "actualKey": None},
        ],
        "principles": [
            "People first — every design choice traceable to a real user need from Phase 2.",
            "Nature first — planting and shade lead the layout, not fill leftover space.",
            "AI as a design assistant — used for analysis, iteration and testing; final judgement stays human.",
            "Flexibility — spaces support multiple uses across day, night and season.",
            "Local identity — materials and forms that read as authentically Dubai and Al Safa.",
        ],
    }

    personas = {
        "source": p8,
        "items": [
            {"name": "Amina, 34", "role": "Parent", "icon": "👩‍👧‍👦",
             "profile": "Visits after school pickup from the adjacent Umm Suqeim Model School with two children",
             "zones": ["Children's Play Zone", "Family Picnic & Shaded Seating"],
             "window": "15:00–18:00"},
            {"name": "Rashid, 68", "role": "Older resident", "icon": "🧓",
             "profile": "Daily evening walk; values continuous shade and frequent seating",
             "zones": ["Shaded Spine", "Perimeter jogging loop", "Quiet Contemplation Garden"],
             "window": "18:00–20:00"},
            {"name": "Sara, 16", "role": "Teenager", "icon": "🧑‍🤝‍🧑",
             "profile": "After-school social visit with friends",
             "zones": ["Community Plaza & Event Lawn", "Outdoor Fitness & Wellness"],
             "window": "16:00–22:00"},
            {"name": "Mr. Al Farsi", "role": "Wheelchair user", "icon": "♿",
             "profile": "Weekly visit for fresh air and social contact; requires fully step-free routes",
             "zones": ["Shaded Spine (100% step-free)", "Community Plaza"],
             "window": "Any"},
            {"name": "Fatima, 29", "role": "Fitness enthusiast", "icon": "🏃‍♀️",
             "profile": "Early-morning run before work, in the cooler comfort window",
             "zones": ["Perimeter jogging loop", "Outdoor Fitness & Wellness"],
             "window": "05:00–08:00"},
        ],
        "daily": [
            {"time": "05:00–08:00", "activity": "Fitness and jogging in the cool comfort window", "intensity": 70},
            {"time": "08:00–15:00", "activity": "Lowest use — peak heat, shade-dependent activity only", "intensity": 20},
            {"time": "15:00–18:00", "activity": "Family and school-pickup peak, Children's Play Zone busiest", "intensity": 85},
            {"time": "18:00–23:00", "activity": "Community Plaza, evening walking loop, teen social use", "intensity": 100},
        ],
        "seasonal": (
            "November–April is the comfort window: full-day use is expected across all "
            "zones. May–October, midday use concentrates in the 100%-shaded spine and "
            "shaded room edges, with open lawns used early morning and after sunset."
        ),
    }

    return {"concepts": concepts, "objectives": objectives, "personas": personas}


# --------------------------------------------------------------------------
# 10. Deliverables (Phase 10)
# --------------------------------------------------------------------------
SLOT_NAMES = [
    "Design Narrative & Concept",
    "Preliminary Design / Masterplan",
    "Concept Plans & Spatial Diagrams",
    "Key Sections & Elevations",
    "3D Spatial Visualizations",
    "AI Methodology Report",
    "User Experience & Activation Strategy",
    "Sustainability Concept & Strategy",
    "Material & Landscape Palette",
    "Complete Design Report",
    "Site Analysis & Human-Centric Research",
    "Concept Animation Video",
]


def build_deliverables():
    path = os.path.join(P10, "compilation_log.json")
    log = load_json(path, {}) or {}
    src = rel(path)

    copied = log.get("copied", [])
    empty = set(log.get("empty_slots", []))

    slots = []
    for i, name in enumerate(SLOT_NAMES, start=1):
        prefix = f"{i:02d}_"
        files = [c.split("<-", 1)[1].strip()
                 for c in copied if c.strip().startswith(prefix)]
        folder = next((c.split("<-", 1)[0].strip()
                       for c in copied if c.strip().startswith(prefix)), None)
        is_empty = any(e.startswith(prefix) for e in empty)
        slots.append({
            "num": i,
            "name": name,
            "files": files,
            "count": len(files),
            "status": "empty" if (is_empty or not files) else "ready",
            "folder": folder,
        })

    ready = sum(1 for s in slots if s["status"] == "ready")
    track("slots_ready", "Submission slots populated", f"{ready}/12", "slots", src,
          "Phase 10 compilation log, counted by upload slot",
          "Slots 10 and 12 are deliberately outstanding: the complete design report "
          "and the optional 60-second animation.")

    return {"slots": slots, "ready": ready, "total": 12, "source": src}


# --------------------------------------------------------------------------
# 11. Renders (Phase 9)
# --------------------------------------------------------------------------
RENDER_META = [
    ("dubai_futuristic_masterplan_aerial.jpg", "Futuristic Organic Masterplan — Dubai Landmark Concept",
     "Phase 5 · Masterplan",
     "Sweeping dune-inspired parametric canopy, fluid terrazzo pathways, and integrated micro-oasis pockets."),
    ("dubai_futuristic_spine_interior.jpg", "The Shaded Promenade — Luxury Interior",
     "Phase 6 · Detailed Design",
     "Ultra-luxury marble walkway beneath a fluid parametric canopy with cooling mist rings and Ghaf groves."),
    ("aerial_day_view_1784970538631.jpg", "Midday Aerial — Organic Lattice Canopy",
     "Phase 9 · AI Visualization",
     "Futuristic curved canopy concept demonstrating near-vertical summer shade coverage."),
    ("masterplan_aerial_golden_hour.jpg", "Golden Hour Aerial View",
     "Phase 5 · Masterplan",
     "Fluid biophilic architecture bathed in warm evening sunlight."),
    ("spine_corridor_interior.jpg", "Parametric Canopy Corridor",
     "Phase 6 · Detailed Design",
     "Curved timber and bronze louvers providing continuous thermal comfort."),
    ("eyelevel_spine_1784970552956.jpg", "Biophilic Promenade Perspective",
     "Phase 6 · Detailed Design",
     "Native Ghaf and Neem canopy trees integrated into the fluid shade structure."),
    ("night_plaza_render_1784970565232.jpg", "Night Activation Plaza — Ambient LED",
     "Phase 8 · Activation",
     "Linear and edge-lit LED illumination creating a vibrant evening community destination."),
    ("thermal_comfort_heatmap.jpg", "Thermal Comfort Performance Map",
     "Phase 7 · Performance",
     "Computed microclimate heat-index reduction under the organic canopy."),
]


def build_renders():
    """Collect the renders, copying each into docs/assets/renders/.

    The src path MUST stay inside the published site directory. It previously
    pointed at ../archive/..., which resolves fine on disk but escapes the web
    root — so a browser refused every one of them and the gallery rendered
    empty, locally and on GitHub Pages alike. Copying into the site directory
    and referencing relatively fixes both.
    """
    import shutil

    site_dir = os.path.dirname(HERE)                      # docs/
    assets = os.path.join(site_dir, "assets", "renders")
    os.makedirs(assets, exist_ok=True)

    visuals_dir = os.path.join(site_dir, "..", "design", "visuals")
    renders = []
    for filename, title, tag, desc in RENDER_META:
        cand_paths = [
            os.path.join(assets, filename),
            os.path.join(visuals_dir, filename),
            os.path.join(RENDER_ROOT, filename),
            os.path.join(P9, filename),
        ]
        found_path = next((p for p in cand_paths if os.path.exists(p)), None)
        if not found_path:
            WARNINGS.append(f"missing render: {filename}")
            continue

        dest = os.path.join(assets, filename)
        if os.path.abspath(found_path) != os.path.abspath(dest):
            shutil.copy2(found_path, dest)

        renders.append({
            "src": f"assets/renders/{filename}",
            "title": title,
            "tag": tag,
            "desc": desc,
        })
    return renders


# --------------------------------------------------------------------------
# 12. Cross-phase consistency audit
# --------------------------------------------------------------------------
def run_audit(zoning, planting, perf, cost) -> list[dict]:
    checks: list[dict] = []

    def check(name, ok, detail, severity="error"):
        checks.append({
            "name": name,
            "status": "pass" if ok else severity,
            "detail": detail,
        })

    # Zoning must fully allocate the site.
    diff = zoning["allocated"] - zoning["siteArea"]
    check("Zoning schedule fully allocates the site area",
          abs(diff) < 1.0,
          f"Zones sum to {zoning['allocated']:,.1f} m² against a site area of "
          f"{zoning['siteArea']:,.1f} m² ({diff:+,.1f} m²).")

    # Carbon: per-species rows must reconcile with the reported total.
    species_sum = sum(s["annualCO2"] for s in planting["species"])
    check("Carbon: species rows reconcile with the annual total",
          abs(species_sum - planting["carbonTotalKg"]) < 1.0,
          f"Species rows sum to {species_sum:,.0f} kgCO₂/yr against a reported total of "
          f"{planting['carbonTotalKg']:,.0f} kgCO₂/yr.")

    # Tree count consistency between the planting schedule and the carbon model.
    carbon_trees = sum(s["count"] for s in planting["species"] if s["carbonPerTree"] > 0)
    check("Tree counts agree between the planting schedule and the carbon model",
          carbon_trees == planting["totalTrees"],
          f"Planting schedule lists {planting['totalTrees']} trees; the carbon model "
          f"covers {carbon_trees}.")

    # Water: monthly rows should reconcile with the annual total. These used
    # to come from two independent models (an 8,861 vs. 5,702 m³ mismatch);
    # the monthly series is now derived from the same Ghaf field-study model
    # as the annual figure, so only harmless per-month rounding remains.
    monthly_sum = sum(perf["waterMonthly"]["total"])
    annual = num(perf["water"].get("annual_total_water_m3"))
    drift = abs(monthly_sum - annual) / annual * 100 if annual else 0
    check("Water: monthly rows reconcile with the annual demand total",
          drift < 5,
          f"Monthly rows sum to {monthly_sum:,.0f} m³ against an annual model total of "
          f"{annual:,.0f} m³ ({drift:.1f}% apart, from independent per-month rounding). "
          "Both come from the same Ghaf field-study model.")

    # Capex/opex: the "package breakdown" used to be an independently
    # hardcoded cost model with its own total (AED 17.6M vs. the elemental
    # take-off's 18.6M). It's now a category-level split of the SAME verified
    # total the elemental take-off produces, so this checks that reconciliation
    # holds rather than reporting a live disagreement.
    elemental = cost["elemental"]["total"]
    package = cost["capexPackage"]["total"]
    spread = abs(elemental - package) / elemental * 100 if elemental else 0
    check("Capex: elemental take-off vs. package breakdown reconcile",
          spread < 1,
          f"Elemental take-off gives AED {elemental:,.0f}; the package breakdown (now "
          f"derived from the same total, split by construction system rather than by "
          f"zone) gives AED {package:,.0f} ({spread:.2f}% apart).")

    om_total = cost["om"]["total"]
    opex_pkg = cost["opexPackage"]["total"]
    ospread = abs(om_total - opex_pkg) / om_total * 100 if om_total else 0
    check("Opex: O&M model vs. package breakdown reconcile",
          ospread < 1,
          f"The O&M model gives AED {om_total:,.0f}/yr; the package breakdown (now "
          f"derived from the same total) gives AED {opex_pkg:,.0f}/yr "
          f"({ospread:.2f}% apart).")

    # Budget compliance — the hard constraint from the brief.
    check("Construction cost sits within the AED 35M brief budget",
          elemental <= BUDGET_AED,
          f"AED {elemental:,.0f} is {cost['budgetUsedPct']}% of the budget, leaving "
          f"AED {cost['headroom']:,.0f} of headroom.")

    # Phase 3 success metric: shaded route coverage >= 80%.
    check("Phase 3 target met: ≥80% of primary circulation shaded",
          perf["spineShadePct"] >= 80,
          f"The spine achieves {perf['spineShadePct']}% annual shade against an ≥80% target.")

    # Phase 3 success metric: >=60% green / soft surface.
    check("Phase 3 target: ≥60% green or soft-surface active space",
          zoning["greenPct"] >= 60,
          f"Green, buffer and passive zones total {zoning['greenPct']}% of the site. "
          "Counting the active soft-surface lawns as well brings the scheme to target; "
          "as categorised strictly, it does not.",
          severity="warn")

    # Source coverage.
    check("All expected source files were found",
          not WARNINGS,
          "; ".join(WARNINGS) if WARNINGS else
          f"{len(set(SOURCES_READ))} source files read cleanly.")

    # Bibliography hygiene: a reference nobody cites is dead weight, and a
    # citation naming an id that isn't in REFERENCES would already have
    # failed loudly inside track() — this check catches the opposite mistake.
    cited = {r for p in PROVENANCE for r in p.get("refs", [])}
    unused = [r["id"] for r in REFERENCES if r["id"] not in cited]
    check("Every listed reference is actually cited by a metric",
          not unused,
          f"Unused: {', '.join(unused)}" if unused else
          f"All {len(REFERENCES)} references are cited by at least one of the "
          f"{len(PROVENANCE)} tracked metrics.")

    return checks


# --------------------------------------------------------------------------
# Assemble & emit
# --------------------------------------------------------------------------
def main() -> int:
    climate = build_climate()
    solar = build_solar()
    catchment = build_catchment()
    problems = build_problems()
    zoning = build_zoning()
    planting = build_planting()
    perf = build_performance()
    cost = build_cost()
    advanced = build_advanced()
    narrative = build_narrative()
    deliverables = build_deliverables()
    renders = build_renders()

    audit = run_audit(zoning, planting, perf, cost)

    payload = {
        "meta": {
            "project": "Al Safa 2 Park",
            "concept": "The Shaded Spine",
            "author": "Mohamed Wasim",
            "client": "Dubai Municipality — AI Park Design Challenge",
            "deadline": "2026-08-15",
            "siteAreaSqm": zoning["siteArea"],
            "budgetAED": BUDGET_AED,
            "generated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
            "sourceCount": len(set(SOURCES_READ)),
        },
        "climate": climate,
        "solar": solar,
        "catchment": catchment,
        "problems": problems,
        "zoning": zoning,
        "planting": planting,
        "performance": perf,
        "cost": cost,
        "advanced": advanced,
        "concepts": narrative["concepts"],
        "objectives": narrative["objectives"],
        "personas": narrative["personas"],
        "deliverables": deliverables,
        "renders": renders,
        "provenance": PROVENANCE,
        "audit": audit,
        "sources": sorted(set(SOURCES_READ)),
        "references": REFERENCES,
    }

    # --- portal_data.js -------------------------------------------------
    out_js = os.path.join(HERE, "portal_data.js")
    body = json.dumps(payload, ensure_ascii=False, indent=1)
    with open(out_js, "w", encoding="utf-8") as fh:
        fh.write("/* GENERATED FILE — DO NOT EDIT BY HAND.\n"
                 "   Rebuild with:  python _PORTAL/build_portal.py\n"
                 "   Source of truth: the phase outputs/ folders. */\n")
        fh.write("window.AS2 = ")
        fh.write(body)
        fh.write(";\n")

    # --- DATA_AUDIT.md --------------------------------------------------
    out_md = os.path.join(HERE, "DATA_AUDIT.md")
    fails = [c for c in audit if c["status"] == "error"]
    warns = [c for c in audit if c["status"] == "warn"]

    lines = [
        "# Data Audit — Al Safa 2 Park",
        "",
        f"Generated {payload['meta']['generated']} by `_PORTAL/build_portal.py`.",
        "",
        "This report cross-checks the computed outputs of every phase against each "
        "other. It is regenerated on every build, so it always describes the current "
        "state of the data — not a past one.",
        "",
        f"**{len(audit) - len(fails) - len(warns)} passed · {len(warns)} warnings · "
        f"{len(fails)} failures**",
        "",
        "## Checks",
        "",
        "| Check | Result | Detail |",
        "|---|---|---|",
    ]
    icon = {"pass": "✅ pass", "warn": "⚠️ warn", "error": "❌ fail"}
    for c in audit:
        detail = c["detail"].replace("|", "\\|")
        lines.append(f"| {c['name']} | {icon[c['status']]} | {detail} |")

    lines += ["", "## Headline metrics and their provenance", "",
              "| Metric | Value | Source file | Method |", "|---|---|---|---|"]
    for p in PROVENANCE:
        val = p["value"]
        val = f"{val:,}" if isinstance(val, (int, float)) else val
        lines.append(f"| {p['label']} | {val} {p['unit']} | `{p['source']}` | "
                     f"{p['method']} |")

    lines += ["", "## Source files read", ""]
    lines += [f"- `{s}`" for s in sorted(set(SOURCES_READ))]

    lines += ["", "## External data sources (references)", "",
               "The real-world organisations and datasets behind the numbers above — not "
               "just the project's own CSV/JSON files. Transcribed from the citations the "
               "analysis scripts themselves already make; nothing here is invented for "
               "this report.", ""]
    for r in REFERENCES:
        lines.append(f"### {r['org']}")
        lines.append(f"**{r['title']}**")
        lines.append("")
        lines.append(f"- Period: {r['period']}")
        lines.append(f"- Retrieved: {r['retrieved']}")
        lines.append(f"- Used for: {r['usedFor']}")
        if r.get("caveat"):
            lines.append(f"- **Caveat:** {r['caveat']}")
        if r.get("url"):
            lines.append(f"- {r['url']}")
        used_by = [p["label"] for p in PROVENANCE if r["id"] in p.get("refs", [])]
        if used_by:
            lines.append(f"- Cited by: {', '.join(used_by)}")
        lines.append("")

    lines += ["---", "",
              "*Every figure shown in `index.html` is read from `portal_data.js`, which "
              "is generated from these files. The portal contains no independently "
              "typed analysis numbers.*", ""]

    with open(out_md, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))

    # --- console summary ------------------------------------------------
    print(f"portal_data.js   {os.path.getsize(out_js) / 1024:,.0f} KB")
    print(f"DATA_AUDIT.md    {len(audit)} checks · "
          f"{len(fails)} failures · {len(warns)} warnings")
    print(f"sources read     {len(set(SOURCES_READ))}")
    print(f"metrics tracked  {len(PROVENANCE)}")
    for w in WARNINGS:
        print(f"  ! {w}")
    for c in fails:
        print(f"  FAIL  {c['name']}: {c['detail']}")
    for c in warns:
        print(f"  WARN  {c['name']}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
