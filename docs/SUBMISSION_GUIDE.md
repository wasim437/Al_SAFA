# The 12 submission files — detailed guide

*Al Safa 2 Park · Falaj Al Safa · Dubai Municipality AI Park Design Challenge*
**Deadline: 15 August 2026**

This is the reference for what goes into each of the twelve upload slots on the
Dubai Municipality portal: what the file is, what is inside it, **which analysis
backs it**, the format the portal will accept, and what still needs doing.

Applicant: Mohamed Wasim · Individual Applicant

> Contact details (email, mobile) are entered directly on the Dubai Municipality
> portal at submission time and are deliberately **not** recorded in this
> repository, which is public.

---

## How to read the "Backed by" column

The competition asks participants to show how AI supported the design. A report
that asserts a number is weak; a report whose number can be traced to a dataset
and a piece of runnable code is strong. Each slot below names the analysis that
stands behind it, so that if a juror asks *"where does 64.6% come from?"* the
answer is a file path, not an opinion.

---

## 01 · Design Narrative & Concept
**Portal accepts:** PDF · **Status:** ✅ ready

The argument. What is wrong with Al Safa 2 Park today, and what Falaj Al Safa
does about it.

| | |
|---|---|
| **Files** | `Phase3_Opportunity_and_Objectives_Report.pdf`, `Phase4_Concept_Development_Report.pdf` |
| **Backed by** | Ranked problem severity model; three concepts scored against weighted criteria |
| **Key claim** | Comfortable daylight hours rise from **44.5% → 64.6%** |
| **Evidence** | [`notebooks/`](../notebooks/AL_SAFA_2_PARK_COMPLETE_ANALYSIS.ipynb) §12, [`figures/fig02_comfort_bands.png`](../figures/fig02_comfort_bands.png) |

> **Before submitting:** the concept scoring is weight-sensitive. State the
> weighting explicitly in the narrative — a juror who suspects the weights were
> chosen to make Concept A win will discount the whole section.

---

## 02 · Preliminary Design Masterplan
**Portal accepts:** PDF · **Status:** ✅ ready

The plan at scale.

| | |
|---|---|
| **Files** | `Phase5_Masterplan_Development_Report.pdf`, `masterplan_diagram.png` |
| **Backed by** | [`data/raw/site_zoning_schedule.csv`](../data/raw/site_zoning_schedule.csv) — 14 zones summing to exactly 15,000 m² |
| **Verification** | Asserted in [`tests/test_pipeline.py`](../tests/test_pipeline.py); the build fails if the schedule stops summing to the site area |
| **Figure** | [`figures/fig10_masterplan.png`](../figures/fig10_masterplan.png) — drawn from the *same* geometry the models use |

> ⚠️ **Open item.** The 150 × 100 m site envelope is an **assumption**. Open
> `00_BRIEF/Al Safa Park 2 Plan (5).dwg` and confirm the real boundary
> before submitting. **Every area figure in the submission depends on this.**

---

## 03 · Concept Plans & Spatial Organisation Diagrams
**Portal accepts:** PDF, DWG · **Status:** ✅ ready

How the park is organised — the crescent, the radial alleys, and the rooms between them.

| | |
|---|---|
| **Files** | `circulation_diagram.png`, `masterplan_diagram.png`, `Phase4_Concept_Development_Report.pdf` |
| **Backed by** | Zone adjacency and circulation hierarchy; walk-distance analysis |
| **Note** | The portal accepts DWG here — attaching the marked-up DWG alongside the PDF is worth doing if time allows |

---

## 04 · Key Sections & Elevations
**Portal accepts:** PDF, DWG · **Status:** ✅ ready

| | |
|---|---|
| **Files** | `section_crescent.png`, `elevation_crescent.png`, `Phase6_Detailed_Design_Report.pdf`, `MANIFEST.md` |
| **Backed by** | Canopy height 5.5 m and width 9 m, driven by the shadow geometry in [`src/solar.py`](../src/solar.py) |
| **Key relationship** | Shadow length = height ÷ tan(solar elevation). At Dubai's 87.4° summer noon a 6 m tree casts a 0.19 m shadow; at 20° it casts 16.5 m — which is *why* the canopy alone cannot carry winter shade, and why the tree avenue exists |

