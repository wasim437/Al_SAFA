# Slot 06 AI Methodology Report

Files in this folder, and what produced each one.

| File | What it is |
|---|---|
| `fig05_surrogate_performance.png` | The shade surrogate against ray-traced ground truth, held-out test set. |
| `fig06_feature_importance.png` | Permutation importance — which design levers actually move the outcome. |
| `fig07_confusion_matrix.png` | Comfort classifier, with temperature and humidity withheld. |
| `Phase9_AI_Workflow_and_Visualization_Report.pdf` | Written report / supporting document. |

Every image here is generated. Rebuild them with:

```
python run_analysis.py      # datasets, models, figures/
python -m src.drawings      # design/visuals/ — section, elevation, circulation, planting
python -m src.boards        # design/boards/ — the two presentation boards
python tools/sync_submission.py
```

Images withdrawn from this submission, and why, are recorded in
`archive/withdrawn_visuals/README.md`.
