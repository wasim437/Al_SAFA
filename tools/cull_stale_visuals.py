"""Withdraw images that the submission can no longer stand behind.

Two separate problems, and it matters which is which.

FABRICATED
    Three images present invented data as measurement. A "PET / CFD thermal
    comfort analysis" dashboard sourced to "CFD Simulation Data" — no CFD was
    ever run, and its own legend repeats two bands and prints the humidity
    twice. A "Satellite Remote Sensing NDVI Analytics" pair — the pixels are
    numpy noise, no Sentinel scene was ever downloaded. A "Generative Parametric
    Voronoi Canopy Mesh / Algorithmic Solar Optimization" — the seeds are
    uniform random and no optimisation was performed.

    These are the most serious thing in the package. A juror who checks one of
    them has grounds to discard the whole submission, and would be right to.
    They go, and this file records why.

SUPERSEDED
    The rest are honest drawings of a scheme that no longer exists. They show
    the rectangular-room, straight-spine layout, a 10 m walk under a 5.5 m
    canopy with no louvre, and a circulation diagram still claiming "100%
    shaded" — a figure this project withdrew. Their replacements are generated
    from the live geometry by src/drawings.py.

Nothing is deleted. Everything moves to archive/withdrawn_visuals/ with this
note beside it.

    python tools/cull_stale_visuals.py --dry-run
    python tools/cull_stale_visuals.py
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "archive" / "withdrawn_visuals"

FABRICATED = {
    "thermal_comfort_heatmap.jpg":
        "Presents invented output as a CFD/PET simulation. No CFD was run. Its "
        "own legend lists 28-34 °C twice and 42-52 °C twice, and prints "
        "'Rel. Humidity: 48%, 48%'.",
    "sentinel_ndvi_analytics.png":
        "Titled 'Satellite Remote Sensing NDVI Analytics'. The raster is numpy "
        "noise. No Sentinel-2 scene was ever retrieved, and no NDVI was computed.",
    "parametric_canopy_mesh.png":
        "Titled 'Algorithmic Solar Optimization'. The Voronoi seeds are drawn "
        "from a uniform distribution; no objective was defined and nothing was "
        "optimised. It also draws a 100 x 15 m canopy, which is not the design.",
}

SUPERSEDED = {
    "masterplan_diagram.png":
        "The rectangular-room layout, superseded by the crescent. Also carries "
        "'AI-generated draft layout for review' in its own title block.",
    "circulation_diagram.png":
        "Draws the straight spine and claims '100% shaded', a figure this "
        "project has withdrawn. Replaced by circulation_crescent.png.",
    "section_shaded_spine.png":
        "Shows a 10 m walk under a 5.5 m canopy with no louvre. The section is "
        "now a 7 m walk under an 18 m gridshell at 4.5 m with a 3 m southern "
        "louvre. Replaced by section_crescent.png.",
    "elevation_shaded_spine_long.png":
        "Elevation of the superseded straight canopy. Replaced by "
        "elevation_crescent.png.",
    "elevation_entrance_gateway.png":
        "Gateway of the superseded scheme; the entrances are now the crescent's "
        "two horns breaking through the berm.",
    "planting_plan.png":
        "Plants the superseded rectangular rooms. Replaced by "
        "planting_crescent.png.",
    "presentation_board_1_concept.png":
        "Composed from the superseded drawings above.",
    "presentation_board_2_evidence.png":
        "Composed from the superseded drawings above.",
    "aerial_day_view_1784970538631.jpg":
        "Photoreal render of a dead-straight PV-clad canopy bar over a "
        "rectilinear park. It is a picture of the scheme that was replaced, and "
        "it is the specific image the design critique was about.",
}

SEARCH = ["submission", "design", "docs/assets/renders"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    reasons = {**FABRICATED, **SUPERSEDED}
    moved, hits = 0, {}
    for folder in SEARCH:
        base = ROOT / folder
        if not base.exists():
            continue
        for p in sorted(base.rglob("*")):
            if not p.is_file() or p.name not in reasons:
                continue
            rel = p.relative_to(ROOT)
            kind = "fabricated" if p.name in FABRICATED else "superseded"
            target = DEST / kind / p.name
            print(f"  [{kind:<11}] {rel}")
            hits.setdefault(p.name, kind)
            if not args.dry_run:
                target.parent.mkdir(parents=True, exist_ok=True)
                if target.exists():
                    p.unlink()          # already archived from another folder
                else:
                    shutil.move(str(p), str(target))
            moved += 1

    print(f"\n{moved} file(s) {'would move' if args.dry_run else 'moved'} "
          f"to archive/withdrawn_visuals/")

    missing = sorted(set(reasons) - set(hits))
    if missing:
        print(f"not found (already withdrawn): {', '.join(missing)}")

    if not args.dry_run and moved:
        lines = ["# Withdrawn visuals\n",
                 "These images were removed from the submission. Nothing is "
                 "deleted; every file is here.\n",
                 "\n## Fabricated — invented data presented as measurement\n",
                 "\nThese are the serious ones. Each states a source it does not "
                 "have. They were withdrawn on the same principle the project "
                 "applied to its own 99.2% shade claim: a number or an image "
                 "that cannot survive being checked should not be in front of a "
                 "juror.\n\n"]
        for name, why in FABRICATED.items():
            lines.append(f"- **{name}** — {why}\n")
        lines.append("\n## Superseded — honest drawings of a scheme that changed\n\n")
        lines.append("The park was redesigned from a rectangular-room layout on a "
                     "straight spine to a single crescent with radial rooms. "
                     "These drawings describe the old scheme correctly and the "
                     "new one not at all. Their replacements are generated from "
                     "the live geometry by `src/drawings.py`.\n\n")
        for name, why in SUPERSEDED.items():
            lines.append(f"- **{name}** — {why}\n")
        DEST.mkdir(parents=True, exist_ok=True)
        (DEST / "README.md").write_text("".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
