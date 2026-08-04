# AL SAFA 2 PARK — MASTER PROMPT

**One file. Everything an AI needs to understand this project and generate the visuals.**

Paste **Section A** into any image AI first (it teaches the model the project),
then paste **one prompt from Section C**. Section D is the test each image must
pass before it goes into the submission.

Every number below is pulled from the live code — `src/config.py`, `src/plan.py`,
`data/raw/site_zoning_schedule.csv`. Nothing here is invented. If you change the
design, re-run `python run_analysis.py` and these numbers change with it.

---

# SECTION A — THE PROJECT, IN FULL

## A1. What this is

| | |
|---|---|
| **Project** | Al Safa 2 Park redesign — concept name **"Falaj Al Safa"** |
| **Meaning** | *a crescent of shade over a channel of water* |
| **Client** | Dubai Municipality — AI Park Design Challenge |
| **Applicant** | Mohamed Wasim · Individual Applicant |
| **Deadline** | 15 August 2026 |
| **Budget** | AED 35,000,000 ceiling · costed at **AED 26,973,013 (77.1%)** |
| **Repository** | https://github.com/wasim437/Al_SAFA |
| **Live portal** | https://wasim437.github.io/Al_SAFA/ |

## A2. The real location — this is a real place

| | |
|---|---|
| **Site** | Al Safa 2 Park, Dubai, United Arab Emirates |
| **Latitude / Longitude** | **25.19° N, 55.238° E** |
| **Elevation** | 5 m above sea level |
| **Timezone** | Asia/Dubai (UTC+4) |
| **Site area** | **15,000 m²** |
| **Site envelope** | **150 m (E–W) × 100 m (N–S)** rectangle |
| **Boundary status** | ⚠️ **ASSUMED** — pending confirmation against `Al Safa Park 2 Plan (5).dwg` |
| **Context** | Dense low-rise residential neighbourhood, Sheikh Zayed Road corridor nearby, roads on the south and the two short edges |
| **Catchment** | **7,640 residents** within a 10-minute walk (Dubai Statistics Centre, 2023) |

**Climate reality that drives the entire design:**
- 39 years of NCM monthly normals (1977–2015), reconstructed to an 8,760-hour year
- **4,402 daylight hours** modelled per year
- Peak heat index in the open: **56.8 °C**
- Sun at 25.19° N passes **north of vertical in summer** — a critical fact: an
  east–west canopy must overhang on its **south** side to work

## A3. The one-sentence design

> **One continuous crescent-shaped shade canopy sweeps across the site. A narrow
> water channel runs along its northern shaded edge. Every room in the park is
> struck off the same arc centre, so no room is a rectangle and every room faces
> the crescent square-on.**

## A4. Why an arc and not a straight line — the design was solved, not styled

A straight canopy presents **one orientation**. When a sun angle defeats it, it
defeats the entire length at once and the walk has no shade anywhere. An arc
changes heading continuously, so some segment is always angled well.

Swept against the full 8,760-hour solar model:

| Plan form | Mean cover | Worst month | **Hours with NO shade anywhere** |
|---|---|---|---|
| Straight east–west bar | **87.4%** | 68.7% | 330 |
| Sine meander *(superseded)* | 85.0% | 73.1% | 63 |
| Arc, sagitta 10 m | 87.1% | 70.2% | 116 |
| Arc, sagitta 14 m | 86.6% | 71.3% | 62 |
| **Arc, sagitta 18 m** | 85.9% | **72.1%** | **52** ← **ADOPTED** |
| Arc, sagitta 22 m | 84.9% | 72.3% | 61 |
| Closed elliptical loop | 79.1% | 69.8% | 89 |

The straight bar shades **more** ground on average. The crescent is adopted
because it removes six-sevenths of the hours in which the route offers nowhere
at all to stand. That trade is stated in the direction that is not flattering.

## A5. THE EXACT GEOMETRY — non-negotiable in every image

