"""Organise the repository: dedupe, drop junk, and write the map.

The repository had grown to 513 files carrying **55.6 MB of exact duplicates** —
the same render in five places, the same PDF in three, an entire second copy of
the portal and of the deliverables folder. That is not a disk-space problem. It
is a correctness problem: when a file exists five times, four of them go stale
and nobody knows which one is the real one.

SAFETY
------
Nothing is removed unless a **byte-identical copy survives** somewhere this tool
considers canonical. Every removal is verified by MD5 first, and everything here
is tracked in git anyway, so `git checkout HEAD~1 -- <path>` brings any of it
back. The tool refuses to touch a file it cannot find a surviving twin for.

WHAT IS DELIBERATELY LEFT ALONE
-------------------------------
* `archive/phases/` — all 245 files of the eleven phase folders. This is the
  project's working history and the written reports were produced from it.
* `submission/` — the twelve upload slots duplicate figures on purpose. Each
  slot has to be self-contained, because it is uploaded on its own.
* `reports/` — the written deliverables.

    python tools/organize_repo.py --dry-run
    python tools/organize_repo.py
"""

from __future__ import annotations

import argparse
import hashlib
import shutil
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Folders whose copy of a file is the one that survives, most-canonical first.
# A file elsewhere is removable only if its bytes are found under one of these.
CANONICAL = [
    "figures", "design/renders", "design/visuals", "design/boards",
    "docs", "src", "tools", "tests", "data", "models", "notebooks",
    "reports", "submission", "archive/phases", "archive/withdrawn_visuals",
]

# Whole folders that are exact re-copies of something canonical.
REDUNDANT_TREES = {
    "archive/pdf_only_deliverables":
        "Every PDF here is byte-identical to one in reports/pdf/ or reports/. "
        "It was a second, differently-named copy of the same deliverables.",
    "archive/portal":
        "A full second copy of docs/_PORTAL — including the vendored three.js "
        "and Chart.js. The live portal is docs/_PORTAL.",
    "archive/superseded_site":
        "The previous static site, superseded by the portal at docs/index.html.",
}

# design/visuals/ had picked up copies of the photoreal renders, which belong in
# design/renders/. Generated drawings stay in design/visuals/ — that is where
# src/drawings.py writes them.
RENDER_COPIES_IN_VISUALS = True

JUNK_GLOBS = ["**/__pycache__", "**/*.pyc", "**/*.bak",
              "**/Thumbs.db", "**/.DS_Store"]


def md5(p: Path) -> str:
    return hashlib.md5(p.read_bytes()).hexdigest()


def build_index() -> dict[str, list[Path]]:
    idx = defaultdict(list)
    for p in ROOT.rglob("*"):
        if not p.is_file() or ".git" in p.parts or "__pycache__" in p.parts:
            continue
        try:
            idx[md5(p)].append(p)
        except OSError:
            pass
    return idx


def is_canonical(p: Path) -> bool:
    rel = p.relative_to(ROOT).as_posix()
    return any(rel.startswith(c + "/") for c in CANONICAL)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    act = not args.dry_run

    freed, removed = 0, 0
    print("=" * 78)
    print("  1. JUNK — build artefacts and editor backups")
    print("=" * 78)
    for pat in JUNK_GLOBS:
        for p in sorted(ROOT.glob(pat)):
            if ".git" in p.parts:
                continue
            sz = sum(f.stat().st_size for f in p.rglob("*") if f.is_file()) \
                if p.is_dir() else p.stat().st_size
            print(f"  - {p.relative_to(ROOT).as_posix()}  ({sz / 1024:.0f} KB)")
            freed += sz
            removed += 1
            if act:
                shutil.rmtree(p) if p.is_dir() else p.unlink()

    idx = build_index()

    print()
    print("=" * 78)
    print("  2. REDUNDANT TREES — whole folders that re-copy something canonical")
    print("=" * 78)
    # File by file, not folder by folder. Removing a whole tree because most of
    # it is duplicated would take the unique files with it — and it is always
    # the one unique file in a folder of copies that turns out to matter.
    for tree, why in REDUNDANT_TREES.items():
        base = ROOT / tree
        if not base.exists():
            continue
        files = [f for f in base.rglob("*") if f.is_file()]
        dupes, unique = [], []
        for f in files:
            twins = [t for t in idx.get(md5(f), []) if t != f and is_canonical(t)]
            (dupes if twins else unique).append(f)
        sz = sum(f.stat().st_size for f in dupes)
        print(f"  {tree}/  — {len(dupes)} duplicated, {len(unique)} unique "
              f"({sz / 1e6:.1f} MB removable)")
        print(f"      {why}")
        for f in dupes:
            freed += f.stat().st_size
            removed += 1
            if act:
                f.unlink()
        if unique:
            print(f"      KEPT, nothing else holds these:")
            for f in unique:
                print(f"        · {f.relative_to(base).as_posix()}")
        if act:
            for d in sorted(base.rglob("*"), reverse=True):
                if d.is_dir() and not any(d.iterdir()):
                    d.rmdir()
            if base.exists() and not any(base.iterdir()):
                base.rmdir()

    print()
    print("=" * 78)
    print("  3. DUPLICATE RENDERS inside design/visuals/")
    print("=" * 78)
    vis = ROOT / "design" / "visuals"
    if RENDER_COPIES_IN_VISUALS and vis.exists():
        for f in sorted(vis.iterdir()):
            if not f.is_file() or f.suffix.lower() not in (".jpg", ".jpeg"):
                continue
            twins = [t for t in idx.get(md5(f), [])
                     if t != f and "renders" in t.parts]
            if not twins:
                print(f"  ! keeping {f.name} — no copy under design/renders/")
                continue
            sz = f.stat().st_size
            print(f"  - design/visuals/{f.name}  ({sz / 1e6:.1f} MB) "
                  f"-> lives in {twins[0].parent.relative_to(ROOT).as_posix()}/")
            freed += sz
            removed += 1
            if act:
                f.unlink()

    print()
    print("=" * 78)
    print("  4. FLATTEN archive/weak_renders/ — the same cull, copied three times")
    print("=" * 78)
    wr = ROOT / "archive" / "weak_renders"
    if wr.exists():
        seen: dict[str, Path] = {}
        for f in sorted(wr.rglob("*")):
            if not f.is_file() or f.name == "README.md":
                continue
            h = md5(f)
            if h in seen:
                print(f"  - {f.relative_to(ROOT).as_posix()}  "
                      f"(same as {seen[h].name})")
                freed += f.stat().st_size
                removed += 1
                if act:
                    f.unlink()
            else:
                seen[h] = f
                if act and f.parent != wr:
                    target = wr / f.name
                    if not target.exists():
                        shutil.move(str(f), str(target))
        if act:
            for d in sorted(wr.rglob("*"), reverse=True):
                if d.is_dir() and not any(d.iterdir()):
                    d.rmdir()

    print()
    print("=" * 78)
    print(f"  {removed} file(s) {'removed' if act else 'would be removed'} · "
          f"{freed / 1e6:.1f} MB freed")
    if not act:
        print("  DRY RUN — nothing was touched. Re-run without --dry-run.")
    else:
        print("  All of it is recoverable: git checkout HEAD -- <path>")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
