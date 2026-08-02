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

## ⚠️ Rules that apply to EVERY prompt

**MUST be true in every image:**
1. The canopy is **ONE continuous arc**, 141 m radius, bowing **convex south**.
   Never straight. Never an S-curve. Never a full ring or closed loop.
2. Water is a **0.9 m narrow channel** at the canopy's northern edge.
   **NEVER a lagoon, lake, pond, canal or reflecting pool.**
3. The palm court (Oasis Basin) sits in the **concave / north** side.
4. Trees are **Ghaf, Neem, Ficus nitida, Date Palm, Olive** — desert species only.
5. Light through the soffit is **dappled at 12% transmittance** — not solid shadow.
6. Real Dubai residential context — low-rise beige/sand buildings, palm-lined
   streets. **Not** a skyline of glass towers. **Not** the Museum of the Future.
7. Real people using it: Emirati and expatriate families, mixed ages, modest
   dress including kanduras and abayas, children, older people, joggers.

---

## PROMPT 01 — Aerial masterplan view (HIGHEST PRIORITY)

> Photorealistic aerial architectural visualisation of a 15,000 m² neighbourhood
> park in Dubai, UAE, at 25.19°N, viewed from 120 m altitude at a 45° oblique
> angle looking north, golden hour late afternoon light with long soft shadows.
>
> The park is a 150 × 100 metre rectangle. Its single organising element is ONE
> continuous crescent-shaped shade canopy — a triangulated steel-and-timber
> gridshell 18 metres wide and 4.5 metres high, sweeping in a smooth arc of 141
> metre radius across the full width of the site, bowing convex toward the south.
> The arc is 144 metres long end to end with an 18 metre bow depth. Its soffit is
> a translucent ETFE diagrid casting intricate dappled light at 12% transmittance
> onto a 7 metre wide sand-coloured stone walkway beneath. A 3 metre deep vertical
> louvre fin runs along the canopy's southern edge.
>
> Running along the canopy's northern drip line is a very narrow shallow water
> channel, only 0.9 metres wide — a thin stone-lined rill flush with the paving,
> ankle deep, catching the light as a bright thread. It is a traditional Emirati
> falaj irrigation channel, NOT a lake or lagoon.
>
> On the concave northern side of the crescent: a sunken date palm court in a
> shallow basin, a quiet contemplation garden with olive trees, a children's play
> area shaped from sculpted sand dunes, and a family picnic grove under Neem
> trees. On the convex southern side: a community plaza and event lawn, a
> multipurpose sports lawn, eight small modular souk kiosks, and an outdoor
> fitness terrace.
>
> Narrow 3 metre radial alleys run outward from the arc's centre, dividing these
> rooms like slices — no room is a rectangle. A 2.5 metre wide unshaded running
> loop traces the perimeter. A 3.5 metre planted earth berm buffers the park from
> the roads.
>
> 131 desert trees: Ghaf (Prosopis cineraria) with broad 12 metre crowns on the
> southern rank, Neem on the northern rank, date palms in the basin, olives at
> the margins. Arid-climate ground cover, decomposed granite, gravel mulch,
> drought-tolerant native grasses — sparse and silvery, not lush green lawn.
>
> Surrounding context: low-rise beige and sand-coloured Dubai residential
> villas, palm-lined streets, mid-rise apartment blocks in the far distance.
>
> Families walking in the shade, children playing, people seated at the water's
> edge. Architectural photography, ultra-detailed, 8K, professional landscape
> architecture competition rendering, warm desert palette of sand, terracotta,
> bronze, sage green and pale limestone.

**Save to:** `design/renders/Aerial/masterplan_aerial_golden_hour.jpg`

---

## PROMPT 02 — Night plaza and canopy

> Photorealistic night architectural visualisation of a neighbourhood park in
> Dubai. A continuous curved gridshell canopy 18 metres wide and 4.5 metres high
> arcs gently across the frame, bowing away from the viewer. Warm concealed
> uplighting washes the triangulated diagrid soffit from below, making the
> structure glow like a lantern against a deep blue desert night sky.
>
> Beneath it, a 7 metre wide pale stone walkway. Along its northern edge a very
> narrow 0.9 metre water channel runs, lit from within, a thin ribbon of light
> reflecting the canopy above. Low bollard lighting at 3 metre intervals. NO jet
> fountains, NO large water features, NO lagoon.
>
> To one side, a community plaza with an event lawn where families gather in the
> evening cool; small modular souk kiosks with warm light spilling from their
> serving counters. Ghaf and Neem trees uplit softly. Date palms silhouetted.
>
> Emirati and expatriate families, mixed ages, some in kanduras and abayas,
> children running, people seated on low stone benches. Warm 2700K lighting,
> dark sky compliant, no light pollution upward.
>
> Low-rise Dubai residential context in the background. Architectural night
> photography, long exposure quality, ultra-detailed, 8K.

**Save to:** `design/renders/Night/night_plaza_render_1784970565232.jpg`

---

## PROMPT 03 — Eye-level under the crescent walk

