# 🌳 AL SAFA 2 PARK — AI DESIGN CHALLENGE — START HERE

**Project:** Redesign of Al Safa 2 Park (15,000 m²) for the Dubai Municipality AI Park Design Challenge.
**Design concept:** "The Shaded Spine."
**Deadline:** 15 August 2026.

---

## 👉 IF YOU ONLY OPEN 3 THINGS, OPEN THESE

| # | File | What it is |
|---|------|-----------|
| 1 | **`index.html`** | ⭐ **The interactive portal — double-click it.** Thirteen pages covering the whole project, with a live solar simulator, a 3D model and a data-verification page. Works offline. **Start here.** |
| 2 | `_FINAL_DELIVERABLES/EASY_UNDERSTANDING_GUIDE.pdf` | The whole project explained in plain, simple words. |
| 3 | `_FINAL_DELIVERABLES/03_Submission_Package/Al_Safa_2_Park_Complete_Design_Report.pdf` | The flagship master report — the full story from evidence to design. |
| ➕ | `_FINAL_DELIVERABLES/PROJECT_METHODOLOGY_ROADMAP.pdf` | **The step-by-step method** — how each phase produces its answer and feeds the next, all the way to the 12 files. |

---

## 🖥️ THE PORTAL (`index.html`)

Double-click `index.html`. No install, no server, no internet needed.

**Every number in the portal is generated from the phase `outputs/` folders** by
`_PORTAL/build_portal.py`. The portal types no figures of its own, so it cannot
drift out of step with the reports. Click any headline tile to see the source file
and the computation behind it.

| Try this | What happens |
|---|---|
| `Ctrl` + `K` | Search every metric, zone, species, problem and source file |
| Click a KPI tile | Shows where that number comes from and how to read it |
| **Solar** page → `▶ Play day` | Watches the sun move for any date you choose — computed live, not a lookup table |
| **Concepts** page → drag the weight sliders | Re-ranks the three concepts, testing whether Concept A wins on merit or on weighting |
| **3D Model** page → change the sun date/time | Shadows update to what the real site would get |
| **Verification** page | The cross-phase consistency audit — including the disagreements |
| **Verification** page → "External data sources" | The real organisations behind the numbers — NCM, pvlib/NREL, Dubai Statistics Center, DEWA and more — with honest caveats where a source has limits |
| `⎙` button | Prints all thirteen pages as a paginated report |

To rebuild after changing any analysis:

```
python _PORTAL/build_portal.py     # regenerate the portal's data
node   _PORTAL/selftest.js         # 38 checks — optional but recommended
```

See `_PORTAL/README.md` for the full picture.

---

## ✏️ WANT TO EDIT THE TEXT? (new — Word format)

Every report now exists as a **directly editable Word `.docx`** alongside its final PDF.
**To change any wording: open the `.docx` in Word, edit, save.** No code involved.

| Where | What |
|---|---|
| `_FINAL_DELIVERABLES/01_All_Phase_Reports_EDITABLE_DOCX/` | ⭐ All phase reports as editable Word files |
| `_FINAL_DELIVERABLES/01_All_Phase_Reports/` | The same reports as final PDFs |
| `EASY_UNDERSTANDING_GUIDE.docx` / `.pdf` | Plain-language guide, both formats |

Python is now used **only** for the analysis and charts (which genuinely need real
computation) — not for assembling the written text. Each phase's `_scripts/gen_docx_*.py`
regenerates its Word file if you'd rather rebuild than hand-edit.

---

## 📁 FOLDER MAP

| Folder | What's inside |
|--------|---------------|
| **`_FINAL_DELIVERABLES/`** | ⭐ **Everything important, gathered in one place** — all phase reports, all key visuals, the submission package. Start here. |
| `00_MASTER_TRACKER/` | Project tracker (full status/version history) + the easy guide. |
| `01_PHASE1_EXISTING_PARK/` | Site understanding — 13 sub-analyses (climate, solar, catchment, etc.), each a PDF with a code-proof appendix. |
| `02_PHASE2_PROBLEM_DEFINITION/` | Problems, ranked by a computed severity model. |
| `03_PHASE3_...` | Vision, mission, objectives, success metrics. |
| `04_PHASE4_...` | 3 concepts scored → "Shaded Spine" chosen. |
| `05_PHASE5_...` | Master plan (to-scale geometry) + circulation diagram. |
| `06_PHASE6_...` | Planting plan, materials, section + elevations. |
| `07_PHASE7_...` | Performance: shade, water, cost, carbon, comfort, O&M — all computed. |
| `08_PHASE8_...` | User personas, daily/seasonal use, journey maps. |
| `09_PHASE9_...` | AI methodology + renders (aerial day/night, eye-level) + presentation boards. |
| `10_PHASE10_UPLOAD_DOCUMENTS/` | **The 12 official submission files, sorted into their upload folders** (`10.2_Required_Files/`). |
| `99_SOURCE_FILES/` | The original documents Dubai Municipality provided (brief, manual, DWG, master plan). |
| `_PORTAL/` | The engine behind `index.html` — the data pipeline, the audit report, and the offline chart/3D libraries. See its own README. |

Each phase folder has a `_scripts/` sub-folder holding the Python code that generated its analysis and PDF.

---

## ✅ WHAT'S PROVEN WITH REAL DATA / COMPUTATION

- **Shade:** Shaded Spine = **99.2% annual shade** (4,391 of 4,425 annual daylight hours).
- **Comfort:** shade adds **+3 comfortable months/year** (NWS Heat Index on real Dubai climate).
- **Water:** **~5,700 m³/year** irrigation (real Ghaf field-study data).
- **Build cost:** **~AED 18.6M = 53% of the 35M budget** (real Dubai unit rates).
- **Running cost:** **~AED 2.0M/year**, 10-year total cost of ownership **~AED 38M**.
- **Carbon:** **~2.1 tonnes CO₂/year** sequestered (131 newly planted trees, real rates).
- **Population served:** **~7,640 residents** within a 10-min (800 m) walk (Dubai Statistics Center 2023).
- **30-year outlook:** **AED 35.6M net present value**, 13.6% IRR, 8-year payback (discounted at the HM Treasury Green Book's 3.5% public-sector rate — see the portal's "Advanced 30-year model" section).
- **Energy, stated honestly:** the canopy-mounted solar array covers **~13% of the site's lighting/systems load** — a deficit, not a surplus. An earlier draft mislabelled this shortfall as power sold back to the grid; it's now stated as what it is.

Each of these is traceable in the portal: open `index.html`, go to **Verification**,
and every figure lists its source file and its computation. The same table is in
`_PORTAL/DATA_AUDIT.md`.

---

## ⚠️ WHAT STILL NEEDS A HUMAN (before submitting)

1. Review & approve the design (everything from Phase 2 on is marked "AI-GENERATED DRAFT").
2. **Open the DWG file to confirm the real park boundary** (we assumed a 150×100 m rectangle). Every area figure depends on this.
3. **Decide how green space should be categorised** — the one remaining flagged item on the portal's Verification page. Strictly categorised, green/buffer/passive space is 32.5% of the site against a ≥60% target; counting active soft-surface lawns reaches it. This is a design-intent call, not a data bug. (The two cost models and the two water models that used to disagree here have since been fixed at the source — see `_PORTAL/README.md`.)
4. Produce the consolidated design report (upload slot 10) and the optional 60-second video (slot 12).
5. Export the image sheets (renders) into PDF where the upload form requires PDF.
6. Submit on the challenge website & tick all 4 declarations before **15 August 2026**.
