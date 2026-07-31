# Slot 09 Material Landscape Palette

Files in this folder, and what produced each one.

| File | What it is |
|---|---|
| `planting_crescent.png` | Planting plan — species, counts, mature canopy and summer water demand. |
| `section_crescent.png` | Section A–A, showing the surface build-up and the falaj channel. |
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
