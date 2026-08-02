# Slot 05 3D Spatial Visualizations

Files in this folder, and what produced each one.

| File | What it is |
|---|---|
| `board_1_concept.png` | Presentation board 1 — concept. |
| `board_2_evidence.png` | Presentation board 2 — evidence. |

Every image here is generated. Rebuild them with:

```
python run_analysis.py      # datasets, models, figures/
python -m src.drawings      # design/visuals/ — section, elevation, circulation, planting
python -m src.boards        # design/boards/ — the two presentation boards
python tools/sync_submission.py
```

Images withdrawn from this submission, and why, are recorded in
`archive/withdrawn_visuals/README.md`.
