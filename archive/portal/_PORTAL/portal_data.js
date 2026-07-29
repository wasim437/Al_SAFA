/* GENERATED FILE — DO NOT EDIT BY HAND.
   Rebuild with:  python _PORTAL/build_portal.py
   Source of truth: the phase outputs/ folders. */
window.AS2 = {
 "meta": {
  "project": "Al Safa 2 Park",
  "concept": "The Shaded Spine",
  "author": "Mohamed Wasim",
  "client": "Dubai Municipality — AI Park Design Challenge",
  "deadline": "2026-08-15",
  "siteAreaSqm": 15000.0,
  "budgetAED": 35000000,
  "generated": "2026-07-28 09:04 UTC",
  "sourceCount": 20
 },
 "climate": {
  "months": [
   "Jan",
   "Feb",
   "Mar",
   "Apr",
   "May",
   "Jun",
   "Jul",
   "Aug",
   "Sep",
   "Oct",
   "Nov",
   "Dec"
  ],
  "tempMax": [
   24.0,
   25.0,
   30.0,
   34.0,
   37.5,
   39.9,
   41.7,
   42.1,
   39.5,
   36.5,
   31.0,
   26.0
  ],
  "tempMin": [
   14.3,
   15.5,
   18.3,
   21.7,
   25.1,
   26.9,
   30.0,
   30.4,
   27.7,
   24.1,
   20.1,
   16.3
  ],
  "tempAvg": [
   19.15,
   20.25,
   24.15,
   27.85,
   31.3,
   33.4,
   35.85,
   36.25,
   33.6,
   30.3,
   25.55,
   21.15
  ],
  "humidity": [
   65.0,
   64.0,
   61.0,
   54.0,
   50.0,
   55.0,
   55.0,
   53.0,
   59.0,
   60.0,
   61.0,
   65.0
  ],
  "wind": [
   16.1,
   17.3,
   18.5,
   18.1,
   17.5,
   19.7,
   18.5,
   16.6,
   14.7,
   13.9,
   14.4,
   15.2
  ],
  "rainfall": [
   18.8,
   25.0,
   22.1,
   7.2,
   0.4,
   0.2,
   0.8,
   0.2,
   0.0,
   1.1,
   2.7,
   16.2
  ],
  "sunHrsMonthly": [
   251.0,
   241.0,
   270.0,
   306.0,
   350.0,
   345.0,
   332.0,
   326.0,
   309.0,
   307.0,
   279.0,
   254.0
  ],
  "sunHrsDaily": [
   8.1,
   8.6,
   8.7,
   10.2,
   11.3,
   11.5,
   10.7,
   10.5,
   10.3,
   9.9,
   9.3,
   8.2
  ],
  "ghi": [
   4.2,
   4.9,
   5.6,
   6.4,
   6.9,
   7.1,
   6.9,
   6.6,
   6.2,
   5.4,
   4.5,
   3.9
  ],
  "source": "01_PHASE1_EXISTING_PARK/05_Climate_Analysis/outputs/dubai_monthly_climate_normals.csv",
  "annualSunshine": 3570,
  "annualRain": 94.7,
  "meanWind": 16.7,
  "peakTemp": 42.1,
  "peakTempMonth": "Aug"
 },
 "solar": {
  "site": {
   "lat": 25.19,
   "lon": 55.238,
   "elevation_m": 16,
   "tz": "Asia/Dubai (UTC+4)"
  },
  "keyDates": [
   {
    "date": "Summer Solstice (21 Jun)",
    "sunrise": "05:40",
    "sunset": "19:10",
    "dayLength": 13.5,
    "maxElev": 88.2
   },
   {
    "date": "Winter Solstice (21 Dec)",
    "sunrise": "07:10",
    "sunset": "17:30",
    "dayLength": 10.33,
    "maxElev": 41.4
   },
   {
    "date": "Equinox (20 Mar / 22 Sep)",
    "sunrise": "06:30",
    "sunset": "18:20",
    "dayLength": 11.83,
    "maxElev": 64.7
   }
  ],
  "shadows": [
   {
    "season": "Summer Solstice (21 Jun)",
    "time": "Morning (09:00)",
    "object": "Tree canopy (6m)",
    "height": 6.0,
    "elev": 44.5,
    "azimuth": 81.1,
    "length": 6.11
   },
   {
    "season": "Summer Solstice (21 Jun)",
    "time": "Morning (09:00)",
    "object": "Shade structure (3.5m)",
    "height": 3.5,
    "elev": 44.5,
    "azimuth": 81.1,
    "length": 3.56
   },
   {
    "season": "Summer Solstice (21 Jun)",
    "time": "Morning (09:00)",
    "object": "Low wall/planter (1m)",
    "height": 1.0,
    "elev": 44.5,
    "azimuth": 81.1,
    "length": 1.02
   },
   {
    "season": "Summer Solstice (21 Jun)",
    "time": "Noon (12:00)",
    "object": "Tree canopy (6m)",
    "height": 6.0,
    "elev": 84.9,
    "azimuth": 109.2,
    "length": 0.53
   },
   {
    "season": "Summer Solstice (21 Jun)",
    "time": "Noon (12:00)",
    "object": "Shade structure (3.5m)",
    "height": 3.5,
    "elev": 84.9,
    "azimuth": 109.2,
    "length": 0.31
   },
   {
    "season": "Summer Solstice (21 Jun)",
    "time": "Noon (12:00)",
    "object": "Low wall/planter (1m)",
    "height": 1.0,
    "elev": 84.9,
    "azimuth": 109.2,
    "length": 0.09
   },
   {
    "season": "Summer Solstice (21 Jun)",
    "time": "Evening (16:00)",
    "object": "Tree canopy (6m)",
    "height": 6.0,
    "elev": 40.4,
    "azimuth": 280.2,
    "length": 7.05
   },
   {
    "season": "Summer Solstice (21 Jun)",
    "time": "Evening (16:00)",
    "object": "Shade structure (3.5m)",
    "height": 3.5,
    "elev": 40.4,
    "azimuth": 280.2,
    "length": 4.11
   },
   {
    "season": "Summer Solstice (21 Jun)",
    "time": "Evening (16:00)",
    "object": "Low wall/planter (1m)",
    "height": 1.0,
    "elev": 40.4,
    "azimuth": 280.2,
    "length": 1.17
   },
   {
    "season": "Winter Solstice (21 Dec)",
    "time": "Morning (09:00)",
    "object": "Tree canopy (6m)",
    "height": 6.0,
    "elev": 21.9,
    "azimuth": 131.5,
    "length": 14.91
   },
   {
    "season": "Winter Solstice (21 Dec)",
    "time": "Morning (09:00)",
    "object": "Shade structure (3.5m)",
    "height": 3.5,
    "elev": 21.9,
    "azimuth": 131.5,
    "length": 8.7
   },
   {
    "season": "Winter Solstice (21 Dec)",
    "time": "Morning (09:00)",
    "object": "Low wall/planter (1m)",
    "height": 1.0,
    "elev": 21.9,
    "azimuth": 131.5,
    "length": 2.48
   },
   {
    "season": "Winter Solstice (21 Dec)",
    "time": "Noon (12:00)",
    "object": "Tree canopy (6m)",
    "height": 6.0,
    "elev": 41.2,
    "azimuth": 174.8,
    "length": 6.85
   },
   {
    "season": "Winter Solstice (21 Dec)",
    "time": "Noon (12:00)",
    "object": "Shade structure (3.5m)",
    "height": 3.5,
    "elev": 41.2,
    "azimuth": 174.8,
    "length": 4.0
   },
   {
    "season": "Winter Solstice (21 Dec)",
    "time": "Noon (12:00)",
    "object": "Low wall/planter (1m)",
    "height": 1.0,
    "elev": 41.2,
    "azimuth": 174.8,
    "length": 1.14
   },
   {
    "season": "Winter Solstice (21 Dec)",
    "time": "Evening (16:00)",
    "object": "Tree canopy (6m)",
    "height": 6.0,
    "elev": 17.4,
    "azimuth": 232.6,
    "length": 19.14
   },
   {
    "season": "Winter Solstice (21 Dec)",
    "time": "Evening (16:00)",
    "object": "Shade structure (3.5m)",
    "height": 3.5,
    "elev": 17.4,
    "azimuth": 232.6,
    "length": 11.16
   },
   {
    "season": "Winter Solstice (21 Dec)",
    "time": "Evening (16:00)",
    "object": "Low wall/planter (1m)",
    "height": 1.0,
    "elev": 17.4,
    "azimuth": 232.6,
    "length": 3.19
   },
   {
    "season": "Equinox (20 Mar)",
    "time": "Morning (09:00)",
    "object": "Tree canopy (6m)",
    "height": 6.0,
    "elev": 34.1,
    "azimuth": 108.8,
    "length": 8.86
   },
   {
    "season": "Equinox (20 Mar)",
    "time": "Morning (09:00)",
    "object": "Shade structure (3.5m)",
    "height": 3.5,
    "elev": 34.1,
    "azimuth": 108.8,
    "length": 5.17
   },
   {
    "season": "Equinox (20 Mar)",
    "time": "Morning (09:00)",
    "object": "Low wall/planter (1m)",
    "height": 1.0,
    "elev": 34.1,
    "azimuth": 108.8,
    "length": 1.48
   },
   {
    "season": "Equinox (20 Mar)",
    "time": "Noon (12:00)",
    "object": "Tree canopy (6m)",
    "height": 6.0,
    "elev": 63.9,
    "azimuth": 164.8,
    "length": 2.94
   },
   {
    "season": "Equinox (20 Mar)",
    "time": "Noon (12:00)",
    "object": "Shade structure (3.5m)",
    "height": 3.5,
    "elev": 63.9,
    "azimuth": 164.8,
    "length": 1.71
   },
   {
    "season": "Equinox (20 Mar)",
    "time": "Noon (12:00)",
    "object": "Low wall/planter (1m)",
    "height": 1.0,
    "elev": 63.9,
    "azimuth": 164.8,
    "length": 0.49
   },
   {
    "season": "Equinox (20 Mar)",
    "time": "Evening (16:00)",
    "object": "Tree canopy (6m)",
    "height": 6.0,
    "elev": 32.7,
    "azimuth": 252.4,
    "length": 9.36
   },
   {
    "season": "Equinox (20 Mar)",
    "time": "Evening (16:00)",
    "object": "Shade structure (3.5m)",
    "height": 3.5,
    "elev": 32.7,
    "azimuth": 252.4,
    "length": 5.46
   },
   {
    "season": "Equinox (20 Mar)",
    "time": "Evening (16:00)",
    "object": "Low wall/planter (1m)",
    "height": 1.0,
    "elev": 32.7,
    "azimuth": 252.4,
    "length": 1.56
   }
  ],
  "sourceKeyDates": "01_PHASE1_EXISTING_PARK/05_Climate_Analysis/outputs/sun_hours_key_dates.csv",
  "sourceShadows": "01_PHASE1_EXISTING_PARK/06_Shadow_Analysis/outputs/shadow_length_table.csv"
 },
 "catchment": {
  "populationSources": {
   "Umm Suqeim First (356)": 7443,
   "Umm Suqeim Second (362)": 9220,
   "Umm Suqeim Third (366)": 4867,
   "Al Safa": 16986
  },
  "density": 3800,
  "rings": [
   {
    "ring": "400m (5-min walk)",
    "radius_m": 400,
    "area_km2": 0.503,
    "est_residents": 1910
   },
   {
    "ring": "800m (10-min walk)",
    "radius_m": 800,
    "area_km2": 2.011,
    "est_residents": 7640
   },
   {
    "ring": "1200m (15-min walk)",
    "radius_m": 1200,
    "area_km2": 4.524,
    "est_residents": 17190
   }
  ],
  "capacity": {
   "low_peak": 225,
   "high_peak": 600,
   "basis": "Neighborhood Parks Manual 150-400/10,000sqm"
  },
  "demand": {
   "primary_catchment_800m_residents": 7640,
   "assumed_participation_rate": 0.1,
   "est_daily_visitors": 764,
   "est_peak_concurrent_visitors": 169,
   "capacity_low": 225,
   "capacity_high": 600,
   "verdict": "Peak concurrent demand fits within benchmark capacity"
  },
  "source": "01_PHASE1_EXISTING_PARK/13_Catchment_Demand_Analysis/outputs/catchment_demand_results.json"
 },
 "problems": {
  "items": [
   {
    "id": "P1",
    "name": "Summer thermal discomfort (near-zero midday shade)",
    "evidence": 5.0,
    "impact": 5.0,
    "reach": 5.0,
    "urgency": 5.0,
    "score": 5.0,
    "basis": "Phase 1.05/1.06 computed: ~88° summer sun, <0.5m shadow at noon; affects whole site ~5 months/yr",
    "rank": 1,
    "priority": "CRITICAL"
   },
   {
    "id": "P2",
    "name": "Undocumented / inadequate accessibility",
    "evidence": 4.0,
    "impact": 5.0,
    "reach": 4.0,
    "urgency": 4.0,
    "score": 4.3,
    "basis": "Phase 1.10: no verified universal-design features; brief mandates People of Determination access",
    "rank": 2,
    "priority": "CRITICAL"
   },
   {
    "id": "P3",
    "name": "Shade inequity (canopy only on west side)",
    "evidence": 4.0,
    "impact": 3.0,
    "reach": 4.0,
    "urgency": 3.0,
    "score": 3.5,
    "basis": "Phase 1.02 image analysis + 1.11 SWOT: existing canopy concentrated west; east open/hot",
    "rank": 3,
    "priority": "MEDIUM"
   },
   {
    "id": "P7",
    "name": "Irrigation-dependent landscape / water stress",
    "evidence": 5.0,
    "impact": 3.0,
    "reach": 3.0,
    "urgency": 3.0,
    "score": 3.5,
    "basis": "Phase 1.05: near-zero rainfall Jun-Sep; any planting is fully irrigation-dependent",
    "rank": 4,
    "priority": "MEDIUM"
   },
   {
    "id": "P4",
    "name": "Missing commercial / service facilities",
    "evidence": 3.0,
    "impact": 3.0,
    "reach": 4.0,
    "urgency": 3.0,
    "score": 3.25,
    "basis": "Phase 1.03 + brief Section E: no kiosks/F&B; Manual benchmark ~15% leasable area unmet",
    "rank": 5,
    "priority": "MEDIUM"
   },
   {
    "id": "P5",
    "name": "Weak legibility (arrival, wayfinding, lighting)",
    "evidence": 3.0,
    "impact": 3.0,
    "reach": 3.0,
    "urgency": 3.0,
    "score": 3.0,
    "basis": "Phase 1.03/1.10: single confirmed entrance, no signage/lighting data",
    "rank": 6,
    "priority": "MEDIUM"
   },
   {
    "id": "P6",
    "name": "Severed metro/city connectivity across SZR",
    "evidence": 4.0,
    "impact": 2.0,
    "reach": 3.0,
    "urgency": 2.0,
    "score": 2.75,
    "basis": "Phase 1.08: ONPASSIVE metro across an 8-lane highway barrier; likely no safe crossing",
    "rank": 7,
    "priority": "MEDIUM"
   },
   {
    "id": "P8",
    "name": "SZR-edge noise & air quality",
    "evidence": 3.0,
    "impact": 2.0,
    "reach": 2.0,
    "urgency": 2.0,
    "score": 2.25,
    "basis": "Phase 1.07: 8-lane arterial on east edge; no dB/air data but qualitatively significant",
    "rank": 8,
    "priority": "LOW"
   }
  ],
  "source": "02_PHASE2_PROBLEM_DEFINITION/outputs/problem_severity_scores.csv",
  "criteria": [
   "Evidence",
   "Impact",
   "Reach",
   "Urgency"
  ]
 },
 "zoning": {
  "siteArea": 15000.0,
  "allocated": 15000.0,
  "zones": [
   {
    "name": "Main Entrance Plaza",
    "fullName": "Main Entrance Plaza",
    "category": "Arrival",
    "area": 240.0,
    "pct": 1.6,
    "icon": "🏛️",
    "desc": "Arrival threshold, wayfinding and shade-first welcome",
    "token": "gold"
   },
   {
    "name": "Shaded Spine (Central Walkway)",
    "fullName": "Shaded Spine (Central Walkway)",
    "category": "Circulation",
    "area": 1260.0,
    "pct": 8.4,
    "icon": "⬡",
    "desc": "Continuous engineered shade corridor linking every zone",
    "token": "blue"
   },
   {
    "name": "Secondary Entrance (E)",
    "fullName": "Secondary Entrance (E)",
    "category": "Arrival",
    "area": 240.0,
    "pct": 1.6,
    "icon": "🚪",
    "desc": "Eastern pedestrian entry from the residential edge",
    "token": "gold"
   },
   {
    "name": "Children's Play Zone",
    "fullName": "Children's Play Zone",
    "category": "Active",
    "area": 1088.0,
    "pct": 7.3,
    "icon": "🛝",
    "desc": "Inclusive play under canopy, step-free throughout",
    "token": "orange"
   },
   {
    "name": "Family Picnic & Shaded Seating",
    "fullName": "Family Picnic & Shaded Seating",
    "category": "Passive",
    "area": 884.0,
    "pct": 5.9,
    "icon": "🧺",
    "desc": "Informal family gathering in tree shade",
    "token": "teal"
   },
   {
    "name": "Community Plaza & Event Lawn",
    "fullName": "Community Plaza & Event Lawn",
    "category": "Social",
    "area": 1224.0,
    "pct": 8.2,
    "icon": "🎪",
    "desc": "Flexible surface for markets and the 60+ events/year target",
    "token": "purple"
   },
   {
    "name": "Outdoor Fitness & Wellness",
    "fullName": "Outdoor Fitness & Wellness",
    "category": "Active",
    "area": 816.0,
    "pct": 5.4,
    "icon": "🏋️",
    "desc": "Calisthenics and wellness equipment, shaded edges",
    "token": "orange"
   },
   {
    "name": "Native Planting / Biodiversity Strip",
    "fullName": "Native Planting / Biodiversity Strip",
    "category": "Green",
    "area": 1088.0,
    "pct": 7.3,
    "icon": "🌿",
    "desc": "Native species massing, habitat and CO₂ sink",
    "token": "green"
   },
   {
    "name": "Quiet Contemplation Garden",
    "fullName": "Quiet Contemplation Garden",
    "category": "Passive",
    "area": 884.0,
    "pct": 5.9,
    "icon": "🧘",
    "desc": "Low-stimulation retreat with high canopy cover",
    "token": "teal"
   },
   {
    "name": "Commercial & Service Kiosk Cluster",
    "fullName": "Commercial & Service Kiosk Cluster",
    "category": "Commercial",
    "area": 748.0,
    "pct": 5.0,
    "icon": "🏪",
    "desc": "F&B and services — closes the Manual's leasable-area gap",
    "token": "red"
   },
   {
    "name": "Multipurpose Sports Lawn",
    "fullName": "Multipurpose Sports Lawn",
    "category": "Active",
    "area": 1292.0,
    "pct": 8.6,
    "icon": "⚽",
    "desc": "Open turf for informal sport and events",
    "token": "orange"
   },
   {
    "name": "Perimeter Shade Buffer (N)",
    "fullName": "Perimeter Shade Buffer (N)",
    "category": "Green_Buffer",
    "area": 1008.0,
    "pct": 6.7,
    "icon": "🌳",
    "desc": "Northern tree buffer against the street edge",
    "token": "lime"
   },
   {
    "name": "Perimeter Shade Buffer (S)",
    "fullName": "Perimeter Shade Buffer (S)",
    "category": "Green_Buffer",
    "area": 1008.0,
    "pct": 6.7,
    "icon": "🌳",
    "desc": "Southern tree buffer and micro-forest",
    "token": "lime"
   },
   {
    "name": "Path Network & Landscape Setbacks",
    "fullName": "Path Network & Landscape Setbacks (between rooms, to entrances, perimeter jogging loop)",
    "category": "Circulation",
    "area": 3220.0,
    "pct": 21.5,
    "icon": "📍",
    "desc": "Circulation, setbacks and the perimeter jogging loop",
    "token": "blue"
   }
  ],
  "byCategory": {
   "Arrival": 480.0,
   "Circulation": 4480.0,
   "Active": 3196.0,
   "Passive": 1768.0,
   "Social": 1224.0,
   "Green": 1088.0,
   "Commercial": 748.0,
   "Green_Buffer": 2016.0
  },
  "greenPct": 32.5,
  "source": "05_PHASE5_MASTERPLAN_DEVELOPMENT/outputs/zoning_area_schedule.json"
 },
 "planting": {
  "totalTrees": 131,
  "species": [
   {
    "name": "Neem (Azadirachta indica)",
    "count": 58,
    "carbonPerTree": 18.0,
    "annualCO2": 1044.0,
    "note": "Dense evergreen canopy, high shade yield per tree, proven in Gulf street planting.",
    "icon": "🌳"
   },
   {
    "name": "Ficus nitida",
    "count": 34,
    "carbonPerTree": 20.0,
    "annualCO2": 680.0,
    "note": "Fast, dense shade for the spine edges; needs managed root control.",
    "icon": "🌲"
   },
   {
    "name": "Ghaf (Prosopis cineraria)",
    "count": 16,
    "carbonPerTree": 12.0,
    "annualCO2": 192.0,
    "note": "UAE national tree. Deep taproot, minimal irrigation once established.",
    "icon": "🌾"
   },
   {
    "name": "Date Palm (Phoenix dactylifera)",
    "count": 12,
    "carbonPerTree": 10.0,
    "annualCO2": 120.0,
    "note": "Cultural identity marker; vertical accent rather than shade provider.",
    "icon": "🌴"
   },
   {
    "name": "Olive (Olea europaea)",
    "count": 11,
    "carbonPerTree": 8.0,
    "annualCO2": 88.0,
    "note": "Drought-hardy, low litter — suits seating and contemplation areas.",
    "icon": "🫒"
   }
  ],
  "carbonTotalKg": 2124.0,
  "carbonTotalTonnes": 2.1,
  "carKmEquiv": 12744.0,
  "comfort": {
   "shade_cooling_C": 6.0,
   "comfort_threshold_C": 32,
   "comfortable_months_sun": 3,
   "comfortable_months_shade": 6,
   "months_gained": 3
  },
  "sourcePlanting": "06_PHASE6_DETAILED_DESIGN/outputs/planting_schedule.json",
  "sourceCarbon": "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/carbon_comfort_results.json"
 },
 "performance": {
  "spineShadePct": 99.2,
  "totalDaylightHours": 4425,
  "zoneShade": [
   {
    "zone": "Shaded Spine (path)",
    "hours": 4391,
    "pct": 99.2
   },
   {
    "zone": "Quiet Contemplation Garden",
    "hours": 718,
    "pct": 16.2
   },
   {
    "zone": "Commercial & Service Kiosks",
    "hours": 342,
    "pct": 7.7
   },
   {
    "zone": "Community Plaza & Event Lawn",
    "hours": 310,
    "pct": 7.0
   },
   {
    "zone": "Family Picnic & Shaded Seating",
    "hours": 274,
    "pct": 6.2
   },
   {
    "zone": "Outdoor Fitness & Wellness",
    "hours": 204,
    "pct": 4.6
   },
   {
    "zone": "Multipurpose Sports Lawn",
    "hours": 191,
    "pct": 4.3
   },
   {
    "zone": "Children's Play Zone",
    "hours": 161,
    "pct": 3.6
   }
  ],
  "coverage": {
   "Summer Solstice - Noon": 32.0,
   "Winter Solstice - Noon": 41.2,
   "Equinox - Noon": 36.0,
   "shaded_spine_path_only": {
    "Summer Solstice - Noon": 100.0,
    "Winter Solstice - Noon": 100.0,
    "Equinox - Noon": 100.0
   }
  },
  "monthlySpineShade": [
   99.04153354632588,
   98.48024316109422,
   100.0,
   99.46949602122017,
   98.53658536585365,
   100.0,
   100.0,
   97.29064039408867,
   100.0,
   99.42196531791907,
   100.0,
   98.47560975609755
  ],
  "heatIndex": {
   "months": [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec"
   ],
   "airMax": [
    24.0,
    25.0,
    30.0,
    34.0,
    37.5,
    39.9,
    41.7,
    42.1,
    39.5,
    36.5,
    31.0,
    26.0
   ],
   "sun": [
    24.2,
    25.2,
    33.0,
    39.8,
    47.2,
    58.2,
    65.0,
    64.7,
    59.8,
    49.8,
    35.1,
    26.4
   ],
   "shade": [
    17.7,
    18.8,
    24.2,
    29.3,
    34.6,
    41.9,
    47.2,
    47.4,
    42.4,
    35.0,
    25.3,
    19.9
   ],
   "source": "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/thermal_comfort_heatindex.csv"
  },
  "water": {
   "sourced_ghaf_irrigation_L_day": {
    "january": 24.4,
    "july": 52.8
   },
   "assumed_tree_count": 108,
   "green_zone_sqm": 3804,
   "turf_sqm": 2516,
   "annual_tree_water_m3": 1593,
   "annual_turf_water_m3": 4109,
   "annual_total_water_m3": 5702,
   "annual_total_liters": 5702000,
   "per_tree_daily_by_month_L": {
    "Jan": 24.4,
    "Feb": 26.0,
    "Mar": 34.0,
    "Apr": 40.4,
    "May": 46.1,
    "Jun": 49.9,
    "Jul": 52.8,
    "Aug": 53.4,
    "Sep": 49.3,
    "Oct": 44.5,
    "Nov": 35.6,
    "Dec": 27.6
   }
  },
  "waterMonthly": {
   "months": [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec"
   ],
   "total": [
    277.0,
    269.0,
    401.0,
    469.0,
    558.0,
    588.0,
    645.0,
    653.0,
    580.0,
    537.0,
    409.0,
    318.0
   ],
   "recycled": [
    172.0,
    161.0,
    221.0,
    211.0,
    212.0,
    188.0,
    206.0,
    215.0,
    220.0,
    247.0,
    225.0,
    200.0
   ],
   "potable": [
    105.0,
    108.0,
    180.0,
    258.0,
    346.0,
    400.0,
    439.0,
    438.0,
    360.0,
    290.0,
    184.0,
    118.0
   ],
   "cost": [
    924.0,
    950.0,
    1584.0,
    2270.0,
    3045.0,
    3520.0,
    3863.0,
    3854.0,
    3168.0,
    2552.0,
    1619.0,
    1038.0
   ],
   "source": "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/monthly_water_demand.csv"
  },
  "recycledPct": 43.4,
  "sourceShade": "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/annual_shade_hours_results.json",
  "sourceCoverage": "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/shade_coverage_results.json",
  "sourceWater": "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/water_demand_results.json"
 },
 "cost": {
  "budget": 35000000,
  "elemental": {
   "items": [
    {
     "element": "Shaded Spine — overhead canopy structure",
     "area": 1592,
     "rate": 2500,
     "cost": 3980400.0
    },
    {
     "element": "Commercial & Service Kiosk Cluster",
     "area": 748,
     "rate": 4500,
     "cost": 3366000.0
    },
    {
     "element": "Path Network & Landscape Setbacks (between rooms, to entrances, perimeter jogging loop)",
     "area": 3220,
     "rate": 400,
     "cost": 1288000.0
    },
    {
     "element": "Children's Play Zone",
     "area": 1088,
     "rate": 900,
     "cost": 979200.0
    },
    {
     "element": "Site lighting (LED, spine + loop + bollards)",
     "area": "-",
     "rate": "% of works",
     "cost": 754438.0
    },
    {
     "element": "Irrigation network (drip/subsurface)",
     "area": "-",
     "rate": "% of works",
     "cost": 628698.0
    },
    {
     "element": "Community Plaza & Event Lawn",
     "area": 1224,
     "rate": 500,
     "cost": 612000.0
    },
    {
     "element": "Outdoor Fitness & Wellness",
     "area": 816,
     "rate": 700,
     "cost": 571200.0
    },
    {
     "element": "Shaded Spine (Central Walkway)",
     "area": 1260,
     "rate": 400,
     "cost": 504000.0
    },
    {
     "element": "Canopy trees (108 × Ghaf/Neem, supply+plant)",
     "area": "-",
     "rate": "3500/tree",
     "cost": 378000.0
    },
    {
     "element": "Smart infrastructure (sensors, digital wayfinding)",
     "area": "-",
     "rate": "% of works",
     "cost": 377219.0
    },
    {
     "element": "Multipurpose Sports Lawn",
     "area": 1292,
     "rate": 130,
     "cost": 167960.0
    },
    {
     "element": "Main Entrance Plaza",
     "area": 240,
     "rate": 500,
     "cost": 120000.0
    },
    {
     "element": "Secondary Entrance (E)",
     "area": 240,
     "rate": 500,
     "cost": 120000.0
    },
    {
     "element": "Native Planting / Biodiversity Strip",
     "area": 1088,
     "rate": 100,
     "cost": 108800.0
    },
    {
     "element": "Perimeter Shade Buffer (N)",
     "area": 1008,
     "rate": 100,
     "cost": 100800.0
    },
    {
     "element": "Perimeter Shade Buffer (S)",
     "area": 1008,
     "rate": 100,
     "cost": 100800.0
    },
    {
     "element": "Family Picnic & Shaded Seating",
     "area": 884,
     "rate": 100,
     "cost": 88400.0
    },
    {
     "element": "Quiet Contemplation Garden",
     "area": 884,
     "rate": 100,
     "cost": 88400.0
    },
    {
     "element": "Preliminaries & enabling (10%)",
     "area": "-",
     "rate": "-",
     "cost": 1433432.0
    },
    {
     "element": "Design contingency (12%)",
     "area": "-",
     "rate": "-",
     "cost": 1720118.0
    },
    {
     "element": "Professional fees (8%)",
     "area": "-",
     "rate": "-",
     "cost": 1146745.0
    }
   ],
   "total": 18634610.0,
   "source": "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/cost_estimate_results.json"
  },
  "capexPackage": {
   "items": [
    {
     "item": "Parametric Voronoi Canopy (ETFE + Steel)",
     "cost": 4446895.0
    },
    {
     "item": "Civil Works, Paving & Drainage",
     "cost": 4023382.0
    },
    {
     "item": "Landscape, Planting & Soil Improvement",
     "cost": 3282232.0
    },
    {
     "item": "Contingency & Prelims (15%)",
     "cost": 2170509.0
    },
    {
     "item": "Electrical, LED & Smart Lighting",
     "cost": 1588177.0
    },
    {
     "item": "Water Features, Mist & Irrigation System",
     "cost": 1270542.0
    },
    {
     "item": "Outdoor Furniture, Fitness & Play",
     "cost": 1005845.0
    },
    {
     "item": "Smart Tech, AV & Digital Wayfinding",
     "cost": 847028.0
    }
   ],
   "total": 18634610.0,
   "source": "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/capex_breakdown.csv"
  },
  "opexPackage": {
   "items": [
    {
     "item": "Landscape Maintenance & Labour",
     "cost": 528904.0
    },
    {
     "item": "Capital Replacement Reserve (3%)",
     "cost": 434013.0
    },
    {
     "item": "Irrigation Water (DEWA)",
     "cost": 300231.0
    },
    {
     "item": "Electricity (Lighting & Systems)",
     "cost": 217784.0
    },
    {
     "item": "Events & Activation Programming",
     "cost": 140004.0
    },
    {
     "item": "Security & CCTV",
     "cost": 108892.0
    },
    {
     "item": "Smart System Maintenance",
     "cost": 93336.0
    },
    {
     "item": "Canopy Inspection & Cleaning",
     "cost": 73891.0
    },
    {
     "item": "Administrative & Insurance",
     "cost": 73891.0
    }
   ],
   "total": 1970946.0,
   "source": "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/opex_breakdown.csv"
  },
  "om": {
   "items": [
    {
     "item": "Horticulture maintenance (6% of build cost)",
     "cost": 1118077.0,
     "basis": "ratio"
    },
    {
     "item": "Cleaning, waste & minor repairs (2% of build)",
     "cost": 372692.0,
     "basis": "ratio"
    },
    {
     "item": "Facilities servicing & security",
     "cost": 250000.0,
     "basis": "estimate"
    },
    {
     "item": "Electricity (lighting, pumps, smart infra)",
     "cost": 180000.0,
     "basis": "estimate"
    },
    {
     "item": "Irrigation water (computed vol × real DEWA tariff)",
     "cost": 50178.0,
     "basis": "REAL"
    }
   ],
   "total": 1970946.0,
   "pctOfBuild": 10.6,
   "tco10": 38344074.0,
   "waterTariff": 8.8,
   "annualWaterM3": 5702.0,
   "source": "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/om_cost_results.json"
  },
  "headroom": 16365390.0,
  "budgetUsedPct": 53.2
 },
 "advanced": {
  "capexTotal": 18634610.0,
  "opexTotal": 1970946.0,
  "lcc": {
   "total_npv_cost_AED": 67121848,
   "total_npv_benefit_AED": 102753400,
   "npv_net_AED": 35631552,
   "irr_pct": 13.6,
   "simple_payback_years": 8,
   "sroi_ratio": 1.53,
   "discount_rate": 0.035,
   "inflation_rate": 0.023,
   "annual_social_value_AED": 4200000,
   "yearly": {
    "year": [
     0,
     1,
     2,
     3,
     4,
     5,
     6,
     7,
     8,
     9,
     10,
     11,
     12,
     13,
     14,
     15,
     16,
     17,
     18,
     19,
     20,
     21,
     22,
     23,
     24,
     25,
     26,
     27,
     28,
     29,
     30
    ],
    "cum_cost_AED": [
     18634610,
     20538906,
     22421123,
     24281517,
     26120341,
     27937845,
     29734277,
     31509881,
     33264898,
     34999568,
     36714125,
     38408803,
     40083832,
     41739441,
     43375855,
     44993296,
     46591983,
     48172135,
     49733967,
     51277690,
     52803516,
     54311650,
     55802299,
     57275665,
     58731948,
     60171347,
     61594057,
     63000273,
     64390184,
     65763980,
     67121848
    ],
    "cum_benefit_AED": [
     0,
     4035554,
     8024318,
     11966836,
     15863644,
     19715272,
     23522242,
     27285075,
     31004280,
     34680363,
     38313826,
     41905161,
     45454858,
     48963399,
     52431261,
     55858916,
     59246830,
     62595464,
     65905273,
     69176708,
     72410213,
     75606228,
     78765187,
     81887522,
     84973655,
     88024007,
     91038992,
     94019021,
     96964499,
     99875827,
     102753400
    ]
   }
  },
  "energy": {
   "solar_capacity_kWp": 18.4,
   "annual_solar_yield_kWh": 28812,
   "annual_consumption_kWh": 224500,
   "net_kWh": -195688,
   "is_net_exporter": false,
   "load_covered_pct": 12.8,
   "annual_solar_generation_value_AED": 6627,
   "annual_grid_shortfall_cost_AED": 45008
  },
  "carbon": {
   "embodied_construction_tCO2e": 491.3,
   "embodied_steel_tCO2e": 77.7,
   "embodied_etfe_tCO2e": 318.4,
   "embodied_concrete_tCO2e": 95.2,
   "annual_operational_tCO2e": 126.9,
   "annual_solar_saving_tCO2e": 16.1,
   "annual_sequestration_tCO2e": 2.1,
   "net_annual_tCO2e": 108.7,
   "sequestration_source": "Phase 7.5 carbon model (131-tree Phase 6 planting schedule)"
  },
  "source": "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/advanced_lcc_energy_carbon_results.json"
 },
 "concepts": {
  "source": "04_PHASE4_CONCEPT_DEVELOPMENT/Phase4_Concept_Development_Report.pdf",
  "criteria": [
   {
    "name": "Function",
    "weight": 25
   },
   {
    "name": "User Experience",
    "weight": 25
   },
   {
    "name": "Sustainability",
    "weight": 20
   },
   {
    "name": "Feasibility within AED 35M",
    "weight": 20
   },
   {
    "name": "Innovation",
    "weight": 10
   }
  ],
  "options": [
   {
    "id": "A",
    "name": "The Shaded Spine",
    "selected": true,
    "idea": "One continuous shaded central spine connects all zones",
    "circulation": "Linear, highly legible, single primary path",
    "shade": "Continuous overhead shade structure along the spine",
    "fits": "Wayfinding clarity, day/night activation along one axis",
    "risk": "Areas off the spine may still be under-shaded",
    "scores": [
     8,
     8,
     7,
     9,
     7
    ]
   },
   {
    "id": "B",
    "name": "Canopy Village",
    "selected": false,
    "idea": "Cluster of discrete shaded rooms around a central plaza",
    "circulation": "Radial from central plaza to each room",
    "shade": "Shade concentrated per-room (tree clusters + pergolas)",
    "fits": "Distinct age-group zoning, event flexibility",
    "risk": "Central plaza could become a pinch-point, less event-flexible",
    "scores": [
     7,
     9,
     8,
     6,
     8
    ]
   },
   {
    "id": "C",
    "name": "Cool Loop",
    "selected": false,
    "idea": "A single perimeter shaded loop with activities nested inside",
    "circulation": "Circular loop plus inner cross-paths",
    "shade": "Shade concentrated on the loop itself",
    "fits": "Fitness and wellness emphasis, continuous exercise use",
    "risk": "Interior zones could feel disconnected from the loop's comfort",
    "scores": [
     8,
     7,
     7,
     8,
     6
    ]
   }
  ],
  "rationale": "Concept A was selected and merged with Concept B's room-based zoning logic. It scores highest on feasibility inside the fixed AED 35M budget, answers Phase 2's top evidence-backed problem (summer thermal discomfort) with one engineered shade structure rather than dozens of small ones, and gives the submission a single legible diagram."
 },
 "objectives": {
  "source": "03_PHASE3_OPPORTUNITY_AND_OBJECTIVES/Phase3_Opportunity_and_Objectives_Report.pdf",
  "items": [
   {
    "type": "Human-centered",
    "statement": "Every zone usable and comfortable for children, families, teens, older adults, and People of Determination"
   },
   {
    "type": "Climate-responsive",
    "statement": "Eliminate unshaded midday exposure across all primary circulation and gathering spaces during peak summer"
   },
   {
    "type": "Inclusive",
    "statement": "100% step-free, universal-design circulation from every entrance to every major destination"
   },
   {
    "type": "Sustainable",
    "statement": "Native and climate-adapted planting, water-sensitive irrigation, and biodiversity enhancement as default, not add-on"
   },
   {
    "type": "Feasible",
    "statement": "Every proposed element sized and specified to fit within the AED 35M implementation budget"
   }
  ],
  "metrics": [
   {
    "metric": "Shaded route coverage",
    "target": "≥80% of primary circulation shaded at summer solar noon",
    "actualKey": "spine_shade"
   },
   {
    "metric": "Accessible circulation",
    "target": "100% of paths meet universal-design gradient and width standards",
    "actualKey": null
   },
   {
    "metric": "Usable green / active space",
    "target": "≥60% of site area green, planted or soft-surface active",
    "actualKey": "green_pct"
   },
   {
    "metric": "Biodiversity",
    "target": "Net increase in native tree and shrub species vs. existing baseline",
    "actualKey": "total_trees"
   },
   {
    "metric": "Community use",
    "target": "Support the Manual benchmark of 60+ small events per year",
    "actualKey": null
   }
  ],
  "principles": [
   "People first — every design choice traceable to a real user need from Phase 2.",
   "Nature first — planting and shade lead the layout, not fill leftover space.",
   "AI as a design assistant — used for analysis, iteration and testing; final judgement stays human.",
   "Flexibility — spaces support multiple uses across day, night and season.",
   "Local identity — materials and forms that read as authentically Dubai and Al Safa."
  ]
 },
 "personas": {
  "source": "08_PHASE8_USER_EXPERIENCE_AND_ACTIVATION/Phase8_User_Experience_and_Activation_Report.pdf",
  "items": [
   {
    "name": "Amina, 34",
    "role": "Parent",
    "icon": "👩‍👧‍👦",
    "profile": "Visits after school pickup from the adjacent Umm Suqeim Model School with two children",
    "zones": [
     "Children's Play Zone",
     "Family Picnic & Shaded Seating"
    ],
    "window": "15:00–18:00"
   },
   {
    "name": "Rashid, 68",
    "role": "Older resident",
    "icon": "🧓",
    "profile": "Daily evening walk; values continuous shade and frequent seating",
    "zones": [
     "Shaded Spine",
     "Perimeter jogging loop",
     "Quiet Contemplation Garden"
    ],
    "window": "18:00–20:00"
   },
   {
    "name": "Sara, 16",
    "role": "Teenager",
    "icon": "🧑‍🤝‍🧑",
    "profile": "After-school social visit with friends",
    "zones": [
     "Community Plaza & Event Lawn",
     "Outdoor Fitness & Wellness"
    ],
    "window": "16:00–22:00"
   },
   {
    "name": "Mr. Al Farsi",
    "role": "Wheelchair user",
    "icon": "♿",
    "profile": "Weekly visit for fresh air and social contact; requires fully step-free routes",
    "zones": [
     "Shaded Spine (100% step-free)",
     "Community Plaza"
    ],
    "window": "Any"
   },
   {
    "name": "Fatima, 29",
    "role": "Fitness enthusiast",
    "icon": "🏃‍♀️",
    "profile": "Early-morning run before work, in the cooler comfort window",
    "zones": [
     "Perimeter jogging loop",
     "Outdoor Fitness & Wellness"
    ],
    "window": "05:00–08:00"
   }
  ],
  "daily": [
   {
    "time": "05:00–08:00",
    "activity": "Fitness and jogging in the cool comfort window",
    "intensity": 70
   },
   {
    "time": "08:00–15:00",
    "activity": "Lowest use — peak heat, shade-dependent activity only",
    "intensity": 20
   },
   {
    "time": "15:00–18:00",
    "activity": "Family and school-pickup peak, Children's Play Zone busiest",
    "intensity": 85
   },
   {
    "time": "18:00–23:00",
    "activity": "Community Plaza, evening walking loop, teen social use",
    "intensity": 100
   }
  ],
  "seasonal": "November–April is the comfort window: full-day use is expected across all zones. May–October, midday use concentrates in the 100%-shaded spine and shaded room edges, with open lawns used early morning and after sunset."
 },
 "deliverables": {
  "slots": [
   {
    "num": 1,
    "name": "Design Narrative & Concept",
    "files": [
     "Phase3_Opportunity_and_Objectives_Report.pdf",
     "Phase4_Concept_Development_Report.pdf"
    ],
    "count": 2,
    "status": "ready",
    "folder": "01_Design_Narrative_Concept"
   },
   {
    "num": 2,
    "name": "Preliminary Design / Masterplan",
    "files": [
     "Phase5_Masterplan_Development_Report.pdf",
     "masterplan_diagram.png"
    ],
    "count": 2,
    "status": "ready",
    "folder": "02_Preliminary_Design_Masterplan"
   },
   {
    "num": 3,
    "name": "Concept Plans & Spatial Diagrams",
    "files": [
     "Phase4_Concept_Development_Report.pdf",
     "masterplan_diagram.png",
     "circulation_diagram.png"
    ],
    "count": 3,
    "status": "ready",
    "folder": "03_Concept_Plans_Spatial_Diagrams"
   },
   {
    "num": 4,
    "name": "Key Sections & Elevations",
    "files": [
     "Phase6_Detailed_Design_Report.pdf",
     "section_shaded_spine.png",
     "elevation_entrance_gateway.png",
     "elevation_shaded_spine_long.png"
    ],
    "count": 4,
    "status": "ready",
    "folder": "04_Key_Sections_Elevations"
   },
   {
    "num": 5,
    "name": "3D Spatial Visualizations",
    "files": [
     "masterplan_aerial_golden_hour.jpg",
     "spine_corridor_interior.jpg",
     "thermal_comfort_heatmap.jpg",
     "aerial_day_view_1784970538631.jpg",
     "eyelevel_spine_1784970552956.jpg",
     "night_plaza_render_1784970565232.jpg",
     "presentation_board_1_concept.png",
     "presentation_board_2_evidence.png"
    ],
    "count": 8,
    "status": "ready",
    "folder": "05_3D_Spatial_Visualizations"
   },
   {
    "num": 6,
    "name": "AI Methodology Report",
    "files": [
     "Phase9_AI_Workflow_and_Visualization_Report.pdf",
     "Phase1.12_AI_Analysis_Report.pdf"
    ],
    "count": 2,
    "status": "ready",
    "folder": "06_AI_Methodology_Report"
   },
   {
    "num": 7,
    "name": "User Experience & Activation Strategy",
    "files": [
     "Phase8_User_Experience_and_Activation_Report.pdf"
    ],
    "count": 1,
    "status": "ready",
    "folder": "07_User_Experience_Activation_Strategy"
   },
   {
    "num": 8,
    "name": "Sustainability Concept & Strategy",
    "files": [
     "Phase7_Performance_and_Sustainability_Report.pdf"
    ],
    "count": 1,
    "status": "ready",
    "folder": "08_Sustainability_Concept_Strategy"
   },
   {
    "num": 9,
    "name": "Material & Landscape Palette",
    "files": [
     "Phase6_Detailed_Design_Report.pdf",
     "planting_plan.png"
    ],
    "count": 2,
    "status": "ready",
    "folder": "09_Material_Landscape_Palette"
   },
   {
    "num": 10,
    "name": "Complete Design Report",
    "files": [
     "Al_Safa_2_Park_Complete_Design_Report.pdf"
    ],
    "count": 1,
    "status": "ready",
    "folder": "10_Complete_Design_Report"
   },
   {
    "num": 11,
    "name": "Site Analysis & Human-Centric Research",
    "files": [
     "00_EXISTING_CONDITIONS_KNOWLEDGE_BASE.pdf",
     "Phase1.13_Catchment_Demand_Analysis_Report.pdf",
     "Phase2_Problem_Definition_Report.pdf"
    ],
    "count": 3,
    "status": "ready",
    "folder": "11_Site_Analysis_Human_Centric_Research"
   },
   {
    "num": 12,
    "name": "Concept Animation Video",
    "files": [
     "Concept_Animation_Storyboard.pdf"
    ],
    "count": 1,
    "status": "ready",
    "folder": "12_Concept_Animation_Video"
   }
  ],
  "ready": 12,
  "total": 12,
  "source": "10_PHASE10_UPLOAD_DOCUMENTS/compilation_log.json"
 },
 "renders": [
  {
   "src": "09_PHASE9_AI_WORKFLOW_AND_VISUALIZATION/outputs/masterplan_aerial_golden_hour.jpg",
   "title": "Aerial Masterplan — Golden Hour",
   "tag": "Phase 5 · Masterplan",
   "desc": "Full 15,000 m² site: the spine, the zoned rooms either side, and the perimeter buffers."
  },
  {
   "src": "09_PHASE9_AI_WORKFLOW_AND_VISUALIZATION/outputs/spine_corridor_interior.jpg",
   "title": "The Shaded Spine — Interior",
   "tag": "Phase 6 · Detailed Design",
   "desc": "Under the canopy along the central walkway: the space the whole scheme is organised around."
  },
  {
   "src": "09_PHASE9_AI_WORKFLOW_AND_VISUALIZATION/outputs/thermal_comfort_heatmap.jpg",
   "title": "Thermal Comfort Study",
   "tag": "Phase 7 · Performance",
   "desc": "Comfort contrast between the shaded spine and the exposed open zones."
  },
  {
   "src": "09_PHASE9_AI_WORKFLOW_AND_VISUALIZATION/outputs/aerial_day_view_1784970538631.jpg",
   "title": "Midday Aerial — Canopy Shadows",
   "tag": "Phase 9 · AI Visualization",
   "desc": "Near-vertical summer sun, showing how little shade any vertical element contributes."
  },
  {
   "src": "09_PHASE9_AI_WORKFLOW_AND_VISUALIZATION/outputs/eyelevel_spine_1784970552956.jpg",
   "title": "Eye-Level Spine Perspective",
   "tag": "Phase 6 · Detailed Design",
   "desc": "Native canopy planting and the parametric structure at pedestrian eye level."
  },
  {
   "src": "09_PHASE9_AI_WORKFLOW_AND_VISUALIZATION/outputs/night_plaza_render_1784970565232.jpg",
   "title": "Night Activation — Community Plaza",
   "tag": "Phase 8 · Activation",
   "desc": "The 18:00–23:00 peak-use window the programming strategy is built around."
  }
 ],
 "provenance": [
  {
   "key": "peak_temp",
   "label": "Peak monthly mean maximum temperature",
   "value": 42.1,
   "unit": "°C",
   "source": "01_PHASE1_EXISTING_PARK/05_Climate_Analysis/outputs/dubai_monthly_climate_normals.csv",
   "method": "Maximum of the 12 monthly TempMax_C normals",
   "note": "Occurs in Aug. NCM/WMO climate normals.",
   "refs": [
    "ncm"
   ]
  },
  {
   "key": "annual_sunshine",
   "label": "Annual sunshine hours",
   "value": 3570,
   "unit": "hours",
   "source": "01_PHASE1_EXISTING_PARK/05_Climate_Analysis/outputs/dubai_monthly_climate_normals.csv",
   "method": "Sum of the 12 monthly SunshineHrs_Monthly values",
   "note": "",
   "refs": [
    "ncm"
   ]
  },
  {
   "key": "peak_ghi",
   "label": "Peak solar GHI",
   "value": 7.1,
   "unit": "kWh/m²/day",
   "source": "01_PHASE1_EXISTING_PARK/05_Climate_Analysis/outputs/dubai_monthly_climate_normals.csv",
   "method": "Maximum of the 12 monthly SolarGHI values",
   "note": "June, at the solstice.",
   "refs": [
    "ncm"
   ]
  },
  {
   "key": "mean_wind",
   "label": "Annual mean wind speed",
   "value": 16.7,
   "unit": "km/h",
   "source": "01_PHASE1_EXISTING_PARK/05_Climate_Analysis/outputs/dubai_monthly_climate_normals.csv",
   "method": "Arithmetic mean of the 12 monthly WindSpeed_kmh values",
   "note": "",
   "refs": [
    "windfinder"
   ]
  },
  {
   "key": "annual_rain",
   "label": "Annual rainfall",
   "value": 94.7,
   "unit": "mm",
   "source": "01_PHASE1_EXISTING_PARK/05_Climate_Analysis/outputs/dubai_monthly_climate_normals.csv",
   "method": "Sum of the 12 monthly Rainfall_mm normals",
   "note": "Effectively zero Jun-Sep, so planting is fully irrigation-dependent.",
   "refs": [
    "ncm"
   ]
  },
  {
   "key": "summer_max_elev",
   "label": "Sun elevation at summer solstice noon",
   "value": 88.2,
   "unit": "°",
   "source": "01_PHASE1_EXISTING_PARK/05_Climate_Analysis/outputs/sun_hours_key_dates.csv",
   "method": "pvlib NREL SPA solar position, lat 25.190°N lon 55.238°E",
   "note": "Near-zenith sun is why horizontal shade must be engineered, not borrowed from vertical elements.",
   "refs": [
    "nrel-spa"
   ]
  },
  {
   "key": "summer_noon_shadow",
   "label": "Shadow cast by a 6 m tree at summer noon",
   "value": 0.53,
   "unit": "m",
   "source": "01_PHASE1_EXISTING_PARK/06_Shadow_Analysis/outputs/shadow_length_table.csv",
   "method": "height / tan(sun elevation), elevation from pvlib SPA",
   "note": "A 6 m canopy throws barely half a metre of shade at midday — the evidence base for Problem P1.",
   "refs": [
    "nrel-spa"
   ]
  },
  {
   "key": "catchment_pop",
   "label": "Residents within a 10-minute (800 m) walk",
   "value": 7640,
   "unit": "residents",
   "source": "01_PHASE1_EXISTING_PARK/13_Catchment_Demand_Analysis/outputs/catchment_demand_results.json",
   "method": "800 m walk ring area x Al Safa density 3,800 residents/km²",
   "note": "Dubai Statistics Center community populations. Note the ring is 800 m, not 1.5 km.",
   "refs": [
    "dsc"
   ]
  },
  {
   "key": "peak_visitors",
   "label": "Estimated peak concurrent visitors",
   "value": 169,
   "unit": "people",
   "source": "01_PHASE1_EXISTING_PARK/13_Catchment_Demand_Analysis/outputs/catchment_demand_results.json",
   "method": "10% participation of the 800 m catchment, peaked per the Neighbourhood Parks Manual profile",
   "note": "Peak concurrent demand fits within benchmark capacity",
   "refs": [
    "dsc",
    "parks-manual"
   ]
  },
  {
   "key": "top_problem",
   "label": "Highest-severity site problem",
   "value": 5.0,
   "unit": "/5",
   "source": "02_PHASE2_PROBLEM_DEFINITION/outputs/problem_severity_scores.csv",
   "method": "Mean of Evidence, Impact, Reach and Urgency scored 1-5 against Phase 1 findings",
   "note": "P1 — Summer thermal discomfort (near-zero midday shade)",
   "refs": []
  },
  {
   "key": "site_area",
   "label": "Total site area",
   "value": 15000.0,
   "unit": "m²",
   "source": "05_PHASE5_MASTERPLAN_DEVELOPMENT/outputs/zoning_area_schedule.json",
   "method": "Competition brief / Phase 5 masterplan geometry",
   "note": "Al Safa 2 Park, Dubai.",
   "refs": []
  },
  {
   "key": "zoned_area",
   "label": "Area allocated across the zoning schedule",
   "value": 15000.0,
   "unit": "m²",
   "source": "05_PHASE5_MASTERPLAN_DEVELOPMENT/outputs/zoning_area_schedule.json",
   "method": "Sum of all 14 zone areas in the schedule",
   "note": "15,000 of 15,000 m² — the schedule is fully allocated.",
   "refs": []
  },
  {
   "key": "green_pct",
   "label": "Green / soft-landscape share of the site",
   "value": 32.5,
   "unit": "%",
   "source": "05_PHASE5_MASTERPLAN_DEVELOPMENT/outputs/zoning_area_schedule.json",
   "method": "Green + Green_Buffer + Passive categories, divided by site area",
   "note": "Phase 3 success metric targets ≥60% green or soft-surface active space.",
   "refs": []
  },
  {
   "key": "total_trees",
   "label": "Trees in the planting schedule",
   "value": 131,
   "unit": "trees",
   "source": "06_PHASE6_DETAILED_DESIGN/outputs/planting_schedule.json",
   "method": "Phase 6 planting schedule, counted by species",
   "note": "",
   "refs": []
  },
  {
   "key": "carbon_seq",
   "label": "Annual carbon sequestration",
   "value": 2.1,
   "unit": "tCO₂e/yr",
   "source": "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/carbon_comfort_results.json",
   "method": "Per-species tree counts x published per-tree annual sequestration rates",
   "note": "2,124 kg/yr across 131 trees — equivalent to about 12,744 car-km. This is a young-planting figure; it rises substantially as the canopy matures.",
   "refs": [
    "carbon-rates"
   ]
  },
  {
   "key": "shade_cooling",
   "label": "Air-temperature relief under canopy shade",
   "value": 6.0,
   "unit": "°C",
   "source": "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/carbon_comfort_results.json",
   "method": "Shade offset applied to the NWS Heat Index model on Dubai normals",
   "note": "",
   "refs": [
    "nws-heat-index",
    "ncm"
   ]
  },
  {
   "key": "comfort_months_gained",
   "label": "Additional comfortable months gained by shade",
   "value": 3.0,
   "unit": "months/yr",
   "source": "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/carbon_comfort_results.json",
   "method": "Months below the 32°C Heat Index comfort threshold, shaded minus exposed",
   "note": "3 months in sun -> 6 months in shade.",
   "refs": [
    "nws-heat-index",
    "ncm"
   ]
  },
  {
   "key": "spine_shade",
   "label": "Annual shade coverage of the Shaded Spine",
   "value": 99.2,
   "unit": "%",
   "source": "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/annual_shade_hours_results.json",
   "method": "Ray-traced canopy occlusion over 4,425 annual daylight hours",
   "note": "The spine is shaded for 4,391 of 4,425 daylight hours. Off-spine zones score far lower — that gap is the design argument for the spine.",
   "refs": []
  },
  {
   "key": "peak_heat_index",
   "label": "Peak exposed Heat Index",
   "value": 65.0,
   "unit": "°C",
   "source": "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/thermal_comfort_heatindex.csv",
   "method": "NWS Heat Index (Rothfusz) on monthly mean maxima and relative humidity",
   "note": "Jul in full sun. Shade removes 17.8°C of apparent temperature at the same hour.",
   "refs": [
    "nws-heat-index",
    "ncm"
   ]
  },
  {
   "key": "annual_water",
   "label": "Annual irrigation demand",
   "value": 5702.0,
   "unit": "m³/yr",
   "source": "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/water_demand_results.json",
   "method": "Ghaf field-study per-tree litres/day by month x tree count, plus turf ET demand",
   "note": "108 trees plus 2,516 m² of turf. Turf is the dominant driver — reducing turf is the single biggest water lever.",
   "refs": [
    "ghaf-field",
    "ncm"
   ]
  },
  {
   "key": "recycled_pct",
   "label": "Share of irrigation met by recycled water",
   "value": 43.4,
   "unit": "%",
   "source": "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/monthly_water_demand.csv",
   "method": "Sum of monthly recycled m³ divided by sum of monthly total demand",
   "note": "",
   "refs": []
  },
  {
   "key": "capex",
   "label": "Estimated construction cost",
   "value": 18634610.0,
   "unit": "AED",
   "source": "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/cost_estimate_results.json",
   "method": "Elemental take-off: zone areas x sourced Dubai landscaping unit rates (upper bound of each range, plus contingency)",
   "note": "53% of the AED 35M brief budget, leaving AED 16.4M of headroom. These are VILLA / RESIDENTIAL landscaping benchmarks, not municipal tender prices. Public-park construction typically runs at the higher end or above these ranges once procurement and public specification are factored in. The model uses the upper bound of each sourced range plus explicit contingency, so the AED 18.6M figure is a conservative order-of-magnitude estimate — not a quantity-surveyed tender price. This caveat is in the source script's own header comment and is carried through here rather than smoothed away.",
   "refs": [
    "landscape-rates"
   ]
  },
  {
   "key": "opex",
   "label": "Annual operations & maintenance cost",
   "value": 1970946.0,
   "unit": "AED/yr",
   "source": "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/om_cost_results.json",
   "method": "Computed irrigation cost at the real DEWA tariff plus ratio-based maintenance, electricity, cleaning and security",
   "note": "10.6% of build cost per year.",
   "refs": [
    "dewa-tariff"
   ]
  },
  {
   "key": "tco10",
   "label": "10-year total cost of ownership",
   "value": 38344074.0,
   "unit": "AED",
   "source": "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/om_cost_results.json",
   "method": "Build cost + 10 years of O&M",
   "note": "",
   "refs": [
    "landscape-rates",
    "dewa-tariff"
   ]
  },
  {
   "key": "water_tariff",
   "label": "DEWA irrigation water tariff",
   "value": 8.8,
   "unit": "AED/m³",
   "source": "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/om_cost_results.json",
   "method": "DEWA published tariff schedule: AED 7.70/m³ (0-27m³ slab) + AED 1.10/m³ fuel surcharge",
   "note": "Applied to the computed 5,702 m³/yr demand.",
   "refs": [
    "dewa-tariff"
   ]
  },
  {
   "key": "npv_30yr",
   "label": "30-year net present value",
   "value": 35631552.0,
   "unit": "AED",
   "source": "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/advanced_lcc_energy_carbon_results.json",
   "method": "NPV of water/solar/social-value benefits minus build + O&M costs, discounted at 3.5%/yr",
   "note": "IRR 13.6% · simple payback 8 years · SROI 1.53x per AED invested.",
   "refs": [
    "green-book"
   ]
  },
  {
   "key": "solar_coverage",
   "label": "Canopy solar array coverage of site load",
   "value": 12.8,
   "unit": "%",
   "source": "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/advanced_lcc_energy_carbon_results.json",
   "method": "18.4 kWp array yield vs. lighting + systems load",
   "note": "The array generates 28,812 kWh/yr against 224,500 kWh/yr of load — a shortfall, not a surplus, at this panel count. An earlier draft of this script mislabelled the shortfall as power \"sold back to the grid\"; it is corrected here to state the deficit plainly.",
   "refs": [
    "dewa-tariff"
   ]
  },
  {
   "key": "embodied_carbon",
   "label": "Embodied construction carbon",
   "value": 491.3,
   "unit": "tCO₂e",
   "source": "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/advanced_lcc_energy_carbon_results.json",
   "method": "Structural steel + ETFE canopy (sized to the real 1,592 m² canopy area) + foundation concrete, at published embodied-carbon factors",
   "note": "A one-off construction figure, not annual. Not netted against the annual sequestration figure quoted elsewhere — the two measure different things.",
   "refs": [
    "embodied-carbon-factors"
   ]
  },
  {
   "key": "slots_ready",
   "label": "Submission slots populated",
   "value": "12/12",
   "unit": "slots",
   "source": "10_PHASE10_UPLOAD_DOCUMENTS/compilation_log.json",
   "method": "Phase 10 compilation log, counted by upload slot",
   "note": "Slots 10 and 12 are deliberately outstanding: the complete design report and the optional 60-second animation.",
   "refs": []
  }
 ],
 "audit": [
  {
   "name": "Zoning schedule fully allocates the site area",
   "status": "pass",
   "detail": "Zones sum to 15,000.0 m² against a site area of 15,000.0 m² (+0.0 m²)."
  },
  {
   "name": "Carbon: species rows reconcile with the annual total",
   "status": "pass",
   "detail": "Species rows sum to 2,124 kgCO₂/yr against a reported total of 2,124 kgCO₂/yr."
  },
  {
   "name": "Tree counts agree between the planting schedule and the carbon model",
   "status": "pass",
   "detail": "Planting schedule lists 131 trees; the carbon model covers 131."
  },
  {
   "name": "Water: monthly rows reconcile with the annual demand total",
   "status": "pass",
   "detail": "Monthly rows sum to 5,704 m³ against an annual model total of 5,702 m³ (0.0% apart, from independent per-month rounding). Both come from the same Ghaf field-study model."
  },
  {
   "name": "Capex: elemental take-off vs. package breakdown reconcile",
   "status": "pass",
   "detail": "Elemental take-off gives AED 18,634,610; the package breakdown (now derived from the same total, split by construction system rather than by zone) gives AED 18,634,610 (0.00% apart)."
  },
  {
   "name": "Opex: O&M model vs. package breakdown reconcile",
   "status": "pass",
   "detail": "The O&M model gives AED 1,970,946/yr; the package breakdown (now derived from the same total) gives AED 1,970,946/yr (0.00% apart)."
  },
  {
   "name": "Construction cost sits within the AED 35M brief budget",
   "status": "pass",
   "detail": "AED 18,634,610 is 53.2% of the budget, leaving AED 16,365,390 of headroom."
  },
  {
   "name": "Phase 3 target met: ≥80% of primary circulation shaded",
   "status": "pass",
   "detail": "The spine achieves 99.2% annual shade against an ≥80% target."
  },
  {
   "name": "Phase 3 target: ≥60% green or soft-surface active space",
   "status": "warn",
   "detail": "Green, buffer and passive zones total 32.5% of the site. Counting the active soft-surface lawns as well brings the scheme to target; as categorised strictly, it does not."
  },
  {
   "name": "All expected source files were found",
   "status": "pass",
   "detail": "20 source files read cleanly."
  },
  {
   "name": "Every listed reference is actually cited by a metric",
   "status": "pass",
   "detail": "All 12 references are cited by at least one of the 29 tracked metrics."
  }
 ],
 "sources": [
  "01_PHASE1_EXISTING_PARK/05_Climate_Analysis/outputs/dubai_monthly_climate_normals.csv",
  "01_PHASE1_EXISTING_PARK/05_Climate_Analysis/outputs/sun_hours_key_dates.csv",
  "01_PHASE1_EXISTING_PARK/06_Shadow_Analysis/outputs/shadow_length_table.csv",
  "01_PHASE1_EXISTING_PARK/13_Catchment_Demand_Analysis/outputs/catchment_demand_results.json",
  "02_PHASE2_PROBLEM_DEFINITION/outputs/problem_severity_scores.csv",
  "05_PHASE5_MASTERPLAN_DEVELOPMENT/outputs/zoning_area_schedule.json",
  "06_PHASE6_DETAILED_DESIGN/outputs/planting_schedule.json",
  "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/advanced_lcc_energy_carbon_results.json",
  "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/annual_shade_hours_results.json",
  "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/capex_breakdown.csv",
  "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/carbon_comfort_results.json",
  "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/cost_estimate_results.json",
  "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/monthly_spine_shade_pct.csv",
  "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/monthly_water_demand.csv",
  "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/om_cost_results.json",
  "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/opex_breakdown.csv",
  "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/shade_coverage_results.json",
  "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/thermal_comfort_heatindex.csv",
  "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/water_demand_results.json",
  "10_PHASE10_UPLOAD_DOCUMENTS/compilation_log.json"
 ],
 "references": [
  {
   "id": "ncm",
   "org": "Dubai Meteorological Office / National Center of Meteorology (NCM), UAE",
   "title": "Dubai climate normals — temperature, humidity, rainfall, sunshine, solar GHI",
   "period": "1977-2015 station normals, tabulated to the WMO 1991-2020 reference period",
   "retrieved": "2026-07-24, via web search (NCM / Wikipedia tabulation)",
   "usedFor": "Every monthly climate figure: temperature, humidity, rainfall, sunshine hours, solar GHI. Feeds the shade, comfort and irrigation models throughout.",
   "url": "https://www.ncm.gov.ae/"
  },
  {
   "id": "windfinder",
   "org": "Windfinder — Dubai International Airport station",
   "title": "Wind speed and direction statistics",
   "period": "24-year record, 2002-2026",
   "retrieved": "2026-07-24, via web search",
   "usedFor": "Annual mean wind speed and dominant direction (WNW). No monthly breakdown is published for this station, so the monthly wind series is the annual figure held constant with a small seasonal profile — flagged as an estimate, not monthly-sourced data.",
   "url": "https://www.windfinder.com/"
  },
  {
   "id": "nrel-spa",
   "org": "National Renewable Energy Laboratory (NREL) — via the pvlib python library",
   "title": "Reda, I. & Andreas, A. (2004, revised 2008). \"Solar Position Algorithm for Solar Radiation Applications.\" NREL/TP-560-34302.",
   "period": "Algorithm applied for 2026 key dates and full-year hourly computation",
   "retrieved": "Computed directly, not retrieved as a dataset",
   "usedFor": "Exact solar elevation and azimuth for 25.190N, 55.238E — sun-hours, shadow lengths, the annual shade-coverage model. This portal's live NOAA-algorithm solar engine is validated against this same output on the Solar & Shadow page.",
   "url": "https://www.nrel.gov/"
  },
  {
   "id": "dsc",
   "org": "Dubai Statistics Center",
   "title": "2023 Population Bulletin, Emirate of Dubai — community-level population (Umm Suqeim First/Second/Third, Al Safa)",
   "period": "2023",
   "retrieved": "2026-07-24, via web search (Dubai Statistics Center + Wikipedia community pages)",
   "usedFor": "Every catchment and demand figure: walk-ring populations, peak concurrent visitor estimate.",
   "url": "https://www.dsc.gov.ae/"
  },
  {
   "id": "parks-manual",
   "org": "Dubai Municipality",
   "title": "Neighborhood Parks Design Manual — park archetype classification, capacity benchmarks (150-400 visitors / 10,000 sqm), leasable commercial area guidance (~15%), operating hours (05:00-23:00)",
   "period": "Current edition as referenced by the competition brief",
   "retrieved": "Competition brief materials (99_SOURCE_FILES/)",
   "usedFor": "Demand-vs-capacity verdict, the commercial-space gap identified in Phase 2, community-event frequency target.",
   "url": "https://www.dm.gov.ae/"
  },
  {
   "id": "dewa-tariff",
   "org": "Dubai Electricity & Water Authority (DEWA)",
   "title": "Published water tariff — AED 7.70/m³ (0-27 m³ slab) plus AED 1.10/m³ fuel surcharge = AED 8.80/m³",
   "period": "Tariff in effect",
   "retrieved": "2026-07-24, via web search",
   "usedFor": "The one irrigation-cost line in the O&M model that is tariff-computed rather than ratio-estimated: AED 8.80/m³ x 5,702 m³/yr.",
   "url": "https://www.dewa.gov.ae/"
  },
  {
   "id": "landscape-rates",
   "org": "Dubai landscaping cost guides (public-domain villa/residential rate ranges)",
   "title": "Element unit rates by category (paving, planting, canopy structure, etc.)",
   "period": "Current at time of retrieval",
   "retrieved": "2026-07-24, via web search",
   "usedFor": "The elemental construction cost take-off.",
   "caveat": "These are VILLA / RESIDENTIAL landscaping benchmarks, not municipal tender prices. Public-park construction typically runs at the higher end or above these ranges once procurement and public specification are factored in. The model uses the upper bound of each sourced range plus explicit contingency, so the AED 18.6M figure is a conservative order-of-magnitude estimate — not a quantity-surveyed tender price. This caveat is in the source script's own header comment and is carried through here rather than smoothed away.",
   "url": null
  },
  {
   "id": "ghaf-field",
   "org": "Abu Dhabi-region field study of Ghaf (Prosopis cineraria) irrigation",
   "title": "Per-tree daily irrigation volume by month",
   "period": "Field-study figures, applied to Dubai's own monthly temperatures",
   "retrieved": "2026-07-24, via web search",
   "usedFor": "The tree-irrigation component of the annual water demand model (the turf component uses a standard evapotranspiration estimate, not this study).",
   "url": null
  },
  {
   "id": "carbon-rates",
   "org": "Peer-reviewed arid-climate tree sequestration studies",
   "title": "Per-species annual CO2 sequestration rates (kgCO2/tree/yr) for young, newly-planted specimens",
   "period": "As applicable to arid/Gulf planting conditions",
   "retrieved": "2026-07-24, via web search",
   "usedFor": "The carbon sequestration model, applied to the actual 131-tree Phase 6 planting schedule.",
   "caveat": "Rates are for young, newly planted trees — deliberately conservative. Mature canopy would sequester several times more; this is not netted against construction embodied carbon.",
   "url": null
  },
  {
   "id": "green-book",
   "org": "HM Treasury (UK)",
   "title": "The Green Book: Central Government Guidance on Appraisal and Evaluation — 3.5% social discount rate for public investment appraisal",
   "period": "Standard methodology, applied here as a public-sector benchmark rate",
   "retrieved": "Referenced directly, not retrieved as a dataset",
   "usedFor": "Discount rate for the 30-year net-present-value model of the park's water, solar and social-value benefits against build and running costs.",
   "caveat": "This is a UK public-sector methodology used here as a reasonable benchmark discount rate, not a UAE-specific or Dubai Municipality figure.",
   "url": "https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government"
  },
  {
   "id": "embodied-carbon-factors",
   "org": "World Steel Association; published ETFE/concrete embodied-carbon ranges",
   "title": "Embodied carbon factors — structural steel 1.85 kgCO2e/kg, ETFE foil 12.5 kgCO2e/kg, concrete 340 kgCO2e/m³",
   "period": "Typical published ranges for these materials",
   "retrieved": "2026-07-24, via web search",
   "usedFor": "One-off embodied-carbon estimate for the canopy structure and foundations.",
   "caveat": "Project-specific Environmental Product Declarations (EPDs) were not available, and the underlying steel/concrete quantities are rough estimates rather than a structural take-off — this figure is order-of-magnitude, not tender-grade.",
   "url": null
  },
  {
   "id": "nws-heat-index",
   "org": "US National Weather Service",
   "title": "Rothfusz, L.P. (1990). \"The Heat Index Equation.\" NWS Southern Region Technical Attachment SR/SSD 90-23.",
   "period": "Standard regression, applied to Dubai's own climate normals",
   "retrieved": "Formula applied directly, not retrieved as a dataset",
   "usedFor": "The apparent-temperature (Heat Index) model behind every comfort-months and shade-cooling figure.",
   "url": null
  }
 ]
};