```
ARC
  radius                  141.25 m
  arc centre              (75.0, 182.25)  ← NORTH of the site, off-site
  chord (end to end)      138.0 m
  sagitta (bow depth)     18.0 m
  bows CONVEX SOUTH       midpoint at y=44.5 m, ends at y=57.65 m
  arc length              144.2 m

CANOPY  ("Al Hilal")
  walking surface width    7.0 m
  canopy width            18.0 m   (overhangs the walk on both sides)
  canopy height            4.5 m   (underside, above the walk)
  southern louvre depth    3.0 m   (vertical fin, blocks low southern sun)
  soffit transmittance    12%      (ETFE — dappled light, NOT solid black shade)
  structure               steel/timber gridshell, triangulated diagrid

WATER  ("Al Falaj")
  channel width            0.9 m   ← NARROW. A rill, not a lagoon.
  position                 9.0 m NORTH of the walk centreline
  why                      sits on the canopy's drip line, shaded all day,
                           so it does not evaporate
  total water area       105.2 m²  (0.70% of the site)
  depth                   shallow, ankle-deep, stone-lined, flush with paving

PERIMETER
  running loop width       2.5 m   ("Al Madar") — UNSHADED, deliberately
  dune berm depth          3.5 m   ("Al Kathib") — planted earth against roads
```

## A6. The complete room schedule — 18 zones, measured, closing on 15,000 m²

Areas are the **shoelace area of the actual drawn polygon** — measured, not
authored. That is why the schedule closes exactly.

| # | Zone | Category | Area m² | % site |
|---|---|---|---|---|
| 1 | **Al Mamsha** — the Crescent Walk | Circulation | 871.2 | 5.81 |
| 2 | **Al Falaj** — the water channel | Water | 105.2 | 0.70 |
| 3 | Crescent Shade Margin (North) | Green | 549.0 | 3.66 |
| 4 | Crescent Shade Margin (South) | Green | 714.8 | 4.77 |
| 5 | West Gate Majlis | Arrival | 439.0 | 2.93 |
| 6 | East Gate Majlis | Arrival | 439.0 | 2.93 |
| 7 | **Al Nakhil** — the Oasis Basin | Green | 1,139.5 | 7.60 |
| 8 | Quiet Contemplation Garden | Passive | 707.5 | 4.72 |
| 9 | Children's Dune Play | Active | 1,267.3 | 8.45 |
| 10 | Family Picnic Grove | Passive | 1,267.3 | 8.45 |
| 11 | Outdoor Fitness Terrace | Active | 908.5 | 6.06 |
| 12 | Native Planting / Biodiversity Wadi | Green | 893.8 | 5.96 |
| 13 | Community Plaza & Event Lawn | Social | 787.5 | 5.25 |
| 14 | Souk Kiosks & Services | Commercial | 417.0 | 2.78 |
| 15 | Multipurpose Sports Lawn | Active | 630.0 | 4.20 |
| 16 | **Al Kathib** — the dune berm | Green Buffer | 1,463.8 | 9.76 |
| 17 | **Al Madar** — the perimeter loop | Circulation | 985.6 | 6.57 |
| 18 | **Al Sikkak** — shaded alleys & setbacks | Circulation | 1,414.0 | 9.43 |
| | **TOTAL** | | **15,000** | **100** |

**Which side each room sits on — this matters for every image:**

- **CONCAVE (north) side — the cool pocket, where people linger:**
  Oasis Basin, Quiet Contemplation Garden, Children's Dune Play, Family Picnic Grove
- **CONVEX (south) side — active and civic:**
  Community Plaza & Event Lawn, Multipurpose Sports Lawn, Souk Kiosks,
  Outdoor Fitness Terrace, Biodiversity Wadi

The arc bows convex south so the structure sits between the sun and the hollow
it wraps — making the concave side the park's cool pocket rather than a
south-facing bowl.

## A7. The planting — 131 trees, 5 desert species only

| Species | Botanical | Crown radius | Height | Where | Water |
|---|---|---|---|---|---|
| **Ghaf** | *Prosopis cineraria* | 6.0 m | 8.0 m | **South rank** of the avenue | 45 L/day |
| **Neem** | *Azadirachta indica* | 5.0 m | 9.0 m | **North rank**, + 18 at the gates | 90 L/day |
| **Ficus nitida** | *Ficus microcarpa* | 4.5 m | 8.0 m | Biodiversity wadi | — |
| **Date Palm** | *Phoenix dactylifera* | — | tall, slender | Oasis Basin palm court | — |
| **Olive** | *Olea europaea* | — | low, silver | Quiet garden, margins | — |

