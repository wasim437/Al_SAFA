# Slot 04 Key Sections Elevations

Files in this folder, and what produced each one.

| File | What it is |
|---|---|
| `section_crescent.png` | Section A–A through the Crescent Canopy at midspan, with both solstice sun angles computed by the NREL algorithm. |
| `elevation_crescent.png` | Long elevation — the bay rhythm, the perforated soffit and the southern louvre. |
| `Phase6_Detailed_Design_Report.pdf` | Written report / supporting document. |

Every image here is generated. Rebuild them with:

```
python run_analysis.py      # datasets, models, figures/
python -m src.drawings      # design/visuals/ — section, elevation, circulation, planting
python -m src.boards        # design/boards/ — the two presentation boards
python tools/sync_submission.py
```

Images withdrawn from this submission, and why, are recorded in
`archive/withdrawn_visuals/README.md`.
