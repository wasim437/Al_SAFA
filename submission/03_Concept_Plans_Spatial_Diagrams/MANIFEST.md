# Slot 03 Concept Plans Spatial Diagrams

Files in this folder, and what produced each one.

| File | What it is |
|---|---|
| `fig10_masterplan.png` | The masterplan and its room schedule. |
| `circulation_crescent.png` | Circulation and accessibility — the shaded primary route, the radial sikkas, and Al Madar, the running loop. |
| `fig04_site_comfort_map.png` | Predicted July comfort per square metre — the spatial argument for where each room was placed. |
| `Phase4_Concept_Development_Report.pdf` | Written report / supporting document. |

Every image here is generated. Rebuild them with:

```
python run_analysis.py      # datasets, models, figures/
python -m src.drawings      # design/visuals/ — section, elevation, circulation, planting
python -m src.boards        # design/boards/ — the two presentation boards
python tools/sync_submission.py
```

Images withdrawn from this submission, and why, are recorded in
`archive/withdrawn_visuals/README.md`.
