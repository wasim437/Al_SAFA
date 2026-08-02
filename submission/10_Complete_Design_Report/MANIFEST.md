# Slot 10 Complete Design Report

Files in this folder, and what produced each one.

| File | What it is |
|---|---|
| `fig10_masterplan.png` | The masterplan and its measured room schedule, closing on 15,000 m². |
| `board_2_evidence.png` | Presentation board 2 — the evidence behind every claim in this report. |
| `fig11_cost_plan.png` | The capital cost plan against the AED 35 M ceiling, line by line. |
| `section_crescent.png` | Section A–A through the Crescent Canopy — the detail the whole thermal argument rests on. |
| `Al_Safa_2_Park_Complete_Design_Report.docx` | Written report / supporting document. |
| `Al_Safa_2_Park_Complete_Design_Report.pdf` | Written report / supporting document. |

Every image here is generated. Rebuild them with:

```
python run_analysis.py      # datasets, models, figures/
python -m src.drawings      # design/visuals/ — section, elevation, circulation, planting
python -m src.boards        # design/boards/ — the two presentation boards
python tools/sync_submission.py
```

Images withdrawn from this submission, and why, are recorded in
`archive/withdrawn_visuals/README.md`.
