# PROJECT PLAN — START HERE

**Al Safa 2 Park · "Falaj Al Safa" · Dubai Municipality AI Park Design Challenge**
Applicant: Mohamed Wasim · Individual Applicant

> **This is the only file you need to read to understand the whole project.**
> Everything else is either a deliverable, code that produces a deliverable, or
> reference material. If any other document contradicts this one, this one is
> right.

---

## 0. The deadline — read this first

| | |
|---|---|
| **Today** | 1 August 2026 |
| **Submission deadline** | **15 August 2026** |
| **Time remaining** | **14 days** |
| Questions & clarifications deadline | 5 August 2026 (4 days) — *if you want to ask DM anything, ask now* |

Source: official Scope of Work, Schedule 5 "Program", and the challenge website.
**The deadline is not today.** There are two full weeks. That is enough time to
fix everything listed in §6, in order, without rushing the work that earns marks.

---

## 1. What the competition actually asks for

### 1.1 Prizes
1st: **AED 100,000** · 2nd: AED 65,000 · 3rd: AED 35,000

### 1.2 How it is judged — this drives every decision below

| # | Criterion | Weight |
|---|---|---|
| 1 | Innovation and Creativity | **20%** |
| 2 | Human-Centered Design, Sustainability and Quality of Life | **20%** |
| 3 | Integration and Effective Use of Artificial Intelligence | **20%** |
| 4 | Quality of Design and User Experience | **15%** |
| 5 | **Feasibility and Implementation Potential** | **20%** |
| 6 | Quality of Presentation and Communication | **5%** |

Scored 1–10 per criterion. Then: **jury shortlists → the community votes for the
winner.**

**Two things this table tells us that change the plan:**

- **Feasibility is worth 20% — the same as AI, four times as much as presentation.**
  The brief requires the design to work within a **AED 35 million** budget. Right
  now costed at AED 26.97 M — 77.1% of budget, with AED 8.03 M of headroom.
- **Presentation is only 5%.** Beautiful renders matter — but mostly through
  criteria 1 and 4, and through the *community vote*, not through criterion 6.
  Renders are worth fixing (see §7) — and they are now the single biggest gap,
  because every compliance item in §6 is closed.

### 1.3 The AED 35 million budget
> *"Participants are also required to consider the project's total implementation
> budget of AED 35 million and demonstrate the feasibility, scalability, and
> practicality of their proposals within this financial framework."*

### 1.4 What must be uploaded — 12 slots, **one PDF each**

Every slot takes **a single file**, max 100 MB.

| # | Slot | Accepts | Mandatory |
|---|---|---|---|
| 1 | Design Narrative & Concept | PDF | ✅ |
| 2 | Neighborhood Park Preliminary Design Masterplan | PDF | ✅ |
| 3 | Concept Plans and Spatial Organization Diagrams | PDF, **DWG** | ✅ |
| 4 | Key Sections & Elevations | PDF, **DWG** | ✅ |
| 5 | 3D & Spatial Visualizations | PDF | ✅ |
| 6 | AI Methodology Report | PDF | ✅ |
| 7 | User Experience & Activation Strategy | PDF | ✅ |
| 8 | Sustainability Concept & Strategy | PDF | ✅ |
| 9 | Material & Landscape Palette | PDF | ✅ |
| 10 | Complete Design Report | PDF | ✅ |
| 11 | Site Analysis & Human-Centric Research | PDF | ✅ |
| 12 | One-minute concept animation | ZIP, PDF | optional |

Plus 4 declarations to tick.

> ### ✅ RESOLVED — the 12 upload files now exist
> `submission/` holds twelve *folders*; the form takes one PDF per slot.
> `python tools/build_submission_pdfs.py` merges each into a single cover-paged
> PDF in `UPLOAD_THESE_12_FILES/`. Re-run it after any content change.