Ghaf is the **UAE national tree** and the most drought-tolerant in the schedule —
it takes the hot southern rank on purpose. That is not decoration, it is the
reason the irrigation budget closes.

❌ **NO tropical planting.** No rainforest, no cycads, no banana, no flowering
jungle, no dense green lawn everywhere. This is a **desert** park.

## A8. Facilities — 20 placed, every one required by the brief

| Type | Count | Where |
|---|---|---|
| Souk kiosks (F&B + retail) | 8 modular | Convex face, facing plaza + event lawn |
| Café pavilion | 1 | Between plaza and play — the two longest-dwell spaces |
| Restrooms (universally accessible) | 2 | At West and East gates |
| Drinking fountains + bottle fill | 6 | 4 on the shaded walk, 1 at play, 1 at fitness |
| Waste & recycling (paired, screened) | 5 | Gates, plaza, picnic grove, play |
| Service & maintenance store | 1 | Behind the berm, invisible from the walk |
| Bicycle parking (sheltered) | 2 | Inside each gate |
| Drop-off / pick-up bays | 2 | Street edge, level and step-free |

## A9. The measured performance — what the design achieves

| Metric | Value |
|---|---|
| Annual daylight hours modelled | 4,402 |
| Comfortable daylight hours — **today** | **44.5%** |
| Comfortable daylight hours — **as designed** | **64.6%** |
| Mean heat-index reduction under canopy | **7.13 °C** |
| Peak heat index, exposed → shaded | 56.8 °C → **48.7 °C** |
| Crescent Walk shaded (canopy + louvre) | **87.3%** of daylight hours |
| Same walk with tree avenue counted | 88.5% |
| Site-wide mean shade | 34.1% |
| Trees planted | 131 |

## A10. The four AI models behind it

| Model | Task | Result | Why it is a real problem |
|---|---|---|---|
| **M1a** Random Forest | Shade surrogate | R² 0.998 | Learns a slow ray-traced simulation from cheap plan geometry |
| **M1b** Neural network | Shade surrogate (deployed) | R² 0.994 | Differentiable → usable inside a layout optimiser |
| **M2** Gradient Boosting | Comfort band (4-class) | 97.5% acc | Temperature and humidity **withheld** — sees only sun position + calendar |
| **M3** K-Means | Microclimate regimes | k=2 by silhouette | k is *selected*, not chosen to look tidy |

The discipline: **the target must not be recoverable from the inputs by algebra.**

## A11. Two corrections this project makes to itself — keep them

1. **A withdrawn shade claim.** An earlier version claimed **99.2%** annual shade
   on a flat 9 m canopy over a 9 m walk. It fails a geometric check — at low sun
   the shadow slides clean off the path. Withdrawn; section re-solved; now **87.3%**.
2. **Three withdrawn images.** A "PET/CFD thermal comfort analysis" where no CFD
   was run; a "Satellite NDVI Analytics" whose raster is numpy noise; and a
   "Generative Parametric Voronoi Canopy — Algorithmic Solar Optimization" in
   which nothing was optimised. All withdrawn.

---

# SECTION B — HOW THE PROJECT FOLDER IS ORGANISED

**The only 5 things a human touches:**

| | |
|---|---|
| `EXPLAIN_THE_PROJECT/START_HERE.md` | plain-language walkthrough |
| `PROJECT_PLAN.md` | full detail — requirements, phases, what's left |
| `00_BRIEF/` | what Dubai Municipality actually asked for |
| `AL_SAFA_MASTER_PROMPT.md` | **this file** — the visuals |
| `UPLOAD_THESE_12_FILES/` | the 12 PDFs that get submitted |

**The machinery that produces them:**

```
src/plan.py       ⭐ SINGLE SOURCE of the crescent geometry
src/climate.py       8,760-hour year rebuilt from 39yr NCM normals
src/solar.py         sun position + shadow ray-tracing
src/dataset.py       assembles the ML training tables
src/models.py        the four models
src/drawings.py      section, elevation, circulation, planting, facilities
src/boards.py        the two presentation boards
src/costing.py       the AED 35M cost model
data/raw/            6 documented source datasets + sources.json
data/processed/      8,760-hour series + 15,000-cell grid
figures/             fig01–fig11, one visual system
design/visuals/      generated technical drawings
design/renders/      ⚠️ EMPTY — this file exists to fill it
tests/               38 pipeline checks + portal + film tests
```