---

## 05 · 3D & Spatial Visualisations
**Portal accepts:** PDF · **Status:** ⚠️ check format

| | |
|---|---|
| **Files** | `Al_Safa_2_Park_3D_Spatial_Visualizations.pdf` (8.6 MB), the two presentation boards, and three photoreal renders |
| **Backed by** | Renders are AI-generated illustrations; the **thermal comfort heatmap is computed**, not illustrated — see [`figures/fig04_site_comfort_map.png`](../figures/fig04_site_comfort_map.png) |

> ### The render/plan mismatch — mostly resolved, and worth reading
>
> This used to be the most serious unresolved issue in the submission. The
> photoreal JPGs showed a **curved park with a sweeping shell and standing water**;
> the plans and every number in the analysis described a **rectangular grid of
> rooms with a straight spine and no water at all**. They were not two views of one
> design, and a juror would have seen it immediately.
>
> The design was changed rather than the renders. The plan is now a single
> crescent with a sunken palm court and a running water channel, which is the same
> language the renders speak. `masterplan_aerial_golden_hour.jpg` in particular
> now reads as the scheme rather than as a different project.
>
> **What is still not reconciled, and should be said out loud:**
>
> - The renders show **more standing water** than the design has. Al Falaj is a
>   0.9 m recirculating channel — about 105 m² of water surface, deliberately set
>   under the canopy's drip line to cut evaporation. It is not a lagoon, and the
>   water-scarcity argument in slot 08 depends on it not being one.
> - The site is still drawn as a **rectangle**; the renders imply a curved
>   boundary. That is pending the DWG.
> - The renders remain **AI-generated illustrations**. They should be captioned as
>   such. Nothing in slot 05 is presented as analysis.
>
> **Three ways out, in order of strength:**
> 1. Regenerate the photoreal renders to match the analysed scheme, so plans,
>    renders and numbers all describe one park.
> 2. Redo the analysis geometry to match the curved render — defensible, but it
>    invalidates the current shade, comfort and cost figures until re-run.
> 3. Drop the weak script-drawn PNGs, keep the photoreal set, and caption them
>    *"artistic impression — illustrative of concept intent"* with the plans
>    labelled *"technical drawing, to scale"*. Cheapest; the mismatch remains.
>
> The 60-second film in slot 12 already shows the **analysed** scheme, so it is
> consistent with the numbers.

---

## 06 · AI Methodology Report
**Portal accepts:** PDF · **Status:** ✅ ready — **and this is the differentiator**

This is the slot the challenge exists for. Most entrants will describe prompting
an image generator. This submission can show a reproducible analysis pipeline.

| | |
|---|---|
| **Files** | `Phase9_AI_Workflow_and_Visualization_Report.pdf`, `Phase1.12_AI_Analysis_Report.pdf` |
| **Backed by** | The entire [`notebooks/AL_SAFA_2_PARK_COMPLETE_ANALYSIS.ipynb`](../notebooks/AL_SAFA_2_PARK_COMPLETE_ANALYSIS.ipynb) |
| **Four models** | Random Forest + neural-network shade surrogate (R² 0.995); Gradient Boosting comfort classifier (97.5%); K-Means microclimate regimes |
| **Reproducibility** | `python run_analysis.py` regenerates every number; `python -m tests.test_pipeline` runs 23 correctness checks |

**Put these three points in the report, in this order:**

1. **The surrogate model.** Ray-tracing annual shade across 15,000 ground cells is
   slow and must be re-run for every design variation — that cost is what stops a
   designer exploring. A neural network trained on the simulation answers in
   milliseconds instead of minutes. That is AI changing how the design was made,
   not decorating it afterwards.
2. **The leakage discipline.** The comfort classifier is denied temperature and
   humidity, because the heat index is a closed-form function of them and
   including them would make the task algebra. It reaches 97.5% from sun position
   and the calendar alone — which means park operations need no sensor network.
