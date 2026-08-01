# Al Safa 2 Park — Project Workflow (one file, start to finish)

*Dubai Municipality AI Park Design Challenge · Deadline 15 August 2026*
*Applicant: Mohamed Wasim*

This is the single file that explains **what this project is, what every folder
is for, and what was done in what order** — from raw site documents to a
12-file competition submission. For the design argument itself (why the park
is a crescent), read [`README.md`](README.md). For exactly what goes in each
upload slot, read [`docs/SUBMISSION_GUIDE.md`](docs/SUBMISSION_GUIDE.md). This
file sits above both and explains the machinery that connects them.

---

## 1. The concept, in one paragraph

Al Safa 2 Park is a 15,000 m² neighbourhood park in Dubai that is currently too
hot to use for most of the year. The redesign — **Falaj Al Safa** — is one
continuous crescent-shaped shade canopy, 141 m in radius, with a shaded water
channel on its drip line and every room in the park struck off the same
centre. The claim is not "we made it nicer" — it's **44.5% → 64.6%** of the
year's daylight hours becoming comfortable to stand in, and that number (like
every other number in the submission) is *computed from a model*, not typed
into a report by hand. The whole repository exists to make that computation
reproducible: run one script and every chart, drawing, and headline figure
regenerates from the same source data and the same plan geometry.

---

## 2. The complete folder structure

```
AL SAFA/
│
├── data/                     THE INPUTS — nothing downstream is hand-typed
│   ├── raw/                    6 source datasets + sources.json manifest
│   │                            (climate normals, population, unit rates,
│   │                             zoning, tree species, walk-catchment rings)
│   └── processed/              8,760-hour climate series + 15,000-cell grid
│                                 — generated FROM raw/, feeds the ML models
│
├── src/                      THE ENGINE — one Python package, nine modules
│   ├── plan.py                  ⭐ single source of the crescent's geometry —
│   │                             every other drawing/figure/film reads THIS
│   ├── climate.py               rebuilds an 8,760-hr year from 39yr normals
│   ├── solar.py                 sun position + shadow ray-tracing
│   ├── dataset.py               assembles the ML training tables
│   ├── models.py                the 4 trained models
│   ├── viz.py / figures.py      the 10 analysis charts
│   ├── drawings.py              section, elevation, circulation, planting
│   └── boards.py                the 2 presentation boards
│
├── models/                   trained-model metrics (accuracy, R², etc.)
├── figures/                  fig01–fig10 — every analysis chart, one style
├── design/
│   ├── visuals/                 generated technical drawings (from src/drawings.py)
│   ├── boards/                  the 2 presentation boards
│   └── renders/                 AI-generated photoreal illustrations
│
├── notebooks/                 the complete analysis notebook — start here
│                                 if you want to see the whole pipeline run
│
├── reports/                   WRITTEN reports — human-authored prose (Word/PDF)
│   ├── editable_docx/           Phase 1–9 reports, editable
│   └── pdf/                     same reports, exported
│
├── submission/                ⭐ THE ACTUAL DELIVERABLE — 12 folders, one per
│   01…12_*/                     Dubai Municipality upload slot. Each has a
│                                 MANIFEST.md listing what's inside and why.
│
├── docs/                      the public website / analytics portal
│   ├── index.html               single entry point (the portal)
│   ├── assets/                  renders, figures, drawings, boards — copied
│   │                             in for the site by tools/build_docs.py
│   └── _PORTAL/                 css/js/vendored libs + generated data files
│
├── tests/                     automated verification (not manual checking)
│   ├── test_pipeline.py         33 checks on the data/model pipeline
│   └── test_film.js             renders every frame of the concept film
│
├── tools/                     the scripts that keep everything in sync
│   ├── build_docs.py             → assembles docs/ website
│   ├── sync_portal.py            → refreshes portal analytics data
│   ├── sync_film.py              → regenerates the 60s concept film
│   ├── sync_submission.py        → repopulates submission/01–12
│   ├── organize_repo.py          → dedupes the whole repo (MD5-verified)
│   ├── cull_weak_renders.py      → moves rejected renders to archive/
│   └── restructure.py            → the original folder-restructure tool
│
├── archive/                   EVERYTHING SUPERSEDED — kept, not deleted
│   ├── phases/                   the original 10-phase working folders —
│   │                             the project's full history, source of the
│   │                             written reports
│   ├── withdrawn_visuals/        images pulled from the submission, with a
│   │                             README explaining exactly why each one was
│   │                             pulled (see §6 below — do not delete these)
│   ├── weak_renders/              renders judged not strong enough to submit
│   ├── source_files/              the original brief, DWG, scope of work
│   └── misc_superseded/           ⭐ ONE folder for everything else with no
│       ├── legacy_outputs/          remaining live reference — old analysis
│       ├── legacy_scripts/          runs, an old PDF-typesetting script set,
│       ├── final_deliverables/      a second copy of an old deliverables
│       ├── superseded_site/         folder, the pre-portal static website,
│       ├── pdf_only_deliverables/   a duplicate PDF export set, and the old
│       ├── portal/                  portal before it moved to docs/_PORTAL.
│       └── START_HERE_superseded.md   Nothing here is pointed at by name from
│                                     any tool or doc, unlike phases/,
│                                     withdrawn_visuals/, weak_renders/ and
│                                     source_files/ above, which stayed as
│                                     their own folders because the pipeline
│                                     and MANIFEST.md files reference them
│                                     directly by path.
│
├── run_analysis.py            THE master command — data → models → figures
├── requirements.txt
├── README.md                   the design argument, written for a juror
├── DATA_SOURCES.md              every data source, its period, its limits
├── MIGRATION_MAP.md             where every old folder path went
└── PROJECT_WORKFLOW.md          THIS FILE
```