### 1.5 Required park program (from the brief)
Arrival & gateway · secondary access · universal accessibility · **bicycle parking**
· **drop-off** · walking paths · **jogging track ~1 km** · shaded connections ·
wayfinding · inclusive playground for **different age groups** · nature play ·
family seating · fitness stations · multipurpose lawn · community plaza · event
lawn · picnic areas · social seating · native planting · tree canopy ·
biodiversity · sensory landscape · shaded seating · quiet contemplation ·
**public restrooms** · **drinking fountains** · café/kiosk · **service &
maintenance facilities** · **waste and recycling stations** · water-sensitive
design · efficient irrigation · efficient lighting · smart technologies ·
monitoring systems.

Also explicitly required as a deliverable:
> *"The proposal shall include a **Commercial and Service Facilities Map**
> illustrating the location, distribution, and integration of the proposed
> commercial and service uses."*

---

## 2. The design — what we are proposing

**One arc.** A crescent of shade, 141 m in radius, sweeps across the 15,000 m²
site. A water channel runs beneath its northern drip line. Every room in the park
is struck off the same centre, so no room is a rectangle and every room faces the
crescent square-on.

| Element | | |
|---|---|---|
| **Al Hilal** | the Crescent Canopy | 18 m gridshell over a 7 m walk, 3 m southern louvre |
| **Al Falaj** | the water channel | 0.9 m wide, on the drip line so it is shaded all day |
| **Al Nakhil** | the Oasis Basin | sunken palm court in the crescent's concave side |
| **Al Sikkak** | the alleys | radial, 3 m wide, each one a radius of the same arc |
| **Al Madar** | the perimeter loop | 438 m running circuit, tree-shaded |
| **Al Kathib** | the dune berm | planted earth against the roads — noise, glare, heat |

### The measured result

| Metric | Value |
|---|---|
| Annual daylight hours modelled | 4,402 |
| Comfortable daylight hours — **today** | **44.5%** |
| Comfortable daylight hours — **as designed** | **64.6%** |
| Mean heat-index reduction under canopy | **7.13 °C** |
| Peak heat index, exposed → shaded | 56.8 °C → **48.7 °C** |
| Crescent Walk shaded (canopy + louvre) | **87.3%** |
| Site-wide mean shade | 34.1% |
| Trees planted | 131 |

Every number is regenerated by `python run_analysis.py`. None is typed by hand.

### Why an arc (the part that was solved, not styled)
A straight canopy presents one orientation — when a sun angle defeats it, it
defeats the whole length at once. An arc changes heading continuously. Swept
against the 8,760-hour solar model:

| Plan form | Mean cover | Hours with **no shade anywhere** |
|---|---|---|
| Straight east–west bar | **87.4%** | 330 |
| Arc, sagitta 14 m | 86.6% | 62 |
| **Arc, sagitta 18 m** | 85.9% | **52** ← adopted |
| Closed elliptical loop | 79.1% | 89 |

The straight bar shades *more ground on average*. The crescent is adopted because
it removes six-sevenths of the hours in which the route offers nowhere to stand.
That trade is stated in the direction that is not flattering — which is itself
worth marks under criterion 3.

---

## 3. The four AI models

| Model | Task | Result | Why it is a real problem |
|---|---|---|---|
| **M1a** Random Forest | Shade surrogate | R² 0.998 | Learns a slow ray-traced simulation from cheap plan geometry |
| **M1b** Neural network | Shade surrogate (deployed) | R² 0.994 | Differentiable → usable inside a layout optimiser |
| **M2** Gradient Boosting | Comfort band (4-class) | 97.5% acc | Temperature and humidity **withheld** — sees only sun position and calendar |
| **M3** K-Means | Microclimate regimes | k=2 by silhouette | k is *selected*, not chosen to look tidy |

The discipline that makes these credible: **the target must not be recoverable
from the inputs by algebra.** Heat index is a closed-form function of temperature
and humidity, so predicting it from temperature and humidity is arithmetic in a
lab coat. M2 is denied both and still reaches 97.5% — which means park operations
can be scheduled from an almanac with **no sensor network**.

---

## 4. Folder structure — what every folder is for

### The only four things you actually touch

