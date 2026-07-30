"""
Move the weak script-drawn pseudo-renders out of the submission.

The 3D Visualisations slot currently mixes two incompatible things: photoreal
renders, and flat matplotlib drawings of the same subjects. The matplotlib ones
(an "aerial view" made of coloured rectangles, an "eye-level view" made of
trapezoids and circles) are the weakest images in the package, and putting them
beside a photoreal render invites the comparison rather than surviving it.

They are moved, not deleted — archive/weak_renders/ keeps every one.

Genuine technical drawings are NOT touched: sections, elevations, the planting
plan, the circulation and masterplan diagrams and the presentation boards are
all doing a job a photograph cannot, and they belong in the submission.

    python tools/cull_weak_renders.py --dry-run
    python tools/cull_weak_renders.py
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "archive" / "weak_renders"

# Filenames that are script-drawn imitations of photography. Matched anywhere
# under submission/ and design/.
CULL = [
    "aerial_day.png",
    "aerial_night.png",
    "eyelevel_shaded_spine.png",
    "eyelevel_community_plaza.png",
]

SEARCH = ["submission", "design"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    moved = 0
    for folder in SEARCH:
        base = ROOT / folder
        if not base.exists():
            continue
        for p in sorted(base.rglob("*")):
            if not p.is_file() or p.name not in CULL:
                continue
            rel = p.relative_to(ROOT)
            target = DEST / rel.parent.relative_to(folder) / p.name \
                if rel.parent != Path(folder) else DEST / folder / p.name
            print(f"  {rel}  ->  {target.relative_to(ROOT)}")
            if not args.dry_run:
                target.parent.mkdir(parents=True, exist_ok=True)
                if target.exists():
                    target = target.with_name(f"{target.stem}_{rel.parent.name}{target.suffix}")
                shutil.move(str(p), str(target))
            moved += 1

    print(f"\n{moved} file(s) {'would move' if args.dry_run else 'moved'} to archive/weak_renders/")
    if not args.dry_run and moved:
        (DEST / "README.md").write_text(
            "# Weak renders — withdrawn from the submission\n\n"
            "These are matplotlib drawings that imitate photography: an aerial "
            "view built from coloured rectangles, eye-level views built from "
            "trapezoids and circles.\n\n"
            "They were withdrawn because the 3D Visualisations slot also holds "
            "photoreal renders of the same subjects, and placing the two side by "
            "side invites a comparison the drawings cannot win. Nothing here is "
            "deleted; if a drawing is wanted again it is intact.\n\n"
            "Genuine technical drawings — sections, elevations, planting plan, "
            "circulation and masterplan diagrams, presentation boards — were not "
            "touched. Those do a job a photograph cannot.\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
