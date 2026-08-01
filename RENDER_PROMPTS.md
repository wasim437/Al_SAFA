# Render prompt sheet — Falaj Al Safa

**Purpose:** regenerate every visualisation so it shows *the park that the
drawings and the analysis describe*. The current renders show a different
project, and that mismatch is the most visible weakness in the submission.

Generate these in **Antigravity** (or any image model). Each block below is
copy-paste ready. **Do not paraphrase the numbers** — they are what make the
image agree with `figures/fig10_masterplan.png`.

---

## The design facts every prompt must respect

Lock these. If a render contradicts any of them, regenerate it.

| Fact | Value | Why it matters |
|---|---|---|
| Plan form | **one continuous arc**, radius **141 m**, sagitta 18 m | Not straight. Not a full ring. Not two arcs. |
| Arc bows | **convex south** — the hollow faces **north** | The cool pocket is on the concave side |
| Canopy | **18 m wide gridshell**, **4.5 m** high, over a **7 m** walk | Not a solid roof — a lattice |
| Soffit | perforated, **12% light transmittance** | Dappled light on the ground, not blackout shade |
| Louvre | **3 m deep, southern face only** | Vertical fin screen catching low sun |
| Structural bays | **6 m** | Sets the rhythm of the columns |
| Water — Al Falaj | **0.9 m wide channel**, ~105 m² total | **NOT a lagoon or lake.** Sits under the canopy drip line |
| Oasis Basin | sunken palm court in the **concave/north** side | 1,140 m² |
| Trees | **131**: Neem 58, Ficus nitida 34, Ghaf 16, Date Palm 12, Olive 11 | Desert species — **no tropical planting** |
| Perimeter | planted **dune berm** against the roads | Earth mounding, not a wall or fence |
| Site | 150 × 100 m, flat | Low-rise Al Safa 2 villa neighbourhood beyond |
| Latitude | Dubai, 25°N | High summer sun; long low winter shadows |

**Universal negative prompt** — append to every generation:

```
NEGATIVE: straight linear canopy, rectangular pergola, circular ring building,
large lake, lagoon, reflecting pool, canals, tropical planting, banana palms,
rainforest, pine trees, deciduous autumn trees, grass lawns everywhere, snow,
mountains, high-rise towers adjacent, glass skyscrapers, solar panel field,
futuristic white blob architecture, parametric voronoi shell, people wearing
winter clothing, text, watermark, logo, signature, distorted anatomy,
duplicated limbs, oversaturated HDR, fisheye distortion
```

**House style for all ten** — append to every generation:

```
STYLE: photoreal architectural visualisation, physically accurate daylight,
Dubai desert palette — warm sand, bleached limestone, terracotta, deep planting
green, weathered bronze. Natural human scale. Restrained and credible, not
sci-fi. Shot on 35mm, f/8, natural depth of field.
```

---

## 01 · Aerial, golden hour — **the hero image**
*Slots 05, 02 · aspect 16:9 · this is the one image most people will remember*

```
Aerial three-quarter view of a 15,000 square metre neighbourhood park in Al Safa
2, Dubai, late afternoon golden hour, long soft shadows.

The park is organised by ONE CONTINUOUS CURVED SHADE CANOPY — a single arc of
141 metre radius sweeping the full width of the site, bowing convex toward the
south so its hollow opens to the north. The canopy is an 18 metre wide steel
gridshell lattice standing 4.5 metres high on slender columns at 6 metre bays,
with a perforated soffit that throws dappled light onto the walkway below. Along
its southern face hangs a 3 metre deep vertical louvre screen of weathered
bronze fins.

Running beneath the canopy's northern edge is a NARROW water channel just 0.9
metres wide — a thin ribbon of moving water, shaded all day, NOT a pond or lake.

Inside the crescent's concave northern hollow sits a sunken palm court: date
palms in a shallow basin reached by wide shallow steps. Radial pedestrian alleys
3 metres wide fan outward from the arc like spokes, each one a radius of the
same circle, dividing the park into wedge-shaped rooms — a children's play area
of sculpted sand dunes, a family picnic grove, a quiet garden, a community
plaza, an open sports lawn, and a small souk of shaded kiosks.

A 438 metre running loop traces the park's perimeter, backed by a planted dune
berm of mounded earth that screens the surrounding streets. 131 desert trees —
ghaf, neem, ficus nitida, date palm and olive — are distributed through the
park, densest along the southern rank.

Beyond the park: low-rise Dubai villa neighbourhood, two storeys, sand-coloured.
Families walking, children playing, people seated in shade.
```