| | |
|---|---|
| 📄 **`PROJECT_PLAN.md`** | this file — what to do and in what order |
| 📥 **`00_BRIEF/`** | what Dubai Municipality asked for |
| 📤 **`UPLOAD_THESE_12_FILES/`** | **the 12 PDFs you drag into the form.** Nothing else gets uploaded |
| 🎨 **`RENDER_PROMPTS.md`** | the prompts for generating the visuals |
| 🔗 **`LINKS.md`** | every public URL, and how to make them live |

Everything else below is machinery that produces those files. You never need to
open it unless you are changing the design.

> **Why the code folders are not renamed with numbers.** `src/`, `data/`,
> `tools/`, `tests/`, `figures/`, `models/`, `docs/`, `design/` and `submission/`
> are referenced by name in 6–18 code files each. Renaming them 14 days before a
> deadline, on a pipeline that currently passes 38 tests, would risk breaking the
> thing that generates the submission in order to make a folder list prettier.
> `submission_upload/` was renamed to `UPLOAD_THESE_12_FILES/` because exactly
> one file referenced it — that one was worth doing.


```
AL SAFA/
│
├── PROJECT_PLAN.md         ⭐ THIS FILE — start here
├── README.md                the design argument, written for a juror (GitHub front page)
├── DATA_SOURCES.md          every data source, its period, and its limitations
├── PUSH_TO_GITHUB.md        how to publish the repo + what must stay private
│
├── 00_BRIEF/               ⭐ THE OFFICIAL COMPETITION DOCUMENTS
│                             scope of work, parks manual, site DWG, masterplan
│                             (UPLODED DOCUMENT DETAILS.txt has your email and
│                              mobile — it is gitignored, never pushed)
│
├── submission/             ⭐ THE DELIVERABLE — 12 folders → 12 upload PDFs
│   01…12_*/                  each with a MANIFEST.md
│
├── data/
│   ├── raw/                  6 documented source datasets + sources.json
│   └── processed/            8,760-hour climate series, 15,000-cell grid
│
├── src/                     THE ENGINE
│   ├── plan.py                ⭐ single source of the crescent geometry —
│   │                           every drawing, figure and film reads THIS
│   ├── climate.py             8,760-hr year rebuilt from 39yr NCM normals
│   ├── solar.py               sun position + shadow ray-tracing
│   ├── dataset.py             assembles the ML training tables
│   ├── models.py              the four models
│   ├── viz.py / figures.py    the ten analysis charts
│   ├── drawings.py            section, elevation, circulation, planting
│   └── boards.py              the two presentation boards
│
├── figures/                 fig01–fig10, one visual system
├── design/
│   ├── visuals/               generated technical drawings
│   ├── boards/                the two presentation boards
│   └── renders/               AI-generated photoreal illustrations
├── models/                  trained-model metrics + headline numbers
├── notebooks/               the complete analysis, outputs embedded
├── reports/                 written reports (Word + PDF)
├── docs/                    the public website / analytics portal
├── tests/                   33 pipeline checks + portal + film tests
├── tools/                   the sync + build scripts
│
├── archive/
│   ├── phases/                the ten phase folders — real working history
│   └── withdrawn_visuals/     images withdrawn on purpose (see §8)
│
└── _TRASH/                  nothing here is part of the submission. Gitignored.
                             Delete the folder once the upload is done.
```

**The rule that makes the whole thing trustworthy:** everything in `figures/`,
`design/visuals/`, `docs/` and `submission/` is derived from `data/` and `src/`.
Nothing downstream is hand-drawn or hand-typed. Change an input, re-run, and
every chart, drawing and figure moves with it — or a test fails loudly.

---

## 5. Phase by phase — what was done, and the steps inside each

### Phase 0 · Source material → `00_BRIEF/`
1. Downloaded the DM scope of work, general terms, and the Neighbourhood Parks manual.
2. Extracted both PDFs to plain text so they are greppable (`SCOPE_OF_WORK_FULL_TEXT.txt`).
3. Captured the upload form's exact slot list and accepted formats.
4. Obtained the site DWG and the existing-park masterplan.

