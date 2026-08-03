# Slot 11 Site Analysis Human Centric Research

Files in this folder, and what produced each one.

| File | What it is |
|---|---|
| `fig01_climate_and_comfort.png` | Dubai monthly normals against the modelled heat index. |
| `fig09_diurnal_comfort.png` | Hour-by-month comfort surface, exposed today and shaded as designed. |
| `Phase2_Problem_Definition_Report.pdf` | Written report / supporting document. |

Every image here is generated. Rebuild them with:

```
python run_analysis.py      # datasets, models, figures/
python -m src.drawings      # design/visuals/ — section, elevation, circulation, planting
python -m src.boards        # design/boards/ — the two presentation boards
python tools/sync_submission.py
```

Images withdrawn from this submission, and why, are recorded in
`archive/withdrawn_visuals/README.md`.
