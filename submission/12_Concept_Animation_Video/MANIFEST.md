# Slot 12 Concept Animation Video

Files in this folder, and what produced each one.

| File | What it is |
|---|---|
| `fig10_masterplan.png` | The masterplan the sixty-second film flies over. Every frame of the film reads the same geometry, asserted by tests/test_film.js. |
| `Concept_Animation_Storyboard.pdf` | Written report / supporting document. |
| `concept_film.html` | Written report / supporting document. |
| `Falaj_Al_Safa_Concept_Film_60s_1080p.mp4` | Written report / supporting document. |
| `Falaj_Al_Safa_Concept_Film_60s_4K.mp4` | Written report / supporting document. |
| `narration` | Written report / supporting document. |
| `README_VIDEO.txt` | Written report / supporting document. |

Every image here is generated. Rebuild them with:

```
python run_analysis.py      # datasets, models, figures/
python -m src.drawings      # design/visuals/ — section, elevation, circulation, planting
python -m src.boards        # design/boards/ — the two presentation boards
python tools/sync_submission.py
```

Images withdrawn from this submission, and why, are recorded in
`archive/withdrawn_visuals/README.md`.