**The rule that makes it trustworthy:** everything in `figures/`,
`design/visuals/`, `docs/` and `submission/` is derived from `data/` and `src/`.
Change an input, re-run, and every chart, drawing and figure moves with it — or
a test fails loudly.

**The 10 phases:** Site Analysis → Problem Definition → Objectives → Concept →
Masterplan → Detailed Design → Sustainability → User Experience → AI &
Visualisation → Submission Assembly. Detail in `PROJECT_PLAN.md` §5.

---

# SECTION C — THE IMAGE PROMPTS

**Six images. Generate them in the order below — the first three are the ones
the submission actually needs; the last three are depth.**

These are written for a park-only frame. Earlier versions of these prompts asked
for the surrounding Dubai streets and villas, and the context ate the subject:
the park became a small thing in the middle of a neighbourhood, and the crescent
— the entire idea — stopped reading. **Every prompt below now keeps the camera
inside the park.** Where a boundary has to exist, it is the planted dune berm,
which is part of the design.

---

## ⚠️ Rules that apply to EVERY prompt

**MUST be true in every image:**

1. The canopy is **ONE continuous arc**, 141 m radius, bowing **convex south**.
   Never straight. Never an S-curve. Never a full ring or closed loop.
2. Water is a **0.9 m narrow channel** at the canopy's northern edge.
   **NEVER a lagoon, lake, pond, canal or reflecting pool.** It is a rill you
   could step across.
3. The palm court (Oasis Basin) sits on the **concave / north** side.
4. Trees are **Ghaf, Neem, Ficus nitida, Date Palm, Olive** — desert species
   only. Sparse, silvery, drought-adapted. Never a lush green lawn.
5. Light through the soffit is **dappled at 12% transmittance** — a fine mesh of
   light on the ground, not a solid black shadow.
6. **The park fills the frame.** No roads, no cars, no villas, no apartment
   blocks, no skyline, no city beyond the trees. If an edge must be visible it
   is the 3.5 m planted earth berm and the trees on it.
7. Real people using it: Emirati and expatriate families, mixed ages, modest
   dress including kanduras and abayas, children, older people, joggers.

---

## HOW TO USE THESE — IF THE TOOL CAN READ THIS REPOSITORY

If you have given the whole project folder to the tool (Antigravity, Cursor,
Claude, a Gemini project with the files attached), **do not make it imagine the
park — make it look at the park.** The drawings in this repository are the
ground truth, and a model that has seen `figures/fig10_masterplan.png` will not
invent a lagoon.

**Paste this first, once, before any image prompt:**

> Before you generate anything, read these files from the project folder and
> use them as the ground truth for every image. Do not invent geometry that
> contradicts them.
>
> **Read first — the design itself:**
> - `AL_SAFA_MASTER_PROMPT.md` — Section A is the whole project: exact
>   geometry, the 18-room schedule, the planting, the facilities.
> - `src/config.py` — the CRESCENT block. Radius, canopy width, canopy height,
>   louvre depth, walk width. These are the real numbers; nothing overrides them.
> - `src/plan.py` — how every room is struck off the arc centre.
>
> **Look at these images — this is what the park actually looks like in plan
> and section. Match them:**
> - `figures/fig10_masterplan.png` — THE MASTERPLAN. The single most important
>   reference. The arc, the rooms, the alleys, the loop, in true proportion.
> - `design/visuals/section_crescent.png` — the canopy in section, with real
>   solstice sun angles. Use this for the canopy's shape and proportions.
> - `design/visuals/elevation_crescent.png` — the structural bay, repeated.
> - `design/visuals/planting_crescent.png` — where all 131 trees actually are.
> - `design/visuals/facilities_crescent.png` — where the 20 facilities sit.
> - `design/visuals/circulation_crescent.png` — every route through the park.
> - `figures/fig04_site_comfort_map.png` — where the site is hot and cool.
>
> **Then tell me, before drawing:** in one short paragraph, describe the plan
> as you understand it from those files — the arc's direction of bow, which
> rooms are on the concave side, and how wide the water channel is. If your
> description does not match the files, read them again. Only then generate.
>
> Every image must show the park and nothing outside it: no roads, no cars, no
> villas, no apartment blocks, no skyline.