3. **The corrections.** The project revised its own headline shade figure downward
   from 99.2% when a geometric check contradicted it, then re-solved the section
   and re-measured it at 87.3%. It also withdrew three images that presented
   invented data as measurement. Say both out loud — a submission that audits
   itself in public is more credible than one that never had to.

---

## 07 · User Experience & Activation Strategy
**Portal accepts:** PDF · **Status:** ✅ ready

| | |
|---|---|
| **File** | `Phase8_User_Experience_and_Activation_Report.pdf` |
| **Backed by** | K-Means microclimate regimes; catchment of **7,640 residents** within a 10-minute walk (Dubai Statistics Center 2023) |
| **Figure** | [`figures/fig09_diurnal_comfort.png`](../figures/fig09_diurnal_comfort.png) — comfort by hour and month |
| **Design consequence** | Programming targets **late afternoon in spring and autumn**, where the modelled comfort gain concentrates. Summer midday is not programmed outdoors. |

> **Be honest about the demand model.** Visitor numbers are a *scenario*, not a
> prediction — no footfall data exists for this site. It is deliberately excluded
> from the machine learning suite because a model trained on it would only recover
> the assumption that produced it. Say this in the report; it costs nothing and it
> is exactly the kind of restraint a jury rewards.

---

## 08 · Sustainability Concept & Strategy
**Portal accepts:** PDF · **Status:** ✅ ready

| | |
|---|---|
| **Files** | `Phase7_Performance_and_Sustainability_Report.pdf`, `sentinel_ndvi_analytics.png` |
| **Backed by** | Water balance (~5,700 m³/yr, 43% recycled); carbon 2.1 tCO₂e/yr across 131 trees; DEWA tariff AED 8.80/m³ |

> **Keep the energy paragraph honest.** The canopy solar array covers about **13%**
> of the site's lighting and systems load. That is a **deficit, not a surplus**. An
> earlier draft described this shortfall as power sold back to the grid. Stating it
> correctly is not a weakness — a jury that catches an overclaim here will
> re-examine every other number in the submission.

---

## 09 · Material & Landscape Palette
**Portal accepts:** PDF · **Status:** ✅ ready

| | |
|---|---|
| **Files** | `planting_plan.png`, `Phase6_Detailed_Design_Report.pdf` |
| **Backed by** | [`data/raw/species_water_carbon_rates.csv`](../data/raw/species_water_carbon_rates.csv) — 131 trees across 5 species with per-species water and carbon rates |
| **Species** | Neem 58 · Ficus nitida 34 · Ghaf 16 · Date Palm 12 · Olive 11 |
| **Model link** | Permutation importance shows **tree density within 20 m** is the dominant driver of shade — ahead of canopy width. This palette is a *performance* decision, not only an aesthetic one. |

---

## 10 · Complete Design Report
**Portal accepts:** PDF · **Status:** ✅ ready — the flagship

| | |
|---|---|
| **Files** | `Al_Safa_2_Park_Complete_Design_Report.pdf` (2.6 MB) + editable `.docx` |
| **Backed by** | Everything above |

> ### ⚠️ This report describes the superseded scheme
>
> The park was redesigned: a straight spine through rectangular rooms became a
> single crescent with radial rooms, a water channel and a sunken palm court. The
> code, the drawings, the portal and the film are all on the new scheme. **The
> Word documents in `reports/` are not.**
>
> Before submitting, the `.docx` needs: the concept renamed to **Falaj Al Safa**,
> the shade figure changed from the withdrawn **99.2%** to **87.3%** (canopy and
> louvre) / **88.5%** (per m² with the tree avenue), and the room schedule replaced
> with the one in [`data/raw/site_zoning_schedule.csv`](../data/raw/site_zoning_schedule.csv).
> The corrected reasoning is in [`README.md`](../README.md).

---

## 11 · Site Analysis & Human-Centric Research
**Portal accepts:** PDF · **Status:** ✅ ready

