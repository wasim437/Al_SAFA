# Slot 05 3D Spatial Visualizations

Files in this folder, and what produced each one.

| File | What it is |
|---|---|
| `board_1_concept.png` | Presentation board 1 — concept. |
| `board_2_evidence.png` | Presentation board 2 — evidence. |
| `dubai_futuristic_masterplan_aerial.jpg` | Aerial — the canopy and the channel running the length of the crescent. |
| `Al_Safa_2_Park_3D_Spatial_Visualizations.pdf` | Written report / supporting document. |
| `eyelevel_spine_1784970552956.jpg` | Written report / supporting document. |
| `masterplan_aerial_golden_hour.jpg` | Written report / supporting document. |
| `night_plaza_render_1784970565232.jpg` | Written report / supporting document. |
| `spine_corridor_interior.jpg` | Written report / supporting document. |

Every image here is generated. Rebuild them with:

```
python run_analysis.py      # datasets, models, figures/
python -m src.drawings      # design/visuals/ — section, elevation, circulation, planting
python -m src.boards        # design/boards/ — the two presentation boards
python tools/sync_submission.py
```

Images withdrawn from this submission, and why, are recorded in
`archive/withdrawn_visuals/README.md`.