**The rule that makes this all trustworthy:** everything in `figures/`,
`design/visuals/`, `docs/`, and `submission/` is a *copy or a derivative* of
something computed in `data/` and `src/`. Nothing downstream is hand-drawn or
hand-typed. Change a number in `data/raw/`, re-run the pipeline, and every
chart, drawing, and report figure that depends on it changes with it — or a
test fails and tells you where.

---

## 3. Step by step — what was done, in what order

### Phase 0 — Existing materials (`archive/source_files/`)
Started from the brief itself: the Dubai Municipality scope of work, the
Neighbourhood Parks design manual, and the original site plan/DWG. Nothing
here was generated — it's what the client/competition supplied.

### Phase 1 — Existing Park / Knowledge Base
Read the site as it is today: urban context, climate analysis (temperature,
humidity, wind, sun path), shadow analysis, SWOT, and a catchment/demand study
(who lives within a 10-minute walk, and how many). Output: the knowledge base
that every later decision is checked against.

### Phase 2 — Problem Definition
Turned the Phase 1 findings into a ranked list of problems — scored by
severity, not just listed. This is what justifies *why* the redesign focuses
on shade and thermal comfort above everything else.

### Phase 3 — Opportunity & Objectives
Set the measurable targets the design has to hit (comfortable-hours
percentage, shade coverage, etc.) — the numbers that appear in the README's
results table trace back to targets set here.

### Phase 4 — Concept Development
Generated and scored multiple concepts against weighted criteria. The
crescent-shaped canopy is the concept that won that scoring — not the only
one drawn.

### Phase 5 — Masterplan Development
Turned the winning concept into an actual plan: room-by-room zoning that
sums to exactly 15,000 m² (verified automatically, not reconciled by hand).
This is also where the *straight-spine* layout was first drawn — later
superseded by the crescent (see Phase 11 below).

### Phase 6 — Detailed Design
Solved the canopy section: height, width, gridshell geometry, louvre depth —
driven directly by the shadow-length math in `src/solar.py`, not eyeballed.
Also: elevations, planting plan, material palette.

### Phase 7 — Performance & Sustainability
Ran the physics: water balance, carbon sequestration, energy budget, shade
performance by zone. This phase is also where an **overclaim was caught and
corrected** — an early draft described the canopy's solar array as
power sold back to the grid; it's actually a ~13% deficit, and the report
was corrected to say so.

### Phase 8 — User Experience & Activation
Used the microclimate clustering model (K-Means) to decide *when* the park
should be programmed — late afternoon in spring/autumn is where the comfort
gain concentrates, so that's where activation is targeted. Summer midday is
deliberately not programmed outdoors.