**Passes if:** the canopy reads as ONE arc · the water is a thin line, not a pool
· the palm court is inside the hollow · no towers on the skyline.

---

## 02 · Aerial, blue hour / night
*Slots 05, 07 · aspect 16:9 · the brief explicitly asks for day AND night*

```
Same park, same aerial three-quarter angle, now at blue hour just after sunset.

The single 141 metre radius curved gridshell canopy is lit from within — warm
light washing up into the lattice so the arc reads as a glowing ribbon across
the site. Downlights at each 6 metre bay pool onto the 7 metre walkway. The
narrow 0.9 metre water channel beneath the canopy's northern edge catches and
doubles the light as a thin bright line.

The sunken palm court in the crescent's northern hollow is lit from below, palm
trunks uplit against the darkening sky. The radial alleys are marked by low
bollard lighting. The community plaza is active with an evening gathering. The
running loop is lit at ankle height along the perimeter berm.

Deep blue sky, warm amber artificial light, clear separation between lit paths
and dark planting. Low-rise Dubai villa neighbourhood beyond with scattered
window lights. Families and evening walkers throughout.
```

**Passes if:** it is recognisably the *same* park as 01 · lighting is warm and
restrained, not a nightclub · water still a thin line.

---

## 03 · Eye level beneath the canopy — **the experience shot**
*Slots 05, 07 · aspect 3:2 · this is the image that sells the whole idea*

```
Eye-level view standing on the walkway directly beneath the curved shade canopy,
looking along its length so the arc visibly curves away to the left and out of
frame.

Overhead: an 18 metre wide steel gridshell lattice at 4.5 metres, its perforated
soffit at 12 percent transmittance casting a fine dappled pattern of light and
shadow across the paving — bright pinpoints on warm sand-coloured stone. Slender
columns march away in 6 metre bays. On the right, the southern face carries a 3
metre deep vertical louvre screen of weathered bronze fins, slicing the low
afternoon sun into bands.

On the left, at the canopy's edge, a narrow 0.9 metre water channel runs the
length of the walk — shallow, moving, lined in dark stone, level with the paving.
A child trails a hand in it.

Beyond the channel, the ground drops gently into the sunken palm court with date
palms. Ghaf and neem trees alternate along the walkway edge.

People: a family walking, an older couple seated on a shaded stone bench, a
person jogging past. Midday heat outside the canopy is visible as brightness
beyond its edge — inside it is clearly, comfortably cool.

Strong contrast between the shaded walkway and the bright exposed ground beyond.
```

**Passes if:** the curve is visible · dappled light, not flat shadow · the louvre
is on the right/south · water is a channel at the edge.

---

## 04 · The Oasis Basin — Al Nakhil
*Slots 05, 09 · aspect 3:2*

```
Eye-level view within a sunken palm court in the concave hollow of a curved
shade canopy. The ground drops about 1.2 metres below the surrounding park,
reached by wide shallow limestone steps that double as informal seating.

Date palms rise from a floor of decomposed granite and low desert planting. The
curved canopy arcs overhead along the far edge, its lattice visible against the
sky, the narrow water channel glinting along its lip and feeding a small basin
at the lowest point.

Late afternoon. Warm raking light down the palm trunks. Dappled shade. A few
people seated on the steps, a child on the lower level. Intimate, sheltered,
distinctly cooler than the open park beyond.
```

**Passes if:** clearly sunken · date palms not tropical palms · canopy arc
visible at the edge.

---

## 05 · Community Plaza & Event Lawn
*Slots 01, 07 · aspect 16:9*

```
A community plaza on the convex southern side of a curved shade canopy, early
evening, set up for a neighbourhood event.

Wedge-shaped in plan — its edges are radial alleys converging toward the arc.
Sand-coloured stone paving, shade sails and mature ficus nitida trees along the
edges, movable seating. An open lawn adjoining. Small shaded kiosks — a souk of
timber and bronze stalls — line one edge, selling food and drink.

The curved gridshell canopy passes along the northern edge of the plaza, lit
from within, tying the space back to the park's main spine.

A mixed crowd: families, older residents, teenagers, children. Warm string
lighting. Active but not crowded. Genuine neighbourhood feel, not a commercial
mall.
```

---

## 06 · Children's Dune Play
*Slots 05, 07 · aspect 3:2*

```
An inclusive children's play area built as sculpted sand-coloured dunes — mounded
landforms with embedded slides, climbing nets, tunnels and shaded scramble
structures, in a wedge-shaped area defined by radial pathways.

Separate zones for different ages: a gentle toddler area with low mounds and soft
surfacing in the foreground, taller climbing dunes for older children beyond.
Shade sails and mature neem trees over the seating. Parents seated in shade with
clear sightlines. A drinking fountain and a shaded family seating terrace at the
edge.

Wheelchair-accessible ramped route onto the lowest mound — inclusive design,
visible.

The curved canopy arcs across the background. Late afternoon, warm light,
children playing, safe and joyful.
```

