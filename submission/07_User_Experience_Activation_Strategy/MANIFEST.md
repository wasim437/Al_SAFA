# Slot 07 User Experience Activation Strategy

Files in this folder, and what produced each one.

| File | What it is |
|---|---|
| `fig09_diurnal_comfort.png` | Hour-by-month comfort surface — the calendar the activation programme is built from. It is why summer midday is not programmed outdoors and late afternoon is. |
| `fig08_microclimate_regimes.png` | K-Means microclimate regimes across the site, k selected by silhouette score. Different regimes take different programmes. |
| `circulation_crescent.png` | Circulation and accessibility — how a visitor actually reaches each room, step-free, from the shaded primary route. |
| `childrens_dune_play.jpg` | Written report / supporting document. |
| `Phase8_User_Experience_and_Activation_Report.pdf` | Written report / supporting document. |

Every image here is generated. Rebuild them with:

```
python run_analysis.py      # datasets, models, figures/
python -m src.drawings      # design/visuals/ — section, elevation, circulation, planting
python -m src.boards        # design/boards/ — the two presentation boards
python tools/sync_submission.py
```

Images withdrawn from this submission, and why, are recorded in
`archive/withdrawn_visuals/README.md`.
