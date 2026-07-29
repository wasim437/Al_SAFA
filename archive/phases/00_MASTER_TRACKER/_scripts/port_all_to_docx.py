"""
Bulk-port every remaining gen_pdf_*.py report generator to the .docx pipeline.

WHY: the user wants report TEXT to live in directly-editable Word files rather
than inside Python code. Rather than hand-rewrite ~20 near-identical scripts,
this reads each existing gen_pdf_*.py, rewrites the few lines that differ
(import, builder call, output extension, HTML entities), and writes a sibling
gen_docx_*.py. Then it runs each one.

The section CONTENT is copied verbatim - this is a mechanical format port, so
no analysis text, number, or table value changes.
"""

import os
import re
import subprocess
import sys

PROJECT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# (script path relative to PROJECT, already-ported?)
# NOTE: gen_docx_00..10 for Phase 1 were already ported by an earlier pass and
# are intentionally excluded here so their work isn't overwritten. Only the
# genuinely-missing ones are listed.
TARGETS = [
    "01_PHASE1_EXISTING_PARK/_scripts/gen_pdf_11_swot.py",
    "01_PHASE1_EXISTING_PARK/_scripts/gen_pdf_12_ai_analysis.py",
    "01_PHASE1_EXISTING_PARK/_scripts/gen_pdf_13_catchment.py",
    "04_PHASE4_CONCEPT_DEVELOPMENT/_scripts/gen_pdf_phase4.py",
    "05_PHASE5_MASTERPLAN_DEVELOPMENT/_scripts/gen_pdf_phase5.py",
    "06_PHASE6_DETAILED_DESIGN/_scripts/gen_pdf_phase6.py",
    "07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/_scripts/gen_pdf_phase7.py",
    "08_PHASE8_USER_EXPERIENCE_AND_ACTIVATION/_scripts/gen_pdf_phase8.py",
    "09_PHASE9_AI_WORKFLOW_AND_VISUALIZATION/_scripts/gen_pdf_phase9.py",
    "00_MASTER_TRACKER/_scripts/gen_pdf_easy_understanding.py",
    "00_MASTER_TRACKER/_scripts/gen_pdf_roadmap.py",
    "10_PHASE10_UPLOAD_DOCUMENTS/_scripts/02_complete_design_report.py",
    "10_PHASE10_UPLOAD_DOCUMENTS/_scripts/03_animation_storyboard.py",
    "10_PHASE10_UPLOAD_DOCUMENTS/_scripts/04_submission_checklist.py",
]

# HTML entities that the old ReportLab pipeline needed -> plain unicode for Word
ENTITY_MAP = {
    "&#176;": "°",   # degree
    "&ge;": "≥",
    "&le;": "≤",
    "&amp;": "&",
    "&rsquo;": "'",
    "&lsquo;": "'",
    "&ndash;": "–",
    "&mdash;": "—",
    "&hellip;": "…",
    "&nbsp;": " ",
    "&deg;": "°",
}


def port(src_rel):
    src = os.path.join(PROJECT, src_rel)
    if not os.path.exists(src):
        return ("MISSING", src_rel, "source not found")

    with open(src, "r", encoding="utf-8") as f:
        code = f.read()

    if "build_report" not in code:
        return ("SKIP", src_rel, "no build_report() call - not a report generator")

    # 1. swap the builder import
    code = code.replace(
        "from report_builder import build_report",
        "from docx_report_builder import build_docx_report, convert_docx_to_pdf",
    )

    # 2. entities -> unicode
    for ent, ch in ENTITY_MAP.items():
        code = code.replace(ent, ch)

    # 3. build_report( -> docx_path = build_docx_report(
    code = re.sub(r"\bbuild_report\(", "docx_path = build_docx_report(", code, count=1)

    # 4. output_path .pdf -> .docx
    code = re.sub(r'(output_path\s*=\s*os\.path\.join\([^)]*?)\.pdf"', r'\1.docx"', code)

    # 5. append the PDF conversion after the build call.
    #    Find the closing paren of the build_docx_report(...) call and insert after.
    idx = code.find("docx_path = build_docx_report(")
    if idx != -1:
        depth = 0
        end = None
        for i in range(code.find("(", idx), len(code)):
            if code[i] == "(":
                depth += 1
            elif code[i] == ")":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        if end:
            code = code[:end] + "\nconvert_docx_to_pdf(docx_path)" + code[end:]

    dst_rel = src_rel.replace("gen_pdf_", "gen_docx_")
    if "gen_docx_" not in dst_rel:  # phase-10 scripts don't use the gen_pdf_ prefix
        d, fn = os.path.split(dst_rel)
        dst_rel = os.path.join(d, "docx_" + fn)
    dst = os.path.join(PROJECT, dst_rel)

    with open(dst, "w", encoding="utf-8") as f:
        f.write(code)

    return ("WROTE", dst_rel, "")


def run(script_rel):
    script = os.path.join(PROJECT, script_rel)
    cwd = os.path.dirname(script)
    try:
        r = subprocess.run([sys.executable, os.path.basename(script)],
                           cwd=cwd, capture_output=True, text=True, timeout=300)
        out = (r.stdout or "") + (r.stderr or "")
        ok = "Saved DOCX" in out
        pdf = "Saved PDF" in out
        if ok and pdf:
            return ("PASS", "docx+pdf")
        if ok:
            return ("PARTIAL", "docx only (pdf convert failed)")
        tail = out.strip().splitlines()[-3:] if out.strip() else ["no output"]
        return ("FAIL", " | ".join(tail))
    except subprocess.TimeoutExpired:
        return ("TIMEOUT", "exceeded 300s")
    except Exception as e:
        return ("ERROR", str(e)[:200])


if __name__ == "__main__":
    print("=" * 72)
    print("BULK PORT: gen_pdf_*.py  ->  .docx pipeline")
    print("=" * 72)

    written = []
    for t in TARGETS:
        status, rel, note = port(t)
        print(f"[{status:8}] {rel}" + (f"  ({note})" if note else ""))
        if status == "WROTE":
            written.append(rel)

    print()
    print("=" * 72)
    print(f"RUNNING {len(written)} ported scripts")
    print("=" * 72)

    results = {}
    for rel in written:
        status, note = run(rel)
        results[rel] = (status, note)
        print(f"[{status:8}] {rel}  {note}")

    print()
    print("=" * 72)
    print("SUMMARY")
    print("=" * 72)
    from collections import Counter
    c = Counter(s for s, _ in results.values())
    for k, v in c.items():
        print(f"  {k}: {v}")
    fails = {k: v for k, v in results.items() if v[0] not in ("PASS",)}
    if fails:
        print("\n  NEEDS ATTENTION:")
        for k, (s, n) in fails.items():
            print(f"    [{s}] {k}: {n}")
