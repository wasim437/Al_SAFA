# `_PORTAL/` — the Al Safa 2 analytics portal

Everything that makes `index.html` work. Open `index.html` by double-clicking it;
nothing needs to be installed or served, and it works with no internet connection.

---

## Why this folder exists

`index.html` used to carry its own hand-typed copy of every number in the project.
That copy had drifted from the computed phase outputs. The worst case: the portal
showed annual carbon sequestration as **147 tCO₂e/yr** when the Phase 7 model
computes **2.1 t/yr** — a 70× overstatement that contradicted the submitted report.

The fix was structural rather than a one-off correction:

```
   phase outputs/  ──►  build_portal.py  ──►  portal_data.js  ──►  index.html
   (CSV + JSON)         reads, validates,     single source        renders only
                        attaches provenance   of truth
```

`index.html` now computes no analysis figures of its own. If a number is wrong,
the source data is wrong — and the portal cannot silently disagree with the reports.

A second layer goes one step further: each headline metric also carries a link
to the **real-world organisation or dataset** behind it — NCM climate normals,
pvlib/NREL solar geometry, Dubai Statistics Center population, the DEWA tariff,
and so on — not just the project's own CSV/JSON. See "Bibliography" below.

---

## Files

| File | What it is |
|---|---|
| `build_portal.py` | The pipeline. Reads 19 phase output files, cross-checks them, writes the two files below. Python 3.8+, standard library only. |
| `portal_data.js` | **Generated — do not hand-edit.** Every figure the portal displays, plus a provenance record for each headline metric. |
| `DATA_AUDIT.md` | **Generated.** The cross-phase consistency report in plain text, for reviewing without opening the portal. |
| `portal.css` | Design system: dark and light themes, responsive layout, and a print sheet that turns the portal into a paginated report. |
| `portal.js` | The application: routing, charts, the NOAA solar engine, the 3D model, search and exports. |
| `selftest.js` | Verification. Run before trusting a build. |
| `vendor/` | Chart.js 4.4.0 and Three.js r160, held locally so the portal runs offline. |

---

## Rebuilding after you change an analysis

```bash
python _PORTAL/build_portal.py     # regenerate portal_data.js + DATA_AUDIT.md
node   _PORTAL/selftest.js         # verify the result (optional but recommended)
```

`build_portal.py` exits non-zero if a consistency check fails outright, so it can
gate a release. Warnings do not block — they are published on the portal's
Verification page instead of being hidden.

---

## What the self-test checks

`node _PORTAL/selftest.js` — 45 checks in six groups:

1. **Solar engine** — the browser's NOAA solar-position implementation against
   the project's own pvlib NREL SPA output for the three key dates, plus physical
   sanity properties (declination at the solstices, azimuth range, solar noon).
2. **HTML/JS contract** — every element id, chart canvas, routed page and local
   asset that `portal.js` reaches for actually exists.
3. **Data fidelity** — the rendered figures still equal the source JSON/CSV, and
   the bibliography (below) is internally consistent: every citation resolves,
   every declared reference is actually cited, and the cost-rate honesty caveat
   survives into the portal's copy.
4. **Drawn geometry** — every block in the plan and the 3D model matches its
   scheduled area to within 0.5 m², sits inside the site envelope, and does not
   overlap another block.
5. **Regression guard** — the four retired incorrect claims (147 tCO₂e, −8.5 °C
   PET, 94.3 comfort days, 1.5 km catchment) cannot reappear as literals.

---

## Bibliography — the real-world data behind the numbers

Every phase's `_scripts/*.py` already cites where its inputs came from (see the
header comments and inline `# sourced:` notes). `build_portal.py` collects those
citations into a `REFERENCES` list — organisation, dataset, retrieval date, and
what it feeds — and attaches the relevant ones to each tracked metric via
`refs=[...]`. Nothing in that list is invented for the portal; it is a transcription
of citations the analysis scripts already make.

This shows up in three places:

- **Verification page → "External data sources"** — one card per reference,
  with which metrics cite it and, where a source has a real limitation, the
  caveat spelled out (not smoothed over).
- **Any KPI's provenance drawer** — click a tile; if it's backed by an external
  source, that source appears under "Real-world data source(s)" with a link to
  jump to the full bibliography.
- **`DATA_AUDIT.md` → "External data sources"** — the same bibliography as
  plain text.

Two references carry an explicit **caveat** worth knowing about before quoting
either figure elsewhere:

