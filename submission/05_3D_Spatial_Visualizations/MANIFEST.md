# Slot 05 3D Spatial Visualizations

Files in this folder, and what produced each one.

| File | What it is |
|---|---|
| `board_1_concept.png` | Presentation board 1 — concept. |
| `board_2_evidence.png` | Presentation board 2 — evidence. |
| `fig10_masterplan.png` | The masterplan the visualisations must agree with. Any render that does not show this park does not belong in this slot. |
| `masterplan_aerial_golden_hour.jpg` | Aerial, golden hour — artistic impression, illustrative of design intent. Master prompt 01. |
| `spine_corridor_interior.jpg` | Eye level beneath Al Hilal — artistic impression. Master prompt 03. |
| `night_plaza_render_1784970565232.jpg` | The plaza at night — artistic impression. Master prompt 02. |
| `Visualisation_Strategy_and_Image_Provenance.pdf` | Written report / supporting document. |

Every image here is generated. Rebuild them with:

```
python run_analysis.py      # datasets, models, figures/
python -m src.drawings      # design/visuals/ — section, elevation, circulation, planting
python -m src.boards        # design/boards/ — the two presentation boards
python tools/sync_submission.py
```

Images withdrawn from this submission, and why, are recorded in
`archive/withdrawn_visuals/README.md`.
