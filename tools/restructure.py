"""
One-time repository restructure.

Moves the project from a phase-numbered working folder into a conventional
repository layout. Nothing is deleted — every file is moved, and the complete
before/after map is written to MIGRATION_MAP.md.

    python tools/restructure.py --dry-run    show what would move
    python tools/restructure.py              do it

The one editorial judgement in here: the 55 Python scripts whose only job was to
typeset PDFs and Word documents move to archive/. They still run, and the
documents they produced are kept, but they no longer sit alongside the analysis
code. Python in this project should read as "computation on data", and 55 of the
94 scripts saying otherwise was the loudest problem with the old layout.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (source, destination). Directories move whole.
MOVES: list[tuple[str, str]] = [
    # The 12 official submission files get their own top-level home.
    ("10_PHASE10_UPLOAD_DOCUMENTS/10.2_Required_Files", "submission"),

    # Final written reports and key visuals stay first-class.
    ("_FINAL_DELIVERABLES/01_All_Phase_Reports", "reports/pdf"),
    ("_FINAL_DELIVERABLES/01_All_Phase_Reports_EDITABLE_DOCX", "reports/editable_docx"),
    ("_FINAL_DELIVERABLES/02_Key_Visuals", "design/visuals"),
    ("_FINAL_DELIVERABLES/03_Submission_Package", "reports/submission_package"),
    ("_FINAL_DELIVERABLES/EASY_UNDERSTANDING_GUIDE.pdf", "reports/EASY_UNDERSTANDING_GUIDE.pdf"),
    ("_FINAL_DELIVERABLES/EASY_UNDERSTANDING_GUIDE.docx", "reports/EASY_UNDERSTANDING_GUIDE.docx"),
    ("_FINAL_DELIVERABLES/PROJECT_METHODOLOGY_ROADMAP.pdf", "reports/PROJECT_METHODOLOGY_ROADMAP.pdf"),
    ("_FINAL_DELIVERABLES/PROJECT_METHODOLOGY_ROADMAP.docx", "reports/PROJECT_METHODOLOGY_ROADMAP.docx"),
    ("_FINAL_DELIVERABLES/AL_SAFA_2_PARK_MASTER_ALL_IN_ONE.pdf", "reports/AL_SAFA_2_PARK_MASTER_ALL_IN_ONE.pdf"),

    # Renders and boards.
    ("09_PHASE9_AI_WORKFLOW_AND_VISUALIZATION/9.7_Renderings", "design/renders"),
    ("09_PHASE9_AI_WORKFLOW_AND_VISUALIZATION/9.9_Presentation_Graphics", "design/boards"),

    # Source documents from Dubai Municipality.
    ("99_SOURCE_FILES", "archive/source_files"),

    # The offline portal — index.html and _PORTAL move together so the
    # relative paths between them keep working.
    ("_PORTAL", "archive/portal/_PORTAL"),
    ("index.html", "archive/portal/index.html"),

    # Phase working folders, including their _scripts/ typesetters.
    ("00_MASTER_TRACKER", "archive/phases/00_MASTER_TRACKER"),
    ("01_PHASE1_EXISTING_PARK", "archive/phases/01_PHASE1_EXISTING_PARK"),
    ("02_PHASE2_PROBLEM_DEFINITION", "archive/phases/02_PHASE2_PROBLEM_DEFINITION"),
    ("03_PHASE3_OPPORTUNITY_AND_OBJECTIVES", "archive/phases/03_PHASE3_OPPORTUNITY_AND_OBJECTIVES"),
    ("04_PHASE4_CONCEPT_DEVELOPMENT", "archive/phases/04_PHASE4_CONCEPT_DEVELOPMENT"),
    ("05_PHASE5_MASTERPLAN_DEVELOPMENT", "archive/phases/05_PHASE5_MASTERPLAN_DEVELOPMENT"),
    ("06_PHASE6_DETAILED_DESIGN", "archive/phases/06_PHASE6_DETAILED_DESIGN"),
    ("07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY", "archive/phases/07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY"),
    ("08_PHASE8_USER_EXPERIENCE_AND_ACTIVATION", "archive/phases/08_PHASE8_USER_EXPERIENCE_AND_ACTIVATION"),
    ("09_PHASE9_AI_WORKFLOW_AND_VISUALIZATION", "archive/phases/09_PHASE9_AI_WORKFLOW_AND_VISUALIZATION"),
    ("10_PHASE10_UPLOAD_DOCUMENTS", "archive/phases/10_PHASE10_UPLOAD_DOCUMENTS"),
    ("_FINAL_DELIVERABLES", "archive/final_deliverables"),
    ("PDF_ONLY_DELIVERABLES", "archive/pdf_only_deliverables"),

    # Superseded analysis and its outputs.
    ("ADVANCED_ANALYSIS_OUTPUTS", "archive/legacy_outputs"),
    ("ADVANCED_DATASET_ANALYSIS.py", "archive/legacy_scripts/ADVANCED_DATASET_ANALYSIS.py"),
    ("gen_pdf_advanced_dataset_analysis.py", "archive/legacy_scripts/gen_pdf_advanced_dataset_analysis.py"),
    ("gen_pdf_winning_competition_package.py", "archive/legacy_scripts/gen_pdf_winning_competition_package.py"),
    ("START_HERE.md", "archive/START_HERE_superseded.md"),
]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    log: list[str] = []
    moved = skipped = 0

    for src_rel, dst_rel in MOVES:
        src, dst = ROOT / src_rel, ROOT / dst_rel
        if not src.exists():
            log.append(f"| `{src_rel}` | — | not present, skipped |")
            skipped += 1
            continue
        if dst.exists():
            log.append(f"| `{src_rel}` | `{dst_rel}` | destination exists, skipped |")
            skipped += 1
            continue

        n = len(list(src.rglob("*"))) if src.is_dir() else 1
        print(f"  {src_rel}  ->  {dst_rel}   ({n} items)")
        if not args.dry_run:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))
        log.append(f"| `{src_rel}` | `{dst_rel}` | {n} items |")
        moved += 1

    print(f"\n{moved} moved, {skipped} skipped"
          f"{'  (dry run — nothing changed)' if args.dry_run else ''}")

    if not args.dry_run:
        (ROOT / "MIGRATION_MAP.md").write_text(
            "# Migration map\n\n"
            "Where everything went when the project was restructured into a "
            "repository layout. **Nothing was deleted** — every path below was "
            "moved, not removed.\n\n"
            "Run `python tools/restructure.py --dry-run` to see the rules that "
            "produced this.\n\n"
            "| Was | Is now | Contents |\n|---|---|---|\n" + "\n".join(log) + "\n",
            encoding="utf-8",
        )
        print("wrote MIGRATION_MAP.md")


if __name__ == "__main__":
    main()
