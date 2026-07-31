/* GENERATED FILE — DO NOT EDIT BY HAND.
   Rebuild with:  python tools/sync_portal.py
   Source of truth: src/plan.py, src/solar.py, and
   models/headline_metrics.json — i.e. the code that is run,
   not the frozen phase folders this file was first built from. */
window.AS2 = {
 "meta": {
  "project": "Al Safa 2 Park",
  "concept": "Falaj Al Safa",
  "author": "Mohamed Wasim",
  "client": "Dubai Municipality — AI Park Design Challenge",
  "deadline": "2026-08-15",
  "siteAreaSqm": 15000.0,
  "budgetAED": 35000000,
  "generated": "2026-07-31 16:54 UTC",
  "sourceCount": 20,
  "conceptSubtitle": "a crescent of shade over a channel of water"
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
  "source": "../archive/phases/01_PHASE1_EXISTING_PARK/05_Climate_Analysis/outputs/dubai_monthly_climate_normals.csv",
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
  "sourceKeyDates": "../archive/phases/01_PHASE1_EXISTING_PARK/05_Climate_Analysis/outputs/sun_hours_key_dates.csv",
  "sourceShadows": "../archive/phases/01_PHASE1_EXISTING_PARK/06_Shadow_Analysis/outputs/shadow_length_table.csv"
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
  "source": "../archive/phases/01_PHASE1_EXISTING_PARK/13_Catchment_Demand_Analysis/outputs/catchment_demand_results.json"
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
  "source": "../archive/phases/02_PHASE2_PROBLEM_DEFINITION/outputs/problem_severity_scores.csv",
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
    "name": "Al Mamsha — the Crescent Walk",
    "fullName": "Al Mamsha — the Crescent Walk",
    "key": "crescent_walk",
    "category": "Circulation",
    "area": 871.2,
    "pct": 5.8,
    "icon": "🚶",
    "desc": "The 7 m shaded walk beneath the crescent gridshell",
    "token": "blue",
    "residual": false,
    "labelXY": [
     60.24,
     41.77
    ],
    "parts": [
     [
      [
       16.26,
       57.65
      ],
      [
       18.01,
       56.84
      ],
      [
       19.77,
       56.06
      ],
      [
       21.54,
       55.3
      ],
      [
       23.32,
       54.56
      ],
      [
       25.11,
       53.85
      ],
      [
       26.91,
       53.17
      ],
      [
       28.72,
       52.51
      ],
      [
       30.54,
       51.87
      ],
      [
       32.36,
       51.26
      ],
      [
       34.2,
       50.68
      ],
      [
       36.04,
       50.12
      ],
      [
       37.9,
       49.59
      ],
      [
       39.76,
       49.09
      ],
      [
       41.62,
       48.61
      ],
      [
       43.49,
       48.15
      ],
      [
       45.37,
       47.72
      ],
      [
       47.26,
       47.32
      ],
      [
       49.15,
       46.95
      ],
      [
       51.04,
       46.6
      ],
      [
       52.94,
       46.28
      ],
      [
       54.84,
       45.98
      ],
      [
       56.75,
       45.71
      ],
      [
       58.66,
       45.47
      ],
      [
       60.58,
       45.26
      ],
      [
       62.49,
       45.07
      ],
      [
       64.41,
       44.91
      ],
      [
       66.34,
       44.77
      ],
      [
       68.26,
       44.66
      ],
      [
       70.18,
       44.58
      ],
      [
       72.11,
       44.53
      ],
      [
       74.04,
       44.5
      ],
      [
       75.96,
       44.5
      ],
      [
       77.89,
       44.53
      ],
      [
       79.82,
       44.58
      ],
      [
       81.74,
       44.66
      ],
      [
       83.66,
       44.77
      ],
      [
       85.59,
       44.91
      ],
      [
       87.51,
       45.07
      ],
      [
       89.42,
       45.26
      ],
      [
       91.34,
       45.47
      ],
      [
       93.25,
       45.71
      ],
      [
       95.16,
       45.98
      ],
      [
       97.06,
       46.28
      ],
      [
       98.96,
       46.6
      ],
      [
       100.85,
       46.95
      ],
      [
       102.74,
       47.32
      ],
      [
       104.63,
       47.72
      ],
      [
       106.51,
       48.15
      ],
      [
       108.38,
       48.61
      ],
      [
       110.24,
       49.09
      ],
      [
       112.1,
       49.59
      ],
      [
       113.96,
       50.12
      ],
      [
       115.8,
       50.68
      ],
      [
       117.64,
       51.26
      ],
      [
       119.46,
       51.87
      ],
      [
       121.28,
       52.51
      ],
      [
       123.09,
       53.17
      ],
      [
       124.89,
       53.85
      ],
      [
       126.68,
       54.56
      ],
      [
       128.46,
       55.3
      ],
      [
       130.23,
       56.06
      ],
      [
       131.99,
       56.84
      ],
      [
       133.74,
       57.65
      ],
      [
       136.73,
       51.32
      ],
      [
       134.89,
       50.47
      ],
      [
       133.04,
       49.65
      ],
      [
       131.18,
       48.85
      ],
      [
       129.31,
       48.07
      ],
      [
       127.43,
       47.33
      ],
      [
       125.54,
       46.61
      ],
      [
       123.63,
       45.91
      ],
      [
       121.72,
       45.25
      ],
      [
       119.8,
       44.61
      ],
      [
       117.87,
       43.99
      ],
      [
       115.93,
       43.41
      ],
      [
       113.99,
       42.85
      ],
      [
       112.04,
       42.32
      ],
      [
       110.08,
       41.81
      ],
      [
       108.11,
       41.34
      ],
      [
       106.13,
       40.89
      ],
      [
       104.15,
       40.47
      ],
      [
       102.17,
       40.07
      ],
      [
       100.18,
       39.71
      ],
      [
       98.18,
       39.37
      ],
      [
       96.18,
       39.06
      ],
      [
       94.18,
       38.78
      ],
      [
       92.17,
       38.52
      ],
      [
       90.16,
       38.3
      ],
      [
       88.14,
       38.1
      ],
      [
       86.12,
       37.93
      ],
      [
       84.1,
       37.79
      ],
      [
       82.08,
       37.67
      ],
      [
       80.06,
       37.59
      ],
      [
       78.04,
       37.53
      ],
      [
       76.01,
       37.5
      ],
      [
       73.99,
       37.5
      ],
      [
       71.96,
       37.53
      ],
      [
       69.94,
       37.59
      ],
      [
       67.92,
       37.67
      ],
      [
       65.9,
       37.79
      ],
      [
       63.88,
       37.93
      ],
      [
       61.86,
       38.1
      ],
      [
       59.84,
       38.3
      ],
      [
       57.83,
       38.52
      ],
      [
       55.82,
       38.78
      ],
      [
       53.82,
       39.06
      ],
      [
       51.82,
       39.37
      ],
      [
       49.82,
       39.71
      ],
      [
       47.83,
       40.07
      ],
      [
       45.85,
       40.47
      ],
      [
       43.87,
       40.89
      ],
      [
       41.89,
       41.34
      ],
      [
       39.92,
       41.81
      ],
      [
       37.96,
       42.32
      ],
      [
       36.01,
       42.85
      ],
      [
       34.07,
       43.41
      ],
      [
       32.13,
       43.99
      ],
      [
       30.2,
       44.61
      ],
      [
       28.28,
       45.25
      ],
      [
       26.37,
       45.91
      ],
      [
       24.46,
       46.61
      ],
      [
       22.57,
       47.33
      ],
      [
       20.69,
       48.07
      ],
      [
       18.82,
       48.85
      ],
      [
       16.96,
       49.65
      ],
      [
       15.11,
       50.47
      ],
      [
       13.27,
       51.32
      ]
     ]
    ]
   },
   {
    "name": "Al Falaj — the water channel",
    "fullName": "Al Falaj — the water channel",
    "key": "falaj",
    "category": "Water",
    "area": 105.2,
    "pct": 0.7,
    "icon": "💧",
    "desc": "A 0.9 m recirculating channel on the canopy's northern drip line",
    "token": "teal",
    "residual": false,
    "labelXY": [
     116.01,
     56.04
    ],
    "parts": [
     [
      [
       18.6,
       62.63
      ],
      [
       20.28,
       61.85
      ],
      [
       21.97,
       61.1
      ],
      [
       23.67,
       60.37
      ],
      [
       25.38,
       59.66
      ],
      [
       27.1,
       58.98
      ],
      [
       28.83,
       58.32
      ],
      [
       30.57,
       57.69
      ],
      [
       32.31,
       57.08
      ],
      [
       34.07,
       56.49
      ],
      [
       35.83,
       55.93
      ],
      [
       37.6,
       55.4
      ],
      [
       39.38,
       54.89
      ],
      [
       41.16,
       54.4
      ],
      [
       42.95,
       53.94
      ],
      [
       44.75,
       53.51
      ],
      [
       46.55,
       53.1
      ],
      [
       48.36,
       52.71
      ],
      [
       50.18,
       52.35
      ],
      [
       52.0,
       52.02
      ],
      [
       53.82,
       51.71
      ],
      [
       55.65,
       51.42
      ],
      [
       57.48,
       51.17
      ],
      [
       59.32,
       50.93
      ],
      [
       61.15,
       50.73
      ],
      [
       62.99,
       50.55
      ],
      [
       64.84,
       50.39
      ],
      [
       66.68,
       50.26
      ],
      [
       68.53,
       50.16
      ],
      [
       70.38,
       50.08
      ],
      [
       72.23,
       50.03
      ],
      [
       74.08,
       50.0
      ],
      [
       75.92,
       50.0
      ],
      [
       77.77,
       50.03
      ],
      [
       79.62,
       50.08
      ],
      [
       81.47,
       50.16
      ],
      [
       83.32,
       50.26
      ],
      [
       85.16,
       50.39
      ],
      [
       87.01,
       50.55
      ],
      [
       88.85,
       50.73
      ],
      [
       90.68,
       50.93
      ],
      [
       92.52,
       51.17
      ],
      [
       94.35,
       51.42
      ],
      [
       96.18,
       51.71
      ],
      [
       98.0,
       52.02
      ],
      [
       99.82,
       52.35
      ],
      [
       101.64,
       52.71
      ],
      [
       103.45,
       53.1
      ],
      [
       105.25,
       53.51
      ],
      [
       107.05,
       53.94
      ],
      [
       108.84,
       54.4
      ],
      [
       110.62,
       54.89
      ],
      [
       112.4,
       55.4
      ],
      [
       114.17,
       55.93
      ],
      [
       115.93,
       56.49
      ],
      [
       117.69,
       57.08
      ],
      [
       119.43,
       57.69
      ],
      [
       121.17,
       58.32
      ],
      [
       122.9,
       58.98
      ],
      [
       124.62,
       59.66
      ],
      [
       126.33,
       60.37
      ],
      [
       128.03,
       61.1
      ],
      [
       129.72,
       61.85
      ],
      [
       131.4,
       62.63
      ],
      [
       131.78,
       61.81
      ],
      [
       130.09,
       61.03
      ],
      [
       128.39,
       60.27
      ],
      [
       126.68,
       59.54
      ],
      [
       124.96,
       58.83
      ],
      [
       123.23,
       58.14
      ],
      [
       121.49,
       57.48
      ],
      [
       119.74,
       56.84
      ],
      [
       117.98,
       56.23
      ],
      [
       116.21,
       55.64
      ],
      [
       114.44,
       55.07
      ],
      [
       112.65,
       54.54
      ],
      [
       110.86,
       54.02
      ],
      [
       109.07,
       53.53
      ],
      [
       107.26,
       53.07
      ],
      [
       105.45,
       52.63
      ],
      [
       103.64,
       52.22
      ],
      [
       101.82,
       51.83
      ],
      [
       99.99,
       51.47
      ],
      [
       98.16,
       51.13
      ],
      [
       96.32,
       50.82
      ],
      [
       94.48,
       50.53
      ],
      [
       92.64,
       50.27
      ],
      [
       90.79,
       50.04
      ],
      [
       88.94,
       49.83
      ],
      [
       87.09,
       49.65
      ],
      [
       85.23,
       49.49
      ],
      [
       83.37,
       49.36
      ],
      [
       81.52,
       49.26
      ],
      [
       79.65,
       49.18
      ],
      [
       77.79,
       49.13
      ],
      [
       75.93,
       49.1
      ],
      [
       74.07,
       49.1
      ],
      [
       72.21,
       49.13
      ],
      [
       70.35,
       49.18
      ],
      [
       68.48,
       49.26
      ],
      [
       66.63,
       49.36
      ],
      [
       64.77,
       49.49
      ],
      [
       62.91,
       49.65
      ],
      [
       61.06,
       49.83
      ],
      [
       59.21,
       50.04
      ],
      [
       57.36,
       50.27
      ],
      [
       55.52,
       50.53
      ],
      [
       53.68,
       50.82
      ],
      [
       51.84,
       51.13
      ],
      [
       50.01,
       51.47
      ],
      [
       48.18,
       51.83
      ],
      [
       46.36,
       52.22
      ],
      [
       44.55,
       52.63
      ],
      [
       42.74,
       53.07
      ],
      [
       40.93,
       53.53
      ],
      [
       39.14,
       54.02
      ],
      [
       37.35,
       54.54
      ],
      [
       35.56,
       55.07
      ],
      [
       33.79,
       55.64
      ],
      [
       32.02,
       56.23
      ],
      [
       30.26,
       56.84
      ],
      [
       28.51,
       57.48
      ],
      [
       26.77,
       58.14
      ],
      [
       25.04,
       58.83
      ],
      [
       23.32,
       59.54
      ],
      [
       21.61,
       60.27
      ],
      [
       19.91,
       61.03
      ],
      [
       18.22,
       61.81
      ]
     ]
    ]
   },
   {
    "name": "Crescent Shade Margin (N)",
    "fullName": "Crescent Shade Margin (N)",
    "key": "margin_n",
    "category": "Green",
    "area": 549.0,
    "pct": 3.7,
    "icon": "🌿",
    "desc": "Planted margin under the northern overhang; the tree avenue",
    "token": "lime",
    "residual": false,
    "labelXY": [
     89.16,
     47.54
    ],
    "parts": [
     [
      [
       18.22,
       61.81
      ],
      [
       19.91,
       61.03
      ],
      [
       21.61,
       60.27
      ],
      [
       23.32,
       59.54
      ],
      [
       25.04,
       58.83
      ],
      [
       26.77,
       58.14
      ],
      [
       28.51,
       57.48
      ],
      [
       30.26,
       56.84
      ],
      [
       32.02,
       56.23
      ],
      [
       33.79,
       55.64
      ],
      [
       35.56,
       55.07
      ],
      [
       37.35,
       54.54
      ],
      [
       39.14,
       54.02
      ],
      [
       40.93,
       53.53
      ],
      [
       42.74,
       53.07
      ],
      [
       44.55,
       52.63
      ],
      [
       46.36,
       52.22
      ],
      [
       48.18,
       51.83
      ],
      [
       50.01,
       51.47
      ],
      [
       51.84,
       51.13
      ],
      [
       53.68,
       50.82
      ],
      [
       55.52,
       50.53
      ],
      [
       57.36,
       50.27
      ],
      [
       59.21,
       50.04
      ],
      [
       61.06,
       49.83
      ],
      [
       62.91,
       49.65
      ],
      [
       64.77,
       49.49
      ],
      [
       66.63,
       49.36
      ],
      [
       68.48,
       49.26
      ],
      [
       70.35,
       49.18
      ],
      [
       72.21,
       49.13
      ],
      [
       74.07,
       49.1
      ],
      [
       75.93,
       49.1
      ],
      [
       77.79,
       49.13
      ],
      [
       79.65,
       49.18
      ],
      [
       81.52,
       49.26
      ],
      [
       83.37,
       49.36
      ],
      [
       85.23,
       49.49
      ],
      [
       87.09,
       49.65
      ],
      [
       88.94,
       49.83
      ],
      [
       90.79,
       50.04
      ],
      [
       92.64,
       50.27
      ],
      [
       94.48,
       50.53
      ],
      [
       96.32,
       50.82
      ],
      [
       98.16,
       51.13
      ],
      [
       99.99,
       51.47
      ],
      [
       101.82,
       51.83
      ],
      [
       103.64,
       52.22
      ],
      [
       105.45,
       52.63
      ],
      [
       107.26,
       53.07
      ],
      [
       109.07,
       53.53
      ],
      [
       110.86,
       54.02
      ],
      [
       112.65,
       54.54
      ],
      [
       114.44,
       55.07
      ],
      [
       116.21,
       55.64
      ],
      [
       117.98,
       56.23
      ],
      [
       119.74,
       56.84
      ],
      [
       121.49,
       57.48
      ],
      [
       123.23,
       58.14
      ],
      [
       124.96,
       58.83
      ],
      [
       126.68,
       59.54
      ],
      [
       128.39,
       60.27
      ],
      [
       130.09,
       61.03
      ],
      [
       131.78,
       61.81
      ],
      [
       133.74,
       57.65
      ],
      [
       131.99,
       56.84
      ],
      [
       130.23,
       56.06
      ],
      [
       128.46,
       55.3
      ],
      [
       126.68,
       54.56
      ],
      [
       124.89,
       53.85
      ],
      [
       123.09,
       53.17
      ],
      [
       121.28,
       52.51
      ],
      [
       119.46,
       51.87
      ],
      [
       117.64,
       51.26
      ],
      [
       115.8,
       50.68
      ],
      [
       113.96,
       50.12
      ],
      [
       112.1,
       49.59
      ],
      [
       110.24,
       49.09
      ],
      [
       108.38,
       48.61
      ],
      [
       106.51,
       48.15
      ],
      [
       104.63,
       47.72
      ],
      [
       102.74,
       47.32
      ],
      [
       100.85,
       46.95
      ],
      [
       98.96,
       46.6
      ],
      [
       97.06,
       46.28
      ],
      [
       95.16,
       45.98
      ],
      [
       93.25,
       45.71
      ],
      [
       91.34,
       45.47
      ],
      [
       89.42,
       45.26
      ],
      [
       87.51,
       45.07
      ],
      [
       85.59,
       44.91
      ],
      [
       83.66,
       44.77
      ],
      [
       81.74,
       44.66
      ],
      [
       79.82,
       44.58
      ],
      [
       77.89,
       44.53
      ],
      [
       75.96,
       44.5
      ],
      [
       74.04,
       44.5
      ],
      [
       72.11,
       44.53
      ],
      [
       70.18,
       44.58
      ],
      [
       68.26,
       44.66
      ],
      [
       66.34,
       44.77
      ],
      [
       64.41,
       44.91
      ],
      [
       62.49,
       45.07
      ],
      [
       60.58,
       45.26
      ],
      [
       58.66,
       45.47
      ],
      [
       56.75,
       45.71
      ],
      [
       54.84,
       45.98
      ],
      [
       52.94,
       46.28
      ],
      [
       51.04,
       46.6
      ],
      [
       49.15,
       46.95
      ],
      [
       47.26,
       47.32
      ],
      [
       45.37,
       47.72
      ],
      [
       43.49,
       48.15
      ],
      [
       41.62,
       48.61
      ],
      [
       39.76,
       49.09
      ],
      [
       37.9,
       49.59
      ],
      [
       36.04,
       50.12
      ],
      [
       34.2,
       50.68
      ],
      [
       32.36,
       51.26
      ],
      [
       30.54,
       51.87
      ],
      [
       28.72,
       52.51
      ],
      [
       26.91,
       53.17
      ],
      [
       25.11,
       53.85
      ],
      [
       23.32,
       54.56
      ],
      [
       21.54,
       55.3
      ],
      [
       19.77,
       56.06
      ],
      [
       18.01,
       56.84
      ],
      [
       16.26,
       57.65
      ]
     ]
    ]
   },
   {
    "name": "Crescent Shade Margin (S)",
    "fullName": "Crescent Shade Margin (S)",
    "key": "margin_s",
    "category": "Green",
    "area": 714.8,
    "pct": 4.8,
    "icon": "🌿",
    "desc": "Planted margin under the southern louvre; the tree avenue",
    "token": "lime",
    "residual": false,
    "labelXY": [
     29.42,
     41.97
    ],
    "parts": [
     [
      [
       13.27,
       51.32
      ],
      [
       15.11,
       50.47
      ],
      [
       16.96,
       49.65
      ],
      [
       18.82,
       48.85
      ],
      [
       20.69,
       48.07
      ],
      [
       22.57,
       47.33
      ],
      [
       24.46,
       46.61
      ],
      [
       26.37,
       45.91
      ],
      [
       28.28,
       45.25
      ],
      [
       30.2,
       44.61
      ],
      [
       32.13,
       43.99
      ],
      [
       34.07,
       43.41
      ],
      [
       36.01,
       42.85
      ],
      [
       37.96,
       42.32
      ],
      [
       39.92,
       41.81
      ],
      [
       41.89,
       41.34
      ],
      [
       43.87,
       40.89
      ],
      [
       45.85,
       40.47
      ],
      [
       47.83,
       40.07
      ],
      [
       49.82,
       39.71
      ],
      [
       51.82,
       39.37
      ],
      [
       53.82,
       39.06
      ],
      [
       55.82,
       38.78
      ],
      [
       57.83,
       38.52
      ],
      [
       59.84,
       38.3
      ],
      [
       61.86,
       38.1
      ],
      [
       63.88,
       37.93
      ],
      [
       65.9,
       37.79
      ],
      [
       67.92,
       37.67
      ],
      [
       69.94,
       37.59
      ],
      [
       71.96,
       37.53
      ],
      [
       73.99,
       37.5
      ],
      [
       76.01,
       37.5
      ],
      [
       78.04,
       37.53
      ],
      [
       80.06,
       37.59
      ],
      [
       82.08,
       37.67
      ],
      [
       84.1,
       37.79
      ],
      [
       86.12,
       37.93
      ],
      [
       88.14,
       38.1
      ],
      [
       90.16,
       38.3
      ],
      [
       92.17,
       38.52
      ],
      [
       94.18,
       38.78
      ],
      [
       96.18,
       39.06
      ],
      [
       98.18,
       39.37
      ],
      [
       100.18,
       39.71
      ],
      [
       102.17,
       40.07
      ],
      [
       104.15,
       40.47
      ],
      [
       106.13,
       40.89
      ],
      [
       108.11,
       41.34
      ],
      [
       110.08,
       41.81
      ],
      [
       112.04,
       42.32
      ],
      [
       113.99,
       42.85
      ],
      [
       115.93,
       43.41
      ],
      [
       117.87,
       43.99
      ],
      [
       119.8,
       44.61
      ],
      [
       121.72,
       45.25
      ],
      [
       123.63,
       45.91
      ],
      [
       125.54,
       46.61
      ],
      [
       127.43,
       47.33
      ],
      [
       129.31,
       48.07
      ],
      [
       131.18,
       48.85
      ],
      [
       133.04,
       49.65
      ],
      [
       134.89,
       50.47
      ],
      [
       136.73,
       51.32
      ],
      [
       139.07,
       46.35
      ],
      [
       137.17,
       45.46
      ],
      [
       135.25,
       44.61
      ],
      [
       133.32,
       43.78
      ],
      [
       131.37,
       42.98
      ],
      [
       129.42,
       42.2
      ],
      [
       127.46,
       41.45
      ],
      [
       125.48,
       40.73
      ],
      [
       123.5,
       40.04
      ],
      [
       121.5,
       39.38
      ],
      [
       119.5,
       38.74
      ],
      [
       117.49,
       38.13
      ],
      [
       115.47,
       37.55
      ],
      [
       113.44,
       37.0
      ],
      [
       111.41,
       36.48
      ],
      [
       109.37,
       35.98
      ],
      [
       107.32,
       35.52
      ],
      [
       105.26,
       35.08
      ],
      [
       103.2,
       34.67
      ],
      [
       101.13,
       34.29
      ],
      [
       99.06,
       33.94
      ],
      [
       96.99,
       33.62
      ],
      [
       94.9,
       33.32
      ],
      [
       92.82,
       33.06
      ],
      [
       90.73,
       32.83
      ],
      [
       88.64,
       32.62
      ],
      [
       86.55,
       32.44
      ],
      [
       84.45,
       32.3
      ],
      [
       82.35,
       32.18
      ],
      [
       80.25,
       32.09
      ],
      [
       78.15,
       32.03
      ],
      [
       76.05,
       32.0
      ],
      [
       73.95,
       32.0
      ],
      [
       71.85,
       32.03
      ],
      [
       69.75,
       32.09
      ],
      [
       67.65,
       32.18
      ],
      [
       65.55,
       32.3
      ],
      [
       63.45,
       32.44
      ],
      [
       61.36,
       32.62
      ],
      [
       59.27,
       32.83
      ],
      [
       57.18,
       33.06
      ],
      [
       55.1,
       33.32
      ],
      [
       53.01,
       33.62
      ],
      [
       50.94,
       33.94
      ],
      [
       48.87,
       34.29
      ],
      [
       46.8,
       34.67
      ],
      [
       44.74,
       35.08
      ],
      [
       42.68,
       35.52
      ],
      [
       40.63,
       35.98
      ],
      [
       38.59,
       36.48
      ],
      [
       36.56,
       37.0
      ],
      [
       34.53,
       37.55
      ],
      [
       32.51,
       38.13
      ],
      [
       30.5,
       38.74
      ],
      [
       28.5,
       39.38
      ],
      [
       26.5,
       40.04
      ],
      [
       24.52,
       40.73
      ],
      [
       22.54,
       41.45
      ],
      [
       20.58,
       42.2
      ],
      [
       18.63,
       42.98
      ],
      [
       16.68,
       43.78
      ],
      [
       14.75,
       44.61
      ],
      [
       12.83,
       45.46
      ],
      [
       10.93,
       46.35
      ]
     ]
    ]
   },
   {
    "name": "West Gate Majlis",
    "fullName": "West Gate Majlis",
    "key": "gate_w",
    "category": "Arrival",
    "area": 439.0,
    "pct": 2.9,
    "icon": "🚪",
    "desc": "Arrival majlis at the western horn, breaking through the berm",
    "token": "gold",
    "residual": false,
    "labelXY": [
     8.44,
     64.54
    ],
    "parts": [
     [
      [
       0.0,
       78.22
      ],
      [
       0.24,
       78.05
      ],
      [
       0.55,
       77.82
      ],
      [
       0.86,
       77.6
      ],
      [
       1.17,
       77.38
      ],
      [
       1.48,
       77.16
      ],
      [
       1.8,
       76.94
      ],
      [
       2.11,
       76.73
      ],
      [
       2.43,
       76.51
      ],
      [
       2.74,
       76.29
      ],
      [
       3.06,
       76.08
      ],
      [
       3.37,
       75.86
      ],
      [
       3.69,
       75.65
      ],
      [
       4.01,
       75.44
      ],
      [
       4.33,
       75.23
      ],
      [
       4.65,
       75.02
      ],
      [
       4.97,
       74.81
      ],
      [
       5.29,
       74.6
      ],
      [
       5.61,
       74.39
      ],
      [
       5.93,
       74.19
      ],
      [
       6.25,
       73.98
      ],
      [
       6.58,
       73.78
      ],
      [
       6.9,
       73.57
      ],
      [
       7.22,
       73.37
      ],
      [
       7.55,
       73.17
      ],
      [
       7.87,
       72.97
      ],
      [
       8.2,
       72.77
      ],
      [
       8.53,
       72.57
      ],
      [
       8.85,
       72.37
      ],
      [
       9.18,
       72.18
      ],
      [
       9.51,
       71.98
      ],
      [
       9.84,
       71.79
      ],
      [
       10.17,
       71.59
      ],
      [
       10.5,
       71.4
      ],
      [
       10.83,
       71.21
      ],
      [
       11.16,
       71.02
      ],
      [
       11.49,
       70.83
      ],
      [
       11.83,
       70.64
      ],
      [
       12.16,
       70.45
      ],
      [
       12.49,
       70.26
      ],
      [
       12.83,
       70.08
      ],
      [
       13.16,
       69.89
      ],
      [
       13.5,
       69.71
      ],
      [
       13.83,
       69.53
      ],
      [
       14.17,
       69.35
      ],
      [
       14.5,
       69.16
      ],
      [
       14.84,
       68.98
      ],
      [
       15.18,
       68.81
      ],
      [
       15.52,
       68.63
      ],
      [
       15.86,
       68.45
      ],
      [
       16.2,
       68.28
      ],
      [
       16.54,
       68.1
      ],
      [
       16.88,
       67.93
      ],
      [
       17.22,
       67.75
      ],
      [
       17.56,
       67.58
      ],
      [
       17.9,
       67.41
      ],
      [
       18.24,
       67.24
      ],
      [
       18.59,
       67.07
      ],
      [
       18.93,
       66.91
      ],
      [
       19.27,
       66.74
      ],
      [
       19.62,
       66.57
      ],
      [
       19.96,
       66.41
      ],
      [
       20.31,
       66.25
      ],
      [
       9.22,
       42.73
      ],
      [
       8.81,
       42.92
      ],
      [
       8.39,
       43.12
      ],
      [
       7.98,
       43.32
      ],
      [
       7.56,
       43.52
      ],
      [
       7.15,
       43.72
      ],
      [
       6.74,
       43.93
      ],
      [
       6.33,
       44.13
      ],
      [
       5.91,
       44.34
      ],
      [
       5.5,
       44.54
      ],
      [
       5.09,
       44.75
      ],
      [
       4.68,
       44.96
      ],
      [
       4.27,
       45.17
      ],
      [
       3.87,
       45.38
      ],
      [
       3.46,
       45.59
      ],
      [
       3.05,
       45.81
      ],
      [
       2.65,
       46.02
      ],
      [
       2.24,
       46.24
      ],
      [
       1.84,
       46.46
      ],
      [
       1.43,
       46.67
      ],
      [
       1.03,
       46.89
      ],
      [
       0.62,
       47.12
      ],
      [
       0.22,
       47.34
      ],
      [
       0.0,
       47.46
      ]
     ]
    ]
   },
   {
    "name": "East Gate Majlis",
    "fullName": "East Gate Majlis",
    "key": "gate_e",
    "category": "Arrival",
    "area": 439.0,
    "pct": 2.9,
    "icon": "🚪",
    "desc": "Arrival majlis at the eastern horn, breaking through the berm",
    "token": "gold",
    "residual": false,
    "labelXY": [
     141.56,
     64.54
    ],
    "parts": [
     [
      [
       129.69,
       66.25
      ],
      [
       130.04,
       66.41
      ],
      [
       130.38,
       66.57
      ],
      [
       130.73,
       66.74
      ],
      [
       131.07,
       66.91
      ],
      [
       131.41,
       67.07
      ],
      [
       131.76,
       67.24
      ],
      [
       132.1,
       67.41
      ],
      [
       132.44,
       67.58
      ],
      [
       132.78,
       67.75
      ],
      [
       133.12,
       67.93
      ],
      [
       133.46,
       68.1
      ],
      [
       133.8,
       68.28
      ],
      [
       134.14,
       68.45
      ],
      [
       134.48,
       68.63
      ],
      [
       134.82,
       68.81
      ],
      [
       135.16,
       68.98
      ],
      [
       135.5,
       69.16
      ],
      [
       135.83,
       69.35
      ],
      [
       136.17,
       69.53
      ],
      [
       136.5,
       69.71
      ],
      [
       136.84,
       69.89
      ],
      [
       137.17,
       70.08
      ],
      [
       137.51,
       70.26
      ],
      [
       137.84,
       70.45
      ],
      [
       138.17,
       70.64
      ],
      [
       138.51,
       70.83
      ],
      [
       138.84,
       71.02
      ],
      [
       139.17,
       71.21
      ],
      [
       139.5,
       71.4
      ],
      [
       139.83,
       71.59
      ],
      [
       140.16,
       71.79
      ],
      [
       140.49,
       71.98
      ],
      [
       140.82,
       72.18
      ],
      [
       141.15,
       72.37
      ],
      [
       141.47,
       72.57
      ],
      [
       141.8,
       72.77
      ],
      [
       142.13,
       72.97
      ],
      [
       142.45,
       73.17
      ],
      [
       142.78,
       73.37
      ],
      [
       143.1,
       73.57
      ],
      [
       143.42,
       73.78
      ],
      [
       143.75,
       73.98
      ],
      [
       144.07,
       74.19
      ],
      [
       144.39,
       74.39
      ],
      [
       144.71,
       74.6
      ],
      [
       145.03,
       74.81
      ],
      [
       145.35,
       75.02
      ],
      [
       145.67,
       75.23
      ],
      [
       145.99,
       75.44
      ],
      [
       146.31,
       75.65
      ],
      [
       146.63,
       75.86
      ],
      [
       146.94,
       76.08
      ],
      [
       147.26,
       76.29
      ],
      [
       147.57,
       76.51
      ],
      [
       147.89,
       76.73
      ],
      [
       148.2,
       76.94
      ],
      [
       148.52,
       77.16
      ],
      [
       148.83,
       77.38
      ],
      [
       149.14,
       77.6
      ],
      [
       149.45,
       77.82
      ],
      [
       149.76,
       78.05
      ],
      [
       150.0,
       78.22
      ],
      [
       150.0,
       47.46
      ],
      [
       149.78,
       47.34
      ],
      [
       149.38,
       47.12
      ],
      [
       148.97,
       46.89
      ],
      [
       148.57,
       46.67
      ],
      [
       148.16,
       46.46
      ],
      [
       147.76,
       46.24
      ],
      [
       147.35,
       46.02
      ],
      [
       146.95,
       45.81
      ],
      [
       146.54,
       45.59
      ],
      [
       146.13,
       45.38
      ],
      [
       145.73,
       45.17
      ],
      [
       145.32,
       44.96
      ],
      [
       144.91,
       44.75
      ],
      [
       144.5,
       44.54
      ],
      [
       144.09,
       44.34
      ],
      [
       143.67,
       44.13
      ],
      [
       143.26,
       43.93
      ],
      [
       142.85,
       43.72
      ],
      [
       142.44,
       43.52
      ],
      [
       142.02,
       43.32
      ],
      [
       141.61,
       43.12
      ],
      [
       141.19,
       42.92
      ],
      [
       140.78,
       42.73
      ]
     ]
    ]
   },
   {
    "name": "Al Nakhil — the Oasis Basin",
    "fullName": "Al Nakhil — the Oasis Basin",
    "key": "basin",
    "category": "Green",
    "area": 1139.5,
    "pct": 7.6,
    "icon": "🌴",
    "desc": "Sunken crescent palm court fed by the falaj; the park's heart",
    "token": "teal",
    "residual": false,
    "labelXY": [
     75.0,
     63.0
    ],
    "parts": [
     [
      [
       51.66,
       76.03
      ],
      [
       52.39,
       75.88
      ],
      [
       53.12,
       75.72
      ],
      [
       53.86,
       75.58
      ],
      [
       54.59,
       75.43
      ],
      [
       55.32,
       75.3
      ],
      [
       56.06,
       75.16
      ],
      [
       56.79,
       75.03
      ],
      [
       57.53,
       74.91
      ],
      [
       58.27,
       74.8
      ],
      [
       59.01,
       74.68
      ],
      [
       59.74,
       74.58
      ],
      [
       60.48,
       74.47
      ],
      [
       61.22,
       74.38
      ],
      [
       61.96,
       74.28
      ],
      [
       62.71,
       74.2
      ],
      [
       63.45,
       74.12
      ],
      [
       64.19,
       74.04
      ],
      [
       64.93,
       73.97
      ],
      [
       65.68,
       73.9
      ],
      [
       66.42,
       73.84
      ],
      [
       67.17,
       73.78
      ],
      [
       67.91,
       73.73
      ],
      [
       68.66,
       73.69
      ],
      [
       69.4,
       73.64
      ],
      [
       70.15,
       73.61
      ],
      [
       70.89,
       73.58
      ],
      [
       71.64,
       73.55
      ],
      [
       72.39,
       73.53
      ],
      [
       73.13,
       73.52
      ],
      [
       73.88,
       73.51
      ],
      [
       74.63,
       73.5
      ],
      [
       75.37,
       73.5
      ],
      [
       76.12,
       73.51
      ],
      [
       76.87,
       73.52
      ],
      [
       77.61,
       73.53
      ],
      [
       78.36,
       73.55
      ],
      [
       79.11,
       73.58
      ],
      [
       79.85,
       73.61
      ],
      [
       80.6,
       73.64
      ],
      [
       81.34,
       73.69
      ],
      [
       82.09,
       73.73
      ],
      [
       82.83,
       73.78
      ],
      [
       83.58,
       73.84
      ],
      [
       84.32,
       73.9
      ],
      [
       85.07,
       73.97
      ],
      [
       85.81,
       74.04
      ],
      [
       86.55,
       74.12
      ],
      [
       87.29,
       74.2
      ],
      [
       88.04,
       74.28
      ],
      [
       88.78,
       74.38
      ],
      [
       89.52,
       74.47
      ],
      [
       90.26,
       74.58
      ],
      [
       90.99,
       74.68
      ],
      [
       91.73,
       74.8
      ],
      [
       92.47,
       74.91
      ],
      [
       93.21,
       75.03
      ],
      [
       93.94,
       75.16
      ],
      [
       94.68,
       75.3
      ],
      [
       95.41,
       75.43
      ],
      [
       96.14,
       75.58
      ],
      [
       96.88,
       75.72
      ],
      [
       97.61,
       75.88
      ],
      [
       98.34,
       76.03
      ],
      [
       103.06,
       54.55
      ],
      [
       102.18,
       54.36
      ],
      [
       101.3,
       54.17
      ],
      [
       100.42,
       54.0
      ],
      [
       99.54,
       53.82
      ],
      [
       98.66,
       53.66
      ],
      [
       97.77,
       53.5
      ],
      [
       96.89,
       53.35
      ],
      [
       96.0,
       53.2
      ],
      [
       95.12,
       53.06
      ],
      [
       94.23,
       52.92
      ],
      [
       93.34,
       52.79
      ],
      [
       92.45,
       52.67
      ],
      [
       91.56,
       52.55
      ],
      [
       90.67,
       52.44
      ],
      [
       89.78,
       52.34
      ],
      [
       88.89,
       52.24
      ],
      [
       88.0,
       52.15
      ],
      [
       87.1,
       52.06
      ],
      [
       86.21,
       51.98
      ],
      [
       85.31,
       51.91
      ],
      [
       84.42,
       51.84
      ],
      [
       83.52,
       51.78
      ],
      [
       82.63,
       51.72
      ],
      [
       81.73,
       51.67
      ],
      [
       80.83,
       51.63
      ],
      [
       79.94,
       51.59
      ],
      [
       79.04,
       51.56
      ],
      [
       78.14,
       51.54
      ],
      [
       77.24,
       51.52
      ],
      [
       76.35,
       51.51
      ],
      [
       75.45,
       51.5
      ],
      [
       74.55,
       51.5
      ],
      [
       73.65,
       51.51
      ],
      [
       72.76,
       51.52
      ],
      [
       71.86,
       51.54
      ],
      [
       70.96,
       51.56
      ],
      [
       70.06,
       51.59
      ],
      [
       69.17,
       51.63
      ],
      [
       68.27,
       51.67
      ],
      [
       67.37,
       51.72
      ],
      [
       66.48,
       51.78
      ],
      [
       65.58,
       51.84
      ],
      [
       64.69,
       51.91
      ],
      [
       63.79,
       51.98
      ],
      [
       62.9,
       52.06
      ],
      [
       62.0,
       52.15
      ],
      [
       61.11,
       52.24
      ],
      [
       60.22,
       52.34
      ],
      [
       59.33,
       52.44
      ],
      [
       58.44,
       52.55
      ],
      [
       57.55,
       52.67
      ],
      [
       56.66,
       52.79
      ],
      [
       55.77,
       52.92
      ],
      [
       54.88,
       53.06
      ],
      [
       54.0,
       53.2
      ],
      [
       53.11,
       53.35
      ],
      [
       52.23,
       53.5
      ],
      [
       51.34,
       53.66
      ],
      [
       50.46,
       53.82
      ],
      [
       49.58,
       54.0
      ],
      [
       48.7,
       54.17
      ],
      [
       47.82,
       54.36
      ],
      [
       46.94,
       54.55
      ]
     ]
    ]
   },
   {
    "name": "Quiet Contemplation Garden",
    "fullName": "Quiet Contemplation Garden",
    "key": "quiet",
    "category": "Passive",
    "area": 707.5,
    "pct": 4.7,
    "icon": "🧘",
    "desc": "The deepest pocket of the hollow, screened behind the basin",
    "token": "purple",
    "residual": false,
    "labelXY": [
     75.0,
     85.0
    ],
    "parts": [
     [
      [
       55.61,
       94.0
      ],
      [
       94.39,
       94.0
      ],
      [
       97.69,
       78.96
      ],
      [
       96.98,
       78.81
      ],
      [
       96.27,
       78.66
      ],
      [
       95.56,
       78.52
      ],
      [
       94.85,
       78.38
      ],
      [
       94.13,
       78.25
      ],
      [
       93.42,
       78.12
      ],
      [
       92.7,
       77.99
      ],
      [
       91.99,
       77.87
      ],
      [
       91.27,
       77.76
      ],
      [
       90.55,
       77.65
      ],
      [
       89.84,
       77.55
      ],
      [
       89.12,
       77.45
      ],
      [
       88.4,
       77.35
      ],
      [
       87.68,
       77.26
      ],
      [
       86.95,
       77.18
      ],
      [
       86.23,
       77.1
      ],
      [
       85.51,
       77.02
      ],
      [
       84.79,
       76.95
      ],
      [
       84.06,
       76.89
      ],
      [
       83.34,
       76.83
      ],
      [
       82.62,
       76.77
      ],
      [
       81.89,
       76.72
      ],
      [
       81.17,
       76.68
      ],
      [
       80.44,
       76.64
      ],
      [
       79.72,
       76.61
      ],
      [
       78.99,
       76.58
      ],
      [
       78.27,
       76.55
      ],
      [
       77.54,
       76.53
      ],
      [
       76.82,
       76.52
      ],
      [
       76.09,
       76.51
      ],
      [
       75.36,
       76.5
      ],
      [
       74.64,
       76.5
      ],
      [
       73.91,
       76.51
      ],
      [
       73.18,
       76.52
      ],
      [
       72.46,
       76.53
      ],
      [
       71.73,
       76.55
      ],
      [
       71.01,
       76.58
      ],
      [
       70.28,
       76.61
      ],
      [
       69.56,
       76.64
      ],
      [
       68.83,
       76.68
      ],
      [
       68.11,
       76.72
      ],
      [
       67.38,
       76.77
      ],
      [
       66.66,
       76.83
      ],
      [
       65.94,
       76.89
      ],
      [
       65.21,
       76.95
      ],
      [
       64.49,
       77.02
      ],
      [
       63.77,
       77.1
      ],
      [
       63.05,
       77.18
      ],
      [
       62.32,
       77.26
      ],
      [
       61.6,
       77.35
      ],
      [
       60.88,
       77.45
      ],
      [
       60.16,
       77.55
      ],
      [
       59.45,
       77.65
      ],
      [
       58.73,
       77.76
      ],
      [
       58.01,
       77.87
      ],
      [
       57.3,
       77.99
      ],
      [
       56.58,
       78.12
      ],
      [
       55.87,
       78.25
      ],
      [
       55.15,
       78.38
      ],
      [
       54.44,
       78.52
      ],
      [
       53.73,
       78.66
      ],
      [
       53.02,
       78.81
      ],
      [
       52.31,
       78.96
      ]
     ]
    ]
   },
   {
    "name": "Children's Dune Play",
    "fullName": "Children's Dune Play",
    "key": "play",
    "category": "Active",
    "area": 1267.3,
    "pct": 8.4,
    "icon": "🛝",
    "desc": "Modelled play dunes in the crescent's western shadow",
    "token": "red",
    "residual": false,
    "labelXY": [
     38.13,
     75.17
    ],
    "parts": [
     [
      [
       34.53,
       94.0
      ],
      [
       53.64,
       94.0
      ],
      [
       44.24,
       55.17
      ],
      [
       43.85,
       55.27
      ],
      [
       43.46,
       55.36
      ],
      [
       43.07,
       55.46
      ],
      [
       42.69,
       55.56
      ],
      [
       42.3,
       55.66
      ],
      [
       41.91,
       55.76
      ],
      [
       41.53,
       55.86
      ],
      [
       41.14,
       55.96
      ],
      [
       40.76,
       56.06
      ],
      [
       40.37,
       56.17
      ],
      [
       39.99,
       56.28
      ],
      [
       39.6,
       56.38
      ],
      [
       39.22,
       56.49
      ],
      [
       38.83,
       56.6
      ],
      [
       38.45,
       56.71
      ],
      [
       38.07,
       56.83
      ],
      [
       37.68,
       56.94
      ],
      [
       37.3,
       57.05
      ],
      [
       36.92,
       57.17
      ],
      [
       36.54,
       57.29
      ],
      [
       36.15,
       57.4
      ],
      [
       35.77,
       57.52
      ],
      [
       35.39,
       57.64
      ],
      [
       35.01,
       57.76
      ],
      [
       34.63,
       57.89
      ],
      [
       34.25,
       58.01
      ],
      [
       33.87,
       58.14
      ],
      [
       33.49,
       58.26
      ],
      [
       33.12,
       58.39
      ],
      [
       32.74,
       58.52
      ],
      [
       32.36,
       58.65
      ],
      [
       31.98,
       58.78
      ],
      [
       31.61,
       58.91
      ],
      [
       31.23,
       59.04
      ],
      [
       30.85,
       59.18
      ],
      [
       30.48,
       59.31
      ],
      [
       30.1,
       59.45
      ],
      [
       29.73,
       59.59
      ],
      [
       29.35,
       59.73
      ],
      [
       28.98,
       59.87
      ],
      [
       28.61,
       60.01
      ],
      [
       28.23,
       60.15
      ],
      [
       27.86,
       60.29
      ],
      [
       27.49,
       60.44
      ],
      [
       27.12,
       60.58
      ],
      [
       26.74,
       60.73
      ],
      [
       26.37,
       60.88
      ],
      [
       26.0,
       61.03
      ],
      [
       25.63,
       61.18
      ],
      [
       25.26,
       61.33
      ],
      [
       24.89,
       61.48
      ],
      [
       24.53,
       61.64
      ],
      [
       24.16,
       61.79
      ],
      [
       23.79,
       61.95
      ],
      [
       23.42,
       62.1
      ],
      [
       23.06,
       62.26
      ],
      [
       22.69,
       62.42
      ],
      [
       22.32,
       62.58
      ],
      [
       21.96,
       62.74
      ],
      [
       21.59,
       62.9
      ],
      [
       21.23,
       63.07
      ],
      [
       20.87,
       63.23
      ],
      [
       20.5,
       63.4
      ]
     ],
     [
      [
       6.0,
       94.0
      ],
      [
       32.24,
       94.0
      ],
      [
       19.73,
       68.18
      ],
      [
       19.12,
       68.48
      ],
      [
       18.5,
       68.79
      ],
      [
       17.89,
       69.1
      ],
      [
       17.28,
       69.41
      ],
      [
       16.67,
       69.72
      ],
      [
       16.06,
       70.04
      ],
      [
       15.45,
       70.36
      ],
      [
       14.85,
       70.68
      ],
      [
       14.24,
       71.01
      ],
      [
       13.64,
       71.34
      ],
      [
       13.04,
       71.67
      ],
      [
       12.45,
       72.01
      ],
      [
       11.85,
       72.35
      ],
      [
       11.26,
       72.7
      ],
      [
       10.66,
       73.04
      ],
      [
       10.07,
       73.39
      ],
      [
       9.49,
       73.74
      ],
      [
       8.9,
       74.1
      ],
      [
       8.31,
       74.46
      ],
      [
       7.73,
       74.82
      ],
      [
       7.15,
       75.19
      ],
      [
       6.57,
       75.56
      ],
      [
       6.0,
       75.93
      ]
     ]
    ]
   },
   {
    "name": "Family Picnic Grove",
    "fullName": "Family Picnic Grove",
    "key": "picnic",
    "category": "Passive",
    "area": 1267.3,
    "pct": 8.4,
    "icon": "🧺",
    "desc": "Shaded lawn terraces in the crescent's eastern shadow",
    "token": "lime",
    "residual": false,
    "labelXY": [
     111.87,
     75.17
    ],
    "parts": [
     [
      [
       96.36,
       94.0
      ],
      [
       115.47,
       94.0
      ],
      [
       129.5,
       63.4
      ],
      [
       129.13,
       63.23
      ],
      [
       128.77,
       63.07
      ],
      [
       128.41,
       62.9
      ],
      [
       128.04,
       62.74
      ],
      [
       127.68,
       62.58
      ],
      [
       127.31,
       62.42
      ],
      [
       126.94,
       62.26
      ],
      [
       126.58,
       62.1
      ],
      [
       126.21,
       61.95
      ],
      [
       125.84,
       61.79
      ],
      [
       125.47,
       61.64
      ],
      [
       125.11,
       61.48
      ],
      [
       124.74,
       61.33
      ],
      [
       124.37,
       61.18
      ],
      [
       124.0,
       61.03
      ],
      [
       123.63,
       60.88
      ],
      [
       123.26,
       60.73
      ],
      [
       122.88,
       60.58
      ],
      [
       122.51,
       60.44
      ],
      [
       122.14,
       60.29
      ],
      [
       121.77,
       60.15
      ],
      [
       121.39,
       60.01
      ],
      [
       121.02,
       59.87
      ],
      [
       120.65,
       59.73
      ],
      [
       120.27,
       59.59
      ],
      [
       119.9,
       59.45
      ],
      [
       119.52,
       59.31
      ],
      [
       119.15,
       59.18
      ],
      [
       118.77,
       59.04
      ],
      [
       118.39,
       58.91
      ],
      [
       118.02,
       58.78
      ],
      [
       117.64,
       58.65
      ],
      [
       117.26,
       58.52
      ],
      [
       116.88,
       58.39
      ],
      [
       116.51,
       58.26
      ],
      [
       116.13,
       58.14
      ],
      [
       115.75,
       58.01
      ],
      [
       115.37,
       57.89
      ],
      [
       114.99,
       57.76
      ],
      [
       114.61,
       57.64
      ],
      [
       114.23,
       57.52
      ],
      [
       113.85,
       57.4
      ],
      [
       113.46,
       57.29
      ],
      [
       113.08,
       57.17
      ],
      [
       112.7,
       57.05
      ],
      [
       112.32,
       56.94
      ],
      [
       111.93,
       56.83
      ],
      [
       111.55,
       56.71
      ],
      [
       111.17,
       56.6
      ],
      [
       110.78,
       56.49
      ],
      [
       110.4,
       56.38
      ],
      [
       110.01,
       56.28
      ],
      [
       109.63,
       56.17
      ],
      [
       109.24,
       56.06
      ],
      [
       108.86,
       55.96
      ],
      [
       108.47,
       55.86
      ],
      [
       108.09,
       55.76
      ],
      [
       107.7,
       55.66
      ],
      [
       107.31,
       55.56
      ],
      [
       106.93,
       55.46
      ],
      [
       106.54,
       55.36
      ],
      [
       106.15,
       55.27
      ],
      [
       105.76,
       55.17
      ]
     ],
     [
      [
       117.76,
       94.0
      ],
      [
       144.0,
       94.0
      ],
      [
       144.0,
       75.93
      ],
      [
       143.43,
       75.56
      ],
      [
       142.85,
       75.19
      ],
      [
       142.27,
       74.82
      ],
      [
       141.69,
       74.46
      ],
      [
       141.1,
       74.1
      ],
      [
       140.51,
       73.74
      ],
      [
       139.93,
       73.39
      ],
      [
       139.34,
       73.04
      ],
      [
       138.74,
       72.7
      ],
      [
       138.15,
       72.35
      ],
      [
       137.55,
       72.01
      ],
      [
       136.96,
       71.67
      ],
      [
       136.36,
       71.34
      ],
      [
       135.76,
       71.01
      ],
      [
       135.15,
       70.68
      ],
      [
       134.55,
       70.36
      ],
      [
       133.94,
       70.04
      ],
      [
       133.33,
       69.72
      ],
      [
       132.72,
       69.41
      ],
      [
       132.11,
       69.1
      ],
      [
       131.5,
       68.79
      ],
      [
       130.88,
       68.48
      ],
      [
       130.27,
       68.18
      ]
     ]
    ]
   },
   {
    "name": "Outdoor Fitness Terrace",
    "fullName": "Outdoor Fitness Terrace",
    "key": "fitness",
    "category": "Active",
    "area": 908.5,
    "pct": 6.1,
    "icon": "🏋️",
    "desc": "Calisthenics terraces stepped into the southern berm",
    "token": "orange",
    "residual": false,
    "labelXY": [
     17.8,
     25.09
    ],
    "parts": [
     [
      [
       6.0,
       6.0
      ],
      [
       6.0,
       31.77
      ],
      [
       11.75,
       44.31
      ],
      [
       12.13,
       44.14
      ],
      [
       12.52,
       43.96
      ],
      [
       12.9,
       43.79
      ],
      [
       13.29,
       43.62
      ],
      [
       13.67,
       43.45
      ],
      [
       14.06,
       43.28
      ],
      [
       14.44,
       43.11
      ],
      [
       14.83,
       42.94
      ],
      [
       15.22,
       42.77
      ],
      [
       15.6,
       42.61
      ],
      [
       15.99,
       42.44
      ],
      [
       16.38,
       42.28
      ],
      [
       16.77,
       42.12
      ],
      [
       17.16,
       41.96
      ],
      [
       17.55,
       41.8
      ],
      [
       17.94,
       41.64
      ],
      [
       18.33,
       41.48
      ],
      [
       18.72,
       41.32
      ],
      [
       19.11,
       41.17
      ],
      [
       19.5,
       41.01
      ],
      [
       19.9,
       40.86
      ],
      [
       20.29,
       40.71
      ],
      [
       20.68,
       40.55
      ],
      [
       21.08,
       40.4
      ],
      [
       21.47,
       40.25
      ],
      [
       21.87,
       40.11
      ],
      [
       22.26,
       39.96
      ],
      [
       22.66,
       39.81
      ],
      [
       23.05,
       39.67
      ],
      [
       23.45,
       39.52
      ],
      [
       23.84,
       39.38
      ],
      [
       24.24,
       39.24
      ],
      [
       24.64,
       39.1
      ],
      [
       25.04,
       38.96
      ],
      [
       25.43,
       38.82
      ],
      [
       25.83,
       38.69
      ],
      [
       26.23,
       38.55
      ],
      [
       26.63,
       38.41
      ],
      [
       27.03,
       38.28
      ],
      [
       27.43,
       38.15
      ],
      [
       27.83,
       38.02
      ],
      [
       28.23,
       37.89
      ],
      [
       28.63,
       37.76
      ],
      [
       29.04,
       37.63
      ],
      [
       29.44,
       37.5
      ],
      [
       29.84,
       37.38
      ],
      [
       30.24,
       37.25
      ],
      [
       30.64,
       37.13
      ],
      [
       31.05,
       37.0
      ],
      [
       31.45,
       36.88
      ],
      [
       31.86,
       36.76
      ],
      [
       32.26,
       36.64
      ],
      [
       32.66,
       36.53
      ],
      [
       33.07,
       36.41
      ],
      [
       33.47,
       36.29
      ],
      [
       33.88,
       36.18
      ],
      [
       34.29,
       36.06
      ],
      [
       34.69,
       35.95
      ],
      [
       35.1,
       35.84
      ],
      [
       35.5,
       35.73
      ],
      [
       35.91,
       35.62
      ],
      [
       36.32,
       35.51
      ],
      [
       36.73,
       35.41
      ],
      [
       29.06,
       6.0
      ]
     ],
     [
      [
       6.0,
       42.62
      ],
      [
       6.33,
       42.45
      ],
      [
       7.09,
       42.08
      ],
      [
       6.0,
       39.84
      ]
     ]
    ]
   },
   {
    "name": "Native Planting / Biodiversity Wadi",
    "fullName": "Native Planting / Biodiversity Wadi",
    "key": "wadi",
    "category": "Green",
    "area": 893.8,
    "pct": 6.0,
    "icon": "🌾",
    "desc": "Dry watercourse of native species; habitat and stormwater sink",
    "token": "green",
    "residual": false,
    "labelXY": [
     53.17,
     16.43
    ],
    "parts": [
     [
      [
       33.04,
       6.0
      ],
      [
       39.85,
       34.63
      ],
      [
       40.34,
       34.51
      ],
      [
       40.82,
       34.4
      ],
      [
       41.3,
       34.29
      ],
      [
       41.78,
       34.18
      ],
      [
       42.27,
       34.07
      ],
      [
       42.75,
       33.97
      ],
      [
       43.24,
       33.86
      ],
      [
       43.72,
       33.76
      ],
      [
       44.21,
       33.66
      ],
      [
       44.69,
       33.56
      ],
      [
       45.18,
       33.46
      ],
      [
       45.66,
       33.36
      ],
      [
       46.15,
       33.27
      ],
      [
       46.63,
       33.17
      ],
      [
       47.12,
       33.08
      ],
      [
       47.61,
       32.99
      ],
      [
       48.1,
       32.9
      ],
      [
       48.58,
       32.82
      ],
      [
       49.07,
       32.73
      ],
      [
       49.56,
       32.65
      ],
      [
       50.05,
       32.57
      ],
      [
       50.54,
       32.48
      ],
      [
       51.03,
       32.41
      ],
      [
       51.52,
       32.33
      ],
      [
       52.01,
       32.25
      ],
      [
       52.49,
       32.18
      ],
      [
       52.98,
       32.11
      ],
      [
       53.48,
       32.03
      ],
      [
       53.97,
       31.96
      ],
      [
       54.46,
       31.9
      ],
      [
       54.95,
       31.83
      ],
      [
       55.44,
       31.77
      ],
      [
       55.93,
       31.7
      ],
      [
       56.42,
       31.64
      ],
      [
       56.91,
       31.58
      ],
      [
       57.4,
       31.52
      ],
      [
       57.9,
       31.47
      ],
      [
       58.39,
       31.41
      ],
      [
       58.88,
       31.36
      ],
      [
       59.37,
       31.31
      ],
      [
       59.87,
       31.26
      ],
      [
       60.36,
       31.21
      ],
      [
       60.85,
       31.16
      ],
      [
       61.35,
       31.12
      ],
      [
       61.84,
       31.07
      ],
      [
       62.33,
       31.03
      ],
      [
       62.83,
       30.99
      ],
      [
       63.32,
       30.95
      ],
      [
       63.82,
       30.91
      ],
      [
       64.31,
       30.88
      ],
      [
       64.8,
       30.84
      ],
      [
       65.3,
       30.81
      ],
      [
       65.79,
       30.78
      ],
      [
       66.29,
       30.75
      ],
      [
       66.78,
       30.72
      ],
      [
       67.28,
       30.7
      ],
      [
       67.77,
       30.67
      ],
      [
       68.27,
       30.65
      ],
      [
       68.76,
       30.63
      ],
      [
       69.26,
       30.61
      ],
      [
       69.75,
       30.59
      ],
      [
       70.25,
       30.57
      ],
      [
       70.74,
       30.56
      ],
      [
       70.05,
       6.0
      ]
     ]
    ]
   },
   {
    "name": "Community Plaza & Event Lawn",
    "fullName": "Community Plaza & Event Lawn",
    "key": "plaza",
    "category": "Social",
    "area": 787.5,
    "pct": 5.2,
    "icon": "🎪",
    "desc": "Evening events, addressing the crescent's convex face",
    "token": "gold",
    "residual": false,
    "labelXY": [
     89.58,
     15.64
    ],
    "parts": [
     [
      [
       73.8,
       6.0
      ],
      [
       73.96,
       30.5
      ],
      [
       74.42,
       30.5
      ],
      [
       74.87,
       30.5
      ],
      [
       75.32,
       30.5
      ],
      [
       75.78,
       30.5
      ],
      [
       76.23,
       30.5
      ],
      [
       76.68,
       30.51
      ],
      [
       77.14,
       30.52
      ],
      [
       77.59,
       30.52
      ],
      [
       78.04,
       30.53
      ],
      [
       78.5,
       30.54
      ],
      [
       78.95,
       30.55
      ],
      [
       79.4,
       30.56
      ],
      [
       79.86,
       30.58
      ],
      [
       80.31,
       30.59
      ],
      [
       80.76,
       30.61
      ],
      [
       81.21,
       30.63
      ],
      [
       81.67,
       30.65
      ],
      [
       82.12,
       30.67
      ],
      [
       82.57,
       30.69
      ],
      [
       83.03,
       30.71
      ],
      [
       83.48,
       30.74
      ],
      [
       83.93,
       30.76
      ],
      [
       84.38,
       30.79
      ],
      [
       84.84,
       30.82
      ],
      [
       85.29,
       30.85
      ],
      [
       85.74,
       30.88
      ],
      [
       86.19,
       30.91
      ],
      [
       86.64,
       30.95
      ],
      [
       87.1,
       30.98
      ],
      [
       87.55,
       31.02
      ],
      [
       88.0,
       31.06
      ],
      [
       88.45,
       31.1
      ],
      [
       88.9,
       31.14
      ],
      [
       89.35,
       31.18
      ],
      [
       89.81,
       31.22
      ],
      [
       90.26,
       31.27
      ],
      [
       90.71,
       31.32
      ],
      [
       91.16,
       31.36
      ],
      [
       91.61,
       31.41
      ],
      [
       92.06,
       31.46
      ],
      [
       92.51,
       31.51
      ],
      [
       92.96,
       31.57
      ],
      [
       93.41,
       31.62
      ],
      [
       93.86,
       31.68
      ],
      [
       94.31,
       31.73
      ],
      [
       94.76,
       31.79
      ],
      [
       95.21,
       31.85
      ],
      [
       95.66,
       31.91
      ],
      [
       96.11,
       31.98
      ],
      [
       96.56,
       32.04
      ],
      [
       97.0,
       32.1
      ],
      [
       97.45,
       32.17
      ],
      [
       97.9,
       32.24
      ],
      [
       98.35,
       32.31
      ],
      [
       98.8,
       32.38
      ],
      [
       99.24,
       32.45
      ],
      [
       99.69,
       32.52
      ],
      [
       100.14,
       32.6
      ],
      [
       100.59,
       32.67
      ],
      [
       101.03,
       32.75
      ],
      [
       101.48,
       32.83
      ],
      [
       101.93,
       32.91
      ],
      [
       102.37,
       32.99
      ],
      [
       107.32,
       6.0
      ]
     ]
    ]
   },
   {
    "name": "Souk Kiosks & Services",
    "fullName": "Souk Kiosks & Services",
    "key": "souk",
    "category": "Commercial",
    "area": 417.0,
    "pct": 2.8,
    "icon": "🏪",
    "desc": "Small trading units on the sikka to the east gate",
    "token": "orange",
    "residual": false,
    "labelXY": [
     115.12,
     27.1
    ],
    "parts": [
     [
      [
       111.21,
       6.0
      ],
      [
       105.54,
       33.6
      ],
      [
       105.73,
       33.64
      ],
      [
       105.93,
       33.69
      ],
      [
       106.13,
       33.73
      ],
      [
       106.32,
       33.77
      ],
      [
       106.52,
       33.81
      ],
      [
       106.72,
       33.85
      ],
      [
       106.91,
       33.89
      ],
      [
       107.11,
       33.94
      ],
      [
       107.31,
       33.98
      ],
      [
       107.5,
       34.02
      ],
      [
       107.7,
       34.06
      ],
      [
       107.9,
       34.11
      ],
      [
       108.09,
       34.15
      ],
      [
       108.29,
       34.2
      ],
      [
       108.48,
       34.24
      ],
      [
       108.68,
       34.28
      ],
      [
       108.88,
       34.33
      ],
      [
       109.07,
       34.37
      ],
      [
       109.27,
       34.42
      ],
      [
       109.46,
       34.47
      ],
      [
       109.66,
       34.51
      ],
      [
       109.86,
       34.56
      ],
      [
       110.05,
       34.6
      ],
      [
       110.25,
       34.65
      ],
      [
       110.44,
       34.7
      ],
      [
       110.64,
       34.74
      ],
      [
       110.83,
       34.79
      ],
      [
       111.03,
       34.84
      ],
      [
       111.22,
       34.89
      ],
      [
       111.42,
       34.93
      ],
      [
       111.61,
       34.98
      ],
      [
       111.81,
       35.03
      ],
      [
       112.0,
       35.08
      ],
      [
       112.2,
       35.13
      ],
      [
       112.39,
       35.18
      ],
      [
       112.59,
       35.23
      ],
      [
       112.78,
       35.28
      ],
      [
       112.98,
       35.33
      ],
      [
       113.17,
       35.38
      ],
      [
       113.37,
       35.43
      ],
      [
       113.56,
       35.48
      ],
      [
       113.76,
       35.53
      ],
      [
       113.95,
       35.58
      ],
      [
       114.15,
       35.64
      ],
      [
       114.34,
       35.69
      ],
      [
       114.53,
       35.74
      ],
      [
       114.73,
       35.79
      ],
      [
       114.92,
       35.85
      ],
      [
       115.12,
       35.9
      ],
      [
       115.31,
       35.95
      ],
      [
       115.5,
       36.01
      ],
      [
       115.7,
       36.06
      ],
      [
       115.89,
       36.11
      ],
      [
       116.08,
       36.17
      ],
      [
       116.28,
       36.22
      ],
      [
       116.47,
       36.28
      ],
      [
       116.67,
       36.33
      ],
      [
       116.86,
       36.39
      ],
      [
       117.05,
       36.44
      ],
      [
       117.24,
       36.5
      ],
      [
       117.44,
       36.55
      ],
      [
       117.63,
       36.61
      ],
      [
       117.82,
       36.67
      ],
      [
       126.84,
       6.0
      ]
     ]
    ]
   },
   {
    "name": "Multipurpose Sports Lawn",
    "fullName": "Multipurpose Sports Lawn",
    "key": "sports",
    "category": "Active",
    "area": 630.0,
    "pct": 4.2,
    "icon": "⚽",
    "desc": "Open turf sized for five-a-side, in the south-east corner",
    "token": "green",
    "residual": false,
    "labelXY": [
     139.15,
     23.47
    ],
    "parts": [
     [
      [
       130.94,
       6.0
      ],
      [
       120.91,
       37.61
      ],
      [
       121.19,
       37.7
      ],
      [
       121.47,
       37.79
      ],
      [
       121.75,
       37.88
      ],
      [
       122.03,
       37.97
      ],
      [
       122.31,
       38.06
      ],
      [
       122.59,
       38.16
      ],
      [
       122.87,
       38.25
      ],
      [
       123.15,
       38.34
      ],
      [
       123.43,
       38.44
      ],
      [
       123.71,
       38.53
      ],
      [
       123.99,
       38.63
      ],
      [
       124.27,
       38.72
      ],
      [
       124.55,
       38.82
      ],
      [
       124.83,
       38.91
      ],
      [
       125.11,
       39.01
      ],
      [
       125.39,
       39.11
      ],
      [
       125.67,
       39.21
      ],
      [
       125.94,
       39.31
      ],
      [
       126.22,
       39.41
      ],
      [
       126.5,
       39.51
      ],
      [
       126.78,
       39.61
      ],
      [
       127.05,
       39.71
      ],
      [
       127.33,
       39.81
      ],
      [
       127.61,
       39.91
      ],
      [
       127.89,
       40.01
      ],
      [
       128.16,
       40.12
      ],
      [
       128.44,
       40.22
      ],
      [
       128.72,
       40.33
      ],
      [
       128.99,
       40.43
      ],
      [
       129.27,
       40.54
      ],
      [
       129.54,
       40.64
      ],
      [
       129.82,
       40.75
      ],
      [
       130.09,
       40.85
      ],
      [
       130.37,
       40.96
      ],
      [
       130.64,
       41.07
      ],
      [
       130.92,
       41.18
      ],
      [
       131.19,
       41.29
      ],
      [
       131.47,
       41.4
      ],
      [
       131.74,
       41.51
      ],
      [
       132.02,
       41.62
      ],
      [
       132.29,
       41.73
      ],
      [
       132.56,
       41.84
      ],
      [
       132.84,
       41.95
      ],
      [
       133.11,
       42.07
      ],
      [
       133.38,
       42.18
      ],
      [
       133.65,
       42.29
      ],
      [
       133.93,
       42.41
      ],
      [
       134.2,
       42.52
      ],
      [
       134.47,
       42.64
      ],
      [
       134.74,
       42.75
      ],
      [
       135.01,
       42.87
      ],
      [
       135.28,
       42.99
      ],
      [
       135.55,
       43.11
      ],
      [
       135.83,
       43.22
      ],
      [
       136.1,
       43.34
      ],
      [
       136.37,
       43.46
      ],
      [
       136.64,
       43.58
      ],
      [
       136.91,
       43.7
      ],
      [
       137.18,
       43.82
      ],
      [
       137.44,
       43.94
      ],
      [
       137.71,
       44.07
      ],
      [
       137.98,
       44.19
      ],
      [
       138.25,
       44.31
      ],
      [
       144.0,
       31.77
      ],
      [
       144.0,
       6.0
      ]
     ],
     [
      [
       144.0,
       39.84
      ],
      [
       142.91,
       42.08
      ],
      [
       143.67,
       42.45
      ],
      [
       144.0,
       42.62
      ]
     ]
    ]
   },
   {
    "name": "Al Kathib — the dune berm",
    "fullName": "Al Kathib — the dune berm",
    "key": "berm",
    "category": "Green_Buffer",
    "area": 1463.8,
    "pct": 9.8,
    "icon": "🏜️",
    "desc": "Planted earth berm against the roads; noise, glare and heat",
    "token": "lime",
    "residual": false,
    "labelXY": [
     112.0,
     1.75
    ],
    "parts": [
     [
      [
       0.0,
       0.0
      ],
      [
       150.0,
       0.0
      ],
      [
       150.0,
       3.5
      ],
      [
       0.0,
       3.5
      ]
     ],
     [
      [
       0.0,
       96.5
      ],
      [
       150.0,
       96.5
      ],
      [
       150.0,
       100.0
      ],
      [
       0.0,
       100.0
      ]
     ],
     [
      [
       0.0,
       3.5
      ],
      [
       3.5,
       3.5
      ],
      [
       3.5,
       44.34
      ],
      [
       0.0,
       44.34
      ]
     ],
     [
      [
       0.0,
       78.22
      ],
      [
       3.5,
       78.22
      ],
      [
       3.5,
       96.5
      ],
      [
       0.0,
       96.5
      ]
     ],
     [
      [
       146.5,
       3.5
      ],
      [
       150.0,
       3.5
      ],
      [
       150.0,
       44.34
      ],
      [
       146.5,
       44.34
      ]
     ],
     [
      [
       146.5,
       78.22
      ],
      [
       150.0,
       78.22
      ],
      [
       150.0,
       96.5
      ],
      [
       146.5,
       96.5
      ]
     ]
    ]
   },
   {
    "name": "Al Madar — the perimeter loop",
    "fullName": "Al Madar — the perimeter loop",
    "key": "loop",
    "category": "Circulation",
    "area": 985.6,
    "pct": 6.6,
    "icon": "🏃",
    "desc": "2.5 m running and walking circuit, shaded by the berm planting",
    "token": "blue",
    "residual": false,
    "labelXY": [
     38.0,
     4.75
    ],
    "parts": [
     [
      [
       3.5,
       3.5
      ],
      [
       146.5,
       3.5
      ],
      [
       146.5,
       6.0
      ],
      [
       3.5,
       6.0
      ]
     ],
     [
      [
       3.5,
       94.0
      ],
      [
       146.5,
       94.0
      ],
      [
       146.5,
       96.5
      ],
      [
       3.5,
       96.5
      ]
     ],
     [
      [
       3.5,
       6.0
      ],
      [
       6.0,
       6.0
      ],
      [
       6.0,
       44.34
      ],
      [
       3.5,
       44.34
      ]
     ],
     [
      [
       3.5,
       78.22
      ],
      [
       6.0,
       78.22
      ],
      [
       6.0,
       94.0
      ],
      [
       3.5,
       94.0
      ]
     ],
     [
      [
       144.0,
       6.0
      ],
      [
       146.5,
       6.0
      ],
      [
       146.5,
       44.34
      ],
      [
       144.0,
       44.34
      ]
     ],
     [
      [
       144.0,
       78.22
      ],
      [
       146.5,
       78.22
      ],
      [
       146.5,
       94.0
      ],
      [
       144.0,
       94.0
      ]
     ]
    ]
   },
   {
    "name": "Al Sikkak — shaded alleys & setbacks",
    "fullName": "Al Sikkak — shaded alleys & setbacks",
    "key": "sikkak",
    "category": "Circulation",
    "area": 1414.0,
    "pct": 9.4,
    "icon": "🌀",
    "desc": "Radial alleys linking the crescent to the loop, and the setbacks",
    "token": "blue",
    "residual": true,
    "labelXY": [
     0,
     0
    ],
    "parts": [
     [
      [
       6.0,
       6.0
      ],
      [
       144.0,
       6.0
      ],
      [
       144.0,
       94.0
      ],
      [
       6.0,
       94.0
      ]
     ]
    ]
   }
  ],
  "byCategory": {
   "Active": 2805.8,
   "Arrival": 878.1,
   "Circulation": 3270.7,
   "Commercial": 417.0,
   "Green": 3297.1,
   "Green_Buffer": 1463.8,
   "Passive": 1974.8,
   "Social": 787.5,
   "Water": 105.2
  },
  "greenPct": 45.6,
  "source": "src/plan.py — every area is the shoelace area of the drawn polygon, so the schedule cannot disagree with the drawing."
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
  "sourcePlanting": "src/solar.py tree_positions() — each species is planted into the room the masterplan gives it, by rejection sampling inside its polygon.",
  "sourceCarbon": "../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/carbon_comfort_results.json",
  "nativeCount": 28
 },
 "performance": {
  "spineShadePct": 87.28,
  "totalDaylightHours": 4402,
  "zoneShade": [
   {
    "zone": "Crescent Shade Margin (N)",
    "pct": 91.0
   },
   {
    "zone": "Al Falaj — the water channel",
    "pct": 89.3
   },
   {
    "zone": "Al Mamsha — the Crescent Walk",
    "pct": 89.0
   },
   {
    "zone": "Crescent Shade Margin (S)",
    "pct": 76.5
   },
   {
    "zone": "West Gate Majlis",
    "pct": 63.8
   },
   {
    "zone": "Al Nakhil — the Oasis Basin",
    "pct": 46.1
   },
   {
    "zone": "East Gate Majlis",
    "pct": 45.8
   },
   {
    "zone": "Native Planting / Biodiversity Wadi",
    "pct": 45.2
   },
   {
    "zone": "Al Sikkak — shaded alleys & setbacks",
    "pct": 36.3
   },
   {
    "zone": "Quiet Contemplation Garden",
    "pct": 33.7
   },
   {
    "zone": "Children's Dune Play",
    "pct": 25.8
   },
   {
    "zone": "Outdoor Fitness Terrace",
    "pct": 19.0
   },
   {
    "zone": "Family Picnic Grove",
    "pct": 17.6
   },
   {
    "zone": "Community Plaza & Event Lawn",
    "pct": 10.7
   },
   {
    "zone": "Al Madar — the perimeter loop",
    "pct": 8.5
   },
   {
    "zone": "Multipurpose Sports Lawn",
    "pct": 7.9
   },
   {
    "zone": "Souk Kiosks & Services",
    "pct": 6.9
   },
   {
    "zone": "Al Kathib — the dune berm",
    "pct": 5.2
   }
  ],
  "coverage": {
   "_correction": "Recomputed from the ray-traced geometric model. The earlier version showed 100% spine coverage at all three key dates; that used a narrower single-moment check than the full-width walkway occlusion model this file now reports.",
   "Summer Solstice - Noon": 100.0,
   "Winter Solstice - Noon": 100.0,
   "Equinox - Noon": 100.0,
   "shaded_spine_path_only": {
    "Summer Solstice - Noon": 100.0,
    "Winter Solstice - Noon": 100.0,
    "Equinox - Noon": 100.0
   }
  },
  "monthlySpineShade": [
   76.54,
   88.96,
   92.92,
   89.23,
   92.31,
   89.33,
   92.31,
   91.81,
   89.92,
   84.68,
   80.82,
   74.01
  ],
  "heatIndex": {
   "peakExposed": 56.8,
   "peakShaded": 48.7,
   "meanReduction": 7.13,
   "comfortableExposedPct": 44.5,
   "comfortableShadedPct": 64.6
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
   "source": "../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/monthly_water_demand.csv"
  },
  "recycledPct": 43.4,
  "sourceShade": "src/solar.py — geometric occlusion at every daylight hour, NREL SPA sun angles via pvlib.",
  "sourceCoverage": "../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/shade_coverage_results.json",
  "sourceWater": "../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/water_demand_results.json",
  "crescentShadePct": 87.28,
  "walkMeanShadePct": 88.5,
  "siteMeanShadePct": 34.1
 },
 "cost": {
  "budget": 35000000,
  "elemental": {
   "items": [
    {
     "element": "Al Hilal — the Crescent Canopy (gridshell + louvre)",
     "area": 2240,
     "rate": 2500.0,
     "cost": 5600330
    },
    {
     "element": "Al Kathib — the dune berm",
     "area": 1464,
     "rate": 100.0,
     "cost": 146384
    },
    {
     "element": "Al Sikkak — shaded alleys & setbacks",
     "area": 1414,
     "rate": 400.0,
     "cost": 565586
    },
    {
     "element": "Children's Dune Play",
     "area": 1267,
     "rate": 900.0,
     "cost": 1140581
    },
    {
     "element": "Family Picnic Grove",
     "area": 1267,
     "rate": 100.0,
     "cost": 126731
    },
    {
     "element": "Al Nakhil — the Oasis Basin",
     "area": 1140,
     "rate": 100.0,
     "cost": 113954
    },
    {
     "element": "Al Madar — the perimeter loop",
     "area": 986,
     "rate": 400.0,
     "cost": 394240
    },
    {
     "element": "Outdoor Fitness Terrace",
     "area": 908,
     "rate": 700.0,
     "cost": 635930
    },
    {
     "element": "Native Planting / Biodiversity Wadi",
     "area": 894,
     "rate": 100.0,
     "cost": 89379
    },
    {
     "element": "Al Mamsha — the Crescent Walk",
     "area": 871,
     "rate": 400.0,
     "cost": 348465
    },
    {
     "element": "Community Plaza & Event Lawn",
     "area": 787,
     "rate": 500.0,
     "cost": 393747
    },
    {
     "element": "Crescent Shade Margin (S)",
     "area": 715,
     "rate": 100.0,
     "cost": 71477
    },
    {
     "element": "Quiet Contemplation Garden",
     "area": 707,
     "rate": 100.0,
     "cost": 70747
    },
    {
     "element": "Multipurpose Sports Lawn",
     "area": 630,
     "rate": 130.0,
     "cost": 81901
    },
    {
     "element": "Crescent Shade Margin (N)",
     "area": 549,
     "rate": 100.0,
     "cost": 54897
    },
    {
     "element": "East Gate Majlis",
     "area": 439,
     "rate": 500.0,
     "cost": 219524
    },
    {
     "element": "West Gate Majlis",
     "area": 439,
     "rate": 500.0,
     "cost": 219524
    },
    {
     "element": "Souk Kiosks & Services",
     "area": 417,
     "rate": 4500.0,
     "cost": 1876411
    },
    {
     "element": "Al Falaj — the water channel",
     "area": 105,
     "rate": 100.0,
     "cost": 10523
    },
    {
     "element": "Canopy trees (108 × Ghaf/Neem/Ficus, supply + plant)",
     "area": "-",
     "rate": "3500/tree",
     "cost": 378000
    },
    {
     "element": "Site lighting (LED — crescent, sikkas, loop, bollards)",
     "area": "-",
     "rate": "% of works",
     "cost": 564225
    },
    {
     "element": "Irrigation network (drip / subsurface)",
     "area": "-",
     "rate": "% of works",
     "cost": 438842
    },
    {
     "element": "Smart infrastructure (sensors, digital wayfinding)",
     "area": "-",
     "rate": "% of works",
     "cost": 313458
    },
    {
     "element": "Preliminaries & enabling (10%)",
     "area": "-",
     "rate": "-",
     "cost": 1385486
    },
    {
     "element": "Design contingency (12%)",
     "area": "-",
     "rate": "-",
     "cost": 1662583
    },
    {
     "element": "Professional fees (8%)",
     "area": "-",
     "rate": "-",
     "cost": 1108388
    }
   ],
   "total": 18011313,
   "source": "data/raw/construction_unit_rates_aed.csv against the drawn areas in src/plan.py. Rates are Dubai landscape contractor quotations for 2025, not municipal tender pricing."
  },
  "capexPackage": {
   "items": [
    {
     "item": "Al Hilal — Crescent Canopy (ETFE + steel gridshell)",
     "cost": 4298154
    },
    {
     "item": "Civil Works, Paving & Drainage",
     "cost": 3888807
    },
    {
     "item": "Landscape, Planting & Soil Improvement",
     "cost": 3172447
    },
    {
     "item": "Contingency & Prelims (15%)",
     "cost": 2097909
    },
    {
     "item": "Electrical, LED & Smart Lighting",
     "cost": 1535055
    },
    {
     "item": "Water Features, Mist & Irrigation System",
     "cost": 1228044
    },
    {
     "item": "Outdoor Furniture, Fitness & Play",
     "cost": 972201
    },
    {
     "item": "Smart Tech, AV & Digital Wayfinding",
     "cost": 818696
    }
   ],
   "total": 18011313,
   "source": "The same money as the elemental take-off, grouped by trade package. Rescaled by 1.0000 when the redesign changed the measured areas; the split between packages is unchanged."
  },
  "opexPackage": {
   "items": [
    {
     "item": "Landscape Maintenance & Labour",
     "cost": 515523
    },
    {
     "item": "Capital Replacement Reserve (3%)",
     "cost": 423033
    },
    {
     "item": "Irrigation Water (DEWA)",
     "cost": 292635
    },
    {
     "item": "Electricity (Lighting & Systems)",
     "cost": 212274
    },
    {
     "item": "Events & Activation Programming",
     "cost": 136462
    },
    {
     "item": "Security & CCTV",
     "cost": 106137
    },
    {
     "item": "Smart System Maintenance",
     "cost": 90975
    },
    {
     "item": "Canopy Inspection & Cleaning",
     "cost": 72022
    },
    {
     "item": "Administrative & Insurance",
     "cost": 72022
    }
   ],
   "total": 1921083,
   "source": "../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/opex_breakdown.csv"
  },
  "om": {
   "items": [
    {
     "item": "Horticulture maintenance (6% of build cost)",
     "cost": 1080679,
     "basis": "ratio"
    },
    {
     "item": "Cleaning, waste & minor repairs (2% of build)",
     "cost": 360226,
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
   "total": 1921083.0,
   "pctOfBuild": 10.7,
   "tco10": 38344074.0,
   "waterTariff": 8.8,
   "annualWaterM3": 5702.0,
   "source": "../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/om_cost_results.json",
   "buildCost": 18011313
  },
  "headroom": 16988687,
  "budgetUsedPct": 51.5
 },
 "advanced": {
  "capexTotal": 18011313,
  "opexTotal": 1921083.0,
  "lcc": {
   "total_npv_cost_AED": 66358864,
   "total_npv_benefit_AED": 102753400,
   "npv_net_AED": 36394536,
   "irr_pct": 13.6,
   "simple_payback_years": 8,
   "sroi_ratio": 1.55,
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
     18011313,
     19976581,
     21987050,
     24043760,
     26147774,
     28300181,
     30502092,
     32754648,
     35059013,
     37416378,
     39827962,
     42295013,
     44818806,
     47400646,
     50041869,
     52743840,
     55507956,
     58335646,
     61228374,
     64187634,
     67214958,
     70311909,
     73480091,
     76721141,
     80036735,
     83428587,
     86898452,
     90448125,
     94079439,
     97794274,
     101594550
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
  "source": "../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/advanced_lcc_energy_carbon_results.json Cost side rebuilt from the redesigned take-off (AED 18,011,313) at 4% discount and 2.3% inflation over 30 years. Cost side rebuilt from the redesigned take-off (AED 18,011,313) at 4% discount and 2.3% inflation over 30 years."
 },
 "concepts": {
  "source": "src/config.py CRESCENT — the sweep table is in the file.",
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
    "name": "A — Falaj Al Safa (the crescent)",
    "idea": "A single arc carries the shade; every room in the park is struck off its centre, and a water channel runs its length.",
    "shade": "87.3% of daylight hours on the walk",
    "strength": "The route changes heading continuously, so some segment is always angled well against the sun. The hours in which the walk has no shade anywhere fall from 330 to 56.",
    "risk": "Concentrating the shade budget into one element means the open rooms stay hot. That is a deliberate position, not an oversight — see the site-wide mean.",
    "selected": true
   },
   {
    "name": "B — the straight spine (superseded)",
    "idea": "A straight east-west canopy through the middle of the site, with rectangular rooms packed either side.",
    "shade": "87.4% of daylight hours on the walk",
    "strength": "The highest mean coverage of any plan form tested. An east-west canopy is close to the optimum orientation for 25°N.",
    "risk": "One orientation. When a sun angle defeats it, it defeats the entire length at once and the walk has no shade anywhere — 330 hours a year of that.",
    "selected": false
   },
   {
    "name": "C — the closed loop",
    "idea": "A shaded circuit around the site rather than a route across it.",
    "shade": "79.1% of daylight hours on the walk",
    "strength": "A circuit is what people actually walk in a neighbourhood park.",
    "risk": "A loop forces half its length to run north-south, and a canopy over a north-south route only works when the sun is low in the east or west. It loses on every measure.",
    "selected": false
   }
  ],
  "rationale": "The three plan forms were not judged by eye. Each was run against the 8,760-hour solar model at the same fixed section, and scored on mean coverage, worst month, and the number of hours in which the walk offers no shade anywhere along it. The straight bar wins the first measure and loses the third badly; the loop loses all three. The crescent was adopted for the third measure, at a cost of about one point on the first — and the concept keeps the loop as Al Madar, an unshaded running circuit, because that is what a circuit is actually for."
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
     "Children's Dune Play",
     "Family Picnic Grove"
    ],
    "window": "15:00–18:00"
   },
   {
    "name": "Rashid, 68",
    "role": "Older resident",
    "icon": "🧓",
    "profile": "Daily evening walk; values continuous shade and frequent seating",
    "zones": [
     "Al Mamsha — the Crescent Walk",
     "Al Madar — the perimeter loop",
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
     "Outdoor Fitness Terrace"
    ],
    "window": "16:00–22:00"
   },
   {
    "name": "Mr. Al Farsi",
    "role": "Wheelchair user",
    "icon": "♿",
    "profile": "Weekly visit for fresh air and social contact; requires fully step-free routes",
    "zones": [
     "Al Mamsha — the Crescent Walk (step-free)",
     "Community Plaza & Event Lawn"
    ],
    "window": "Any"
   },
   {
    "name": "Fatima, 29",
    "role": "Fitness enthusiast",
    "icon": "🏃‍♀️",
    "profile": "Early-morning run before work, in the cooler comfort window",
    "zones": [
     "Al Madar — the perimeter loop",
     "Outdoor Fitness Terrace"
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
  "seasonal": "November–April is the comfort window: full-day use is expected across every room. May–October, midday use concentrates under the crescent and along its shaded margins, with the open lawns used early in the morning and after sunset. The crescent is shaded for 87.3% of the daylight year, not all of it — the 56 hours that have no shade anywhere are stated in the performance section rather than rounded away."
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
  "source": "../archive/phases/10_PHASE10_UPLOAD_DOCUMENTS/compilation_log.json"
 },
 "renders": [
  {
   "src": "assets/renders/dubai_futuristic_masterplan_aerial.jpg",
   "title": "Canopy and channel, aerial",
   "tag": "Phase 5 · Masterplan",
   "desc": "Sweeping dune-inspired parametric canopy, fluid terrazzo pathways, and integrated micro-oasis pockets.",
   "caption": "The gridshell and the falaj running together the length of the crescent, with the sikkas cutting radially out to the perimeter."
  },
  {
   "src": "assets/renders/dubai_futuristic_spine_interior.jpg",
   "title": "Al Mamsha — the Crescent Walk",
   "tag": "Phase 6 · Detailed Design",
   "desc": "Ultra-luxury marble walkway beneath a fluid parametric canopy with cooling mist rings and Ghaf groves.",
   "caption": "The 7 m walk under an 18 m shell. The overhang is what keeps the shadow on the path when the sun is low."
  },
  {
   "src": "assets/renders/masterplan_aerial_golden_hour.jpg",
   "title": "The crescent from the north-west",
   "tag": "Phase 5 · Masterplan",
   "desc": "Fluid biophilic architecture bathed in warm evening sunlight.",
   "caption": "The arc reads as one continuous element from horn to horn, with the Oasis Basin held in its concave side."
  },
  {
   "src": "assets/renders/spine_corridor_interior.jpg",
   "title": "Beneath Al Hilal — the perforated soffit",
   "tag": "Phase 6 · Detailed Design",
   "desc": "Curved timber and bronze louvers providing continuous thermal comfort.",
   "caption": "The mashrabiya rule at full size: light through, heat stopped. 12% direct-beam transmittance."
  },
  {
   "src": "assets/renders/eyelevel_spine_1784970552956.jpg",
   "title": "The walk in the shoulder season",
   "tag": "Phase 6 · Detailed Design",
   "desc": "Native Ghaf and Neem canopy trees integrated into the fluid shade structure.",
   "caption": "Late afternoon in spring and autumn is where the comfort gain concentrates, and where the activation strategy is aimed."
  },
  {
   "src": "assets/renders/night_plaza_render_1784970565232.jpg",
   "title": "The Community Plaza after dark",
   "tag": "Phase 8 · Activation",
   "desc": "Linear and edge-lit LED illumination creating a vibrant evening community destination.",
   "caption": "The convex side takes the uses that run in the evening, when its exposure stops being a liability."
  }
 ],
 "provenance": [
  {
   "key": "peak_temp",
   "label": "Peak monthly mean maximum temperature",
   "value": 42.1,
   "unit": "°C",
   "source": "../archive/phases/01_PHASE1_EXISTING_PARK/05_Climate_Analysis/outputs/dubai_monthly_climate_normals.csv",
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
   "source": "../archive/phases/01_PHASE1_EXISTING_PARK/05_Climate_Analysis/outputs/dubai_monthly_climate_normals.csv",
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
   "source": "../archive/phases/01_PHASE1_EXISTING_PARK/05_Climate_Analysis/outputs/dubai_monthly_climate_normals.csv",
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
   "source": "../archive/phases/01_PHASE1_EXISTING_PARK/05_Climate_Analysis/outputs/dubai_monthly_climate_normals.csv",
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
   "source": "../archive/phases/01_PHASE1_EXISTING_PARK/05_Climate_Analysis/outputs/dubai_monthly_climate_normals.csv",
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
   "source": "../archive/phases/01_PHASE1_EXISTING_PARK/05_Climate_Analysis/outputs/sun_hours_key_dates.csv",
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
   "source": "../archive/phases/01_PHASE1_EXISTING_PARK/06_Shadow_Analysis/outputs/shadow_length_table.csv",
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
   "source": "../archive/phases/01_PHASE1_EXISTING_PARK/13_Catchment_Demand_Analysis/outputs/catchment_demand_results.json",
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
   "source": "../archive/phases/01_PHASE1_EXISTING_PARK/13_Catchment_Demand_Analysis/outputs/catchment_demand_results.json",
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
   "source": "../archive/phases/02_PHASE2_PROBLEM_DEFINITION/outputs/problem_severity_scores.csv",
   "method": "Mean of Evidence, Impact, Reach and Urgency scored 1-5 against Phase 1 findings",
   "note": "P1 — Summer thermal discomfort (near-zero midday shade)",
   "refs": []
  },
  {
   "key": "site_area",
   "label": "Total site area",
   "value": 15000.0,
   "unit": "m²",
   "source": "../archive/phases/05_PHASE5_MASTERPLAN_DEVELOPMENT/outputs/zoning_area_schedule.json",
   "method": "Competition brief / Phase 5 masterplan geometry",
   "note": "Al Safa 2 Park, Dubai.",
   "refs": []
  },
  {
   "key": "zoned_area",
   "label": "Area allocated across the zoning schedule",
   "value": 15000.0,
   "unit": "m²",
   "source": "../archive/phases/05_PHASE5_MASTERPLAN_DEVELOPMENT/outputs/zoning_area_schedule.json",
   "method": "Sum of all 14 zone areas in the schedule",
   "note": "15,000 of 15,000 m² — the schedule is fully allocated.",
   "refs": []
  },
  {
   "key": "green_pct",
   "label": "Green / soft-landscape share of the site",
   "value": 45.6,
   "unit": "%",
   "source": "../archive/phases/05_PHASE5_MASTERPLAN_DEVELOPMENT/outputs/zoning_area_schedule.json",
   "method": "Green + Green_Buffer + Passive categories, divided by site area",
   "note": "Green, buffer, passive and water categories, measured from the drawn polygons.",
   "refs": []
  },
  {
   "key": "total_trees",
   "label": "Trees in the planting schedule",
   "value": 131,
   "unit": "trees",
   "source": "../archive/phases/06_PHASE6_DETAILED_DESIGN/outputs/planting_schedule.json",
   "method": "Phase 6 planting schedule, counted by species",
   "note": "",
   "refs": []
  },
  {
   "key": "carbon_seq",
   "label": "Annual carbon sequestration",
   "value": 2.1,
   "unit": "tCO₂e/yr",
   "source": "../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/carbon_comfort_results.json",
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
   "source": "../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/carbon_comfort_results.json",
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
   "source": "../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/carbon_comfort_results.json",
   "method": "Months below the 32°C Heat Index comfort threshold, shaded minus exposed",
   "note": "3 months in sun -> 6 months in shade.",
   "refs": [
    "nws-heat-index",
    "ncm"
   ]
  },
  {
   "key": "spine_shade",
   "label": "Annual shade coverage of the Crescent Walk",
   "value": 87.28,
   "unit": "%",
   "source": "../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/annual_shade_hours_results.json",
   "method": "Geometric occlusion of the 18 m gridshell and its 3 m southern louvre, evaluated at every daylight hour of the year with NREL SPA sun angles. An hour counts as shaded when at least half the walk width is covered.",
   "note": "87.3% of 4,402 daylight hours. Only 56 hours a year leave the walk with no shade anywhere along it; the straight canopy this replaced left 330.",
   "refs": []
  },
  {
   "key": "peak_heat_index",
   "label": "Peak exposed Heat Index",
   "value": 56.8,
   "unit": "°C",
   "source": "../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/thermal_comfort_heatindex.csv",
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
   "source": "../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/water_demand_results.json",
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
   "source": "../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/monthly_water_demand.csv",
   "method": "Sum of monthly recycled m³ divided by sum of monthly total demand",
   "note": "",
   "refs": []
  },
  {
   "key": "capex",
   "label": "Estimated construction cost",
   "value": 18011313,
   "unit": "AED",
   "source": "../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/cost_estimate_results.json",
   "method": "Elemental take-off: zone areas x sourced Dubai landscaping unit rates (upper bound of each range, plus contingency)",
   "note": "53% of the AED 35M brief budget, leaving AED 16.4M of headroom. These are VILLA / RESIDENTIAL landscaping benchmarks, not municipal tender prices. Public-park construction typically runs at the higher end or above these ranges once procurement and public specification are factored in. The model uses the upper bound of each sourced range plus explicit contingency, so the AED 18.6M figure is a conservative order-of-magnitude estimate — not a quantity-surveyed tender price. This caveat is in the source script's own header comment and is carried through here rather than smoothed away.",
   "refs": [
    "landscape-rates"
   ]
  },
  {
   "key": "opex",
   "label": "Annual operations & maintenance cost",
   "value": 1921083.0,
   "unit": "AED/yr",
   "source": "../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/om_cost_results.json",
   "method": "Computed irrigation cost at the real DEWA tariff plus ratio-based maintenance, electricity, cleaning and security",
   "note": "10.6% of build cost per year.",
   "refs": [
    "dewa-tariff"
   ]
  },
  {
   "key": "tco10",
   "label": "10-year total cost of ownership",
   "value": 37222143,
   "unit": "AED",
   "source": "../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/om_cost_results.json",
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
   "source": "../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/om_cost_results.json",
   "method": "DEWA published tariff schedule: AED 7.70/m³ (0-27m³ slab) + AED 1.10/m³ fuel surcharge",
   "note": "Applied to the computed 5,702 m³/yr demand.",
   "refs": [
    "dewa-tariff"
   ]
  },
  {
   "key": "npv_30yr",
   "label": "30-year net present value",
   "value": 36394536,
   "unit": "AED",
   "source": "../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/advanced_lcc_energy_carbon_results.json",
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
   "source": "../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/advanced_lcc_energy_carbon_results.json",
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
   "source": "../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/advanced_lcc_energy_carbon_results.json",
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
   "source": "../archive/phases/10_PHASE10_UPLOAD_DOCUMENTS/compilation_log.json",
   "method": "Phase 10 compilation log, counted by upload slot",
   "note": "Slots 10 and 12 are deliberately outstanding: the complete design report and the optional 60-second animation.",
   "refs": []
  }
 ],
 "audit": [
  {
   "name": "Zoning schedule closes on the site area",
   "ok": true,
   "detail": "Rooms and the alley residual sum to 15,000 m² against a site area of 15,000 m². The areas are the shoelace area of each drawn polygon, so this closes by construction rather than by reconciliation."
  },
  {
   "name": "No ground is claimed by two rooms",
   "ok": true,
   "detail": "Rooms are disjoint boxes in the crescent's polar frame, and that frame is injective — checked on the 1 m grid by tests/test_pipeline.py."
  },
  {
   "name": "The walk is shaded for most of the daylight year",
   "ok": true,
   "detail": "87.3% of 4,402 daylight hours have at least half the walk width in shadow."
  },
  {
   "name": "Site-wide shade is stated, not hidden",
   "ok": true,
   "detail": "Site-wide mean shade is 34.1%. This scheme concentrates its shade budget; the open rooms are hot and the submission says so."
  },
  {
   "name": "The 99.2% shade claim has been withdrawn",
   "ok": true,
   "detail": "An earlier version claimed 99.2% annual shade on a flat 9 m canopy over a 9 m walkway. It does not survive a geometric check and was withdrawn."
  },
  {
   "name": "Fabricated visuals have been withdrawn",
   "ok": true,
   "detail": "Three images presented invented data as measurement — a CFD dashboard, an NDVI analysis and a 'solar-optimised' canopy mesh. None had the source it claimed. See archive/withdrawn_visuals/README.md."
  },
  {
   "name": "Site boundary is assumed, not surveyed",
   "ok": false,
   "detail": "The 150 × 100 m rectangle is an assumption pending confirmation against the supplied DWG. Every area figure depends on it."
  }
 ],
 "sources": [
  "../archive/phases/01_PHASE1_EXISTING_PARK/05_Climate_Analysis/outputs/dubai_monthly_climate_normals.csv",
  "../archive/phases/01_PHASE1_EXISTING_PARK/05_Climate_Analysis/outputs/sun_hours_key_dates.csv",
  "../archive/phases/01_PHASE1_EXISTING_PARK/06_Shadow_Analysis/outputs/shadow_length_table.csv",
  "../archive/phases/01_PHASE1_EXISTING_PARK/13_Catchment_Demand_Analysis/outputs/catchment_demand_results.json",
  "../archive/phases/02_PHASE2_PROBLEM_DEFINITION/outputs/problem_severity_scores.csv",
  "../archive/phases/05_PHASE5_MASTERPLAN_DEVELOPMENT/outputs/zoning_area_schedule.json",
  "../archive/phases/06_PHASE6_DETAILED_DESIGN/outputs/planting_schedule.json",
  "../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/advanced_lcc_energy_carbon_results.json",
  "../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/annual_shade_hours_results.json",
  "../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/capex_breakdown.csv",
  "../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/carbon_comfort_results.json",
  "../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/cost_estimate_results.json",
  "../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/monthly_spine_shade_pct.csv",
  "../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/monthly_water_demand.csv",
  "../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/om_cost_results.json",
  "../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/opex_breakdown.csv",
  "../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/shade_coverage_results.json",
  "../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/thermal_comfort_heatindex.csv",
  "../archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/water_demand_results.json",
  "../archive/phases/10_PHASE10_UPLOAD_DOCUMENTS/compilation_log.json"
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