### Phase 1 · Site & Context Analysis → `archive/phases/01_*`
1. Urban context — surrounding land use, access, connectivity, catchment.
2. Climate — 39 years of NCM monthly normals: temperature, humidity, wind, sun path.
3. Reconstructed an **8,760-hour year** from those normals (`src/climate.py`),
   verified back against them to within **0.39 °C**.
4. Solar geometry for every hour via NREL/pvlib (`src/solar.py`).
5. Shadow analysis — shadow length = height ÷ tan(elevation).
6. Catchment & demand — **7,640 residents** within a 10-minute walk (DSC 2023).
7. SWOT of the existing park.
→ **Output:** the knowledge base every later decision is checked against.

### Phase 2 · Problem Definition → `archive/phases/02_*`
1. Turned Phase 1 findings into a list of problems.
2. **Scored each by severity** rather than listing them flat.
3. Ranked → thermal discomfort dominates everything else.
→ **Output:** the justification for making shade the organising idea.

### Phase 3 · Opportunity & Objectives → `archive/phases/03_*`
1. Converted the ranked problems into **measurable targets**.
2. Set the comfort-hours target that the design is later tested against.
→ **Output:** the numbers §2's results table is scored against.

### Phase 4 · Concept Development → `archive/phases/04_*`
1. Generated multiple concepts.
2. Scored them against weighted criteria.
3. Selected the crescent canopy.
→ **Output:** design narrative + concept diagrams.
> ⚠️ State the **weights explicitly** in the slot-01 narrative. A juror who
> suspects the weights were reverse-engineered to pick a winner discounts the
> whole section.

### Phase 5 · Masterplan Development → `archive/phases/05_*`
1. Room-by-room zoning, every room struck off the crescent's centre.
2. Areas taken as the **shoelace area of the drawn polygon** — measured, not authored.
3. Schedule closes on exactly **15,000 m²**, asserted by a test.
→ **Output:** `figures/fig10_masterplan.png`, `data/raw/site_zoning_schedule.csv`.

### Phase 6 · Detailed Design → `archive/phases/06_*`
1. Solved the canopy section against the shadow geometry — 7 m walk, 18 m
   gridshell at 4.5 m, 3 m southern louvre.
2. Elevations, bay rhythm, 12% soffit transmittance.
3. Planting plan — 131 trees, 5 species, drawn at mature canopy radius.
→ **Output:** `design/visuals/section_crescent.png`, `elevation_crescent.png`, `planting_crescent.png`.

### Phase 7 · Performance & Sustainability → `archive/phases/07_*`
1. Water balance (~5,700 m³/yr, 43% recycled).
2. Carbon — 2.1 tCO₂e/yr across 131 trees.
3. Energy — canopy PV covers **~13% of load: a deficit, not a surplus.**
   *(An earlier draft called this power sold back to the grid. It was corrected.)*
4. Shade performance by zone.
→ **Output:** the sustainability strategy.

### Phase 8 · User Experience & Activation → `archive/phases/08_*`
1. K-Means microclimate regimes.
2. Mapped comfort by hour × month.
3. Programming targets **late afternoon, spring and autumn**. Summer midday is
   deliberately not programmed outdoors.
→ **Output:** the activation strategy.

### Phase 9 · AI Workflow & Visualization → `archive/phases/09_*`
1. Documented the four models and the anti-leakage discipline.
2. Generated the photoreal renders.
3. Built the analytics portal and the 60-second concept film.
→ **Output:** the AI methodology report — **the differentiator** (criterion 3, 20%).

### Phase 10 · Submission Assembly → `submission/`
1. Mapped every report and visual onto the 12 upload slots.
2. Wrote a `MANIFEST.md` per slot naming each file and what produced it.

### Phase 11 · The redesign — the biggest change in the project
1. A geometric check found the original straight-spine claim of **99.2% shade**
   does not survive: at low sun the shadow slides clean off the walkway.
2. **The plan was redrawn rather than the number patched** — one crescent, radial
   rooms, all struck off one centre.