**Why the read-first step matters:** six earlier renders of this project were
generated from description alone. Every one of them showed a different park —
a straight corridor, an S-curve, a lagoon — and all six were withdrawn. The
files below exist so that cannot happen again.

---

## HOW TO USE THESE — IF THE TOOL HAS ONLY TEXT

Most image tools do better if they understand the project before they are asked
to draw it. Paste this first, once, then the prompt you want:

> You are producing photorealistic architectural visualisations for a real
> competition entry: the redesign of Al Safa 2 Park in Dubai (25.19°N), a
> 15,000 m² neighbourhood park. The design is called Falaj Al Safa, meaning *a
> crescent of shade over a channel of water*.
>
> The whole scheme is one move. A single continuous crescent-shaped shade
> canopy, 141 metres in radius, sweeps across the site and bows convex toward
> the south, so the structure sits between the sun and the hollow it wraps. A
> narrow 0.9 metre water channel runs along its northern, permanently shaded
> edge — placed there so it does not evaporate. Every room in the park is
> struck off the same arc centre, so no room is a rectangle and every room
> faces the crescent square-on.
>
> The arc is not a styling choice. A straight canopy faces one direction, and
> when a sun angle defeats it the walk has no shade anywhere along its whole
> length. An arc changes heading continuously, so some segment is always
> angled well. Tested against 8,760 hours of real sun positions, the arc cuts
> the hours with no shade anywhere from 330 to 52.
>
> This is a desert park in a hot arid climate: sparse silvery planting,
> decomposed granite, sand-coloured stone, deep shade, glare. It is not a
> temperate park and not a tropical resort.
>
> Every image must show the park and nothing outside it.

---

## PROMPT 01 — Aerial over the whole park (HIGHEST PRIORITY)

> Photorealistic aerial architectural visualisation of a desert neighbourhood
> park in Dubai, viewed from 110 metres at a 40° oblique angle looking north,
> late afternoon golden hour, long soft shadows raking across the ground.
>
> **The park completely fills the frame, edge to edge. There are no roads, no
> cars, no buildings, no city, no horizon line of towers — only the park.**
> The composition is cropped to the park itself.
>
> The single organising element is ONE continuous crescent-shaped shade canopy:
> a triangulated steel-and-timber gridshell, 18 metres wide and 4.5 metres
> high, sweeping in one smooth arc of 141 metre radius across the full width of
> the park, bowing convex toward the south. It is 144 metres long with an 18
> metre bow depth. Its soffit is a translucent ETFE diagrid casting an intricate
> dappled mesh of light onto a 7 metre wide sand-coloured stone walkway beneath.
> A 3 metre deep vertical louvre fin runs along the canopy's southern edge.
>
> Along the canopy's northern drip line runs a very narrow shallow water
> channel, only 0.9 metres wide — a thin stone-lined rill flush with the paving,
> ankle deep, catching the low sun as a single bright thread. A traditional
> Emirati falaj irrigation channel. NOT a lake, pond or lagoon.
>
> On the concave northern side of the crescent: a sunken date palm court in a
> shallow basin, a quiet contemplation garden with olive trees, a children's
> play area sculpted from sand dunes, and a family picnic grove under Neem
> trees. On the convex southern side: a community plaza and event lawn, a
> multipurpose sports lawn, eight small modular souk kiosks, and an outdoor
> fitness terrace.
>
> Narrow 3 metre alleys run radially outward from the arc's centre, slicing
> these rooms like segments — no room is a rectangle. A 2.5 metre unshaded
> running loop traces the park's edge. A 3.5 metre planted earth berm forms the
> outer boundary of the image and closes the composition — beyond it, nothing
> is shown.
>
> 131 desert trees: Ghaf with broad open 12 metre crowns on the southern rank,
> Neem on the northern rank, date palms in the basin, olives at the margins.
> Arid ground cover, decomposed granite, gravel mulch, drought-tolerant native
> grasses — sparse and silvery, never lush green lawn.
>
> Families walking in the shade, children playing, people seated at the water's
> edge. Photorealistic architectural rendering, ultra detailed, professional
> competition visualisation, 8K.