- **Construction cost rates** are Dubai *villa/residential* landscaping
  benchmarks (public-domain cost guides), upper-bounded and with contingency
  added — not a municipal tender price. An earlier draft of this portal
  mislabelled these as "Dubai Municipality unit rates," which overstated their
  authority; the provenance text and this README now say what they actually are.
- **Carbon sequestration rates** are for young, newly-planted trees —
  deliberately conservative. Mature-canopy rates would be several times higher.

---

## Resolved: the Phase 7 duplicate-model problem

Three of the four disagreements this section used to list — two capex models,
two opex models, and a monthly-vs-annual water mismatch — turned out to share
one root cause: `08_advanced_lca_sustainability_master.py` (an "advanced"
30-year LCC/energy/carbon analysis added late in Phase 7) computed its own
independent capex, opex and water totals from scratch, instead of reading the
figures the rest of Phase 7 had already computed. Two unrelated models
answering the same question is not the same as one team writing two reports —
this is what a duplicate, unreconciled input pipeline produces. So they were
fixed at the source rather than papered over in the portal:

- `03_water_demand_model.py` now exports the monthly water series itself
  (it already computed the monthly numbers internally, just never saved
  them) — there is exactly one water model in the project now, with one
  citation, not two disagreeing ones.
- `08_advanced_lca_sustainability_master.py` now **reads** its capex, opex,
  water and tree-sequestration totals from the phase outputs that actually
  compute them, and keeps its own category-level *breakdown* as an
  explicitly-labelled illustrative split of that verified total — never a
  second, competing total.
- Its genuinely new analysis — 30-year NPV/IRR/payback/SROI, a canopy solar
  energy budget, and embodied construction carbon — survives the rewrite
  and is now surfaced on the **Performance** page's "Advanced 30-year model"
  section, sourced from `advanced_lcc_energy_carbon_results.json`.

Two more issues surfaced during that rewrite and were fixed the same way:

- The elemental cost table's own rows used to sum to only 77% of its footer
  total — the "addons" (prelims, design contingency, professional fees) were
  applied to the total but never shown as line items. They're real rows now.
- The energy model's solar array (18.4 kWp, sized to the real canopy area)
  covers only ~13% of the assumed lighting/systems load — a deficit, not a
  surplus. The script used to print this as power "sold back to the grid"
  regardless of sign. It now says "imported (shortfall)" when the number is
  negative, because it is.

Rebuild order after touching any Phase 7 script:
`python 07_.../03_water_demand_model.py` (writes the water series) →
`python 07_.../08_advanced_lca_sustainability_master.py` (reads it, and the
capex/opex/carbon totals) → `python _PORTAL/build_portal.py`.

## Remaining known disagreement

| Issue | Detail |
|---|---|
| **Green-space target** | Phase 3 targets ≥60% green or soft-surface. Strictly categorised, green + buffer + passive is 32.5%. Counting the active soft-surface lawns reaches the target; the strict figure is what the portal reports. |
| **Day length vs. pvlib** (engine validation, not a data disagreement) | Up to 17 minutes apart, because the browser's solar engine uses the NOAA 90.833° zenith and the project's values are rounded to 10-minute steps. Peak elevation — what the shade model depends on — agrees to 0.05°. |

The green-space figure is a categorisation choice (which zones count as
"green"), not a computational error, so it's reported rather than resolved —
resolving it means deciding whether active soft-surface lawns count, which is
a design call for a human, not a data-pipeline bug.

---

## Portal features worth knowing

- **`Ctrl` + `K`** — search every metric, zone, species, problem and source file.
- **Click any KPI tile** — opens its provenance: the source file, the computation,
  and how to interpret it.
- **Keys `1`–`9`** — jump straight to a page. `/` opens search. `Esc` closes anything.
- **Solar page** — any date and time, not just the three key dates; `▶ Play day`
  animates sunrise to sunset.
- **Concepts page** — the criterion weights are live sliders. Moving them
  recomputes the ranking, which tests whether Concept A wins because of the
  design or because of the weighting.
- **3D model** — the sun is driven by the same solar engine, so shadows are
  physically correct for the chosen date and time.
- **Print (`⎙`)** — prints all thirteen pages as a paginated report, not a
  screenshot of a dashboard.
- **CSV / PNG buttons** — export any table or chart.

---

## Site geometry caveat

The plan and the 3D model assume a **150 × 100 m rectangle**. This is the
project's working assumption, not a surveyed boundary. Every area figure depends
on it, so confirming it against the municipality DWG remains an outstanding task
before submission.