3. `src/plan.py` became the single source of that geometry.
4. Figures, drawings, portal and film were all rewired to read it.
5. The re-solved section measures **87.3%**, regenerated by code every run.
6. Three fabricated images were withdrawn (see §8).

### Phase 12 · Repository cleanup
1. Removed **55.6 MB of byte-identical duplicates**, each verified by MD5 against
   a surviving canonical copy before deletion.
2. Retired two dead website pages whose links pointed at an unpushed repo.
3. Assembled `docs/` into one site that actually shows the drawings.
4. Promoted the official brief to `00_BRIEF/`; moved all dead weight to `_TRASH/`.
5. Verified: 33 pipeline + 64 portal + film frame tests all pass.

### Phase 13 · Submission hardening — **NOT DONE YET.** This is §6.

---

## 6. What is left — in priority order

### ✅ Done (all P0 compliance items are closed)

| Task | Result |
|---|---|
| Merge 12 slots into 12 single PDFs | `UPLOAD_THESE_12_FILES/` — 90 pages, 22.9 MB, all under the 100 MB ceiling |
| Strip the `[AI DRAFT]` markers | **Zero** remain. The build fails if one reappears |
| Rewrite the reports onto the crescent | 9 reports generated from live data by `tools/build_reports.py` |
| Cost model against AED 35 M | **AED 26.97 M — 77.1%**, AED 8.03 M headroom, 5 new tests |
| Commercial & Service Facilities Map | Required deliverable, now exists — 20 facilities placed |
| Restrooms, fountains, bike parking, drop-off, waste | All placed via `plan.facilities()` |
| Fill the three phases with no analysis | Ph3 objectives table · Ph4 plan-form sweep · Ph8 personas + activation calendar |
| Renders that contradicted the plan | All 6 withdrawn to `_TRASH/`; boards and portal self-heal |

### 🔴 What only you can do

| # | Task | Why it matters |
|---|---|---|
| 1 | **Generate the renders** from [`RENDER_PROMPTS.md`](RENDER_PROMPTS.md) in Antigravity | You currently have **no** visualisation of the crescent. Prompts 01, 02, 03 first — they fix Board 1 and slot 05. Save over the original filenames and re-run the pipeline |
| 2 | **Open the DWG** in `00_BRIEF/` and confirm the real boundary | The 150 × 100 m envelope is an assumption. Every area figure depends on it |
| 3 | **Record the 60-second film** to MP4 | Slot 12. Optional, but the shortlist goes to a community vote, and a community votes on what it can see |
| 4 | **Read the 9 reports and approve the content** | They are generated, but the design judgement in them is yours to stand behind |
| 5 | Push to GitHub and put the links in slot 06 | See §9. Confirm the PII file is not pushed first |

### 🟡 Optional polish

| # | Task |
|---|---|
| 6 | Attach the marked-up DWG to slots 03 and 04 (the form accepts DWG there) |
| 7 | State the concept-scoring weights explicitly in slot 01 |
| 8 | Check the 9-page legacy PDF in slot 05 for embedded withdrawn renders |

## 7. The render problem, and how to fix it

**Your instinct is right, and it is the most visible weakness in the submission.**
The photoreal renders show a park that is not the park in the drawings. A juror
comparing slot 02 (masterplan) with slot 05 (visualisations) sees two different
projects, and the analysis loses its authority.

The fix is not to drop the renders — it is to **regenerate them from the actual
geometry**. Every prompt must carry the crescent's real numbers.

👉 **The full prompt sheet is `RENDER_PROMPTS.md`.** It contains ten
generation-ready prompts, each locked to the measured design, plus negative
prompts and the acceptance test each image must pass before it goes in.

Non-negotiables for every render:
- The canopy is **one continuous arc**, 141 m radius, bowing **convex south** — never straight, never a full ring.
- Water is a **0.9 m channel** under the canopy edge — **not a lagoon**, not a lake. The sustainability argument in slot 08 depends on it being small.
- The palm court sits in the crescent's **concave (north) side**.
- Trees are **Ghaf, Neem, Ficus nitida, Date Palm, Olive** — desert species, not tropical.
- Every render must be captioned **"artistic impression — illustrative of design intent"**, with drawings captioned **"technical drawing, to scale"**.

