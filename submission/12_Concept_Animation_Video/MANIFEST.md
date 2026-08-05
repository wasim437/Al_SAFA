# Slot 12 Concept Animation Video

Files in this folder, and what produced each one.

| File | What it is |
|---|---|
| `fig10_masterplan.png` | The masterplan the sixty-second film flies over. Every frame of the film reads the same geometry, asserted by tests/test_film.js. |
| `Concept_Animation_Storyboard.pdf` | Written report / supporting document. |
| `concept_film.html` | The original real-time cut: the park drawn in 3D from src/plan.py with shadows computed live, kept because it demonstrates that the film and the drawings share one geometry. Every frame is asserted by tests/test_film.js. |
| `concept_film_hero.html` | The film that produced the MP4 — drawn entirely from the project's own data, no photographs. Seven plan forms swept and scored, and a heat index falling from 56.8 to 48.7 C. Press Record to rebuild the video at 1080p or 4K. Built by tools/build_concept_film_hero.py. |
| `concept_film_presentation.html` | An alternative cut using the six photoreal renders against the same narration, moving between the visualisations and the analysis behind them. Built by tools/build_concept_film_v2.py. |
| `Falaj_Al_Safa_Concept_Film_60s_4K.mp4` | **Deliverable 15 — the one-minute concept animation.** 3840x2160, sixty seconds, H.264 with AAC narration. Upload this file. Recorded from concept_film_hero.html. |
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