### Phase 9 — AI Workflow & Visualization
The methodology chapter: documents the four ML models, why each one is a
genuine prediction problem (not arithmetic in disguise — see README §"The
machine learning"), and generates the AI-generated photoreal renders.

### Phase 10 — Upload Documents / Submission Assembly
Every phase report and visual gets mapped onto the Dubai Municipality's
actual 12-slot upload form. This is the origin of the `submission/` folder.

### Phase 11 — The redesign (post-Phase-10, the biggest change in the project)
A later geometric check found the original straight-spine canopy's headline
shade claim (**99.2%**) doesn't survive scrutiny — low-angle sun slides the
shadow clean off the walkway. Rather than patch the number, **the plan itself
was redrawn**: a single crescent, radial rooms, all struck off one centre.
`src/plan.py` became the one file that generates that geometry, and
everything downstream (figures, drawings, the portal, the 60-second film) was
rewired to read it. The re-solved canopy section now measures **87.3%**, and
that number is regenerated by code every time, not retyped.

### Phase 12 — Repository cleanup and organisation *(done today)*
The project had grown to 500+ files with **55.6 MB of exact duplicate
copies** — the same render saved in five folders, a second full copy of the
website, `.docx.bak` backup files, PDFs saved under two different names.
`tools/organize_repo.py` was run: every removal was verified byte-for-byte
(MD5) against a surviving canonical copy first, so nothing without a twin was
touched. Then `tools/build_docs.py` was run to retire two dead website pages
whose links pointed at an unpushed GitHub repo, and to assemble the current
`docs/` site so the portal actually displays the drawings. Verified clean
with 33 pipeline tests + 64 portal tests + the film frame-render test — all
passing — then committed.

---

## 4. The pipeline, as commands (this is how you regenerate everything)

Run in this order — each stage consumes the previous stage's output:

```bash
pip install -r requirements.txt

python run_analysis.py           # data/raw → models/ → figures/*.png   (~3 min)
python -m src.drawings           # src/plan.py geometry → design/visuals/*.png
python -m src.boards             # figures + drawings → design/boards/*.png
python tools/build_docs.py       # → docs/ website (the portal)
python tools/sync_portal.py      # → docs/_PORTAL analytics data
python tools/sync_film.py        # src/plan.py geometry → the 60s concept film
python tools/sync_submission.py  # → populates submission/01–12
```

Verification — run these before trusting any number or shipping any change:

```bash
python -m tests.test_pipeline    # 33 checks: climate accuracy, no double-
                                  # claimed ground, zoning sums to 15,000 m², …
node docs/_PORTAL/selftest.js    # 64 checks: portal shows no retired claims
node tests/test_film.js          # every frame of the film, no NaN/undefined
```

Housekeeping — run only when the repo has accumulated new duplicates:

```bash
python tools/organize_repo.py --dry-run   # see what it would remove first
python tools/organize_repo.py             # then actually remove it
```

---

## 5. Where the 12 submission files come from

| # | Upload slot | Built from |
|---|---|---|
| 1 | Design Narrative & Concept | Phase 3 + 4 reports |
| 2 | Preliminary Design Masterplan | Phase 5 report + `figures/fig10_masterplan.png` |
| 3 | Concept Plans & Spatial Diagrams | Phase 4 report + circulation/masterplan drawings |
| 4 | Key Sections & Elevations | Phase 6 report + `design/visuals/section_crescent.png` etc. |
| 5 | 3D & Spatial Visualisations | Phase 9 renders + both presentation boards |
| 6 | AI Methodology Report | Phase 9 report + the entire `notebooks/` analysis |
| 7 | User Experience & Activation | Phase 8 report + `fig09_diurnal_comfort.png` |
| 8 | Sustainability Concept & Strategy | Phase 7 report |
| 9 | Material & Landscape Palette | Phase 6 report + `planting_crescent.png` |
| 10 | Complete Design Report | everything above, combined |
| 11 | Site Analysis & Human-Centric Research | Phase 1 + 2 reports |
| 12 | Concept Animation Video | `submission/12_.../concept_film.html`, generated by `tools/sync_film.py` |

Full detail on each slot — exact files, what still needs fixing, and the
format the portal wants — is in
[`docs/SUBMISSION_GUIDE.md`](docs/SUBMISSION_GUIDE.md).

---

## 6. About "unwanted images" — read before deleting anything

I checked every image file in the repository by name and content. **There is
no clutter unrelated to the project** — no screenshots, no random downloads,
nothing off-topic. Every image is one of:

1. **Current deliverables** — `figures/`, `design/`, `docs/assets/`,
   `submission/` (already deduplicated in the cleanup above).
2. **Phase history** — `archive/phases/*/outputs/` — the working charts each
   phase actually produced.
3. **`archive/withdrawn_visuals/`** — three images the project *itself*
   caught as fabricated (a fake CFD heatmap, a fake NDVI satellite map, a fake
   "optimised" canopy mesh — none of them ran the analysis they claim to),
   plus several superseded drawings of the old straight-spine layout. These
   are kept **on purpose** — the AI Methodology Report (submission slot 06)
   explicitly tells the jury *"the project revised its own headline shade
   figure downward... and withdrew three images that presented invented data
   as measurement... a submission that audits itself in public is more
   credible than one that never had to."* Deleting these images would remove
   the evidence behind that claim.

**If you still want them gone**, tell me and I'll delete
`archive/withdrawn_visuals/` and `archive/weak_renders/` outright (recoverable
via git history, but gone from the working folder) — I didn't do it
automatically because it would undercut a point your own submission makes to
the jury.

---

## 7. What's still open before 15 August 2026

1. **Open the DWG** (`archive/source_files/Al Safa Park 2 Plan (5).dwg`) and
   confirm the real site boundary — every area figure in the submission
   depends on the current assumed 150×100 m rectangle.
2. **Rewrite the Word reports in `reports/`** — they still describe the
   *superseded* straight-spine scheme. The code, drawings, portal, and film
   are all on the crescent design; the `.docx` files are not.
3. **Record the 60-second film** from
   `submission/12_Concept_Animation_Video/concept_film.html` to MP4 (steps in
   `docs/SUBMISSION_GUIDE.md` §12).
4. **Export image sheets to PDF** wherever the upload portal requires PDF.
5. **Tick all four declarations** on the Dubai Municipality portal and submit.
