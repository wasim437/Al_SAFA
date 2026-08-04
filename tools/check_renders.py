"""Check generated renders before they go anywhere near the submission.

WHY THIS EXISTS
---------------
Six earlier renders of this project were generated, accepted, put into the
boards, and then withdrawn — every one of them showed a different park. A
straight corridor. An S-curve. A lagoon. They were withdrawn because a render
that contradicts the drawings is worse than no render: it tells a juror the
applicant does not know their own scheme.

This catches the mechanical failures — wrong filename, wrong folder, too small
to print, wrong shape, a file that is not really an image. It cannot see
whether the canopy is an arc. That is the ten-point test in
AL_SAFA_MASTER_PROMPT.md Section D, and it needs eyes.

    python tools/check_renders.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RENDERS = ROOT / "design" / "renders"

# The six the pipeline reads by name. src/boards.py looks for these exact
# paths, so a file that is merely "in the right folder" is not enough.
EXPECTED = [
    ("Aerial/masterplan_aerial_golden_hour.jpg",
     "Aerial over the whole park — deliverable 12", "HIGHEST"),
    ("Night/night_plaza_render_1784970565232.jpg",
     "Night plaza — deliverable 13 cannot be met without this", "HIGH"),
    ("Eye_Level/spine_corridor_interior.jpg",
     "Eye level beneath the crescent — deliverable 12, human scale", "HIGH"),
    ("Eye_Level/oasis_basin.jpg",
     "Al Nakhil, the sunken palm court", "NICE"),
    ("Day/childrens_dune_play.jpg",
     "Children's Dune Play", "NICE"),
    ("Day/souk_plaza.jpg",
     "Souk kiosks and community plaza", "NICE"),
]

MIN_PIXELS = 1_200_000        # ~1400x860. Below this it prints soft on a board.
MIN_EDGE = 900


def main() -> int:
    print("=" * 78)
    print("  RENDER CHECK — mechanical faults only. The ten-point test needs eyes.")
    print("=" * 78)

    try:
        from PIL import Image
    except ImportError:
        print("  [X] Pillow not installed — pip install -r requirements.txt")
        return 1

    found = sorted(p for p in RENDERS.rglob("*")
                   if p.is_file() and p.suffix.lower() in
                   (".jpg", ".jpeg", ".png", ".webp"))
    expected_paths = {RENDERS / rel for rel, _, _ in EXPECTED}

    problems = 0
    have = 0
    for rel, what, weight in EXPECTED:
        p = RENDERS / rel
        if not p.exists():
            print(f"  [ ]  MISSING  {weight:<8} {rel}")
            print(f"           {what}")
            continue
        have += 1
        try:
            with Image.open(p) as im:
                w, h = im.size
                mode = im.mode
        except Exception as e:
            print(f"  [X]  BROKEN   {rel} — not a readable image ({e})")
            problems += 1
            continue

        notes = []
        if w * h < MIN_PIXELS or min(w, h) < MIN_EDGE:
            notes.append(f"too small to print ({w}x{h})")
        if mode not in ("RGB", "L"):
            notes.append(f"colour mode {mode} — flatten to RGB")
        mb = p.stat().st_size / 1e6
        if mb > 12:
            notes.append(f"{mb:.1f} MB — heavier than the boards need")

        if notes:
            print(f"  [!]  {rel}  {w}x{h}  {mb:.1f} MB")
            for n in notes:
                print(f"           - {n}")
            problems += 1
        else:
            print(f"  [ok] {rel}  {w}x{h}  {mb:.1f} MB")

    stray = [p for p in found if p not in expected_paths]
    if stray:
        print("")
        print("  Files in design/renders/ that the pipeline will IGNORE —")
        print("  src/boards.py reads by exact name, so rename these:")
        for p in stray:
            print(f"    {p.relative_to(RENDERS)}")
        problems += len(stray)

    print("")
    print(f"  {have} of {len(EXPECTED)} expected renders present")
    if have == 0:
        print("  Nothing to check yet. Generate from AL_SAFA_MASTER_PROMPT.md "
              "Section C.")
    else:
        print("")
        print("  NOW DO THE PART THIS SCRIPT CANNOT DO — for each image ask:")
        for i, q in enumerate([
                "Is the canopy ONE continuous arc? (not straight, not S, not a ring)",
                "Does it bow convex SOUTH — midpoint further south than the ends?",
                "Is the water a narrow channel you could step across, not a lagoon?",
                "Is the water on the canopy's NORTHERN edge?",
                "Is the light through the soffit dappled, not solid black?",
                "Are all trees desert species? (no jungle, no green lawn)",
                "Does the park fill the frame? (no roads, cars, villas, skyline)",
                "Real people, mixed ages, actually using it?",
                "Canopy ~18 m wide, 4.5 m high, over a 7 m walk?",
                "Would a juror comparing it with figures/fig10_masterplan.png "
                "see THE SAME PARK?"], 1):
            print(f"    {i:>2}. {q}")
        print("")
        print("  Question 10 is the one that matters. It is the test the six "
              "withdrawn renders failed.")
    print("=" * 78)
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