**Passes if:** two distinct age zones visible · accessibility route visible ·
desert-toned, not primary-colour plastic playground.

---

## 07 · The West Gate Majlis — arrival
*Slots 01, 03 · aspect 3:2*

```
The main park entrance, where the curved canopy's western horn breaks through a
planted dune berm to meet the street.

A shaded arrival majlis — a gathering threshold of stone benches under the
canopy's tapering end, framed by ghaf trees. The gridshell narrows and touches
down here. Beyond, the arc sweeps away into the park.

Wayfinding totem in Arabic and English. Bicycle racks and a shaded drop-off bay
at the street edge. Level, barrier-free paving throughout — no steps at the
entrance.

Morning light. People arriving on foot and by bicycle, a family with a pushchair,
an older resident with a walking frame. Welcoming, generous, obviously
accessible.
```

**Passes if:** bicycle parking and step-free access are both visible — these are
brief requirements and this is the render that evidences them.

---

## 08 · Section-perspective through the canopy — *technical/hybrid*
*Slot 04 · aspect 16:9 · supports the section drawing*

```
A cutaway section perspective through the crescent canopy, drawn as a clean
architectural visualisation with a cut plane on the left.

The section shows: a 7 metre wide walkway; an 18 metre wide gridshell canopy
4.5 metres above it on slender columns; a 3 metre deep vertical louvre screen on
the southern (right) face; the 0.9 metre water channel at the northern (left)
edge, level with the paving; the ground sloping left into the sunken palm court.

Sun rays drawn from the upper right at a low winter angle, intercepted by the
louvre; a second set at a steep summer angle intercepted by the canopy soffit.

Human figures for scale beneath the canopy. Trees in elevation behind. Clean,
measured, professional — a technical drawing that is also beautiful. Muted
palette with the shaded zone tinted cool.
```

---

## 09 · The perimeter loop — Al Madar
*Slots 03, 07 · aspect 16:9*

```
Eye-level view along a 438 metre running and walking loop tracing the park's
perimeter, early morning.

A 2.5 metre wide resilient running surface in warm terracotta, curving gently.
On the outer side, a planted dune berm of mounded earth rises to screen the
street beyond — native desert grasses, ghaf and olive trees on the mound. On the
inner side, the park opens up with the curved canopy visible in the middle
distance.

Distance markers set into the surface. Runners, a walking group of older
residents, a parent with a stroller. Long soft morning shadows, cool blue-gold
light. Calm and healthy.
```

---

## 10 · Before / after pair — the argument in one frame
*Slots 01, 11 · aspect 16:9 each · generate as two matched images*

```
IMAGE A — BEFORE:
The existing Al Safa 2 neighbourhood park at midday in summer. A flat, largely
exposed 15,000 square metre site: patchy irrigated grass, a few scattered mature
trees casting small isolated shadows, a plain concrete path, dated play
equipment, no continuous shade anywhere. Harsh overhead sun, bleached colours,
hard black shadows, heat shimmer. The park is empty — nobody is outside. Low-rise
Dubai villas beyond.

IMAGE B — AFTER:
The identical viewpoint, camera position and time of day, transformed. The single
141 metre radius curved gridshell canopy now sweeps across the site, throwing a
continuous band of dappled shade. The narrow water channel runs along its
northern edge. The sunken palm court sits in the hollow. 131 desert trees are
established. The dune berm screens the street.

Same harsh midday summer sun — but now the park is full of people: families
walking, children in the dune play area, people seated in shade. Same light, same
hour, opposite outcome.
```

**Passes if:** the two images share camera position and sun angle exactly. That
match *is* the argument — same day, same hour, different park.

---

## After generating

1. Save to `design/renders/` — `Aerial/`, `Eye_Level/`, `Night/`.
2. Delete anything that fails its acceptance test. A wrong render is worse than
   no render, because it contradicts the drawings.
3. Re-run the pipeline so the website and submission folders pick them up:
   ```bash
   python tools/build_docs.py
   python tools/sync_submission.py
   ```
4. Caption every one **"Artistic impression — illustrative of design intent.
   AI-generated."** and every drawing **"Technical drawing — to scale."**
   The brief invites AI visualisation, so this costs nothing and protects the
   analysis's credibility.
5. Check `docs/index.html` shows the new set, and that no withdrawn image
   reappears.