| | |
|---|---|
| **Files** | `00_EXISTING_CONDITIONS_KNOWLEDGE_BASE.pdf`, `Phase1.13_Catchment_Demand_Analysis_Report.pdf`, `Phase2_Problem_Definition_Report.pdf` |
| **Backed by** | 39 years of NCM climate normals; NREL solar positions for all 8,760 hours; Dubai Statistics Center 2023 |
| **Data provenance** | [`DATA_SOURCES.md`](../DATA_SOURCES.md) — every source with its period, years of record **and its limitations** |

---

## 12 · Concept Animation Video
**Portal accepts:** ZIP, PDF · **Status:** ✅ **film built — needs screen-recording to MP4**

| | |
|---|---|
| **Files** | `concept_film.html` — the 60-second film, `Concept_Animation_Storyboard.pdf` / `.docx` |
| **Backed by** | Every frame is drawn from the project's own analysis: the same 8,760-hour solar model, the same 150 × 100 m plan geometry, the same 131 trees |

The film runs exactly 60 seconds across five scenes: the site (0–7s), the heat
(7–18s), the crescent building and planting itself while a full computed day
passes over it (18–38s), a walk beneath the canopy at eye level (38–48s), and the
measured comfort result as the park fills at dusk (48–60s).

Its geometry is regenerated from `src/plan.py` by `python tools/sync_film.py`, so
the film cannot drift away from the drawings the way the previous one did.

**To turn it into the MP4 the portal wants:**

1. Open `concept_film.html` in Chrome or Edge.
2. Press **Record the film to a video file** and leave the tab in front.
3. Sixty seconds later `Falaj_Al_Safa_Concept_Film_60s.mp4` downloads on its own
   — 1920 × 1080, sixty seconds **with narration**, about 9 MB.
4. Upload it.

**Narration on / off** beside it records a silent version instead.

The page records the canvas directly rather than the screen, so the file carries
no browser chrome, no desktop behind it, and no dependence on the window size.
Every frame in the film is a pure function of the elapsed time, which is what
makes recording it a matter of reading the canvas rather than filming a monitor.

The voice is four fifteen-second segments cued to 0, 15, 30 and 45 seconds,
embedded in the page as audio data rather than kept in files beside it — a
browser opened on a local file will not load a sibling audio file, and cannot
route one into a recording. Regenerate the embedding with
`python tools/embed_narration.py`. The voice is synthesised; every number it
speaks is the number the analysis produces.

A browser that cannot write MP4 falls back to WebM, and a WebM written this way
carries no duration in its header — it plays, but some players show no timeline.
Convert it with `ffmpeg -i film.webm -c:v libx264 -pix_fmt yuv420p film.mp4`, or
record again in Chrome or Edge.

This slot is **optional** on the portal, but it is the highest-leverage item you
have: the shortlist goes to a **community vote**, and a community votes on what
it can see, not on an R² score.

> The film shows the *analysed* scheme exactly: the same arc, the same 131 trees,
> the same solar model. `node tests/test_film.js` renders every frame and fails on
> any NaN, so a geometry change that breaks it cannot ship quietly.

---

## Pre-submission checklist

| | Item |
|---|---|
| ☐ | **Open the DWG** and confirm the site boundary — every area figure depends on it |
| ☐ | **Rewrite the Word reports** — they still describe the superseded straight-spine scheme |
| ☐ | Replace **99.2% → 87.3%** in the Complete Design Report and anywhere else it appears |
| ☐ | Label renders as *illustrative* and analysis outputs as *computed* in slot 05 |
| ☐ | State the concept-scoring weights explicitly in slot 01 |
| ☐ | Confirm the solar array **deficit** wording in slot 08 |
| ☐ | Export image sheets to PDF where the portal requires PDF |
| ☐ | Produce the 60-second animation (slot 12, optional) |
| ☐ | Review and approve all AI-assisted draft content |
| ☐ | Tick all four declarations on the portal |
| ☐ | **Submit before 15 August 2026** |

---

## One suggestion about the repository link

The AI Methodology Report (slot 06) is the only place a juror can be *shown* that
the analysis is real rather than asserted. Put the repository URL in that PDF, on
the first page:

> *The complete analysis — data, code, models and tests — is published at
> `github.com/wasim437/Al_SAFA` and runs end to end with
> `python run_analysis.py`.*

Most entries cannot offer that. It costs one line.
