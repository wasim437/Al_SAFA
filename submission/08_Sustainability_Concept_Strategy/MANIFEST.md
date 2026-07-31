# Slot 08 Sustainability Concept Strategy

Files in this folder, and what produced each one.

| File | What it is |
|---|---|
| `fig03_shade_by_zone.png` | Ray-traced annual shade coverage by zone type. |
| `fig02_comfort_bands.png` | Share of the daylight year in each comfort band, exposed and shaded. |
| `Phase7_Performance_and_Sustainability_Report.pdf` | Written report / supporting document. |

Every image here is generated. Rebuild them with:

```
python run_analysis.py      # datasets, models, figures/
python -m src.drawings      # design/visuals/ — section, elevation, circulation, planting
python -m src.boards        # design/boards/ — the two presentation boards
python tools/sync_submission.py
```

Images withdrawn from this submission, and why, are recorded in
`archive/withdrawn_visuals/README.md`.
