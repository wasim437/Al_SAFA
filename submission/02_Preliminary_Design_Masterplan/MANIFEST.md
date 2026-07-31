# Slot 02 Preliminary Design Masterplan

Files in this folder, and what produced each one.

| File | What it is |
|---|---|
| `fig10_masterplan.png` | The masterplan, with the numbered room schedule. Drawn from src/plan.py; every area is the shoelace area of the drawn polygon. |
| `planting_crescent.png` | Planting plan — 131 trees at mature canopy radius. |
| `Phase5_Masterplan_Development_Report.pdf` | Written report / supporting document. |

Every image here is generated. Rebuild them with:

```
python run_analysis.py      # datasets, models, figures/
python -m src.drawings      # design/visuals/ — section, elevation, circulation, planting
python -m src.boards        # design/boards/ — the two presentation boards
python tools/sync_submission.py
```

Images withdrawn from this submission, and why, are recorded in
`archive/withdrawn_visuals/README.md`.