> Photorealistic eye-level architectural visualisation, standing on a 7 metre
> wide sand-coloured stone walkway beneath a curving shade canopy in Dubai at
> midday. The canopy is a triangulated steel-and-timber gridshell 18 metres wide,
> 4.5 metres above the walk, and it CURVES CONTINUOUSLY away from the viewer in
> one smooth arc — the far end of the walk bends out of sight around the curve.
> It is not straight, and it does not S-bend.
>
> The translucent ETFE soffit casts an intricate lattice of dappled light and
> shadow onto the paving at 12% transmittance — bright and legible, not dark.
> Along the canopy's southern edge a 3 metre deep vertical louvre fin cuts the
> low sun. Along the northern edge, at the canopy's drip line, a very narrow 0.9
> metre wide shallow water channel runs parallel to the walk — a thin stone rill
> flush with the paving, ankle deep, water moving slowly, catching light. It is
> narrow enough to step across.
>
> Ghaf trees with broad umbrella crowns line the southern rank, Neem trees the
> northern. Low stone seating benches in the shade margin. A drinking fountain
> and bottle-fill station. Beyond the canopy's edge, bright sunlit desert
> planting — gravel mulch, drought-tolerant grasses, olive trees.
>
> Emirati and expatriate families walking, a child trailing a hand in the water
> channel, an older couple seated in the shade, a jogger passing. Mixed ages,
> modest dress.
>
> Strong contrast between the cool shaded walkway and the brilliant sunlit
> landscape beyond. Architectural photography, 35mm lens, ultra-detailed, 8K,
> warm desert palette.

**Save to:** `design/renders/Eye_Level/spine_corridor_interior.jpg`

---

## PROMPT 04 — The Oasis Basin (Al Nakhil)

> Photorealistic architectural visualisation of a sunken palm court in a Dubai
> neighbourhood park, late afternoon. A shallow circular basin stepped down 1.5
> metres below the surrounding grade, held in the concave northern side of a
> large curving shade canopy which arcs across the background, its triangulated
> gridshell visible above and behind.
>
> Date palms (Phoenix dactylifera) rise from the basin floor in an informal
> grove, their crowns level with the surrounding ground so people walking above
> look into the canopy of the palms. Stepped stone seating rings the basin.
> Decomposed granite and pale gravel underfoot. A narrow 0.9 metre water channel
> feeds the basin from the canopy's edge — a thin rill, not a pool.
>
> Families seated on the steps, children on the basin floor, people sheltering
> from the sun. Warm low light raking across the stone. Traditional Emirati
> falaj irrigation reference — the oasis as a cool sunken room.
>
> Desert planting only: date palms, olives, drought-tolerant grasses. Low-rise
> Dubai residential context beyond. Architectural photography, ultra-detailed,
> 8K, sand, bronze, sage and limestone palette.

**Save to:** `design/renders/Eye_Level/oasis_basin.jpg`

---

## PROMPT 05 — Children's Dune Play

> Photorealistic architectural visualisation of an inclusive children's play area
> in a Dubai neighbourhood park, morning light. The play landscape is sculpted
> from rolling sand-coloured mounds and dunes — climbable earthworks with
> embedded slides, rope nets, tunnels and shaded nature-play elements built from
> timber and stone. Nature play, not primary-colour plastic equipment.
>
> It sits on the cool concave northern side of a large curving shade canopy,
> whose triangulated gridshell arcs across the background casting dappled shade.
> Neem trees provide additional canopy. A drinking fountain nearby. Shaded family
> seating along the edge where parents can watch.
>
> Designed for different age groups and universal accessibility — a ramped route
> up the largest dune, ground-level play elements, sensory planting.
>
> Emirati and expatriate children playing, parents seated in shade, mixed ages
> and abilities. Desert planting, gravel and sand surfaces, no lush lawn.
> Architectural photography, ultra-detailed, 8K, warm sand and terracotta palette.

**Save to:** `design/renders/Day/childrens_dune_play.jpg`

---

## PROMPT 06 — The Souk Kiosks and Community Plaza

> Photorealistic architectural visualisation of a small community plaza and
> market edge in a Dubai neighbourhood park, early evening. Eight small modular
> souk kiosks in timber and perforated bronze-toned metal line one edge, serving
> food and drink, their shutters open, warm light spilling out.
>
> They face an open plaza and event lawn on the convex southern side of a large
> curving shade canopy, which arcs across the background. The kiosks are small
> and modular — market stalls, not a shopping centre.
>
> Families gathering in the evening cool, people queuing at a kiosk, children on
> the lawn, an informal event setting up. Low stone benches, shade sails over
> the seating, Ghaf trees with broad crowns.
>
> Low-rise Dubai residential context beyond. Warm evening light. Architectural
> photography, ultra-detailed, 8K, desert palette of sand, bronze and terracotta.

**Save to:** `design/renders/Day/souk_plaza.jpg`

---

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
| 7 | Is the context **low-rise Dubai residential**? (no glass towers) | ☐ |
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
python -m tests.test_pipeline           # confirm 38 checks still pass
```

Every render must be captioned **"artistic impression — illustrative of design
intent"**. Technical drawings are captioned **"technical drawing, to scale"**.
A juror must never have to guess which they are looking at.

---

*Generated from the live project. Repository: https://github.com/wasim437/Al_SAFA*
