# The 12 submission files — detailed guide

*Al Safa 2 Park · The Shaded Spine · Dubai Municipality AI Park Design Challenge*
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

The argument. What is wrong with Al Safa 2 Park today, and what the Shaded Spine
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
> `archive/source_files/Al Safa Park 2 Plan (5).dwg` and confirm the real boundary
> before submitting. **Every area figure in the submission depends on this.**

---

## 03 · Concept Plans & Spatial Organisation Diagrams
**Portal accepts:** PDF, DWG · **Status:** ✅ ready

How the park is organised — rooms, thresholds, and the spine that links them.

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
| **Files** | `section_shaded_spine.png`, `elevation_shaded_spine_long.png`, `elevation_entrance_gateway.png`, `parametric_canopy_mesh.png`, `Phase6_Detailed_Design_Report.pdf` |
| **Backed by** | Canopy height 5.5 m and width 9 m, driven by the shadow geometry in [`src/solar.py`](../src/solar.py) |
| **Key relationship** | Shadow length = height ÷ tan(solar elevation). At Dubai's 87.4° summer noon a 6 m tree casts a 0.19 m shadow; at 20° it casts 16.5 m — which is *why* the canopy alone cannot carry winter shade, and why the tree avenue exists |

---

## 05 · 3D & Spatial Visualisations
**Portal accepts:** PDF · **Status:** ⚠️ check format

| | |
|---|---|
| **Files** | `Al_Safa_2_Park_3D_Spatial_Visualizations.pdf` (8.6 MB) plus aerial day/night, eye-level spine and plaza, thermal comfort heatmap |
| **Backed by** | Renders are AI-generated illustrations; the **thermal comfort heatmap is computed**, not illustrated — see [`figures/fig04_site_comfort_map.png`](../figures/fig04_site_comfort_map.png) |

> ### ⚠️ The renders show a different park from the plans
>
> This is the most serious unresolved issue in the submission. The photoreal JPGs
> show a **curved, oval park with a large water lagoon** under a hexagonal lattice
> shell. The plans, the diagrams and **every number in the analysis** describe a
> **rectangular 150 × 100 m site with a straight 140 m spine and no water**.
>
> They are not two views of one design. A juror will see it immediately — and the
> lagoon also contradicts the water-scarcity argument in slot 08 (5,700 m³/yr
> irrigation, 43% recycled).
>
> **Also:** `aerial_day.png`, `aerial_night.png` and the `eyelevel_*.png` files are
> script-drawn diagrams sitting next to photoreal renders of the same subject.
> They are the weakest images in the submission and they make the mismatch louder.
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
3. **The correction.** The project revised its own headline shade figure downward
   from 99.2% to 69.6% when a geometric check contradicted it. Say so explicitly.

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

> **Update before submitting.** This report still carries the withdrawn **99.2%**
> shade figure. Replace it with **69.6% (canopy + tree avenue)** and add a line
> explaining the revision. The `.docx` is editable — open it in Word and change the
> text directly. The corrected reasoning is in [`README.md`](../README.md).

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

The film runs exactly 60 seconds across five scenes: the heat (0–10s), the spine
building itself (10–25s), a walk beneath the canopy (25–40s), the computed
comfort map resolving (40–50s), and the park in evening use (50–60s).

**To turn it into the MP4 the portal wants:**

1. Open `concept_film.html` full-screen in a browser.
2. Start a screen recording — `Win + Alt + R` on Windows, `Shift + Cmd + 5` on macOS.
3. Press **Restart** and let all sixty seconds run.
4. Stop, trim the ends, add a voiceover if you want one.
5. Upload the MP4.

This slot is **optional** on the portal, but it is the highest-leverage item you
have: the shortlist goes to a **community vote**, and a community votes on what
it can see, not on an R² score.

> The film deliberately shows the *analysed* scheme — straight spine, rectangular
> site, no water feature. See the note under slot 05 about why that matters.

---

## Pre-submission checklist

| | Item |
|---|---|
| ☐ | **Open the DWG** and confirm the site boundary — every area figure depends on it |
| ☐ | Replace **99.2% → 69.6%** in the Complete Design Report and anywhere else it appears |
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
> `github.com/wasimmisaw437/al-safa-2-park-ai` and runs end to end with
> `python run_analysis.py`.*

Most entries cannot offer that. It costs one line.
