"""Inline the spoken narration into the concept film.

WHY THIS EXISTS
---------------
The film needed a voice-over, and the obvious arrangement — four audio files
next to the HTML, loaded by `new Audio("narration/vo_01.wav")` — does not work
where it matters. Opened as a local file, which is how anyone actually opens
this, Chromium refuses the request outright:

    Access to audio at 'file:///.../vo_01.wav' from origin 'null' has been
    blocked by CORS policy

and even when a file does load, Web Audio will not let a graph tap a media
element it considers cross-origin, so `MediaRecorder` would have written sixty
seconds of silent pictures. A `data:` URI is same-origin, so it loads from a
local file and it can be recorded.

That also keeps the film a single standalone file, which is the same reason its
geometry is inlined by tools/sync_film.py rather than fetched.

WHAT IT DOES
------------
Reads `submission/12_Concept_Animation_Video/narration/vo_0*.wav`, base64-encodes
each, and writes them into the film between the GENERATED NARRATION markers.
Nothing outside those markers is touched, so hand-authored scene and camera code
survives — the same contract tools/sync_film.py works to.

The WAVs are 24 kHz mono: speech quality, a quarter of the bytes of the 48 kHz
stereo the voice was generated at. They are produced from the source clips in
`narration/vo_0*.mp4`.

    python tools/embed_narration.py
"""

from __future__ import annotations

import base64
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILM = ROOT / "submission" / "12_Concept_Animation_Video" / "concept_film.html"
VOICE = FILM.parent / "narration"

START = "  // ===== GENERATED NARRATION — python tools/embed_narration.py ====="
END = "  // ===== END GENERATED NARRATION ====="


def main() -> int:
    if not FILM.exists():
        print(f"  [X] no film at {FILM}")
        return 1

    clips = sorted(VOICE.glob("vo_0*.wav"))
    if not clips:
        print(f"  [X] no vo_0*.wav in {VOICE}")
        print("      Generate the voice first, then convert it to 24 kHz mono WAV.")
        return 1

    print("=" * 74)
    print("  EMBEDDING NARRATION into the concept film")
    print("=" * 74)

    entries, total = [], 0
    for c in clips:
        raw = c.read_bytes()
        total += len(raw)
        b64 = base64.b64encode(raw).decode("ascii")
        entries.append(f'    "data:audio/wav;base64,{b64}",')
        print(f"  {c.name:12} {len(raw)/1024:7.0f} KB  ->  {len(b64)/1024:7.0f} KB base64")

    block = "\n".join([START,
                       "  const VO_DATA = [",
                       *entries,
                       "  ];",
                       END])

    text = FILM.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    if not pattern.search(text):
        print("  [X] markers not found in the film — cannot embed safely")
        return 1

    before = len(text)
    text = pattern.sub(lambda _m: block, text, count=1)
    FILM.write_text(text, encoding="utf-8")

    print("")
    print(f"  {len(clips)} clip(s), {total/1024:.0f} KB of audio")
    print(f"  film {before/1024:.0f} KB -> {len(text)/1024:.0f} KB")
    print("=" * 74)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