---

## 8. Two corrections this submission makes to itself

Keep both. They are worth marks under criterion 3, and they are the reason the
rest of the numbers are believable.

1. **A withdrawn shade claim.** An earlier version claimed **99.2%** annual shade
   on a flat 9 m canopy over a 9 m walkway. It does not survive a geometric check.
   It was withdrawn, the section re-solved, and it now measures **87.3%**.
2. **Three withdrawn images.** A "PET/CFD thermal comfort analysis" where no CFD
   was run; a "Satellite NDVI Analytics" whose raster is numpy noise; and a
   "Generative Parametric Voronoi Canopy — Algorithmic Solar Optimization" in
   which nothing was optimised. All three are in `archive/withdrawn_visuals/`
   with a README explaining each.

> Say both out loud in the AI Methodology Report. A submission that audits itself
> in public is more credible than one that never had to.

---

## 9. The GitHub / portal strategy

This is a good idea and it is worth doing — **but as supporting evidence, not as
a substitute for the PDFs.** Jurors evaluate the uploaded files; assume some will
never click a link.

1. Push the repository public (see `PUSH_TO_GITHUB.md`).
   **Confirm `00_BRIEF/UPLODED DOCUMENT DETAILS.txt` is not pushed — it has your
   email and mobile number.** It is gitignored; verify with `git ls-files | grep UPLODED`
   returning nothing before you push.
2. **GitHub renders PDFs in-browser**, so a link to a PDF in the repo opens
   directly — no download. Links will resolve.
3. Enable **GitHub Pages** on `docs/` → the analytics portal becomes a live URL.
4. Put both links on **page 1 of the AI Methodology Report (slot 06)**:
   > *The complete analysis — data, code, models and tests — is published at
   > `github.com/<user>/al-safa-2-park-ai` and runs end to end with
   > `python run_analysis.py`. Live analytics portal: `<pages-url>`.*
5. Optionally mirror the 12 PDFs to Google Drive as a backup link.

Most entries cannot offer a reproducible pipeline. It costs one line and it is
the strongest single sentence available under criterion 3.

---

## 10. How to run everything

```bash
pip install -r requirements.txt

python run_analysis.py           # data → models → figures        (~3 min)
python -m src.drawings           # plan geometry → design/visuals/
python -m src.boards             # → design/boards/
python tools/build_docs.py       # → docs/ website
python tools/sync_portal.py      # → portal analytics data
python tools/sync_film.py        # → the 60-second film
python tools/sync_submission.py  # → submission/01–12
```

Verify before trusting any number:

```bash
python -m tests.test_pipeline    # 33 checks
node docs/_PORTAL/selftest.js    # 64 checks
node tests/test_film.js          # every frame of the film
```

**If you change the design, re-run all of it.** `src/plan.py` is the single source
of geometry — the figures, drawings, portal and film all read it, so they move
together or the tests fail loudly.

---

## 11. Pre-submission checklist

| | Item |
|---|---|
| ☐ | 12 slots merged into 12 single PDFs |
| ☐ | Cost model closes against AED 35M |
| ☐ | Commercial & Service Facilities Map produced |
| ☐ | Word reports describe the **crescent**, not the straight spine |
| ☐ | 99.2% replaced by 87.3% everywhere |
| ☐ | Site boundary confirmed against the DWG |
| ☐ | Restrooms, fountains, bike parking, drop-off, waste stations in the plan |
| ☐ | Jogging loop length justified |
| ☐ | Renders regenerated and captioned "artistic impression" |
| ☐ | Concept-scoring weights stated in slot 01 |
| ☐ | Solar array **deficit** wording confirmed in slot 08 |
| ☐ | 60-second animation recorded to MP4 |
| ☐ | Repo pushed; PII confirmed absent; links in slot 06 |
| ☐ | All four declarations ticked |
| ☐ | **Submitted before 15 August 2026** |
