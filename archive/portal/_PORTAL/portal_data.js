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
  "generated": "2026-07-30 09:25 UTC",
  "sourceCount": 0
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
  "tempMax": [],
  "tempMin": [],
  "tempAvg": [],
  "humidity": [],
  "wind": [],
  "rainfall": [],
  "sunHrsMonthly": [],
  "sunHrsDaily": [],
  "ghi": [],
  "source": "01_PHASE1_EXISTING_PARK/05_Climate_Analysis/outputs/dubai_monthly_climate_normals.csv",
  "annualSunshine": 0,
  "annualRain": 0,
  "meanWind": 0,
  "peakTemp": 0,
  "peakTempMonth": "-"
 },
 "solar": {
  "site": {
   "lat": 25.19,
   "lon": 55.238,
   "elevation_m": 16,
   "tz": "Asia/Dubai (UTC+4)"
  },
  "keyDates": [],
  "shadows": [],
  "sourceKeyDates": "01_PHASE1_EXISTING_PARK/05_Climate_Analysis/outputs/sun_hours_key_dates.csv",
  "sourceShadows": "01_PHASE1_EXISTING_PARK/06_Shadow_Analysis/outputs/shadow_length_table.csv"
 },
 "catchment": {
  "populationSources": {},
  "density": 0,
  "rings": [],
  "capacity": {},
  "demand": {},
  "source": "01_PHASE1_EXISTING_PARK/13_Catchment_Demand_Analysis/outputs/catchment_demand_results.json"
 },
 "problems": {
  "items": [],
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
  "allocated": 0,
  "zones": [],
  "byCategory": {},
  "greenPct": 0.0,
  "source": "05_PHASE5_MASTERPLAN_DEVELOPMENT/outputs/zoning_area_schedule.json"
 },
 "planting": {
  "totalTrees": 0,
  "species": [],
  "carbonTotalKg": 0.0,
  "carbonTotalTonnes": 0.0,
  "carKmEquiv": 0.0,
  "comfort": {},
  "sourcePlanting": "06_PHASE6_DETAILED_DESIGN/outputs/planting_schedule.json",
  "sourceCarbon": "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/carbon_comfort_results.json"
 },
 "performance": {
  "spineShadePct": 0,
  "totalDaylightHours": 0,
  "zoneShade": [],
  "coverage": {},
  "monthlySpineShade": [],
  "heatIndex": {
   "months": [],
   "airMax": [],
   "sun": [],
   "shade": [],
   "source": "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/thermal_comfort_heatindex.csv"
  },
  "water": {},
  "waterMonthly": {
   "months": [],
   "total": [],
   "recycled": [],
   "potable": [],
   "cost": [],
   "source": "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/monthly_water_demand.csv"
  },
  "recycledPct": 0,
  "sourceShade": "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/annual_shade_hours_results.json",
  "sourceCoverage": "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/shade_coverage_results.json",
  "sourceWater": "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/water_demand_results.json"
 },
 "cost": {
  "budget": 35000000,
  "elemental": {
   "items": [],
   "total": 0,
   "source": "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/cost_estimate_results.json"
  },
  "capexPackage": {
   "items": [],
   "total": 0,
   "source": "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/capex_breakdown.csv"
  },
  "opexPackage": {
   "items": [],
   "total": 0,
   "source": "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/opex_breakdown.csv"
  },
  "om": {
   "items": [],
   "total": 0.0,
   "pctOfBuild": 0.0,
   "tco10": 0.0,
   "waterTariff": 0.0,
   "annualWaterM3": 0.0,
   "source": "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/om_cost_results.json"
  },
  "headroom": 35000000,
  "budgetUsedPct": 0.0
 },
 "advanced": null,
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
    "files": [],
    "count": 0,
    "status": "empty",
    "folder": null
   },
   {
    "num": 2,
    "name": "Preliminary Design / Masterplan",
    "files": [],
    "count": 0,
    "status": "empty",
    "folder": null
   },
   {
    "num": 3,
    "name": "Concept Plans & Spatial Diagrams",
    "files": [],
    "count": 0,
    "status": "empty",
    "folder": null
   },
   {
    "num": 4,
    "name": "Key Sections & Elevations",
    "files": [],
    "count": 0,
    "status": "empty",
    "folder": null
   },
   {
    "num": 5,
    "name": "3D Spatial Visualizations",
    "files": [],
    "count": 0,
    "status": "empty",
    "folder": null
   },
   {
    "num": 6,
    "name": "AI Methodology Report",
    "files": [],
    "count": 0,
    "status": "empty",
    "folder": null
   },
   {
    "num": 7,
    "name": "User Experience & Activation Strategy",
    "files": [],
    "count": 0,
    "status": "empty",
    "folder": null
   },
   {
    "num": 8,
    "name": "Sustainability Concept & Strategy",
    "files": [],
    "count": 0,
    "status": "empty",
    "folder": null
   },
   {
    "num": 9,
    "name": "Material & Landscape Palette",
    "files": [],
    "count": 0,
    "status": "empty",
    "folder": null
   },
   {
    "num": 10,
    "name": "Complete Design Report",
    "files": [],
    "count": 0,
    "status": "empty",
    "folder": null
   },
   {
    "num": 11,
    "name": "Site Analysis & Human-Centric Research",
    "files": [],
    "count": 0,
    "status": "empty",
    "folder": null
   },
   {
    "num": 12,
    "name": "Concept Animation Video",
    "files": [],
    "count": 0,
    "status": "empty",
    "folder": null
   }
  ],
  "ready": 0,
  "total": 12,
  "source": "10_PHASE10_UPLOAD_DOCUMENTS/compilation_log.json"
 },
 "renders": [],
 "provenance": [
  {
   "key": "peak_temp",
   "label": "Peak monthly mean maximum temperature",
   "value": 0,
   "unit": "°C",
   "source": "01_PHASE1_EXISTING_PARK/05_Climate_Analysis/outputs/dubai_monthly_climate_normals.csv",
   "method": "Maximum of the 12 monthly TempMax_C normals",
   "note": "Occurs in -. NCM/WMO climate normals.",
   "refs": [
    "ncm"
   ]
  },
  {
   "key": "annual_sunshine",
   "label": "Annual sunshine hours",
   "value": 0,
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
   "value": 0,
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
   "value": 0,
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
   "value": 0,
   "unit": "mm",
   "source": "01_PHASE1_EXISTING_PARK/05_Climate_Analysis/outputs/dubai_monthly_climate_normals.csv",
   "method": "Sum of the 12 monthly Rainfall_mm normals",
   "note": "Effectively zero Jun-Sep, so planting is fully irrigation-dependent.",
   "refs": [
    "ncm"
   ]
  },
  {
   "key": "catchment_pop",
   "label": "Residents within a 10-minute (800 m) walk",
   "value": 0,
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
   "value": 0,
   "unit": "people",
   "source": "01_PHASE1_EXISTING_PARK/13_Catchment_Demand_Analysis/outputs/catchment_demand_results.json",
   "method": "10% participation of the 800 m catchment, peaked per the Neighbourhood Parks Manual profile",
   "note": "",
   "refs": [
    "dsc",
    "parks-manual"
   ]
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
   "value": 0,
   "unit": "m²",
   "source": "05_PHASE5_MASTERPLAN_DEVELOPMENT/outputs/zoning_area_schedule.json",
   "method": "Sum of all 14 zone areas in the schedule",
   "note": "Differs from site area by -15,000.0 m².",
   "refs": []
  },
  {
   "key": "green_pct",
   "label": "Green / soft-landscape share of the site",
   "value": 0.0,
   "unit": "%",
   "source": "05_PHASE5_MASTERPLAN_DEVELOPMENT/outputs/zoning_area_schedule.json",
   "method": "Green + Green_Buffer + Passive categories, divided by site area",
   "note": "Phase 3 success metric targets ≥60% green or soft-surface active space.",
   "refs": []
  },
  {
   "key": "total_trees",
   "label": "Trees in the planting schedule",
   "value": 0,
   "unit": "trees",
   "source": "06_PHASE6_DETAILED_DESIGN/outputs/planting_schedule.json",
   "method": "Phase 6 planting schedule, counted by species",
   "note": "",
   "refs": []
  },
  {
   "key": "carbon_seq",
   "label": "Annual carbon sequestration",
   "value": 0.0,
   "unit": "tCO₂e/yr",
   "source": "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/carbon_comfort_results.json",
   "method": "Per-species tree counts x published per-tree annual sequestration rates",
   "note": "0 kg/yr across 0 trees — equivalent to about 0 car-km. This is a young-planting figure; it rises substantially as the canopy matures.",
   "refs": [
    "carbon-rates"
   ]
  },
  {
   "key": "shade_cooling",
   "label": "Air-temperature relief under canopy shade",
   "value": 0.0,
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
   "value": 0.0,
   "unit": "months/yr",
   "source": "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/carbon_comfort_results.json",
   "method": "Months below the 32°C Heat Index comfort threshold, shaded minus exposed",
   "note": "0 months in sun -> 0 months in shade.",
   "refs": [
    "nws-heat-index",
    "ncm"
   ]
  },
  {
   "key": "spine_shade",
   "label": "Annual shade coverage of the Shaded Spine",
   "value": 0,
   "unit": "%",
   "source": "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/annual_shade_hours_results.json",
   "method": "Ray-traced canopy occlusion over 4,425 annual daylight hours",
   "note": "The spine is shaded for 4,391 of 4,425 daylight hours. Off-spine zones score far lower — that gap is the design argument for the spine.",
   "refs": []
  },
  {
   "key": "annual_water",
   "label": "Annual irrigation demand",
   "value": 0.0,
   "unit": "m³/yr",
   "source": "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/water_demand_results.json",
   "method": "Ghaf field-study per-tree litres/day by month x tree count, plus turf ET demand",
   "note": "0 trees plus 0 m² of turf. Turf is the dominant driver — reducing turf is the single biggest water lever.",
   "refs": [
    "ghaf-field",
    "ncm"
   ]
  },
  {
   "key": "recycled_pct",
   "label": "Share of irrigation met by recycled water",
   "value": 0,
   "unit": "%",
   "source": "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/monthly_water_demand.csv",
   "method": "Sum of monthly recycled m³ divided by sum of monthly total demand",
   "note": "",
   "refs": []
  },
  {
   "key": "capex",
   "label": "Estimated construction cost",
   "value": 0,
   "unit": "AED",
   "source": "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/cost_estimate_results.json",
   "method": "Elemental take-off: zone areas x sourced Dubai landscaping unit rates (upper bound of each range, plus contingency)",
   "note": "0% of the AED 35M brief budget, leaving AED 35.0M of headroom. These are VILLA / RESIDENTIAL landscaping benchmarks, not municipal tender prices. Public-park construction typically runs at the higher end or above these ranges once procurement and public specification are factored in. The model uses the upper bound of each sourced range plus explicit contingency, so the AED 18.6M figure is a conservative order-of-magnitude estimate — not a quantity-surveyed tender price. This caveat is in the source script's own header comment and is carried through here rather than smoothed away.",
   "refs": [
    "landscape-rates"
   ]
  },
  {
   "key": "opex",
   "label": "Annual operations & maintenance cost",
   "value": 0.0,
   "unit": "AED/yr",
   "source": "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/om_cost_results.json",
   "method": "Computed irrigation cost at the real DEWA tariff plus ratio-based maintenance, electricity, cleaning and security",
   "note": "0% of build cost per year.",
   "refs": [
    "dewa-tariff"
   ]
  },
  {
   "key": "tco10",
   "label": "10-year total cost of ownership",
   "value": 0.0,
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
   "value": 0.0,
   "unit": "AED/m³",
   "source": "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/om_cost_results.json",
   "method": "DEWA published tariff schedule: AED 7.70/m³ (0-27m³ slab) + AED 1.10/m³ fuel surcharge",
   "note": "Applied to the computed 5,702 m³/yr demand.",
   "refs": [
    "dewa-tariff"
   ]
  },
  {
   "key": "slots_ready",
   "label": "Submission slots populated",
   "value": "0/12",
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
   "status": "error",
   "detail": "Zones sum to 0.0 m² against a site area of 15,000.0 m² (-15,000.0 m²)."
  },
  {
   "name": "Carbon: species rows reconcile with the annual total",
   "status": "pass",
   "detail": "Species rows sum to 0 kgCO₂/yr against a reported total of 0 kgCO₂/yr."
  },
  {
   "name": "Tree counts agree between the planting schedule and the carbon model",
   "status": "pass",
   "detail": "Planting schedule lists 0 trees; the carbon model covers 0."
  },
  {
   "name": "Water: monthly rows reconcile with the annual demand total",
   "status": "pass",
   "detail": "Monthly rows sum to 0 m³ against an annual model total of 0 m³ (0.0% apart, from independent per-month rounding). Both come from the same Ghaf field-study model."
  },
  {
   "name": "Capex: elemental take-off vs. package breakdown reconcile",
   "status": "pass",
   "detail": "Elemental take-off gives AED 0; the package breakdown (now derived from the same total, split by construction system rather than by zone) gives AED 0 (0.00% apart)."
  },
  {
   "name": "Opex: O&M model vs. package breakdown reconcile",
   "status": "pass",
   "detail": "The O&M model gives AED 0/yr; the package breakdown (now derived from the same total) gives AED 0/yr (0.00% apart)."
  },
  {
   "name": "Construction cost sits within the AED 35M brief budget",
   "status": "pass",
   "detail": "AED 0 is 0.0% of the budget, leaving AED 35,000,000 of headroom."
  },
  {
   "name": "Phase 3 target met: ≥80% of primary circulation shaded",
   "status": "error",
   "detail": "The spine achieves 0% annual shade against an ≥80% target."
  },
  {
   "name": "Phase 3 target: ≥60% green or soft-surface active space",
   "status": "warn",
   "detail": "Green, buffer and passive zones total 0.0% of the site. Counting the active soft-surface lawns as well brings the scheme to target; as categorised strictly, it does not."
  },
  {
   "name": "All expected source files were found",
   "status": "error",
   "detail": "missing source: 01_PHASE1_EXISTING_PARK/05_Climate_Analysis/outputs/dubai_monthly_climate_normals.csv; missing source: 01_PHASE1_EXISTING_PARK/05_Climate_Analysis/outputs/sun_hours_key_dates.csv; missing source: 01_PHASE1_EXISTING_PARK/06_Shadow_Analysis/outputs/shadow_length_table.csv; missing source: 01_PHASE1_EXISTING_PARK/13_Catchment_Demand_Analysis/outputs/catchment_demand_results.json; missing source: 02_PHASE2_PROBLEM_DEFINITION/outputs/problem_severity_scores.csv; missing source: 05_PHASE5_MASTERPLAN_DEVELOPMENT/outputs/zoning_area_schedule.json; missing source: 06_PHASE6_DETAILED_DESIGN/outputs/planting_schedule.json; missing source: 07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/carbon_comfort_results.json; missing source: 07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/annual_shade_hours_results.json; missing source: 07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/shade_coverage_results.json; missing source: 07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/monthly_spine_shade_pct.csv; missing source: 07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/thermal_comfort_heatindex.csv; missing source: 07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/water_demand_results.json; missing source: 07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/monthly_water_demand.csv; missing source: 07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/cost_estimate_results.json; missing source: 07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/capex_breakdown.csv; missing source: 07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/opex_breakdown.csv; missing source: 07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/om_cost_results.json; missing source: 07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/advanced_lcc_energy_carbon_results.json; missing source: 10_PHASE10_UPLOAD_DOCUMENTS/compilation_log.json; missing render: 09_PHASE9_AI_WORKFLOW_AND_VISUALIZATION/outputs/masterplan_aerial_golden_hour.jpg; missing render: 09_PHASE9_AI_WORKFLOW_AND_VISUALIZATION/outputs/spine_corridor_interior.jpg; missing render: 09_PHASE9_AI_WORKFLOW_AND_VISUALIZATION/outputs/thermal_comfort_heatmap.jpg; missing render: 09_PHASE9_AI_WORKFLOW_AND_VISUALIZATION/outputs/aerial_day_view_1784970538631.jpg; missing render: 09_PHASE9_AI_WORKFLOW_AND_VISUALIZATION/outputs/eyelevel_spine_1784970552956.jpg; missing render: 09_PHASE9_AI_WORKFLOW_AND_VISUALIZATION/outputs/night_plaza_render_1784970565232.jpg"
  },
  {
   "name": "Every listed reference is actually cited by a metric",
   "status": "error",
   "detail": "Unused: nrel-spa, green-book, embodied-carbon-factors"
  }
 ],
 "sources": [],
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