**Match against these files before you draw:**
- `figures/fig10_masterplan.png` — the plan this view must match, exactly
- `design/visuals/planting_crescent.png` — where all 131 trees are
- `design/visuals/facilities_crescent.png` — where the 20 facilities are

**Save to:** `design/renders/Aerial/masterplan_aerial_golden_hour.jpg`

---

## PROMPT 02 — Night, the plaza under the canopy

> Photorealistic architectural visualisation at night, standing in the community
> plaza on the southern convex side of a desert park in Dubai, looking north
> toward a great illuminated shade canopy.
>
> **The park fills the frame entirely. No roads, no cars, no buildings, no city
> lights beyond the park — the darkness past the trees is simply dark.**
>
> A single continuous crescent-shaped gridshell canopy, 18 metres wide and 4.5
> metres high, sweeps across the view in one smooth arc bowing convex toward the
> camera. It is lit from within: warm light glowing up through a triangulated
> ETFE diagrid soffit, so the structure reads as a long band of light curving
> away into the dark at both ends. A 3 metre vertical louvre fin runs along its
> near southern edge.
>
> Beneath it, a 7 metre sand-coloured stone walkway. Beyond it on the far side,
> a narrow 0.9 metre water channel catches the canopy's light as a thin bright
> line. Low bollard lighting along the walk. Eight small modular souk kiosks
> face the plaza, warmly lit, a few people at them.
>
> Emirati and expatriate families in the plaza in the evening cool, children
> running, older people seated. Ghaf and Neem trees silhouetted against the
> glow. Warm amber artificial light against deep blue night, no neon, no purple,
> no cyberpunk colour. Photorealistic architectural rendering, ultra detailed,
> professional competition visualisation, 8K.

**Match against these files before you draw:**
- `design/visuals/facilities_crescent.png` — the souk kiosks and plaza position
- `design/visuals/section_crescent.png` — the canopy's true section and height
- `figures/fig10_masterplan.png` — the plaza sits on the CONVEX south face

**Save to:** `design/renders/Night/night_plaza_render_1784970565232.jpg`

---

## PROMPT 03 — Eye level, walking beneath the crescent

> Photorealistic architectural visualisation at eye level, 1.7 metres above the
> ground, standing on the walkway directly beneath a great curving shade canopy
> in a desert park in Dubai, at two in the afternoon in August.
>
> **The frame is entirely inside the park. No roads, no cars, no buildings.**
>
> The canopy overhead is a triangulated steel-and-timber gridshell, 18 metres
> wide, its underside 4.5 metres above the walk, curving gently away to the left
> and out of sight — the far end is hidden by the curve, because the walk is an
> arc rather than a straight corridor. A translucent ETFE diagrid soffit throws
> an intricate dappled mesh of light and shadow across a 7 metre wide
> sand-coloured stone walkway. The contrast is extreme: brilliant Dubai
> sunlight outside the canopy's edge, deep cool shade beneath it.
>
> A 3 metre deep vertical louvre fin runs along the southern edge on the right,
> cutting the low afternoon sun. To the left, 9 metres away, a very narrow 0.9
> metre stone-lined water channel runs flush with the paving, ankle deep,
> shaded, still.
>
> A double avenue of trees flanks the walk — broad open Ghaf crowns on the
> sunny right side, Neem on the left. Beyond them, glimpses of the park's rooms
> through the trunks.
>
> Families walking, an older man seated in the shade, children ahead on the
> path, a woman in an abaya, a man in a kandura. Photorealistic architectural
> rendering, ultra detailed, professional competition visualisation, 8K.

**Match against these files before you draw:**
- `design/visuals/section_crescent.png` — the canopy in section; match it
- `design/visuals/elevation_crescent.png` — the 6 m structural bay, repeated
- `design/visuals/planting_crescent.png` — Ghaf south rank, Neem north rank

**Save to:** `design/renders/Eye_Level/spine_corridor_interior.jpg`

---

## PROMPT 04 — Al Nakhil, the sunken Oasis Basin

