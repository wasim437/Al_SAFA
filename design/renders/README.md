# design/renders/ — currently empty, and that is deliberate

All six photoreal renders were withdrawn after being opened and compared against
the masterplan. None of them showed this park:

| File | What it actually showed |
|---|---|
| `masterplan_aerial_golden_hour.jpg` | Serpentine S-curve canopy over a large lagoon |
| `dubai_futuristic_masterplan_aerial.jpg` | Free-form organic shells, canals, rainforest planting |
| `spine_corridor_interior.jpg` | A dead-straight corridor — the superseded scheme |
| `dubai_futuristic_spine_interior.jpg` | Vaulted botanical pavilion with tropical planting |
| `eyelevel_spine_1784970552956.jpg` | Curved walk, but an S-curve and no water channel |
| `night_plaza_render_1784970565232.jpg` | Plaza at night, but jet fountains contradict the falaj |

All six were deleted on 3 August 2026. They were never part of the submission,
and keeping images that contradict the plan only invites them back in by
mistake. The reasoning behind each withdrawal is preserved above and in
[`archive/withdrawn_visuals/README.md`](../../archive/withdrawn_visuals/README.md).

## To refill this folder

Generate from [`AL_SAFA_MASTER_PROMPT.md`](../../AL_SAFA_MASTER_PROMPT.md) —
one file carrying the real geometry, the planting palette and the acceptance
test. Prompts 01, 02 and 03 are the priority: they repopulate Board 1 and
upload slot 05.

Save them to these exact paths, because `src/boards.py` reads them by name:

```
design/renders/Aerial/masterplan_aerial_golden_hour.jpg      <- prompt 01
design/renders/Eye_Level/spine_corridor_interior.jpg         <- prompt 03
design/renders/Night/night_plaza_render_1784970565232.jpg    <- prompt 02
design/renders/Eye_Level/eyelevel_spine_1784970552956.jpg    <- prompt 03, 2nd angle
```

Then re-run, in this order:

```bash
python -m src.boards                    # boards pick the renders back up
python tools/build_docs.py              # website
python tools/sync_portal.py             # portal gallery
python tools/build_submission_pdfs.py   # the 12 upload PDFs
```

Until then, Board 1 shows a "Visualisation in preparation" placeholder naming
the prompt that fills it. That is a smaller cost than captioning a lagoon as
"the crescent", which is what it did before.

**Every render must pass its acceptance test in `AL_SAFA_MASTER_PROMPT.md`
before it goes in.** A render that contradicts the drawings is worse than no
render.