> Photorealistic architectural visualisation at eye level inside a sunken date
> palm court in a desert park in Dubai, late afternoon, warm low light.
>
> **The park fills the frame. No roads, no cars, no buildings beyond it.**
>
> A shallow circular basin set about 1.2 metres below the surrounding ground,
> reached by broad shallow sand-coloured stone steps that double as seating on
> all sides. Tall slender date palms rise from the basin floor, their crowns
> level with the ground above, casting long thin shadows down the steps.
>
> Behind and above the basin to the south, the underside of a great curving
> shade canopy is visible — a triangulated gridshell 4.5 metres high, sweeping
> past in one smooth arc, its ETFE soffit glowing. Between the basin and the
> canopy, a very narrow 0.9 metre stone-lined water channel runs flush with the
> paving, ankle deep, shaded, feeding the basin's planting.
>
> Decomposed granite ground, gravel mulch, sparse silvery drought-tolerant
> grasses and olive trees at the rim. Families seated on the steps in the
> shade, children with bare feet at the water channel, an older couple
> talking. Photorealistic architectural rendering, ultra detailed, professional
> competition visualisation, 8K.

**Match against these files before you draw:**
- `figures/fig10_masterplan.png` — Al Nakhil sits on the CONCAVE north side
- `design/visuals/planting_crescent.png` — the date palms in the basin

**Save to:** `design/renders/Eye_Level/oasis_basin.jpg`

---

## PROMPT 05 — Children's Dune Play

> Photorealistic architectural visualisation of a children's play landscape in a
> desert park in Dubai, mid-morning, strong clear light and crisp shadows.
>
> **The park fills the frame. No roads, no cars, no buildings.**
>
> The play area is sculpted from the ground itself: smooth rolling artificial
> sand dunes in warm sand-coloured rammed earth and soft sand-textured safety
> surfacing, with timber and rope climbing structures set into the slopes,
> shaded tunnels cut through the dunes, and low timber decks. Natural materials
> only — timber, rope, sand, stone. No brightly coloured plastic equipment.
>
> Broad Neem and Ghaf trees stand over the dunes throwing generous shade, and to
> the south the great curving shade canopy sweeps past in one smooth arc, its
> gridshell soffit visible, casting a dappled mesh of light onto the near edge of
> the play area.
>
> Emirati and expatriate children of mixed ages climbing and running, parents
> watching from shaded timber seating, a mother in an abaya, a father with a
> toddler. Photorealistic architectural rendering, ultra detailed, professional
> competition visualisation, 8K.

**Match against these files before you draw:**
- `figures/fig10_masterplan.png` — the play area is on the CONCAVE north side
- `design/visuals/circulation_crescent.png` — how it is reached, step-free

**Save to:** `design/renders/Day/childrens_dune_play.jpg`

---

## PROMPT 06 — The souk kiosks and community plaza

> Photorealistic architectural visualisation of a small open-air market and
> gathering plaza in a desert park in Dubai, late afternoon, warm raking light.
>
> **The park fills the frame. No roads, no cars, no buildings beyond the park.**
>
> Eight small modular kiosks in timber and pale stone, single storey, simple
> and repeating, arranged in a gentle curve facing an open plaza of
> sand-coloured stone paving. Food and small retail, shaded by deep overhangs
> and by fabric shades stretched between them. Behind them to the north rises
> the great curving shade canopy — a triangulated gridshell, 18 metres wide,
> 4.5 metres high, sweeping past in one continuous arc with a 3 metre vertical
> louvre fin along its southern face, the side that faces the plaza.
>
> The plaza opens onto an event lawn of sparse drought-tolerant grass. Ghaf
> trees with broad open crowns stand around its edges. Beyond, the planted
> earth berm closes the view — nothing outside the park is visible.
>
> Families eating, people queuing at a kiosk, children running across the
> plaza, an older group seated in the shade, a vendor serving. Photorealistic
> architectural rendering, ultra detailed, professional competition
> visualisation, 8K.

**Match against these files before you draw:**
- `design/visuals/facilities_crescent.png` — 8 modular kiosks, placed
- `figures/fig10_masterplan.png` — plaza and event lawn on the CONVEX south face

**Save to:** `design/renders/Day/souk_plaza.jpg`

---

---

## ⚠️ WHAT THE FIRST GENERATED SET GOT WRONG — read before regenerating

Six images were generated on 4 August 2026. Two failed and two were weak, and
the faults were the same each time. State these explicitly in any regeneration.

**1. The canopy came back as a CLOSED RING.** The aerial showed an oval loop
running the whole way round the park. That is not this scheme — it is the
closed elliptical loop the sweep in Section A4 tested and rejected, at 79.1%
mean cover and 89 hours with no shade anywhere against the arc's 52. The arc is
ONE OPEN CURVE with two ends that stop at the park boundary. Say so in the
words a model cannot misread: not a ring, not a loop, not an oval, not closed,
two open ends.

**2. The neighbourhood stayed in shot.** Villas, roads and cars were visible in
five of the six. "The park fills the frame" was not strong enough on its own —
name the things that must not appear, one by one.

**3. The canopy came back too tall and too short.** In the souk image it read as
a single arch like a footbridge. It is 18 m wide, 4.5 m high and 144 m long —
low, long and horizontal. A model given "gridshell" alone reaches for a hall.

**4. Bright green lawn.** This is a desert park. Sparse, dry, silvery grass.

Add to the negative prompt when regenerating:
`ring, oval, loop, closed curve, racetrack, doughnut, stadium, arena, tall arch,
footbridge, hangar, bright green lawn, manicured turf, cars, parked cars, road,
street, villa, house, apartment block, city skyline`

## NEGATIVE PROMPT — paste this with every single prompt

```
straight canopy, S-curve, serpentine, sine wave, meandering path, closed loop,
full ring, circular canopy, multiple separate canopies, free-form organic shells,
lagoon, lake, pond, large water feature, reflecting pool, canal, river, wide
water, jet fountains, water jets, splash pad, swimming pool, tropical planting,
rainforest, jungle, cycads, banana plants, flowering tropical shrubs, dense green
lawn everywhere, temperate trees, pine, oak, maple, glass skyscrapers, Burj
Khalifa, Museum of the Future, futuristic sci-fi architecture, empty park, no
people, snow, rain, overcast, cold light, neon, purple lighting, cyberpunk,
plastic playground equipment, primary colours, cartoon, illustration, painting,
low quality, blurry, distorted, watermark, text, logo
```

---

# SECTION D — THE ACCEPTANCE TEST

**Open the image and check every line. If any fails, regenerate. A render that
contradicts the drawings is worse than no render — that is exactly why the
previous six were withdrawn.**

| # | Test | Pass? |
|---|---|---|
| 1 | Is the canopy **ONE continuous arc**? (not straight, not S, not a ring) | ☐ |
| 2 | Does it bow **convex south** — midpoint further south than the ends? | ☐ |
| 3 | Is the water a **narrow channel you could step across**? (not a lagoon) | ☐ |
| 4 | Is the water on the canopy's **northern** edge? | ☐ |
| 5 | Is the light through the soffit **dappled**, not solid black shade? | ☐ |
| 6 | Are all trees **desert species**? (no tropical, no temperate) | ☐ |
| 7 | Does the **park fill the frame**? (no roads, cars, villas or skyline) | ☐ |
| 8 | Are there **real people of mixed ages** actually using it? | ☐ |
| 9 | Does the canopy read as roughly **18 m wide, 4.5 m high** over a **7 m walk**? | ☐ |
| 10 | Would a juror comparing this with `figures/fig10_masterplan.png` see **the same park**? | ☐ |

**Test 10 is the one that matters.** It is the test the withdrawn renders failed.

---

# SECTION E — AFTER YOU GENERATE THE IMAGES

Save each file to the exact path given under its prompt — `src/boards.py` reads
them **by name**. Then re-run, in this order:

```bash
python -m src.boards                    # boards pick the renders back up
python tools/build_docs.py              # website
python tools/sync_portal.py             # portal gallery
python tools/sync_submission.py         # submission/01-12
python tools/build_submission_pdfs.py   # the 12 upload PDFs
python -m tests.test_pipeline           # confirm 41 checks still pass
```

Every render must be captioned **"artistic impression — illustrative of design
intent"**. Technical drawings are captioned **"technical drawing, to scale"**.
A juror must never have to guess which they are looking at.

---

*Generated from the live project. Repository: https://github.com/wasim437/Al_SAFA*
